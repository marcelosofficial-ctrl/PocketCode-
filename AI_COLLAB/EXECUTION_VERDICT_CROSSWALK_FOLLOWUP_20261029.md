# PocketCode Execution Verdict Crosswalk — Follow-up 2026-10-29

**Status:** Read-only semantic review; documentation follow-up only.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Authority:** `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` and its CASE criteria remain canonical. This note does not amend acceptance, freeze schema, or authorize source/test changes.

## 1. Scope and exact artifacts inspected

- Canonical acceptance: `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.
- Execution contract: `PRODUCT/EXECUTION_CONTRACT.md`, blob `128a00a9b2a335514814cab76fb5781fe8f9f858`.
- Pure report helper: `scripts/report_contract.py`, blob `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817`.
- Unit test source: `scripts/test_report_contract.py`, blob `85109f056009d65a274e9306deb39b68e1fefbd2`.
- Owner decision register: `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md`, blob `e67b2659cf2d71ef77d8e4619c91143e71062470`.
- Prior reconciliation: `AI_COLLAB/EXECUTION_VERDICT_ARTIFACT_RELEASE_RECONCILIATION_20261029.md`, blob `8f0d592995a625f9bf47ac15848c92008e15f855`.

These are GitHub blob observations. No code was run and no tests were executed.

## 2. Confirmed static discrepancy: timeout status can be overridden by exit code

The current helper `classify_verdict(execution_status, exit_code)` checks whether a valid integer exit code is nonzero **before** checking `execution_status == "program_failed"` or the successful-exit condition. Consequently, `classify_verdict("timed_out", 124)` returns `FAIL` under the current code, as would any trusted `timed_out` status paired with a nonzero integer termination code.

Canonical CASE-04 says a deadline/infinite-loop case is `INCOMPLETE / timed_out` only when trusted execution control confirms the timeout outcome. LOOP-05 also says timeout outcomes cannot be shown as success. The D-01 owner register explicitly preserves this canonical timeout mapping and says not to reclassify a timeout as FAIL merely because a trusted limit caused termination.

The existing test `test_timeout_cancel_rejection_and_infrastructure_failure_are_incomplete` tests these statuses only with `exit_code=None`. It therefore does not cover a timeout paired with a nonzero code, including a code emitted by a timeout/termination wrapper. This is a **test-coverage gap and potential verdict-precedence defect**, established by static reading, not by executing the helper.

### Required next review (do not implement in this pass)

1. Ask the contract owner/independent reviewer to confirm the intended precedence when trusted terminal lifecycle state is `timed_out` and an exit/termination code is nonzero.
2. Distinguish an authoritative child-program exit code from a wrapper/termination code. Do not assume every nonzero integer is proof of a program failure.
3. If canonical CASE-04 remains authoritative, prepare a minimal proposed regression case for `timed_out` + nonzero termination code that expects `INCOMPLETE`, alongside `succeeded` + nonzero child exit expecting `FAIL` and `program_failed` expecting `FAIL`.
4. Before any implementation, decide whether the minimal fix belongs in classifier precedence, explicit exit-code provenance, or a richer evidence input. Preserve the observed code and lifecycle state even when the user-facing verdict is INCOMPLETE.
5. Update source/tests only after explicit task authorization; do not change canonical acceptance silently. Then run the exact focused suite only when an execution environment is available and authorized.

Do not blindly change the classifier to always prioritize `timed_out` without reviewing contradictory or malformed evidence. If lifecycle status and exit-code provenance conflict, preserve both and use the contract's conservative outcome.

## 3. Remaining semantic crosswalk

| Area | Canonical rule | Current static observation | Status |
|---|---|---|---|
| PASS | LOOP-03 / CASE-01: trusted successful terminal evidence and exit 0 | Helper returns PASS only for `succeeded` + integer exit 0; simulated formatter forces INCOMPLETE | Static alignment observed; tests NOT RUN |
| Program failure | LOOP-04 / CASE-02/03/10: confirmed program/runtime failure or nonzero program exit | Helper returns FAIL for `program_failed` or any nonzero integer exit, without exit-code provenance | Timeout/wrapper ambiguity above remains OPEN |
| Timeout | LOOP-05 / CASE-04: trusted timeout → INCOMPLETE / timed_out | Nonzero integer exit currently takes precedence over `timed_out` | Static discrepancy; owner/reviewer decision required |
| Provider/infrastructure failure | LOOP-05 / CASE-06/11/13: uncertain child result remains INCOMPLETE; no fabricated exit | Missing exit or infrastructure status yields INCOMPLETE, unless a nonzero integer is also supplied | Provenance/precedence needs explicit cross-check |
| Artifact-free task | LOOP-03, LOOP-10 and contract release clarification: no universal file-presence gate | Classifier does not depend on files; formatter lists supplied file metadata | Static alignment observed; no release implementation reviewed |
| Artifact release | Execution PASS is not release authorization | Formatter renders metadata only; no release decision or enforcement exists in this helper | Separate boundary; NOT IMPLEMENTED/NOT RUN here |
| Script-reported checks | CASE-09: process PASS can coexist with script-reported failed check | Formatter retains supplied check lines and provenance; verdict is based on supplied status/exit | Static alignment observed; input trust is caller responsibility |
| Run identity/retry | LOOP-09, CASE-13, CASE-16 | This pure formatter cannot prove durable identity, authoritative recovery or no duplicate dispatch | Outside helper; not verified by this review |

## 4. Product-direction and repository boundaries

The current PocketCode research documents and RevDev's current workflow master now record the owner's clarified destination: one coherent PC-and-phone product/program, with separate repositories, roadmaps, implementations, clients/adapters, acceptance suites, evidence and release gates during development. Integration topology remains undecided and approval-gated. This is a direction clarification, not merge or shared-runtime authorization.

PocketCode PR #2 and PR #3 remain separate and untouched. Canonical acceptance IDs were not changed. D-01..D-04 remain open as marked; working defaults are not frozen schema decisions.

## 5. Explicit limits

- No source or test changes.
- No tests run.
- No provider, runtime, account, billing, workload, Actions, merge, deployment, or PR #2/#3 action.
- No claim that the current code is integrated into a production execution path.
- `scripts/lifecycle_contract.py` was absent from the inspected research branch and `main` at the time of the prior audit; do not infer it exists in another revision without re-fetching that exact ref.

## 6. Next bounded task

Get independent review of the timeout/nonzero-code precedence issue, then do one exact-ref static scan for other verdict-precedence combinations where lifecycle terminal state and exit-code provenance conflict. Return a compact table of source lines, canonical CASE/LOOP rule, expected outcome, current helper behavior, and whether a source/test change is actually justified. Do not expand into another general architecture review.


## 7. Cross-branch follow-up — candidate fix exists in PR #2, not merged (2026-10-29)

A fresh exact-ref comparison changes the next-step framing but does not erase the main-branch finding:

| Ref | Helper blob | Relevant behavior | Test blob/status |
|---|---|---|---|
| `main` | `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817` | Any valid nonzero `exit_code` returns FAIL before status-specific handling; `timed_out` + 137 therefore maps to FAIL | Test blob `85109f056009d65a274e9306deb39b68e1fefbd2`; does not test nonzero code with timeout |
| Research branch `pocketcode-ai-workflow-director-research-2026-10-28` | Same as `main` at this check | Same static discrepancy | Same as `main`; NOT RUN |
| PR #2 branch `chat-continuity-report-regressions-2026-10-26` | `e9d944a722c2fac5279952696528da72a7011af3` | Candidate classifier returns FAIL for `program_failed`; uses `exit_code` to choose PASS/FAIL only when status is `succeeded`; other states, including `timed_out` with nonzero code, remain INCOMPLETE | Test blob `39f3a3ef865ed55f333a1edc208096d99197d023`; includes `test_nonzero_exit_does_not_override_uncertain_lifecycle`, covering `timed_out/137`, `cancelled/143`, infrastructure failure, rejection, running and unknown states. Tests NOT RUN. |

PR #2 was re-fetched as open/draft/unmerged at head `eb8b7ea83cb0e8fe1880351276c485b761431791`. The candidate fix and regression test exist on that branch but are not merged into `main`; do not describe the main-branch issue as fixed or imply the PR's tests passed. No PR action or source/test edit was performed during this comparison.

### What remains for independent review

The PR #2 candidate appears to fix the specific status-precedence mismatch for timeout/cancellation/rejection/infrastructure/nonterminal states. It does not add exit-code provenance to the helper interface. The review should determine whether that is sufficient under the intended caller contract:

- `exit_code` must be the authoritative child-program exit code when it is used to classify `succeeded`; a wrapper/termination code must not be misrepresented as the child's exit.
- A trusted `timed_out` terminal state must remain INCOMPLETE / `timed_out`, even if an external wrapper reports a nonzero termination code.
- `succeeded` + nonzero code is expected FAIL only when the code is the authoritative child-program exit under the contract; contradictory lifecycle/exit evidence must not be silently normalized.
- `program_failed` is a separate authoritative lifecycle fact and may classify FAIL without a numeric exit code.
- Preserve raw status and code in the report even when the verdict is INCOMPLETE.

**Next task:** read the exact PR #2 helper/test and canonical CASE-04/LOOP-05 together; provide a narrow static verdict table and proposed additional test only if a real uncovered case remains. Do not edit PR #2, tests, canonical acceptance, or implementation. Independent Claude/Gemini review is optional input; if unavailable, continue read-only and mark it outstanding.

No tests were run. No implementation, PR, provider, runtime, deployment, or canonical acceptance changes occurred.
