# PocketCode Verdict Precedence Recheck — 2026-10-29

**Status:** Read-only semantic crosswalk; documentation checkpoint only.
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`
**Authority:** `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` and its LOOP/CASE criteria remain canonical.
**Scope:** Re-fetch exact helper, tests, acceptance, execution contract and owner decision register; analyze lifecycle/exit-code precedence and directly adjacent combinations only.
**Restrictions:** No source/test/acceptance edits; no tests run; no provider/runtime calls; no PR #2/#3 action; no merge, deploy, spending, queue mutation or mission replay.

## 1. Exact artifacts re-fetched

| Path | Blob SHA | Finding |
|---|---|---|
| `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` | `c6714c27db52b2962fe8d1c7e6a16829d46a8338` | Canonical LOOP/CASE requirements |
| `PRODUCT/EXECUTION_CONTRACT.md` | `128a00a9b2a335514814cab76fb5781fe8f9f858` | Conceptual lifecycle; server/provider is authoritative |
| `scripts/report_contract.py` | `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817` | Current classifier source |
| `scripts/test_report_contract.py` | `85109f056009d65a274e9306deb39b68e1fefbd2` | Current test source |
| `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md` | `e67b2659cf2d71ef77d8e4619c91143e71062470` | D-01..D-04 remain open; D-01 working default preserves trusted timeout as INCOMPLETE |
| `AI_COLLAB/EXECUTION_VERDICT_CROSSWALK_FOLLOWUP_20261029.md` | `a57aa70254d70bd373bf150af85c1682ec34e8b9` | Prior cross-branch assessment |
| `AI_COLLAB/EXECUTION_VERDICT_ARTIFACT_RELEASE_RECONCILIATION_20261029.md` | `8f0d592995a625f9bf47ac15848c92008e15f855` | Prior report/artifact boundary review |

The requested RevDev + PocketCode handoff was re-fetched at blob `14e88707d34773ca156fe028735bfe2f0ec57e14`. The named branches are present in GitHub branch search. That search did not return current commit HEAD SHAs, so this checkpoint does not assert a verified current HEAD SHA.

## 2. Exact source semantics

In `scripts/report_contract.py`, `classify_verdict(execution_status, exit_code)` accepts an integer exit code except booleans. It first returns FAIL when the code is nonzero **or** status is `program_failed`. Only afterward does it return PASS for `succeeded` plus zero. Every other combination returns INCOMPLETE.

Therefore, as a static inference from the function body:
- `classify_verdict("timed_out", 137)` => FAIL.
- `classify_verdict("cancelled", 143)` => FAIL.
- `classify_verdict("infrastructure_failed", 1)` => FAIL.
- `classify_verdict("rejected", 1)` => FAIL.
- `classify_verdict("running", 1)` => FAIL.
- `classify_verdict("succeeded", 2)` => FAIL.
- `classify_verdict("program_failed", None)` => FAIL.
- `classify_verdict("timed_out", None)` => INCOMPLETE.
These are reasoned outcomes from the inspected source, not executed tests.

The current test `test_timeout_cancel_rejection_and_infrastructure_failure_are_incomplete` passes `None` as the exit code for each uncertain status. It does not test any such status paired with a nonzero integer. Existing tests do cover succeeded/0 => PASS, succeeded/nonzero => FAIL, program_failed/missing => FAIL, missing exit => INCOMPLETE, nonterminal status/zero => INCOMPLETE, and boolean-as-exit-code => INCOMPLETE.

## 3. Compact canonical crosswalk

| Canonical requirement | Current source behavior | Existing test coverage | Expected result | Evidence status / minimal regression |
|---|---|---|---|---|
| LOOP-03 / CASE-01: trusted successful terminal result + exit 0 | PASS only for status `succeeded` and integer 0 | Covered | PASS | Static alignment; tests NOT RUN |
| LOOP-04 / CASE-02, CASE-03, CASE-10: confirmed program/runtime failure or actual nonzero program exit | `program_failed` or any nonzero integer yields FAIL regardless of status | Confirmed failure and succeeded/nonzero covered | FAIL when failure is confirmed | Partial alignment; provenance ambiguity remains |
| LOOP-05 / CASE-04: trusted timeout is INCOMPLETE / `timed_out` | Nonzero integer is checked first, so `timed_out` + 137 maps to FAIL | Timeout tested only with missing code | INCOMPLETE / `timed_out` | Static mismatch. Add proposed test `classify_verdict("timed_out", 137) == "INCOMPLETE"`; do not edit without authorization |
| LOOP-05 / CASE-05: cancellation requires trustworthy termination evidence; unconfirmed termination remains uncertain | Any nonzero integer forces FAIL even for `cancelled` | Cancelled tested only with missing code | INCOMPLETE when cancellation/termination state is the trusted terminal outcome and code is wrapper/termination metadata | Adjacent static risk. Proposed `cancelled/143` regression if 143 is explicitly identified as a wrapper/termination code |
| LOOP-05 / CASE-06 and CASE-11: infrastructure loss or disconnect without trustworthy child result is INCOMPLETE | Any nonzero integer forces FAIL | Infrastructure failure tested only with missing code | INCOMPLETE absent independently confirmed child failure | Adjacent static risk. Proposed `infrastructure_failed/1` case with code provenance explicitly marked as non-child |
| CASE-13: ambiguous retry must not invent result or duplicate execution | Classifier cannot establish retry identity or authoritative state; it only classifies supplied fields | No retry/idempotency test in this unit suite | Preserve UNKNOWN/INCOMPLETE absent trusted terminal evidence | Outside this pure helper; no inference of backend behavior |
| CASE-16 / LOOP-07, LOOP-09: run identity and out-of-order completion correlation | Formatter prints supplied run ID; classifier cannot validate identity/correlation | Formatting coverage exists; no concurrency/identity authority test | Preserve correct run/attempt association | Not provable by this helper or its unit tests |
| LOOP-06 / CASE-09: program-reported checks remain visible and distinct from process verdict | Formatter preserves supplied check lines/provenance; succeeded/0 may PASS even with a reported failed check | Covered | Process PASS may coexist with visible program-reported failed check | Static alignment; does not prove task correctness |
| LOOP-10 / contract release clarification: artifact-free execution may PASS; release is separate | Classifier does not require output files; formatter displays supplied metadata | No release-boundary test here | No universal artifact gate; separate authorization at release time | Static alignment for helper only; release implementation NOT reviewed/proven |

## 4. Precedence analysis: trusted lifecycle vs child exit vs wrapper code

The canonical execution contract defines `timed_out` as trusted server/provider enforcement ending a run because its deadline expired. `cancelled` likewise requires trusted execution-control confirmation. `infrastructure_failed` means the provider/coordinator prevented a trustworthy program result. By contrast, `program_failed` is a program result and `succeeded` conceptually means the program ended with exit 0 and a complete provider result.

The classifier has only two inputs and no exit-code provenance field. Consequently it cannot distinguish:
1. authoritative child-program exit code;
2. wrapper/termination utility code generated while enforcing a timeout or cancellation;
3. a code supplied by a caller despite missing or contradictory lifecycle evidence.

Canonical CASE-04 resolves the specific trusted-timeout case: do not convert the timeout to FAIL merely because the trusted enforcement path has a nonzero termination code. But this does not prove that every nonzero integer is a wrapper code, nor does it justify discarding an independently confirmed child failure. Preserve raw evidence and source provenance separately.

**Narrow static recommendation:** treat trusted terminal lifecycle state as authoritative for timeout/cancellation/infrastructure uncertainty; use a numeric code to classify program success/failure only when its provenance and lifecycle semantics establish that it is the child's authoritative exit code. The current helper signature cannot itself verify that invariant. This is a proposed contract interpretation, not an implementation instruction or frozen schema.

## 5. Cross-branch candidate status

The prior crosswalk records a candidate fix on PR #2 branch `chat-continuity-report-regressions-2026-10-26`: helper blob `e9d944a722c2fac5279952696528da72a7011af3`, test blob `39f3a3ef865ed55f333a1edc208096d99197d023`, previously reported branch head `eb8b7ea83cb0e8fe1880351276c485b761431791`. It places numeric exit-code classification under `succeeded` and keeps uncertain statuses INCOMPLETE; its test source includes timeout/137 and adjacent uncertain states.

Those hashes and PR status are historical observations recorded in the prior crosswalk, not freshly re-fetched in this pass. The candidate was reported as open/draft/unmerged, with tests NOT RUN. It is not a fix to the current research-branch helper. PR #2 and PR #3 were not touched.

## 6. Independent review and evidence limits

No direct Claude/Gemini review channel is available to this chat, so an independent response could not be requested here. This does not block the read-only analysis; independent review remains outstanding and should be narrowly scoped to: (a) CASE-04 timeout plus nonzero wrapper code; (b) child-exit vs wrapper-code provenance; and (c) whether cancelled/infrastructure states need the same precedence rule.

No tests were run. No implementation, test, canonical acceptance, runtime, provider, account, workload, GitHub Actions, merge, deployment, PR #2/#3, or host action occurred. No production caller for this pure helper is established by this review. `scripts/lifecycle_contract.py` is not claimed to exist on this ref.

## 7. Next bounded task

When a direct reviewer is available, request only the three questions in §6. Then, if separately authorized, add the narrow regression test(s) to a new isolated change or the explicitly designated branch and run the exact focused suite against recorded blob SHAs. Until then, leave source, tests, canonical acceptance, PR #2 and PR #3 unchanged. Keep RevDev acceptance IDs AWC-001–AWC-018, P8U-01–12, P0-D 1–10 distinct from PocketCode AEC-001–AEC-012. RevDev publisher/orphan/retry/recovery P0 remains release-blocking; PocketCode execution location and integration topology remain undecided.
