"""Pure report-contract helpers; this module does not execute submitted code.

Input data must come from a caller. These helpers format evidence; they are not
a runner, provider adapter, API, or source of trusted execution metadata.
"""
from __future__ import annotations

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
    """Return PASS/FAIL/INCOMPLETE from terminal evidence only.

    PASS requires status=succeeded and exit_code=0. A confirmed nonzero exit or
    program_failed status is FAIL. Nonterminal/unknown/uncertain states are
    INCOMPLETE. Script-printed text is deliberately not an input to this rule.
    """
    status = execution_status if isinstance(execution_status, str) else ""
    valid_exit = isinstance(exit_code, int) and not isinstance(exit_code, bool)

    if (valid_exit and exit_code != 0) or status == "program_failed":
        return "FAIL"
    if status == "succeeded" and valid_exit and exit_code == 0:
        return "PASS"
    return "INCOMPLETE"


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
    if isinstance(duration, (int, float)) and not isinstance(duration, bool) and duration >= 0:
        lines.append(f"Duration: {duration:g} s")
    else:
        lines.append("Duration: unknown")
    lines.extend([
        f"Evidence source: {_safe_text(result.get('evidence_source', 'unknown'))}",
        f"Task summary: {_safe_text(result.get('task_summary', 'unspecified'))}",
        "",
        "CHECKS (provenance must be explicit)",
    ])

    checks = result.get("checks", [])
    if not isinstance(checks, list):
        checks = []
    for check in checks[:MAX_CHECKS]:
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

    for key in ("stdout", "stderr"):
        raw = result.get(key)
        if raw is None:
            value = "unavailable"
        elif raw == "":
            value = "(empty)"
        else:
            value = _safe_text(raw, MAX_OUTPUT_CHARS)
        truncated = bool(result.get(f"{key}_truncated", False))
        if truncated and not value.endswith("[field truncated]"):
            value += " …[output truncated by source]"
        lines.extend(["", key + ":", value])

    lines.extend(["", "Output files:"])
    files = result.get("output_files", [])
    if not isinstance(files, list):
        files = []
    rendered_files = 0
    for item in files[:MAX_FILES]:
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

    lines.extend(["", "Truncation:"])
    for key in ("stdout", "stderr", "check list"):
        source_key = key.replace(" ", "_") + "_truncated"
        lines.append(f"- {key}: {'yes' if bool(result.get(source_key, False)) else 'no'}")
    notes = result.get("notes", [])
    lines.extend(["", "Uncertainty / notes:"])
    if isinstance(notes, list) and notes:
        lines.extend(f"- {_safe_text(note, 500)}" for note in notes[:20])
    else:
        lines.append("- No additional notes supplied.")

    report = "\n".join(lines)
    if len(report) > MAX_REPORT_CHARS:
        report = report[:MAX_REPORT_CHARS - 32] + "\n[REPORT TRUNCATED TO SIZE LIMIT]"
    return report
