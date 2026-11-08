# NEXT TASK: PocketCode   (one task; under 350 words)

## Goal
Write the child-exit vs wrapper-exit vs termination provenance resolution as a short spec section plus a list of test cases, so scripts/report_contract.py can be changed safely later. No code change in this task.

## Files to read
- [Exit provenance matrix](VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md) (read it in sections)
- scripts/report_contract.py (function and class names first, then only the classifier)
- STATE.md open item O-5

## Constraints for this task
- Mode: normal. About 350 lines per turn. Commit the draft to GitHub before summarizing.
- Keep CASE-04 as INCOMPLETE / timed_out. Do not make a precedence-only patch. Do not claim any device or product test that was not run.
- Out of scope: choosing a runtime, provider or database; changing LOOP, CASE or D IDs; touching PR #2 or #3.

## Steps
1. List the observable facts a result can carry: child exit, wrapper exit, termination confirmation, timeout, contradictory observations.
2. Write a resolution table: which combinations give PASS, FAIL, INCOMPLETE, UNKNOWN, and why.
3. Write test cases (inputs and expected verdicts) that would fail on a precedence-only patch.
4. Save to AI_COLLAB/EXIT_PROVENANCE_RESOLUTION_<date>.md and add a row to INDEX.md.

## Done when
- The new file exists and is committed, the CI run for the commit is checked, and STATE.md, CHECKPOINT.md and INBOX_claude.md (a request for review) are updated.

## If blocked
Write the blocker in CHECKPOINT.md and stop.
