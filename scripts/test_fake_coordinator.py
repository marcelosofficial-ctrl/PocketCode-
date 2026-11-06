import unittest

try:
    from fake_coordinator import FakeCoordinator
    from fake_outbox import FakeOutboxStore, OutboxConflict, StaleLease
    from event_journal import AuthenticatedProducer, EventJournal, JournalConflict
except ModuleNotFoundError:
    from scripts.fake_coordinator import FakeCoordinator
    from scripts.fake_outbox import FakeOutboxStore, OutboxConflict, StaleLease
    from scripts.event_journal import AuthenticatedProducer, EventJournal, JournalConflict


class FakeCoordinatorTests(unittest.TestCase):
    def setUp(self):
        self.store = FakeOutboxStore()
        self.journal = EventJournal(expected_audience="pocketcode")
        self.producer = AuthenticatedProducer(
            issuer="pocketcode.test", subject="coordinator-1",
            key_id="test-key-1", credential_fingerprint="sha256:test",
            audience="pocketcode", authorized_sources=("pocketcode.coordinator",),
        )
        self.coordinator = FakeCoordinator(
            store=self.store, journal=self.journal, producer=self.producer,
        )
        self.coordinator.reserve("effect-1", "attempt-1", "sha256:req",
                                 b'{"op":"build"}', at_ms=10)

    def dispatch(self, *, now=20, lease_seconds=10):
        lease = self.coordinator.claim("effect-1", "worker-A", now=now,
                                       lease_seconds=lease_seconds)
        self.coordinator.mark_dispatching(lease, now=now + 1)
        return lease

    def test_reservation_records_outbox_and_journal(self):
        self.assertEqual(self.store.get("effect-1").state, "pending")
        self.assertEqual(len(self.journal.events), 1)
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state, "reserved")

    def test_reservation_event_append_is_repaired_after_crash(self):
        with self.assertRaises(RuntimeError):
            self.coordinator.reserve("effect-2", "attempt-2", "sha256:req2",
                                     b'{"op":2}', at_ms=11,
                                     crash_after_store_commit=True)
        self.assertEqual(self.coordinator.repair_missing_reservation_event("effect-2"),
                         "accepted")
        self.assertEqual(self.coordinator.repair_missing_reservation_event("effect-2"),
                         "duplicate")

    def test_reservation_replay_is_idempotent(self):
        self.assertEqual(self.coordinator.reserve(
            "effect-1", "attempt-1", "sha256:req", b'{"op":"build"}', at_ms=10
        ), "duplicate")
        self.assertEqual(len(self.journal.events), 1)

    def test_claim_and_dispatch_intent_are_attempt_and_fence_bound(self):
        lease = self.dispatch()
        payloads = [e.payload for e in self.journal.events]
        self.assertTrue(any(b'"kind":"lease_claimed"' in p for p in payloads))
        self.assertTrue(any(b'"kind":"dispatch_intent"' in p for p in payloads))
        rebuilt = self.coordinator.rebuild_effect("effect-1")
        self.assertEqual(rebuilt.state, "dispatching")
        self.assertEqual(rebuilt.attempt_id, lease.attempt_id)

    def test_expired_pre_send_lease_is_safe_to_reclaim(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=5)
        self.assertEqual(self.coordinator.recover_expired("effect-1", now=25),
                         "safe_to_reclaim_before_send")
        newer = self.coordinator.claim("effect-1", "worker-B", now=25, lease_seconds=5)
        self.assertGreater(newer.fence, lease.fence)
        with self.assertRaises(StaleLease):
            self.coordinator.mark_dispatching(lease, now=25)

    def test_dispatch_intent_store_commit_without_event_is_visible_as_gap(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=5)
        with self.assertRaises(RuntimeError):
            self.coordinator.mark_dispatching(
                lease, now=21, crash_after_store_transition=True,
            )
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state,
                         "dispatch_intent_unjournaled")
        self.assertEqual(self.coordinator.recover_expired("effect-1", now=25),
                         "reconcile_before_any_retry")
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state,
                         "reconciliation_required")

    def test_expired_post_intent_requires_reconciliation(self):
        self.dispatch(now=20, lease_seconds=5)
        self.assertEqual(self.coordinator.recover_expired("effect-1", now=26),
                         "reconcile_before_any_retry")
        with self.assertRaises(OutboxConflict):
            self.coordinator.claim("effect-1", "worker-B", now=26, lease_seconds=5)

    def test_acknowledgement_is_rebuilt_from_journal(self):
        lease = self.dispatch()
        self.assertEqual(self.coordinator.acknowledge(lease, "provider-7", now=23),
                         "accepted")
        rebuilt = self.coordinator.rebuild_effect("effect-1")
        self.assertEqual(rebuilt.state, "acknowledged")
        self.assertEqual(rebuilt.provider_reference, "provider-7")

    def test_crash_after_outbox_ack_is_repaired_from_accepted_record(self):
        lease = self.dispatch()
        with self.assertRaises(RuntimeError):
            self.coordinator.acknowledge(
                lease, "provider-7", now=23, crash_after_store_transition=True,
            )
        self.assertEqual(self.store.get("effect-1").state, "acknowledged")
        self.assertEqual(self.coordinator.repair_missing_ack_event("effect-1"), "accepted")
        self.assertEqual(self.coordinator.repair_missing_ack_event("effect-1"), "duplicate")
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").provider_reference,
                         "provider-7")

    def test_stale_ack_cannot_become_journal_evidence(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=2)
        self.coordinator.mark_dispatching(lease, now=21)
        with self.assertRaises(StaleLease):
            self.coordinator.acknowledge(lease, "provider-7", now=22)
        self.assertFalse(any(b'"kind":"dispatch_acknowledged"' in e.payload
                             for e in self.journal.events))

    def test_projection_rebuild_is_deterministic(self):
        lease = self.dispatch()
        self.coordinator.acknowledge(lease, "provider-7", now=23)
        self.assertEqual(self.coordinator.rebuild_effect("effect-1"),
                         self.coordinator.rebuild_effect("effect-1"))

    def test_event_replay_does_not_add_second_accepted_event(self):
        lease = self.dispatch()
        before = len(self.journal.events)
        self.coordinator._append(
            kind="dispatch_intent", effect_id=lease.effect_id,
            attempt_id=lease.attempt_id,
            event_id=f"dispatch:{lease.effect_id}:{lease.attempt_id}:{lease.fence}",
            at_ms=21, fence=lease.fence,
        )
        self.assertEqual(len(self.journal.events), before)

    def test_wrong_audience_fails_closed(self):
        wrong = AuthenticatedProducer(
            issuer="other", subject="x", key_id="k", credential_fingerprint="f",
            audience="wrong", authorized_sources=("pocketcode.coordinator",),
        )
        coordinator = FakeCoordinator(
            store=FakeOutboxStore(), journal=self.journal, producer=wrong,
        )
        with self.assertRaises(JournalConflict):
            coordinator.reserve("effect-2", "attempt-2", "sha256:x", b"x", at_ms=1)

    def test_quarantined_conflicts_do_not_enter_rebuilt_projection(self):
        lease = self.dispatch()
        original = next(e for e in self.journal.events
                        if e.producer_event_id.startswith("dispatch:"))
        self.journal.append(
            producer=self.producer, source=original.source,
            event_id=original.producer_event_id, payload=b'{"kind":"forged"}',
            occurred_at_ms=21, observed_at_ms=21,
            effect_id=lease.effect_id, attempt_id=lease.attempt_id, fence=lease.fence,
        )
        self.assertEqual(len(self.journal.conflicts), 1)
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state,
                         "dispatching")


if __name__ == "__main__":
    unittest.main(verbosity=2)
