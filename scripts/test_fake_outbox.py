import unittest

try:
    from fake_outbox import FakeOutboxStore, OutboxConflict, StaleLease
except ModuleNotFoundError:
    from scripts.fake_outbox import FakeOutboxStore, OutboxConflict, StaleLease


class FakeOutboxTests(unittest.TestCase):
    def setUp(self):
        self.store = FakeOutboxStore()
        self.store.reserve("effect-1", "attempt-1", "sha256:abc", b'{"x":1}')

    def test_reservation_and_outbox_intent_are_created_together(self):
        record = self.store.get("effect-1")
        self.assertEqual(record.state, "pending")
        self.assertEqual(record.reservation.sequence, 1)

    def test_crash_before_commit_leaves_no_partial_reservation_or_sequence(self):
        with self.assertRaises(RuntimeError):
            self.store.reserve("effect-2", "attempt-2", "sha256:def", b'{"y":2}', fail_before_commit=True)
        self.assertEqual(len(self.store.records), 1)
        got = self.store.reserve("effect-2", "attempt-2", "sha256:def", b'{"y":2}')
        self.assertEqual(got.sequence, 2)

    def test_exact_reservation_is_idempotent(self):
        first = self.store.get("effect-1").reservation
        second = self.store.reserve("effect-1", "attempt-1", "sha256:abc", b'{"x":1}')
        self.assertEqual(first, second)
        self.assertEqual(len(self.store.records), 1)

    def test_effect_id_new_attempt_requires_terminal_and_explicit_authorization(self):
        with self.assertRaises(OutboxConflict):
            self.store.reserve("effect-1", "attempt-2", "sha256:abc", b'{"x":1}', new_attempt_authorized=True)
        self.store.mark_terminal("effect-1")
        with self.assertRaises(OutboxConflict):
            self.store.reserve("effect-1", "attempt-2", "sha256:abc", b'{"x":1}')
        new = self.store.reserve("effect-1", "attempt-2", "sha256:abc", b'{"x":1}', new_attempt_authorized=True)
        self.assertEqual(new.effect_id, "effect-1")
        self.assertEqual(new.attempt_id, "attempt-2")
        self.assertEqual(self.store.get("effect-1").reservation.attempt_id, "attempt-2")

    def test_attempt_identity_cannot_be_reused_for_changed_request(self):
        with self.assertRaises(OutboxConflict):
            self.store.reserve("effect-1", "attempt-1", "sha256:changed", b'{"x":2}')

    def test_crash_before_send_can_be_reclaimed(self):
        lease = self.store.claim("effect-1", "worker-A", now=10, lease_seconds=5)
        self.assertEqual(self.store.recover_expired("effect-1", now=15), "safe_to_reclaim_before_send")
        next_lease = self.store.claim("effect-1", "worker-B", now=15, lease_seconds=5)
        self.assertGreater(next_lease.fence, lease.fence)

    def test_active_lease_cannot_be_stolen(self):
        self.store.claim("effect-1", "worker-A", now=10, lease_seconds=10)
        with self.assertRaises(OutboxConflict):
            self.store.claim("effect-1", "worker-B", now=19, lease_seconds=10)

    def test_stale_worker_is_fenced_after_reclaim(self):
        old = self.store.claim("effect-1", "worker-A", now=0, lease_seconds=5)
        self.store.recover_expired("effect-1", now=5)
        self.store.claim("effect-1", "worker-B", now=5, lease_seconds=5)
        with self.assertRaises(StaleLease):
            self.store.mark_dispatching(old, now=5)

    def test_crash_after_dispatch_intent_requires_reconciliation(self):
        lease = self.store.claim("effect-1", "worker-A", now=0, lease_seconds=5)
        self.store.mark_dispatching(lease, now=1)
        self.assertEqual(self.store.recover_expired("effect-1", now=5), "reconcile_before_any_retry")
        with self.assertRaises(OutboxConflict):
            self.store.claim("effect-1", "worker-B", now=5, lease_seconds=5)

    def test_lost_ack_found_reconciles_without_second_dispatch(self):
        lease = self.store.claim("effect-1", "worker-A", now=0, lease_seconds=5)
        self.store.mark_dispatching(lease, now=1)
        self.store.recover_expired("effect-1", now=5)
        result = self.store.resolve_reconciliation(
            "effect-1", outcome="found", exact_identity_match=True,
            authoritative=True, provider_reference="provider-op-9",
        )
        self.assertEqual(result, "adopt_existing")
        self.assertEqual(self.store.get("effect-1").state, "acknowledged")

    def test_eventually_consistent_not_found_holds_unknown(self):
        lease = self.store.claim("effect-1", "worker-A", now=0, lease_seconds=5)
        self.store.mark_dispatching(lease, now=1)
        self.store.recover_expired("effect-1", now=5)
        result = self.store.resolve_reconciliation(
            "effect-1", outcome="not_found", exact_identity_match=True,
            authoritative=True, absence_final=False,
        )
        self.assertEqual(result, "hold_unknown")
        self.assertEqual(self.store.get("effect-1").state, "reconciling")

    def test_final_exact_absence_allows_same_attempt_retry(self):
        lease = self.store.claim("effect-1", "worker-A", now=0, lease_seconds=5)
        self.store.mark_dispatching(lease, now=1)
        self.store.recover_expired("effect-1", now=5)
        result = self.store.resolve_reconciliation(
            "effect-1", outcome="not_found", exact_identity_match=True,
            authoritative=True, absence_final=True,
        )
        self.assertEqual(result, "safe_to_retry_same_attempt")
        self.assertEqual(self.store.get("effect-1").state, "pending")
        self.assertEqual(self.store.get("effect-1").reservation.attempt_id, "attempt-1")

    def test_non_authoritative_or_wrong_identity_cannot_release_hold(self):
        lease = self.store.claim("effect-1", "worker-A", now=0, lease_seconds=5)
        self.store.mark_dispatching(lease, now=1)
        self.store.recover_expired("effect-1", now=5)
        for exact, authoritative in ((False, True), (True, False)):
            self.assertEqual(self.store.resolve_reconciliation(
                "effect-1", outcome="not_found", exact_identity_match=exact,
                authoritative=authoritative, absence_final=True,
            ), "hold_unknown")

    def test_duplicate_delivery_is_deduplicated(self):
        first = self.store.consume("effect-1", "sha256:abc", "provider-op-1")
        second = self.store.consume("effect-1", "sha256:abc", "provider-op-duplicate")
        self.assertEqual(first.disposition, "accepted")
        self.assertEqual(second.disposition, "duplicate")
        self.assertEqual(second.provider_reference, "provider-op-1")

    def test_same_effect_with_changed_fingerprint_is_conflict(self):
        self.store.consume("effect-1", "sha256:abc", "provider-op-1")
        result = self.store.consume("effect-1", "sha256:changed", "provider-op-2")
        self.assertEqual(result.disposition, "conflict")

    def test_invalid_time_and_lease_types_are_rejected(self):
        for now, lease_seconds in ((True, 5), (0, True), (-1, 5), (0, 0), (0, "5")):
            with self.subTest(now=now, lease_seconds=lease_seconds):
                with self.assertRaises(ValueError):
                    self.store.claim("effect-1", "worker-A", now=now, lease_seconds=lease_seconds)

    def test_expired_acknowledgement_is_rejected(self):
        lease = self.store.claim("effect-1", "worker-A", now=0, lease_seconds=5)
        self.store.mark_dispatching(lease, now=1)
        with self.assertRaises(StaleLease):
            self.store.acknowledge(lease, "provider-op-1", now=5)

    def test_reconciled_found_result_cannot_be_claimed_for_a_second_dispatch(self):
        lease = self.store.claim("effect-1", "worker-A", now=0, lease_seconds=5)
        self.store.mark_dispatching(lease, now=1)
        self.store.recover_expired("effect-1", now=5)
        self.store.resolve_reconciliation(
            "effect-1", outcome="found", exact_identity_match=True,
            authoritative=True, provider_reference="provider-op-1",
        )
        with self.assertRaises(OutboxConflict):
            self.store.claim("effect-1", "worker-B", now=6, lease_seconds=5)

    def test_reservation_persists_creation_timestamp_for_recovery(self):
        reservation = self.store.reserve(
            "effect-time", "attempt-time", "sha256:t", b'{"t":1}', created_at_ms=123,
        )
        self.assertEqual(reservation.created_at_ms, 123)
        replay = self.store.reserve(
            "effect-time", "attempt-time", "sha256:t", b'{"t":1}', created_at_ms=999,
        )
        self.assertEqual(replay.created_at_ms, 123)

    def test_acknowledgement_persists_observation_timestamp(self):
        lease = self.store.claim("effect-1", "worker-A", now=10, lease_seconds=20)
        self.store.mark_dispatching(lease, now=11)
        self.store.acknowledge(lease, "provider-time", now=12)
        self.assertEqual(self.store.get("effect-1").acknowledged_at, 12)

    def test_reconciliation_found_persists_observation_time(self):
        lease = self.store.claim("effect-1", "worker", now=1, lease_seconds=2)
        self.store.mark_dispatching(lease, now=2)
        self.store.recover_expired("effect-1", now=3)
        self.assertEqual(self.store.resolve_reconciliation(
            "effect-1", outcome="found", exact_identity_match=True,
            authoritative=True, provider_reference="provider-1", now=4,
        ), "adopt_existing")
        self.assertEqual(self.store.get("effect-1").acknowledged_at, 4)

    def test_acknowledgement_requires_current_dispatch_lease(self):
        lease = self.store.claim("effect-1", "worker-A", now=0, lease_seconds=5)
        self.store.mark_dispatching(lease, now=1)
        self.store.acknowledge(lease, "provider-op-1", now=2)
        self.assertEqual(self.store.get("effect-1").state, "acknowledged")
        with self.assertRaises(StaleLease):
            self.store.acknowledge(lease, "provider-op-1", now=3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
