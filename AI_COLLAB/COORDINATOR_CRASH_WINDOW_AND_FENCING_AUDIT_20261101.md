# PocketCode: Coordinator Crash-Window, Fencing and Replay Audit

**Date:** 2026-11-01  
**Status:** Read-only design falsification. SPECIFIED ONLY / NOT IMPLEMENTED / NOT RUN.  
**Scope:** Review the provider-neutral operation sketch, adapter envelope, fake-adapter tests, recovery checklist and artifact/report publication rules for crash windows, concurrent workers, stale actors and replay safety. This is not canonical acceptance and approves no provider, store, schema or implementation.

## 1. Executive finding

The existing design correctly prohibits blind redispatch after ambiguous start and requires durable reservation, dispatch intent, provider lookup, immutable evidence and idempotent report append. However, the conceptual interface is not yet sufficient to specify safe concurrent coordinator behavior.

The largest missing contract is **fencing of stale workers**. The sketch discusses worker leases and recovery, but does not define a monotonic reservation/attempt generation or fencing token that every mutating coordinator operation must present and that the durable authority validates. Lease expiry alone cannot stop an old worker from resuming and writing stale state after a recovery worker has taken over.

A second gap is that the provider idempotency token is named, but its full namespace, retention horizon and concurrent-call semantics are not bound to the attempt. A stable token helps only if the provider guarantees repeated and concurrent Start calls with that token cannot create distinct operations.

A third gap is that fake tests need explicit stale-worker and crash-after-each-commit-point cases. Current DR and COORD plans cover many failure scenarios, but do not fully test stale lease holders attempting dispatch, event append, terminal transition, report publication or artifact publication after takeover.

## 2. Findings

### F-01: No explicit fencing token or epoch in coordinator mutation interfaces

The boundary sketch includes a reservation version in dispatch-intent commit, and the recovery checklist says lease timeout permits reconciliation rather than a second start. But it does not define a monotonic worker/claim epoch, nor require every later mutation to prove it still owns the current epoch.

Failure scenario:
1. Worker A claims an attempt under lease epoch 4.
2. A pauses long enough for its lease to expire.
3. Worker B claims reconciliation under epoch 5 and resolves provider state.
4. Worker A resumes with stale state and attempts Start, accepts evidence, or publishes a report/artifact.

A database lease check performed only when the lease is acquired does not fence subsequent external or storage operations. A process-local lock is not a fence.

Required resolution:
- Define a monotonically increasing claim epoch/fencing token per job/attempt (name illustrative).
- Every coordinator state mutation must compare the supplied epoch with the currently committed epoch inside the same transaction as the mutation.
- A stale epoch must not append accepted evidence, alter disposition, publish a manifest or authorize release.
- External Start is harder: the provider must enforce stable-token idempotency and, if possible, a provider-side generation/precondition. If it cannot enforce fencing, the coordinator must prove only one Start caller can cross the boundary and preserve UNKNOWN on ambiguity. A database lease alone does not fence an external side effect.
- Recovery workers may take over lookup/reconciliation using a newer epoch; this must not allocate a new attempt or provider token.

Proposed tests: stale worker after lease expiry; stale worker resumes during lookup; two workers race to claim; stale worker attempts every mutating operation; process pauses after final local check but before provider call.

**Status:** DESIGN GAP. D-06 remains OPEN. No implementation or persistence test exists.

### F-02: Provider idempotency token lacks full namespace and lifetime binding

The sketch requires a stable provider token and asks for provider scope, retention horizon, concurrent request behavior and same-token result semantics. It does not yet specify a canonical mapping from internal identity to provider token namespace or a retention inequality.

Required resolution:
- Bind provider account/project/region (or equivalent provider namespace), adapter/version, internal tenant/job/attempt and token derivation version.
- Document whether token uniqueness is global, account-scoped, project-scoped or endpoint-scoped.
- Document provider retention and whether token expiry permits a second operation.
- Require the safe reconciliation/retry horizon to end before provider deduplication expires, or keep the attempt non-retryable after that point.
- Define concurrent same-token calls and same-token/different-payload behavior.
- Never regenerate a token when resuming an ambiguous attempt.
- Keep credentials and sensitive token material out of reports/logs.

A locally stable token is not proof of provider idempotency. If the provider does not guarantee same-token behavior for the full retry horizon, UNKNOWN remains non-retryable automatically.

**Status:** CONTRACT GAP. D-06 remains OPEN; provider not selected.

### F-03: Dispatch-intent crash windows need one explicit call-order table

The sketch distinguishes crash before dispatch-intent commit from crash after commit, correctly stating that missing acknowledgement is not evidence that no call occurred. Exact semantics of RESERVED, DISPATCH_INTENT and the external call still need one authoritative transition table.

| Window | Durable fact | External call possible? | Recovery |
|---|---|---:|---|
| Before reservation commit | No committed reservation known | No, if ordering is enforced | Revalidate and atomically reserve |
| After reservation, before dispatch intent | Reservation exists | No, only if protocol forbids earlier call | Claim attempt; validate policy; commit intent |
| After dispatch intent, before Start invocation | Intent exists | Cannot safely infer no call after crash | Lookup same provider token; no blind Start |
| During Start / acknowledgement lost | Intent exists | Yes | Lookup/reconcile same token |
| Provider accepted, local acknowledgement not committed | Operation may exist | Yes | Lookup same token; persist recovered operation |
| Acknowledgement persisted, terminal evidence absent | Provider operation known | Yes, active or unknown | Lookup same operation; no new attempt |
| Terminal evidence accepted, report not published | Evidence durable | No new start | Recompute/append using stable projection identity |
| Report committed, caller acknowledgement lost | Report may exist | No new start | Lookup same append operation ID |
| Artifact object written, manifest not committed | Object may be orphaned | No release | Reconcile or quarantine orphan |
| Manifest/report cross-store commit ambiguous | Partial publication may exist | No release | Reconcile stable publication operation; show pending/unknown |

Because a crash immediately after intent but before call is indistinguishable from a crash immediately after call unless provider idempotency/lookup resolves it, the safe default remains reconciliation, not redispatch.

### F-04: Fencing must extend to event acceptance and report/artifact publication

The sketch says accepted evidence is persisted before projection and report versions are immutable. It does not explicitly say a stale worker cannot append late events or publish stale projections after a newer worker has advanced the attempt.

Required resolution:
- Bind accepted event append to current attempt state version/epoch using compare-and-swap or an equivalent transaction.
- Preserve legitimate late provider observations as evidence, but distinguish accepting a real late event from permission to perform a stale state transition.
- Recompute projections from durable accepted evidence and current state version. A stale worker must not publish a report based on an older evidence watermark.
- Bind manifest publication to the exact committed report/evidence version and publication operation ID.
- Release must load the latest committed lifecycle/quarantine state, not trust a cached projection.

**Status:** DESIGN GAP. D-04, D-07 and D-08 remain OPEN.

### F-05: Separate all event, projection, report and publication identities

The sketch already distinguishes append operation ID from report version ID. The coordinator design should also distinguish source event identity, coordinator event identity, projection/recompute request identity, report append operation identity, immutable report version identity and cross-store publication operation identity.

A retry of one operation must not be mistaken for a new evidence event or logical report version. Conversely, a new accepted observation or schema/rules version must not be suppressed as a duplicate merely because the job ID is unchanged.

Proposed tests: same append ID/same canonical content; same append ID/changed content; same evidence set/recompute same schema; same evidence set/new projection schema; new evidence/new version; concurrent recomputes; acknowledgement loss after commit.

### F-06: Artifact release needs exact-byte and range-transfer semantics

The release sketch requires digest/size verification against exact immutable bytes and records bytes sent, transfer completion and integrity verification. It correctly notes already-sent bytes cannot be recalled. Before implementation, define whether full digest verification occurs before any bytes are sent, or whether a trusted immutable object version and storage checksum are relied on during streaming.

Required resolution:
- Prefer immutable version-addressed objects with trusted digest/size recorded at publication.
- Verify the exact version and digest before releasing bytes, or specify the storage checksum guarantee and how it binds to the returned stream.
- If streaming hash verification occurs only after bytes are sent, the API cannot claim the recipient received verified bytes until transfer completion. Partial transfer must be marked incomplete/unverified.
- Metadata HEAD followed by mutable-path GET is insufficient due to TOCTOU.
- Define range requests, aggregate byte limits and whether a range response is independently verifiable.
- Reauthorize at the chosen release snapshot/lease boundary; document revocation semantics during long transfers.

**Status:** DESIGN DETAIL OPEN. D-07 remains OPEN; no store/API selected.

## 3. Minimum state-transition contract before implementation

1. Every logical job and attempt has one durable authoritative record and monotonic state version.
2. Every worker claim/takeover has a monotonically increasing fencing epoch.
3. Every state-changing transaction checks expected state version and fencing epoch atomically.
4. Reservation identity, attempt identity and provider token are stable across recovery.
5. Dispatch intent is durable before any provider Start call.
6. Once dispatch may have occurred, only lookup/reconciliation is allowed unless provider-enforced same-token idempotency explicitly makes repeated Start safe.
7. Provider NOT_FOUND is not definitive unless provider contract proves consistency and retry semantics.
8. Evidence acceptance authenticates producer and binds tenant/job/attempt/source/policy before immutable append.
9. Legitimate late evidence can be appended, but stale workers cannot overwrite newer derived state.
10. Report projection is rebuilt from an identified immutable evidence watermark and versioned schema/rules.
11. Report append, artifact publication and release each use separate stable operation identities and reconciliation rules.
12. Artifact release binds current authorization, current lifecycle state, exact immutable object version and exact byte integrity.
13. Every ambiguous commit has a stable lookup identity. No retry generates a new operation ID to escape uncertainty.
14. Every unresolved ambiguity remains visible as UNKNOWN/PENDING and blocks dependent actions.

## 4. Proposed additional falsification cases

Do not allocate canonical LOOP/CASE IDs or duplicate COORD/DR/AR/RH IDs until traceability is refreshed.

| Case | Setup | Required assertion | Evidence layer |
|---|---|---|---|
| STALE-01 | Worker A lease expires; B claims newer epoch; A resumes | A mutations rejected; no stale dispatch or projection | Coordinator + persistence |
| STALE-02 | A pauses after local pre-dispatch check; B takes over before A calls provider | Provider idempotency/fencing prevents duplicate start, or system remains blocked/UNKNOWN; DB lease alone is not proof | Provider integration |
| STALE-03 | Two workers concurrently claim same attempt | One current epoch; stale claimant cannot mutate | Persistence concurrency |
| STALE-04 | Stale worker submits valid late provider event | Event may be authenticated/appended once, but stale worker cannot rewrite current projection | Ingress + persistence |
| STALE-05 | Stale worker publishes report/manifest after newer evidence version exists | Publication rejected or reconciled against exact current evidence watermark | Persistence + cross-store |
| TOKEN-01 | Provider token expires while local attempt unresolved | No new token/start; preserve UNKNOWN or manual recovery | Provider contract/integration |
| TOKEN-02 | Same provider token submitted concurrently with identical payload | At most one provider operation; same identity returned | Provider integration |
| TOKEN-03 | Same provider token reused with changed payload | Provider rejects conflict or coordinator blocks | Provider integration |
| TOKEN-04 | Token namespace differs by project/account/region | Mapping prevents accidental collision or cross-scope lookup | Adapter + provider integration |
| PUB-01 | Crash after artifact object write before manifest commit | Object remains unservable; orphan reconciled/quarantined | Store integration |
| PUB-02 | Crash after manifest commit before report publication acknowledgement | Stable publication operation recovers one consistent state | Cross-store integration |
| REL-01 | Object metadata verified, mutable key replaced before GET | Immutable version/checksum prevents different bytes being sent as verified | Store/API/HTTP |
| REL-02 | Range download fails after partial bytes | transfer_complete=false; no claim of fully verified download | API/HTTP |
| REL-03 | Authorization revoked during long transfer | Behavior matches documented snapshot/lease/revocation contract | API/HTTP |

## 5. Recommended priority

Before implementation, extend the existing coordinator/recovery design with: worker fencing epochs and state-version compare-and-swap; provider idempotency namespace and retention contract; exact dispatch-intent crash/call-order table; stale-worker rules for event/report/artifact transitions; immutable report evidence watermark and publication operation identity; exact-byte/range-transfer semantics.

Do not choose a provider or store just to fill these fields. If no $0 provider can provide the necessary policy barrier, idempotency and authoritative lookup semantics, reject that provider rather than weakening the guarantees.

## 6. Source pins and evidence limits

Reviewed pinned documents on branch pocketcode-execution-boundary-crosswalk-2026-11-01:
- PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md: 16985f50a0302ac5c55798445705971807eb5661
- ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md: 7d75b6844815570dd9faf1cd75791ba0abac33c1
- COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md: 214bb4aaffe002f95323be3dcab4c6cdd924f28c
- IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md: 534ba2b67ee7227b3e02a7a27d74ff6b2ba9e158
- CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md: 428897fb54e02c0dc27e987efa7a9690706c9732

This is static design review only. No implementation changed, no tests/workloads ran, no provider/store/runtime was selected, no account/billing action occurred, and no PR was merged or deployed.