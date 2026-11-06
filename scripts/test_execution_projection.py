import unittest

try:
    from execution_projection import (
        ExitObservation, LifecycleObservation, ProgramFailureObservation, project_verdict,
    )
except ModuleNotFoundError:
    from scripts.execution_projection import (
        ExitObservation, LifecycleObservation, ProgramFailureObservation, project_verdict,
    )

A = "attempt-001"


def lifecycle(status, attempt=A, producer="coordinator", sequence=3):
    return LifecycleObservation(attempt, status, producer, sequence)


def child(code, attempt=A, producer="direct_child_wait", sequence=2):
    return ExitObservation(attempt, producer, "natural_exit", sequence, exit_code=code)


def wrapper(code, attempt=A):
    return ExitObservation(attempt, "shell_wrapper", "wrapper_exit", 2, exit_code=code)


class ProjectionTests(unittest.TestCase):
    def test_pass_requires_succeeded_and_natural_child_zero(self):
        got = project_verdict(A, lifecycle("succeeded"), child(0))
        self.assertEqual((got.verdict, got.child_exit_code), ("PASS", 0))

    def test_direct_child_nonzero_is_fail_without_lifecycle(self):
        self.assertEqual(project_verdict(A, None, child(2)).verdict, "FAIL")

    def test_direct_child_nonzero_with_runtime_confirmation_is_fail(self):
        failure = ProgramFailureObservation(A, "trusted_runtime", True, 4)
        self.assertEqual(project_verdict(A, None, child(2), failure).verdict, "FAIL")

    def test_program_failed_plus_direct_child_nonzero_is_fail(self):
        self.assertEqual(project_verdict(A, lifecycle("program_failed"), child(2)).verdict, "FAIL")

    def test_coordinator_program_failed_is_confirmed_without_child_exit(self):
        self.assertEqual(project_verdict(A, lifecycle("program_failed")).verdict, "FAIL")

    def test_trusted_program_failure_can_confirm_program_failed(self):
        failure = ProgramFailureObservation(A, "trusted_runtime", True, 4)
        self.assertEqual(project_verdict(A, lifecycle("program_failed"), program_failure=failure).verdict, "FAIL")

    def test_program_failed_plus_child_zero_is_contradictory(self):
        self.assertEqual(project_verdict(A, lifecycle("program_failed"), child(0)).verdict, "INCOMPLETE")

    def test_succeeded_plus_child_nonzero_is_contradictory(self):
        self.assertEqual(project_verdict(A, lifecycle("succeeded"), child(7)).verdict, "INCOMPLETE")

    def test_timeout_plus_wrapper_137_is_incomplete(self):
        got = project_verdict(A, lifecycle("timed_out"), wrapper(137))
        self.assertEqual(got.verdict, "INCOMPLETE")
        self.assertIsNone(got.child_exit_code)

    def test_timeout_plus_child_137_is_incomplete(self):
        self.assertEqual(project_verdict(A, lifecycle("timed_out"), child(137)).verdict, "INCOMPLETE")

    def test_wrapper_nonzero_never_becomes_child_exit(self):
        got = project_verdict(A, lifecycle("succeeded"), wrapper(2))
        self.assertEqual(got.verdict, "INCOMPLETE")
        self.assertIsNone(got.child_exit_code)

    def test_embedded_system_exit_zero_is_not_native_child_exit(self):
        obs = ExitObservation(A, "embedded_interpreter", "system_exit_requested", 2, exit_code=0)
        self.assertEqual(project_verdict(A, lifecycle("succeeded"), obs).verdict, "INCOMPLETE")

    def test_embedded_system_exit_zero_conflicts_with_program_failed_lifecycle(self):
        obs = ExitObservation(A, "embedded_interpreter", "system_exit_requested", 2, exit_code=0)
        self.assertEqual(project_verdict(A, lifecycle("program_failed"), obs).verdict, "INCOMPLETE")

    def test_embedded_exception_with_coordinator_program_failed_is_fail(self):
        obs = ExitObservation(A, "embedded_interpreter", "embedded_exception", 2)
        self.assertEqual(project_verdict(A, lifecycle("program_failed"), obs).verdict, "FAIL")

    def test_signal_termination_is_not_mapped_to_exit_code(self):
        obs = ExitObservation(A, "direct_child_wait", "signal_terminated", 2, signal_number=9)
        got = project_verdict(A, lifecycle("timed_out"), obs)
        self.assertEqual(got.verdict, "INCOMPLETE")
        self.assertIsNone(got.child_exit_code)

    def test_signal_plus_program_failed_uses_coordinator_failure_not_signal_code(self):
        obs = ExitObservation(A, "provider_child_wait", "signal_terminated", 2, signal_number=9)
        got = project_verdict(A, lifecycle("program_failed"), obs)
        self.assertEqual(got.verdict, "FAIL")
        self.assertIsNone(got.child_exit_code)

    def test_nonterminal_lifecycle_does_not_pass_on_zero(self):
        for state in ("accepted", "queued", "running"):
            with self.subTest(state=state):
                self.assertEqual(project_verdict(A, lifecycle(state), child(0)).verdict, "INCOMPLETE")

    def test_cancel_reject_and_infrastructure_states_stay_incomplete(self):
        for state in ("cancelled", "rejected", "infrastructure_failed"):
            with self.subTest(state=state):
                self.assertEqual(project_verdict(A, lifecycle(state), child(2)).verdict, "INCOMPLETE")

    def test_stale_child_exit_attempt_is_rejected(self):
        got = project_verdict(A, lifecycle("succeeded"), child(0, attempt="attempt-old"))
        self.assertEqual(got.reason, "exit_attempt_mismatch")
        self.assertEqual(got.verdict, "INCOMPLETE")

    def test_stale_lifecycle_attempt_is_rejected(self):
        got = project_verdict(A, lifecycle("succeeded", attempt="attempt-old"), child(0))
        self.assertEqual(got.reason, "lifecycle_attempt_mismatch")
        self.assertEqual(got.verdict, "INCOMPLETE")

    def test_wrong_lifecycle_producer_is_rejected(self):
        got = project_verdict(A, lifecycle("succeeded", producer="submitted_script"), child(0))
        self.assertEqual(got.verdict, "INCOMPLETE")

    def test_wrapper_cannot_claim_direct_child_source(self):
        got = project_verdict(A, lifecycle("succeeded"), child(0, producer="shell_wrapper"))
        self.assertEqual(got.verdict, "INCOMPLETE")

    def test_untrusted_runtime_cannot_confirm_program_failure(self):
        failure = ProgramFailureObservation(A, "submitted_script", True, 4)
        self.assertEqual(project_verdict(A, lifecycle("program_failed"), program_failure=failure).verdict, "INCOMPLETE")

    def test_failure_confirmation_must_be_literal_boolean(self):
        failure = ProgramFailureObservation(A, "trusted_runtime", 1, 4)
        self.assertEqual(project_verdict(A, lifecycle("program_failed"), program_failure=failure).verdict, "INCOMPLETE")

    def test_bool_is_not_a_valid_child_exit_code(self):
        self.assertEqual(project_verdict(A, lifecycle("succeeded"), child(True)).verdict, "INCOMPLETE")

    def test_bool_is_not_a_valid_sequence(self):
        obs = LifecycleObservation(A, "succeeded", "coordinator", True)
        self.assertEqual(project_verdict(A, obs, child(0)).verdict, "INCOMPLETE")

    def test_unknown_lifecycle_status_is_rejected(self):
        self.assertEqual(project_verdict(A, lifecycle("complete"), child(0)).verdict, "INCOMPLETE")

    def test_empty_attempt_id_is_rejected(self):
        self.assertEqual(project_verdict(" ", lifecycle("succeeded"), child(0)).verdict, "INCOMPLETE")

    def test_no_evidence_is_incomplete(self):
        self.assertEqual(project_verdict(A, None).verdict, "INCOMPLETE")

    def test_success_conflicts_with_confirmed_failure(self):
        failure = ProgramFailureObservation(A, "provider_runtime", True, 4)
        self.assertEqual(project_verdict(A, lifecycle("succeeded"), child(0), failure).verdict, "INCOMPLETE")

    def test_confirmed_failure_conflicts_with_nonterminal_lifecycle(self):
        failure = ProgramFailureObservation(A, "trusted_runtime", True, 4)
        self.assertEqual(project_verdict(A, lifecycle("running"), program_failure=failure).verdict, "INCOMPLETE")


if __name__ == "__main__":
    unittest.main(verbosity=2)
