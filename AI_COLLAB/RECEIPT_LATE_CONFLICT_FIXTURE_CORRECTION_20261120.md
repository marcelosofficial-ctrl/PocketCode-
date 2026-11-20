# Receipt late-conflict fixture correction — 2026-11-20

Status: VERIFIED source excerpt; CI interpretation remains unresolved without current run logs.

## Exact fixture facts

In `scripts/test_result_receipts.py`:
- `journal_snapshot()` constructs a **new** EventJournal each call.
- That fresh journal appends exactly two entries for effect-1/attempt-1: accepted event, then duplicate-ID conflict.
- It appends two additional observations for effect-2/attempt-2 (accepted then conflict), making global observation high-water 4 and accepted high-water 3; exact effect-1/attempt-1 conflicts are (2,).
- Therefore the expected tuple `(2, 1, (2,))` is inconsistent with this helper's global high-water semantics; the helper snapshot tuple is `(4, 3, (2,))`.
- The test still does **not** test a late conflict: each helper invocation creates a fresh journal and captures the same prebuilt event sequence. No conflict is appended after predecessor receipt creation on a retained journal.

## Correct repair (not expectation-only)

1. Retain one journal instance across receipt creation.
2. Capture initial snapshot and create predecessor receipt; assert predecessor watermarks/conflicts.
3. Append a later conflicting event to the same journal for exact effect-1/attempt-1.
4. Capture successor snapshot and create successor receipt linked to predecessor.
5. Assert predecessor unchanged; successor global observation high-water advances; accepted high-water does not advance for conflict; scoped conflict sequence includes later conflict.
6. Add a parallel conflict for another attempt and ensure excluded from exact-scope refs.

**Avoid a weak expectation-only fix.** `(4, 3, (2,))` corrects global watermarks but still does not test late-evidence successor behavior. Exact-head CI discrepancy requires current logs/run confirmation; prior result remains recorded.
