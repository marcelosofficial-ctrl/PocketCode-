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
- Latest relevant CI remains run #59. Documentation-only changes do not match Python workflow path filters.
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

## Branch reconciliation

Before this unit, latest five commits were:
- 03e65ef35d8b22cb4337ac7097b2a31247c3721e — STATE.md post-Gemini gate/Claude wait
- 319d3da7291465a2f209bf7cada2a9bb66ae6d7f — README banner/name note
- 3e09ada6b4eaacae4b0e8d9193bdb746a796d859 — INBOX housekeeping
- c598371c6447a605398d2b6e48aca903842b58dd — NEXT_TASK gate clarification
- a8ff22690afe97858a17f10efdc26159d90f63db — checkpoint

New documentation unit began at `03e65ef35d8b22cb4337ac7097b2a31247c3721e`; runbook commit `b0e590ded211d1406e0fcd205babe2ad876e9779`. INDEX, STATE, NEXT_TASK and this checkpoint are being reconciled on the active branch. Tests this unit: NOT RUN. No CI result is claimed.

Next startup: read BOOT.md, STATE.md, NEXT_TASK.md, CHECKPOINT.md, INBOX_chatgpt.md; then list latest five commits. Use INDEX for further reads. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER; never read any file over 1,500 words whole.
