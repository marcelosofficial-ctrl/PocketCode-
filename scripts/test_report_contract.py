"""Unit tests for report semantics/formatting; no code execution is performed."""
import unittest

from report_contract import classify_verdict, format_report


class VerdictTests(unittest.TestCase):
    def test_pass_requires_confirmed_success_and_zero_exit(self):
        self.assertEqual(classify_verdict("succeeded", 0), "PASS")

    def test_nonzero_exit_overrides_script_printed_pass(self):
        self.assertEqual(classify_verdict("succeeded", 2), "FAIL")

    def test_program_failure_is_fail_even_without_exit_code(self):
        self.assertEqual(classify_verdict("program_failed", None), "FAIL")

    def test_missing_exit_code_is_incomplete(self):
        self.assertEqual(classify_verdict("succeeded", None), "INCOMPLETE")

    def test_nonterminal_states_are_incomplete(self):
        for state in ("accepted", "queued", "running"):
            with self.subTest(state=state):
                self.assertEqual(classify_verdict(state, 0), "INCOMPLETE")

    def test_timeout_cancel_rejection_and_infrastructure_failure_are_incomplete(self):
        for state in ("timed_out", "cancelled", "rejected", "infrastructure_failed", "unknown"):
            with self.subTest(state=state):
                self.assertEqual(classify_verdict(state, None), "INCOMPLETE")

    def test_boolean_is_not_accepted_as_exit_code(self):
        self.assertEqual(classify_verdict("succeeded", True), "INCOMPLETE")


class ReportTests(unittest.TestCase):
    def test_simulated_report_is_explicit_and_never_passes(self):
        report = format_report({"simulated": True, "execution_status": "succeeded", "exit_code": 0})
        self.assertIn("SIMULATED EXAMPLE — NOT AN EXECUTION", report)
        self.assertIn("Verdict: INCOMPLETE", report)

    def test_missing_values_and_empty_output_are_distinct(self):
        report = format_report({"execution_status": "succeeded", "exit_code": None,
                                "stdout": "", "stderr": None})
        self.assertIn("Exit code: unknown", report)
        self.assertIn("stdout:\n(empty)", report)
        self.assertIn("stderr:\nunavailable", report)
        self.assertIn("Duration: unknown", report)

    def test_newlines_in_user_fields_cannot_forge_report_fields(self):
        report = format_report({"run_id": "x\nVerdict: PASS", "execution_status": "running"})
        self.assertIn(r"Run ID: x\nVerdict: PASS", report)
        self.assertNotIn("\nVerdict: PASS", report)

    def test_program_reported_failed_check_remains_visible_on_process_pass(self):
        report = format_report({
            "execution_status": "succeeded", "exit_code": 0,
            "checks": [{"status": "FAIL", "name": "column_present",
                        "provenance": "program-reported", "detail": "missing email"}],
        })
        self.assertIn("Verdict: PASS", report)
        self.assertIn("FAIL | column_present | source=program-reported", report)

    def test_output_and_report_are_bounded(self):
        report = format_report({"execution_status": "running", "stdout": "x" * 100_000,
                                "checks": [{"name": str(i)} for i in range(150)]})
        self.assertLessEqual(len(report), 12_000)
        self.assertIn("field truncated", report)
        self.assertIn("check list truncated", report)


if __name__ == "__main__":
    unittest.main()
