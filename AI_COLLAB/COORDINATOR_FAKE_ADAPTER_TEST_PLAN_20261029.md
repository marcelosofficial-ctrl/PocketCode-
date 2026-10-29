# PocketCode — coordinator/fake-adapter test plan

**Date:** 2026-10-29  
**Status:** Test design only. No coordinator or provider adapter is implemented/validated by this document. No tests run.  
**Branch:** pocketcode-ai-workflow-director-research-2026-10-28  
**Companion:** AI_COLLAB/FUNCTION_LEVEL_CONFORMANCE_AUDIT_20261029.md

## Purpose

Convert the current canonical acceptance contract and helper-level audit into a minimal, high-signal test plan for a future coordinator. These tests are deliberately not assigned to the report formatter or pure lifecycle helpers when they require authoritative state, ordering, durable storage, or an actual execution boundary.

This document does not amend canonical acceptance, select a provider/runtime, freeze an API schema, or authorize implementation.

## 1. Source-grounded constraints

- PR #2's classify_verdict("succeeded", 0) returns PASS; format_report() explicitly states that it does not verify the trustworthiness of its input. Source: [report_contract.py](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/chat-continuity-report-regressions-2026-10-26/scripts/report_contract.py).
- PR #3's derive_disposition() requires confirmed cleanup and explicit boolean-identity gates before EXIT_ZERO can become PASS; contradictory evidence takes precedence and yields INCOMPLETE. Source: [lifecycle_contract.py](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-pass0-audit-2026-10-26/scripts/lifecycle_contract.py).
- reduce_terminal_events() deterministically reduces supplied event records but does not receive an expected attempt ID; caller-level event binding remains necessary.
- reserve_idempotency(), reserve_idempotency_batch(), and ReportHistory explicitly model single-process/in-memory behavior. They do not establish atomic persistent storage.
- Canonical acceptance source is unchanged: PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md, blob c6714c27db52b2962fe8d1c7e6a16829d46a8338.
- Canonical criteria remain LOOP-01..14 and CASE-01..16. See AI_COLLAB/CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md.

## 2. Test harness shape

When a coordinator exists, use a deterministic fake adapter and observable fake stores. Each test should record an ordered event log, not only a final return value.

Recommended log event fields (illustrative test harness fields, not a frozen public schema): monotonic coordinator sequence; job ID and attempt ID; operation (prepare, policy_read, dispatch, lookup, cancel, terminate, collect, store, release); request fingerprint and policy revision where applicable; adapter return/timeout/connection failure; evidence source and trust classification.

Assertions should cover final execution outcome; job disposition; user-facing report verdict; artifact-release decision; ordered adapter calls and exact dispatch count; preservation of unresolved/contradictory evidence; and no cross-job or cross-attempt evidence leakage.

A fake can validate coordinator logic against a scripted adapter. It cannot prove provider behavior, actual isolation, server-enforced limits, durable transaction semantics, or a real download boundary.

## 3. Minimal high-signal coordinator tests

### COORD-01 — PASS is a projection of all required trusted gates

**Setup:** Adapter reports valid completion for attempt A with exit 0; policy revision matches; termination is confirmed; required output collection is complete; artifact digest and association are verified; cleanup is confirmed; tenant authorization is current.

**Assertions:** disposition PASS; report verdict PASS; release allowed only after release-time revalidation; event log contains evidence for every required gate; report contains the same job/attempt identity.

**Negative variants:** independently remove or mark UNKNOWN each required gate. Every variant must prevent PASS and artifact release. Preserve the actual execution observation separately from the derived disposition.

**Anchors:** LOOP-03/07/10; CASE-01/12/14.

### COORD-02 — program failure remains FAIL when cleanup is unknown

**Setup:** Trusted program terminal event says EXIT_NONZERO; cleanup is UNKNOWN.

**Assertions:** execution outcome remains EXIT_NONZERO; disposition remains FAILED under the documented semantic decision; report is FAIL rather than PASS; cleanup is shown UNKNOWN; artifacts remain blocked.

This prevents cleanup uncertainty from erasing a confirmed program failure while still failing closed for artifact release.

**Anchors:** LOOP-03/04/05/10; CASE-02/03/12.

### COORD-03 — infrastructure failure does not fabricate a child exit

**Setup:** Worker/provider reports failure before a trusted child exit event exists.

**Assertions:** no synthetic exit code is inserted; execution outcome remains UNKNOWN/appropriate infrastructure evidence; disposition is PROVIDER_ERROR or INCOMPLETE according to the resolved projection policy; report cannot PASS; artifact release is denied.

**Decision needed:** choose one canonical user-facing projection for provider failure without pretending an exit code exists. Preserve raw provider failure and derived disposition separately.

**Anchors:** LOOP-04/05/07; CASE-06.

### COORD-04 — contradictory terminal events force INCOMPLETE

**Setup:** Same attempt produces timeout followed by a distinct exit-zero terminal event, or vice versa, with coordinator sequence numbers.

**Assertions:** both terminal observations are preserved; contradictory flag is set; disposition and report verdict are INCOMPLETE; no release; no second dispatch; late event does not overwrite the prior evidence record.

**Anchors:** LOOP-03/05/09/10; CASE-04/05/11/16.

### COORD-05 — attempt identity is enforced before event reduction

**Setup:** Attempt A is active. Fake adapter supplies a valid exit-zero event bound to attempt B, then a real status lookup for A returns UNKNOWN.

**Assertions:** B's event cannot resolve A; attempt A remains unresolved; report is INCOMPLETE; no artifact is released; coordinator does not silently rebind the event.

This must be enforced outside the current reducer because its interface has no expected attempt ID.

**Anchors:** LOOP-03/05/09; CASE-11/13/16.

### COORD-06 — policy revision barrier fails closed

**Setup:** Preparation captures policy revision R1. Fake policy store changes to R2 before dispatch.

**Assertions:** coordinator's atomic/conditional dispatch barrier rejects dispatch; fake adapter dispatch call count is exactly zero; no run is claimed; disposition reflects rejection or incomplete according to the chosen contract; audit event records expected/current revision without leaking secrets.

Repeat for missing, pending, stale, and mismatched policy evidence.

A test that merely reads policy twice and then calls dispatch is not an atomic barrier. The implementation must make the check and dispatch authorization indivisible at the relevant trust boundary, or use a documented provider-enforced revision token/ETag condition.

**Anchors:** LOOP-12/14; CASE-15.

### COORD-07 — dispatch accepted, acknowledgement lost

**Setup:** Fake adapter accepts dispatch for attempt A but simulates a lost acknowledgement before the coordinator receives the response.

**Assertions:** coordinator records the outcome as ambiguous; it performs authoritative lookup using the same tenant/job/attempt/idempotency identity; if lookup finds A, coordinator resumes A without creating a second dispatch; exact dispatch count remains one.

**Anchors:** LOOP-05/09; CASE-11/13/16.

### COORD-08 — ambiguous dispatch lookup remains UNKNOWN

**Setup:** Same as COORD-07, but authoritative lookup returns UNKNOWN or times out.

**Assertions:** no automatic second dispatch; no PASS; disposition/report stays INCOMPLETE or explicitly unresolved; job retains its idempotency key and attempt identity; subsequent retry resumes lookup/reconciliation instead of creating a new attempt unless an explicit, safe recovery rule proves the original was never accepted.

**Anchors:** LOOP-05/09; CASE-11/13.

### COORD-09 — release-time artifact revalidation

**Setup:** Run previously passed. Before download, revoke tenant authorization or mutate/replace the stored artifact so the final-byte digest differs. Also test unsafe path, disallowed media type, excessive size/count, quarantine, and wrong attempt association.

**Assertions:** release denied immediately before bytes are returned; no path outside the artifact root is opened; response does not reveal other tenants' existence or artifact details; event log contains the failed gate; prior execution PASS remains historical and is not rewritten to mean that release succeeded.

**Anchors:** LOOP-10/11/12; CASE-08/14/15.

### COORD-10 — report projection preserves outcome, disposition and uncertainty

**Setup:** Produce the same execution observation with multiple dispositions: for example, EXIT_NONZERO with cleanup UNKNOWN versus EXIT_ZERO with cleanup UNKNOWN, and runtime cap versus UI-only display truncation.

**Assertions:** report projection preserves raw execution outcome separately from disposition; FAIL is not converted to PASS because cleanup is uncertain; UI-only truncation cannot create LIMIT_EXCEEDED; required collector failure cannot be treated as complete output; no unsupported status is silently mapped to generic UNKNOWN without preserving original evidence.

**Anchors:** LOOP-03/04/07/11; CASE-03/06/07/09/10/12.

## 4. Required output-collection state model

Do not represent output collection with one ambiguous boolean. At minimum, the internal evidence model needs to distinguish:

| Evidence | Meaning | PASS implication |
|---|---|---|
| COMPLETE | Required stream was collected through the defined terminal boundary | May satisfy collection gate, subject to provenance |
| PARTIAL | Some output collected, but required stream is incomplete | Must not satisfy a required-complete collection gate |
| UNAVAILABLE | No reliable output collection evidence | Must not satisfy a required-complete collection gate |
| EMPTY | Collection completed and stream contains zero bytes | Can be valid complete output |
| RUNTIME_LIMIT | Runtime/collector enforced a configured output cap | Apply documented limit disposition; preserve bytes/limit evidence |
| DISPLAY_TRUNCATED | Only report presentation was shortened after collection | Must not alter execution disposition |

This is a proposed internal semantic distinction, not a frozen external schema. Define exactly when a stream is required before implementing PASS gating. A provider's lack of separate stdout/stderr or terminal-flush guarantees may constrain the selected adapter and must be evaluated rather than guessed.

## 5. Test layers and evidence gates

| Layer | Can establish | Cannot establish alone |
|---|---|---|
| Pure helper tests | Deterministic validation, mapping, ordering and predicate behavior on supplied values | Authenticity of evidence, concurrency, provider semantics |
| Coordinator + fake adapter | Call ordering, no-dispatch on barrier failure, retry logic, event binding, projection behavior under scripted conditions | Actual provider behavior, true atomicity if only simulated, isolation |
| Persistence integration | Transaction/unique-constraint behavior, restart recovery, concurrent requests, durable report versions | Runtime isolation or provider termination |
| Real controlled execution | Actual termination, resource limits, output handling, network denial, artifact flow, cleanup | Broader guarantees not exercised or repeated |
| Product acceptance | Phone-first flow, copy/paste, result history, truthful status and zero-cost gate | Hidden server guarantees without independent evidence |

## 6. Suggested order once implementation is authorized

1. Resolve semantic choices: provider error projection, whether output collection is a required PASS gate for every runtime, and precise policy-barrier semantics.
2. Add pure-helper regression tests for the concrete gaps in the companion function-level audit.
3. Define the internal coordinator interfaces and deterministic fake-adapter harness, keeping raw execution outcome separate from job disposition and report verdict.
4. Implement state transition/reconciliation path with exact dispatch-count assertions.
5. Add persistence-backed idempotency and report-history tests; do not call in-memory tests durable proof.
6. Add artifact storage and release-time validation tests.
7. Only after a runtime/provider is separately selected and explicitly approved, run applicable controlled boundary tests.
8. Run the complete canonical LOOP/CASE matrix; record NOT RUN/UNKNOWN for unavailable criteria rather than lowering acceptance.

## 7. Evidence status

- This is a test plan, not test output.
- No coordinator/provider adapter has been claimed implemented or verified.
- No tests, provider workload, account, billing action, merge, or deployment was initiated.
- PR #2, PR #3, and canonical acceptance remain unchanged.


### COORD-11 — duplicate identity and sequence-collision diagnostics

**Setup A:** Submit the same event ID, coordinator sequence, kind, and payload twice, but change an identity-bearing field (such as attempt ID, job ID, or tenant) that the finalized event schema says must be immutable.

**Assertions A:** the changed identity is rejected or recorded as contradictory; it cannot be silently treated as an identical retry; the conflict record preserves enough evidence to diagnose the mismatch. Define event-ID scope explicitly before choosing the expected behavior.

**Setup B:** Submit two distinct nonterminal events with the same coordinator sequence, then repeat with one terminal and one nonterminal event.

**Assertions B:** contradiction is set and every colliding event is identifiable in structured diagnostics; conflict output is deterministic and does not duplicate records accidentally.

**Boundary:** these are reducer/coordinator evidence-integrity tests. They do not establish provider authenticity or attempt binding unless the trusted caller supplies and verifies the expected job/attempt identity.

**Anchors:** LOOP-05/07/09/11; CASE-11/13/16.
