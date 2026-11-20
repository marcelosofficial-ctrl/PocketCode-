# GitHub Git-Data Patch Workflow — 2026-11-20

## Verified capability change

The connected GitHub toolset includes `create_blob`, `create_tree`, `create_commit`, and `update_ref` with `expected_sha`. This enables a small targeted patch without whole-file Contents API replacement, provided complete file contents are safely retrieved and the branch lease is respected. Previously source edits were blocked by the Contents API's whole-file replacement limitation; this restriction is now narrower, not gone.


## Safe patch protocol

1. Confirm branch head and read the target source/test file in bounded ranges. Do not read a file exceeding 1,500 words whole; if it exceeds that, use a local patch-capable workflow or split only after establishing a safe complete reconstruction method. Keep source/test inspection within the per-pass limit.
2. Retrieve each complete target file only when its size is within the allowed cap; preserve bytes/line endings and unrelated content. Apply an exact, asserted text replacement in the reconstructed complete file. If anchors are ambiguous, stop.
3. Create blobs for changed files. Create a tree with each changed path/mode/type/blob SHA over the verified base tree. Create a commit with the current head as parent. Update the branch using `force=true` plus `expected_sha=current_head` (force-with-lease) only as required by the API contract; do not use force without expected SHA. On rejection, re-fetch head and reconcile rather than retry blindly.
4. Keep a commit small, ideally one fix/test pair. Re-fetch the committed files and commit SHA to verify what was written. Test results remain NOT RUN until CI or executable test output exists.

## Prioritized implementation packet (unchanged scope)

### A. Receipt late-conflict regression (scripts/test_result_receipts.py)

- Current test uses `self.receipt` created without journal evidence and then calls `journal_snapshot()` to create a fresh journal already containing four events. It does not append a late conflict to the same retained journal after predecessor creation.
- Correct behavior to exercise: create a retained EventJournal and producer; establish initial scoped evidence; create predecessor receipt; append a conflicting event for effect-1/attempt-1 to that same journal; create successor with its newly derived snapshot; assert predecessor immutable; successor global observation high-water advances; accepted high-water does not advance for a conflict; exact target conflict sequences advance; conflict from another attempt is excluded.
- Existing expected snapshot for helper: global highwaters `(4,3)`, target conflicts `(2,)` (VERIFIED in prior pass). Do not alter this to hide fixture semantics.

### B. Outbox reconciliation timestamp validation (scripts/fake_outbox.py + scripts/test_fake_outbox.py)

- In `resolve_reconciliation`, both `found` and `not_found`/`absence_final=True` branches validate `now` only when it is non-None. Missing timestamp therefore accepted and persisted as None.
- Require a non-bool integer >=0 before any mutation in both positive reconciliation branches. Invalid inputs: `None`, `True`, float, string, negative. Keep unknown/non-final absence as `hold_unknown` and do not authorize retry.
- Test state immutability for invalid timestamps (all reconciliation/ack/state fields unchanged); positive `found` timestamps persist both acknowledgement and reconciliation time; final exact absence timestamp persists and still allows only same EffectId/AttemptId retry.

## Scope and caveats

- This unlocks a route to bounded source edits; it is not proof any edits or tests have occurred.
- Models are in-memory test fakes, not durable database/provider integrations. Caller-provided `authoritative` flags remain assumptions, not verified provider evidence.
- Tests have NOT RUN in this pass. Exact-head CI run #69 remains historically 279 tests / 1 failure; rerun required after actual repair.
- Limit next patch pass to receipt test fixture and timestamp guard with tests, then run focused tests and exact-head CI. Avoid production-boundary claims.
