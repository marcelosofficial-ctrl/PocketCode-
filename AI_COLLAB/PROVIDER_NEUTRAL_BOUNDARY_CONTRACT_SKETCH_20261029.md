# PocketCode — Provider-Neutral Boundary Contract Sketch (Dispatch, Evidence, Reports, Artifacts)

**Date:** 2026-10-29  
**Status:** Proposed interface sketch for owner/architecture review. SPECIFIED ONLY / NOT RUN. Not a frozen public schema, implementation, provider selection, or authorization to launch workloads.

## Purpose

Turn D-05 through D-08 into a minimum boundary contract that can be implemented and falsified without prematurely selecting a provider or persistence engine. The contract deliberately separates local coordination guarantees from guarantees that only a real provider, durable store, artifact store, HTTP boundary, or device can establish.

Related research: `OWNER_DECISION_REGISTER_20261029.md`, `ADAPTER_BOUNDARY_DECISION_GATE_20261029.md`, `IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md`, `REPORT_HISTORY_PERSISTENCE_FALSIFICATION_CHECKLIST_20261029.md`, `ARTIFACT_RELEASE_FALSIFICATION_CHECKLIST_20261029.md`, and `CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md`.

## 1. Contract rules

1. Every operation is scoped to an authenticated tenant and stable logical job/attempt identity. User-supplied IDs never establish authorization.
2. Request fingerprint and applied-policy binding are distinct fields with distinct evidence. A fingerprint does not prove what policy ran.
3. Reservation and dispatch intent must be durably committed before external start can be called.
4. Once dispatch intent is committed, missing acknowledgement is ambiguous. Recovery reconciles the original attempt; it never creates a new attempt merely because a lease expired, a request timed out, or a lookup is unavailable.
5. Raw evidence is immutable after acceptance. A conflict adds diagnostic evidence or a new projection; it does not silently overwrite the prior observation.
6. Report versions are immutable. A new accepted observation or derived-state change produces a new version; old versions remain addressable under the documented retention policy.
7. Artifact release is a new authorization decision at the release boundary. Execution PASS is neither a release token nor a substitute for current authorization, manifest integrity, lifecycle checks, and exact-object verification.
8. Any missing/contradictory mandatory evidence yields UNKNOWN/INCOMPLETE or BLOCKED according to the owning contract; never synthesize success.
9. Every interface operation must return a typed outcome distinguishing success, definitive rejection, conflict, retryable failure, and unresolved/ambiguous outcome. Generic exceptions must not be translated into success.
10. This sketch does not decide owner-open D-01..D-04 semantics or override canonical acceptance.

## 2. Shared identity vocabulary

The eventual schema should carry, where applicable:

- `tenant_id`: authenticated scope, derived from trusted identity.
- `job_id`: stable logical request identity.
- `attempt_id`: stable identity of one intended external execution attempt.
- `idempotency_key`: caller retry key, scoped to tenant; never globally authoritative by itself.
- `request_fingerprint` and `fingerprint_schema_version`: canonical digest and version for all accepted execution-affecting request semantics.
- `expected_policy_revision`: policy revision required for the attempt, if applicable.
- `applied_policy_revision` plus trusted evidence reference: what the dispatch boundary proves was applied to this attempt.
- `provider_operation_id` and `provider_idempotency_token`: namespaced external identifiers, nullable until authoritatively established.
- `event_id`: coordinator-owned canonical accepted-event identity.
- `source_namespace` and `source_event_id`: authenticated producer namespace and external replay identity, where supplied.
- `append_operation_id`: stable idempotency key for one report/evidence append request.
- `report_version_id` / monotonic per-job `report_version`: immutable issued projection identity.
- `artifact_id`, `manifest_version`, immutable `object_version`, digest and byte size: artifact and exact content identity.
- `correlation_id`: diagnostics only; not an authorization, deduplication, or execution identity substitute.

Identifiers must be validated as bounded values at their trust boundary. Do not put credentials, secrets, or raw sensitive policy values in identifiers or logs.

## 3. Reservation and dispatch interface

### 3.1 Reserve

Conceptual input:
`Reserve(tenant, idempotency_key, request_fingerprint, fingerprint_schema_version, validated_request_ref, expected_policy_revision)`

Atomic result:
- `RESERVED_NEW(job_id, attempt_id, reservation_version)` — unique reservation committed; no provider call has occurred.
- `EXISTING_SAME(job_id, attempt_id, current_state)` — same tenant/key/fingerprint resolves to the original identity.
- `CONFLICT` — key already bound to changed semantics; zero new dispatches.
- `REJECTED` — validation or authorization failed before reservation.
- `UNAVAILABLE/UNKNOWN` — reservation outcome cannot be established; reconcile by the tenant-scoped idempotency key and reservation identity before retrying. Report append-operation identity is a separate namespace and must not be used to resolve a reservation.

Required atomicity: one durable uniqueness boundary on the documented tenant/key scope, with fingerprint comparison performed against the committed row. A process-local lock/dictionary is not sufficient evidence.

### 3.2 Record dispatch intent

Conceptual operation:
`CommitDispatchIntent(job_id, attempt_id, reservation_version, expected_policy_revision, provider_idempotency_token)`

It must atomically verify that the reservation is still eligible, persist the stable attempt/provider token, and record the exact policy revision requirement before any external start call. If the boundary cannot bind the required policy revision immutably or conditionally at start, return `BLOCKED_POLICY_BARRIER`; do not call the provider.

A crash before dispatch intent commit is a different recovery state from a crash after intent commit. This distinction must be enforced by transaction/call ordering, not inferred from missing acknowledgement rows.

### 3.3 Start or reconcile

Conceptual provider adapter operations:
- `Start(attempt_id, provider_idempotency_token, immutable_policy_binding, bounded_execution_request)`
- `LookupOriginal(provider_idempotency_token, provider_operation_id?)`

Typed outcomes:
- `ACCEPTED(provider_operation_id, provider_evidence_ref, applied_policy_evidence)`
- `DEFINITIVELY_REJECTED_BEFORE_START(reason, authoritative_evidence)`
- `DEFINITIVELY_NOT_CREATED(authoritative_evidence, retry_semantics)`
- `AMBIGUOUS(reason)`
- `UNAVAILABLE(reason)`

The last two outcomes do not permit a second start. `DEFINITIVELY_NOT_CREATED` is usable only if the selected provider contract proves its meaning, consistency, and retry-token behavior. An ordinary not-found response must not be presumed authoritative.

After a start may have been sent, retry the lookup/reconciliation for the same original attempt and token. Provider idempotency semantics must be documented: scope, retention horizon, concurrent request behavior, and whether the same token returns the same operation. If the provider cannot supply safe idempotent start or authoritative lookup, the product cannot claim duplicate-free recovery; preserve UNKNOWN and require an explicitly approved manual path.

## 4. Evidence acceptance and reduction

Conceptual operation:
`AcceptEvidence(expected_tenant, job_id, attempt_id, source_namespace, source_event_id, payload, authenticated_producer_context)`

Before reduction:
1. authenticate producer and trust class;
2. validate tenant/job/attempt and relevant policy binding against the reservation;
3. validate bounded schema/version and canonical payload;
4. assign coordinator-owned `event_id` and attempt-scoped monotonic sequence;
5. enforce replay identity and immutable-content equality;
6. persist accepted evidence before exposing a derived projection.

Outcomes:
- `ACCEPTED_NEW(event_id, sequence)`
- `EXACT_REPLAY(existing_event_id)`
- `CONFLICT(existing_identity, bounded_conflict_reason)`
- `REJECTED_UNTRUSTED`
- `UNKNOWN_STORE_COMMIT` — reconcile by append/event identity; do not assume rollback or append a second logical event.

Exact replay requires same scoped source identity and all immutable observation fields. Reuse of an identity with changed payload, attempt, tenant, source, sequence or relevant policy binding is conflict, not success. Client-provided trust flags are never sufficient proof of trusted producer identity.

The reducer must preserve separate fields for execution outcome, job disposition, user-facing verdict, cleanup state, output collection state/completeness, applied-policy barrier, report publication state, and artifact release state. Do not compress these into one status enum.

## 5. Append-only report publication

Conceptual operation:
`AppendReportEvidence(tenant_id, job_id, attempt_id, append_operation_id, accepted_event_ids, projection_schema_version)`

Requirements:
- append identity is idempotent for identical canonical content; changed-content reuse conflicts;
- evidence references are immutable and scope-bound;
- per-job version allocation is atomic, monotonic and concurrency-safe;
- projection content and evidence references become visible as one complete version;
- lost commit acknowledgement is reconciled using the same append operation ID;
- late/contradictory evidence creates a new version with conflict diagnostics, never mutation of an issued version;
- deterministic projection records its schema/version and exact evidence set;
- a cleanup or release update creates a later projection without rewriting historical execution observations.

Possible outcomes:
- `COMMITTED(report_version_id, report_version)`
- `EXISTING_IDENTICAL(report_version_id, report_version)`
- `CONFLICT_APPEND_ID`
- `REJECTED_SCOPE`
- `COMMIT_UNKNOWN` (reconcile; never blindly append under a new ID)

Do not call an in-memory list durable history. A persistence claim requires restart, transaction, uniqueness and concurrent-writer evidence against the selected store.

## 6. Artifact publication and release

### 6.1 Trusted publication

Only a trusted publisher may commit a manifest that binds:
- tenant/job/attempt and the producing accepted evidence;
- opaque artifact ID and manifest version;
- immutable object version/reference;
- digest algorithm/value and exact byte size;
- validated media type and normalized display name;
- lifecycle/quarantine state and retention/expiry metadata.

Manifest publication must be tied to the corresponding report/evidence state. If report and object/manifest live in different stores, use a documented transactional outbox or reconciliation protocol. While publication is pending or inconsistent, the report must not advertise the artifact as releasable. Crash recovery must resolve to a complete committed state or a visible pending/unknown state.

### 6.2 Release decision

Conceptual operation:
`AuthorizeAndOpenArtifact(authenticated_principal, tenant_id, job_id, attempt_id, artifact_id, manifest_version, requested_transfer_bounds)`

The release boundary must:
1. authorize the current principal and scope;
2. check the exact tenant/job/attempt association;
3. load a trusted complete manifest and current lifecycle/quarantine state;
4. resolve an immutable object version/handle rather than a user-controlled path;
5. enforce object count/size/type and request/range/aggregate limits;
6. verify digest and size against the exact immutable bytes to be returned, with documented verification timing;
7. establish a race-resistant authorization/object snapshot or explicitly document lease/revocation semantics;
8. record allow/deny, exact object version/digest, and bounded reason without leaking cross-tenant existence.

Possible outcomes:
- `RELEASE_OPENED(exact_object_version, expected_digest, expected_size, authorization_snapshot_or_lease)`
- `DENIED_AUTHORIZATION`
- `DENIED_SCOPE`
- `DENIED_MANIFEST_OR_LIFECYCLE`
- `DENIED_INTEGRITY`
- `DENIED_LIMIT`
- `RELEASE_UNKNOWN`

A long transfer must separately report `bytes_sent`, `transfer_complete`, and `integrity_verified`. A mid-stream failure cannot be undone; it must not be reported as a completed verified download. If immediate revocation during transfer is required, the selected API must define and prove how active streams are terminated. Do not imply zero bytes after revocation unless that exact guarantee is tested.

Execution verdict and release status remain separate. A release denial must not rewrite historical execution PASS. If a specific acceptance case requires a valid artifact, that case's overall gate remains unsatisfied until its release requirements pass.

## 7. Cross-store consistency and retention

Before selecting a store, document the transaction/consistency primitives for:
- reservation uniqueness and fingerprint conflict;
- dispatch-intent durability and state transitions;
- event append identity and accepted evidence;
- monotonic report-version allocation;
- report/manifest publication and reconciliation;
- quarantine/deletion/expiry racing with release;
- retention of reservation keys/tombstones, evidence, reports, manifests and object bytes.

Required relationship: no dependent record should remain misleadingly actionable after the identity/evidence needed to validate it has expired. Define minimum horizons for the longest permitted retry, provider lookup, reconciliation and artifact/report availability. After expiry, behavior must be explicit and must not accidentally reopen an idempotency key or permit an unsafe second start.

If atomic multi-store transactions are unavailable, choose and test a recoverable state machine such as PREPARED → COMMITTED, with explicit RECONCILING/UNKNOWN states. A reconciliation worker must be idempotent and must never turn missing evidence into assumed success. Exact state names are illustrative, not frozen schema.

## 8. Required falsification suite and proof levels

Minimum traceability:
- Reservation/dispatch/recovery: DR-01..DR-12; provider-boundary PBR-01..07 and PF-01..05.
- Evidence/reducer: COORD-04/05/11/12 and FLA-04/06/07/08/11.
- Report history: RH-01..RH-14.
- Artifact release: AR-01..AR-14.
- Product behavior: LOOP-01..14 and CASE-01..16.

For each test, record exact source revision, selected boundary and version, fixture, expected outcome, observed outcome, dispatch count, identity bindings, persisted evidence/version IDs, and evidence level.

Evidence must be labeled precisely:
- pure helper/unit test;
- fake-adapter test;
- persistence integration;
- provider integration;
- artifact store/API/HTTP integration;
- device acceptance.

A fake can prove that the coordinator chooses not to redispatch for UNKNOWN. It cannot prove provider idempotency. A mocked transaction cannot prove durable uniqueness or crash recovery. A release predicate unit test cannot prove that HTTP returns only the verified immutable bytes. A desktop test cannot prove phone behavior.

## 9. Hard stops

Mark the relevant claim BLOCKED/UNKNOWN and do not proceed past the gate if:
- the actual policy applied to the attempt cannot be established;
- ambiguous dispatch can trigger an automatic second start;
- evidence can cross tenant/job/attempt or policy boundaries;
- append/version identity can overwrite or duplicate history silently;
- a partial report or manifest can be exposed as committed;
- artifact release relies on historical PASS or a user-controlled path/name;
- authorization, quarantine, immutable version or digest/size is unknown;
- storage commit outcome cannot be reconciled by stable identity;
- required account, billing, workload, permission or cost is not explicitly approved.

## 10. Current state and next decision

This is a proposed boundary contract sketch only. No implementation or test was run, no provider/store/API/runtime was selected, and no account, billing, workload, merge, or deployment action occurred. D-01..D-04 remain owner-open; D-05 remains BLOCKED until a real policy/dispatch boundary is selected and proven; D-06..D-08 remain proposals requiring owner review.

Next, review this sketch against the intended first runtime architecture and resolve owner decisions before freezing schemas. Do not implement provider-specific guarantees in a fake adapter or claim that this document proves the system is safe.
