"""Synthetic lifecycle tests only; no user code or provider is executed."""
import unittest

from lifecycle_contract import (
    DeletionTombstones, IdempotencyConflict, OutputBudget, ReportHistory,
    artifact_release_allowed, canonical_request_fingerprint, derive_disposition,
    reduce_terminal_events, reserve_idempotency, reserve_idempotency_batch,
    StreamingRedactor,
)


class LifecycleTests(unittest.TestCase):
    def test_contradictory_evidence_takes_precedence_over_not_started(self):
        self.assertEqual(derive_disposition(
            "NOT_STARTED", "CONFIRMED", policy_confirmed=False,
            termination_confirmed=False, artifacts_valid=False,
            tenant_job_authorized=False, contradictory_evidence=True), "INCOMPLETE")

    def test_exit_zero_needs_cleanup_policy_termination_artifact_and_tenant_gates(self):
        args = dict(policy_confirmed=True, termination_confirmed=True,
                    artifacts_valid=True, tenant_job_authorized=True)
        self.assertEqual(derive_disposition("EXIT_ZERO", "CONFIRMED", **args), "PASS")
        for field in args:
            broken = dict(args)
            broken[field] = False
            self.assertEqual(derive_disposition("EXIT_ZERO", "CONFIRMED", **broken), "INCOMPLETE")
        self.assertEqual(derive_disposition("EXIT_ZERO", "UNKNOWN", **args), "INCOMPLETE")

    def test_timeout_unknown_termination_and_output_violation_never_pass(self):
        self.assertEqual(derive_disposition(
            "TIMED_OUT", "CONFIRMED", policy_confirmed=True,
            termination_confirmed=False, artifacts_valid=True,
            tenant_job_authorized=True), "INCOMPLETE")
        self.assertEqual(derive_disposition(
            "EXIT_ZERO", "CONFIRMED", policy_confirmed=True,
            termination_confirmed=True, artifacts_valid=True,
            tenant_job_authorized=True, output_truncated=True), "LIMIT_EXCEEDED")

    def test_coordinator_sequence_wins_over_provider_timestamp(self):
        result = reduce_terminal_events([
            {"event_id": "timeout", "sequence": 10, "kind": "timeout",
             "payload": {}, "provider_timestamp": 999},
            {"event_id": "exit", "sequence": 11, "kind": "exit_zero",
             "payload": {}, "provider_timestamp": 1},
        ])
        self.assertEqual(result["execution_outcome"], "TIMED_OUT")
        self.assertEqual(result["winning_event_id"], "timeout")
        self.assertTrue(result["contradictory_evidence"])
        self.assertEqual([event["event_id"] for event in result["conflicts"]], ["exit"])
        self.assertEqual(derive_disposition(
            result["execution_outcome"], "CONFIRMED", policy_confirmed=True,
            termination_confirmed=True, artifacts_valid=True,
            tenant_job_authorized=True,
            contradictory_evidence=result["contradictory_evidence"]), "INCOMPLETE")

    def test_duplicate_event_is_idempotent_but_conflict_is_marked(self):
        event = {"event_id": "e1", "sequence": 1, "kind": "exit_zero", "payload": {"exit": 0}}
        result = reduce_terminal_events([event, dict(event)])
        self.assertEqual(len(result["events"]), 1)
        conflict = reduce_terminal_events([event, {
            "event_id": "e1", "sequence": 2, "kind": "timeout", "payload": {"exit": 0}
        }])
        self.assertTrue(conflict["contradictory_evidence"])
        self.assertEqual(len(conflict["conflicts"]), 1)

    def test_fingerprint_binds_source_policy_and_canonical_inputs(self):
        def fp(source=b"print(1)", inputs=None, policy=None):
            return canonical_request_fingerprint(
                contract_version="pc-run/0.1", tenant_id="t1", runtime="Python",
                entrypoint="main.py", source=source,
                inputs=inputs if inputs is not None else [("input.csv", "TEXT/CSV", b"a,b\n1,2\n")],
                effective_policy=policy or {"network": "deny", "version": 1})
        self.assertEqual(fp(), fp())
        self.assertNotEqual(fp(), fp(source=b"print(2)"))
        self.assertNotEqual(fp(), fp(policy={"network": "deny", "version": 2}))
        self.assertEqual(fp(inputs=[("b.txt", "text/plain", b"B"), ("a.csv", "text/csv", b"A")]),
                         fp(inputs=[("a.csv", "text/csv", b"A"), ("b.txt", "text/plain", b"B")]))
        with self.assertRaises(ValueError):
            fp(inputs=[("café.csv", "text/csv", b"A"), ("cafe\u0301.csv", "text/csv", b"B")])

    def test_idempotency_replay_conflict_and_tenant_scope(self):
        records = {}
        self.assertEqual(reserve_idempotency(records, tenant_id="t1", key="k",
                         fingerprint="f1", proposed_job_id="j1"), ("CREATED", "j1"))
        self.assertEqual(reserve_idempotency(records, tenant_id="t1", key="k",
                         fingerprint="f1", proposed_job_id="j2"), ("REPLAY", "j1"))
        with self.assertRaises(IdempotencyConflict):
            reserve_idempotency(records, tenant_id="t1", key="k",
                                fingerprint="f2", proposed_job_id="j3")
        self.assertEqual(reserve_idempotency(records, tenant_id="t2", key="k",
                         fingerprint="f2", proposed_job_id="j4"), ("CREATED", "j4"))

    def test_artifact_and_output_gates(self):
        self.assertFalse(artifact_release_allowed(
            cleanup_state="UNKNOWN", digest_valid=True,
            job_association_valid=True, tenant_authorized=True))
        budget = OutputBudget(per_stream_cap=4, aggregate_cap=6)
        budget.add("stdout", b"1234")
        budget.add("stderr", b"56")
        budget.add("stdout", b"7")
        self.assertTrue(budget.exceeded)
        self.assertLessEqual(len(budget.retained_bytes("stdout")), 4)
        self.assertLessEqual(len(budget.retained_bytes("stdout")) +
                             len(budget.retained_bytes("stderr")), 6)


    def test_configured_secret_pattern_is_redacted_across_chunks_before_retention(self):
        budget = OutputBudget(per_stream_cap=4096, aggregate_cap=8192)
        budget.add("stdout", b"x" * 800 + b" secret=alpha-")
        budget.add("stdout", b"beta-token suffix" + b"y" * 800)
        budget.finish()
        retained = budget.retained_bytes("stdout")
        self.assertNotIn(b"alpha-beta-token", retained)
        self.assertIn(b"*" * len(b"secret=alpha-beta-token"), retained)

    def test_bearer_and_provider_key_patterns_are_redacted(self):
        raw = (b"Authorization: Bearer abcdefghijklmnop "
               b" sk-1234567890abcdef "
               b" ghp_123456789012345678901234567890")
        redacted = StreamingRedactor._redact(raw)
        self.assertNotIn(b"abcdefghijklmnop", redacted)
        self.assertNotIn(b"sk-1234567890abcdef", redacted)
        self.assertNotIn(b"ghp_123456789012345678901234567890", redacted)
        self.assertEqual(len(raw), len(redacted))

    def test_redaction_does_not_leak_a_match_split_at_carry_boundary(self):
        redactor = StreamingRedactor()
        prefix = b"x" * 750
        secret = b"secret=alpha-beta-token"
        first = redactor.feed(prefix + secret[:10])
        # This chunk makes the carry cutoff land inside the secret match.
        second = redactor.feed(secret[10:] + b"y" * 749)
        tail = redactor.finish()
        retained = first + second + tail
        self.assertNotIn(b"alpha-beta-token", retained)
        self.assertIn(b"*" * len(secret), retained)

    def test_duplicate_event_id_with_changed_sequence_is_conflict(self):
        event = {"event_id": "same", "sequence": 1, "kind": "exit_zero", "payload": {}}
        result = reduce_terminal_events([event, {
            "event_id": "same", "sequence": 2, "kind": "exit_zero", "payload": {}
        }])
        self.assertTrue(result["contradictory_evidence"])
        self.assertEqual(len(result["conflicts"]), 1)

    def test_duplicate_coordinator_sequence_has_deterministic_replay_order(self):
        first = {"event_id": "z-event", "sequence": 7, "kind": "timeout", "payload": {}}
        second = {"event_id": "a-event", "sequence": 7, "kind": "exit_zero", "payload": {}}
        left = reduce_terminal_events([first, second])
        right = reduce_terminal_events([second, first])
        self.assertTrue(left["contradictory_evidence"])
        self.assertTrue(right["contradictory_evidence"])
        self.assertEqual(left["events"], right["events"])
        self.assertEqual(left["execution_outcome"], right["execution_outcome"])

    def test_artifact_release_requires_each_gate_independently(self):
        valid = dict(cleanup_state="CONFIRMED", digest_valid=True,
                     job_association_valid=True, tenant_authorized=True)
        self.assertTrue(artifact_release_allowed(**valid))
        for field in valid:
            broken = dict(valid)
            broken[field] = "UNKNOWN" if field == "cleanup_state" else False
            self.assertFalse(artifact_release_allowed(**broken))

    def test_output_budget_counts_observed_bytes_and_stops_retaining_on_overflow(self):
        budget = OutputBudget(per_stream_cap=4, aggregate_cap=6)
        budget.add("stdout", b"1234")
        budget.add("stderr", b"56")
        budget.add("stdout", b"789")
        self.assertTrue(budget.exceeded)
        self.assertEqual(budget.observed, {"stdout": 7, "stderr": 2})
        before = (budget.retained_bytes("stdout"), budget.retained_bytes("stderr"))
        budget.add("stderr", b"more bytes after overflow")
        budget.finish()
        self.assertEqual((budget.retained_bytes("stdout"), budget.retained_bytes("stderr")), before)

    def test_cleanup_reconciliation_appends_new_report_version_without_rewriting_history(self):
        history = ReportHistory()
        original = history.append("job-1", disposition="INCOMPLETE",
                                  cleanup_state="UNKNOWN", evidence_ref="evidence-v1")
        corrected = history.append("job-1", disposition="PASS",
                                   cleanup_state="CONFIRMED", evidence_ref="evidence-v2")
        self.assertEqual(original["version"], 1)
        self.assertEqual(corrected["version"], 2)
        self.assertEqual(original["disposition"], "INCOMPLETE")
        versions = history.versions("job-1")
        self.assertEqual([v["disposition"] for v in versions], ["INCOMPLETE", "PASS"])
        corrected["disposition"] = "TAMPERED"
        versions[0]["disposition"] = "TAMPERED"
        self.assertEqual([v["disposition"] for v in history.versions("job-1")],
                         ["INCOMPLETE", "PASS"])

    def test_report_history_versions_are_per_job_and_require_evidence_reference(self):
        history = ReportHistory()
        self.assertEqual(history.append("a", disposition="FAILED", cleanup_state="CONFIRMED",
                                        evidence_ref="e1")["version"], 1)
        self.assertEqual(history.append("b", disposition="FAILED", cleanup_state="CONFIRMED",
                                        evidence_ref="e2")["version"], 1)
        with self.assertRaises(ValueError):
            history.append("a", disposition="INCOMPLETE", cleanup_state="UNKNOWN", evidence_ref="")
        with self.assertRaises(ValueError):
            history.append("a", disposition="PASS", cleanup_state="UNKNOWN", evidence_ref="e3")

    def test_deletion_tombstone_is_tenant_scoped_and_expires_at_30_days(self):
        tombstones = DeletionTombstones()
        tombstones.add(tenant_id="t1", key="k", fingerprint="f1", deleted_at=100)
        deadline = 100 + DeletionTombstones.RETENTION_SECONDS
        self.assertEqual(tombstones.lookup(tenant_id="t1", key="k", now=deadline - 1),
                         ("TOMBSTONE", "f1"))
        self.assertIsNone(tombstones.lookup(tenant_id="t2", key="k", now=deadline - 1))
        self.assertIsNone(tombstones.lookup(tenant_id="t1", key="k", now=deadline))
        self.assertIsNone(tombstones.lookup(tenant_id="t1", key="k", now=deadline + 1))

    def test_same_key_same_fingerprint_race_has_one_created_job_and_replays(self):
        records = {}
        submissions = [
            {"tenant_id": "t1", "key": "k", "fingerprint": "f", "proposed_job_id": "j1"},
            {"tenant_id": "t1", "key": "k", "fingerprint": "f", "proposed_job_id": "j2"},
            {"tenant_id": "t1", "key": "k", "fingerprint": "f", "proposed_job_id": "j3"},
        ]
        result = reserve_idempotency_batch(records, submissions)
        self.assertEqual([item["status"] for item in result], ["CREATED", "REPLAY", "REPLAY"])
        self.assertEqual({item["job_id"] for item in result}, {"j1"})
        self.assertEqual(len(records), 1)

    def test_same_key_different_fingerprint_race_conflicts_after_first_reservation(self):
        records = {}
        result = reserve_idempotency_batch(records, [
            {"tenant_id": "t1", "key": "k", "fingerprint": "f1", "proposed_job_id": "j1"},
            {"tenant_id": "t1", "key": "k", "fingerprint": "f2", "proposed_job_id": "j2"},
        ])
        self.assertEqual([item["status"] for item in result], ["CREATED", "CONFLICT"])
        self.assertEqual(records[("t1", "k")], ("f1", "j1"))
        self.assertEqual(len(records), 1)


if __name__ == "__main__":
    unittest.main()
