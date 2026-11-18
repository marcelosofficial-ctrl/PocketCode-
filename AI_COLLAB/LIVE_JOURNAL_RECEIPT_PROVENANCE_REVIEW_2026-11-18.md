# Live-journal receipt provenance — implementation review (2026-11-18)

## Current branch findings

- VERIFIED: `EventJournal.receipt_snapshot(effect_id, attempt_id)` derives observation high-water, accepted-event high-water and exact effect/attempt conflict sequence references from the journal's current in-memory collections.
- VERIFIED: `ResultReceiptStore.create_receipt(..., journal_snapshot=...)` accepts a detached snapshot and copies its values into an immutable receipt. It validates snapshot type/seal and effect/attempt identity, but does not consult the live journal.
- VERIFIED: the snapshot seal is not a security boundary. `event_journal._JOURNAL_SNAPSHOT_SEAL` is an importable module attribute, and the module also exposes the predicate that accepts it.
- VERIFIED: existing tests prove snapshot object immutability and scope matching, but do not prove freshness at receipt creation. A caller can capture a snapshot, append a same-attempt conflict, and then create a receipt from the stale snapshot.
- VERIFIED: tests currently use `journal_snapshot=` in the watermarks test and late-conflict successor test; the test helper returns a detached snapshot. The unsealed-snapshot test directly constructs the dataclass and expects TypeError.
- INFERRED: receipt immutability and revision-key fingerprinting already provide the right immutable-history behavior once the source evidence is captured freshly. If evidence changes after a receipt exists, create a new successor revision; do not mutate the predecessor.

## Narrow API correction

1. Change the receipt API to accept `journal: Optional[EventJournal] = None`, not a detached snapshot.
2. If supplied, require `isinstance(journal, EventJournal)` and derive exactly once inside `create_receipt` via `journal.receipt_snapshot(effect_id, attempt_id)`. Derivation must happen as part of receipt creation, not in the caller before invocation.
3. Keep the zero-watermark behavior when no journal is supplied only if the compatibility contract still requires receipts without journal evidence. Do not interpret zero as proof that no events exist.
4. Reject any non-None legacy `journal_snapshot` and all caller-supplied watermark/ref values. Keeping deprecated keyword parameters temporarily is acceptable if they fail closed with `ReceiptConflict`; otherwise remove them and migrate every call site.
5. Remove the seal/predicate as a claimed provenance control. The snapshot may remain a frozen value object returned by EventJournal for diagnostics/tests, but possession of a snapshot is not proof of origin.
6. Preserve the current validation of integer watermarks, accepted-high-water <= observation-high-water, immutable ordered unique conflict sequences, and exact effect/attempt scope. These checks are defense-in-depth, not authentication.
7. Capture once and bind those values into the canonical receipt fingerprint. Do not re-read the journal midway through one receipt construction.

## Concurrency contract

- The current journal is an in-memory synchronous model with no demonstrated lock around `append` and `receipt_snapshot`.
- A direct journal parameter closes the detached-snapshot freshness gap for the intended single-owner/synchronous model, but does not by itself guarantee an atomic prefix if another thread can append concurrently.
- Explicitly document EventJournal as single-threaded/not thread-safe unless a real concurrency requirement is accepted. If concurrent append is required, add one journal-owned lock covering both mutation of sequence/event/conflict collections and the entire snapshot read. A receipt must call the locked snapshot method once. Do not claim cross-process or durable transactionality.
- Avoid adding an EventJournal-to-ResultReceiptStore callback/transaction protocol in this narrow model change. That would be a separate design decision.

## Required regression coverage

1. `test_receipt_creation_derives_snapshot_from_live_journal`: append accepted seq 1 and same-identity conflicting seq 2; call create_receipt with the journal object; assert observation high-water 2, accepted high-water 1 and scoped conflicts `(2,)`.
2. `test_receipt_includes_conflict_arriving_after_old_snapshot_capture`: capture a diagnostic snapshot, append a same-attempt conflict, then create with the live journal. Assert the receipt includes the later conflict and current high-waters. The detached snapshot must not be an input to receipt creation.
3. `test_receipt_conflict_refs_are_exact_effect_attempt`: include conflicts for another effect/attempt and assert only matching refs are included while watermarks remain journal-global.
4. `test_receipt_rejects_detached_snapshot_and_scalar_claims`: passing an old snapshot or caller-claimed watermark/ref tuple cannot create journal provenance.
5. `test_receipt_successor_binds_late_conflict_without_mutating_predecessor`: create version 1, append a late conflict, create version 2 from the live journal and assert predecessor hash/conflict tuple unchanged while successor contains new evidence.
6. `test_same_revision_key_after_journal_advance_conflicts`: replaying the same revision key after new journal evidence changes the canonical fingerprint must conflict; caller creates a new revision key linked to the prior receipt.
7. Preserve zero-journal compatibility only as explicitly non-evidentiary values; test that no-journal receipt carries zeros and does not claim a journal was consulted.
8. If thread safety is explicitly added, add a barrier-controlled append/snapshot test proving a coherent prefix. Otherwise tests must not imply concurrent safety.

## Scope / evidence limits

- This is an in-memory model correction, not producer authentication. `AuthenticatedProducer` remains a trusted-adapter assertion; this module does not verify keys, signatures or credentials.
- A live object reference is not durable storage, a transaction boundary, or cross-process coordination.
- The exact journal snapshot still contains only current journal high-waters and scoped conflict references; it does not establish provider-side execution truth or independently validate the evidence payloads named by other receipt fields.
- Do not change report format 1, P39 adapter conformance, CASE-04, provider/runtime/adapter choices, workflows, PRs, or canonical LOOP/CASE/D/OD identifiers.
- Tests/CI must run on the exact source SHA after implementation. Existing Actions #63 is historical SHA-only evidence, not proof for current changes.

## Editing / next action

The current GitHub tool surface offers complete-file replacement and Git object creation, but no safe patch/hunk application or writable checkout. Do not reconstruct or replace the large `result_receipts.py` or `test_result_receipts.py` files. Apply this change in a patch-capable working tree, inspect the resulting diff, run focused tests then the full suite on that exact tree, and record the SHA/results. Keep the outbox timestamp guard packet as a separate narrow change.
