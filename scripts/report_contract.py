"""Pure report-contract helpers; this module does not execute submitted code.

Input data must come from a caller. These helpers format evidence; they are not
a runner, provider adapter, API, or source of trusted execution metadata.
"""
from __future__ import annotations

import math
from typing import Any, Mapping

KNOWN_STATUSES = {
    "accepted", "queued", "running", "succeeded", "program_failed",
    "timed_out", "cancelled", "rejected", "infrastructure_failed",
}
MAX_FIELD_CHARS = 2_000
MAX_OUTPUT_CHARS = 4_000
MAX_CHECKS = 100
MAX_FILES = 50
MAX_REPORT_CHARS = 12_000


def _safe_text(value: Any, limit: int = MAX_FIELD_CHARS) -> str:
    """Convert a value to bounded single-line text, escaping control characters."""
    text = str(value)
    safe = "".join(
        ch if ch.isprintable() and ch not in "\r\n\t" else {
            "\r": r"\r", "\n": r"\n", "\t": r"\t"
        }.get(ch, "?")
        for ch in text
    )
    if len(safe) > limit:
        return safe[:limit] + "…[field truncated]"
    return safe


def classify_verdict(execution_status: Any, exit_code: Any = None) -> str:
    """Return PASS/FAIL/INCOMPLETE from authoritative lifecycle evidence.

    A nonzero exit code is a program failure only when the authoritative
    lifecycle status is succeeded. Exit codes attached to timeout, cancellation,
    rejection, infrastructure failure, or nonterminal states may be stale or
    belong to an interrupted attempt, so those states remain INCOMPLETE.
    """
    status = execution_status if isinstance(execution_status, str) else ""
    valid_exit = isinstance(exit_code, int) and not isinstance(exit_code, bool)

    if status == "program_failed":
        return "FAIL"
    if status == "succeeded" and valid_exit:
        return "PASS" if exit_code == 0 else "FAIL"
    return "INCOMPLETE"


def _finite_nonnegative_number(value: Any) -> bool:
    """Return whether a duration is a finite, nonnegative numeric value."""
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return False
    try:
        return math.isfinite(value) and value >= 0
    except (OverflowError, TypeError, ValueError):
        return False


def format_report(result: Mapping[str, Any]) -> str:
    """Render bounded, plain-text report fields from supplied result metadata.

    This formatter does not verify the trustworthiness of its input. Production
    callers must supply status/exit evidence from an authoritative runner.
    """
    simulated = bool(result.get("simulated", False))
    status_value = result.get("execution_status")
    status = status_value if isinstance(status_value, str) and status_value in KNOWN_STATUSES else "unknown"
    exit_code = result.get("exit_code")
    if not isinstance(exit_code, int) or isinstance(exit_code, bool):
        exit_code = None
    verdict = "INCOMPLETE" if simulated else classify_verdict(status, exit_code)

    lines = ["POCKETCODE RUN REPORT", "Report format: 1"]
    if simulated:
        lines.append("SIMULATED EXAMPLE — NOT AN EXECUTION")
    lines.extend([
        f"Run ID: {_safe_text(result.get('run_id', 'unknown'))}",
        f"Verdict: {verdict}",
        f"Execution status: {status}",
        f"Runtime: {_safe_text(result.get('runtime', 'unknown'))}",
        f"Exit code: {exit_code if exit_code is not None else 'unknown'}",
    ])

    duration = result.get("duration_seconds")
    if _finite_nonnegative_number(duration):
        lines.append(f"Duration: {duration:g} s")
    else:
        lines.append("Duration: unknown")
    lines.extend([
        f"Evidence source: {_safe_text(result.get('evidence_source', 'unknown'))}",
        f"Task summary: {_safe_text(result.get('task_summary', 'unspecified'))}",
        "",
        "CHECKS (provenance must be explicit)",
    ])

    diagnostic_notes = []
    checks = result.get("checks", [])
    if not isinstance(checks, list):
        diagnostic_notes.append("Malformed checks container omitted; expected a list.")
        checks = []
    visible_checks = checks[:MAX_CHECKS]
    malformed_checks = sum(not isinstance(check, Mapping) for check in visible_checks)
    if malformed_checks:
        diagnostic_notes.append(f"{malformed_checks} malformed check entr{'y' if malformed_checks == 1 else 'ies'} omitted.")
    for check in visible_checks:
        if not isinstance(check, Mapping):
            continue
        check_status = _safe_text(check.get("status", "unknown"), 32).upper()
        name = _safe_text(check.get("name", "unnamed"), 160)
        provenance = _safe_text(check.get("provenance", "unspecified"), 64)
        detail = _safe_text(check.get("detail", ""), 500)
        lines.append(f"- {check_status} | {name} | source={provenance} | {detail}")
    if len(checks) > MAX_CHECKS:
        lines.append(f"- [check list truncated: {len(checks) - MAX_CHECKS} additional item(s) omitted]")
    if not checks:
        lines.append("- none reported")

    rendered_outputs = {}
    output_truncated = {}
    for key in ("stdout", "stderr"):
        raw = result.get(key)
        if raw is None:
            value = "unavailable"
        elif raw == "":
            value = "(empty)"
        else:
            value = _safe_text(raw, MAX_OUTPUT_CHARS)
        source_truncated_flag = result.get(f"{key}_truncated", False)
        source_says_truncated = source_truncated_flag is True
        if not isinstance(source_truncated_flag, bool):
            diagnostic_notes.append(
                f"Invalid {key}_truncated flag ignored; expected a boolean."
            )
        was_truncated = source_says_truncated or value.endswith("[field truncated]")
        output_truncated[key] = was_truncated
        if source_says_truncated and not value.endswith("[field truncated]"):
            value += " …[output truncated by source]"
        rendered_outputs[key] = value
        lines.extend(["", key + ":", value])

    lines.extend(["", "Output files:"])
    files = result.get("output_files", [])
    if not isinstance(files, list):
        diagnostic_notes.append("Malformed output files container omitted; expected a list.")
        files = []
    visible_files = files[:MAX_FILES]
    malformed_files = sum(not isinstance(item, Mapping) for item in visible_files)
    if malformed_files:
        diagnostic_notes.append(
            f"{malformed_files} malformed output file entr{'y' if malformed_files == 1 else 'ies'} omitted."
        )
    rendered_files = 0
    for item in visible_files:
        if not isinstance(item, Mapping):
            continue
        name = _safe_text(item.get("name", "unnamed"), 180)
        size = item.get("size_bytes")
        size_text = str(size) if isinstance(size, int) and not isinstance(size, bool) and size >= 0 else "unknown"
        lines.append(f"- {name} ({size_text} bytes)")
        rendered_files += 1
    if not rendered_files:
        lines.append("- none reported")
    if len(files) > MAX_FILES:
        lines.append(f"- [file list truncated: {len(files) - MAX_FILES} additional item(s) omitted]")

    check_list_truncated = bool(result.get("check_list_truncated", False)) or len(checks) > MAX_CHECKS
    file_list_truncated = bool(result.get("file_list_truncated", False)) or len(files) > MAX_FILES
    lines.extend(["", "Truncation:"])
    lines.append(f"- stdout: {'yes' if output_truncated['stdout'] else 'no'}")
    lines.append(f"- stderr: {'yes' if output_truncated['stderr'] else 'no'}")
    lines.append(f"- check list: {'yes' if check_list_truncated else 'no'}")
    lines.append(f"- file list: {'yes' if file_list_truncated else 'no'}")

    notes = result.get("notes", [])
    lines.extend(["", "Uncertainty / notes:"])
    if isinstance(notes, list) and notes:
        lines.extend(f"- {_safe_text(note, 500)}" for note in notes[:20])
    else:
        lines.append("- No additional notes supplied.")
    lines.extend(f"- {note}" for note in diagnostic_notes)

    report = "\n".join(lines)
    if len(report) > MAX_REPORT_CHARS:
        # Preserve the complete evidence header and a truthful, explicit footer.
        # Middle details are lower priority and may be shortened to fit.
        header_end = next(
            (i for i, line in enumerate(lines) if line.startswith("Task summary:")),
            min(len(lines) - 1, 10),
        )
        header = "\n".join(lines[:header_end + 1])
        footer_lines = [
            "[REPORT TRUNCATED TO SIZE LIMIT]",
            "",
            "Uncertainty / notes:",
            "- Report shortened to fit the size limit; checks, output, files, or notes may be omitted.",
        ]
        if verdict == "INCOMPLETE":
            footer_lines.append("- Execution outcome remains unconfirmed.")
        footer = "\n".join(footer_lines)
        middle = "\n".join(lines[header_end + 1:])
        available_middle = max(0, MAX_REPORT_CHARS - len(header) - len(footer) - 2)
        report = header + "\n" + middle[:available_middle].rstrip() + "\n" + footer
    return report
