# Release-grant adapter research, executable model and red-team corrections

**Checkpoint:** PC-2026-11-07-P39  
**Research checked:** 2026-11-07  
**Decision:** no database, queue, distributed lock, workflow engine, provider or hosted service selected.

## 1. Ranked gaps

| Rank | Gap | Why it matters | P39 deliverable |
|---:|---|---|---|
| 1 | Receipt-head serialization and grant reservation | A latest-receipt read followed by an independent write is a check-then-act race. | Executable CAS interleaving model and first-head bootstrap rule |
| 2 | Grant/event/outbox atomicity and ordered delivery | Atomic local writes do not prevent duplicate publication or event reordering. | Crash failpoints, stable event identity, gap deferral and ordered-consumer rule |
| 3 | Worker leases, fencing and external effects | Lease expiry does not stop a paused worker; fencing only works when the protected resource validates the token. | Executable worker takeover model and transport boundary |
| 4 | Idempotency versus authorization evidence | A rotating proof must not change request identity, but refreshed proof must authorize the exact same effect, receipt, object version and scope. | Exact proof-binding checks and stable-intent replay tests |
| 5 | Storage/workflow choice under phone-first/$0 constraints | Engine guarantees differ materially; a model cannot justify a database or hosted workflow choice. | Primary-source comparison and selection gates |

## 2. Primary-source research

Claims marked VERIFIED were checked against the linked primary source during this pass. INFERRED marks PocketCode design conclusions drawn from those guarantees.

### 2.1 Transaction isolation and compare-and-swap

**PostgreSQL 18**
- **VERIFIED:** PostgreSQL 18 documents Serializable transactions detecting dangerous read/write dependency patterns and aborting one transaction. Applications must retry the whole transaction after serialization failure. Explicit row locks protect selected rows against conflicting updates while the transaction holds the lock. Sources: [Serializable and explicit-lock consistency](https://www.postgresql.org/docs/18/applevel-consistency.html), [INSERT and ON CONFLICT](https://www.postgresql.org/docs/18/sql-insert.html), [SELECT locking clauses](https://www.postgresql.org/docs/current/sql-select.html).
- **VERIFIED:** INSERT ON CONFLICT DO UPDATE is documented as an atomic insert-or-update outcome under high concurrency when its unique arbiter is correctly defined. This helps idempotency-key arbitration but does not itself serialize a separate receipt-head read.
- **INFERRED:** A PostgreSQL adapter can use a stable head-row lock and re-read inside one transaction, or Serializable transactions with whole-transaction retry. Isolation level, unique constraints, lock order, retryable SQLSTATEs and failover behavior must be pinned and integration-tested.

**SQLite**
- **VERIFIED:** SQLite supports DEFERRED, IMMEDIATE and EXCLUSIVE transactions. BEGIN IMMEDIATE starts a write transaction immediately and can fail with SQLITE_BUSY if another writer is active. Source: [SQLite transaction control](https://sqlite.org/lang_transaction.html).
- **VERIFIED:** WAL allows readers and a writer to proceed concurrently, but only one writer can exist at a time. WAL requires participating processes on the same host and does not work over a network filesystem. Source: [SQLite WAL](https://www.sqlite.org/wal.html).
- **VERIFIED:** The WAL-reset bug affects WAL databases with concurrent connections and is fixed in 3.51.3 and later, with documented backports 3.44.6 and 3.50.7. The official WAL page was updated 2026-08-25. Source: [SQLite WAL-reset bug](https://www.sqlite.org/wal.html#the_wal_reset_bug).
- **VERIFIED:** SQLite core is public domain. Source: [SQLite copyright](https://www.sqlite.org/copyright.html).
- **INFERRED:** SQLite remains a plausible local/single-host candidate, not an automatic fit for a horizontally scaled worker fleet or cross-device shared database. A candidate must pin bundled SQLite build, journal mode, synchronous setting, filesystem and topology, then pass crash/reopen, busy-retry and two-connection race tests. Not selected.

**DynamoDB conditional-write pattern**
- **VERIFIED:** AWS documents optimistic locking through version attributes and conditional writes, transactions for atomic multi-item writes, and warns that global tables use last-writer-wins reconciliation, so ordinary optimistic-lock assumptions do not hold across Regions. Sources: [Optimistic locking](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BestPractices_OptimisticLocking.html), [version-control strategies](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BestPractices_ImplementingVersionControl.html), [conditional-write idempotence](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html).
- **INFERRED:** Reuse expected-version CAS and atomic multi-item transaction concepts, not the managed service. Pricing, region model and deployment assumptions remain unevaluated.

### 2.2 Transactional outbox and event identity

**AWS transactional outbox**
- **VERIFIED:** AWS describes the outbox as a remedy for database-write plus message-publish dual-write. Duplicate messages can occur, consumers should be idempotent, notification order should match database update order, and rolled-back transactions must not publish. Sources: [Transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html), [ordering and failure considerations](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html#issues-and-considerations).
- **INFERRED:** P37's atomic grant/event/outbox row is necessary but insufficient. Relay must not publish aggregate N+1 while N remains undelivered, unless the consumer durably buffers gaps and applies only contiguous versions. SKIP LOCKED may distribute independent queue rows, but aggregate ordering needs its own rule.

**CloudEvents**
- **VERIFIED:** CloudEvents identifies v1.0.2 as the latest released core spec and says the project is CNCF graduated. Its LICENSE is Apache-2.0. Sources: [Project and releases](https://github.com/cloudevents/spec), [v1.0.2 core specification](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md), [LICENSE](https://github.com/cloudevents/spec/blob/main/LICENSE).
- **VERIFIED:** CloudEvents requires source and id; producers ensure source+id uniqueness for distinct events, a resent duplicate may reuse the same ID, and consumers may treat identical source/ID as duplicates. Source: [Event identity](https://github.com/cloudevents/spec/blob/v1.0.2/cloudevents/spec.md#id).
- **INFERRED:** Use stable (source,event_id) for deduplication and aggregate version as a separate ordering coordinate. CloudEvents does not provide transport, authentication, ordering or exactly-once delivery.

### 2.3 Worker leases and fencing

**etcd**
- **VERIFIED:** etcd API guarantees document increasing revisions usable as a logical clock and explain that clients may be uncertain about operation status after timeout/network interruption. Sources: [etcd API guarantees](https://etcd.io/docs/v3.4/learning/api_guarantees/), [mutex implementation](https://github.com/etcd-io/etcd/blob/main/client/v3/concurrency/mutex.go).
- **VERIFIED:** etcd repository declares Apache-2.0 and showed a current main branch with substantial recent activity. Source: [etcd repository/license](https://github.com/etcd-io/etcd).
- **INFERRED:** The useful pattern is a monotonic revision/fencing token generated by the authoritative coordinator, not a timestamp or random lease ID. The protected resource must compare the token on every mutation. etcd itself adds an operational cluster and is disproportionate to an unvalidated $0 MVP.

**Redis**
- **VERIFIED:** Redis's own distributed-lock documentation recommends fencing tokens for long-running processes and warns not to assume a lease remains held merely because the client process is alive. It discusses clock drift and safety caveats. Source: [Redis distributed locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/).
- **INFERRED:** A TTL lock without a monotonic token checked by the protected state store is insufficient for grant, event or transfer correctness.

### 2.4 Durable workflow references

**Temporal**
- **VERIFIED:** Temporal describes ordered event history as the source of truth for workflow replay. Workflow code must be deterministic against recorded history; external side effects, API calls, database access and LLM calls belong in Activities. Activities can retry, so they must be idempotent. Sources: [Workflow replay](https://docs.temporal.io/workflows), [Activity idempotency](https://docs.temporal.io/develop/python/best-practices/error-handling).
- **VERIFIED:** Temporal server repository is public and declares MIT. The repository showed recent activity and releases when checked; no exact version is pinned because a version is not needed for semantic reuse. Source: [Temporal server repository/license](https://github.com/temporalio/temporal).
- **INFERRED:** Reuse ordered event history, deterministic projection and idempotent side-effect semantics. Defer the full server because it adds an operational service and persistence dependency before the first execution workflow is validated.

## 3. Reuse decision

| Project/pattern | Reusable lesson | Licence / maturity evidence | PocketCode decision |
|---|---|---|---|
| PostgreSQL 18 | Serializable retry, row locking, unique-key arbitration | PostgreSQL License; five-year major support policy | Future candidate only |
| SQLite WAL | Same-host local journal; one writer; busy/checkpoint behavior | Public domain; mature embedded engine | Local-device candidate only after actual mobile build is pinned |
| DynamoDB | Expected-version CAS and atomic multi-item writes | Managed commercial service | Reuse concepts, do not adopt service |
| AWS outbox | Atomic local state + outbox, at-least-once relay, idempotent consumer, ordering | Public design guidance | Adopt pattern, not AWS-specific service |
| CloudEvents v1.0.2 | Source-scoped event identity | Apache-2.0; CNCF graduated | Reuse identity semantics; SDK not needed yet |
| etcd | Consensus-backed revisions, lease/mutex | Apache-2.0; active repository | Learn fencing pattern; operationally heavy now |
| Redis lock pattern | Lease alone is insufficient; fencing must reach protected resource | Official Redis guidance with caveats | Not grant authority |
| Temporal | Event-history replay and idempotent Activities | MIT server; maintained project | Reuse concepts; defer server |

No source code was copied. The deliverable adapts documented semantics into PocketCode contracts and tests.

## 4. Red-team corrections to P37/P38

### RT-01: contradictory authorization fingerprint
**Prior weakness:** P37 step 5 said the fingerprint covered authorization decision identity/revision. P38 correctly changed the model to stable release intent, but P37 remained contradictory.

**Correction:** fingerprint exact effect/attempt, receipt ID/revision/hash, artifact ID/object version, operation scope and explicit share-target scope. Exclude rotating authorization ID, token expiry and policy revision. Still authenticate before lookup and require the current decision to bind the exact same principal, tenant, effect, attempt, receipt, artifact/object version and operation. Preserve first decision ID/revision as immutable grant provenance. Replay is not permission to send/resume bytes.

### RT-02: first receipt-head creation unspecified
**Prior weakness:** P37 required a stable head row but did not define race-safe initialization.

**Correction:** create initial head anchor and first immutable receipt in the same transaction under a unique (EffectId, DispatchAttemptId) key. A losing initializer reloads the winning head; it must not create another root.

### RT-03: outbox ordering ambiguous
**Prior weakness:** P37 said consumers reject stale versions but did not distinguish a delayed predecessor from a stale event.

**Correction:** relay claims are ordered per aggregate. N+1 cannot be claimed while N remains undelivered. A consumer receiving a future version returns retryable deferred_gap without marking it consumed. It applies only contiguous versions. Same source/event ID and same digest is duplicate; same identity with changed digest is conflict. Unknown event at or below the last applied version is stale/conflicting.

### RT-04: fence reset after deletion/recreation
**Prior weakness:** P37 required monotonic fences but did not forbid resetting after record recreation.

**Correction:** fence epoch remains durable and monotonic for the grant identity. Completed/cancelled grant identities and highest fence remain tombstoned for the recovery/audit horizon. Never recycle grant IDs or reset fences after deletion, restore or migration.

### RT-05: refreshed authorization and stream side effects
**Prior weakness:** stable-intent replay could be misread as permitting a differently scoped refreshed authorization. State fencing cannot stop a stale worker continuing an already-open stream.

**Correction:** refreshed decision must bind exact same immutable intent and scope. Every state mutation validates current fence and lease. Before bytes are sent/resumed, transport independently validates a current single-use or stream-scoped capability and enforces cancellation/revocation policy. Already-emitted bytes cannot be recalled. Client receipt remains a separate authenticated fact.

## 5. Executable P39 reference model

New files:
- scripts/release_grant_conformance.py
- scripts/test_release_grant_conformance.py

The model exposes receipt-head CAS and both legal receipt/grant commit orders; tenant/principal/request-key idempotency with stable intent fingerprint; refreshed proof replay preserving original provenance; exact authorization binding to effect, attempt, receipt, artifact, object version and operation; injected failures after staged grant, after staged event and before commit; worker expiry/fencing; bounded monotonic progress; source-scoped event dedupe, payload conflict and future-version gap deferral.

**Critical limitation:** deterministic sequential reference model only. It does not run two threads/processes or a database and does not prove crash durability, lock behavior, network stream cancellation or real relay ordering. It is a semantic oracle for CI; adapter-specific P37 race tests remain mandatory.

## 6. Adapter transaction recipe

1. Verify caller authentication and obtain a fresh trusted authorization decision.
2. Begin a transaction at a documented isolation level.
3. Ensure stable receipt-head anchor exists; initial anchor and first receipt creation must be unique and atomic.
4. Lock or CAS the stable head (EffectId, DispatchAttemptId), then re-read latest receipt and exact immutable object version.
5. Verify authorization binding to the exact stable intent. Do not put rotating proof fields into the idempotency fingerprint.
6. Claim unique (tenant_id, principal_id, request_key) and compare stable intent fingerprint. Same fingerprint returns original grant; changed intent conflicts.
7. For a new key, insert grant, immutable initial event and outbox row in this transaction.
8. Commit. Only then issue a transfer capability.
9. On ambiguous commit response, authenticate again and recover by the same key. Never infer rollback from timeout.
10. Worker claims durable higher fence. Every progress/completion/cancel mutation checks fence, lease expiry, grant state and object version.
11. Relay publishes only earliest undelivered event version per aggregate. Consumer applies contiguous versions and deduplicates (source,event_id).
12. Retain identity/fence tombstones and idempotency records for the full retry, recovery and audit horizon.

## 7. Adapter acceptance matrix

| ID | Required test | Pass condition |
|---|---|---|
| RACE-01 | Grant commits before successor | Grant pins predecessor receipt/object; successor then advances |
| RACE-02 | Successor commits before grant | Old-receipt grant rejected |
| RACE-03 | Two initial-head creators | One head/first receipt wins; loser reloads |
| RACE-04 | Two successor writers from same head | One CAS wins; no fork |
| RACE-05 | N same-key/same-intent requests | One grant, one initial event, one outbox identity |
| RACE-06 | Same key, different intent | One fingerprint wins; others conflict |
| RACE-07 | Same key in different principal/tenant | Independent namespaces, no cross-tenant read |
| CRASH-01 | Fail after each insert and before commit | No partial grant/event/outbox |
| CRASH-02 | Commit succeeds, response lost | Same-key retry returns original grant |
| CRASH-03 | Relay publishes then crashes before mark | Duplicate publish has one logical consumer effect |
| ORDER-01 | Aggregate N+1 arrives before N | N+1 deferred, not consumed; then applied after N |
| ORDER-02 | Two relay workers compete | N+1 cannot publish while N remains undelivered |
| ORDER-03 | Same source/id with changed payload | Quarantine/conflict, never overwrite |
| FENCE-01 | Old worker resumes after takeover | All old-fence state writes fail |
| FENCE-02 | Expired worker writes before takeover | Write rejected based on expiry/current lease |
| FENCE-03 | Grant restore/delete/recreate | Fence epoch cannot reset or grant ID be reused |
| FENCE-04 | Old relay marks delivered after takeover | Stale relay fence rejected |
| ARTIFACT-01 | Object version changes | Old grant stays pinned; new grant binds new head/version |
| POLICY-01 | Revocation before grant commit | Denied |
| POLICY-02 | Revocation after grant commit/in-flight | Explicit selected rule, no implicit behavior |
| STREAM-01 | Old worker continues stream after takeover | Transport capability/ownership prevents unauthorized continuation |
| RECOVERY-01 | Kill workers and restart | Durable state reconciles grants, progress, leases and pending outbox |
| INTEGRITY-01 | Rebuild projection from events | Event identity, digest, aggregate version and contiguous order verified |

Capture exact adapter build, DB engine/version, isolation config, schema migration, independent connection/process count, deterministic barrier schedule, crash point, commit SHA and complete test output.

## 8. Storage and workflow selection gate

No adapter is approved by this report. The first candidate must be chosen only after deployment topology is known.

- If strictly one-host/local-first with bounded write contention, SQLite can be tested. Pin a build at or above the documented WAL-reset fix if WAL is used; verify same-host placement, BEGIN IMMEDIATE/busy retries, synchronous durability, checkpoint behavior and process-kill recovery.
- If multiple independent server workers/hosts mutate state, test a server database or store with documented atomic conditional transactions and stable head. PostgreSQL is a strong candidate for evaluation, not a decision.
- Do not add Redis as sole correctness authority for grant/fence state.
- Do not add etcd solely to solve one row-level serialization problem.
- Do not add Temporal until the first bounded workflow proves it needs a separate durable workflow service beyond a database-backed journal/outbox.
- Do not use a queue's limited deduplication window as grant idempotency retention.
- Do not use network-mounted SQLite WAL files as a multi-host database.

Every candidate must pass the full P37/P39 adapter matrix on the actual topology, then run the canonical PocketCode suite unchanged. Cost and operator burden must remain consistent with the $0 default or require a separate owner decision.

## 9. Open decisions

1. Does policy revocation stop an already committed in-flight transfer?
2. Are concurrent transfer streams for one grant forbidden? How does transport enforce single-stream ownership?
3. Is authenticated client receipt required, or is server-side transfer completion sufficient for MVP?
4. What are retention periods for idempotency keys, grant events, outbox rows, lease epochs and tombstones?
5. Which trust service issues authorization decisions, and how are issuer, policy revision, audience, expiry and revocation verified?
6. Which execution/deployment topology is required by the first validated PocketCode workflow?

Until answered, the correct state is UNKNOWN / NOT SELECTED.
