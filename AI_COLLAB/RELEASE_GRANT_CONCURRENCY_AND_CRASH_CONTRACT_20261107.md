# Release-grant concurrency and crash contract

**Checkpoint:** PC-2026-11-07-P37  
**Scope:** Adapter-neutral transaction, interleaving, idempotency, outbox and fencing requirements for T9 release grants.  
**Status:** Design/conformance specification only. No durable adapter, database, distributed lock, provider or production authorization authority is implemented or selected.

## 1. Purpose and authority

P36 supplies a sequential in-memory state machine. It is useful as a semantic reference for request-key replay and transfer lifecycle, but its Python dictionaries and append-only lists do not serialize concurrent workers or survive a crash. This packet closes the design gap between that model and a durable implementation.

This contract refines T9 in `DURABLE_ADAPTER_CONTRACT_20261106.md`. It does not change canonical LOOP/CASE/D identifiers, the $0 default, mobile/runtime decisions, security boundaries or PR state.

## 2. Required linearization point

A new grant is authorized at one database commit, not when a handler begins, when a policy service returns, or when the first byte is sent.

Within one transaction, the adapter MUST:

1. Authenticate the caller outside the persistence adapter and obtain a trusted, bounded authorization decision bound to principal, tenant, exact receipt, artifact/object version, effect/attempt, operation scope, policy revision and expiry.
2. Lock or compare-and-swap a stable receipt-head row for the exact `(EffectId, DispatchAttemptId)`. The head row must exist independently of receipt versions. Locking only the current receipt row is insufficient because two workers can otherwise race to insert competing successors (a phantom/new-row race).
3. Re-read and validate the head and latest immutable receipt. The supplied receipt must equal the current head; the receipt manifest must contain the exact artifact ID and immutable object version; the artifact must be complete, digest-verified and not quarantined.
4. Validate the authorization decision's identity, scope, policy revision, expiry and revocation snapshot against the request. Do not accept a caller-constructed allow object as trusted authority.
5. Claim the unique idempotency identity `(tenant_id, principal_id, request_key)`. Store a canonical request fingerprint covering effect, attempt, receipt ID/version/hash, artifact ID/object version, operation scope and authorization decision identity/revision.
6. Insert the immutable ReleaseGrant, its initial `reserved` event and a durable outbox event in the same transaction. Enforce uniqueness on the idempotency identity and stable grant/event IDs.
7. Commit. Only after successful commit may transfer bytes be made available.

**The successful commit is the grant linearization point.** A failed or rolled-back transaction authorizes no bytes. A lost commit response is an ambiguous client observation, not evidence of rollback. The caller must query/replay the same idempotency identity.

### Stable receipt-head requirement

Maintain a stable serialization anchor keyed by `(EffectId, DispatchAttemptId)`, with current receipt ID/version (or an equivalent monotonic head token). Receipt successor creation and release-grant reservation must both update/read this same anchor under the same serialization rule.

Acceptable mechanisms include:
- row-level lock on the stable head row, then read/validate and update under the transaction;
- compare-and-swap on the head token, with retry on conflict;
- serializable isolation with verified predicate/phantom protection and retry handling.

A plain `SELECT MAX(version)` followed by an insert is not sufficient. A process-local mutex is not sufficient. The chosen engine's actual isolation semantics must be proven by a two-connection test, not inferred from API names.

## 3. Receipt-successor race: only two valid outcomes

Let R1 be the current receipt and R2 its successor. Let G1 be a proposed grant pinned to R1.

| Serialization winner | Required result |
|---|---|
| Grant transaction commits first | G1 is valid and permanently pins R1 plus the exact object version. R2 may then become current. R2 does not rewrite or retroactively invalidate G1. |
| Receipt-successor transaction commits first | The head now names R2. A new request for R1 must fail as stale. A grant may be created only after fresh authorization against R2 and its exact artifact manifest. |

No execution may commit a grant for R1 after R2 has won the shared head serialization point. No receipt chain may fork from R1 because a concurrent writer ignored the head token.

## 4. Idempotency and response-loss semantics

The database uniqueness constraint, not a prior read, arbitrates concurrent duplicate requests.

- Same principal + tenant + request key + same canonical fingerprint: one grant exists. All contenders resolve to that same grant ID and immutable binding.
- Same principal + tenant + request key + different fingerprint: conflict. Never overwrite or reinterpret the first request.
- Different tenant or principal: distinct idempotency namespace.
- A retry after a lost response looks up the committed grant before attempting a new reservation. It does not create a second grant and does not reinterpret the original request as a new grant against a later receipt.
- A replay response that returns an existing grant is not itself permission to restart bytes. Transfer continuation/revocation policy is checked separately and explicitly. The product must decide whether an existing in-flight grant may resume after policy revocation; do not smuggle that decision into idempotency behavior.
- Idempotency records and grant identity must be retained for at least the full retry/recovery horizon. Expiring a key while a transfer can still be retried can create a duplicate grant.

The current P36 model fingerprints a caller-supplied authorization snapshot. Production must fingerprint a trusted decision reference or verifiable signed decision, not trust caller-supplied fields.

## 5. Grant event and outbox atomicity

The grant row, initial immutable grant event and outbox row are one transaction. There is no valid durable state in which the grant is committed but its required initial event/outbox record is absent.

The relay is at-least-once:
- claim outbox work with a lease and monotonically increasing fencing token;
- publish a stable event ID and aggregate/grant version;
- mark delivered only if the relay still owns the current fence;
- consumers deduplicate by stable event ID and reject stale aggregate versions;
- a crash after publish but before delivered-mark may publish again; duplicate delivery is expected and must not duplicate the logical event/effect.

Do not claim exactly-once delivery. The achievable contract is atomic local intent plus at-least-once delivery plus idempotent consumers.

## 6. Transfer-worker fencing

If transfer work is leased to workers, every lease claim increments a monotonic fence for that grant. Every progress, completion and cancellation mutation includes the fence and performs a conditional write against the currently stored fence and permitted grant state.

A stale worker with fence n MUST be unable to mutate after a newer worker has claimed fence n+1, even if the stale worker resumes after a long pause. Lease expiry alone is not sufficient: the fence comparison is the authority. A worker that loses its lease must discard its result and re-read durable state.

The fence protects PocketCode's durable state. It cannot retract bytes already sent by a stale worker to a remote client. If concurrent transfer streams are prohibited, the transport layer must also bind/rescind stream ownership or use a single-use capability. This is a separate transport guarantee.

Progress updates are monotonic and bounded by the immutable object's length. Completion must bind the server-observed object digest and length. A caller-reported digest is not proof of client receipt. If client receipt matters, define a separate authenticated client acknowledgement with its own provenance and idempotency.

## 7. Crash-injection matrix

| Failure point | Durable outcome allowed | Recovery |
|---|---|---|
| Before transaction begins | No grant, event or outbox | New request may authorize against then-current receipt |
| After head lock, before inserts | No committed changes | Transaction rollback; retry |
| After grant insert, before event/outbox insert | No partial commit | Same transaction rolls back all writes |
| After all inserts, before commit | No committed changes | Rollback; retry with same key |
| Commit succeeds, response lost | One grant + reserved event + outbox | Lookup/replay same key; no second grant |
| Outbox relay crashes before publish | Pending outbox row | Another fenced relay claims and publishes |
| Relay publishes, crashes before delivered mark | Event may be delivered more than once | Consumer deduplicates stable event ID |
| Old relay resumes after new lease | No state mutation by old fence | Reject stale conditional update |
| Transfer worker crashes after partial progress | Grant and last committed progress remain | New worker claims higher fence and resumes under explicit policy |
| Old transfer worker resumes after takeover | No progress/completion write by old fence | Reject stale fence; transport must separately prevent duplicate streams if required |
| Receipt successor wins before grant commit | No grant against predecessor | Re-authorize against latest successor |
| Grant wins before receipt successor | Grant pins predecessor/object version | Later successor affects only new grants |
| Artifact object version changes | Existing grant remains pinned to old immutable version | Never silently substitute new bytes; new grant requires current receipt and new version |
| Revocation occurs after grant commit | Grant remains historically committed | Apply separately selected in-flight revocation policy; record decision/event |

## 8. Minimum adapter conformance suite

Run these against the real candidate adapter using independent connections/processes and deterministic barriers. A mocked repository or sequential fake is not sufficient.

1. **RACE-01 Grant vs successor, grant first:** pause grant after head lock, commit ordering deterministically, then allow grant commit. Assert one grant pinned to R1 and later R2 cannot mutate it.
2. **RACE-02 Successor vs grant, successor first:** commit R2 before grant obtains head. Assert R1 grant denied.
3. **RACE-03 Same-key same-fingerprint:** launch N concurrent requests. Assert one grant ID, one initial event and one outbox identity.
4. **RACE-04 Same-key different-fingerprint:** race different artifact/receipt/scope under same key. Exactly one fingerprint wins; all incompatible contenders conflict.
5. **RACE-05 Different principal/tenant:** same textual key in distinct namespaces does not collide or leak grants.
6. **RACE-06 Receipt successor writers:** two writers based on R1 cannot both create R2 branches. One succeeds; the other reloads/reconciles and must not silently fork.
7. **CRASH-01 Transaction rollback injection:** fail after each individual insert and before commit. Assert no partial grant/event/outbox state.
8. **CRASH-02 Lost commit response:** commit, suppress response, retry exact key. Assert original grant is returned.
9. **CRASH-03 Outbox duplicate delivery:** crash after publish before delivered mark. Assert repeated delivery has one logical consumer effect.
10. **FENCE-01 Stale transfer worker:** worker A owns fence n, worker B claims n+1, then A attempts progress, completion and cancellation. All A writes must fail.
11. **FENCE-02 Stale outbox relay:** old relay attempts delivered-mark after takeover. Conditional update must fail.
12. **ARTIFACT-01 Object-version substitution:** change current manifest/object version between requests. Old grant remains pinned; new grant cannot use stale version.
13. **POLICY-01 Revocation boundary:** test the explicitly chosen rule for revocation before grant commit and after grant commit/in-flight transfer. Record policy version and expected behavior.
14. **RECOVERY-01 Restart:** kill all workers, restart from durable state, reconcile pending outbox, grant state, leases and partial transfer without duplicate grants/events.
15. **INTEGRITY-01 Event chain:** verify event IDs, aggregate versions, grant binding, monotonic progress and immutable event payloads after recovery.

For each run capture adapter/build/version, isolation level, schema/migration revision, independent connection/process count, deterministic schedule/barrier trace, injected crash point, exact commit SHA and complete test output.

## 9. Decisions still required, not assumed

- Which trusted policy authority issues the release decision, and whether it supports revision-bound or short-lived decision verification.
- Whether policy revocation stops an already-started transfer, and how the transport prevents or handles bytes after revocation.
- Whether a grant may have multiple concurrent transfer workers/streams, or whether one active stream is enforced.
- Retention horizon for idempotency keys, grant events and outbox records.
- Whether client receipt is a product requirement or server-side transfer completion is sufficient.

These decisions do not block specifying the transaction shape. They do block claims of production authorization, revocation, or client-delivery guarantees.

## 10. Exit criteria before storage selection

A storage candidate is not accepted until it passes RACE-01 through INTEGRITY-01 on the actual mobile/hosted deployment topology, including restart and two-process contention. Pin the exact linked library/runtime build and transaction configuration. Run the canonical PocketCode suite unchanged. Record costs and operational burden against the $0 default. This specification does not select SQLite or any other database.

## 11. Current evidence boundary

**Implemented:** P36 sequential in-memory grant lifecycle and request-key replay model.

**Specified here:** shared receipt-head serialization, transactional grant/event/outbox insertion, database-arbitrated idempotency, at-least-once outbox, fencing and deterministic adapter conformance schedules.

**Not implemented or verified:** durable transactions, actual concurrent races, crash injection, outbox relay, leases/fences, trusted policy authority, streaming transport, client acknowledgement, storage selection or production behavior.
