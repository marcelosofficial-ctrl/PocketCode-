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
            "artifact-1", "summary.json", "application/json", "effect-1", "attempt-1",
            self.content, True, self.digest,
        ))
        self.receipt = self.create()

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
            principal_id="user-1", tenant_id="tenant-1",
            receipt_id=self.receipt.receipt_id, artifact_id="artifact-1",
            object_version=self.artifact.object_version,
            attempt_id="attempt-1", current_attempt_id="attempt-1",
            scope="artifact:download", authorized=True, revoked=False,
            observed_at_ms=101, expires_at_ms=200,
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
            "artifact-1", "summary.json", "application/json", "effect-1", "attempt-1",
            self.content, True, self.digest,
        ))
        self.assertEqual(replay, self.artifact)
        self.assertEqual(len(self.store.artifacts), 1)

    def test_artifact_identity_cannot_overwrite_different_bytes(self):
        with self.assertRaises(ReceiptConflict):
            self.store.stage_artifact(ArtifactInput(
                "artifact-1", "summary.json", "application/json", "effect-1", "attempt-1",
                b'{"ok":false}', True,
            ))

    def test_partial_write_is_quarantined(self):
        item = self.store.stage_artifact(ArtifactInput(
            "artifact-partial", "partial.json", "application/json", "effect-1", "attempt-1",
            b'{"ok":', False,
        ))
        self.assertTrue(item.quarantined)
        self.assertEqual(item.integrity_state, "partial_write")

    def test_digest_mismatch_is_quarantined(self):
        item = self.store.stage_artifact(ArtifactInput(
            "artifact-bad", "bad.json", "application/json", "effect-1", "attempt-1",
            self.content, True, "0" * 64,
        ))
        self.assertTrue(item.quarantined)
        self.assertEqual(item.integrity_state, "digest_mismatch")

    def test_unsafe_logical_names_are_rejected(self):
        for name in ("../secret", "..", ".", "folder/file", "folder\\file", ""):
            with self.subTest(name=name), self.assertRaises(ReceiptConflict):
                self.store.stage_artifact(ArtifactInput(
                    "bad-" + str(len(name)), name, "text/plain", "effect-1", "attempt-1", b"x", True,
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

    def test_projection_reason_is_part_of_immutable_receipt(self):
        self.assertIsNone(self.receipt.projection_reason)
        with self.assertRaises(ReceiptConflict):
            self.create(projection_reason="insufficient_terminal_evidence")

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

    def test_revision_predecessor_must_match_effect_and_attempt(self):
        predecessor = self.create(revision_key="attempt-2-receipt",
                                  attempt_id="attempt-2", artifact_ids=())
        with self.assertRaises(ReceiptConflict):
            self.create(revision_key="wrong-attempt-link",
                        predecessor_receipt_id=predecessor.receipt_id,
                        revision_reason="invalid cross-attempt link", created_at_ms=101)
        same_attempt_other_effect = self.create(
            revision_key="other-effect", effect_id="effect-2", artifact_ids=(),
        )
        with self.assertRaises(ReceiptConflict):
            self.create(revision_key="wrong-effect-link",
                        predecessor_receipt_id=same_attempt_other_effect.receipt_id,
                        revision_reason="invalid cross-effect link", created_at_ms=102)

    def test_receipt_versions_must_extend_latest_without_forking(self):
        first = self.create()
        second = self.create(
            revision_key="receipt-rev-2", created_at_ms=110,
            predecessor_receipt_id=first.receipt_id,
            revision_reason="late collector evidence",
            collection_state="degraded",
            uncertainties=("stderr collector incomplete",),
        )
        with self.assertRaises(ReceiptConflict):
            self.create(revision_key="receipt-rev-3-fork", created_at_ms=120,
                        predecessor_receipt_id=first.receipt_id,
                        revision_reason="attempt to fork history")
        self.assertEqual(second.version, 2)
        self.assertEqual(len(self.store.receipts), 2)

    def test_receipt_rejects_artifact_from_different_effect_with_same_attempt_id(self):
        self.store.stage_artifact(ArtifactInput(
            "artifact-other-effect", "other.json", "application/json",
            "effect-2", "attempt-1", b"x", True,
        ))
        with self.assertRaises(ReceiptConflict):
            self.create(artifact_ids=("artifact-other-effect",))

    def test_receipt_rejects_mismatched_artifact_attempt(self):
        self.store.stage_artifact(ArtifactInput(
            "artifact-other", "other.json", "application/json", "effect-1", "attempt-2", b"x", True,
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
        result = self.store.release_artifact("artifact-1", self.auth(), receipt_id=self.receipt.receipt_id, now_ms=102)
        self.assertEqual(result.disposition, "released")
        self.assertEqual(result.content, self.content)

    def test_release_rechecks_authorization_on_each_request(self):
        self.assertEqual(self.store.release_artifact(
            "artifact-1", self.auth(), receipt_id=self.receipt.receipt_id, now_ms=102,
        ).disposition, "released")
        revoked = self.auth(authorized=False, authorization_id="auth-revoked")
        self.assertEqual(self.store.release_artifact("artifact-1", revoked, receipt_id=self.receipt.receipt_id, now_ms=102).disposition,
                         "denied_by_current_authorization")

    def test_stale_attempt_cannot_release_artifact(self):
        result = self.store.release_artifact(
            "artifact-1", self.auth(current_attempt_id="attempt-2"),
            receipt_id=self.receipt.receipt_id, now_ms=102,
        )
        self.assertEqual(result.disposition, "denied_stale_or_mismatched_attempt")
        self.assertIsNone(result.content)

    def test_quarantined_artifact_cannot_be_released(self):
        partial = self.store.stage_artifact(ArtifactInput(
            "artifact-partial", "partial.json", "application/json", "effect-1", "attempt-1",
            b"partial", False,
        ))
        partial_receipt = self.store.create_receipt(
            revision_key="receipt-with-partial", effect_id="effect-1", attempt_id="attempt-1",
            contract_version="pc-v1", execution_outcome="INCOMPLETE",
            collection_state="complete", lifecycle_disposition="succeeded",
            cleanup_state="unknown", evidence_refs=("event-partial",),
            evidence_sha256=(self.digest,), artifact_ids=("artifact-partial",),
            created_at_ms=110, predecessor_receipt_id=self.receipt.receipt_id,
            revision_reason="late partial artifact observation",
        )
        result = self.store.release_artifact(
            "artifact-partial", self.auth(artifact_id="artifact-partial",
                object_version=partial.object_version, receipt_id=partial_receipt.receipt_id),
            receipt_id=partial_receipt.receipt_id, now_ms=111,
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

    def test_receipt_rejects_duplicate_evidence_and_artifact_refs(self):
        with self.assertRaises(ReceiptConflict):
            self.create(evidence_refs=("event-1", "event-1"),
                        evidence_sha256=(self.digest, self.digest))
        with self.assertRaises(ReceiptConflict):
            self.create(artifact_ids=("artifact-1", "artifact-1"))

    def test_revision_requires_reason_when_linking_predecessor(self):
        first = self.create()
        with self.assertRaises(ReceiptConflict):
            self.create(revision_key="receipt-rev-2", predecessor_receipt_id=first.receipt_id,
                        created_at_ms=101)

    def test_malformed_authorization_types_fail_closed_without_exception(self):
        malformed = self.auth(policy_revision=None)
        result = self.store.release_artifact(
            "artifact-1", malformed, receipt_id=self.receipt.receipt_id, now_ms=102,
        )
        self.assertEqual(result.disposition, "denied_invalid_authorization")
        self.assertIsNone(result.content)

    def test_release_rejects_malformed_artifact_id_without_exception(self):
        result = self.store.release_artifact(
            [], self.auth(), receipt_id=self.receipt.receipt_id, now_ms=102,
        )
        self.assertEqual(result.disposition, "denied_invalid_artifact_id")
        self.assertIsNone(result.content)

    def test_publish_rejects_malformed_receipt_id_without_exception(self):
        with self.assertRaises(ReceiptConflict):
            self.store.publish_report([], "clipboard", success=True, observed_at_ms=1)

    def test_release_authorization_is_a_caller_supplied_snapshot(self):
        # The model checks each supplied snapshot but does not authenticate or
        # fetch the authority. The caller must resolve a fresh decision per call.
        allowed = self.auth(authorization_id="snapshot-1", authorized=True)
        denied = self.auth(authorization_id="snapshot-2", authorized=False)
        self.assertEqual(self.store.release_artifact(
            "artifact-1", allowed, receipt_id=self.receipt.receipt_id, now_ms=102,
        ).disposition, "released")
        self.assertEqual(self.store.release_artifact(
            "artifact-1", denied, receipt_id=self.receipt.receipt_id, now_ms=102,
        ).disposition, "denied_by_current_authorization")

    def test_release_requires_artifact_membership_in_named_receipt(self):
        other = self.store.create_receipt(
            revision_key="receipt-no-artifact", effect_id="effect-1", attempt_id="attempt-1",
            contract_version="pc-v1", execution_outcome="PASS", collection_state="complete",
            lifecycle_disposition="succeeded", cleanup_state="complete",
            evidence_refs=("event-2",), evidence_sha256=(self.digest,),
            artifact_ids=(), created_at_ms=110,
            predecessor_receipt_id=self.receipt.receipt_id,
            revision_reason="new report version without this artifact",
        )
        auth = self.auth(receipt_id=other.receipt_id)
        result = self.store.release_artifact(
            "artifact-1", auth, receipt_id=other.receipt_id, now_ms=111,
        )
        self.assertEqual(result.disposition, "denied_artifact_not_in_receipt")

    def test_historical_receipt_cannot_authorize_new_release_after_successor(self):
        historical = self.receipt
        historical_hash = historical.receipt_sha256
        latest = self.create(
            revision_key="receipt-rev-2", created_at_ms=110,
            predecessor_receipt_id=historical.receipt_id,
            revision_reason="late non-artifact observation",
            evidence_refs=("event-1", "event-2"),
            evidence_sha256=(self.digest, self.digest),
        )
        old_authorization = self.auth(receipt_id=historical.receipt_id)
        denied = self.store.release_artifact(
            "artifact-1", old_authorization,
            receipt_id=historical.receipt_id, now_ms=111,
        )
        self.assertEqual(denied.disposition, "denied_superseded_receipt")
        self.assertIsNone(denied.content)

        fresh_authorization = self.auth(
            authorization_id="auth-latest",
            receipt_id=latest.receipt_id,
        )
        allowed = self.store.release_artifact(
            "artifact-1", fresh_authorization,
            receipt_id=latest.receipt_id, now_ms=111,
        )
        self.assertEqual(allowed.disposition, "released")
        self.assertEqual(allowed.content, self.content)

        self.assertEqual(len(self.store.receipts), 2)
        self.assertEqual(self.store.receipts[0], historical)
        self.assertEqual(self.store.receipts[0].receipt_sha256, historical_hash)
        self.assertEqual(self.store.receipts[0].version, 1)
        self.assertEqual(self.store.receipts[1].version, 2)

    def test_latest_receipt_removing_artifact_denies_release_without_reviving_history(self):
        historical = self.receipt
        latest = self.create(
            revision_key="receipt-rev-2", created_at_ms=110,
            predecessor_receipt_id=historical.receipt_id,
            revision_reason="artifact no longer included after reconciliation",
            artifact_ids=(),
            evidence_refs=("event-1", "event-2"),
            evidence_sha256=(self.digest, self.digest),
        )
        old_authorization = self.auth(receipt_id=historical.receipt_id)
        old_result = self.store.release_artifact(
            "artifact-1", old_authorization,
            receipt_id=historical.receipt_id, now_ms=111,
        )
        self.assertEqual(old_result.disposition, "denied_superseded_receipt")

        latest_authorization = self.auth(
            authorization_id="auth-latest-no-artifact",
            receipt_id=latest.receipt_id,
        )
        latest_result = self.store.release_artifact(
            "artifact-1", latest_authorization,
            receipt_id=latest.receipt_id, now_ms=111,
        )
        self.assertEqual(latest_result.disposition, "denied_artifact_not_in_receipt")
        self.assertIsNone(latest_result.content)
        self.assertEqual(self.store.receipts[0], historical)
        self.assertEqual(len(self.store.receipts), 2)

    def test_release_binds_exact_object_version_and_operation_scope(self):
        wrong_version = self.auth(object_version="artifact-1:v2")
        self.assertEqual(self.store.release_artifact(
            "artifact-1", wrong_version, receipt_id=self.receipt.receipt_id, now_ms=102,
        ).disposition, "denied_stale_or_mismatched_attempt")
        wrong_scope = self.auth(scope="artifact:share")
        self.assertEqual(self.store.release_artifact(
            "artifact-1", wrong_scope, receipt_id=self.receipt.receipt_id,
            now_ms=102, operation="download",
        ).disposition, "denied_scope_mismatch")

    def test_expired_or_revoked_authorization_is_denied(self):
        expired = self.auth(expires_at_ms=102)
        self.assertEqual(self.store.release_artifact(
            "artifact-1", expired, receipt_id=self.receipt.receipt_id, now_ms=102,
        ).disposition, "denied_expired_authorization")
        revoked = self.auth(revoked=True)
        self.assertEqual(self.store.release_artifact(
            "artifact-1", revoked, receipt_id=self.receipt.receipt_id, now_ms=102,
        ).disposition, "denied_revoked_authorization")

    def test_unknown_receipt_cannot_be_published(self):
        with self.assertRaises(ReceiptConflict):
            self.store.publish_report("missing", "clipboard", success=True, observed_at_ms=1)


    def test_publication_request_replay_with_same_key_returns_original_attempt(self):
        first = self.store.publish_report(self.receipt.receipt_id, "clipboard", success=False, observed_at_ms=150, idempotency_key="copy-request-1")
        replay = self.store.publish_report(self.receipt.receipt_id, "clipboard", success=False, observed_at_ms=150, idempotency_key="copy-request-1")
        self.assertEqual(replay, first)
        self.assertEqual(len(self.store.publication_attempts), 1)

    def test_publication_key_cannot_be_reused_with_changed_result(self):
        self.store.publish_report(self.receipt.receipt_id, "clipboard", success=False, observed_at_ms=150, idempotency_key="copy-request-1")
        with self.assertRaises(ReceiptConflict):
            self.store.publish_report(self.receipt.receipt_id, "clipboard", success=True, observed_at_ms=151, idempotency_key="copy-request-1")
        self.assertEqual(len(self.store.publication_attempts), 1)

    def test_new_publication_key_records_a_real_retry(self):
        first = self.store.publish_report(self.receipt.receipt_id, "clipboard", success=False, observed_at_ms=150, idempotency_key="copy-request-1")
        retry = self.store.publish_report(self.receipt.receipt_id, "clipboard", success=True, observed_at_ms=160, idempotency_key="copy-request-2")
        self.assertEqual((first.attempt_number, retry.attempt_number), (1, 2))
        self.assertEqual(len(self.store.publication_attempts), 2)

    def test_publication_idempotency_key_is_scoped_to_destination(self):
        first = self.store.publish_report(self.receipt.receipt_id, "clipboard", success=False, observed_at_ms=150, idempotency_key="copy-request-1")
        other = self.store.publish_report(self.receipt.receipt_id, "share-sheet", success=True, observed_at_ms=151, idempotency_key="copy-request-1")
        self.assertEqual((first.attempt_number, other.attempt_number), (1, 1))
        self.assertEqual(len(self.store.publication_attempts), 2)

    def test_empty_publication_idempotency_key_rejected(self):
        with self.assertRaises(ReceiptConflict):
            self.store.publish_report(self.receipt.receipt_id, "clipboard", success=False, observed_at_ms=150, idempotency_key=" ")


    def test_release_completed_before_successor_is_not_retroactively_revoked(self):
        old_authorization = self.auth()
        completed = self.store.release_artifact(
            "artifact-1", old_authorization,
            receipt_id=self.receipt.receipt_id, now_ms=102,
        )
        self.assertEqual(completed.disposition, "released")
        self.assertEqual(completed.content, self.content)

        latest = self.create(
            revision_key="receipt-rev-2", created_at_ms=110,
            predecessor_receipt_id=self.receipt.receipt_id,
            revision_reason="later evidence arrived after completed release",
            evidence_refs=("event-2",),
            evidence_sha256=(self.digest,),
        )
        self.assertEqual(latest.version, 2)
        self.assertEqual(completed.disposition, "released")
        self.assertEqual(completed.content, self.content)

        subsequent_old_request = self.store.release_artifact(
            "artifact-1", old_authorization,
            receipt_id=self.receipt.receipt_id, now_ms=111,
        )
        self.assertEqual(subsequent_old_request.disposition, "denied_superseded_receipt")
        self.assertIsNone(subsequent_old_request.content)

    def test_artifact_object_version_rollover_requires_latest_manifest(self):
        new_content = b'{"ok":false}\\n'
        new_digest = hashlib.sha256(new_content).hexdigest()
        new_artifact = self.store.stage_artifact(ArtifactInput(
            "artifact-2", "summary.json", "application/json", "effect-1", "attempt-1",
            new_content, True, new_digest,
        ))
        latest = self.create(
            revision_key="receipt-rev-2", created_at_ms=110,
            predecessor_receipt_id=self.receipt.receipt_id,
            revision_reason="artifact object version rolled forward",
            artifact_ids=("artifact-2",),
            evidence_refs=("event-2",),
            evidence_sha256=(new_digest,),
        )

        old_result = self.store.release_artifact(
            "artifact-1", self.auth(),
            receipt_id=self.receipt.receipt_id, now_ms=111,
        )
        self.assertEqual(old_result.disposition, "denied_superseded_receipt")
        self.assertIsNone(old_result.content)

        latest_auth = self.auth(
            authorization_id="auth-new-artifact",
            receipt_id=latest.receipt_id,
            artifact_id="artifact-2",
            object_version=new_artifact.object_version,
        )
        latest_result = self.store.release_artifact(
            "artifact-2", latest_auth,
            receipt_id=latest.receipt_id, now_ms=111,
        )
        self.assertEqual(latest_result.disposition, "released")
        self.assertEqual(latest_result.object_version, new_artifact.object_version)
        self.assertEqual(latest_result.content, new_content)

        omitted_artifact_auth = self.auth(
            authorization_id="auth-omitted-artifact",
            receipt_id=latest.receipt_id,
        )
        omitted_result = self.store.release_artifact(
            "artifact-1", omitted_artifact_auth,
            receipt_id=latest.receipt_id, now_ms=111,
        )
        self.assertEqual(omitted_result.disposition, "denied_artifact_not_in_receipt")
        self.assertIsNone(omitted_result.content)

    def test_latest_receipt_gate_is_scoped_to_exact_effect_and_attempt(self):
        other_effect = self.create(
            revision_key="other-effect-receipt",
            effect_id="effect-2",
            artifact_ids=(),
            created_at_ms=105,
            evidence_refs=("event-other-effect",),
        )
        self.assertEqual(other_effect.effect_id, "effect-2")
        self.assertEqual(other_effect.version, 1)

        original_result = self.store.release_artifact(
            "artifact-1", self.auth(),
            receipt_id=self.receipt.receipt_id, now_ms=111,
        )
        self.assertEqual(original_result.disposition, "released")
        self.assertEqual(original_result.content, self.content)



if __name__ == "__main__":
    unittest.main(verbosity=2)
