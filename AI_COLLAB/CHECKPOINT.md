STATUS: DONE — 2026-11-20.
- RECOVERED: owner commits `bba1297` (exact-head CI), `83a0690` (strategy/inbox), `a1b5278` (site/inbox); startup files reread fresh after newer commits.
- VERIFIED exact-head run #69 checked out triggering SHA `bba12979794053c19cae2896f597ba2bcaf59f61` and ran 279 tests; 1 failed. Historical pinned P40 job succeeded.
- VERIFIED failure: `test_late_journal_conflict_creates_immutable_successor_receipt` expected `(2,1,(2,))` but observed `(4,3,(2,))`. Targeted test fixture `journal_snapshot()` creates a fresh four-record journal each call, yielding global highwaters 4/3 and effect-1 conflict `(2,)`; another test correctly expects `(4,3,(2,))`. INFERRED this is a stale test expectation/fixture semantics mismatch, not demonstrated production defect.
- INFERRED exact-head CI exposed a false test expectation; freshness regression coverage still missing. The owner-added lane is useful and stays.
- Added recovery note `3a70175` and CI failure triage note `a43a4d5`; no code/workflow edits by ChatGPT.
- Tests: exact-head FAIL (279, 1 test assertion failure); pinned P40 PASS. No additional tests run.
- Next: correct fixture/test intent with patch-capable editing, then implement outbox timestamp guards; follow up receipt snapshot freshness as distinct test.
