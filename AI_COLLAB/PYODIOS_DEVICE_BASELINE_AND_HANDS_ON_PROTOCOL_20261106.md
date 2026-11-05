# Pyodios device baseline and hands-on protocol — 2026-11-06

**Status:** Public documentation reconciled; owner reports app installed; device execution NOT YET OBSERVED. This is a test plan and source audit, not a product acceptance result.
**Target:** Pyodios on the owner's iPhone, using the existing frozen CSV-to-JSON fixture without edits.
**Budget/privacy:** $0; synthetic inputs only; no account, provider, remote kernel, package install, private file, or network workload required.

## 1. Current public-source baseline

The official Pyodios site currently describes v1.1.0, CPython 3.14.2 on Pyodide 314.0.5, iOS/iPadOS 26+, and local on-device execution. These are vendor claims until the installed device's About / Python Session screens are inspected.

Official sources:
- Product/runtime: https://pyodios.caffeinatedmath.com/
- FAQ: https://pyodios.caffeinatedmath.com/faq
- Projects and working directory: https://pyodios.caffeinatedmath.com/guide/projects
- Files/import/export: https://pyodios.caffeinatedmath.com/guide/files
- Editor/run: https://pyodios.caffeinatedmath.com/guide/editor
- Settings/session: https://pyodios.caffeinatedmath.com/guide/settings

### Relevant capabilities and constraints

| Area | Official documentation says | Experimental consequence |
|---|---|---|
| Execution | Local Pyodide/WASM, CPython 3.14.2 / Pyodide 314.0.5 in v1.1.0 | Verify installed version. This is an on-device runtime, not evidence of a separate hostile-code sandbox. |
| Session lifecycle | Fresh Python session on each app launch; variables/imports/console transcript do not persist | Do not equate project/file persistence with live execution resumption. |
| Files | Documents-container files persist across launches; uninstall deletes them | Check exact output file separately from variables/session. |
| Projects | Active project folder becomes the Python working directory; switching projects saves/copies working files back | Create a dedicated empty project and verify `Path.cwd()` plus relative-file access. |
| Project synchronization | Project folder and Python session folder are copies synchronized at specific moments, not continuously; external additions may require reopening the project; deletions do not propagate automatically | Avoid editing/deleting inputs outside the app during an active run. Reopen project after external import. |
| File-size transfer | Files larger than 16 MB are not copied into the Python session; outputs over 16 MB are not copied back | Not relevant to the tiny fixture, but a real adapter must disclose this limit. |
| Memory | Approximately 300 MB available to Python, per FAQ | Treat as vendor-documented soft/approximate capacity, not a product-enforced quota measured by us. |
| Stop/timeout | FAQ says Python code currently cannot be interrupted once executing; a run gives up after 120 seconds and reports timeout, but code continues in background until Python session restart or app close/reopen | Critical limitation. A UI timeout is not confirmed termination. Do not use a deliberate infinite loop or a long-running stress test in the first session. |
| Exit status | Public docs reviewed do not establish a child-process exit-status API | Record exit status UNAVAILABLE unless directly exposed and verified. Script `SystemExit(2)` displayed as text is not automatically a trusted OS child exit code. |
| Import/export | Files tab supports document-picker import and share-sheet export | Verify actual file bytes and export path, not only editor text or preview. |
| Packages/network | Standard-library task needs no packages; Python itself is local. Network is needed for packages not already installed and remote kernels | Keep the first run offline-capable and standard-library-only; do not install pandas or other dependencies. |
| Editor | Whole script runs from green play control when no text is selected; selected text runs separately | Use the whole-file run control; avoid partial-selection execution. |

Sources: official Pyodios product, FAQ, Projects, Files and Editor guides above. Source claims are not device observations.

## 2. Experimental boundary and frozen task

Use the exact `main.py`, success `items.csv`, and malformed `items.csv` contents already frozen in Section 2A/8 of `PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md`.

- Do not regenerate or edit the program.
- Do not install packages.
- Do not connect a remote Jupyter kernel.
- Do not enable cloud sync solely for this experiment.
- Use a dedicated fresh Pyodios project for each scenario so stale `summary.json` cannot satisfy a later attempt.
- Preserve the canonical source and expected results; this document adds no acceptance IDs and changes no schema.

### Success oracle

The actual generated `summary.json` must parse to:
- `grand_total`: string `10.75`
- `line_items`: integer `2`
- `totals_by_item.notebook`: string `7.00`
- `totals_by_item.pen`: string `3.75`

The script's expected stdout is `Wrote summary.json`. Record what Pyodios actually exposes for stderr and exit status; do not infer a process exit code from printed output.

### Malformed-input oracle

Use the frozen CSV with the `unit_price` header removed, in a separate fresh project. Expected script diagnostic: `ERROR: missing required CSV column(s): unit_price`. The script should return 2 when run as a normal Python process. Pyodios may not expose a child-process exit code; record UNAVAILABLE if so. No `summary.json` may be produced in that fresh project.

## 3. Minimal hands-on sequence

### A. Capture installed build before running

In Pyodios, inspect About and Settings > Python Session. Record:
- app version/build;
- Python version;
- Pyodide version;
- iOS version and iPhone model (as displayed in Settings);
- whether a project is already active;
- whether the app reports any runtime or memory warning.

Do not restart the Python session merely to inspect it.

### B. Success path

1. In More > Projects, create a new project named `PC-FIXED-SUCCESS-01`.
2. Import the exact `main.py` and success `items-success.csv` into that project, then rename the imported CSV to `items.csv` using Files > … > Import File (or the iOS Files share-to-Pyodios flow).
3. If files were imported through Files/iOS while the project was already open, follow the app's documented project-refresh behavior and reopen the project before execution if needed.
4. Confirm both filenames appear in the active project. Open `items.csv) and verify its header and two rows.
5. Open `main.py` in Editor. Ensure no text is selected. Run the entire script once.
6. Record the visible output and any status/diagnostic the app exposes.
7. Open Files and confirm a newly modified `summary.json` exists in this project. Open it and inspect values.
8. Share/export `summary.json` through the iOS share sheet to Files. Do not overwrite another fixture. Record whether export completed and where it was saved.
9. Do not run the script again just to obtain a better-looking result. Preserve this first attempt.

### C. Malformed-input path

1. Create a separate new project named `PC-FIXED-FAILURE-01`.
2. Import the exact same `main.py) and malformed `items.csv` fixture.
3. Confirm no `summary.json` exists before running.
4. Run the whole script exactly once.
5. Record visible error text, stderr separation if available, status/exit exposure, and whether `summary.json` exists.
6. Do not copy the success artifact into this project.

### D. File/session persistence observation

Only after both task scenarios are captured:
1. Confirm both project folders and their files remain visible in Files.
2. Close and relaunch Pyodios normally once.
3. Inspect the projects and exact `summary.json` again before running any code.
4. Record whether the project/artifact persists and whether Python variables/session were reset. Do not rerun.
5. This is a natural relaunch observation, not a crash-injection or power-loss durability test.

Do not deliberately force-quit during an active run in this first pass. Official docs state running Python cannot be interrupted normally and that a timeout does not stop the underlying code. First establish the ordinary success/failure behavior and file persistence without risking a stuck session.

## 4. Evidence classification

For each fact, label it:
- **DIRECTLY OBSERVED:** seen on the actual device or verified from the exported artifact bytes.
- **DOCUMENTED CLAIM:** stated by Pyodios official documentation but not tested.
- **UNKNOWN / UNAVAILABLE:** app does not expose it or evidence is insufficient.
- **NOT RUN:** no attempt was made.

Never call the task PASS solely because the UI prints the expected message. Correctness requires the actual file. Never call exit status known unless the app exposes a trustworthy process result. Never claim cancellation/termination from a timeout banner.

## 5. Capture record

```text
Device model:
iOS version:
Pyodios version/build:
Python version:
Pyodide version:
Active project:
Network state (Wi-Fi/cellular/offline):
Cloud sync enabled?:
Scenario: SUCCESS | MALFORMED
Workspace fresh before run?:
Exact frozen source/input supplied unchanged?:
Import route and number of user actions:
Whole-file run used?:
Observed runtime/startup behavior:
Visible stdout:
Visible stderr:
App run status:
Child/process exit status: VALUE | UNAVAILABLE | UNKNOWN
summary.json before run:
summary.json after run:
Parsed output values:
Output file size:
Export action and destination:
Export destination read-back:
Elapsed setup/run time (only if timed):
Errors/warnings:
Scenario result: PASS | FAIL | INCONCLUSIVE | BLOCKED | NOT RUN
Evidence attachments / screenshots:
```

## 6. What this test can and cannot establish

It can establish, for this exact iPhone/app build and small standard-library task:
- whether Pyodios accepts the unchanged multi-file source/input;
- whether the selected project supplies the expected working directory;
- whether the script creates the correct real output file;
- what stdout/error/status evidence the UI exposes;
- whether the artifact can be exported and read back;
- whether project files survive a normal app relaunch.

It cannot establish:
- hostile-code isolation or a security sandbox;
- hard CPU, memory, disk or network enforcement;
- reliable interruption of arbitrary running code;
- child process exit status if the app does not expose one;
- power-loss durability, filesystem transaction guarantees or cross-device sync correctness;
- PocketCode acceptance conformance or product differentiation from one task alone.

## 7. Current decision

Pyodios is now the first hands-on iPhone local comparator because the owner reports it is installed. This does not make it the selected PocketCode runtime or a product dependency. Its documented no-interrupt behavior and session reset are especially important limitations for future recovery design.

**Status:** DOCUMENTATION REVIEW COMPLETE / DEVICE TEST AWAITING OWNER OBSERVATIONS / PRODUCT ACCEPTANCE NOT RUN. No product source, test, canonical fixture, LOOP/CASE ID, schema, provider, runner selection, PR, merge or deployment changed.


## 8. Owner-ready fixture archive

A phone-importable ZIP was prepared from the canonical fixture without changing the Python source. Archive: `pocketcode_pyodios_fixed_task.zip`. Contents: `README.txt`, `main.py`, `items-success.csv`, and `items-missing-unit-price.csv`. Archive SHA-256: `706c6a87d07c496d5a461c9395fb0b967b961fa9c430c719d9799998df5b4099`. The embedded `main.py) is 1,939 bytes and its SHA-256 exactly matches the frozen worksheet sanity-check value `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7`. The archive is a convenience copy only; it does not replace the canonical worksheet fixture.
