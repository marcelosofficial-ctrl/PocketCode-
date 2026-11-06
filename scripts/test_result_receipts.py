import hashlib
import unittest

try:
    from result_receipts import (
        ArtifactInput, ReceiptConflict, ReleaseAuthorization, ResultReceiptStore,
    )
except ModuleNotFoundError:
    from scripts.result_receipts import (
        ArtifactInput, ReceiptConflict, ReleaseAuthorization, ResultReceiptStore,
    )


class ResultReceiptTests(unittest.TestCase):
    def setUp(self):
        self.store = ResultReceiptStore()
        self.content = b'{"ok":true}\n'
        self.digest = hashlib.sha256(self.content).hexdigest()
        self.artifact = self.store.stage_artifact(ArtifactInput(
            "artifact-1", "summary.json", "application/json", "attempt-1",
            self.content, True, self.digest,
        ))

    def create(self, **overrides):
        args = dict(
            revision_key="receipt-rev-1", effect_id="effect-1",
            attempt_id="attempt-1", contract_version="pc-receipt-v1",
            execution_outcome="PASS", collection_state="complete",
            lifecycle_disposition="succeeded", cleanup_state="complete",
            evidence_refs=("event-1",), evidence_sha256=(self.digest,),
            artifact_ids=("artifact-1",), uncertainties=(), created_at_ms=100,
        )
        args.update(overrides)
        return self.store.create_receipt(**args)

    def auth(self, **overrides):
        args = dict(
            authorization_id="auth-1", policy_revision="policy-1",
            artifact_id="artifact-1", attempt_id="attempt-1",
            current_attempt_id="attempt-1", authorized=True, observed_at_ms=101,
        )
        args.update(overrides)
        return ReleaseAuthorization(**args)

    def test_stage_records_exact_digest_size_and_attempt(self):
        self.assertEqual(self.artifact.sha256, self.digest)
        self.assertEqual(self.artifact.byte_length, len(self.content))
        self.assertEqual(self.artifact.attempt_id, "attempt-1")
        self.assertEqual(self.artifact.integrity_state, "verified")

    def test_exact_artifact_replay_is_idempotent(self):
        replay = self.store.stage_artifact(ArtifactInput(
            "artifact-1", "summary.json", "application/json", "attempt-1",
            self.content, True, self.digest,
        ))
        self.assertEqual(replay, self.artifact)
        self.assertEqual(len(self.store.artifacts), 1)

    def test_artifact_identity_cannot_overwrite_different_bytes(self):
        with self.assertRaises(ReceiptConflict):
            self.store.stage_artifact(ArtifactInput(
                "artifact-1", "summary.json", "application/json", "attempt-1",
                b'{"ok":false}', True,
            ))

    def test_partial_write_is_quarantined(self):
        item = self.store.stage_artifact(ArtifactInput(
            "artifact-partial", "partial.json", "application/json", "attempt-1",
            b'{"ok":', False,
        ))
        self.assertTrue(item.quarantined)
        self.assertEqual(item.integrity_state, "partial_write")

    def test_digest_mismatch_is_quarantined(self):
        item = self.store.stage_artifact(ArtifactInput(
            "artifact-bad", "bad.json", "application/json", "attempt-1",
            self.content, True, "0" * 64,
        ))
        self.assertTrue(item.quarantined)
        self.assertEqual(item.integrity_state, "digest_mismatch")

    def test_unsafe_logical_names_are_rejected(self):
        for name in ("../secret", "..", ".", "folder/file", "folder\\file", ""):
            with self.subTest(name=name), self.assertRaises(ReceiptConflict):
                self.store.stage_artifact(ArtifactInput(
                    "bad-" + str(len(name)), name, "text/plain", "attempt-1", b"x", True,
                ))

    def test_receipt_binds_attempt_evidence_and_artifact_manifest(self):
        receipt = self.create()
        self.assertEqual(receipt.version, 1)
        self.assertEqual(receipt.artifact_manifest, (self.artifact,))
        self.assertEqual(receipt.evidence_refs, ("event-1",))
        self.assertEqual(len(receipt.receipt_sha256), 64)

    def test_exact_receipt_replay_is_idempotent(self):
        first = self.create()
        second = self.create()
        self.assertEqual(first, second)
        self.assertEqual(len(self.store.receipts), 1)

    def test_revision_key_cannot_be_reused_for_changed_content(self):
        self.create()
        with self.assertRaises(ReceiptConflict):
            self.create(execution_outcome="FAIL")

    def test_later_observation_creates_new_linked_version(self):
        first = self.create()
        second = self.create(
            revision_key="receipt-rev-2", created_at_ms=110,
            predecessor_receipt_id=first.receipt_id,
            revision_reason="late collector evidence",
            collection_state="degraded",
            uncertainties=("stderr collector incomplete",),
        )
        self.assertEqual(second.version, 2)
        self.assertEqual(second.predecessor_receipt_id, first.receipt_id)
        self.assertEqual(second.revision_reason, "late collector evidence")
        self.assertEqual(len(self.store.receipts), 2)
        self.assertEqual(first.collection_state, "complete")

    def test_receipt_rejects_mismatched_artifact_attempt(self):
        self.store.stage_artifact(ArtifactInput(
            "artifact-other", "other.json", "application/json", "attempt-2", b"x", True,
        ))
        with self.assertRaises(ReceiptConflict):
            self.create(artifact_ids=("artifact-other",))

    def test_receipt_requires_evidence_digest_pairing(self):
        with self.assertRaises(ReceiptConflict):
            self.create(evidence_refs=("event-1", "event-2"), evidence_sha256=(self.digest,))

    def test_receipt_requires_existing_predecessor(self):
        with self.assertRaises(ReceiptConflict):
            self.create(predecessor_receipt_id="missing")

    def test_release_requires_current_attempt_authorization(self):
        result = self.store.release_artifact("artifact-1", self.auth())
        self.assertEqual(result.disposition, "released")
        self.assertEqual(result.content, self.content)

    def test_release_rechecks_authorization_on_each_request(self):
        self.assertEqual(self.store.release_artifact("artifact-1", self.auth()).disposition,
                         "released")
        revoked = self.auth(authorized=False, authorization_id="auth-revoked")
        self.assertEqual(self.store.release_artifact("artifact-1", revoked).disposition,
                         "denied_by_current_authorization")

    def test_stale_attempt_cannot_release_artifact(self):
        result = self.store.release_artifact(
            "artifact-1", self.auth(current_attempt_id="attempt-2"),
        )
        self.assertEqual(result.disposition, "denied_stale_or_mismatched_attempt")
        self.assertIsNone(result.content)

    def test_quarantined_artifact_cannot_be_released(self):
        self.store.stage_artifact(ArtifactInput(
            "artifact-partial", "partial.json", "application/json", "attempt-1",
            b"partial", False,
        ))
        result = self.store.release_artifact(
            "artifact-partial", self.auth(artifact_id="artifact-partial"),
        )
        self.assertEqual(result.disposition, "denied_quarantined_artifact")
        self.assertIsNone(result.content)

    def test_receipt_copy_failure_and_retry_use_same_receipt(self):
        receipt = self.create()
        failed = self.store.publish_report(
            receipt.receipt_id, "clipboard", success=False, observed_at_ms=102,
        )
        retried = self.store.publish_report(
            receipt.receipt_id, "clipboard", success=True, observed_at_ms=103,
        )
        self.assertEqual(failed.receipt_id, retried.receipt_id)
        self.assertEqual(failed.attempt_number, 1)
        self.assertEqual(retried.attempt_number, 2)
        self.assertEqual(retried.disposition, "published")
        self.assertEqual(len(self.store.receipts), 1)

    def test_invalid_boolean_timestamps_and_digests_fail_closed(self):
        with self.assertRaises(ReceiptConflict):
            self.create(created_at_ms=True)
        with self.assertRaises(ReceiptConflict):
            self.create(evidence_sha256=("not-a-digest",))
        with self.assertRaises(ReceiptConflict):
            self.store.publish_report("receipt-1", "clipboard", success=1, observed_at_ms=1)
        with self.assertRaises(ReceiptConflict):
            self.store.publish_report("receipt-1", "clipboard", success=True, observed_at_ms=True)

    def test_unknown_receipt_cannot_be_published(self):
        with self.assertRaises(ReceiptConflict):
            self.store.publish_report("missing", "clipboard", success=True, observed_at_ms=1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
