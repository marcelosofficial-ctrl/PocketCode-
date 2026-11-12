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

## Branch reconciliation completed

This startup/work unit re-read the five required files in order: BOOT.md, STATE.md, NEXT_TASK.md, CHECKPOINT.md and INBOX_chatgpt.md. It then used the branch-ref commits endpoint to verify the latest five commits. Commit-search results were stale and were not treated as branch-tip evidence.

Pre-update branch HEAD: `3565d63f34c9476e58f96ded42af6fc4bfc1b615`. The latest five commits before this reconciliation were:
- `3565d63f34c9476e58f96ded42af6fc4bfc1b615` — checkpoint chronology
- `64ad86ce65b1b1ddbc41096700bc082a7f97fbbf` — NEXT_TASK chronology
- `e2581f224971459c2cb50bea3a01a51a20c9b165` — STATE chronology
- `b7021362cd9ef6564a7ff8d6a769ee39e392ab98` — checkpoint reconciliation
- `fc959d417263a0397f89e0157d103a516c0e47db` — STATE reconciliation

All five were fetched; each changes only AI_COLLAB documentation. This unit corrected stale branch-head chronology in STATE.md and NEXT_TASK.md, then refreshed this checkpoint. No application source, tests, workflows, device evidence, host/provider, deployment or PR changes.

CI: current pre-update HEAD `3565d63f34c9476e58f96ded42af6fc4bfc1b615` has no status checks. Latest relevant workflow remains run #59 / 43126974602 SUCCESS, workflow head `d93cd11e6873090cdb280fd18e45d9eeee9a973f`, checking out exact historical model target `319cffef121e327331aeaff59522ae279b112ecc`; full scripts suite 266/266. It is model-only historical evidence, not current-HEAD, adapter or CASE acceptance. Tests in this reconciliation unit: NOT RUN.

Next startup: read BOOT.md, STATE.md, NEXT_TASK.md, CHECKPOINT.md, INBOX_chatgpt.md; then list latest five commits. Use INDEX.md for further reads. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER; never read any file over 1,500 words whole.
