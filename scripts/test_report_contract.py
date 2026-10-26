"""Unit tests for report semantics/formatting; no code execution is performed."""
import math
import unittest

from report_contract import classify_verdict, format_report


class VerdictTests(unittest.TestCase):
    def test_pass_requires_confirmed_success_and_zero_exit(self):
        self.assertEqual(classify_verdict("succeeded", 0), "PASS")

    def test_nonzero_exit_is_fail_for_confirmed_success(self):
        self.assertEqual(classify_verdict("succeeded", 2), "FAIL")

    def test_nonzero_exit_does_not_override_uncertain_lifecycle(self):
        for state, exit_code in (
            ("timed_out", 137),
            ("cancelled", 143),
            ("infrastructure_failed", 1),
            ("rejected", 2),
            ("running", 1),
            ("unknown", 1),
        ):
            with self.subTest(state=state, exit_code=exit_code):
                self.assertEqual(classify_verdict(state, exit_code), "INCOMPLETE")

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

    def test_non_finite_duration_is_unknown(self):
        for duration in (math.nan, math.inf, -math.inf):
            with self.subTest(duration=duration):
                report = format_report({"execution_status": "running", "duration_seconds": duration})
                self.assertIn("Duration: unknown", report)

    def test_actual_output_truncation_is_reported_without_source_flag(self):
        report = format_report({"execution_status": "running", "stdout": "x" * 10_000})
        self.assertIn("stdout: yes", report)
        self.assertIn("field truncated", report)

    def test_actual_check_list_truncation_is_reported_without_source_flag(self):
        report = format_report({
            "execution_status": "running",
            "checks": [{"name": str(i)} for i in range(105)],
        })
        self.assertIn("check list: yes", report)
        self.assertIn("check list truncated: 5 additional item(s) omitted", report)

    def test_malformed_entries_are_disclosed(self):
        report = format_report({
            "execution_status": "running",
            "checks": [{"name": "valid"}, None, "bad-check"],
            "output_files": [{"name": "valid.txt", "size_bytes": 1}, None, "bad-file"],
        })
        self.assertIn("malformed check entr", report)
        self.assertIn("malformed output file entr", report)

    def test_report_cap_preserves_header_and_uncertainty_footer(self):
        report = format_report({
            "execution_status": "running",
            "run_id": "cap-test",
            "stdout": "x" * 100_000,
            "stderr": "y" * 100_000,
            "checks": [{"name": str(i), "detail": "z" * 500} for i in range(150)],
            "output_files": [{"name": str(i), "size_bytes": i} for i in range(80)],
            "notes": ["Execution outcome remains unconfirmed."] + ["n" * 500 for _ in range(20)],
        })
        self.assertLessEqual(len(report), 12_000)
        self.assertIn("Verdict: INCOMPLETE", report)
        self.assertIn("Execution status: running", report)
        self.assertIn("[REPORT TRUNCATED TO SIZE LIMIT]", report)
        self.assertIn("Uncertainty / notes:", report)
        self.assertIn("Execution outcome remains unconfirmed.", report)


if __name__ == "__main__":
    unittest.main()
