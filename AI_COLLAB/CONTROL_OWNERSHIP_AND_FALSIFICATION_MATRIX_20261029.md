# PocketCode — control ownership and falsification matrix

**Date:** 2026-10-29  
**Status:** Research/test architecture only; not implementation, not a frozen schema, and NOT RUN.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Companions:** `FUNCTION_LEVEL_CONFORMANCE_AUDIT_20261029.md`, `COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md`, `ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md`.

## Purpose

Make the next implementation/review step falsifiable by naming the owner boundary for each safety property, the minimum negative test that can disprove it, and the evidence that would actually support a claim. This document does not assert that any proposed owner/interface currently exists.

## 1. Control-to-owner matrix

| Control | Proposed owner boundary | Required invariant | Minimum falsification test | Existing plan anchor | Evidence needed before claiming satisfied |
|---|---|---|---|---|---|
| Request shape, identity, and input names | Request validator before reservation or file creation | Reject malformed/nonblank identity errors, unsupported recursive policy values, unsafe names, and normalized-name collisions before side effects | Submit whitespace-only IDs, non-string nested policy keys, case/Unicode-colliding names, Windows device aliases; assert rejection and zero writes | FLA-02/09/10/11/13; LOOP-01/10/12; CASE-08/14/15 | Executed unit tests plus coordinator test proving validation precedes any reservation, file creation, or dispatch |
| Fingerprint-to-applied-policy binding | Coordinator + policy enforcement/dispatch boundary | Fingerprint represents the exact effective policy bound to the attempt; revision cannot change between confirmation and dispatch | Capture R1, switch to R2 at the dispatch race point; assert atomic/conditional rejection and dispatch count 0; repeat with same fields but changed policy values | FLA-11; COORD-06; LOOP-12/14; CASE-15 | Executed race/concurrency test against the actual enforcement primitive; fake-only tests prove coordinator logic, not real atomicity |
| Event producer authentication | Trusted adapter ingress / event verifier | Client-controlled payload cannot claim trusted status; producer identity and source class are authenticated or explicitly untrusted | Send forged terminal event with a valid-looking job/attempt and client-set trust flag; assert reject/quarantine and no terminal state change | FLA-04/07; COORD-05/11; LOOP-03/05; CASE-11/16 | Implemented authentication/validation path and negative tests at ingress; reducer tests alone are insufficient |
| Job/attempt/tenant/policy binding | Coordinator event ingress before pure reduction | Every accepted event belongs to the expected tenant, job, attempt and required policy revision; retry identity is explicit | Deliver a real-looking EXIT_ZERO from attempt B while A is active; assert A remains unresolved, no PASS/release, no identity rebinding | FLA-04/07; COORD-05; LOOP-03/05/09; CASE-11/13/16 | Integration test with expected identity passed separately to verifier; source code review showing binding cannot be bypassed |
| Event immutability and conflict diagnosis | Authenticated evidence ingress/store + reducer contract | Coordinator-owned event IDs are unique; source-event dedupe is namespaced by source/tenant/job/attempt; duplicate equivalence covers immutable binding and payload fields; sequence collisions identify every colliding event | Exact source replay; same scoped source ID with changed attempt/job/tenant/source/policy/payload; nested payload mutation; distinct events with the same per-attempt sequence; assert no cross-attempt binding, immutable snapshots and complete deterministic conflicts | FLA-04/06/07/08; COORD-05/11/12; LOOP-03/05/07/11; CASE-11/13/16 | Authenticated ingress tests plus immutable payload tests; persistence integration where durability/concurrency is claimed |
| Terminal verdict projection | Trusted coordinator projection, not report formatter | Execution outcome, job disposition, report verdict, cleanup, collection completeness and release authorization remain distinct; ambiguous/contradictory evidence cannot yield PASS | Remove each required PASS gate in turn; provide EXIT_ZERO with cleanup UNKNOWN; add late contradictory terminal event; assert no PASS | COORD-01/02/04/10; SEM-01..08; LOOP-03/04/05; CASE-01..06/09/10/16 | Pure projection tests and coordinator integration tests; report formatter receives trusted derived fields but does not confer trust itself |
| Output collection and redaction | Runtime adapter/collector before report projection | Distinguish COMPLETE/PARTIAL/UNAVAILABLE/EMPTY/RUNTIME_LIMIT/DISPLAY_TRUNCATED; bound bytes and processing; do not claim exhaustive secret removal | Fail one stream after partial output; test overlength secret-like values and chunk boundaries; exceed per-stream and aggregate caps; separate runtime cap from UI truncation | FLA-03/05/12; COORD-10; LOOP-07/11/12; CASE-07/12/15 | Unit tests, collector integration tests, and controlled hostile-output test on the selected runtime; regex coverage alone is not a security boundary |
| Idempotency and ambiguous dispatch | Coordinator + atomic persistent reservation/store | Same logical request resolves to the same attempt; an uncertain acknowledgement never triggers blind replay; concurrent duplicate submissions cannot create two jobs | Adapter accepts dispatch but response is lost; lookup returns UNKNOWN; concurrently submit same tenant/key; assert exact dispatch count and durable uniqueness | COORD-07/08; G4; LOOP-05/09; CASE-11/13/16 | Persistence-backed concurrency/restart tests and provider-specific lookup semantics; in-memory helpers are not enough |
| Report history and reconciliation | Durable report/evidence store | New observations append a version; prior issued reports are not rewritten; concurrent updates do not lose or reorder evidence | Restart after first report, reconcile cleanup UNKNOWN→CONFIRMED, race two append operations; assert monotonic versions and retained history | FLA-10; COORD-10; SEM-01..08; LOOP-09; CASE-11/12/16 | Transactional storage tests, concurrent writers and restart recovery; in-memory `ReportHistory` only proves local model behavior |
| Artifact validation and release | Artifact store + release-time authorization gate | Release revalidates tenant/job/attempt, current authorization, safe path, type, size/count, quarantine state and stored-byte digest immediately before returning bytes | Pass run then revoke authorization; replace bytes; request wrong-attempt artifact, unsafe path or oversized file; assert zero bytes released and historical verdict unchanged | COORD-01/09; G6; LOOP-10/11/12; CASE-08/14/15 | Storage/download integration tests including final-byte digest and access-control checks; metadata-only fake is not enough |
| Resource isolation, timeout and egress | Selected execution runtime/provider enforcement boundary | Deadline, termination, memory/output bounds and network policy are enforced outside untrusted program claims | Infinite loop, subprocess/spawn attempt, outbound connection, output flood, cancellation race; assert authoritative termination and independently observed enforcement | LOOP-12; CASE-04/05/07/15 | Controlled tests on selected runtime/provider and configuration evidence; a fake adapter cannot establish actual isolation |
| Phone-first user workflow and cost gate | Mobile UI/product integration + owner-controlled configuration | User can select inputs, see truthful state, copy bounded reports, and use the product without unapproved spend/account actions | iPhone end-to-end import/run/export/copy test; verify all run states; assert no paid resource/account/workload creation without explicit approval | LOOP-01/02/08/13/14; CASE-12 | Hands-on target-device acceptance and billing/account audit appropriate to the chosen path; source documentation alone is insufficient |

## 2. Evidence labels (use consistently)

- **VERIFIED IN SOURCE:** exact code path inspected at a pinned ref; describes only that source version and scope.
- **UNIT TESTED:** exact test command and environment ran successfully against the pinned source; record test IDs/counts and commit.
- **FAKE-ADAPTER TESTED:** coordinator behavior passed with deterministic scripted dependencies; not proof of provider or storage guarantees.
- **INTEGRATION TESTED:** actual selected adapter/store/runtime boundary was exercised; record versions, configuration, test case, and observed evidence.
- **DEVICE ACCEPTED:** user-visible workflow was exercised on the target phone/platform.
- **SPECIFIED ONLY:** a document states a requirement; no implementation proof.
- **NOT RUN / UNKNOWN:** no adequate observed evidence. Do not silently promote either to PASS.
- **BLOCKED:** required resource/permission/platform is unavailable or not authorized.

A source pin, written test, synthetic fixture, green fake test, or acceptance checklist is not interchangeable with an integration result.

## 3. Minimal test order after implementation is separately authorized

1. Resolve owner decisions: provider-error projection, required output streams/collection gates, event-ID scope, exact policy binding, and artifact semantics.
2. Add helper-level tests for FLA-01..13 where the relevant helper is selected for integration; fix source/test drift before merging anything.
3. Implement request validation and side-effect-free rejection first.
4. Implement trusted event ingress and job/attempt binding before terminal reduction.
5. Implement the policy revision/dispatch barrier and prove the underlying atomic/conditional primitive.
6. Implement coordinator projection and ambiguous-ack recovery with exact dispatch-count tests.
7. Add persistence concurrency/restart tests for reservations, tombstones and report history.
8. Add collector/output and artifact-release integration tests.
9. Only after a provider/runtime is explicitly selected and approved, run controlled termination, resource, egress and artifact tests.
10. Run the full canonical LOOP-01..14 / CASE-01..16 matrix and record unavailable items as NOT RUN/UNKNOWN rather than weakening acceptance.

## 4. Stop conditions

Stop and do not claim the control is satisfied if any of the following is true:

- The expected job/attempt identity is not known at the point evidence is accepted.
- A terminal event's producer/source cannot be authenticated or classified.
- The policy revision is checked but not bound atomically to dispatch.
- An ambiguous dispatch acknowledgement would cause an automatic new dispatch.
- A required output stream is PARTIAL/UNAVAILABLE but treated as complete.
- Runtime enforcement is inferred only from UI labels or program output.
- Artifact authorization/integrity is checked only when the run first completes, not at release.
- Idempotency/history claims rely only on in-memory state.
- A test was specified or simulated but described as executed against a real boundary.
- Any required security/cost/device criterion remains UNKNOWN but is reported as PASS.

## 5. Current evidence state

- This matrix is a research/test-architecture artifact only.
- The adapter/coordinator specifications remain proposed; no selected provider/runtime or integrated trust boundary has been verified.
- Existing COORD-01..12 cases are design only; no tests were run in this pass.
- Canonical `PRODUCT/EXECUTION_CONTRACT.md` and `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` are not modified.
- PR #2 and PR #3 are not modified. No implementation, account, billing, workload, merge, or deployment action is authorized by this document.
