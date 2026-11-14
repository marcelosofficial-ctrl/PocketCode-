# CHECKPOINT — 2026-11-14

- Startup sequence re-read in required order; active branch head at start: `03deccd1c9a8e52d1c55511223a71610f1f08ac6`. Latest five commits inspected.
- Exact-head status at start: `03deccd` had zero Actions runs and zero status contexts.
- Added journal-derived receipt evidence:
  - `EventJournal.receipt_snapshot(effect_id, attempt_id)` captures global observation and accepted-event high-waters plus conflict sequences scoped to the exact effect/attempt.
  - `JournalReceiptSnapshot` is immutable and carries a private module seal. Receipt creation rejects ordinary fabricated dataclass instances, mismatched effect/attempt, mixed snapshot/manual values, and caller-supplied scalar watermarks/conflict sequences.
  - `ResultReceiptStore.create_receipt` fingerprints the derived snapshot values, preserving immutable successor semantics.
- Regression tests updated for journal-derived watermarks, exact scope, late conflict successor, caller-supplied value rejection, mixed-input rejection and unsealed construction rejection.
- Source/test commits:
  - `9f0ade8e502c87d34a57a73a9105714933305ed0` — derive receipt evidence from snapshots.
  - `af0c770c5df7eeaf40237e50f8931ded16869169` — add private snapshot seal.
  - `91c0d12de0dd5392947888147494be607857ddf3` — correct package-mode test imports.
- CI run #63 (`43627117644`) triggered by `9f0ade8` completed SUCCESS, 266/266, Python 3.12.16, Ubuntu. Critical limitation: workflow step "Check out immutable P40 target" checks out fixed historical SHA `319cffef121e327331aeaff59522ae279b112ecc`. Therefore run #63 does NOT execute or verify the snapshot source/test changes. Latest head `91c0d12` has not had its own Actions/status checked yet.
- Snapshot implementation has only static review so far; current-tree tests NOT RUN. Existing local clone/execution path could not resolve github.com.
- The private seal is an ordinary in-process guard, not cryptographic isolation against hostile Python code with module introspection. Durable journal/store atomicity and authenticated producer proof remain adapter obligations.
- Preserve P39 implementation/adapter gate CLOSED, CASE-04 INCOMPLETE / timed_out, report-v2 gated and successful Pyodios `summary.json`.
- Next: verify latest head CI; exact-tree tests; red-team snapshot serialization/copy/timing/scope behavior; then grant transition replay/order and outbox delivery tests.
