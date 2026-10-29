# PocketCode — semantic decisions and report projection

**Date:** 2026-10-29  
**Status:** Proposed design clarification; not implemented, not run, and not a canonical-contract amendment.  
**Sources inspected:** canonical execution-loop acceptance on `main`; PR #2 report helper/test source; PR #3 lifecycle helper/test source; the provider-neutral result-envelope proposal.  
**Purpose:** Resolve two ambiguities that would otherwise cause the integration to lose evidence or produce misleading reports.

## Executive decisions proposed

1. **A confirmed program failure stays a failure when cleanup is uncertain.** Preserve the nonzero exit/program-failure fact as the user-facing FAIL verdict, but independently show cleanup as UNKNOWN/FAILED and keep artifacts blocked. Cleanup uncertainty does not rewrite a known program result into a claim that the program outcome itself is unknown.
2. **Contradictory or untrusted terminal evidence overrides a nominal result.** If the trusted coordinator cannot establish which terminal outcome is authoritative, the user-facing verdict is INCOMPLETE, regardless of an apparent zero/nonzero exit.
3. **Execution output-limit enforcement and report-display truncation are separate facts.** Hitting an enforced runtime output cap may be a LIMIT_EXCEEDED event. Truncating text only to fit the report-size budget is a presentation condition and must not, by itself, reclassify the execution as LIMIT_EXCEEDED.
4. **Keep execution outcome, job disposition, user-facing verdict, cleanup state, and artifact-release decision separate.** The legacy report formatter may display a projection, but it must not be the only place these distinctions exist.

These are proposed semantic decisions for owner review, not implementation authorization.

## Evidence and rationale

### Canonical verdict contract

The canonical acceptance document defines:
- PASS: trusted terminal result confirms completion and exit code zero.
- FAIL: a nonzero exit code or confirmed program/runtime failure.
- INCOMPLETE: no confirmed success or confirmed program failure, including timeout, cancellation, rejection, infrastructure failure, or missing/ambiguous terminal evidence.
- The exact lifecycle status must also be preserved, and missing evidence must never be silently converted to PASS.
- Script-reported checks remain program output unless PocketCode independently validates them.

This means cleanup uncertainty is important, but it does not erase an already-authoritative program failure. It remains a separate safety/evidence fact.

### Existing PR #3 helper behavior

The reviewed lifecycle helper currently:
- returns INCOMPLETE when terminal evidence is contradictory;
- returns FAILED for EXIT_NONZERO before checking cleanup/policy/artifact/tenant gates;
- returns INCOMPLETE for EXIT_ZERO when cleanup is not confirmed or any required gate is not exactly true;
- returns LIMIT_EXCEEDED if `execution_outcome == LIMIT_EXCEEDED`, `limit_violated`, or `output_truncated` is true, before timeout/cancellation handling.

The first three behaviors align with the proposed decisions above. The fourth is potentially ambiguous because a single boolean named `output_truncated` does not say whether the runtime enforced an execution limit or the report renderer merely shortened displayed text. Do not change the existing helper without checking its intended call-site semantics; instead make that distinction explicit at the envelope/adapter boundary.

### Existing PR #2 helper behavior

The reviewed report helper:
- returns FAIL for lifecycle status `program_failed`;
- returns PASS/FAIL for `succeeded` plus a valid integer exit code;
- returns INCOMPLETE for timeout, cancellation, rejection, infrastructure failure, nonterminal states, or missing exit code;
- deliberately treats script-reported checks as output, not independently verified service facts.

The helper does not accept cleanup, policy revision, artifact validity, tenant authorization, or contradictory-evidence fields. It must therefore only receive a legacy `succeeded` projection after the trusted coordinator has independently established every gate required for PASS. This is a caller-side precondition, not something the current formatter can verify by itself.

## Decision table for the future trusted projection

| Trusted facts | Execution outcome | Cleanup / artifact consequence | User-facing verdict | Job disposition / report detail |
|---|---|---|---|---|
| Authoritative child exit zero; every mandatory PASS gate confirmed; no contradictory evidence or disqualifying limit | EXIT_ZERO | Cleanup confirmed; artifact may be considered for release only after its independent release checks | PASS | PASS |
| Authoritative child exit zero; any mandatory gate missing, stale, or unknown | EXIT_ZERO | Do not release artifacts while relevant gates are unresolved | INCOMPLETE | INCOMPLETE with explicit missing-gate reasons |
| Authoritative child exit nonzero; no contradictory terminal evidence | EXIT_NONZERO | If cleanup is unknown/failed, state that separately and deny artifact release | FAIL | FAILED plus independent cleanup state/reason |
| Timeout/cancel is the only terminal explanation, but actual termination is unconfirmed | TIMED_OUT / CANCELLED | Do not claim the worker stopped; block artifact release until gates pass | INCOMPLETE | INCOMPLETE; request acknowledgement is not termination proof |
| Timeout/cancel is authoritatively terminal and termination is confirmed | TIMED_OUT / CANCELLED | Preserve cleanup state independently | INCOMPLETE | Preserve exact lifecycle status; canonical user-facing verdict remains INCOMPLETE |
| Rejection before execution; no conflicting terminal evidence | NOT_STARTED | No program exit code should be fabricated | INCOMPLETE | REJECTED with reason |
| Trusted terminal events conflict, or a supposedly terminal event cannot be bound to the correct attempt | UNKNOWN / contradictory | Quarantine associated artifacts; do not select success based on arrival order alone | INCOMPLETE | INCOMPLETE with contradiction details |
| Runtime enforced an output/resource cap and authoritative evidence confirms the limit event | Preserve the actual observed outcome and limit event separately | Termination/cleanup still need their own evidence | INCOMPLETE unless the owner later explicitly defines a different canonical verdict | LIMIT_EXCEEDED as lifecycle/disposition detail |
| Report renderer shortened output only to satisfy the report-size cap | Preserve the actual execution outcome | No runtime limit can be inferred from display truncation alone | Verdict remains derived from execution evidence | Add report-display truncation marker; do not manufacture LIMIT_EXCEEDED |

**Important:** the table intentionally does not equate a job disposition with the user-facing verdict. In particular, a confirmed nonzero program exit can produce FAIL while cleanup remains UNKNOWN; the report must prominently retain the cleanup uncertainty, and the artifact gate must remain closed. A contradictory terminal record is different: it prevents claiming a confirmed program result.

## Output truncation: required semantic split

Use distinct typed facts in the future envelope, for example:
- `execution_limit_event`: NONE | OUTPUT_CAP | TIME_LIMIT | MEMORY_LIMIT | OTHER_LIMIT | UNKNOWN.
- `stream_collection_state`: COMPLETE | UNAVAILABLE | PARTIAL_FAILURE | TRUNCATED_BY_EXECUTION_LIMIT.
- `report_rendering_truncated`: boolean plus the report cap/reason and omitted-content count if reliably known.

These are semantic examples, not a frozen schema. If the selected runner has no separate wrapper/collector layer, keep the representation simpler. The invariant is that presentation truncation cannot be used as evidence that user code exceeded an enforced execution limit.

## Terminal evidence and report versioning

The current lifecycle reducer keeps the earliest coordinator-sequenced terminal event as a nominal winner but also marks multiple distinct terminal events as contradictory. The derived disposition must respect the contradiction marker and remain INCOMPLETE; the nominal winner is useful for debugging but is not a clean user-facing result.

When later authoritative evidence resolves a previously unknown cleanup or terminal state:
- append a new report version instead of mutating an issued report;
- retain the original outcome and evidence reference;
- state what new evidence changed the projection;
- do not silently change a previously copied report;
- recompute artifact release at the release boundary from current trusted evidence and authorization.

The in-memory `ReportHistory` helper models append-only versions but does not prove durable storage, atomic version assignment, or tamper resistance.

## Required regression cases to add after implementation authorization

| ID | Setup | Required assertion |
|---|---|---|
| SEM-01 | EXIT_NONZERO with cleanup UNKNOWN | User-facing verdict FAIL; cleanup explicitly UNKNOWN; no artifact release; no PASS |
| SEM-02 | EXIT_NONZERO with contradictory terminal events | User-facing verdict INCOMPLETE; preserve both terminal observations; no artifact release |
| SEM-03 | EXIT_ZERO with cleanup UNKNOWN | User-facing verdict INCOMPLETE; no artifact release |
| SEM-04 | Confirmed EXIT_ZERO with all required gates and no contradiction | PASS is possible only from trusted coordinator projection |
| SEM-05 | Runtime output cap is enforced | Preserve limit event distinctly from report renderer truncation |
| SEM-06 | Report renderer truncates an otherwise valid successful report | Preserve execution verdict; mark report display truncation; do not infer LIMIT_EXCEEDED |
| SEM-07 | Timeout plus a later contradictory exit event | Preserve both events; INCOMPLETE until the selected trusted reconciliation rule resolves the contradiction |
| SEM-08 | Cleanup evidence changes from UNKNOWN to CONFIRMED | Append a new report version; original version remains unchanged; recompute release eligibility independently |

These are acceptance specifications, not passing tests.

## Change-control and evidence status

- This document is on the isolated research branch only.
- Canonical `PRODUCT/EXECUTION_CONTRACT.md` and `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` are unchanged.
- PR #2 and PR #3 remain separate draft branches and are not modified.
- No code was changed, no tests were run, and no runtime/provider behavior was verified.
- The proposed semantics require owner review before implementation; this note does not authorize a schema freeze, provider selection, workload, spend, merge, or deployment.
