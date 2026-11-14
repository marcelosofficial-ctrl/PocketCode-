# NEXT TASK: PocketCode

## Goal
Continue bounded model-only evidence closure. Owner authorization covers source/test work for journal conflict attribution and receipt watermarks. P39 implementation/adapter conformance remains CLOSED.

## Verified snapshot (2026-11-14)
- Grant model `45cb200`; grant regression correction `ed4d821`. The focused grant suite has 30 methods (static count only); exact-tree execution remains NOT RUN.
- Journal snapshot implementation commits: `9f0ade8`, `af0c770`, `91c0d12`, `a4e27bb`. EventJournal derives immutable snapshots with global high-waters and conflict sequences scoped to an exact effect/attempt. Receipt creation consumes a sealed snapshot, rejects mismatched scope and caller-supplied scalar claims, and fingerprints derived values. Tests add cross-scope isolation and immutable-capture coverage (static review only).
- Actions run #63 (`43627117644`) passed 266/266 on Python 3.12.16 / Ubuntu, but checked out historical SHA `319cffef121e327331aeaff59522ae279b112ecc`. It does not verify the snapshot changes. Latest docs head `284bc8b` has zero Actions runs/status contexts. Local clone/test path previously failed DNS; current-tree tests remain NOT RUN.
- Previous research note: AI_COLLAB/FULL_POWER_GAP_RESEARCH_20261114.md.

## Completed this unit
- Added EventJournal.receipt_snapshot(effect_id, attempt_id) to derive journal-global observation/accepted-event high-waters and exact-attempt conflict sequence references.
- ResultReceiptStore.create_receipt requires a valid sealed snapshot for nonzero journal evidence, checks effect/attempt identity, rejects caller-supplied values and includes derived values in the immutable receipt fingerprint.
- Added regression tests for exact scope, other-attempt conflict isolation, immutable snapshots after later appends, successor receipts, wrong-scope rejection, caller-value rejection, mixed inputs and unsealed dataclass construction rejection.
- Commits: 9f0ade8, af0c770, 91c0d12, a4e27bb.
- No adapter, provider, runtime, storage, canonical LOOP/CASE/D/OD ID, PR or infrastructure changes.

## Next
1. Obtain exact-tree test execution for current source/test head a4e27bb. Run #63 is historical-only and does not cover it.
2. Red-team snapshot fabrication, serialization/copy behavior, snapshot timing and receipt revision semantics. The private seal is an in-process guard, not cryptographic isolation.
3. Extend grant model tests for transition replay/order and outbox delivery semantics. Keep relay fencing and atomic consumer inbox implementation gated.
4. Preserve report-v2 gate, format-1 compatibility, CASE-04 INCOMPLETE / timed_out, and the successful Pyodios summary.json.

## Constraints
- $0; no paid service, provider/runtime/database/transport/storage/host selection, deployment, DNS, PR #2/#3/#4 changes or external AI request.
- Preserve LOOP-01..14, CASE-01..16, D-IDs and OD-01..OD-13. PocketCode and RevDev remain separate.
- Explicit paste/import only; no clipboard polling, overlays or automatic capture. Untrusted code requires disposable externally constrained execution; stock Pyodide/WASM remains trusted-light-task only.
- No adapter/device/browser acceptance or artifact rerun. P39 implementation/adapter gate CLOSED.
- Resume sequence: BOOT, STATE, NEXT_TASK, CHECKPOINT, INBOX_chatgpt, live HEAD/latest five; INDEX only after startup. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
