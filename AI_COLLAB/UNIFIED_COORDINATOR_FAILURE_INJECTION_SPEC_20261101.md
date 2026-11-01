# PocketCode — Unified Coordinator Failure-Injection and Durable Transition Specification

**Date:** 2026-11-01  
**Status:** Design synthesis / proposed test specification only. NOT IMPLEMENTED / NOT RUN.  
**Branch:** `pocketcode-execution-boundary-crosswalk-2026-11-01`  
**Purpose:** Reconcile existing DR-01..12 and COORD-01..12 tests with report-history, artifact-release and new fencing/token/publication findings. This document does not create or renumber canonical LOOP/CASE acceptance IDs, close owner decisions, select infrastructure, or authorize implementation, workloads, spending, merge or deployment.

## 1. Verdict and non-negotiable rules

The existing design has the right broad safety direction but is not yet a complete concurrent state-transition contract. In particular, a lease is not a fence, a fake provider is not proof of provider idempotency, a report append is not artifact publication, and a historical PASS is not a current download authorization.

The coordinator must preserve these rules:

1. One authenticated tenant scope, logical job identity and attempt identity follow every transition.
2. The durable authority, not a worker's memory or client request, decides the current state and fencing epoch.
3. Reservation and dispatch intent commit before any provider start call.
4. After dispatch intent, uncertainty is reconciled against the original attempt. No blind redispatch.
5. Every mutating coordinator operation is conditional on the current fencing epoch and expected state/version.
6. Policy expected/applied evidence is bound at the actual dispatch boundary. A request fingerprint is not proof of applied policy.
7. Accepted raw observations are immutable and scoped before event reduction.
8. Execution outcome, job disposition, report verdict, cleanup, output collection, artifact state and release decision remain separate facts.
9. Report versions are immutable and append identities are distinct from event identities and reservation identities.
10. Artifact release revalidates current authorization, quarantine, scope and exact immutable bytes at the release boundary.
11. Any unresolved durable commit, provider call, event append, report append or publication remains UNKNOWN/PENDING and is reconciled by its original operation identity.
12. Fake tests establish branching and call order only. Real durability, provider, HTTP transfer and device claims require their respective integration evidence.

## 2. Identity namespaces that must not collapse

| Identity | Scope / purpose | Must not be substituted by |
|---|---|---|
| tenant/principal | Authenticated ownership scope | Client-supplied tenant ID |
| idempotency key + request fingerprint | Logical request deduplication | Correlation ID or report append ID |
| job ID | Stable logical job | Provider operation ID |
| attempt ID | One intended execution attempt | Worker ID or retry count |
| reservation version | Optimistic state version | Worker lease timestamp |
| fencing epoch/token | Current worker/claim authority | Lease expiry alone |
| provider idempotency token | External start deduplication | Internal job ID without namespace contract |
| provider operation ID | Authoritative external operation | Client-generated ID |
| source namespace + source event ID | External event replay identity | Coordinator event ID |
| coordinator event ID + sequence | Accepted immutable event identity/order | Provider sequence without binding |
| append operation ID | Idempotent report/evidence append request | Event ID |
| report version ID/number | Immutable user-facing projection | Mutable latest-report pointer |
| publication operation ID | Cross-store object/manifest/report reconciliation | Report version ID alone |
| artifact ID + manifest version + object version + digest | Exact artifact content identity | Mutable path or filename |
| release decision ID | Current caller authorization and release attempt | Historical execution PASS |

Each namespace needs explicit uniqueness scope, retention horizon, conflict behavior and audit evidence. A single generic `operation_id` is insufficient unless a typed namespace is part of its immutable value.

## 3. Proposed durable state machine

Names are illustrative, not frozen schema/API values.

| State | Durable meaning | Permitted next actions | Forbidden actions |
|---|---|---|---|
| `VALIDATED` | Authenticated request and bounded schema validated; no reservation yet | Atomic reserve | Provider call |
| `RESERVED` | Unique tenant/key/fingerprint reservation and job/attempt identity committed | Bind expected policy; claim work | Start before dispatch intent |
| `POLICY_READY` | Required policy revision/evidence is available for conditional dispatch | Atomic policy barrier + dispatch-intent commit | Read-then-act dispatch |
| `DISPATCH_INTENT` | Original attempt and provider token durably committed before start call | Invoke original Start once, or reconcile | Allocate replacement attempt because of timeout/lease expiry |
| `DISPATCH_UNKNOWN` | Start may have reached provider; acknowledgement/commit uncertain | Lookup original token/operation; reconcile | New Start without authoritative definitive-not-created proof |
| `ACKNOWLEDGED` | Provider acceptance and operation identity durably bound | Poll/receive authenticated events | Change attempt binding |
| `RUNNING` | Authoritative evidence says same operation active | Observe, request cancel, reconcile | Treat client disconnect as terminal |
| `TERMINAL_OBSERVED` | One or more immutable terminal observations accepted | Reconcile contradictions; derive disposition | Delete/overwrite earlier observations |
| `CLEANUP_PENDING` | Execution terminal but cleanup not confirmed | Cleanup/reconcile | Artifact release requiring cleanup proof |
| `OUTPUT_COLLECTING` | Collection for exact attempt is underway | Persist collection evidence | Present incomplete collection as complete |
| `EVIDENCE_READY` | Required evidence set and scope validated | Derive projection | Synthesize missing exit/stream evidence |
| `REPORT_APPEND_PENDING` | Stable append operation ID and immutable projection candidate exist | Retry/reconcile same append ID | Generate a new append ID on lost acknowledgement |
| `REPORT_COMMITTED` | Immutable report version and evidence references durable | Artifact publication/release evaluation | Mutate prior version |
| `ARTIFACT_PREPARED` | Exact bytes/object version and manifest candidate staged, not yet releasable | Verify object and manifest; reconcile publication | Expose download |
| `PUBLICATION_PENDING` | Some cross-store writes may have committed | Inspect/reconcile by publication operation ID | Assume rollback or publish partial state |
| `PUBLISHED` | Report/manifest/object references are consistent and durable | Release-time authorization check | Treat publication as authorization |
| `RELEASE_DENIED` | Current release predicate failed | Preserve audit and allow later fresh decision if state changes | Rewrite historical execution result |
| `RELEASED` | Exact authorized immutable object version released to caller | Record transfer outcome | Claim full transfer if interrupted |
| `UNKNOWN_MANUAL_RECONCILIATION` | Authority cannot establish safe next state | Preserve identities/evidence; approved manual resolution only | Automatic redispatch or release |

A real implementation may use fewer persisted labels, but it must preserve these semantic distinctions and prove transitions atomically.

## 4. Transaction and external-call boundaries

The coordinator design must identify which authority commits each boundary. The table below is a required failure-injection plan, not a claim that a particular database/provider has these capabilities.

| Boundary | Required durable precondition | Crash/lost-ack ambiguity | Safe recovery |
|---|---|---|---|
| A. Atomic reservation | Authenticated tenant, key, fingerprint and schema version | Commit response may be lost | Read/reconcile by same tenant/key; do not create a second logical job |
| B. Worker claim | Current state/version and next monotonic fencing epoch | Claim commit response lost | Read authoritative epoch; old worker is stale unless it owns current epoch |
| C. Policy barrier + dispatch intent | Expected policy revision, trusted policy binding, attempt and provider token | Intent commit response lost | Read by stable attempt/intent ID; no provider call until commit is known |
| D. Provider Start | Durable dispatch intent exists | Provider may accept even if response is lost | Lookup original provider token/operation; UNKNOWN if not authoritative |
| E. Provider acknowledgement | Provider operation ID and applied-policy evidence validated | Provider accepted but local acknowledgement not committed | Lookup same token and idempotently record same operation |
| F. Event ingress | Authenticated producer, tenant/job/attempt/policy binding, source identity | Event store commit response lost | Reconcile same source identity and immutable payload; do not append duplicate logical event |
| G. Terminal reconciliation | All raw terminal observations retained | Projection update may be lost | Recompute from immutable event set under current fencing epoch |
| H. Cleanup | Exact attempt and cleanup operation identity | Cleanup may have happened but ack lost | Query/retry same idempotent cleanup operation; remain UNKNOWN until confirmed |
| I. Output collection | Attempt, stream identity, collector version and byte limits | Partial object/stream may remain | Mark PARTIAL/UNKNOWN; resume only if exact byte/offset semantics are safe |
| J. Report append | Stable append operation ID, evidence snapshot, expected report version | Append may have committed while ack lost | Query by append ID; return same immutable version or reconcile conflict |
| K. Artifact object write | Stable publication operation ID, digest, size, object version semantics | Object may exist without manifest | Verify exact object version/digest; do not expose |
| L. Manifest/report publication | Immutable manifest/report refs and publication operation ID | One store may commit while another fails | PENDING/RECONCILING; idempotently complete or quarantine; never infer atomicity |
| M. Release authorization | Authenticated current principal and exact manifest/object version | Authorization/quarantine may change during transfer | Apply documented release lease/revocation semantics; record bytes sent and completion separately |
| N. Transfer completion | Exact object version, expected digest/size, transfer ID | Client disconnect or stream failure | PARTIAL/ABORTED; never report complete download |

## 5. Fencing contract

A worker lease is a liveness hint. It does not revoke code already running in an old worker. Every successful claim must advance a monotonic per-attempt fencing epoch (or equivalent unforgeable generation). Every coordinator mutation must present the epoch and be atomically rejected unless it equals the current durable epoch and the expected state/version.

At minimum, enforce fencing for:
- dispatch-intent commit and provider-start authorization;
- accepted event append and event-to-attempt binding;
- terminal reconciliation and disposition projection;
- cleanup state changes;
- output collection completion;
- report append/version publication;
- artifact object/manifest publication;
- release decision creation where a worker acts on behalf of a caller.

A stale worker may still receive authentic late provider events. Do not discard authentic evidence merely because the delivering worker is stale. Instead, authenticate and accept the source event through the trusted ingress boundary, then let the current coordinator epoch reconcile it. The stale worker must not be allowed to mutate current projections or publish artifacts.

A database fencing epoch cannot stop an external provider call already in flight. Provider-side idempotency and operation lookup remain separately required. The Start adapter must be called only after the durable conditional dispatch-intent operation returns a committed authorization for the current epoch. If a stale process can bypass this coordinator gate and call the provider directly, fencing is not established.

**Minimum falsification:** worker A claims epoch 7; its lease expires; worker B claims epoch 8 and reconciles; worker A resumes and attempts each protected mutation with epoch 7. All stale writes must fail, provider Start count must remain unchanged, and authentic late provider evidence must remain ingestible through the trusted ingress path.

## 6. Provider idempotency token contract

A token is useful only with a provider guarantee. Before selecting any provider, document and test:

- namespace: provider account/tenant, project, region, operation type and adapter version;
- binding: internal tenant/job/attempt, request fingerprint and policy revision;
- retention: minimum guaranteed deduplication horizon and exact expiry semantics;
- same-token concurrency: simultaneous Start calls return one operation or a documented conflict, never two jobs;
- same-token changed-payload behavior: reject conflict, never silently create a second operation;
- lookup: authoritative visibility, consistency delay, cross-region behavior and definitive-not-created semantics;
- token expiry: behavior when the provider may still be running but its deduplication key has expired;
- secrecy: tokens are opaque, non-credential identifiers and are not logged as secrets or exposed to clients.

If token retention expires while the original outcome remains unresolved, retain UNKNOWN. Do not mint a replacement token or start a replacement attempt automatically. An ordinary 404/not-found, timeout, stale cache or eventual-consistency gap is not proof of non-creation.

## 7. Fencing and publication test matrix

The following IDs are **proposed extensions**, not canonical acceptance IDs and not replacements for DR/COORD IDs.

| Proposed ID | Fault injection | Required durable result | Provider call count / allowed recovery | Forbidden result | Proof level |
|---|---|---|---|---|---|
| STALE-01 | A(epoch n) resumes after B(epoch n+1) takeover and tries dispatch-intent mutation | A rejected as stale; B remains authority | No extra Start; B reconciles | A writes intent or starts | Fake + persistence concurrency |
| STALE-02 | Stale A appends event after B takeover | Authentic source event accepted only through trusted ingress; stale projection mutation rejected | No Start; B recomputes | Drop authentic event or let A overwrite projection | Pure + authenticated ingress/persistence |
| STALE-03 | Stale A attempts terminal/disposition/report mutation | Current projection unchanged; stale write conflict recorded | Recompute under B epoch | Stale terminal overwrites current state | Fake + persistence |
| STALE-04 | Stale A publishes object/manifest after B takeover | Publication rejected or quarantined pending current-epoch reconciliation | No release | Stale manifest becomes downloadable | Persistence + artifact-store integration |
| STALE-05 | Race: B takes over while A's external Start call is in flight | Same original token/attempt reconciled; epoch alone does not imply provider call cancellation | At most one provider operation under provider contract | B starts a new token because A lease expired | Provider integration |
| TOKEN-01 | Same token, concurrent Start calls | One provider operation identity or documented safe conflict | One operation; lookup same token | Two provider jobs | Provider integration |
| TOKEN-02 | Same token reused with changed immutable payload | Provider/coordinator conflict | Zero additional operation | Silent changed-payload execution | Fake + provider integration |
| TOKEN-03 | Token expires while outcome remains ambiguous | Original attempt remains UNKNOWN | Lookup/manual reconciliation only | New token/attempt auto-start | Provider contract + persistence |
| TOKEN-04 | Provider lookup is delayed/eventually consistent and says not found | Remain UNKNOWN until documented authoritative threshold | Lookup original token | Treat transient not-found as definitive | Provider integration |
| PUB-01 | Crash after object write but before manifest commit | Object remains private/unpublished; publication pending | Verify exact object and resume same publication ID | Download link exposed | Artifact-store integration |
| PUB-02 | Manifest commit succeeds but report pointer update/ack is lost | Reconcile both stores by publication ID; no duplicate version | Idempotently complete/reconcile | Partial state represented as committed | Persistence + artifact integration |
| REL-01 | Authorization revoked after report PASS but before release | Current release denied; historical PASS unchanged | Fresh auth check | PASS used as bearer release token | HTTP/API integration |
| REL-02 | Object replaced or bytes change between metadata check and transfer | Exact immutable object version/digest mismatch denied before disclosure where possible | Re-fetch/verify exact version | Mutable path treated as same artifact | Artifact-store/HTTP integration |
| REL-03 | Mid-transfer disconnect, range retry or auth/quarantine change | Transfer PARTIAL/ABORTED or governed by explicit lease policy; bytes sent recorded | Resume only same immutable version and authorized range | Claim full transfer or recall already-sent bytes | HTTP integration |

## 8. Crosswalk to existing inventories (preserve original meanings)

### Existing canonical acceptance
- `LOOP-01..14` and `CASE-01..16` remain defined only by `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` and its traceability document.
- This specification adds no canonical LOOP/CASE IDs and does not relax their scope.
- CASE-13 remains the canonical ambiguous-network retry scenario; it does not prove durable reservation or provider idempotency by itself.
- CASE-16 remains out-of-order completion identity; it does not prove fencing without stale-worker mutation tests.

### Existing coordinator fake-adapter cases
- `COORD-01..04`: trusted PASS gates, cleanup vs program failure, no fabricated exit, contradictory terminal events.
- `COORD-05`: attempt binding before reduction; overlaps identity spine and event ingress.
- `COORD-06`: policy revision barrier; remains blocked on actual dispatch-boundary semantics.
- `COORD-07..08`: lost acknowledgement and UNKNOWN lookup; overlap DR-05..10.
- `COORD-09`: release-time artifact revalidation; overlaps REL-01..03 and artifact checklist.
- `COORD-10`: outcome/disposition/output collection distinctions; D-01/D-03 owner decisions remain open.
- `COORD-11..12`: scoped replay/collision diagnostics and immutable event snapshot.
- COORD fake tests do not establish durable storage, provider semantics, authenticated HTTP or device behavior.

### Existing ambiguous-dispatch recovery
- `DR-01..03`: atomic tenant-scoped reservation, changed fingerprint conflict and tenant isolation.
- `DR-04`: crash after reservation before intent.
- `DR-05..08`: intent/provider call/acknowledgement ambiguity and authoritative lookup.
- `DR-09..10`: lease expiry and restart after acceptance.
- `DR-11`: terminal evidence scope binding.
- `DR-12`: tombstone and retention behavior.
- New STALE/TOKEN cases extend these; they do not replace or renumber them.

### Report history and artifact release
- Report-history checklist invariants remain: immutable issued versions, monotonic per-job versioning, idempotent append, evidence identity, projection separation, atomic publication, concurrent-writer safety, crash recovery and retention.
- Artifact-release checklist remains conditional on an artifact actually existing and being requested. Artifact-free successful tasks can remain valid.
- Execution verdict, artifact state and release decision are independent. Historical PASS does not authorize release.
- New PUB/REL cases sharpen publication crash windows, exact-byte identity, transfer semantics and authorization races. They do not turn artifact production into a universal PASS requirement.

## 9. Owner decisions versus engineering/test design

The following are not to be silently decided by implementation:

| Decision | Why it is an owner/contract question | Safe interim behavior |
|---|---|---|
| D-01 limit-caused verdict | Whether confirmed runtime limit termination projects FAIL or INCOMPLETE | Preserve raw limit/termination facts; do not PASS; leave mapping unresolved |
| D-02 provider-error projection | User-facing disposition for provider failure without child exit | Preserve provider failure and absent exit; no fabricated exit |
| D-03 required output streams/partial capture | Which streams are mandatory per case and whether partial capture can satisfy it | Use per-case requirement; never make optional streams universal gates |
| D-04 authenticated event identity/replay contract | Trusted producer namespaces, source IDs, scope, ordering and conflict rules | Reject unbound events; preserve conflicts; no trust in client-supplied scope |
| D-05 applied-policy barrier | Atomic expected-to-applied policy binding at actual dispatch | BLOCKED; zero provider calls absent proof |
| D-06 durable idempotency/recovery | Store and provider semantics for uniqueness, tokens, lookup and expiry | UNKNOWN on ambiguity; no blind redispatch |
| D-07 artifact release | Exact object, manifest, authorization and transfer semantics | Fail closed; no release without exact current proof |
| D-08 durable report history | Store, immutable versions, append identity, atomicity and recovery | Do not claim durable history from in-memory helper |

Engineering may define pure test vectors, fake call-order assertions, typed internal outcomes, crash points and evidence capture. It must not choose a provider/store, claim production guarantees, alter canonical acceptance or close owner decisions by implementation convenience.

## 10. Required evidence and acceptance gates

| Gate | Evidence required | What it can establish | What it cannot establish |
|---|---|---|---|
| G0 contract consistency | Canonical IDs crosswalked without remapping; decision register current | Stable design vocabulary | Implementation correctness |
| G1 pure helpers | Strict validation, canonical fingerprint, immutable snapshots, deterministic reducers/projections | Logic on supplied fixtures | Authentication, persistence, provider behavior |
| G2 fake coordinator | Exact call order/count, no dispatch on barrier failure, stale epoch rejection, retry same IDs | Orchestration branches under scripted responses | Real atomicity/provider semantics |
| G3 persistence | Concurrent reservation, fencing CAS, restart, append IDs, version monotonicity, retention and crash injection | Selected store guarantees in tested conditions | Provider-side deduplication or runtime isolation |
| G4 provider | Same-token concurrency/retention, authoritative lookup, policy binding, real lifecycle | Selected provider contract in tested conditions | Other providers or untested regions |
| G5 artifact/API | Immutable object version, manifest consistency, authorization race, exact bytes, range and partial transfer | Release and transfer boundary | Device UI behavior |
| G6 device/product | Supported iPhone flow, honest status, file import/export, copy/report/history | Product acceptance on tested devices | Hidden server security guarantees |
| G7 operational/cost governance | Explicit permission, no-cost/limits evidence, audit and rollback/reconciliation plan | Authorized operational scope | Automatic permission for future workloads |

Promotion is boundary-specific. A PASS at G2 must never be described as G3/G4/G5 proof.

## 11. Minimum coordinator mutation contract

Every mutation should be conditional on:
- authenticated tenant scope (or a trusted system principal with explicit authority);
- job and attempt identity;
- current fencing epoch;
- expected durable state and version;
- operation-specific stable identity (dispatch intent, source event, append, publication, cleanup or transfer);
- relevant policy revision and immutable evidence references;
- idempotent same-identity/same-content replay behavior;
- explicit conflict behavior for same identity with changed content.

A failed conditional write returns a typed conflict/stale/unknown result. It must not be caught and converted into a generic success. Unknown commit acknowledgement is resolved by querying the same operation identity, not by issuing a new logical operation.

## 12. Stop conditions

Stop and retain BLOCKED/UNKNOWN if:
- no durable authority can atomically validate fencing epoch and expected state;
- a stale worker can directly invoke Start or publish outside the coordinator gate;
- provider token namespace, retention or concurrent-call semantics are undocumented;
- provider lookup cannot authoritatively distinguish accepted from not-created;
- policy is checked separately from the dispatch authorization boundary;
- source events can be accepted without authenticated scope binding;
- nested event payloads remain caller-mutable after acceptance;
- report append identity/version is not durable and idempotent;
- report/manifest/object publication can expose partial state;
- a mutable artifact path is used instead of an exact object version/digest;
- release uses historical PASS or stale authorization;
- partial transfer is represented as complete;
- a fake-only test is used to claim provider, persistence, HTTP or device guarantees.

## 13. Source pins refreshed on the active branch

All paths below were fetched from `pocketcode-execution-boundary-crosswalk-2026-11-01` at base commit `d60f9b84bce3afa48f7258f54526269ab87b4cc3` immediately before authoring this synthesis.

| Source | Blob SHA |
|---|---|
| `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` | `c6714c27db52b2962fe8d1c7e6a16829d46a8338` |
| `AI_COLLAB/CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md` | `d236962b3a58b98e96fad22ef5c2c23a7a61d54b` |
| `AI_COLLAB/COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md` | `214bb4aaffe002f95323be3dcab4c6cdd924f28c` |
| `AI_COLLAB/IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md` | `534ba2b67ee7227b3e02a7a27d74ff6b2ba9e158` |
| `AI_COLLAB/REPORT_HISTORY_PERSISTENCE_FALSIFICATION_CHECKLIST_20261029.md` | `8d665bd5b650fe00dd8133a729b13cca7cb523eb` |
| `AI_COLLAB/ARTIFACT_RELEASE_FALSIFICATION_CHECKLIST_20261029.md` | `2db8b0d9dff6b58d3200030f2730332a61dd15a4` |
| `AI_COLLAB/PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md` | `16985f50a0302ac5c55798445705971807eb5661` |
| `AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md` | `7d75b6844815570dd9faf1cd75791ba0abac33c1` |
| `AI_COLLAB/BOUNDARY_PROOF_LEVEL_REVIEW_CHECKLIST_20261029.md` | `2fba0c980a9644a7e9e40e03c2adb19b45399843` |
| `AI_COLLAB/COORDINATOR_CRASH_WINDOW_AND_FENCING_AUDIT_20261101.md` | `109465eecc9bd335541632d7a945a52a2aa85500` |
| `AI_COLLAB/END_TO_END_TRUST_CHAIN_GAP_MATRIX_20261101.md` | `659913f33a238b24b9c1116575d242a2eb026c4a` |

## 14. Current evidence status and next implementation sequence

- This document is a design/test specification only.
- No coordinator, persistence store, provider adapter, artifact store or release API has been implemented or validated by this work.
- No tests or workloads were run. All proposed STALE/TOKEN/PUB/REL cases are NOT RUN.
- D-05 remains BLOCKED; D-06..D-08 remain unproven at real boundaries.
- Canonical LOOP/CASE acceptance is unchanged.
- PR #2, PR #3, implementation branches and default branch were not modified.

When implementation is separately authorized, proceed in this order:
1. Resolve D-01..D-04 owner semantics and freeze the internal evidence contract without changing canonical meanings.
2. Specify exact typed state transitions and operation identities, including fencing epoch and token retention.
3. Build pure tests for type/schema, event snapshots, identity collisions, outcome/disposition/output distinctions.
4. Build fake coordinator tests for COORD-01..12 plus STALE/TOKEN/PUB/REL branch logic and exact call counts.
5. Select a durable store only after requirements are testable; prove G3 with concurrency, restart and crash injection.
6. Select a provider only after token/lookup/policy contracts can satisfy G4.
7. Prove report and artifact publication and release at G5.
8. Run device/product acceptance at G6.
9. Obtain explicit operational/cost authorization before any real workload or deployment.

**Decision:** this consolidated specification is the current coordinator test-design baseline. It is not an implementation approval or a claim of end-to-end readiness.
