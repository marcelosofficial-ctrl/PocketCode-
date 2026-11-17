# Recovery: receipt provenance patch route and read cap

Date: 2026-11-17
Branch: `pocketcode-ai-workflow-director-research-2026-10-28`

## Verified this pass
- Prior DONE `1f42f96118b8db1b1bfae00740d8f6ce74a5f7dd` to current pre-completion head `096fddc60dcfe060d7bef45b43a91887975d82fe`: 1 ahead / 0 behind; only `AI_COLLAB/CHECKPOINT.md` changed.
- Latest five branch commits, newest first: `096fddc` (start pass), `1f42f96` (complete prior checkpoint), `936e64f` (receipt provenance read-budget recovery), `d64b54b` (begin receipt provenance pass), `d59ca7b` (complete bounded recovery).
- Exact-head status contexts: 0; check runs: 0; Actions workflow runs: 0.
- GitHub connector exposes complete-file replacement and Git blob/tree/commit operations, but no patch-application action. PR patch retrieval is read-only and only works for files already changed in a PR.
- BOOT, STATE and NEXT_TASK consumed the three-file read cap. INBOX and source/test files were not read. No source or test change was made.

## Evidence and next step
- Tests and CI: NOT RUN. P39 adapter conformance remains CLOSED; CASE-04 remains INCOMPLETE / `timed_out`.
- The current per-turn rule (three files total) conflicts with the mandatory three startup reads and leaves no capacity for source inspection. Resolve this by explicitly allowing either a fourth targeted source/test read or a reduced continuation startup sequence. Do not silently exceed the cap.
- Once resolved, inspect only targeted excerpts in `scripts/event_journal.py`, `scripts/result_receipts.py` and the focused receipt tests; apply a verified minimal patch only through a genuinely patch-capable working tree. Preserve the exact live-journal derivation contract and all adapter/security gates.
