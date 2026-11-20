# Exact-head failure: corrected test intent analysis (2026-11-20)

## VERIFIED fixture behavior
The `journal_snapshot()` helper in `scripts/test_result_receipts.py` constructs a new `EventJournal` on every call and appends four observations (two accepted records and two conflicting records across two effect/attempt scopes). It then returns a snapshot for `effect-1/attempt-1`, whose global observation/accepted watermarks are 4/3 and scoped conflict tuple is `(2,)`. The `test_receipt_uses_journal_derived_watermarks_and_conflicts` assertion already expects `(4,3,(2,))`.

## Diagnosis
**INFERRED — confirmed fixture/test mismatch, not a demonstrated product defect:** `test_late_journal_conflict_creates_immutable_successor_receipt` calls the same fresh-journal helper but expects `(2,1,(2,))`. It never captures an earlier snapshot and appends a later conflict to the same journal; thus it does not actually exercise “late conflict” behavior. CI's `(4,3,(2,))` is consistent with the helper and exact-scope filtering.

## Minimal correction options (do not implement until patch editing is available)
- If test intent is simply successor immutability: change expected tuple to `(4,3,(2,))`, and rename test to describe immutable successor snapshot of scoped journal evidence. This makes it consistent with helper and sister test, but does **not** test late-arriving conflict freshness.
- If intended to test late-conflict freshness: refactor the helper to return/retain the same journal instance; create first receipt with snapshot at earlier point; append a genuinely later conflicting observation for `effect-1/attempt-1`; create successor snapshot from that same journal. Assert first receipt unchanged, successor high-water advances, scoped conflict refs contain new sequence, and other-attempt conflicts are excluded. This is the stronger regression and preferable if test is intended to cover freshness.

No code changed. Source edit requires a patch-capable checkout/editor; whole-file replacement is unsafe.
