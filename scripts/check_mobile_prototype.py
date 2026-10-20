#!/usr/bin/env python3
"""Dependency-free source checks for the PocketCode mobile prototype.

These checks catch common static regressions; they do not execute browser JavaScript
or verify that the UI works in a real browser.
"""
from collections import Counter
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

    required_actions = {
        "codeTab", "csvTab", "runButton", "errorButton", "copyReport", "copyPrompt"
    }
    for element_id in sorted(required_actions):
        pattern = rf"(?:getElementById\(['\"]{re.escape(element_id)}['\"]\)|\b{re.escape(element_id)})\.addEventListener\(['\"]click['\"]"
        if not re.search(pattern, html):
            errors.append(f"Expected click handler missing for #{element_id}")

    required_phrases = [
        "SIMULATED EXECUTION ONLY",
        "Your code is not executed.",
        "POCKETCODE DEMO REPORT (SIMULATED)",
        "No code was executed.",
    ]
    for phrase in required_phrases:
        if phrase not in html:
            errors.append(f"Missing simulation disclaimer/marker: {phrase!r}")

    prompt_match = re.search(
        r"getElementById\(['\"]copyPrompt['\"]\)\.addEventListener\(['\"]click['\"],\s*\(\)=>copyText\((.*?)\)\);",
        html,
        re.DOTALL,
    )
    if not prompt_match:
        errors.append("Could not locate the debugging-prompt copy handler")
    else:
        prompt_handler = prompt_match.group(1)
        for required in ("editor.value", "csv.textContent", "report()"):
            if required not in prompt_handler:
                errors.append(f"Debugging prompt no longer includes {required}")

    if errors:
        print("Prototype static checks FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Prototype static checks passed:")
    print(f"- {len(ids)} HTML IDs; no duplicates")
    print(f"- {len(referenced)} getElementById references all resolve")
    print(f"- {len(required_actions)} expected UI click handlers are present")
    print("- simulated-execution disclaimers are present")
    print("- debugging prompt includes editor code, sample CSV, and report")
    print("Note: these checks do not run browser interactions or submitted code.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
