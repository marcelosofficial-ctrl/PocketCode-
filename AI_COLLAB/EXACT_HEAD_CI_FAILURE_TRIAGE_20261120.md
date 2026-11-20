# Exact-head CI finding — 2026-11-20

## VERIFIED
- Owner-added `unittest-head` lane checked out exact triggering SHA `bba12979794053c19cae2896f597ba2bcaf59f61`; explicit equality check passed.
- Workflow run #69 / `44705940495`: pinned historical P40 job succeeded; exact-head job failed.
- Exact-head full suite ran **279 tests, 1 failure**. Failing test: `test_late_journal_conflict_creates_immutable_successor_receipt` (`scripts/test_result_receipts.py:143`). Assertion expected successor snapshot `(observation_high_water=2, accepted_high_water=1, conflicts=(2,))`; observed `(4,3,(2,))`.

## Interpretation (INFERRED)
The successor receipt is reflecting newer global journal high-waters, but its exact effect/attempt conflict-sequence references remain at `(2,)`, rather than capturing the newer conflicts expected by the test. This is a composition/freshness/scoping inconsistency in receipt creation or its fixture—not proof of broad receipt corruption. The assertion gives an actionable failure but the source must be inspected at targeted lines and matching test fixture before attributing root cause.

## Red-team / next checks
1. Read only targeted lines of `scripts/result_receipts.py`, `scripts/event_journal.py`, and the failing test (max 3 source/test files; small line windows).
2. Trace which journal instance/snapshot is used for successor creation and what conflict filter defines `(2,)`; compare the later conflicts' effect/attempt identities.
3. Decide whether code defect or test fixture scope mismatch; preserve exact scope semantics. Add minimal regression only with patch-capable editing and owner authorization already granted for model-only source/test slice.
4. Re-run exact-head CI after correction; the new lane is useful and should remain separate from historical P40.

No source changes or workflow edits in this pass. Exact-head test is **FAIL** for this SHA; historical P40 is **PASS**. Current branch subsequent SHA test status remains unknown until a new run.
