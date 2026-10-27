"""Synthetic lifecycle tests only; no user code or provider is executed."""
import unittest

from lifecycle_contract import (
    IdempotencyConflict, OutputBudget, artifact_release_allowed,
    canonical_request_fingerprint, derive_disposition,
    reduce_terminal_events, reserve_idempotency,
)


class LifecycleTests(unittest.TestCase):
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

    def test_duplicate_event_is_idempotent_but_conflict_is_marked(self):
        event = {"event_id": "e1", "sequence": 1, "kind": "exit_zero", "payload": {"exit": 0}}
        result = reduce_terminal_events([event, dict(event)])
        self.assertEqual(len(result["events"]), 1)
        conflict = reduce_terminal_events([event, {
            "event_id": "e1", "sequence": 2, "kind": "timeout", "payload": {"exit": 0}
        }])
        self.assertTrue(conflict["contradictory_evidence"])

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
        budget.add("stdout", b"prefix secret=alpha-")
        budget.add("stdout", b"beta-token suffix")
        budget.finish()
        retained = budget.retained_bytes("stdout")
        self.assertNotIn(b"alpha-beta-token", retained)
        self.assertIn(b"*" * len(b"secret=alpha-beta-token"), retained)


if __name__ == "__main__":
    unittest.main()
