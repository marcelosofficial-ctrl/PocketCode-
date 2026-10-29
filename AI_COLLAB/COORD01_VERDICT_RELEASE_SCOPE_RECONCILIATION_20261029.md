# PocketCode COORD-01 Verdict/Release Scope Reconciliation — 2026-10-29

**Status:** Read-only contradiction audit. SPECIFIED ONLY / NOT RUN.
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`
**Branch HEAD at review:** `3dcfa14f9c134dfe9486eeeb2c309bd48f95df07`
**No implementation, tests, canonical acceptance, PR, provider, runtime, store, or deployment changes.**

## 1. Exact source artifacts

| Path | Blob SHA | Authority/use |
|---|---|---|
| `AI_COLLAB/COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md` | `214bb4aaffe002f95323be3dcab4c6cdd924f28c` | Proposed COORD-01..12 coordinator tests; lines 35–43 define COORD-01 and lines 109–119 define COORD-09/10 |
| `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` | `c6714c27db52b2962fe8d1c7e6a16829d46a8338` | Canonical LOOP/CASE semantics, including CASE-04, CASE-07, CASE-09, CASE-14 |
| `PRODUCT/EXECUTION_CONTRACT.md` | `128a00a9b2a335514814cab76fb5781fe8f9f858` | Proposed contract explicitly separates execution verdict from artifact release |
| `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md` | `e67b2659cf2d71ef77d8e4619c91143e71062470` | D-01/D-03 working defaults; decisions still owner-open before schema/gate freeze |
| `AI_COLLAB/SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md` | `a237e882128865ce6a47651a1f9c6da6901f4994` | Proposed separate projections for outcome, disposition, verdict, cleanup and release |
| `AI_COLLAB/OUTPUT_STATE_AND_VERDICT_RELEASE_CROSSWALK_20261029.md` | `0f5fb8f772941c25ae7db590c9b5b86012c5ad99` | Prior output-state/release note; its claim that COORD-01 text was not located is superseded by this recheck |

The branch ref was fetched from GitHub and resolves to the HEAD SHA above. This establishes the reviewed research-branch tip at the time of this pass, not implementation or runtime evidence.

## 2. Exact COORD-01 meaning

COORD-01 is titled **“PASS is a projection of all required trusted gates.”** Its setup includes trusted completion with exit zero, matching policy revision, confirmed termination, case-required stream collection, verified artifact digest/association, confirmed cleanup, and current tenant authorization. It states that not every stream is universally mandatory. Its negative variants say removing/marking UNKNOWN each required gate must prevent both PASS and artifact release.

The same test plan's **COORD-09** explicitly says that when a run previously passed but release-time authorization or stored-artifact validation fails, release is denied and “prior execution PASS remains historical and is not rewritten to mean that release succeeded.”

The canonical execution contract also says a task without output files may PASS, and that artifact release is a separate, current decision. The owner register's D-03 working default says there is no universal artifact-presence gate and only evidence explicitly required by the acceptance case gates PASS.

## 3. Crosswalk finding: COORD-01 currently bundles two gate classes

**Finding: wording ambiguity / likely internal test-plan contradiction.** COORD-01's setup mixes:
1. **Execution-verdict evidence:** trusted terminal outcome, child exit evidence, and any output/termination facts required by the particular acceptance case.
2. **Release authorization/integrity evidence:** current tenant authorization, artifact digest and artifact-to-job/attempt association, which apply when an artifact is to be released.

COORD-01's blanket negative assertion (“every variant must prevent PASS and artifact release”) is too broad if its “required gate” variants include release-only facts. A missing/stale release authorization or failed artifact digest must deny release, but must not retroactively turn an already established execution PASS into INCOMPLETE/FAIL. That is the explicit COORD-09 rule and canonical contract boundary.

The setup also includes “cleanup is confirmed” as a PASS gate. Cleanup may be a required safety gate for dispatch/continued operation or artifact release, but canonical LOOP/CASE does not establish that every execution verdict universally depends on cleanup confirmation. The current plan should avoid promoting a proposed reducer's cleanup predicate into a universal product-verdict rule without owner-approved acceptance mapping. A confirmed nonzero program exit should remain FAIL even if cleanup is unknown; cleanup uncertainty is separately reported and release stays closed (COORD-02).

## 4. Suggested correction for future owner-approved test-plan editing

Do not edit the plan in this read-only pass. When separately authorized, rewrite COORD-01's negative variants by gate class:

- **Execution-required gate missing/UNKNOWN:** prevent PASS for that acceptance case; preserve raw execution facts; use INCOMPLETE when success/failure cannot be confirmed.
- **Release-only gate missing/failed/UNKNOWN:** deny artifact release; preserve the historical execution verdict unchanged.
- **Case-required output collection missing/incomplete:** block PASS only where that acceptance case requires the stream/collection state; preserve child exit/lifecycle evidence and explicit collection state.
- **Optional diagnostics unavailable or capped:** do not impose a universal verdict failure; retain truthful collection state and any truncation marker.
- **Runtime limit versus collection cap versus display truncation:** preserve separate evidence. Current CASE-04/D-01 working default remains trusted timeout => INCOMPLETE / `timed_out`; D-01 remains OPEN only for a future canonical change, not permission to silently alter CASE-04.
- **Confirmed nonzero child exit with cleanup UNKNOWN:** verdict remains FAIL; cleanup uncertainty is separate and artifact release remains denied.

For fake-adapter assertions, test the projection tuple rather than a single combined PASS/release boolean: `raw_execution_outcome`, `job_disposition`, `user_facing_verdict`, `collection_state`, `cleanup_state`, and `artifact_release_decision`. Keep the actual immutable report/evidence snapshot tied to the exact job and attempt.

## 5. Output-state definitions remain provisional, not a frozen schema

COORD-10 and the coordinator plan distinguish:
- `COMPLETE`: stream captured through its defined terminal boundary;
- `PARTIAL`: some bytes captured, but required stream incomplete;
- `UNAVAILABLE`: no reliable collection evidence;
- `EMPTY`: complete capture of zero bytes;
- `RUNTIME_LIMIT`: runtime or collector cap event, with termination as a separate fact;
- `DISPLAY_TRUNCATED`: report presentation shortened after collection.

D-03 still requires owner review before schema/gate freeze. Requiredness and accepted partial capture must be defined per acceptance case and actual adapter capability. No provider/runtime has been selected or tested, so these are proposed semantics only.

## 6. Related verdict precedence retained

The report helper blob `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817` still returns FAIL for any nonzero integer exit code before checking `timed_out`. Existing tests blob `85109f056009d65a274e9306deb39b68e1fefbd2` does not test `timed_out` plus a nonzero code. Canonical CASE-04 and D-01 working default require trusted timeout to remain INCOMPLETE / `timed_out`. No tests were run, and no code/test edit is made here.

## 7. Evidence limits and next action

- Static document/source review only. No test, coordinator, provider, runtime, persistence, release boundary, or device was run.
- No source, tests, canonical acceptance, PR #2, or PR #3 changed.
- No provider/account/billing/workload/Actions/merge/deployment/host action.
- RevDev AWC-001–AWC-018, P8U-01–12, P0-D 1–10 remain distinct from PocketCode AEC-001–AEC-012.
- RevDev publisher/orphan/retry/recovery P0 remains release-blocking. PocketCode execution location and integration topology remain undecided and approval-gated.

**Next bounded task:** after separate authorization for documentation edits, reconcile COORD-01's wording so execution-required gates and release-only gates are tested independently, then ask for owner resolution of D-01/D-03 before freezing any verdict or collection schema. Until then, keep this as a documented finding and do not implement.

## 8. Additional precedence gap: timeout status plus nonzero exit code

A further static distinction is necessary before a regression can be specified safely. The current helper receives only `execution_status` and `exit_code`; it has no field identifying whether a nonzero code is an authoritative child-process exit or a wrapper/signal code associated with enforced timeout termination.

| Evidence supplied to projection | Safe interpretation under current canonical CASE-04 | Required handling |
|---|---|---|
| Trusted terminal status `timed_out`; numeric nonzero code is only the runner/wrapper's timeout or signal code | The code does not independently establish a program failure | `INCOMPLETE / timed_out`; preserve the code and its provenance without treating it as a child exit |
| Trusted `timed_out` plus independently trusted child `EXIT_NONZERO`, with no authoritative reconciliation explaining the apparent conflict | Two terminal claims conflict or their relationship is underspecified | `INCOMPLETE` until the trusted boundary resolves the conflict; retain both observations |
| Independently trusted child `EXIT_NONZERO` and no competing/contradictory timeout terminal claim | Confirmed program failure | `FAIL`, even if cleanup is separately UNKNOWN |
| Collector-only output cap or renderer truncation, with trusted child `EXIT_ZERO` | Neither fact alone proves timeout termination | Preserve the child result; apply only the applicable case-specific collection requirement |

This means the existing helper's early rule “any valid nonzero exit code means FAIL” is too broad for an input where `exit_code` may be a runner-level termination code. It also means simply reversing precedence so every `timed_out` status wins would be unsafe: that could erase an independently confirmed child failure. The projection boundary must preserve the exit-code source/type and contradiction state, or normalize the input to an authoritative terminal outcome before calling the legacy helper.

**Narrow regression candidates, specified only and NOT RUN:**

1. `timed_out` + wrapper/signal code 137, with no trusted child exit: INCOMPLETE / `timed_out`.
2. `timed_out` + trusted child exit 2, where both are presented as terminal observations and no reconciliation exists: INCOMPLETE with both observations retained.
3. Trusted child `EXIT_NONZERO` without a competing timeout terminal claim, cleanup UNKNOWN: FAIL; cleanup UNKNOWN; release denied.
4. `succeeded` + trusted child exit 0 + collector-only cap: apply D-03 and the case-specific required-stream rule; do not infer timeout.
5. `succeeded` + trusted child exit 0 + display-only truncation: preserve execution verdict.

These cases refine the earlier finding in section 6; they do not resolve D-01/D-03, change canonical acceptance, freeze an event schema, or authorize implementation. Owner review is still required before verdict-test expectations are frozen.

