# PocketCode — lifecycle transition and report projection matrix

**Date:** 2026-10-29  
**Status:** Research specification only; not implementation, not run, and not a canonical acceptance amendment.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Inputs:** unchanged canonical `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` and `PRODUCT/EXECUTION_CONTRACT.md`; PR #2 report helper; PR #3 lifecycle helper; the result-envelope and semantic decision notes.

## Purpose

Give implementation and testing one small reference for translating trusted lifecycle evidence into a user-facing verdict, a richer job disposition, a report projection, and an artifact-release decision. These are separate outputs. The matrix preserves all canonical LOOP/CASE identifiers and does not select a provider or freeze a public schema.

Related documents:
- [Canonical acceptance traceability](CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md)
- [Adapter result envelope and fake-adapter protocol](ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md)
- [Semantic decisions and report projection](SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md)
- [Cross-branch conformance gap audit](CROSS_BRANCH_CONFORMANCE_GAP_AUDIT_20261029.md)

## 1. Projection vocabulary

| Layer | Allowed meaning | Must not be used as |
|---|---|---|
| Execution observation | Trusted facts such as NOT_STARTED, EXIT_ZERO, EXIT_NONZERO, TIMED_OUT, CANCELLED, LIMIT_EXCEEDED, UNKNOWN; preserve event references and any raw exit code | A verdict, a policy approval, or proof cleanup completed |
| Evidence quality | COMPLETE, MISSING, STALE, CONTRADICTORY; details identify which fact is uncertain | A replacement for the actual execution observation |
| User-facing verdict | PASS, FAIL, INCOMPLETE | A complete lifecycle history or artifact authorization |
| Job disposition | REJECTED, PASS, FAILED, TIMED_OUT, CANCELLED, LIMIT_EXCEEDED, INCOMPLETE, PROVIDER_ERROR | A trusted raw event or an implicit permission to release files |
| Artifact release | A fresh decision at the release boundary based on current digest/integrity, job binding, tenant authorization, and required cleanup gates | A cached report field or user/program-supplied boolean |
| Report version | Append-only snapshot/projection of the evidence available at that point | A new execution attempt or silent rewrite of an earlier report |

**Trust rule:** untrusted program output, a printed JSON object, a browser timeout, or a client-supplied status cannot set authoritative lifecycle facts.

## 2. Core transition and verdict matrix

| Trusted evidence at projection time | User verdict | Job disposition | Artifact release | Required report detail |
|---|---|---|---|---|
| No dispatch; trusted validation/policy rejection; no conflicting terminal evidence | INCOMPLETE | REJECTED | Deny/not applicable | Rejection reason; do not fabricate exit code |
| Trusted terminal EXIT_ZERO; policy barrier, termination, cleanup, artifact validation/association, and tenant authorization all confirmed; no contradictory evidence or disqualifying limit | PASS | PASS | Evaluate independently at release boundary; allow only if current release gates all pass | Exact lifecycle status, exit 0, required gate evidence |
| EXIT_ZERO but any mandatory PASS gate is missing, stale, false, or unknown | INCOMPLETE | INCOMPLETE | Deny | Preserve observed exit 0 and list missing gates |
| Trusted nonzero child exit; terminal evidence not contradictory | FAIL | FAILED | Deny until independent release gates pass; cleanup uncertainty keeps it denied | Preserve exact nonzero exit and cleanup state separately |
| Trusted nonzero child exit but cleanup UNKNOWN/FAILED | FAIL | FAILED | Deny | Explicit cleanup warning; do not rewrite known program failure as unknown; never imply cleanup succeeded |
| Terminal evidence contradicts itself or cannot be bound to one attempt | INCOMPLETE | INCOMPLETE | Deny/quarantine | Preserve all event references; no nominal terminal winner may produce PASS |
| Timeout request/event but termination is not confirmed | INCOMPLETE | INCOMPLETE | Deny | Distinguish request/event from confirmed stop; preserve uncertainty |
| Authoritative timeout with confirmed termination | INCOMPLETE | TIMED_OUT | Deny unless separate artifact policy explicitly permits a safe artifact and all gates pass | Exact timeout status; do not use PASS or infer successful completion |
| Cancellation requested but terminal/termination state unknown | INCOMPLETE | INCOMPLETE | Deny | Cancellation requested is not cancellation confirmed |
| Authoritative cancellation and confirmed termination | INCOMPLETE | CANCELLED | Deny unless independent release policy proves safe eligibility | Preserve cancellation status and termination evidence |
| Authoritative enforced execution limit | INCOMPLETE unless an owner-approved canonical verdict rule explicitly says otherwise | LIMIT_EXCEEDED | Deny until termination/cleanup/release gates are established | Identify actual limit event, enforcement source, bounded output and termination state |
| Runtime outcome UNKNOWN; adapter/provider failure is known | INCOMPLETE | PROVIDER_ERROR | Deny | Known cause and missing outcome evidence; no fabricated exit code |
| Runtime outcome UNKNOWN; cause also unknown | INCOMPLETE | INCOMPLETE | Deny | State exactly which observation is missing |
| Report renderer shortened stdout/stderr to fit a display budget, but trusted execution result is otherwise complete | Preserve verdict derived from execution facts | Preserve disposition derived from execution facts | Unchanged; independently evaluate release gates | Mark report-display truncation; do not manufacture LIMIT_EXCEEDED |
| Stream collector partially failed after retaining a prefix | Preserve verdict only if terminal evidence independently supports it; collection failure alone does not rewrite execution outcome | Preserve disposition plus evidence-quality/collection warning | Unchanged or deny if collection is required for release validation | Distinguish PARTIAL_FAILURE from empty output, unavailable output, and display truncation |
| Script prints PASS/FAIL/JSON or a fake exit code | Verdict derived only from trusted lifecycle evidence | Disposition derived only from trusted lifecycle evidence | Never authorize from printed output | Clearly label script-reported checks as untrusted program output |

This matrix follows the canonical user-facing definitions: PASS requires trusted successful completion and exit 0; FAIL requires confirmed program/runtime failure; timeout, cancellation, rejection, infrastructure failure, or ambiguous terminal evidence remain INCOMPLETE. The richer job disposition is retained separately.

## 3. Terminal-event reducer requirements

The source helper on PR #3 currently sorts by coordinator sequence, makes duplicate identical events idempotent, marks conflicting reuse of an event ID as contradictory, chooses the earliest sequenced terminal event as a nominal winner, and marks multiple distinct terminal events as contradictory.

Future adapter integration must preserve these invariants:

1. **Coordinator sequence outranks provider timestamps** for deterministic event ordering only when the coordinator's sequence is authoritative. Provider timestamps alone do not establish event order.
2. **Identical replay is idempotent.** The same event identity and same canonical payload does not create a new terminal outcome or a new execution attempt.
3. **Event identity conflict is not a duplicate.** Reusing one event ID with a different sequence, kind, or canonical payload marks evidence contradictory.
4. **Multiple distinct terminal events remain visible.** A nominal earliest event may be retained for diagnosis, but contradiction forces INCOMPLETE until an explicit trusted reconciliation rule resolves it. Never silently promote a late exit-zero to PASS.
5. **Attempt binding is mandatory.** Evidence for another job or attempt cannot resolve this attempt's state.
6. **No blind retry.** After a lost acknowledgement, query the original idempotency/job/attempt record. Unknown lookup means unknown outcome and no second dispatch.
7. **Late authoritative evidence creates a new report version** when it changes the projection. Do not mutate an already-issued version. A report revision is not a new run attempt.
8. **Artifact release is re-evaluated at the release boundary** using current authoritative evidence and authorization, not just the verdict stored in an older report.

The pure helper and in-memory report-history model do not prove durable storage, atomic ordering across workers, cross-process idempotency, or tamper resistance.

## 4. PR #2 legacy report projection rules

PR #2 currently returns only `PASS`, `FAIL`, or `INCOMPLETE` from `classify_verdict(execution_status, exit_code)`. It has no fields for cleanup, policy barrier revision, artifact validation, tenant authorization, contradictory events, or evidence-quality detail.

| Trusted envelope condition | Legacy projection | Preconditions / caution |
|---|---|---|
| Confirmed success and every canonical PASS gate satisfied | `execution_status=succeeded`, `exit_code=0` → PASS | Coordinator must enforce gates before calling the formatter; the formatter cannot verify them itself |
| Confirmed program failure, including known nonzero child exit | `execution_status=program_failed` → FAIL; preserve exit code if authoritative | Do not erase cleanup uncertainty; retain it in the structured envelope/report detail |
| `succeeded` plus a nonzero exit code | FAIL is the current helper's result, but the envelope must flag the status/exit contradiction for reconciliation | Do not silently claim the source status was consistent; never PASS |
| Timeout/cancel/rejection/infrastructure failure/nonterminal/unknown | INCOMPLETE | Preserve exact lifecycle status and relevant termination/uncertainty detail |
| Contradictory terminal evidence | INCOMPLETE | Do not project the reducer's nominal winner as clean success/failure |
| Runtime limit exceeded | INCOMPLETE verdict plus richer `LIMIT_EXCEEDED` disposition/event | PR #2 has no dedicated status for this; do not map it silently to `program_failed` |
| Display truncation only | Existing execution verdict remains | Add explicit display-truncation marker; never derive runtime-limit status from this alone |
| Missing exit code with `succeeded` | INCOMPLETE in current helper | Do not synthesize zero |

The trusted coordinator should pass a deliberate projection to the legacy formatter; the formatter is a renderer, not an authenticator or policy engine. Preserve the richer envelope as the source of truth.

## 5. Transition-focused conformance cases

All are **specified, NOT RUN**. Tests must assert output values, event/evidence retention, dispatch count/order, report version behavior, and artifact-release decisions—not just a formatted string.

| Test ID | Setup | Required assertion | Canonical linkage |
|---|---|---|---|
| TPM-01 | EXIT_ZERO with all required gates confirmed | PASS only; no unknown mandatory gate | LOOP-03, CASE-01 |
| TPM-02 | EXIT_ZERO with cleanup UNKNOWN | INCOMPLETE; artifact denied | CASE-12 |
| TPM-03 | EXIT_NONZERO with cleanup UNKNOWN | FAIL; preserve cleanup UNKNOWN; artifact denied | CASE-02/03/10, CASE-12 |
| TPM-04 | EXIT_NONZERO with contradictory terminal event | INCOMPLETE; preserve both events; artifact denied | CASE-02/03/06 |
| TPM-05 | `succeeded` plus nonzero exit in legacy projection | Never PASS; report inconsistency and FAIL/INCOMPLETE policy explicitly | LOOP-03/04, CASE-10 |
| TPM-06 | Timeout and exit-zero events in conflict | INCOMPLETE; no arrival-order success promotion | CASE-04 |
| TPM-07 | Same terminal event replayed identically | One logical event; stable disposition and report version | CASE-11/13 |
| TPM-08 | Same event ID reused with changed payload/sequence | Contradiction; INCOMPLETE | CASE-11/13 |
| TPM-09 | Late authoritative cleanup update | Append report version; original immutable; recompute release gate | CASE-12 |
| TPM-10 | Runtime output cap enforced | Preserve limit event and enforcement source; bounded output; not PASS | CASE-07 |
| TPM-11 | Report-only truncation | Keep execution verdict; label display truncation; no LIMIT_EXCEEDED inference | LOOP-07, CASE-12 |
| TPM-12 | Partial collector failure vs empty stream | Distinct evidence states; no invented output | LOOP-07, CASE-12 |
| TPM-13 | Lost dispatch acknowledgement and lookup UNKNOWN | Exactly one dispatch attempt; no automatic redispatch; INCOMPLETE | CASE-13 |
| TPM-14 | Evidence from another attempt arrives late | Reject it as evidence for this attempt; do not change report | CASE-16 |
| TPM-15 | Program prints forged PASS JSON | Authoritative status unchanged; output labeled untrusted | CASE-09/10, LOOP-11 |
| TPM-16 | Report says PASS but release-time tenant/digest/cleanup gate fails | Deny artifact release regardless of old report | LOOP-10/12, CASE-14/15 |

## 6. Cross-branch gaps this matrix deliberately exposes

- The lifecycle helper treats EXIT_NONZERO as FAILED before checking cleanup gates; this is consistent with the proposed verdict distinction, but the report must carry cleanup separately.
- The lifecycle helper currently treats the single `output_truncated` boolean as LIMIT_EXCEEDED. Its future call sites must distinguish enforced execution limits from report presentation truncation.
- The legacy formatter cannot validate cleanup/policy/artifact/tenant gates and has no dedicated LIMIT_EXCEEDED status. It must remain a projection behind trusted coordinator logic.
- The event reducer and in-memory report history are pure models; they do not prove persistence, atomic concurrency, provider truthfulness, actual process termination, artifact storage safety, or egress enforcement.
- CASE-13's in-memory idempotency model is not evidence of durable, cross-worker recovery after a lost acknowledgement.

## 7. Change-control and evidence status

- This is a new research-branch document only.
- Canonical contract and acceptance documents are not modified.
- PR #2 and PR #3 are not modified by this matrix.
- No code changed and no tests were run in this pass.
- No runtime/provider was selected; no workload, account, billing change, merge, or deployment occurred.
- The matrix is a reviewable test plan, not proof of product behavior or authorization to implement.
