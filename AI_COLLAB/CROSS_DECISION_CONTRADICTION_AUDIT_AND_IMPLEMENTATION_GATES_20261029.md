# PocketCode — Cross-Decision Contradiction Audit and Implementation Gate Sequence

**Date:** 2026-10-29  
**Status:** Read-only source/document audit plus proposed sequencing. SPECIFIED ONLY / NOT RUN.  
**Scope:** D-06 idempotency/recovery, D-07 artifact release, D-08 report history, their owner register, control matrix, semantic crosswalk, adapter envelope, coordinator/fake test plan, and D-05 policy-boundary gate. This is not canonical acceptance and does not approve any owner-open decision.

## Executive result

No direct logical contradiction was found among the D-06/D-07/D-08 checklists and their cross-references in the inspected versions. Their core rules align:
- Ambiguous dispatch never authorizes blind redispatch (D-06).
- Execution PASS is not download authorization; release is checked against current authority and exact immutable artifact identity/bytes (D-07).
- Previously issued report versions are immutable; new evidence creates a new version, and report/artifact publication must be atomic or explicitly reconciled (D-08).
- Fake tests can verify coordinator branching and call order, but cannot prove provider idempotency, durable uniqueness, storage atomicity, HTTP release safety, or device behavior.

This is a documentation-level consistency result only, not evidence that any implementation satisfies the rules.

## Cross-boundary invariants

1. **Identity continuity:** authenticated tenant + logical job + attempt + request fingerprint + applied-policy evidence must remain linked from reservation, through provider dispatch/reconciliation, accepted evidence, report version, artifact manifest, and release. A mismatch is rejected/quarantined, not rebound.
2. **Ambiguous dispatch:** once durable dispatch intent exists, missing acknowledgement or lease expiry means reconcile the original attempt. Only a provider-specific authoritative result or provider-enforced idempotency can establish safe recovery. Otherwise retain UNKNOWN and do not dispatch again.
3. **Policy barrier:** request fingerprinting identifies validated request semantics; it does not prove the actual policy applied at start. D-05 stays BLOCKED until a selected boundary proves immutable per-attempt policy binding or an atomic/conditional start barrier.
4. **Evidence and report history:** accepted observations are immutable. Retries use stable append identities; exact retries resolve to the prior append, conflicting reuse is rejected, and late/contradictory evidence is appended and projected into a new report version.
5. **Release boundary:** release independently checks current authorization, tenant/job/attempt binding, trusted complete manifest, lifecycle/quarantine state, immutable object version and digest/size, bounded response, and non-disclosure. Historical PASS does not override a failed release gate.
6. **Cross-store publication:** a report and artifact manifest must not become jointly visible as a successful releasable result until their consistency is established. If atomic transactions are unavailable, use a documented outbox/reconciliation protocol and fail closed while unresolved.
7. **Projection separation:** preserve raw execution outcome, job disposition, user-facing verdict, cleanup state, collection completeness, and artifact-release status separately. A later cleanup/release observation may affect a new projection, but must not rewrite an already issued report version.

## Residual ambiguities to resolve before implementation

These are open interface/owner decisions, not contradictions in the written checklists.

- **A. Dispatch “definitively not created”:** D-06 DR-08 correctly makes retry conditional on provider semantics. The selected adapter contract must specify what exact provider response is authoritative, whether “not found” is strongly consistent, the safe retry window, and whether the same provider token remains valid. Until then, not-found/timeout remains UNKNOWN.
- **B. Authorization during a long download:** D-07 AR-13 identifies the revocation race but does not choose whether authorization is a one-time release snapshot, short-lived lease, or continuously enforced during streaming. The owner/API contract must define revocation consistency and whether mid-stream revocation terminates transfer. Do not claim immediate revocation semantics without that proof.
- **C. Byte integrity and partial disclosure:** pre-release verification against an immutable object version can prevent sending unverified bytes. If mutation or stream integrity failure is detected only after streaming begins, already-sent bytes cannot be recalled. The API must distinguish bytes sent, transfer completion, digest-verification timing, and partial/aborted status; never report complete success for an interrupted or unverified transfer.
- **D. Report/artifact publication order:** D-06's crash matrix and D-08's cross-store invariant agree on fail-closed publication, but the concrete state machine is not selected. Define pending/prepared/committed/reconciling states and the exact point at which a report may advertise artifact availability.
- **E. Retention horizon alignment:** D-06 reservation/tombstone retention, D-08 report/evidence retention, and D-07 artifact/manifest retention must be specified together. Expiring one identity record while a dependent report/artifact remains addressable can create unsafe replay or orphaned references. The selected design must state minimum horizons and post-expiry behavior.
- **F. Append versus projection idempotency:** D-08 requires append operation IDs to be idempotent and changed-content reuse to conflict. The implementation must keep the append-operation identity distinct from report-version identity and evidence-event identity; a projection recompute must not accidentally duplicate raw evidence or mutate a historical version.
- **G. Release-status projection:** keep release denied/quarantined/partial separate from execution verdict. A release failure must not rewrite historical execution PASS, while a required artifact that is part of a particular acceptance case may still mean the case-level success gate was never satisfied. D-03/case-specific requirements remain owner-open.

## Proposed implementation gate sequence

This is an ordering recommendation, not permission to select or deploy a provider/store.

| Gate | Owning boundary | Minimum falsification coverage | Evidence required to pass this gate | Stop condition |
|---|---|---|---|---|
| G0 — Owner semantics | Product owner + canonical contract | D-01..D-04 decisions; required streams/artifacts per case; provider-error and limit mapping; event identity | Explicit decisions recorded; canonical acceptance remains unchanged unless separately authorized | Any unresolved verdict or required-output ambiguity affects the proposed implementation |
| G1 — Boundary and cost gate | Adapter/provider + security + owner | D-05 PBR-01..07/PF-01..05; $0, account, egress and policy enforcement review | Exact selected boundary contract and cost/authorization evidence; real policy-application proof path | No enforceable policy barrier, cost/account ambiguity, or unauthorized hosted workload |
| G2 — Pure contract validation | Request/fingerprint/event/report helpers | FLA findings; strict types; recursive canonical policy validation; scoped replay; immutable snapshots; verdict projections | Reproducible unit tests against pinned source and explicit schemas | Fake/unit result is being represented as persistence/provider proof |
| G3 — Durable reservation and dispatch | Coordinator + transactional store + provider contract | DR-01..12; COORD-07/08; concurrent same-key requests; crash windows; lost acknowledgement; lease expiry | Persistence-backed uniqueness/restart evidence plus provider-specific idempotency/authoritative lookup evidence | Any ambiguous dispatch can trigger blind second start |
| G4 — Trusted evidence and report history | Authenticated ingress + durable event/report store | COORD-04/05/11/12; RH-01..14; append retry/conflict, concurrent writers, crash/publication recovery | Tenant/job/attempt/policy-bound immutable evidence; atomic monotonic report versions; restart and concurrency tests | Evidence can be rebound, lost, mutated, duplicated, or partially published |
| G5 — Artifact publication and release | Coordinator + artifact store + release API/HTTP | AR-01..14; report/manifest cross-store failure; auth revocation; quarantine race; byte mutation; bounded transfer | Exact immutable object/version and digest evidence, current auth check, safe streaming, cross-store reconciliation | Historical PASS alone releases bytes; mismatch/unknown state returns success |
| G6 — Device/user workflow | Phone UI + report/copy/download flows | Device acceptance for all states: retrying, reconciling, UNKNOWN, conflict, denied, quarantined, partial, aborted, completed | Device-observed behavior, bounded copy/report, explicit simulation labels, truthful download state | UI implies external execution, completion, or successful download without authoritative evidence |
| G7 — Canonical regression | Full coordinator/runtime + device path | LOOP-01..14 and CASE-01..16, including retries, ambiguous outcomes, and out-of-order completion | Per-case evidence with exact versions and boundary labels; unavailable cases recorded NOT RUN/UNKNOWN | Any mandatory criterion is silently weakened or marked PASS without evidence |

**Gate dependencies:** G0 precedes final verdict/output semantics; G1 precedes real execution-boundary claims; G2 can proceed with pure helpers but cannot substitute for G3-G6; G3 must precede claims about safe recovery; G4 must precede durable history claims; G5 must precede artifact-release claims; G6/G7 require the integrated path. The sequence may be parallelized only where dependency and evidence boundaries remain explicit.

## Evidence labels

Use labels precisely:
- **SPECIFIED ONLY:** invariant/test described; no implementation proof.
- **VERIFIED IN SOURCE:** static claim about a pinned source revision only.
- **UNIT TESTED:** executed tests for pure logic only.
- **FAKE-ADAPTER TESTED:** scripted coordinator decisions/call counts only.
- **PERSISTENCE INTEGRATION TESTED:** actual selected store, transactions, restart and concurrency exercised.
- **PROVIDER INTEGRATION TESTED:** selected provider's real start/lookup/policy semantics exercised.
- **STORE/API/HTTP INTEGRATION TESTED:** actual artifact and release boundary exercised.
- **DEVICE ACCEPTED:** observed behavior on the supported phone workflow.
- **NOT RUN / UNKNOWN:** evidence absent or insufficient.
- **BLOCKED:** required boundary/resource/permission is unavailable or not authorized.

Do not promote one evidence label to another.

## Cross-reference inventory

- D-06: `IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md` — DR-01..12.
- D-07: `ARTIFACT_RELEASE_FALSIFICATION_CHECKLIST_20261029.md` — AR-01..14.
- D-08: `REPORT_HISTORY_PERSISTENCE_FALSIFICATION_CHECKLIST_20261029.md` — RH-01..14.
- D-05: `ADAPTER_BOUNDARY_DECISION_GATE_20261029.md` — PBR-01..07 and PF-01..05.
- Coordinator: `COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md` — COORD-01..12.
- Envelope: `ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md`.
- Owner state: `OWNER_DECISION_REGISTER_20261029.md`, `CONTROL_OWNERSHIP_AND_FALSIFICATION_MATRIX_20261029.md`, `SEMANTIC_DECISION_CROSSWALK_20261029.md`.

## Final status

No direct contradiction found in this documentation pass; residual ambiguities A-G remain explicitly unresolved. All new gates are recommendations, not approved implementation decisions. No tests or workloads were run. No provider, store, runtime, account, billing, merge, or deployment action was performed. Canonical acceptance and PR #2/#3 are not modified.


## Provider-neutral boundary contract sketch — 2026-10-29
See [PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md](PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md). It defines proposed operations and typed outcomes for atomic reservation, dispatch-intent/reconciliation, trusted evidence acceptance, append-only report publication, artifact publication/release, retention, and hard stops. It is a review sketch only: not a frozen schema, implementation, provider/store selection, or proof of any guarantee. All integration evidence remains NOT RUN.


## Boundary proof-level review checklist — 2026-10-29
See [BOUNDARY_PROOF_LEVEL_REVIEW_CHECKLIST_20261029.md](BOUNDARY_PROOF_LEVEL_REVIEW_CHECKLIST_20261029.md) for the focused proof-level matrix and six concrete blockers covering provider “not created” semantics, the actual policy barrier, report/artifact commit recovery, retention and identity namespaces, release-time authorization/byte integrity, and owner-open D-01..D-04. This is a review aid only; it adds no new approval or implementation evidence.
