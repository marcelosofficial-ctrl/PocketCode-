# NEXT TASK: PocketCode — receipt provenance/freshness

## Goal
Remove detached snapshot provenance: ResultReceiptStore must accept the live EventJournal and derive receipt evidence inside create_receipt(). Keep global observation/accepted-event high-waters and effect/attempt-scoped conflict sequences.

## Implementation route (VERIFIED available)
GitHub connector has no patch endpoint, but Code Mode GitHub tools can fetch full file contents into an in-memory JS string, apply asserted exact-anchor edits, create blobs, build a tree atop the fetched commit's base tree, create a commit, and update the branch with expected-SHA lease. This avoids reconstructing large files. Never output or recreate the 45.6 KB test file manually.


## Planned changes
1. Import EventJournal (module/package fallback); remove detached JournalReceiptSnapshot/private seal reliance.
2. Replace create_receipt's journal_snapshot/scalar parameters with journal: Optional[EventJournal]. For a supplied live journal, call receipt_snapshot(effect_id, attempt_id) inside create_receipt; preserve scope validation and watermark/ref validation. No-journal behavior remains zero evidence.
3. Convert fixture helper to return the live journal, migrate callsites; explicit detached journal_snapshot= rejection via TypeError.
4. Correct late-conflict regression: create predecessor receipt first; append a conflict to the SAME journal afterward; create successor using that journal; verify successor contains the late sequence and predecessor fingerprint/evidence remains unchanged.
5. Inspect EventJournal locking; if no coherent snapshot lock, explicitly document non-thread-safe model/adapter locking obligation.
6. Run exact-head CI and record exact SHA/result only if output is available.

## Constraints
Use <=2 files/commit, anchor assertions, print targeted diffs before commit. No workflow/adapter/runtime/provider changes; tests remain NOT RUN until exact output.