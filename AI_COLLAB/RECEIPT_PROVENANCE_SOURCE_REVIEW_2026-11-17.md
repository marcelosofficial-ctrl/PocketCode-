# Receipt provenance: source inspection and safe implementation boundary

Date: 2026-11-17
Branch: `pocketcode-ai-workflow-director-research-2026-10-28`

## VERIFIED source findings
- `EventJournal.receipt_snapshot(effect_id, attempt_id)` derives global observation high-water, accepted-event high-water, and exact effect/attempt conflict sequence references from the journal's current in-memory collections.
- `ResultReceiptStore.create_receipt(..., journal_snapshot=...)` accepts a detached `JournalReceiptSnapshot`, checks its module sentinel and effect/attempt identity, then copies its values into an immutable receipt. It does not receive or consult the live journal.
- Therefore a valid snapshot can become stale: append a same-attempt conflict after snapshot capture but before receipt creation, and the receipt can still be created without that later conflict. This is a TOCTOU/provenance freshness gap, not a forgery of the snapshot's original values.
- The private sentinel and frozen dataclass do not bind snapshot freshness to receipt-creation time. The existing test `test_journal_snapshot_is_immutable_and_conflicts_are_attempt_scoped` proves snapshot stability, not freshness at receipt creation.
- Existing tests explicitly exercise `journal_snapshot=` on receipt creation; changing this contract requires migrating these call sites and the focused tests.

## Recommended narrow correction (not implemented)
1. Change receipt creation to accept an `EventJournal` instance (or a narrowly typed journal protocol) instead of a detached `JournalReceiptSnapshot`.
2. At the receipt-creation boundary, derive the scoped snapshot internally using the receipt's exact `effect_id` and `attempt_id`; reject non-journal objects and remove the detached snapshot as a caller-supplied provenance input.
3. Keep legacy scalar watermark/conflict arguments rejected. Preserve zero-valued journal fields only when no journal is explicitly supplied, if that remains the intended compatibility contract.
4. Add regression: create journal with accepted event + conflict, then append another conflicting duplicate after the old snapshot would previously have been captured; call receipt creation with the live journal and assert the later sequence is present. Also assert exact effect/attempt scoping, global watermarks, mismatch prevention, and successor immutability.
5. Document the model's single-owner synchronous contract. If concurrent append is to be supported, add a journal lock covering append mutation and snapshot derivation; do not claim atomicity without it.

## Safety and scope
- No source/test changes were made. The connector exposes full-file replacement, not hunk patching; these files are large, so reconstructing/replacing them would violate the no-large-file-rewrite rule.
- No provider, adapter, runtime, storage, workflow, device, PR, or acceptance-ID changes.
- Tests and CI: NOT RUN. Current-tree conformance remains unverified; P39 adapter conformance remains CLOSED; CASE-04 remains INCOMPLETE / `timed_out`.
- Next action: use a local/patch-capable GitHub editing path for the narrowly scoped implementation and tests, then run the exact-tree focused tests before updating any conformance claim.
