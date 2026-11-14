# NEXT TASK: PocketCode

## Goal
Continue bounded model-only evidence closure. Owner authorization covers source/test work for journal conflict attribution and receipt watermarks. P39 implementation/adapter conformance remains CLOSED.

## Verified snapshot (2026-11-14)
- Current HEAD: `97b302f5f753273bbc58369d743e41e87f676b2f`; parent `339bccf62dce3becab848e8f31bf05ca3609c802`.
- Latest commit changes two model modules, their two focused test modules and CHECKPOINT. Exact-HEAD statuses: zero; workflow runs: zero; tests NOT RUN.
- Previous research note remains `AI_COLLAB/FULL_POWER_GAP_RESEARCH_20261114.md`.

## Completed this unit
- Journal conflict quarantine now preserves attempted producer issuer/subject/key ID, effect/attempt/fence and occurrence/observation timestamps.
- EventJournal exposes distinct observation and accepted-event high-water values. The legacy `last_sequence` remains an observation-high-water alias.
- ResultReceipt includes both journal watermarks and ordered conflict sequence references in its immutable digest. A late conflict is represented by a successor receipt, not mutation of the prior receipt.
- Added 2 journal tests and 3 receipt tests covering attribution, high-water behavior, receipt binding, successor immutability and invalid references.
- No adapter, provider, runtime, storage, canonical LOOP/CASE/D/OD ID, PR or infrastructure changes.

## Next
1. Obtain exact test output and inspect CI for HEAD `97b302f`; until then tests remain NOT RUN.
2. Red-team journal/receipt composition. Conflict sequence references are caller-supplied and range-validated, not independently resolved against a journal. Decide whether the next model slice should introduce a narrow typed journal snapshot input before integrating grant semantics.
3. Then model grant semantic no-op/event parity and canonical first-delivery digest verification. Keep relay fencing and atomic consumer inbox implementation gated.
4. Preserve report-v2 gate, format-1 compatibility, CASE-04 INCOMPLETE / timed_out, and the successful Pyodios `summary.json`.

## Constraints
- $0; no paid service, provider/runtime/database/transport/storage/host selection, deployment, DNS, PR #2/#3/#4 changes or external AI request.
- Preserve LOOP-01..14, CASE-01..16, D-IDs and OD-01..OD-13. PocketCode and RevDev remain separate.
- Explicit paste/import only; no clipboard polling, overlays or automatic capture. Untrusted code requires disposable externally constrained execution; stock Pyodide/WASM remains trusted-light-task only.
- No adapter/device/browser acceptance or artifact rerun. P39 implementation/adapter gate CLOSED.
- Resume sequence: BOOT, STATE, NEXT_TASK, CHECKPOINT, INBOX_chatgpt, live HEAD/latest five; INDEX only after startup. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
