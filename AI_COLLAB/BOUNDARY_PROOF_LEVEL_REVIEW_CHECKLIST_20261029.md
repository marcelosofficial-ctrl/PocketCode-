# PocketCode — Boundary Proof-Level Review Checklist

**Date:** 2026-10-29  
**Status:** Review aid / implementation handoff. SPECIFIED ONLY / NOT RUN.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Scope:** Focused review of the provider-neutral boundary sketch, coordinator/fake-adapter plan, and D-05..D-08 gates. This document does not select a provider/store, approve D-01..D-04, authorize implementation/workloads, or alter canonical acceptance.

## Purpose

Before implementation is assigned, force each guarantee to name the boundary that can actually prove it. Pure tests and fake adapters are valuable but must not be cited as evidence for durable transactions, provider behavior, HTTP byte safety, or device acceptance.

## 1. Proof-level matrix

| Claim / invariant | Pure unit test can prove | Fake coordinator/adapter can prove | Required boundary evidence before claiming real guarantee | Stop condition |
|---|---|---|---|---|
| Request/fingerprint validation and deterministic canonicalization | Type, schema, canonicalization, mismatch cases on fixed inputs | Coordinator rejects invalid request before adapter call | Selected request schema and trusted inputs; persistence test if fingerprint is bound to a durable reservation | Boolean/float/type coercion, unstable serialization, or changed semantics accepted under same key |
| Policy revision is the policy actually applied | Pure comparison logic only | No dispatch call when fake barrier says stale/mismatched | Actual dispatch boundary with atomic/conditional revision binding or provider-enforced policy token/ETag; capture trusted applied-policy evidence | Read-then-act race, missing evidence, or fingerprint presented as proof of applied policy |
| Reservation is unique and durable | Helper behavior only | One dispatch in a scripted process | Selected persistent store: unique constraint/transaction, concurrent requests, restart and lost-ack reconciliation | Process-local lock/dictionary treated as durable; two reservations for same tenant/key |
| Ambiguous dispatch does not redispatch | Branching on scripted ACCEPTED/UNKNOWN outcomes | Exact call order/count; UNKNOWN leaves original attempt unresolved | Selected provider contract and integration test for token scope, retention, concurrent starts, authoritative lookup and retry semantics | Timeout/not-found/lease expiry interpreted as proof no operation exists |
| Provider can prove original operation was not created | No | Fake can simulate a declared response only | Provider-specific documented semantics plus integration evidence for consistency and token reuse window | Generic 404/not-found or transient lookup treated as definitive |
| Event scope, replay, and immutable payload | Canonical payload equality, deep-copy/snapshot behavior, conflict projection | Tenant/job/attempt mismatch rejected before reducer; duplicate/conflicting replay paths | Authenticated producer boundary and durable accepted-event identity; restart/replay integration | Client trust flag accepted; changed payload/scope silently treated as exact replay |
| Contradictory terminal evidence remains visible | Deterministic reduction of fixed events | Out-of-order and conflicting events preserved in coordinator projection | Durable event append, concurrency and late-arrival tests | Later event overwrites earlier observation or collision diagnostics omit conflicting records |
| Report append is idempotent and versioned | Projection determinism for supplied evidence | Stable append ID reuse branches under fake store | Actual store transaction/unique constraint; concurrent writers; crash before/after commit; acknowledgement loss; monotonic immutable versions | In-memory history or mock transaction claimed as durable append-only history |
| Report and artifact publication are consistent | State-machine/predicate logic | Simulated partial commit enters PENDING/UNKNOWN and reconciliation path | Selected stores and actual failure injection across commit boundaries; outbox/reconciliation if no shared transaction | Report exposes artifact as downloadable while manifest/object state is incomplete or inconsistent |
| Artifact identity and content are safe | Name/type/size/digest validation on supplied bytes | Release predicate denies scripted bad states | Actual artifact store/API: immutable object version, tenant/job/attempt binding, path/handle safety, TOCTOU and exact bytes | User-controlled path; mutable object reference; unknown manifest or digest accepted |
| Authorization and quarantine are current at release | Predicate logic for supplied current state | Fake revocation/quarantine blocks release | Actual release API/HTTP test, including auth change between lookup and open; documented lease/revocation semantics | Historical PASS or stale authorization used as download permission |
| Integrity and transfer status are honest | Digest computation and status mapping on finite fixtures | Fake stream failures produce PARTIAL/ABORTED, not complete | HTTP/stream integration for exact object version, verification timing, ranges/retries, byte counts and mid-stream failure | Full success reported after partial/unverified transfer; implying already-sent bytes were recalled |
| Output caps and report truncation are distinct | Mapping of RUNTIME_LIMIT / PARTIAL / DISPLAY_TRUNCATED | Fake event sequence exercises the distinct paths | Runtime/collector integration for enforced limits and terminal facts; device test for UI-only truncation | Display truncation creates execution failure, or collection cap is represented as complete output |
| Phone workflow is truthful | Not sufficient | Not sufficient | Supported-device acceptance of run/reconcile/UNKNOWN/copy/download states and explicit simulation labels | UI claims real execution or verified download without boundary evidence |
| $0 / no unauthorized account or workload | Static configuration checks can help | Fake can prove no call in a selected branch | Actual selected architecture, permissions, cost/account review and explicit owner authorization | Paid resource, account, or workload used without explicit approval |

## 2. Focused unresolved blockers for developer and auditor

### B1 — Exact provider evidence for “not created”
Require the adapter proposal to answer, with provider-specific references:
- What exact response means the original operation was not created?
- Is that response strongly consistent across replicas/regions?
- Can a delayed original request still create the operation after that response?
- What are token scope, retention horizon, concurrent same-token behavior, and same-token retry semantics?
- If these cannot be established, does the coordinator retain UNKNOWN and require an owner-approved manual recovery path?

**Required evidence:** provider contract + integration test. Fake-only result is insufficient.

### B2 — Policy barrier at the actual dispatch boundary
Define where expected policy revision is atomically bound to the attempt and how trusted evidence proves what was applied. A read-then-call sequence is not atomic. The fake test must assert zero adapter calls on a stale barrier, but the real claim waits for boundary enforcement proof.

**Required evidence:** pure race/predicate tests + fake call-count test + selected provider/runtime boundary proof. D-05 remains BLOCKED until the last item exists.

### B3 — Report/artifact commit and recovery
Choose one explicit publication strategy only after the store is selected:
- shared transaction; or
- durable outbox/saga with PREPARED/PENDING/COMMITTED/RECONCILING/UNKNOWN-style states (names illustrative).

Specify which record is authoritative, when a report may expose artifact availability, how lost acknowledgements are reconciled, and how restart/concurrent writers behave.

**Required evidence:** pure state-machine tests + real persistence integration with crash/fault injection. Mock stores do not prove transaction durability.

### B4 — Retention horizons and identity namespaces
Publish one retention table covering reservation/idempotency tombstones, provider lookup/token validity, accepted evidence, report versions, manifests, object versions and reconciliation records. Distinguish:
- tenant-scoped idempotency key/reservation identity;
- external source event identity;
- coordinator event identity;
- report append-operation identity;
- immutable report-version identity;
- artifact/manifest/object-version identity.

Specify behavior after each expiry. Expiring a reservation must not accidentally permit a duplicate start while the provider can still have the original operation; expiring evidence must not leave a dependent report/artifact falsely actionable.

**Required evidence:** pure expiry-boundary tests + persistence/restart tests + provider retention semantics where relevant.

### B5 — Release-time authorization and byte-integrity semantics
Define whether authorization is a snapshot, lease, or continuously enforced during a long transfer. State what happens if authorization/quarantine changes after bytes begin streaming. Record bytes sent, transfer completion and integrity verification separately. Prefer verifying the exact immutable object version before sending bytes where practical; do not claim that a post-stream digest check prevents disclosure.

**Required evidence:** pure decision tests + store/API/HTTP integration including race and partial-transfer cases. A release predicate alone is insufficient.

### B6 — Case-level output requirements and verdict semantics
Before freezing coordinator/schema gates, owner decisions D-01..D-04 must settle limit-caused verdict, provider-error projection, per-case required output streams, and event identity/replay semantics. Keep runtime-enforced limit, collection truncation and display truncation distinct. Do not turn optional diagnostic streams into universal PASS gates.

**Required evidence:** explicit owner decisions and canonical traceability. Do not change LOOP/CASE meanings to make an implementation fit.

## 3. Minimum test execution order once separately authorized

1. **Pure contract tests:** strict types, fingerprint determinism, immutable payload snapshots, event replay/conflict, verdict projection, output-state distinctions.
2. **Fake coordinator tests:** COORD-01..12 where applicable; ordered event log; zero dispatch on policy-barrier failure; exact one-dispatch assertion for acknowledgement loss; no redispatch when lookup is UNKNOWN; wrong-attempt evidence rejected.
3. **Persistence integration:** reservation uniqueness under concurrency, restart recovery, stable append identity, monotonic report versions, late evidence, crash/lost-ack reconciliation, retention/expiry.
4. **Provider integration:** same-token concurrent/retry semantics, authoritative lookup, policy binding, actual termination/limits and provider failure behavior.
5. **Artifact store/API/HTTP integration:** immutable object/version, exact digest/size, current authorization, quarantine and cross-store race, bounded ranges/retries, partial transfer status.
6. **Device acceptance:** explicit simulated vs real state, reconnect/reconciliation, report copy/paste, result history, download/partial/denied states.
7. **Canonical regression:** all LOOP-01..14 and CASE-01..16, with each result tied to exact source revision and evidence boundary.

A missing boundary is **BLOCKED/NOT RUN**, not a passing test. Record failures and unknowns; do not weaken acceptance.

## 4. Decision ownership and status

- **D-01..D-04:** OPEN for owner review. Do not freeze final verdict/event schema before resolution.
- **D-05:** BLOCKED until actual policy/dispatch enforcement is selected and proved.
- **D-06:** proposal; requires durable reservation + provider recovery semantics.
- **D-07:** proposal; requires release API/store and current authorization/integrity evidence.
- **D-08:** proposal; requires actual durable append/version/publication evidence.
- **Provider, store, runtime:** none selected.
- **Tests in this pass:** none run. This is a review checklist, not test evidence.
- **Canonical acceptance and PR #2/#3:** unchanged and untouched.
- **No account, billing, workload, merge, deployment, or Actions operation:** performed.

## 5. Source documents

- [Provider-neutral boundary contract sketch](PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md)
- [Coordinator/fake-adapter test plan](COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md)
- [Cross-decision contradiction audit and gates](CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md)
- [Owner decision register](OWNER_DECISION_REGISTER_20261029.md)
- [D-06 idempotency recovery checklist](IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md)
- [D-07 artifact release checklist](ARTIFACT_RELEASE_FALSIFICATION_CHECKLIST_20261029.md)
- [D-08 report history checklist](REPORT_HISTORY_PERSISTENCE_FALSIFICATION_CHECKLIST_20261029.md)
- Canonical acceptance on main: `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` and `PRODUCT/EXECUTION_CONTRACT.md`.


## 6. Suggested independent review tasks

These are ready-to-copy task briefs. They request review only; they do not authorize repository writes, implementation, provider selection, tests that invoke workloads, or changes to canonical acceptance.

### Claude — implementation-readiness review

> Inspect the pinned research-branch documents linked in this checklist, especially the provider-neutral boundary sketch, coordinator/fake-adapter test plan, D-06/D-07/D-08 falsification checklists, and cross-decision gate audit. Do not edit files, select a provider/store/runtime, run workloads, or change canonical acceptance. Return one consolidated review with: (1) any missing state/identity/transition that prevents implementation; (2) exact crash/timeout/ack-loss windows; (3) transaction and reconciliation requirements; (4) a minimum interface and test sequence that avoids premature schema freeze; (5) each claim's required proof boundary; (6) specific blockers and source-document section references. Explicitly separate proposed semantics from implemented code and mark all untested behavior NOT RUN. Preserve D-01..D-04 as owner-open and D-05 as blocked pending actual boundary proof.

### Gemini — independent adversarial audit

> Independently challenge the same pinned documents without assuming the proposed contract is correct. Do not edit files, run workloads, choose a provider/store/runtime, or alter canonical acceptance. Look specifically for: (1) a path to duplicate external execution after ambiguous start; (2) false “definitively not created” conclusions; (3) policy TOCTOU or fake ETag barriers; (4) cross-tenant/job/attempt evidence or artifact confusion; (5) duplicate, lost, mutable, or partially published report versions; (6) expiry combinations that reopen idempotency or orphan dependent evidence; (7) authorization revocation and bytes already sent during streaming; (8) any statement whose evidence level is overstated. Return only concrete counterexamples, missing tests, contradictions, and required boundary evidence, with document/section references. If no defect is found in an area, say what was inspected and what remains unproven. Do not invent or remap canonical LOOP/CASE IDs.

### Reconciliation rule for ChatGPT

Treat both responses as review input. Reconcile every claimed issue against the pinned documents and canonical acceptance; record disagreements and unknowns instead of silently choosing a side. Do not update owner decisions or the implementation contract merely to satisfy either reviewer. A follow-up research edit requires a concrete, source-grounded finding.


## Implementation backlog pointer

The dependency-ordered work packages and closure criteria are now in [IMPLEMENTATION_READINESS_BACKLOG_20261029.md](IMPLEMENTATION_READINESS_BACKLOG_20261029.md). Use that backlog to sequence work after the independent reviews; do not treat its work-package names as approved implementation scope.
