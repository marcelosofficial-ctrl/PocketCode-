#!/usr/bin/env python3
"""Dependency-free static checks for the simulated PocketCode task-receipt prototype.

These checks inspect source text only. They do not execute JavaScript or submitted Python.
"""
from collections import Counter
import hashlib
import html as html_lib
from pathlib import Path
import re
import sys

HTML_PATH = Path("prototypes/mobile-runner/index.html")


def main() -> int:
    html = HTML_PATH.read_text(encoding="utf-8")
    errors: list[str] = []
    ids = re.findall(r'\bid=["\']([^"\']+)["\']', html)
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    if duplicates:
        errors.append("Duplicate HTML IDs: " + ", ".join(duplicates))
    declared = set(ids)
    referenced = set(re.findall(r"getElementById\(['\"]([^'\"]+)['\"]\)", html))
    missing = sorted(referenced - declared)
    if missing:
        errors.append("getElementById references missing IDs: " + ", ".join(missing))

    actions = {"codeTab", "inputTab", "successExample", "failureExample", "copyReport", "copyPrompt"}
    for element_id in sorted(actions):
        pattern = rf"getElementById\(['\"]{re.escape(element_id)}['\"]\)\.addEventListener\(['\"]click['\"]"
        if not re.search(pattern, html):
            errors.append(f"Expected example/control handler missing for #{element_id}")

    if 'name="viewport"' not in html or "width=device-width" not in html:
        errors.append("Missing responsive viewport metadata")
    if len(re.findall(r"<h1\b", html, re.IGNORECASE)) != 1:
        errors.append("Expected exactly one primary <h1> heading")

    for index, attrs in enumerate(re.findall(r"<textarea\b([^>]*)>", html, re.IGNORECASE), start=1):
        if not re.search(r"\baria-label\s*=", attrs, re.IGNORECASE):
            errors.append(f"Textarea {index} is missing an accessible label")

    for phrase in (
        "SIMULATED EXAMPLE — NOT AN EXECUTION",
        "Your code is not executed.",
        "NOT_APPLICABLE — NO JOB WAS DISPATCHED",
        "NOT MEASURED",
        "NOT SELECTED / NOT RUN",
        "NOT OBSERVED",
        "NOT IMPLEMENTED / NOT AUTHORIZED",
        "EXPECTED SUCCESS EXAMPLE",
        "EXPECTED FAILURE EXAMPLE",
        "NOT_CREATED (fresh-workspace fixture expectation)",
        "summary.json",
        "items.csv",
        "main.py",
        "Copy example report",
    ):
        if phrase not in html:
            errors.append(f"Missing task/evidence content: {phrase!r}")

    source_match = re.search(r'<code id="sourceCode">(.*?)</code>', html, re.DOTALL)
    if not source_match:
        errors.append("Canonical main.py source block is missing")
    else:
        source = html_lib.unescape(source_match.group(1))
        source_bytes = source.encode("utf-8")
        if len(source_bytes) != 1939 or hashlib.sha256(source_bytes).hexdigest() != "70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7":
            errors.append("Embedded main.py does not match the frozen canonical SHA-256")

    input_match = re.search(r'<pre class="csv" id="inputData">(.*?)</pre>', html, re.DOTALL)
    expected_input = "item,quantity,unit_price\nnotebook,2,3.50\npen,3,1.25\n"
    if not input_match or html_lib.unescape(input_match.group(1)) != expected_input:
        errors.append("Initial items.csv does not match the canonical success fixture")

    if re.search(r"\b0\.18s\b|\b0\.04s\b|Python 3\.x", html):
        errors.append("Fabricated duration or unselected runtime label remains")
    if re.search(r"\bid=[\"']runButton[\"']|\bRun\s*</button>|download\s*=", html, re.IGNORECASE):
        errors.append("Fake Run or downloadable sample artifact control is not allowed")

    for tab_id, panel_id in (("codeTab", "codePanel"), ("inputTab", "inputPanel")):
        match = re.search(rf"<button\b(?=[^>]*\bid=[\"']{tab_id}[\"'])([^>]*)>", html, re.IGNORECASE)
        if not match or not re.search(r"\brole=[\"']tab[\"']", match.group(1), re.IGNORECASE):
            errors.append(f"#{tab_id} is missing role=tab")
        elif not re.search(rf"\baria-controls=[\"']{panel_id}[\"']", match.group(1), re.IGNORECASE):
            errors.append(f"#{tab_id} is missing aria-controls={panel_id}")
        panel = re.search(rf"<section\b(?=[^>]*\bid=[\"']{panel_id}[\"'])([^>]*)>", html, re.IGNORECASE)
        if not panel or not re.search(rf"\baria-labelledby=[\"']{tab_id}[\"']", panel.group(1), re.IGNORECASE):
            errors.append(f"#{panel_id} is missing aria-labelledby={tab_id}")

    if not re.search(r"\bArrowLeft\b", html) or not re.search(r"\bArrowRight\b", html) or not re.search(r"\bHome\b", html) or not re.search(r"\bEnd\b", html):
        errors.append("Tab keyboard navigation must support arrows, Home and End")
    if not re.search(r"aria-live=[\"\']polite[\"\']", html, re.IGNORECASE):
        errors.append("Missing aria-live status/output region")
    code_tab = re.search(r'<button[^>]*id="codeTab"[^>]*>', html)
    input_tab = re.search(r'<button[^>]*id="inputTab"[^>]*>', html)
    if not code_tab or 'tabindex="0"' not in code_tab.group(0):
        errors.append("Selected code tab must start with tabindex=0")
    if not input_tab or 'tabindex="-1"' not in input_tab.group(0):
        errors.append("Inactive input tab must start with tabindex=-1")
    if "codeTab.setAttribute('tabindex',isCode?'0':'-1')" not in html:
        errors.append("Code tab selection does not update the roving tabindex")
    if "inputTab.setAttribute('tabindex',isCode?'-1':'0')" not in html:
        errors.append("Input tab selection does not update the roving tabindex")

    prompt = re.search(r"getElementById\(['\"]copyPrompt['\"]\)\.addEventListener\(['\"]click['\"],\s*\(\)=>\s*\{(.*?)\}\);", html, re.DOTALL)
    if not prompt:
        errors.append("Could not locate debugging-prompt handler")
    else:
        for required in ("sourceCode.textContent", "inputData.textContent", "report()"):
            if required not in prompt.group(1):
                errors.append(f"Debugging prompt omits {required}")

    if not re.search(r'id=["\']copyFallback["\'][^>]*readonly', html, re.IGNORECASE):
        errors.append("Visible selectable-text fallback is missing")
    if "Clipboard unavailable. Select and copy the text in the fallback box." not in html:
        errors.append("Clipboard failure does not point to selectable fallback")

    if errors:
        print("Prototype static checks FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Prototype static checks passed:")
    print(f"- {len(ids)} HTML IDs; no duplicates")
    print(f"- {len(referenced)} getElementById references all resolve")
    print(f"- {len(actions)} expected example/control handlers are present")
    print("- canonical task and fixture names are represented")
    print("- simulated evidence, artifact, cleanup and release states are explicit")
    print("- fabricated runtime/timing and fake execution/download controls are absent")
    print("- tab relationships, keyboard navigation and fallback copy text are present")
    print("Note: static checks do not execute browser JavaScript or submitted Python.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
