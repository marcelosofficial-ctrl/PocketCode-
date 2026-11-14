# NEXT TASK: PocketCode

## Goal
Continue bounded model-only evidence closure. Owner authorization covers source/test work for journal conflict attribution and receipt watermarks. P39 implementation/adapter conformance remains CLOSED.

## Verified snapshot (2026-11-14)
- Grant model commit `45cb200` updated semantic no-op, aggregate/event/outbox parity and canonical digest checks. Follow-up test commit `ed4d821` fixed a stale malformed future-event fixture, made changed-payload replay test use a valid recomputed digest, and added malformed-envelope tests. 30 test methods now present in that file (static count only). Tests NOT RUN: `git clone` and the execution container could not resolve github.com. Existing Python workflow is pinned to historical SHA `319cffef121e327331aeaff59522ae279b112ecc`; it cannot verify current branch source.
- Previous research note remains `AI_COLLAB/FULL_POWER_GAP_RESEARCH_20261114.md`.

## Completed this unit
- Journal/receipt model from `97b302f`: conflict attribution, separate high-waters, receipt fingerprint binding and successor immutability; 5 focused tests added (NOT RUN).
- Grant model from `45cb200`: progress semantic no-op, versioned event/outbox parity and canonical consumer digest/envelope validation.
- Grant regression test correction `ed4d821`: stale future fixture now canonical; same event identity with a changed but valid canonical payload is rejected as a conflict; malformed source/event-id/version/state envelopes rejected before consumer state mutation. Added one test method with four malformed subcases. Total 30 test methods in grant suite (static count only). NOT RUN.
- No adapter, provider, runtime, storage, canonical LOOP/CASE/D/OD ID, PR or infrastructure changes.

## Next
1. Obtain exact-tree test execution without changing the pinned historical workflow. This environment cannot resolve github.com; current tests remain NOT RUN.
2. Red-team journal/receipt composition: conflict sequence references remain caller-supplied and range-validated, not independently resolved against journal contents. Design a narrow EventJournal snapshot boundary that derives watermarks and conflict references rather than accepting unrelated scalar claims.
3. Extend grant model tests for transition replay/order and outbox delivery semantics. Keep relay fencing and atomic consumer inbox implementation gated.
4. Preserve report-v2 gate, format-1 compatibility, CASE-04 INCOMPLETE / timed_out, and the successful Pyodios `summary.json`.

## Constraints
- $0; no paid service, provider/runtime/database/transport/storage/host selection, deployment, DNS, PR #2/#3/#4 changes or external AI request.
- Preserve LOOP-01..14, CASE-01..16, D-IDs and OD-01..OD-13. PocketCode and RevDev remain separate.
- Explicit paste/import only; no clipboard polling, overlays or automatic capture. Untrusted code requires disposable externally constrained execution; stock Pyodide/WASM remains trusted-light-task only.
- No adapter/device/browser acceptance or artifact rerun. P39 implementation/adapter gate CLOSED.
- Resume sequence: BOOT, STATE, NEXT_TASK, CHECKPOINT, INBOX_chatgpt, live HEAD/latest five; INDEX only after startup. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
