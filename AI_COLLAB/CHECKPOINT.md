# CHECKPOINT — 2026-11-14

- Startup sequence re-read in required order. Start HEAD: 03deccd1c9a8e52d1c55511223a71610f1f08ac6; latest five commits inspected.
- Added journal-derived receipt evidence:
  - EventJournal.receipt_snapshot(effect_id, attempt_id) captures journal-global observation/accepted-event high-waters and conflict sequences scoped to the exact effect/attempt.
  - JournalReceiptSnapshot is immutable and carries a private module seal. Receipt creation rejects ordinary fabricated dataclasses, mismatched effect/attempt, mixed snapshot/manual values and caller-supplied scalar claims.
  - ResultReceiptStore.create_receipt fingerprints derived snapshot values, preserving immutable successor semantics.
  - Tests cover cross-effect/attempt conflict isolation, immutable capture after later appends, successor receipt binding, wrong-scope snapshots, manual-value rejection, mixed-input rejection and unsealed construction rejection.
- Source/test commits: 9f0ade8 (snapshot derivation), af0c770 (seal), 91c0d12 (package-mode imports), a4e27bb (scope and immutability tests).
- Docs commits: 1af5096 and follow-up correction pending.
- Actions run #63 (43627117644) triggered by 9f0ade8 completed SUCCESS, 266/266, Python 3.12.16, Ubuntu. It checked out fixed historical SHA 319cffef121e327331aeaff59522ae279b112ecc, so it did not execute or verify snapshot changes. Latest head 1af5096 has zero Actions runs/status contexts.
- Snapshot source/test changes: static review only; current-tree tests NOT RUN. Prior local clone/execution path could not resolve github.com.
- Private seal is an in-process guard, not cryptographic isolation. Durable journal/store atomicity and authenticated producer proof remain adapter obligations.
- P39 implementation/adapter gate CLOSED; CASE-04 INCOMPLETE / timed_out; report-v2 gated; preserve successful Pyodios summary.json.
- Next: exact-tree tests; red-team snapshot serialization/copy/timing and receipt revision semantics; grant transition replay/order and outbox delivery tests.
