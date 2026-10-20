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

    # Lightweight accessibility/mobile smoke checks. These are source heuristics, not an audit.
    if 'name="viewport"' not in html or "width=device-width" not in html:
        errors.append("Missing responsive viewport metadata")
    if len(re.findall(r"<h1\\b", html, re.IGNORECASE)) != 1:
        errors.append("Expected exactly one primary <h1> heading")

    textareas = re.findall(r"<textarea\\b([^>]*)>", html, re.IGNORECASE)
    for index, attrs in enumerate(textareas, start=1):
        if not re.search(r"\\baria-label\\s*=", attrs, re.IGNORECASE) and not re.search(
            r"\\baria-labelledby\\s*=", attrs, re.IGNORECASE
        ):
            errors.append(f"Textarea {index} is missing an accessible label")

    buttons = re.findall(r"<button\\b([^>]*)>(.*?)</button>", html, re.IGNORECASE | re.DOTALL)
    for index, (attrs, inner) in enumerate(buttons, start=1):
        visible_text = re.sub(r"<[^>]+>", "", inner).strip()
        has_label = re.search(r"\\baria-label\\s*=", attrs, re.IGNORECASE)
        if not visible_text and not has_label:
            errors.append(f"Button {index} has no detectable accessible name")

    for tab_id in ("codeTab", "csvTab"):
        tab_match = re.search(
            rf"<button\\b(?=[^>]*\\bid=[\\\"]{tab_id}[\\\"])([^>]*)>",
            html,
            re.IGNORECASE,
        )
        if not tab_match or not re.search(r"\\brole=[\\\"]tab[\\\"]", tab_match.group(1), re.IGNORECASE):
            errors.append(f"#{tab_id} is missing role=tab")
        elif not re.search(r"\\baria-selected=[\\\"](?:true|false)[\\\"]", tab_match.group(1), re.IGNORECASE):
            errors.append(f"#{tab_id} is missing aria-selected state")

    if not re.search(r"\\baria-live=[\\\"](?:polite|assertive)[\\\"]", html, re.IGNORECASE):
        errors.append("Missing aria-live region for status/output updates")

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
    print("- basic mobile/accessibility source heuristics are satisfied")
    print("- debugging prompt includes editor code, sample CSV, and report")
    print("Note: these checks do not run browser interactions or submitted code.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
