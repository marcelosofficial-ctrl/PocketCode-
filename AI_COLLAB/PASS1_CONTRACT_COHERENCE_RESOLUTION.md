# Contract Coherence Resolution Note — Lifecycle, Evidence, and Verdict

**Status:** Proposed resolution for review; not an accepted product/API decision.
**Prepared:** 2026-10-27
**Branch:** `pocketcode-pass0-audit-2026-10-26`
**Budget / execution gate:** $0; offline review only. No provider, live workload, test run, merge, or deployment.

## Executive finding

The current `DRAFT_EXECUTION_CONTRACT.md` has a real lifecycle ambiguity: its diagram allows `SUCCEEDED` before `CLEANUP_PENDING`, but the prose defines `SUCCEEDED` as requiring cleanup success. Those meanings cannot both be true. A formatter could consequently emit PASS before cleanup is complete, or a cleanup failure could overwrite the observed execution result.

This note recommends separating **execution outcome** from **overall job disposition** and treating the current lifecycle diagram as illustrative, not implementable as-is. It does not silently change the public contract or freeze a status vocabulary.

## Proposed semantic model

Keep two independent records:

1. **Execution outcome** — what authoritative runner evidence says happened to the user task: `NOT_STARTED`, `EXITED_ZERO`, `EXITED_NONZERO`, `TIMED_OUT`, `CANCEL_REQUESTED`, `TERMINATION_CONFIRMED`, `TERMINATION_UNCONFIRMED`, or `PROVIDER_UNKNOWN`. This is illustrative vocabulary, not a final enum.
2. **Job disposition** — whether the service can safely report a completed result: `REJECTED`, `IN_PROGRESS`, `PASS`, `FAIL`, `INCOMPLETE`, `CANCELLED`, `LIMIT_EXCEEDED`, `PROVIDER_ERROR`, or `CLEANUP_FAILED`. This is also illustrative vocabulary.

Do not force a task's process outcome and the service's cleanup/security outcome into one mutable state field. Preserve timestamped events and evidence; corrections append facts rather than rewriting history.

### PASS gate

The report may say **PASS** only when every required condition is affirmatively evidenced:

- request and tenant authorization were validated;
- all mandatory controls were confirmed as actually enforced for this job;
- runner termination is authoritative and exit code is zero;
- no timeout, cancellation, output cap, or other policy violation occurred;
- output/artifact manifest is complete, bounded, validated, and tenant-scoped;
- cleanup completion is confirmed;
- evidence is internally consistent and belongs to this job.

Missing, stale, contradictory, or merely requested (not confirmed) evidence must not satisfy a gate. Unknown cost must remain unknown, never be rendered as $0. A successful process with failed or unconfirmed cleanup is **not overall PASS**, even if the execution outcome remains recorded as exit code zero.

## Race and retry rules

- Timeout and cancellation are requests until termination evidence confirms the process is stopped. A client deadline/disconnect alone is not proof of termination.
- A late provider event must not silently turn an already reported timeout/cancel into PASS. Prefer a monotonic coordinator-ingress sequence assigned to accepted events and a single atomic terminal decision per attempt; preserve competing/late events append-only. Provider timestamps alone do not establish authoritative ordering. If replayable order cannot be established, record ambiguity as incomplete/provider error.
- Cleanup must be idempotent. A retry may add evidence of eventual cleanup but must not erase the initial cleanup failure or alter the historical execution result.
- A repeated client request ID must not permit cross-tenant result reuse. Define idempotency scope and conflict behavior before implementation.
- Terminal *facts* are append-only; a derived disposition may move from incomplete to resolved only through an explicit reconciliation event with supporting evidence. Never rewrite prior reports without versioning.

## Minimum offline acceptance tests (proposed, not run)

| ID | Synthetic scenario | Required assertion |
|---|---|---|
| LC-01 | Exit code 0, cleanup pending | No PASS while cleanup is pending |
| LC-02 | Exit code 0, cleanup fails | Execution outcome remains exit-zero; disposition is not PASS and exposes cleanup failure |
| LC-03 | Timeout requested, termination unknown | No claim that execution stopped; no PASS |
| LC-04 | Cancel requested, late success event arrives | No silent PASS; conflicting chronology is reconciled or marked incomplete |
| LC-05 | Duplicate/out-of-order provider events | Idempotent processing; no regression from a safer terminal disposition to PASS |
| LC-06 | Retry cleanup eventually succeeds | Append cleanup recovery evidence; preserve prior failure event; derive final disposition only under explicit rule |
| LC-07 | Exit code 0 but policy confirmation missing/stale | No PASS |
| LC-08 | Exit code 0 but output/artifact manifest missing or contradictory | No PASS |
| LC-09 | Client supplies status=PASS or fabricated exit code | Client fields cannot influence authoritative outcome |
| LC-10 | Provider cost observation absent | Report cost as unknown, not zero |
| LC-11 | Same idempotency key from two tenants | No cross-tenant collision or data disclosure |
| LC-12 | Cleanup success event belongs to another job | Reject evidence association; no PASS |

These tests can validate pure orchestration/report logic with a fake adapter and synthetic records. They do not prove provider isolation, termination, cleanup, egress enforcement, tenant isolation, or billing.

## Cross-document disposition

- `DRAFT_EXECUTION_CONTRACT.md`: lifecycle wording is ambiguous; do not implement its state diagram literally until this decision is reviewed.
- `CONTRACT_COHERENCE_AUDIT.md`: retain as the finding inventory; this note proposes one resolution and adds concrete race/retry cases.
- `OFFLINE_ACCEPTANCE_TEST_MATRIX.md`: add/trace LC-01 through LC-12 when the matrix is next edited; do not describe these proposed cases as executed.
- `DECISION_REGISTER.md`: D6 remains provisional. Owner review is needed before choosing canonical enum names, retry/reconciliation rules, or external API behavior.
- `MASTER_RESEARCH_IMPLEMENTATION_PLAN.md`: implementation remains blocked pending coherent contract semantics and the other P0 gates.

## Explicitly unresolved

1. Should result artifacts be withheld until cleanup confirmation, or may they be exposed as provisional with a prominent non-PASS warning?
2. What provider evidence is authoritative for event ordering and process-tree termination?
3. What is the exact policy for a cleanup retry that succeeds after an initial cleanup failure?
4. Which states are internal event facts versus externally visible API statuses?
5. What retention and deletion evidence is required before a result can be reported complete?

## Decision boundary

The detailed six-item recommendation and approval checklist is consolidated in [PASS1_OWNER_DECISION_PACKET_20261027.md](PASS1_OWNER_DECISION_PACKET_20261027.md). All items remain pending; this resolution note does not itself approve them.

Recommended next step is owner review of the packet, then a coordinated contract/matrix update. Implement offline schema/state-machine/report tests only after the expected outcomes are agreed and implementation is explicitly authorized. No production implementation, provider SDK, account, live execution, paid service, security test, merge, or deployment is authorized by this note.
