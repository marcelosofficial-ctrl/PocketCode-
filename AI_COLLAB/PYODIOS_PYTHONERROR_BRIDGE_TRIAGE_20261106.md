# Pyodios PythonError bridge triage — 2026-11-06

**Status:** One owner-reported Editor attempt; underlying cause and artifact outcome UNKNOWN. A separate diagnostic wrapper passed two isolated CPython checks but has NOT been run on the phone.
**Authority:** No change to canonical fixture, LOOP/CASE/D acceptance, runtime/provider selection, security boundary or $0 budget.

## Observed attempt

The owner reports that `main.py` and renamed `items.csv` are in the same Pyodios project, the green whole-file Editor play control was tapped, and the complete visible output was exactly `[Bridge/executePython] PythonError`. No traceback or other output was visible.

- **DIRECTLY OBSERVED (owner-reported):** files added to project; green Editor run invoked; exact visible result above.
- **UNKNOWN:** whether `summary.json` was created in the Python session/project; whether `items.csv` was visible to the active Python working folder; the underlying Python exception; whether stderr was surfaced separately; the script-requested exit value.
- **NOT RUN:** malformed-input case, artifact export/read-back, normal relaunch persistence, interruption/recovery and PocketCode acceptance.
- No PASS or FAIL is assigned from the bridge label alone.

The canonical fixture is unchanged. Its final entrypoint is `raise SystemExit(main())`; the main function requests exit value 0 on success and 2 for its handled file/validation errors.

## Ranked gaps

| Rank | Gap | Reason and action |
|---|---|---|
| 1 | Pyodios bridge error has no visible root cause | First hands-on observation is inconclusive. Inspect an existing `summary.json` and timestamped Error Log before rerunning. |
| 2 | CLI exit semantics differ from embedded-interpreter semantics | `SystemExit` is an exception, not a native child-process result. Preserve the fixture and use a separate catch-and-report wrapper only if no artifact exists and the log is unhelpful. |
| 3 | Project and Python working-folder sync | Files added externally while a project is open may not reach Python until the project is reopened. Reopen after external file changes. |
| 4 | Generic exit-code provenance is underspecified | The integer may be child exit, wrapper exit, forced termination, stale or contradictory evidence. Resolve typed provenance before changing `classify_verdict()`. |
| 5 | Interruption and cleanup guarantees are weak | Pyodios says running Python cannot be interrupted; the 120-second UI timeout does not stop it. Avoid long/infinite tests and do not infer termination. |

## Verified primary-source findings

### `PythonError`

Pyodide 314.0.5 says Python exceptions crossing Python/JavaScript entry or exit boundaries are converted into JavaScript `PythonError` exceptions. The error has a formatted traceback; the underlying exception remains accessible inside Python as `sys.last_value`. Therefore `PythonError` is a bridge-level exception type, not the root-cause description or a verdict. Exact-version documentation: https://pyodide.org/en/314.0.5/usage/type-conversions.html

### `SystemExit` hypothesis

Python documents `sys.exit()` as raising `SystemExit`, which an outer caller can intercept. The fixture deliberately raises it with `main()`'s return value. This makes `SystemExit` a credible lead, not a confirmed diagnosis. I also checked the exact Pyodide 314.0.5 source tag (`src/core/error_handling.c`): its `wrap_exception_inner()` comments that `PyErr_Print()` calls `exit()` for `SystemExit` when `PyConfig.inspect` is not set, and that Pyodide generally sets `inspect` except in the CLI runner. Pyodios does not document its value, so we cannot conclude how its Editor handles this case. Missing `items.csv` could cause the fixture to request exit 2; ordinary Python exceptions can also cross the bridge. Exact source: https://github.com/pyodide/pyodide/blob/314.0.5/src/core/error_handling.c. Other sources: https://docs.python.org/3.14/library/sys.html and https://pyodide.org/en/314.0.5/usage/type-conversions.html

### Files and diagnostic log

Pyodios says the open project is the Python working directory. The project folder and Python session folder are copied at defined moments, not continuously; files added externally while a project is open are not visible until the project is reopened. Outputs created by Python should appear in the project Files tab after the cell finishes. Source: https://pyodios.caffeinatedmath.com/guide/projects

Pyodios documents **Settings → Diagnostics → Error Logs → View Error Log**, with timestamps and error details. The app warns that Python code can appear in error messages; inspect and redact before sharing. Source: https://pyodios.caffeinatedmath.com/guide/settings

Pyodios v1.1.0 says Python code cannot be interrupted once it starts. A 120-second UI timeout returns control while code continues in the background. Do not use an infinite loop or timeout as a termination test. Source: https://pyodios.caffeinatedmath.com/faq

Pyodios credits Pyodide, CPython, Comlink and micropip and lists their bundled licences, but this does not establish that Pyodios' own app/bridge source is open source. No app source repository or app-source licence was verified in this pass. Do not copy or claim reuse rights over its bridge. Source: https://pyodios.caffeinatedmath.com/guide/settings

Python's `runpy` documentation explicitly says it executes in the current process and is not a sandbox. It is used only for a bounded synthetic diagnostic. Source: https://docs.python.org/3.14/library/runpy.html

## Owner diagnostic sequence

**Do not run `main.py` again yet. Preserve the current attempt.**

1. Open the same active Pyodios project and its Files tab.
2. Look for `summary.json`. If it exists, open it and compare: `grand_total` = `"10.75"`; `line_items` = `2`; `totals_by_item.notebook` = `"7.00"`; `totals_by_item.pen` = `"3.75"`. Do not overwrite or rerun.
3. Open **Settings → Diagnostics → Error Logs → View Error Log**. Find the entry timestamped around the green-play attempt.
4. Inspect it before sharing. Copy only the relevant entry/traceback; redact personal paths and unrelated source. Do not clear the log.
5. If the log is unhelpful, open the Pyodios Console and run this read-only probe for Pyodide's saved `sys.last_value` from the previous exception. It does not rerun `main.py`:

```python
import sys
import traceback

exc = getattr(sys, "last_value", None)
if exc is None:
    print("No previous Python exception is available as sys.last_value.")
else:
    print("EXCEPTION TYPE:", type(exc).__name__)
    print("EXCEPTION VALUE:", repr(exc))
    print("TRACEBACK:")
    print("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
```

6. Only if no useful Error Log or saved exception is available, and the artifact does not exist, import the separate downloadable wrapper attachment `pocketcode_pyodios_runpy_diagnostic.py` and run it once. It refuses to execute if an input is absent or an earlier `summary.json` exists.

| Observation | Interpretation |
|---|---|
| Existing JSON matches the expected values | Artifact correctness may be observed; native child exit status remains unavailable. |
| Existing JSON differs or cannot be parsed | Preserve it; correctness is not established. |
| Log shows `SystemExit` with request 0 | Supports the bridge hypothesis; still verify the file values. |
| Log shows `SystemExit` with request 2 and missing-file message | Likely fixture-handled file visibility issue; reopen project and confirm files before any later attempt. |
| Log shows another exception | Follow that exact traceback; `SystemExit` hypothesis is insufficient. |
| No JSON and no useful log | Cause remains UNKNOWN; wrapper is a controlled next diagnostic. |

## Separate diagnostic wrapper and local verification

Companion attachment: `pocketcode_pyodios_runpy_diagnostic.py` (downloadable from the current conversation; not a checked-in PocketCode product file). It prints Python version and working directory, checks for the two inputs and prior output, refuses to run if an input is absent or `summary.json` already exists, runs the exact frozen script with `runpy.run_path()`, catches `SystemExit` as a script-requested exit value, prints ordinary Python tracebacks, then parses and compares any newly-created JSON against the success oracle. It does not modify `main.py`, create a subprocess, provide a sandbox or prove an OS exit status.

- Canonical `main.py`: 1,939 bytes; SHA-256 `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7`.
- Wrapper SHA-256: `f2abc0104d74e9910f1712dd582cfbccdebefe0eefc347aeb66c4f7786d73009`.
- Environment: CPython 3.13.5 / Linux, not Pyodios.
- Success fixture: caught script exit request 0; exact expected JSON matched.
- Malformed fixture: caught script exit request 2; missing `unit_price` diagnostic present; no JSON created.
- Result: **2/2 local wrapper checks passed**. Pyodios/Pyodide 314.0.5 device execution remains NOT RUN.

## CASE-04/report-projection reconciliation

`scripts/report_contract.py` currently returns FAIL for a valid nonzero generic `exit_code` or `program_failed`; PASS requires `succeeded` plus integer zero; otherwise INCOMPLETE. Canonical CASE-04 requires a trusted timeout to remain INCOMPLETE / timed_out.

The 2026-11-05 `VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md` explicitly says the generic exit code may be child exit, wrapper exit, forced-termination, stale or contradictory evidence, and says not to patch `classify_verdict()` until the coordinator input contract and exit provenance are resolved. The coordinator seam is not present in the reviewed branch.

**Decision:** no formatter or test patch in this pass. Do not merely move the timeout condition above nonzero exit. Next engineering step is a typed projection at the coordinator boundary that distinguishes child exit, wrapper exit, termination cause/confirmation, lifecycle evidence and contradictions. The formatter should consume an already-reconciled projection. Keep canonical LOOP/CASE/D IDs and wording unchanged.

## Red-team corrections to prior work

1. Earlier wording called `PythonError` a generic app error. Exact-version Pyodide docs define it as the JS-side exception type for a Python exception crossing the language boundary.
2. Earlier steps ran a CLI-style fixture with uncaught `SystemExit` through an embedded interpreter without an adapter. The source fixture stays frozen; a separate wrapper now catches and reports the exit request.
3. Earlier pull-to-refresh advice was unsupported by the vendor docs. Reopen the project after external file additions.
4. The start page suggested a direct CASE-04 precedence reorder. That conflicts with the more precise exit-provenance matrix; typed evidence resolution comes first.
5. Earlier status said the device test awaited any owner observation. An Editor attempt has occurred, but the outcome is UNKNOWN, not NOT RUN and not PASS/FAIL.

## Next actions

1. Resolve the present device attempt from its existing `summary.json` and timestamped Error Log before rerun.
2. Reconcile the start page and define/test the typed child/wrapper/termination projection without freezing speculative schema.
3. Test wrapper behavior with the exact Pyodide 314.0.5 runtime only if a safe $0 harness is available; then verify on device.
4. After the success path is understood, run malformed input in a fresh project, then export/read-back and normal relaunch checks.
5. Compare one alternative such as a-Shell or Carnets only after the fixed-task evidence is complete.

## Non-claims and boundary

This note and wrapper do not select Pyodios/Pyodide as PocketCode's runtime, claim hostile-code isolation, change the $0 budget, choose a provider, change schemas or canonical suites, edit the frozen fixture, install anything, start a workload, modify PR #2/#3, run Actions, merge or deploy. Pyodios documentation lists licences of bundled dependencies but not an app/bridge source licence; no bridge code was adopted.

## Sources

- https://pyodide.org/en/314.0.5/usage/type-conversions.html
- https://docs.python.org/3.14/library/sys.html
- https://docs.python.org/3.14/library/runpy.html
- https://pyodios.caffeinatedmath.com/guide/editor
- https://pyodios.caffeinatedmath.com/guide/projects
- https://pyodios.caffeinatedmath.com/guide/settings
- https://pyodios.caffeinatedmath.com/faq