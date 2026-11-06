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

    def test_reconciliation_found_is_journaled_and_projected(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=2)
        self.coordinator.mark_dispatching(lease, now=21)
        self.assertEqual(self.coordinator.recover_expired("effect-1", now=22),
                         "reconcile_before_any_retry")
        self.assertEqual(self.coordinator.reconcile(
            "effect-1", outcome="found", exact_identity_match=True,
            authoritative=True, provider_reference="provider-9", now=23,
        ), "adopt_existing")
        rebuilt = self.coordinator.rebuild_effect("effect-1")
        self.assertEqual(rebuilt.state, "acknowledged")
        self.assertEqual(rebuilt.provider_reference, "provider-9")
        self.assertEqual(self.coordinator.repair_missing_ack_event("effect-1"), "duplicate")

    def test_final_absence_is_journaled_as_retry_authorization(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=2)
        self.coordinator.mark_dispatching(lease, now=21)
        self.coordinator.recover_expired("effect-1", now=22)
        self.assertEqual(self.coordinator.reconcile(
            "effect-1", outcome="not_found", exact_identity_match=True,
            authoritative=True, absence_final=True, now=23,
        ), "safe_to_retry_same_attempt")
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state,
                         "retry_authorized")

    def test_nonfinal_absence_does_not_authorize_retry_or_emit_event(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=2)
        self.coordinator.mark_dispatching(lease, now=21)
        self.coordinator.recover_expired("effect-1", now=22)
        before = len(self.journal.events)
        self.assertEqual(self.coordinator.reconcile(
            "effect-1", outcome="not_found", exact_identity_match=True,
            authoritative=True, absence_final=False, now=23,
        ), "hold_unknown")
        self.assertEqual(len(self.journal.events), before)
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state,
                         "reconciliation_required")

    def test_crash_after_final_absence_store_commit_is_visible_and_repairable(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=2)
        self.coordinator.mark_dispatching(lease, now=21)
        self.coordinator.recover_expired("effect-1", now=22)
        # Exercise the store commit separately to model a crash before journal append.
        self.store.resolve_reconciliation(
            "effect-1", outcome="not_found", exact_identity_match=True,
            authoritative=True, absence_final=True, now=23,
        )
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state,
                         "retry_authorization_unjournaled")
        self.assertEqual(self.coordinator.repair_missing_reconciliation_event("effect-1"),
                         "accepted")
        self.assertEqual(self.coordinator.repair_missing_reconciliation_event("effect-1"),
                         "duplicate")
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state,
                         "retry_authorized")

    def test_crash_after_found_reconciliation_store_commit_is_repairable(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=2)
        self.coordinator.mark_dispatching(lease, now=21)
        self.coordinator.recover_expired("effect-1", now=22)
        self.store.resolve_reconciliation(
            "effect-1", outcome="found", exact_identity_match=True,
            authoritative=True, provider_reference="provider-crash", now=23,
        )
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state,
                         "acknowledgement_unjournaled")
        self.assertEqual(self.coordinator.repair_missing_ack_event("effect-1"), "accepted")
        self.assertEqual(self.coordinator.repair_missing_ack_event("effect-1"), "duplicate")

    def test_crash_after_lease_store_commit_is_visible_and_repairable(self):
        lease = self.store.claim("effect-1", "worker-A", now=20, lease_seconds=5)
        self.journal.advance_fence(lease.effect_id, lease.attempt_id, lease.fence)
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state,
                         "lease_claim_unjournaled")
        self.assertEqual(self.coordinator.repair_missing_lease_claim_event("effect-1"),
                         "accepted")
        self.assertEqual(self.coordinator.repair_missing_lease_claim_event("effect-1"),
                         "duplicate")

    def test_crash_after_dispatch_intent_is_repairable(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=5)
        self.store.mark_dispatching(lease, now=21)
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state,
                         "dispatch_intent_unjournaled")
        self.assertEqual(self.coordinator.repair_missing_dispatch_intent_event("effect-1"),
                         "accepted")
        self.assertEqual(self.coordinator.repair_missing_dispatch_intent_event("effect-1"),
                         "duplicate")
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state,
                         "dispatching")

    def test_same_attempt_retry_uses_current_fence_for_projection(self):
        first = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=2)
        self.coordinator.mark_dispatching(first, now=21)
        self.coordinator.recover_expired("effect-1", now=22)
        self.coordinator.reconcile(
            "effect-1", outcome="not_found", exact_identity_match=True,
            authoritative=True, absence_final=True, now=23,
        )
        second = self.coordinator.claim("effect-1", "worker-B", now=24, lease_seconds=5)
        self.assertEqual(second.attempt_id, first.attempt_id)
        self.assertGreater(second.fence, first.fence)
        self.store.mark_dispatching(second, now=25)
        self.assertEqual(self.coordinator.rebuild_effect("effect-1").state,
                         "dispatch_intent_unjournaled")

    def test_receipt_binds_only_accepted_attempt_events_and_excludes_quarantine(self):
        from result_receipts import ResultReceiptStore
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=10)
        self.coordinator.mark_dispatching(lease, now=21)
        receipt_store = ResultReceiptStore()
        receipt = self.coordinator.create_result_receipt(
            receipt_store, effect_id="effect-1", attempt_id="attempt-1",
            revision_key="rev-1", contract_version="pc-v1",
            execution_outcome="INCOMPLETE", collection_state="unknown",
            lifecycle_disposition="unknown", cleanup_state="unknown",
            artifact_ids=(), created_at_ms=22,
        )
        self.assertEqual(len(receipt.evidence_refs), 3)
        self.assertEqual(len(receipt.evidence_sha256), 3)
        event = next(e for e in self.journal.events if e.producer_event_id.startswith("dispatch:"))
        self.journal.append(
            producer=self.producer, source=event.source,
            event_id=event.producer_event_id, payload=b'{"kind":"tampered"}',
            occurred_at_ms=21, observed_at_ms=23,
            effect_id="effect-1", attempt_id="attempt-1", fence=lease.fence,
        )
        self.assertEqual(len(self.journal.conflicts), 1)
        self.assertEqual(len(receipt.evidence_refs), 3)

    def test_later_receipt_revision_uses_new_evidence_and_preserves_predecessor(self):
        from result_receipts import ResultReceiptStore
        receipt_store = ResultReceiptStore()
        first = self.coordinator.create_result_receipt(
            receipt_store, effect_id="effect-1", attempt_id="attempt-1",
            revision_key="rev-1", contract_version="pc-v1",
            execution_outcome="INCOMPLETE", collection_state="unknown",
            lifecycle_disposition="unknown", cleanup_state="unknown",
            artifact_ids=(), created_at_ms=11,
        )
        self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=10)
        second = self.coordinator.create_result_receipt(
            receipt_store, effect_id="effect-1", attempt_id="attempt-1",
            revision_key="rev-2", contract_version="pc-v1",
            execution_outcome="INCOMPLETE", collection_state="unknown",
            lifecycle_disposition="unknown", cleanup_state="unknown",
            artifact_ids=(), created_at_ms=21,
            predecessor_receipt_id=first.receipt_id, revision_reason="new lease evidence",
        )
        self.assertEqual(second.version, 2)
        self.assertEqual(second.predecessor_receipt_id, first.receipt_id)
        self.assertGreater(len(second.evidence_refs), len(first.evidence_refs))
        self.assertEqual(first.lifecycle_disposition, "unknown")

    def test_non_object_journal_payload_projects_incomplete(self):
        self.journal.append(
            producer=self.producer, source="pocketcode.coordinator",
            event_id="non-object-payload", payload=b"[]",
            occurred_at_ms=11, observed_at_ms=11,
            effect_id="effect-1", attempt_id="attempt-1",
        )
        projection = self.coordinator.project_attempt_verdict("effect-1", "attempt-1")
        self.assertEqual(projection.verdict, "INCOMPLETE")
        self.assertEqual(projection.reason, "accepted_event_payload_not_object")

    def test_expired_lease_cannot_append_terminal_observation_before_new_fence(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=1)
        self.coordinator.mark_dispatching(lease, now=20)
        self.coordinator.recover_expired("effect-1", now=21)
        with self.assertRaises(OutboxConflict):
            self.coordinator.record_lifecycle_observation(
                "effect-1", "attempt-1", event_id="late-success",
                status="succeeded", fence=lease.fence, now=21,
            )
        self.assertFalse(any(b'"kind":"lifecycle_observation"' in e.payload
                             for e in self.journal.events))

    def test_succeeded_lifecycle_and_natural_child_zero_produce_pass_receipt(self):
        from result_receipts import ResultReceiptStore
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=20)
        self.coordinator.mark_dispatching(lease, now=20)
        self.coordinator.record_lifecycle_observation(
            "effect-1", "attempt-1", event_id="lifecycle-success",
            status="succeeded", fence=lease.fence, now=21,
        )
        self.coordinator.record_exit_observation(
            "effect-1", "attempt-1", event_id="child-exit-zero",
            producer="direct_child_wait", kind="natural_exit",
            exit_code=0, fence=lease.fence, now=22,
        )
        store = ResultReceiptStore()
        receipt = self.coordinator.create_result_receipt(
            store, effect_id="effect-1", attempt_id="attempt-1",
            revision_key="pass-receipt", contract_version="pc-v1",
            execution_outcome="PASS", collection_state="unknown",
            lifecycle_disposition="succeeded", cleanup_state="unknown",
            artifact_ids=(), created_at_ms=23,
        )
        self.assertEqual(receipt.execution_outcome, "PASS")
        self.assertEqual(receipt.projection_reason, "trusted_success_and_child_exit_zero")

    def test_receipt_builder_derives_verdict_when_caller_omits_label(self):
        from result_receipts import ResultReceiptStore
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=20)
        self.coordinator.mark_dispatching(lease, now=20)
        self.coordinator.record_lifecycle_observation(
            "effect-1", "attempt-1", event_id="lifecycle-success",
            status="succeeded", fence=lease.fence, now=21,
        )
        self.coordinator.record_exit_observation(
            "effect-1", "attempt-1", event_id="child-exit-zero",
            producer="direct_child_wait", kind="natural_exit",
            exit_code=0, fence=lease.fence, now=22,
        )
        receipt = self.coordinator.create_result_receipt(
            ResultReceiptStore(), effect_id="effect-1", attempt_id="attempt-1",
            revision_key="derived-pass", contract_version="pc-v1",
            collection_state="unknown", lifecycle_disposition="succeeded",
            cleanup_state="unknown", artifact_ids=(), created_at_ms=23,
        )
        self.assertEqual(receipt.execution_outcome, "PASS")

    def test_program_failed_lifecycle_produces_fail_receipt(self):
        from result_receipts import ResultReceiptStore
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=20)
        self.coordinator.mark_dispatching(lease, now=20)
        self.coordinator.record_lifecycle_observation(
            "effect-1", "attempt-1", event_id="lifecycle-failed",
            status="program_failed", fence=lease.fence, now=21,
        )
        store = ResultReceiptStore()
        receipt = self.coordinator.create_result_receipt(
            store, effect_id="effect-1", attempt_id="attempt-1",
            revision_key="fail-receipt", contract_version="pc-v1",
            execution_outcome="FAIL", collection_state="unknown",
            lifecycle_disposition="program_failed", cleanup_state="unknown",
            artifact_ids=(), created_at_ms=22,
        )
        self.assertEqual(receipt.execution_outcome, "FAIL")
        self.assertEqual(receipt.projection_reason, "coordinator_confirmed_program_failure")

    def test_succeeded_without_natural_child_exit_stays_incomplete(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=20)
        self.coordinator.mark_dispatching(lease, now=20)
        self.coordinator.record_lifecycle_observation(
            "effect-1", "attempt-1", event_id="lifecycle-success",
            status="succeeded", fence=lease.fence, now=21,
        )
        projection = self.coordinator.project_attempt_verdict("effect-1", "attempt-1")
        self.assertEqual(projection.verdict, "INCOMPLETE")
        self.assertEqual(projection.reason, "success_without_natural_child_exit")

    def test_valid_lifecycle_progression_projects_latest_terminal(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=20)
        self.coordinator.mark_dispatching(lease, now=20)
        for event_id, status, now in (("life-queued", "queued", 21),
                                      ("life-running", "running", 22),
                                      ("life-succeeded", "succeeded", 23)):
            self.coordinator.record_lifecycle_observation(
                "effect-1", "attempt-1", event_id=event_id,
                status=status, fence=lease.fence, now=now,
            )
        self.coordinator.record_exit_observation(
            "effect-1", "attempt-1", event_id="child-exit-zero",
            producer="direct_child_wait", kind="natural_exit",
            exit_code=0, fence=lease.fence, now=24,
        )
        projection = self.coordinator.project_attempt_verdict("effect-1", "attempt-1")
        self.assertEqual(projection.verdict, "PASS")
        self.assertEqual(projection.reason, "trusted_success_and_child_exit_zero")

    def test_regressive_lifecycle_progression_is_incomplete(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=20)
        self.coordinator.mark_dispatching(lease, now=20)
        for event_id, status, now in (("life-running", "running", 21),
                                      ("life-queued", "queued", 22)):
            self.coordinator.record_lifecycle_observation(
                "effect-1", "attempt-1", event_id=event_id,
                status=status, fence=lease.fence, now=now,
            )
        projection = self.coordinator.project_attempt_verdict("effect-1", "attempt-1")
        self.assertEqual(projection.verdict, "INCOMPLETE")
        self.assertEqual(projection.reason, "lifecycle_transition_conflict")

    def test_unknown_lifecycle_status_cannot_be_ignored_before_success(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=20)
        self.coordinator.mark_dispatching(lease, now=20)
        self.coordinator.record_lifecycle_observation(
            "effect-1", "attempt-1", event_id="life-unknown",
            status="future_status", fence=lease.fence, now=21,
        )
        self.coordinator.record_lifecycle_observation(
            "effect-1", "attempt-1", event_id="life-success",
            status="succeeded", fence=lease.fence, now=22,
        )
        self.coordinator.record_exit_observation(
            "effect-1", "attempt-1", event_id="child-exit-zero",
            producer="direct_child_wait", kind="natural_exit",
            exit_code=0, fence=lease.fence, now=23,
        )
        projection = self.coordinator.project_attempt_verdict("effect-1", "attempt-1")
        self.assertEqual(projection.verdict, "INCOMPLETE")
        self.assertEqual(projection.reason, "lifecycle_status_unknown")

    def test_non_string_lifecycle_status_fails_closed_without_exception(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=20)
        self.coordinator.mark_dispatching(lease, now=20)
        self.coordinator.record_lifecycle_observation(
            "effect-1", "attempt-1", event_id="life-list-status",
            status=["succeeded"], fence=lease.fence, now=21,
        )
        projection = self.coordinator.project_attempt_verdict("effect-1", "attempt-1")
        self.assertEqual(projection.verdict, "INCOMPLETE")
        self.assertEqual(projection.reason, "lifecycle_status_invalid")

    def test_multiple_terminal_lifecycle_observations_require_reconciliation(self):
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=20)
        self.coordinator.mark_dispatching(lease, now=20)
        for event_id, status, now in (("life-succeeded", "succeeded", 21),
                                      ("life-failed", "program_failed", 22)):
            self.coordinator.record_lifecycle_observation(
                "effect-1", "attempt-1", event_id=event_id,
                status=status, fence=lease.fence, now=now,
            )
        projection = self.coordinator.project_attempt_verdict("effect-1", "attempt-1")
        self.assertEqual(projection.verdict, "INCOMPLETE")
        self.assertEqual(projection.reason, "multiple_terminal_lifecycle_observations")

    def test_old_fence_terminal_observations_force_incomplete_after_authorized_retry(self):
        from result_receipts import ResultReceiptStore
        first = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=2)
        self.coordinator.mark_dispatching(first, now=20)
        self.coordinator.record_lifecycle_observation(
            "effect-1", "attempt-1", event_id="old-lifecycle-success",
            status="succeeded", fence=first.fence, now=20,
        )
        self.coordinator.record_exit_observation(
            "effect-1", "attempt-1", event_id="old-child-zero",
            producer="direct_child_wait", kind="natural_exit",
            exit_code=0, fence=first.fence, now=21,
        )
        self.coordinator.recover_expired("effect-1", now=22)
        self.coordinator.reconcile(
            "effect-1", outcome="not_found", exact_identity_match=True,
            authoritative=True, absence_final=True, now=23,
        )
        second = self.coordinator.claim("effect-1", "worker-B", now=24, lease_seconds=10)
        self.assertGreater(second.fence, first.fence)
        projection = self.coordinator.project_attempt_verdict("effect-1", "attempt-1")
        self.assertEqual(projection.verdict, "INCOMPLETE")
        self.assertEqual(projection.reason,
                         "stale_fence_terminal_observation_requires_reconciliation")

    def test_receipt_lifecycle_disposition_must_match_projected_status(self):
        from result_receipts import ResultReceiptStore
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=10)
        self.coordinator.mark_dispatching(lease, now=20)
        self.coordinator.record_lifecycle_observation(
            "effect-1", "attempt-1", event_id="lifecycle-running",
            status="running", fence=lease.fence, now=21,
        )
        with self.assertRaises(OutboxConflict):
            self.coordinator.create_result_receipt(
                ResultReceiptStore(), effect_id="effect-1", attempt_id="attempt-1",
                revision_key="wrong-lifecycle", contract_version="pc-v1",
                lifecycle_disposition="succeeded", collection_state="unknown",
                cleanup_state="unknown", artifact_ids=(), created_at_ms=22,
            )

    def test_receipt_rejects_unobserved_collection_or_cleanup_claims(self):
        from result_receipts import ResultReceiptStore
        lease = self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=10)
        self.coordinator.mark_dispatching(lease, now=20)
        with self.assertRaises(OutboxConflict):
            self.coordinator.create_result_receipt(
                ResultReceiptStore(), effect_id="effect-1", attempt_id="attempt-1",
                revision_key="unverified-collection", contract_version="pc-v1",
                collection_state="complete", lifecycle_disposition="unknown",
                cleanup_state="unknown", artifact_ids=(), created_at_ms=21,
            )
        with self.assertRaises(OutboxConflict):
            self.coordinator.create_result_receipt(
                ResultReceiptStore(), effect_id="effect-1", attempt_id="attempt-1",
                revision_key="unverified-cleanup", contract_version="pc-v1",
                collection_state="unknown", lifecycle_disposition="unknown",
                cleanup_state="complete", artifact_ids=(), created_at_ms=22,
            )

    def test_dispatch_only_journal_cannot_create_pass_or_fail_receipt(self):
        from result_receipts import ResultReceiptStore
        store = ResultReceiptStore()
        for outcome in ("PASS", "FAIL"):
            with self.subTest(outcome=outcome), self.assertRaises(OutboxConflict):
                self.coordinator.create_result_receipt(
                    store, effect_id="effect-1", attempt_id="attempt-1",
                    revision_key="forbidden-" + outcome, contract_version="pc-v1",
                    execution_outcome=outcome, collection_state="unknown",
                    lifecycle_disposition="succeeded", cleanup_state="unknown",
                    artifact_ids=(), created_at_ms=30,
                )
        self.assertEqual(store.receipts, ())

    def test_reservation_event_is_attempt_bound_and_reservation_replay_after_claim_is_safe(self):
        event = self.journal.events[0]
        self.assertEqual(event.effect_id, "effect-1")
        self.assertEqual(event.attempt_id, "attempt-1")
        self.coordinator.claim("effect-1", "worker-A", now=20, lease_seconds=10)
        self.assertEqual(self.coordinator.reserve(
            "effect-1", "attempt-1", "sha256:req", b'{"op":"build"}', at_ms=10,
        ), "duplicate")

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
