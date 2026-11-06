# Pyodios PythonError bridge triage — 2026-11-06

**Current status:** The owner-reported Editor attempt produced a `summary.json` artifact that the owner inspected and confirmed matches the canonical oracle exactly. The Editor displayed `[Bridge/executePython] PythonError`. The owner then checked More → Settings → Error Log → View Error Log; the only detail was `Editor: PythonError`, with no traceback. Classification: **ARTIFACT-LEVEL FUNCTIONAL SUCCESS / BRIDGE ERROR UNRESOLVED / FULL RUN INCONCLUSIVE**. The underlying Python exception and trusted native process exit status remain UNKNOWN. The saved-exception Console probe and separate wrapper have not run on the phone.
**Authority:** No change to canonical fixture, LOOP/CASE/D acceptance, runtime/provider selection, security boundary or $0 budget.

## Observed attempt

The owner reports that `main.py` and renamed `items.csv` are in the same Pyodios project, the green whole-file Editor play control was tapped, and the complete visible output was exactly `[Bridge/executePython] PythonError`. No traceback or other output was visible.

- **DIRECTLY OBSERVED (owner-reported):** files added to project; green Editor run invoked; exact visible result above.
- **UNKNOWN at the time of the initial report:** whether `summary.json` existed; whether `items.csv` was visible to the active Python working folder; the underlying Python exception; separate stderr; the script-requested exit value. A later owner inspection, recorded in the project work log, confirmed the existing `summary.json` is present and matches the oracle exactly. The bridge cause and native process exit status remain UNKNOWN.
- **NOT RUN:** malformed-input case, artifact export/read-back, normal relaunch persistence, interruption/recovery and PocketCode acceptance.
- No PASS or FAIL is assigned from the bridge label alone.

The canonical fixture is unchanged. Its final entrypoint is `raise SystemExit(main())`; the main function requests exit value 0 on success and 2 for its handled file/validation errors.

## Ranked gaps

| Rank | Gap | Reason and action |
|---|---|---|
| 1 | Pyodios bridge error has no visible root cause | The artifact and Error Log are already checked. Run the read-only `sys.last_exc` / `sys.last_value` Console probe in the existing session; do not rerun the task. |
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

Pyodios says the open project is the Python working directory, but the project folder and Python session folder are copied at defined moments, not continuously. Its Files guide says pull down on the Files list to refresh that browser after external changes. Separately, its Projects guide says files added externally while a project is open are not visible to Python until the project is reopened. These are two layers: pull-to-refresh refreshes the Files browser list; reopening the project synchronizes the project folder into the Python session. Outputs created by Python should appear in the project Files tab after the cell finishes. Source: https://pyodios.caffeinatedmath.com/guide/projects

On iPhone, open **More → Settings**, scroll to **Error Log**, then tap **View Error Log**. The log contains timestamps and error details. The app warns that Python code can appear in error messages, so inspect and redact before sharing. Source: https://pyodios.caffeinatedmath.com/guide/settings

Pyodios v1.1.0 says Python code cannot be interrupted once it starts. A 120-second UI timeout returns control while code continues in the background. Do not use an infinite loop or timeout as a termination test. Source: https://pyodios.caffeinatedmath.com/faq

Pyodios credits Pyodide, CPython, Comlink and micropip and lists their bundled licences, but this does not establish that Pyodios' own app/bridge source is open source. No app source repository or app-source licence was verified in this pass. Do not copy or claim reuse rights over its bridge. Source: https://pyodios.caffeinatedmath.com/guide/settings

Python's `runpy` documentation explicitly says it executes in the current process and is not a sandbox. It is used only for a bounded synthetic diagnostic. Source: https://docs.python.org/3.14/library/runpy.html

## Owner diagnostic sequence

**Do not run `main.py` again. Preserve the current attempt and exact-match artifact. The Error Log has already been checked and yielded only `Editor: PythonError`, without traceback.**

1. Open the same active Pyodios project and its Files tab.
2. The owner has already inspected the existing `summary.json`; it matches the oracle: `grand_total` = `"10.75"`; `line_items` = `2`; `totals_by_item.notebook` = `"7.00"`; `totals_by_item.pen` = `"3.75"`. Preserve this file. Do not overwrite or rerun the success project.
3. Already completed by the owner: More → Settings → Error Log → View Error Log. The only available detail was `Editor: PythonError`; no traceback or underlying exception was exposed. Do not clear the log.
4. Next, tap **Console** in Pyodios' bottom tab bar to open the interactive Python REPL in the existing session. Pyodios documents Console as a first-class section; on iPhone, sections are accessed from the tab bar. Run this read-only probe for Pyodide's saved exception (`sys.last_exc` preferred on Python 3.14, falling back to `sys.last_value`). It does not rerun `main.py`:

```python
import sys
import traceback

exc = getattr(sys, "last_exc", None)
if exc is None:
    exc = getattr(sys, "last_value", None)

if exc is None:
    print("No previous Python exception is available.")
else:
    print("EXCEPTION TYPE:", type(exc).__name__)
    print("EXCEPTION VALUE:", repr(exc))
    print("TRACEBACK:")
    print("".join(traceback.format_exception(type(exc), exc, exc.__traceback__)))
```

6. If the probe returns no saved exception, do not infer that no exception occurred. Do not run the wrapper in the success project. If a further controlled diagnosis is justified, use a separate disposable project and preserve the current success project untouched.

| Observation | Interpretation |
|---|---|
| Existing JSON matches the expected values | Artifact correctness may be observed; native child exit status remains unavailable. |
| Existing JSON differs or cannot be parsed | Preserve it; correctness is not established. |
| Log shows `SystemExit` with request 0 | Supports the bridge hypothesis; still verify the file values. |
| Log shows `SystemExit` with request 2 and missing-file message | Likely fixture-handled file visibility issue; reopen project and confirm files before any later attempt. |
| Log shows another exception | Follow that exact traceback; `SystemExit` hypothesis is insufficient. |
| No saved exception from the Console probe | Cause remains UNKNOWN; absence is unavailable evidence, not proof that no exception occurred. Consider any further wrapper test only in a separate disposable project. |

## Separate diagnostic wrapper and local verification

Companion attachment: `pocketcode_pyodios_runpy_diagnostic.py` (downloadable from the current conversation; not a checked-in PocketCode product file). It prints Python version and working directory, checks for the two inputs and prior output, refuses to run if an input is absent or `summary.json` already exists, runs the exact frozen script with `runpy.run_path()`, catches `SystemExit` as a script-requested exit value, prints ordinary Python tracebacks, then parses and compares any newly-created JSON against the success oracle. It does not modify `main.py`, create a subprocess, provide a sandbox or prove an OS exit status.

- Canonical `main.py`: 1,939 bytes; SHA-256 `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7`.
- Wrapper SHA-256: `f2abc0104d74e9910f1712dd582cfbccdebefe0eefc347aeb66c4f7786d73009`.
- Environment: CPython 3.13.5 / Linux, not Pyodios.
- Success fixture: caught script exit request 0; exact expected JSON matched.
- Malformed fixture: caught script exit request 2; missing `unit_price` diagnostic present on stderr; no JSON created.
- Existing-artifact guard: refused to run and preserved a sentinel `summary.json` byte-for-byte.
- Missing-input guard: refused to run when `items.csv` was absent.
- Result: **4/4 local wrapper checks passed** under CPython 3.13.5 / Linux. A separate `sys.last_exc`-first / `sys.last_value` fallback probe smoke test passed under that same interpreter. Neither wrapper nor probe has been run on Pyodios / Pyodide 314.0.5.



**Verification correction:** the first expanded harness assertion for the malformed case initially looked for the missing-column message in stdout only. The fixture correctly writes that diagnostic to stderr. The assertion was corrected to inspect stdout and stderr, then rerun; the malformed case passed. This was a test-harness assertion bug, not a fixture or wrapper failure.

## CASE-04/report-projection reconciliation

`scripts/report_contract.py` currently returns FAIL for a valid nonzero generic `exit_code` or `program_failed`; PASS requires `succeeded` plus integer zero; otherwise INCOMPLETE. Canonical CASE-04 requires a trusted timeout to remain INCOMPLETE / timed_out.

The 2026-11-05 `VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md` explicitly says the generic exit code may be child exit, wrapper exit, forced-termination, stale or contradictory evidence, and says not to patch `classify_verdict()` until the coordinator input contract and exit provenance are resolved. The coordinator seam is not present in the reviewed branch.

**Decision:** no formatter or test patch in this pass. Do not merely move the timeout condition above nonzero exit. Next engineering step is a typed projection at the coordinator boundary that distinguishes child exit, wrapper exit, termination cause/confirmation, lifecycle evidence and contradictions. The formatter should consume an already-reconciled projection. Keep canonical LOOP/CASE/D IDs and wording unchanged.

## Red-team corrections to prior work

1. Earlier wording called `PythonError` a generic app error. Exact-version Pyodide docs define it as the JS-side exception type for a Python exception crossing the language boundary.
2. Earlier steps ran a CLI-style fixture with uncaught `SystemExit` through an embedded interpreter without an adapter. The source fixture stays frozen; a separate wrapper now catches and reports the exit request.
3. The earlier red-team statement that pull-to-refresh was unsupported was itself incorrect. The Files guide documents pull-to-refresh for the Files browser list; the Projects guide separately requires reopening the project to synchronize external additions into the Python session.
4. The start page suggested a direct CASE-04 precedence reorder. That conflicts with the more precise exit-provenance matrix; typed evidence resolution comes first.
5. The initial artifact state was UNKNOWN. The owner's later inspection confirmed the exact success oracle in `summary.json`. The Editor bridge error and native exit status remain unresolved, so the full run remains INCONCLUSIVE.

## Next actions

1. Preserve the already matching `summary.json`; inspect the timestamped Error Log and, if needed, run the read-only saved-exception probe. Do not rerun or overwrite the success project.
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

### Upstream Pyodide version cross-check

As of 2026-11-06, the upstream Pyodide release list marks 314.0.7 as Latest (released 14 September 2026), while the installed Pyodios 1.1.0 documentation still specifies bundled Pyodide 314.0.5 / CPython 3.14.2. I fetched the exact `src/core/error_handling.c` files from both upstream tags 314.0.5 and 314.0.7: both contain the same `SystemExit` / `PyConfig.inspect` comment and exception-wrapping logic in the inspected function. This does not establish that other changes between the versions are irrelevant or that Pyodios can independently update its embedded runtime. Do not manually replace the bundled runtime; this is a compatibility/maintenance observation only. Sources: https://github.com/pyodide/pyodide/releases and https://raw.githubusercontent.com/pyodide/pyodide/314.0.5/src/core/error_handling.c and https://raw.githubusercontent.com/pyodide/pyodide/314.0.7/src/core/error_handling.c


## 2026-11-06 — Owner-reported artifact result

The owner inspected the existing project's Files tab after the first Editor attempt. `summary.json` exists and was reported with these exact contents:

```json
{
  "grand_total": "10.75",
  "line_items": 2,
  "totals_by_item": {
    "notebook": "7.00",
    "pen": "3.75"
  }
}
```

This exactly matches the frozen success oracle. Classification is **ARTIFACT-LEVEL FUNCTIONAL SUCCESS (owner-inspected) / EDITOR BRIDGE ERROR UNRESOLVED / FULL RUN INCONCLUSIVE**. This supersedes the prior UNKNOWN artifact outcome. The complete visible Editor output remains `[Bridge/executePython] PythonError`. The artifact establishes that execution reached the correct file write, but not why the bridge then reported an error, nor a trusted process exit status, stderr behavior, export/read-back, relaunch persistence, or PocketCode acceptance.

**Preserve this evidence. Do not rerun or overwrite the success project.** Next inspect Pyodios **More → Settings → Error Log → View Error Log** around the attempt timestamp. Redact source, private paths, tokens and personal data before sharing the relevant exception/traceback. If unhelpful, run the documented read-only Console probe for `sys.last_exc` then `sys.last_value`. Do not restart the Python session, clear variables/logs, or run GC merely to investigate.

`SystemExit` or bridge completion handling remains a hypothesis, not a root-cause finding. Do not modify the canonical fixture based on the artifact alone. After preserving diagnostic evidence, run the malformed-input scenario only in a separate fresh project and record its diagnostic/artifact result; do not infer an exit status Pyodios does not expose.


## Error Log inspection result (2026-11-06)

Owner inspected Pyodios Settings → Error Log for the attempt. The only entry/detail available was **`Editor: PythonError`**, with no underlying Python exception, message or traceback. This does not identify the root cause. The existing exact-match `summary.json` remains the artifact-level success evidence. Next diagnostic is the read-only Console probe for `sys.last_exc` (Python 3.14) / `sys.last_value` (Pyodide bridge fallback), already specified above. Do not rerun or overwrite the canonical success project. If the probe reports no saved exception, record that as unavailable evidence, not proof that no Python exception occurred.
