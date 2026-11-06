"""Regression tests for the dependency-free mobile prototype checker."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

CHECKER = Path(__file__).with_name("check_mobile_prototype.py").resolve()

VALID_HTML = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<h1>Fixture</h1>
<div>SIMULATED EXAMPLE — NOT AN EXECUTION Your code is not executed.</div>
<div>NOT_APPLICABLE — NO JOB WAS DISPATCHED NOT MEASURED NOT SELECTED / NOT RUN NOT OBSERVED NOT IMPLEMENTED / NOT AUTHORIZED</div>
<div>EXPECTED SUCCESS EXAMPLE EXPECTED FAILURE EXAMPLE NOT_CREATED (fresh-workspace fixture expectation)</div>
<div>main.py items.csv summary.json Copy example report</div>
<textarea id="copyFallback" aria-label="Fallback" readonly></textarea>
<section aria-live="polite"></section>
<button id="codeTab" role="tab" aria-selected="true" aria-controls="codePanel">Code</button>
<button id="inputTab" role="tab" aria-selected="false" aria-controls="inputPanel">Input</button>
<section id="codePanel" role="tabpanel" aria-labelledby="codeTab"></section>
<section id="inputPanel" role="tabpanel" aria-labelledby="inputTab"></section>
<button id="successExample">Show success expectation</button>
<button id="failureExample">Show malformed-header expectation</button>
<button id="copyReport">Copy example report</button>
<button id="copyPrompt">Copy debugging prompt</button>
<script>
const sourceCode = {textContent: "source"};
const inputData = {textContent: "input"};
function report(){return "report";}
document.getElementById('codeTab').addEventListener('click',()=>{});
document.getElementById('inputTab').addEventListener('click',()=>{});
document.getElementById('successExample').addEventListener('click',()=>{});
document.getElementById('failureExample').addEventListener('click',()=>{});
document.getElementById('copyReport').addEventListener('click',()=>{});
document.getElementById('copyPrompt').addEventListener('click',()=>{const p=sourceCode.textContent+inputData.textContent+report();});
const keys = ['ArrowLeft','ArrowRight','Home','End'];
const fallback = 'Clipboard unavailable. Select and copy the text in the fallback box.';
</script>
"""

class PrototypeCheckerTests(unittest.TestCase):
    def run_checker(self, html: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "prototypes" / "mobile-runner"
            target.mkdir(parents=True)
            (target / "index.html").write_text(html, encoding="utf-8")
            return subprocess.run([sys.executable, str(CHECKER)], cwd=tmp, text=True, capture_output=True, check=False)

    def test_accepts_aligned_static_prototype(self):
        result = self.run_checker(VALID_HTML)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("6 expected example/control handlers", result.stdout)

    def test_rejects_duplicate_ids(self):
        html = VALID_HTML.replace('<h1>Fixture</h1>', '<h1>Fixture</h1><span id="codeTab"></span>')
        result = self.run_checker(html)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Duplicate HTML IDs", result.stdout)

    def test_rejects_missing_task_label(self):
        result = self.run_checker(VALID_HTML.replace("items.csv", "input.csv"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Missing task/evidence content", result.stdout)

    def test_rejects_fabricated_duration(self):
        result = self.run_checker(VALID_HTML.replace("NOT MEASURED", "0.18s"))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Fabricated duration", result.stdout)

    def test_rejects_fake_run_button(self):
        result = self.run_checker(VALID_HTML.replace('<button id="successExample">', '<button id="runButton">Run</button><button id="successExample">'))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Fake Run", result.stdout)

    def test_rejects_broken_tab_relationship(self):
        result = self.run_checker(VALID_HTML.replace('aria-controls="codePanel"', 'aria-controls="missingPanel"'))
        self.assertEqual(result.returncode, 1)
        self.assertIn("aria-controls=codePanel", result.stdout)

    def test_rejects_prompt_without_input(self):
        html = VALID_HTML.replace("inputData.textContent", "inputData.value")
        result = self.run_checker(html)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Debugging prompt omits inputData.textContent", result.stdout)

if __name__ == "__main__":
    unittest.main()
