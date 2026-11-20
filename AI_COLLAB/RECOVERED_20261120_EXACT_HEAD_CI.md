# RECOVERED — 2026-11-20

**VERIFIED:** Since prior checkpoint `22d1993`, owner added commit `bba1297` with an exact-triggering-SHA CI job beside pinned historical P40; commits `83a0690` and `a1b5278` also updated strategy and inbox/site-plan context. Recovery read CHECKPOINT, BOOT, STATE, NEXT_TASK, and INBOX_chatgpt fresh. No unrelated source files inspected.

**CI result:** Run #69 (`44705940495`) for `bba12979794053c19cae2896f597ba2bcaf59f61`. Historical `unittest` job succeeded on pinned P40. New `unittest-head` checked out the triggering SHA correctly but failed full suite: 279 tests, 1 failure, `test_late_journal_conflict_creates_immutable_successor_receipt` expected `(2,1,(2,))`, got `(4,3,(2,))`. This directly exposes receipt snapshot freshness defect (high-water advances; conflict ref tuple remains unchanged). See run/job log. Recovery complete; next unit is diagnosis of stale conflict-ref scoping/snapshot semantics, not workflow editing.
