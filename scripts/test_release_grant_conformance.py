import unittest

try:
    from release_grant_conformance import (
        ContractConflict, ReceiptHead, ReleaseGrantContractModel, StaleFence,
    )
except ModuleNotFoundError:
    from scripts.release_grant_conformance import (
        ContractConflict, ReceiptHead, ReleaseGrantContractModel, StaleFence,
    )


class ReleaseGrantConformanceTests(unittest.TestCase):
    def setUp(self):
        self.store = ReleaseGrantContractModel()
        self.store.seed_head(ReceiptHead(
            "effect-1", "attempt-1", "receipt-1", 1,
            "artifact-1", "object-v1", 10,
        ))
        self.base = dict(
            tenant_id="tenant-1", principal_id="principal-1",
            request_key="download-1", effect_id="effect-1",
            attempt_id="attempt-1", receipt_id="receipt-1",
            receipt_revision=1, artifact_id="artifact-1",
            object_version="object-v1", operation="download",
            auth_tenant_id="tenant-1", auth_principal_id="principal-1",
            auth_allowed=True, auth_operation="download",
            auth_effect_id="effect-1", auth_attempt_id="attempt-1",
            auth_receipt_id="receipt-1", auth_artifact_id="artifact-1",
            auth_object_version="object-v1",
            authorization_id="auth-1", policy_revision="policy-1",
        )

    def reserve(self, **changes):
        values = dict(self.base)
        values.update(changes)
        return self.store.reserve(**values)

    def successor(self, **changes):
        values = dict(
            effect_id="effect-1", attempt_id="attempt-1",
            expected_receipt_id="receipt-1", expected_revision=1,
            successor_receipt_id="receipt-2", artifact_id="artifact-1",
            object_version="object-v2", artifact_length=12,
        )
        values.update(changes)
        return self.store.advance_receipt_head(**values)

    def test_grant_commit_wins_then_successor_keeps_grant_pinned(self):
        grant = self.reserve()
        self.successor()
        self.assertEqual(grant.head.receipt_id, "receipt-1")
        self.assertEqual(grant.head.object_version, "object-v1")
        self.assertEqual(self.store.heads[("effect-1", "attempt-1")].receipt_id, "receipt-2")

    def test_successor_commit_wins_then_old_receipt_grant_is_denied(self):
        self.successor()
        with self.assertRaisesRegex(ContractConflict, "stale receipt"):
            self.reserve()

    def test_only_one_successor_from_same_predecessor_can_win(self):
        self.successor()
        with self.assertRaisesRegex(ContractConflict, "compare-and-swap"):
            self.successor(successor_receipt_id="receipt-3")

    def test_same_key_same_intent_replay_survives_refreshed_authorization_and_successor(self):
        first = self.reserve()
        self.successor()
        replay = self.reserve(authorization_id="auth-refreshed", policy_revision="policy-2")
        self.assertEqual(replay, first)
        self.assertEqual(replay.authorization_id, "auth-1")
        self.assertEqual(replay.policy_revision, "policy-1")

    def test_same_key_changed_object_version_conflicts(self):
        self.reserve()
        with self.assertRaisesRegex(ContractConflict, "different release intent"):
            self.reserve(object_version="object-v2")

    def test_same_key_changed_operation_conflicts(self):
        self.reserve()
        with self.assertRaisesRegex(ContractConflict, "different release intent"):
            self.reserve(operation="share", auth_operation="share")

    def test_idempotency_namespace_is_tenant_and_principal_scoped(self):
        first = self.reserve()
        other_tenant = self.reserve(tenant_id="tenant-2", auth_tenant_id="tenant-2")
        other_principal = self.reserve(
            principal_id="principal-2", auth_principal_id="principal-2",
        )
        self.assertEqual(len(self.store.grants), 3)
        self.assertNotEqual(first.grant_id, other_tenant.grant_id)
        self.assertNotEqual(first.grant_id, other_principal.grant_id)

    def test_unauthenticated_replay_is_rejected_before_idempotency_lookup(self):
        self.reserve()
        with self.assertRaisesRegex(ContractConflict, "authorization"):
            self.reserve(auth_allowed=False)

    def test_wrong_authorization_operation_is_rejected(self):
        with self.assertRaisesRegex(ContractConflict, "scope mismatch"):
            self.reserve(auth_operation="share")

    def test_authorization_must_bind_exact_artifact_object_version(self):
        with self.assertRaisesRegex(ContractConflict, "not bound"):
            self.reserve(object_version="object-v2")

    def test_authorization_must_bind_exact_receipt_revision(self):
        with self.assertRaisesRegex(ContractConflict, "not bound"):
            self.reserve(receipt_id="receipt-2", receipt_revision=2)

    def test_consumer_defers_future_event_until_predecessor_arrives(self):
        self.reserve()
        first = next(iter(self.store.events.values()))
        future = type(first)(
            first.source, "release-grant-1:v3", first.grant_id,
            3, "completed", "future-digest",
        )
        self.assertEqual(self.store.consume_event(future), "deferred_gap")
        self.assertEqual(self.store.consume_event(first), "accepted")
        second = type(first)(
            first.source, "release-grant-1:v2", first.grant_id,
            2, "transferring", "second-digest",
        )
        self.assertEqual(self.store.consume_event(second), "accepted")
        self.assertEqual(self.store.consume_event(future), "accepted")

    def test_crash_after_staged_grant_leaves_no_partial_state(self):
        with self.assertRaisesRegex(RuntimeError, "staged grant"):
            self.reserve(fail_at="after_grant")
        self.assertEqual((len(self.store.grants), len(self.store.events), len(self.store.outbox)), (0, 0, 0))
        self.assertEqual(self.reserve().grant_id, "release-grant-1")

    def test_crash_after_staged_event_leaves_no_partial_state(self):
        with self.assertRaisesRegex(RuntimeError, "staged event"):
            self.reserve(fail_at="after_event")
        self.assertEqual((len(self.store.grants), len(self.store.events), len(self.store.outbox)), (0, 0, 0))

    def test_crash_before_commit_leaves_no_partial_state(self):
        with self.assertRaisesRegex(RuntimeError, "before commit"):
            self.reserve(fail_at="before_commit")
        self.assertEqual((len(self.store.grants), len(self.store.events), len(self.store.outbox)), (0, 0, 0))

    def test_successful_commit_lost_response_replays_original_grant(self):
        first = self.reserve()
        recovered = self.reserve()
        self.assertEqual(first, recovered)
        self.assertEqual((len(self.store.grants), len(self.store.events), len(self.store.outbox)), (1, 1, 1))

    def test_expired_worker_cannot_mutate_before_takeover(self):
        grant = self.reserve()
        lease = self.store.claim_worker(grant_id=grant.grant_id, owner="A", now=10, lease_seconds=5)
        with self.assertRaises(StaleFence):
            self.store.record_progress(lease, now=15, progress_bytes=2)

    def test_old_worker_is_fenced_after_new_worker_takeover(self):
        grant = self.reserve()
        old = self.store.claim_worker(grant_id=grant.grant_id, owner="A", now=10, lease_seconds=5)
        new = self.store.claim_worker(grant_id=grant.grant_id, owner="B", now=15, lease_seconds=5)
        self.assertGreater(new.fence, old.fence)
        with self.assertRaises(StaleFence):
            self.store.record_progress(old, now=16, progress_bytes=2)
        updated = self.store.record_progress(new, now=16, progress_bytes=3)
        self.assertEqual(updated.progress_bytes, 3)

    def test_progress_is_monotonic_and_bounded_by_pinned_object_length(self):
        grant = self.reserve()
        lease = self.store.claim_worker(grant_id=grant.grant_id, owner="A", now=0, lease_seconds=20)
        self.store.record_progress(lease, now=1, progress_bytes=5)
        with self.assertRaisesRegex(ContractConflict, "monotonic"):
            self.store.record_progress(lease, now=2, progress_bytes=4)
        with self.assertRaisesRegex(ContractConflict, "monotonic"):
            self.store.record_progress(lease, now=2, progress_bytes=11)

    def test_consumer_deduplicates_same_source_event_id(self):
        self.reserve()
        event = next(iter(self.store.events.values()))
        self.assertEqual(self.store.consume_event(event), "accepted")
        self.assertEqual(self.store.consume_event(event), "duplicate")

    def test_consumer_rejects_same_event_identity_with_changed_payload(self):
        self.reserve()
        event = next(iter(self.store.events.values()))
        self.store.consume_event(event)
        changed = type(event)(
            event.source, event.event_id, event.grant_id,
            event.aggregate_version, event.state, "different-digest",
        )
        with self.assertRaisesRegex(ContractConflict, "different payload"):
            self.store.consume_event(changed)

    def test_consumer_does_not_mark_future_event_consumed_when_predecessor_is_missing(self):
        self.reserve()
        event = next(iter(self.store.events.values()))
        future = type(event)(
            event.source, "release-grant-1:v3", event.grant_id,
            3, "completed", "future-digest",
        )
        self.assertEqual(self.store.consume_event(future), "deferred_gap")
        self.assertEqual(self.store.consumer_versions[event.grant_id], 0)


if __name__ == "__main__":
    unittest.main()
