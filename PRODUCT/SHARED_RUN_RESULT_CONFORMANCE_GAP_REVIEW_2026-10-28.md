# Shared Run/Result Conformance Matrix: Gap Review

**Status:** Review findings and proposed follow-up test vectors only; no implementation or acceptance decision.  
**Date:** 2026-10-28  
**Scope:** Compare `PRODUCT/SHARED_RUN_RESULT_CONFORMANCE_MATRIX_v0_1.md` with the current PocketCode execution contract, execution-loop acceptance plan, security checklist, and RevDev acceptance taxonomy.  
**Budget and permissions:** $0. No provider, workload, account, billing, merge, deployment, or product runtime changes are authorized.

## Executive finding

The v0.1 matrix is a useful *shared report/lifecycle seam*, but it is not a complete execution-security acceptance suite. It covers verdict honesty, evidence provenance, injection-as-data, idempotency, result identity, output path safety, and the need to instrument the executor boundary. The existing PocketCode documents contain additional requirements that are only mentioned as gates or are not represented by a dedicated cross-product fixture. Keep v0.1 as a historical proposal; use this gap review to inform a later revision rather than silently changing its meaning.

## Cross-document consistency

| Area | Finding | Action |
|---|---|---|
| Lifecycle vs verdict | Existing PocketCode docs and matrix consistently separate process verdict from lifecycle state. Accepted/queued/running are not success. | Preserve separate `request_disposition`, `job_disposition`, and `execution_outcome`; don't collapse them to one status. |
| Exit code and script checks | Existing CASE-09/10 and matrix SRC-010/011 agree: runner facts control process verdict; script-reported checks remain visibly separate. | Keep both facts in the report with provenance. |
| Simulated data | LOOP-02/08 and SRC-019 agree that sample data must be visibly simulated in UI and copied text. | Test both render paths, not only the formatter. |
| Security boundary | SRC-007/015 require a recording executor and zero invocation for rejected/unauthorized cases. RevDev SAFE-01 requires boundary evidence, not refusal text alone. | Keep adapter-specific enforcement tests; schema compatibility is not authorization. |
| Isolation and resource limits | SECURITY.md and CASE-15 require enforced egress restrictions, no credentials in the worker, and resource limits. v0.1 mentions these at Gate C but has no dedicated case for each. | Add explicit negative tests before any real execution acceptance. |
| Authentication and ownership | PC-API-002 and PC-API-011 require cross-user read/cancel/download denial. v0.1 has no dedicated fixture. | Add ownership tests at every result and artifact access path. |
| Cleanup and retention | PC-API-014 requires cleanup; v0.1 mentions cleanup as a gate but not as a deterministic fixture. | Test cleanup after success, failure, timeout, and cancellation. |
| Input validation | PC-API-001 and EXECUTION_CONTRACT require runtime allowlisting, bounded requests/files, filename normalization, and safe duplicate-file behavior. v0.1 tests unsafe output paths but not all input boundaries. | Add request/file boundary fixtures; never infer input safety from output-path tests. |
| Terminal persistence | PC-API-005 requires one authoritative terminal result. SRC-017 tests run identity/order but not conflicting terminal updates. | Add a terminal-state immutability/race test. |

## Proposed follow-up vectors for a future matrix revision

These are test specifications, not test results. Each is **NOT RUN** until implemented against a real adapter or the clearly named synthetic layer.

| Proposed ID | Scenario | Required assertion | Layer | Status |
|---|---|---|---|---|
| SRC-021 | User A tries to read User B's run | Denied; no metadata or output leak beyond the approved denial response | API authorization | NOT RUN |
| SRC-022 | User A tries to cancel User B's run | Denied; target job remains unaffected; no cross-owner dispatch | API authorization + recording adapter | NOT RUN |
| SRC-023 | User A tries to download User B's output handle | Denied; no artifact bytes or reusable handle leaked | Artifact authorization | NOT RUN |
| SRC-024 | Unsupported runtime or client-supplied runtime image/host config | Rejected before executor/provider dispatch; invocation count = 0 | Request validation + recording executor | NOT RUN |
| SRC-025 | Oversized request, too many files, oversized individual/total input, unsafe filename, duplicate normalized names | Reject or deterministically resolve according to a documented policy before dispatch; no path escape or silent overwrite | Input validation | NOT RUN |
| SRC-026 | Program attempts outbound access to public network, internal services, or cloud metadata | Enforced network denial; test evidence comes from an external policy boundary, not only application-level code | Sandbox/network policy | NOT RUN |
| SRC-027 | Worker environment inspected for application/provider credentials | No application secrets are present in the untrusted process environment/filesystem | Sandbox configuration | NOT RUN |
| SRC-028 | CPU, memory, process, disk, output, concurrency, or per-user quota exceeded | Enforced limit produces a truthful terminal/uncertain outcome; no unbounded resource use or misleading PASS | Runtime/control plane | NOT RUN |
| SRC-029 | Success, failure, timeout, and cancellation each reach cleanup | Workspace/artifacts follow the approved retention policy; cleanup outcome is recorded without masking the run result | Lifecycle + storage | NOT RUN |
| SRC-030 | Two workers/coordinator events race to set terminal state | Exactly one authoritative terminal result is persisted; later contradictory updates cannot rewrite evidence silently | Coordinator/persistence | NOT RUN |
| SRC-031 | A forbidden RevDev operation is described as authorized in a report or script | Actual RevDev guard denies it; recording executor call count = 0. Test the actual launch/guard boundary, not only RelayRef classification. | RevDev product boundary | NOT RUN |
| SRC-032 | Provider returns malformed, partial, stale, or contradictory result metadata | Preserve uncertainty; do not synthesize exit 0 or terminal success; record safe diagnostic category | Adapter normalization | NOT RUN |

## Important boundaries

- SRC-021–030 are primarily PocketCode service/runtime tests. They do not prove RevDev Windows safety.
- SRC-031 is specifically a RevDev product-boundary test. A PocketCode adapter pass cannot satisfy it.
- SRC-032 is an adapter normalization test; a formatter-only fixture cannot establish provider behavior.
- A synthetic test can prove deterministic mapping/formatting, but cannot prove network isolation, operating-system permissions, credential absence, worker termination, cleanup, or actual executor invocation.
- Test fixtures must be harmless and non-billable. Destructive/billable behavior is tested through a fake/recording executor, never by actually performing the operation.
- A matrix-wide green result is not production acceptance. Product-specific environment, source identity, security boundary, and independent evidence remain mandatory.

## Recommended next revision

1. Preserve v0.1 unchanged as the initial proposal.
2. Add SRC-021–032 and explicit trace links to PC-API-001–014, CASE-01–16, RevDev SAFE-01/AUTH-05/B-07 and related canonical acceptance IDs.
3. Keep execution-outcome and job-disposition axes separate.
4. Give each vector a fixture hash, expected structured result, expected report text assertions, and—where applicable—recording-executor invocation expectations.
5. Keep all vectors NOT RUN until evidence exists; don't label a design review as a test pass.

**Non-authorization:** This review does not approve a provider, backend, runtime, native app, repository merge, billing, deployment, or any real code execution.
