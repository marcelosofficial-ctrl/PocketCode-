# PocketCode continuation handoff — 2026-11-06

This handoff continues the 2026-11-05 handoff and canonical project docs. It changes no product decision or acceptance contract.

## Repository snapshot
- Repository: marcelosofficial-ctrl/PocketCode-
- Research branch: pocketcode-ai-workflow-director-research-2026-10-28
- Last live comparison: 709 ahead / 0 behind main; merge base 555840d8d83342513d9cd353d4d1522d46a5c82d. Ahead count is accumulated branch history, not implementation progress.
- PR #2 and #3 remain open draft PRs and were not modified.
- Latest commits in this continuation: 7c04a182febd82f7540b96af6310de8c44e5fd00 (Pyodios protocol), 920392c266ca55d77ff357a2b81eb4aafc25b35a (status), ec1fcc685c982575863a2508cd61c1f9af3373de (fixture integrity), e6570c79b21b181e4961020af54357514882b7c9 (status).
- Re-fetch refs before consequential work.

## Owner/device update
The owner reports Pyodios is installed on the iPhone. No device execution has yet been reported. Owner-transcribed About / Settings screens confirm Pyodios 1.1.0 / Build 7, Pyodide 314.0.5, Python 3.14.2, WebAssembly runtime. Device model and iOS version remain UNKNOWN. These are owner-reported observations, not independently inspected by ChatGPT.

A fixture archive was created in the conversation:
- pocketcode_pyodios_fixed_task.zip, 2,184 bytes
- SHA-256: 706c6a87d07c496d5a461c9395fb0b967b961fa9c430c719d9799998df5b4099
- Contents: README.txt, canonical main.py, items-success.csv, items-missing-unit-price.csv.
- Embedded main.py is 1,939 bytes and matches the frozen worksheet SHA-256 70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7.
- The archive is a convenience copy. Canonical source remains Section 2A/8 of AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md.

## Fresh Pyodios findings
Official docs currently describe v1.1.0, CPython 3.14.2 / Pyodide 314.0.5, iOS 26+, and local on-device execution. These are DOCUMENTED CLAIMS until checked against the installed build.

Important documented constraints:
- Every app launch starts a fresh Python session; variables/imports do not persist.
- Project files persist in app Documents, but project and Python working folders are copied/synchronized at specific moments, not continuously.
- Files imported externally while a project is open may require reopening the project to become visible to Python.
- Files over 16 MB are not copied into the Python session; outputs over 16 MB are not copied back.
- FAQ states approximately 300 MB available to Python.
- FAQ says running Python cannot currently be interrupted once executing. A 120-second run timeout reports timeout but code continues in the background; restart Python session or close/reopen the app to stop it, losing variables/imports.
- Public docs reviewed do not establish a trustworthy child-process exit-status API. Do not infer exit status from UI text or script output.

Official sources:
- https://pyodios.caffeinatedmath.com/
- https://pyodios.caffeinatedmath.com/faq
- https://pyodios.caffeinatedmath.com/guide/projects
- https://pyodios.caffeinatedmath.com/guide/files
- https://pyodios.caffeinatedmath.com/guide/editor

## Immediate device plan
Read AI_COLLAB/PYODIOS_DEVICE_BASELINE_AND_HANDS_ON_PROTOCOL_20261106.md.

1. Capture app/build, Python and Pyodide versions from About / Settings > Python Session; capture iOS version and device model.
2. Extract the ZIP in iOS Files.
3. Create fresh project PC-FIXED-SUCCESS-01; import main.py and items-success.csv, rename the CSV to items.csv, run the whole script once, inspect the actual summary.json, and export it.
4. Create separate fresh project PC-FIXED-FAILURE-01; import main.py and items-missing-unit-price.csv, rename the CSV to items.csv, run once, confirm the diagnostic and absence of summary.json.
5. Only after both results are captured, close/relaunch normally and inspect project/artifact persistence before any rerun.

Do not intentionally force-quit during active execution or run an infinite loop. First pass is low-risk ordinary success/failure and file-persistence observation.

Evidence rules:
- Actual file, not just console text.
- Fresh separate workspace for success and failure.
- Capture what the app exposes for stdout/stderr/status; child exit status may be UNAVAILABLE.
- Do not treat timeout, app close or missing response as confirmed termination.
- Separate DOCUMENTED CLAIM, DIRECTLY OBSERVED, UNKNOWN/UNAVAILABLE and NOT RUN.

## Project guardrails
- PocketCode remains in Discovery/product definition; no runtime/provider selected.
- $0 budget; no paid provider, credits, cloud workload or account creation.
- Phone-first; do not assume PC access.
- Do not build a generic Python IDE. Differentiation remains task packet, evidence/receipt provenance, durable history/recovery, portable AI correction handoff and bounded user-approved repair.
- OpenHands and Cline patterns remain references, not wholesale frameworks or integrations.
- MCP Tasks is a possible async task adapter; ACP a possible agent-session adapter; neither identity replaces PocketCode command/attempt identity.
- Default-deny permissions remain mandatory. Reject Cline's tested wildcard auto-approval default.
- RevDev and PocketCode keep separate repositories, runtimes, adapters, roadmaps, acceptance suites and release gates.
- Canonical PocketCode LOOP-01..14 and CASE-01..16 unchanged. EVAL-06 is the separate compact-checkpoint prompt-bundle experiment, not the mobile runner test.
- PR #2/#3 protected and unmodified.

## Next work after device evidence
1. Score Pyodios success and malformed-input paths using the existing worksheet. Do not rank with critical evidence U/unknown.
2. Capture natural relaunch file persistence separately from live Python session persistence.
3. Compare next with one free local path (a-Shell or Carnets) only if it adds information; do not install every competitor.
4. Run raw-evidence vs portable-report correction only after a real path supplies the same underlying evidence for both conditions.
5. Continue source-level implementation/test work on provider-neutral task/receipt logic only where the existing product/acceptance contract supports it. Keep proposals separate from verified product behavior.

**Current evidence state:** public Pyodios review COMPLETE; fixture archive hash VERIFIED; device attempt AWAITING OWNER; PocketCode product acceptance and recovery suites NOT RUN.


## Owner-reported build confirmation (2026-11-06)
The owner reports the Settings screen showed 13 cached packages / 0 KB cache, 85,557 objects / 0 referrers, and GC stats 1,650 collected / 0 uncollectable. These counters are transient diagnostics, not performance/capacity measurements. Do not clear variables, run GC, or restart merely to reset them. The installed app/runtime baseline is now known; the actual fixed-task execution, artifact export, and relaunch-persistence checks remain NOT RUN. See the updated device protocol for the next low-risk steps.
