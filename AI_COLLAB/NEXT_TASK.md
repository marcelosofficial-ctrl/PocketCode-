# NEXT TASK: PocketCode

## Goal
Continue bounded model-only evidence closure. Owner authorization covers source/test work for journal conflict attribution and receipt watermarks. P39 implementation/adapter conformance remains CLOSED.

## Verified snapshot (2026-11-14)
- Latest substantive model commit: `45cb200b3e7959625f1dee8cab1c2577b0b6bb59`; parent `b6db10e75d0207457ac60c9859651192c91f855a`. It updates the grant model and focused tests. A documentation checkpoint follows this source commit. Tests NOT RUN: ephemeral execution could not resolve github.com. Existing Python workflow is pinned to historical SHA `319cffef121e327331aeaff59522ae279b112ecc`; it cannot verify current branch source.
- Previous research note remains `AI_COLLAB/FULL_POWER_GAP_RESEARCH_20261114.md`.

## Completed this unit
- Journal conflict quarantine now preserves attempted producer issuer/subject/key ID, effect/attempt/fence and occurrence/observation timestamps.
- EventJournal exposes distinct observation and accepted-event high-water values. The legacy `last_sequence` remains an observation-high-water alias.
- ResultReceipt includes both journal watermarks and ordered conflict sequence references in its immutable digest. A late conflict is represented by a successor receipt, not mutation of the prior receipt.
- Added 2 journal tests and 3 receipt tests covering attribution, high-water behavior, receipt binding, successor immutability and invalid references.
- No adapter, provider, runtime, storage, canonical LOOP/CASE/D/OD ID, PR or infrastructure changes.

## Next
1. Obtain exact-tree test execution without changing the pinned historical workflow. The current environment cannot resolve github.com; any Actions result from the existing workflow is non-verifying for current source.
2. Red-team journal/receipt composition: conflict sequence references remain caller-supplied and range-validated, not independently resolved against journal contents. Decide whether a typed snapshot model is justified before integration.
3. Extend grant model tests to transition replay/order and canonical envelope edge cases. Keep relay fencing and atomic consumer inbox implementation gated.
4. Preserve report-v2 gate, format-1 compatibility, CASE-04 INCOMPLETE / timed_out, and the successful Pyodios `summary.json`.

## Constraints
- $0; no paid service, provider/runtime/database/transport/storage/host selection, deployment, DNS, PR #2/#3/#4 changes or external AI request.
- Preserve LOOP-01..14, CASE-01..16, D-IDs and OD-01..OD-13. PocketCode and RevDev remain separate.
- Explicit paste/import only; no clipboard polling, overlays or automatic capture. Untrusted code requires disposable externally constrained execution; stock Pyodide/WASM remains trusted-light-task only.
- No adapter/device/browser acceptance or artifact rerun. P39 implementation/adapter gate CLOSED.
- Resume sequence: BOOT, STATE, NEXT_TASK, CHECKPOINT, INBOX_chatgpt, live HEAD/latest five; INDEX only after startup. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
