# CHECKPOINT — 2026-11-12

## Current completed unit

Added `AI_COLLAB/PHONE_DEVICE_VALIDATION_RUNBOOK_20261112.md` as a read-only owner/device evidence protocol.

Coverage:
- Non-destructive Pyodios Console probe. Preserve the already matching `summary.json`; do not rerun `main.py` or any artifact-producing attempt.
- Separate iOS Safari tab, Home Screen web app, WKWebView, Android Chrome tab, Android installed PWA and Android WebView contexts. No cross-context inference.
- Future synthetic-data acceptance for opaque-origin iframe isolation, exact source-bound handshake, narrow wildcard bootstrap, MessagePort validation, CSP/no-network, cancellation evidence, staged artifact read-back, quota/eviction, multi-tab CAS and export/restore.
- Typed lifecycle evidence keeps child exit, wrapper exit, embedded exception, termination acknowledgement, cleanup, artifact collection and client receipt separate.
- Explicit evidence record template and PASS/FAIL/BLOCKED/NOT RUN rules.

No device probe, app code, tests, deployment, host/provider, DNS/settings or storage-engine changes. The runbook does not authorize future device testing or implementation; browser acceptance requires an approved synthetic-data test build. Existing Pyodios success artifact remains untouched.

## Project invariants and gates

- Phone-first, provider-neutral, $0; D-005/D-006 unchanged.
- Keep PocketCode separate from RevDev. Preserve LOOP-01..14, CASE-01..16, all D-IDs and OD-01..OD-13. PR #2/#3/#4 untouched.
- P39 policy decisions OD-01..OD-13 adopted; implementation/adapter gate remains CLOSED.
- CASE-04 remains INCOMPLETE / timed_out.
- No runtime, provider, database, transport, storage engine or host selected.
- Explicit user paste/import only; no clipboard polling/overlays. No sensitive persistence on shared github.io origin.

## Existing evidence

- P40 exact-SHA model run #59 / 43126974602 SUCCESS, full scripts 266/266, exact target `319cffef121e327331aeaff59522ae279b112ecc`; Lane 4 BLOCKED / NOT TESTABLE. Historical model-only evidence, not adapter/CASE acceptance.
- Latest relevant CI remains run #59. Latest documentation HEAD has no status checks; tests in this unit NOT RUN.
- Pages preview run #17 / 39433670146 deployed a static simulation subtree, not app runtime.
- Pyodios iPhone error reported by owner; Console probe NOT RUN; cause/topology UNKNOWN.
- Live Pages response/headers and actual device storage/service-worker state UNKNOWN.

## Indexed design/acceptance documents

- GRANT_EVENT_ENVELOPE_AND_RELAY_CONTRACT_20261112.md
- GRANT_EVENT_MODEL_ACCEPTANCE_PLAN_20261112.md: 29 deterministic model scenarios; implementation/test gate still requires explicit owner approval.
- OPAQUE_ORIGIN_EXECUTION_PROTOCOL_20261112.md
- BROWSER_ARTIFACT_STORAGE_RECOVERY_CONTRACT_20261112.md
- LIFECYCLE_TERMINATION_RECEIPT_ACCEPTANCE_20261112.md
- REPORT_PROJECTION_V2_MIGRATION_AND_ACCEPTANCE_20261112.md: format-2 proposal; preserve legacy format 1; no precedence-only patch.
- PAGES_READ_ONLY_SOURCE_AUDIT_20261112.md
- ZERO_BUDGET_ORIGIN_OPTIONS_20261112.md
- PHONE_DEVICE_VALIDATION_RUNBOOK_20261112.md

## Full work pass: owner visual-check clarification and branch reconciliation

The owner reports opening the previously requested GitHub link and says it looked okay. The previous assistant reply included a GitHub commit URL and separately asked the owner to open the PocketCode Pages preview URL. Therefore the exact target is ambiguous. Record this as an owner-reported informal visual observation only. If the URL was `https://marcelosofficial-ctrl.github.io/PocketCode-/`, it establishes at most that the preview appeared to load/look okay in that one unrecorded context. No exact URL, page content, device/browser/version, screenshot, HTTP headers or service-worker state were captured. Do not ask the owner to repeat the check unless they actually opened the commit URL instead. This does not close the live Pages/device acceptance items.

Startup protocol completed: BOOT.md, STATE.md, NEXT_TASK.md, CHECKPOINT.md and INBOX_chatgpt.md were read in required order. Exact branch-ref API history, not stale commit search, supplied the latest five commits at unit start:
- `6c67df2bd2d7623836bf824c24ebb0a72b4a2cea` — checkpoint
- `56007305d110b94cd5f13ee17a6b766eec3cc027` — next task
- `5b54464ab0423292cec8ef9b0e4bc5481c508c6c` — state
- `3565d63f34c9476e58f96ded42af6fc4bfc1b615` — checkpoint
- `64ad86ce65b1b1ddbc41096700bc082a7f97fbbf` — next task

All five were verified as AI_COLLAB-only. This unit updated STATE.md and NEXT_TASK.md to capture the owner observation with its ambiguity and correct branch chronology, then refreshed this checkpoint. No app source, tests, workflow, deployment, host/provider, DNS/settings, PR or RevDev changes.

CI at unit start: head `6c67df2bd2d7623836bf824c24ebb0a72b4a2cea` had no status checks. Latest relevant run remains #59 / 43126974602 SUCCESS, workflow commit `d93cd11e6873090cdb280fd18e45d9eeee9a973f`, exact historical model target `319cffef121e327331aeaff59522ae279b112ecc`, full scripts suite 266/266. This is not current-head, adapter or CASE acceptance. Tests in this unit: NOT RUN.

Next: owner read-only Pyodios Console probe only. Keep the already matching `summary.json`; do not rerun the artifact-producing attempt. The Pages visual check need not be repeated if the preview URL was the one opened. Keep P39 implementation/adapter gate CLOSED and D-005/D-006 at $0.


## Source-delta verification

GitHub compare from source audit pin `b71315068ec33a0175fed46ef96912e954d87f9f` to the verified branch head at the start of this unit, `04d8181bf159f5a90ae6b7ace017c7f58e31611d`, reports 35 commits ahead, 0 behind, and 11 changed paths. Every changed path is under `AI_COLLAB/`. No application source, scripts/tests, workflow or product assets changed in that interval. This verifies the documented source/test boundary since the source audit pin; it does not imply current-HEAD tests or adapter acceptance.

The user says the previously requested GitHub link looked okay. Since the earlier reply contained both a commit URL and a Pages-preview action, the exact target is ambiguous. This remains a user-reported visual observation, not independently verified live Pages response evidence. If the Pages preview was opened, no repeat check is needed.

Next startup should re-read the five boot files and fetch latest five commits from the active branch. Current CI evidence remains run #59 on the historical pinned model target; current docs head has no status checks. Tests in this unit: NOT RUN.
