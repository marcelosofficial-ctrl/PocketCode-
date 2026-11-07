# Durable adapter contract: PocketCode recovery and publication

**Status:** Proposed, adapter-neutral contract.  
**Decision:** No database, storage engine, backend, cloud host, provider or runtime is selected.  
**Scope:** Translate the tested in-memory recovery, journal, receipt and artifact semantics into a future durable adapter without changing product or security boundaries.

## 1. Purpose and non-goals

The in-memory models now cover reservation, lease/fencing, dispatch intent, ambiguous-send reconciliation, accepted event provenance, typed execution/report observations, immutable receipt revisions, artifact integrity/quarantine, current authorization checks and retryable report publication.

The next implementation must preserve those semantics across process interruption, concurrent workers, app restarts and storage recovery. A durable adapter must not be treated as production-ready merely because records survive a normal restart.

This contract does not select or implement SQLite, PostgreSQL, Redis, a file database, cloud object storage, a provider, model, runtime, execution host, transport, cryptographic algorithm, credential store, signing authority, policy service or mobile framework.

## 2. Identity and authority model

Keep these identifiers distinct and immutable:

- CommandId: user/assistant request identity.
- EffectId: one logical external effect.
- DispatchAttemptId: one authorized dispatch attempt for that effect.
- ExecutionId: one actual execution instance.
- ObservationSequence: coordinator-assigned append order.
- ResultReceiptId plus receipt version: one immutable result snapshot.
- ArtifactId plus object version: one immutable byte object.
- PublicationAttemptId: one attempt to copy/share an existing receipt.

A retry of the same logical effect may reuse the same EffectId and DispatchAttemptId only after the exact-scope reconciliation contract authorizes it. A genuinely new attempt requires a new DispatchAttemptId and explicit authorization. A fencing token is a monotonically increasing lease generation, not a replacement for any of these IDs.

Producer identity must be verified by a trusted adapter before journal append. A database row, payload digest, source string or caller-constructible producer object is not cryptographic authentication. The durable adapter must bind verified issuer, subject, key status, authorized source, audience and revocation policy to the accepted event.

## 3. Atomic transaction boundaries

The following state changes must be atomic within one transactional authority. If a future design spans independent stores, use a durable outbox/inbox protocol and expose intermediate state explicitly. Do not claim cross-store atomicity.

### T1. Effect reservation

One commit must:
1. Insert or retrieve the exact EffectId plus DispatchAttemptId reservation.
2. Bind immutable request bytes and request fingerprint.
3. Enforce the idempotency key and reject a changed request under the same identity.
4. Append the initial attempt-bound effect_reserved event, or persist a durable outbox record that guarantees its eventual append.
5. Preserve the original creation timestamp across retries and repair.

A reservation replay returns the original reservation and original event identity. It must not create a second logical effect or silently change the request.

### T2. Lease claim and fencing

One commit must:
1. Compare current effect/attempt state and lease expiry.
2. Reject terminal, ambiguous or otherwise non-claimable states.
3. Increment the fencing token monotonically.
4. Record owner, lease expiry and claim observation.
5. Append the lease-claim event with the same fencing token.

Concurrent claimants must not both receive a valid current lease. A stale lease must fail every state-changing operation, even if the old worker resumes after a long pause.

### T3. Dispatch intent

Before any provider/network side effect:
1. Compare the supplied lease and fencing token against the current stored generation.
2. Persist dispatching and the exact request/idempotency identity.
3. Append the dispatch-intent event.
4. Commit successfully before sending.

A crash after this commit but before a provider response is an ambiguous-send state. Recovery must reconcile exact identity with the provider. It must not infer that no send occurred.

### T4. Acknowledgement and reconciliation

A confirmed acknowledgement must atomically validate the current lease/fence and attempt identity, persist the provider reference and acknowledgement observation time, and append the acknowledgement event.

If the process crashes between external acknowledgement and local commit, recovery must query/reconcile. It must not blindly resend.

A not-found response authorizes retry only if it is exact-scope for the same effect, attempt and request fingerprint; authoritative for the relevant provider operation; explicitly final rather than eventually consistent or provisional; and recorded with observation time, authority and reconciliation evidence.

Unknown, delayed, partial, non-authoritative or mismatched responses remain reconciliation_required.

### T5. Event journal append

Accepted events and quarantined conflicts are append-only. The append transaction must verify producer identity and source authorization, enforce source-scoped producer event identity, compare immutable payload bytes and occurrence timestamp for exact replay, enforce current fencing generation where relevant, assign a monotonic coordinator observation sequence, and store payload digest, occurrence time, observation time, producer provenance and effect/attempt/fence binding.

Exact replay returns the original accepted event. Changed payload, occurrence timestamp, scope, producer identity or fence generation is quarantined. Never overwrite the original event.

The pre-lease effect_reserved event is the only defined unfenced attempt-bound exception. It must be coordinator-originated, carry matching effect/attempt identity in its structured payload, and be restricted to that event kind. All worker-originated and post-lease effect events require the current fence.

### T6. Typed observations and verdict projection

Lifecycle, direct-child exit, program failure, collection and cleanup observations are separate typed facts. Each observation must be bound to the exact effect and attempt, bound to the current live lease/fence where required, attributed to a trusted producer class, and immutable after acceptance.

The projection must derive execution verdict and lifecycle disposition from accepted typed evidence. Collection and cleanup are separate receipt dimensions. A degraded collector or cleanup failure must not be rewritten as execution success, nor should execution PASS imply collection or cleanup completeness.

Caller-supplied labels that disagree with the projection are rejected. Missing or contradictory evidence fails closed to INCOMPLETE/unknown. Stale-fence terminal observations require reconciliation and cannot silently create a current PASS.

### T7. Receipt revision and artifact manifest

One commit must read a consistent accepted-evidence high-water mark for the exact effect/attempt; derive execution verdict, lifecycle, collection and cleanup fields from that evidence; bind each evidence reference to its immutable digest; bind every artifact manifest entry to exact EffectId, DispatchAttemptId, ArtifactId, object version, byte length and SHA-256; create the next immutable receipt version with a predecessor link and revision reason; and preserve all earlier receipt versions byte-for-byte.

A retry with the same revision key and same canonical content returns the same receipt. Reusing a revision key with changed content is a conflict. A later observation creates a new version; it never mutates an existing receipt.

The receipt must not claim that an artifact is releasable merely because it exists in a temporary directory or staging area.

### T8. Artifact staging and publication

Artifact bytes and receipt metadata may live in different physical stores, but the release contract must prevent a manifest from pointing at incomplete bytes.

Required sequence:
1. Allocate an immutable artifact/object identity.
2. Write to a non-public staging location.
3. Verify write completion, byte length and digest from the stored bytes.
4. Quarantine partial, mismatched or otherwise unverified content.
5. Commit the verified object version and receipt manifest reference.
6. Make the object addressable only through the release gate.

A crash before step 5 leaves an orphan staging object eligible for safe cleanup, not a published artifact. A crash after step 5 must allow exact read-back and digest verification. Never overwrite an existing object version.

### T9. Artifact release authorization and transfer reservation

A new download/share request must obtain a fresh trusted policy decision bound to principal and tenant; exact receipt ID and version; artifact ID and immutable object version; EffectId and DispatchAttemptId; operation scope (download or share); policy revision; expiry; and current revocation state.

One transaction must re-read the latest receipt version for the exact (EffectId, DispatchAttemptId), verify that the requested receipt is still latest and contains the exact immutable artifact object version, validate the fresh policy decision and artifact integrity/quarantine state, and persist a unique ReleaseGrant/transfer reservation. No artifact bytes may flow before this transaction commits. This commit is the authorization linearization point.

A receipt successor committed before the grant transaction causes the old-receipt request to be denied. A grant committed before a successor is an already-authorized release pinned to its receipt and object version; the successor affects later grant requests, not the historical grant. Whether a policy revocation cancels an already-started transfer is a separate explicit policy decision. Do not silently imply either retroactive revocation or unconditional continuation.

If a process stops after grant commit, recovery must locate the same grant and either resume, complete or explicitly cancel it according to current policy. It must not mint a second grant or re-authorize against a superseded receipt merely because the original response was lost. Record authorization, transfer-start, byte-count/digest and completion/client-receipt facts separately where available.

Do not cache a previous allow decision for a new request. Re-check artifact quarantine, receipt membership, object digest and current attempt. The persistence adapter cannot substitute for a real policy authority or producer authentication service. The in-memory model's synchronous `release_artifact()` return of `released` represents a completed byte-release operation, not a streaming transfer or durable grant.

The in-memory grant conformance model separately exposes `reserve_release()`, `start_release_transfer()`, `record_release_progress()`, `complete_release_transfer()`, `cancel_release_transfer()` and `get_release_grant()`. Its state progression is `reserved -> transferring -> completed`, with explicit cancellation from `reserved` or `transferring`. Reservation is idempotent within principal + tenant + request key and fingerprints the exact receipt, artifact, operation and authorization snapshot. Exact replay returns the original grant even if a successor receipt has since been created; a changed request under that key conflicts. A new key must pass the latest-receipt gate. Transfer restart returns the same grant; progress is monotonic and bounded by immutable artifact length; completion requires full recorded length and matching artifact digest; grant transition timestamps cannot move backwards. Completed grants cannot be retroactively cancelled. Cancellation is an explicit operation, not an automatic inference from receipt supersession or authorization revocation.

The conformance suite also composes reservation, partial transfer, receipt successor, lost-response replay, grant lookup, resume and completion in one scenario; it asserts that the original receipt/object binding and single grant survive the interruption. Grant lookup is scoped to principal + tenant + request key. Malformed non-primitive authorization fields and non-string operation values are rejected before fingerprint serialization or set membership, avoiding unhandled type errors in the model.\n\nThese APIs are a sequential in-memory state-machine model only. They do not prove atomic concurrent reservation, persistence, actual byte streaming, client receipt, observed transfer digest from a transport, crash-safe event append or a real revocation policy. In particular, the caller-supplied completion digest is compared with the staged artifact digest; it is not cryptographic evidence that a remote client received those bytes.

### T9A. Release-grant concurrency and crash contract

The detailed adapter-neutral contract is in [RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md](RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md). It is normative for candidate adapters and clarifies that T9's linearization point is the successful commit of one transaction containing the ReleaseGrant, initial immutable grant event and outbox row.

Receipt successor creation and grant reservation must serialize through a stable head row keyed by exact (EffectId, DispatchAttemptId). Locking only an existing receipt row or querying MAX(version) is insufficient to prevent phantom/fork races. A grant transaction must re-read that head, verify the exact latest receipt and immutable object version, validate a trusted bounded policy decision, claim the unique (tenant, principal, request key) idempotency identity, and atomically insert grant + event + outbox before commit. Bytes flow only after commit.

Concurrent same-key/same-fingerprint requests resolve to one grant; changed fingerprints conflict. A lost commit response is recovered by the same key. Outbox delivery is at-least-once with stable event IDs and idempotent consumers, not exactly-once. Transfer/outbox workers require monotonic fencing tokens on every state mutation; lease expiry alone is not protection. Fencing protects durable state but cannot retract bytes already sent, so stream exclusivity is a separate transport requirement.

The new packet defines the two valid receipt-successor/grant serialization outcomes, 15 deterministic adapter race/crash/fencing tests, open policy decisions and explicit exit criteria. These are requirements, not implemented guarantees. P36 remains sequential/in-memory; no durable concurrency or crash behavior is proven.

### T10. Report publication

Copy/share attempts are append-only records referencing an existing receipt. A failed clipboard/share operation may be retried against the same receipt ID/version. It must not rerun execution, create a new dispatch attempt or mutate receipt contents.

## 4. Concurrency and uniqueness invariants

A candidate adapter must provide equivalent guarantees to these constraints:

| Scope | Required invariant |
|---|---|
| Reservation | Unique EffectId plus DispatchAttemptId and immutable request fingerprint |
| Provider event | Unique source plus producer_event_id within the declared producer scope |
| Journal | Monotonic observation sequence; append-only accepted and conflict records |
| Lease | Compare-and-swap current fencing token; one current owner/generation |
| Dispatch | At most one accepted intent per exact attempt/fence identity |
| Acknowledgement | Cannot be committed by a stale fence |
| Receipt | Unique EffectId, DispatchAttemptId and version; unique revision key |
| Receipt chain | New version points to the immediately preceding version in its chain |
| Artifact | Immutable ArtifactId/object_version with exact digest/size and effect/attempt binding |
| Release grant | Unique grant atomically bound to the latest receipt version, exact object version, principal/tenant and operation scope |\n| Publication | Append-only attempts keyed to the same receipt; no execution side effect |

A process-local mutex is not a substitute for cross-process concurrency control. The design must survive two workers racing on different devices or processes.

## 5. Crash/recovery matrix

| Crash point | Durable fact that must exist | Recovery behavior |
|---|---|---|
| Before reservation commit | No reservation | Safe to retry reservation |
| After reservation commit | Reservation plus event/outbox | Return same reservation; repair only missing event |
| After lease commit | New fence and owner | Old worker is stale; current owner may continue |
| After dispatch-intent commit, before send | Intent exists, send may or may not have happened | Reconcile exact provider identity before retry |
| After send, before acknowledgement commit | Ambiguous external effect | Reconcile; never assume absence |
| After provider acknowledgement, before local commit | Provider may have accepted | Query/reconcile and persist original provider reference |
| During event append | Either no event or one complete immutable event | Idempotent retry; never partial payload |
| During receipt creation | Either no new version or one complete version | Retry same revision key; never mutate predecessor |
| During artifact write | Staging object may be partial | Quarantine or remove staging object; do not expose |
| After artifact verification, before manifest commit | Verified orphan object | Reconcile manifest; do not expose until committed |
| After receipt/artifact commit, before clipboard/share | Receipt and artifact remain available | Retry publication using same receipt |
| Before release-grant commit | No transfer grant exists | Re-authorize against the then-current latest receipt; send no bytes |\n| After release-grant commit, before transfer completion | One immutable grant pins receipt/object version | Recover the same grant; apply explicit revocation/cancellation policy; do not create a second grant |

The adapter must expose enough state to distinguish not committed, committed but response lost, ambiguous external effect, and committed and verified.

## 6. Required adapter conformance tests

Before a storage candidate is accepted, run the same semantic tests against it, then add:
1. Two-process reservation race with same and different fingerprints.
2. Two-worker lease claim race and stale-worker write attempts.
3. Crash injection before/after every transaction boundary above.
4. Process kill during journal append, receipt revision and artifact manifest publication.
5. Restart/recovery with pending outbox events and orphan artifacts.
6. Reconciliation with final absence, eventual-consistency not-found, provider outage and mismatched identity.
7. Concurrent receipt revision attempts and predecessor-chain validation.
8. Artifact byte tampering, truncated writes, object-version substitution and stale authorization.
9. Backup/restore, migration interruption and integrity verification.
10. Re-run all canonical PocketCode tests without remapping LOOP/CASE/D IDs or weakening CASE-04.\n11. Race receipt revision against release-grant creation; prove exactly one linearization order wins and no stale grant is issued.\n12. Test object-version rollover, latest-manifest omission, response loss after grant commit, resumed transfer identity, and revocation of an already-started transfer under the explicitly selected policy.

A harness that mocks the adapter is useful for unit testing but is not evidence of durable behavior. Record exact storage version/build, runtime, filesystem, transaction settings, commands, commit SHA and test results.

## 7. Storage evaluation gate

Only consider a candidate after the semantic contract is stable. Score candidates against atomic transactions and conditional writes; cross-process concurrency and fencing; crash recovery and durable commit guarantees; append-only history and uniqueness enforcement; mobile/offline constraints and backup/restore; artifact blob strategy and integrity verification; migration safety, operational complexity and zero-cost default; version pinning and known crash/data-loss advisories.

If SQLite is evaluated, require a version/build containing the WAL-reset fix (3.51.3 or a supported backport) and verify the actual linked runtime, not merely the development package version. This is a guardrail, not a decision to select SQLite.

No candidate is selected by this contract. Do not add a database, paid service, cloud host or provider as a side effect of writing or reviewing it.

## 8. Security boundary reminders

Hashes detect byte changes relative to a known digest; they do not prove producer authenticity. The in-memory AuthenticatedProducer and ReleaseAuthorization types are caller-constructible test values. A durable adapter must sit behind trusted identity/policy verification, not replace it. Stock mobile WASM/Pyodide is not a hostile-code sandbox. Untrusted execution still requires disposable externally constrained isolation, default-deny permissions/egress, quotas, secrets separation and cleanup. PocketCode and RevDev retain separate repositories, roadmaps, clients, adapters, runtimes, security boundaries, acceptance suites and release gates.

## 9. Implementation decision gate

The next engineering step is to map each T1–T10 transaction to the candidate adapter's primitive operations and prove conformance with crash/concurrency tests. Storage selection requires a separate evidence-backed decision. Until then, the in-memory models remain semantic references only.
