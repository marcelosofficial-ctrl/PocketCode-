"""Regression tests for the dependency-free prototype source checker."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECKER = Path(__file__).with_name("check_mobile_prototype.py").resolve()

VALID_HTML = """
<button id="codeTab"></button><button id="csvTab"></button>
<button id="runButton"></button><button id="errorButton"></button>
<button id="copyReport"></button><button id="copyPrompt"></button>
<script>
const codeTab = document.getElementById('codeTab');
const csvTab = document.getElementById('csvTab');
codeTab.addEventListener('click', () => {});
csvTab.addEventListener('click', () => {});
document.getElementById('runButton').addEventListener('click', () => {});
document.getElementById('errorButton').addEventListener('click', () => {});
document.getElementById('copyReport').addEventListener('click', () => {});
document.getElementById('copyPrompt').addEventListener('click', ()=>copyText(
  editor.value + csv.textContent + report()
));
</script>
SIMULATED EXECUTION ONLY
Your code is not executed.
POCKETCODE DEMO REPORT (SIMULATED)
No code was executed.
"""


class PrototypeCheckerTests(unittest.TestCase):
    def run_checker(self, html: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "prototypes" / "mobile-runner"
            target.mkdir(parents=True)
            (target / "index.html").write_text(html, encoding="utf-8")
            return subprocess.run(
                [sys.executable, str(CHECKER)],
                cwd=tmp,
                text=True,
                capture_output=True,
                check=False,
            )

    def test_accepts_valid_source_with_cached_and_direct_handlers(self) -> None:
        result = self.run_checker(VALID_HTML)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("6 expected UI click handlers", result.stdout)

    def test_rejects_duplicate_ids(self) -> None:
        result = self.run_checker(VALID_HTML.replace(
            '<button id="codeTab"></button>',
            '<button id="codeTab"></button><span id="codeTab"></span>',
        ))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Duplicate HTML IDs: codeTab", result.stdout)

    def test_rejects_missing_referenced_id(self) -> None:
        html = VALID_HTML.replace(
            "document.getElementById('runButton').addEventListener('click', () => {});",
            "document.getElementById('missingButton').addEventListener('click', () => {});",
        )
        result = self.run_checker(html)
        self.assertEqual(result.returncode, 1)
        self.assertIn("references missing IDs: missingButton", result.stdout)

    def test_rejects_missing_simulation_disclaimer(self) -> None:
        result = self.run_checker(VALID_HTML.replace("No code was executed.", ""))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing simulation disclaimer/marker", result.stdout)

    def test_rejects_prompt_that_omits_csv(self) -> None:
        result = self.run_checker(VALID_HTML.replace(
            "editor.value + csv.textContent + report()",
            "editor.value + report()",
        ))
        self.assertEqual(result.returncode, 1)
        self.assertIn("debugging prompt no longer includes csv.textContent", result.stdout)


if __name__ == "__main__":
    unittest.main()
