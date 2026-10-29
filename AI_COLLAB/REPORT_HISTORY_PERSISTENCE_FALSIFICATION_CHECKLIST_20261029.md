# PocketCode — Durable Report History and Append-Concurrency Falsification Checklist

**Status:** Research/test specification only. NOT RUN. No persistence store, coordinator, provider, or schema selected. This is not canonical acceptance and authorizes no implementation/deployment.

## Purpose

D-08 defines what must be demonstrated before PocketCode may claim report history is durable, append-only, correctly ordered, and recoverable after concurrent updates or process failure. The existing in-memory ReportHistory model is not proof of persistence, transaction isolation, atomic versioning, or tamper resistance.

## Proposed invariants — owner review required

1. **Issued version immutability:** once a report version is issued, its canonical content and referenced evidence snapshot never change. New evidence creates a new version.
2. **Monotonic per-job versioning:** each job/attempt history has a durable, strictly increasing version/sequence assigned atomically. Concurrent writers cannot publish duplicate or reordered version numbers.
3. **Idempotent append:** retrying the same append operation/event ID does not create duplicate history entries; reusing an append identity with different immutable content is a conflict.
4. **Evidence identity:** each report version references the exact accepted evidence/event IDs and policy/release state used to derive it. Evidence cannot be swapped across tenant/job/attempt.
5. **Projection separation:** raw execution observations, job disposition, user-facing verdict, cleanup state, artifact release state, and collection completeness remain separate fields. A later cleanup/release update must not rewrite earlier execution facts.
6. **Atomic publication:** a report version is visible only when its content and evidence references are durable. Partial writes do not appear as complete versions.
7. **Concurrent update safety:** two writers appending terminal/reconciliation evidence cannot lose one another's observations. Use transaction, compare-and-swap, serializable sequence allocation, or equivalent documented primitive.
8. **Crash recovery:** after process crash at any write/publication boundary, recovery either sees the prior complete version or the new complete version—not a partial/ambiguous mixture. If atomicity cannot be proven, expose recovery as UNKNOWN.
9. **Deterministic recomputation:** given the same accepted evidence snapshot and versioned projection rules, the report projection is reproducible. Rule/schema version is recorded; recomputation creates a new version when it changes issued output.
10. **Contradiction preservation:** late or conflicting terminal evidence is appended and causes the documented conservative projection; it must not silently overwrite an earlier terminal event or delete conflict diagnostics.
11. **Retention and deletion:** report, evidence, idempotency, tombstone and artifact retention rules are explicit and coordinated. Deletion must not erase evidence still required for recovery, audit or owner-approved retention.
12. **Authorization and tenant isolation:** history lookup is tenant-scoped and reauthorizes current access. A report version or existence cannot be discovered through another tenant's IDs.
13. **Integrity:** store canonical bytes or a well-defined immutable representation with integrity checks; if tamper evidence is promised, define the threat model and mechanism rather than assuming ordinary database persistence is tamper-proof.
14. **Report/artifact consistency:** if report publication and artifact manifest publication span stores, use an explicit transactional/outbox/reconciliation protocol. Never expose a PASS report whose required artifact manifest is only partially published.
15. **Honest availability:** storage outage or unresolved commit acknowledgement cannot be described as durable success. Reconcile by append operation identity; do not blindly append duplicates.

## RH-01..RH-14 — falsification cases

| ID | Setup / fault | Required assertion | Evidence boundary |
|---|---|---|---|
| RH-01 | Append first report, restart process/store client, read history | Previously acknowledged version and evidence references remain durable and content-stable | Persistence integration |
| RH-02 | Two writers concurrently append distinct evidence to the same job | Both observations retained; versions/sequence unique and monotonic; no lost update | Concurrent persistence integration |
| RH-03 | Same append operation ID retried with identical canonical content | One logical history entry/version; retry returns existing result | Persistence uniqueness/idempotency integration |
| RH-04 | Same append ID reused with changed evidence or projection content | Conflict; preserve original; do not silently replace prior version | Persistence integration |
| RH-05 | Append cleanup UNKNOWN then later cleanup CONFIRMED | Earlier report remains unchanged; later version records new cleanup evidence and recomputes only dependent disposition/release fields | Projection + persistence integration |
| RH-06 | Append contradictory late terminal event after an earlier terminal event | Both observations and conflict diagnostics retained; conservative projection is versioned; no silent PASS overwrite | Coordinator + persistence integration |
| RH-07 | Crash after content write but before version/index publication | Recovery does not expose partial report; orphan cleanup/reconciliation is explicit | Crash-injection persistence integration |
| RH-08 | Crash after version commit but before acknowledgement to caller | Caller retries with same append ID; existing committed version found, not duplicated | Persistence integration |
| RH-09 | Concurrent writers both read version N and attempt append | Atomic allocation/CAS makes one retry against new version or merges under defined ordering; no duplicate N+1 or lost event | Transaction/concurrency integration |
| RH-10 | Evidence/report reference points to another tenant/job/attempt or mutable payload | Reject; accepted snapshot is immutable and bound to exact evidence identities | Trusted ingress + store integration |
| RH-11 | Recompute under changed projection/schema version | New version identifies rules/schema used; historical version remains as originally issued | Projection/versioning integration |
| RH-12 | Report write succeeds but required artifact manifest write fails, or vice versa | No inconsistent published PASS/downloadable artifact; reconciliation resolves pending publication without fabricating success | Cross-store integration |
| RH-13 | Storage returns timeout after a possible commit; subsequent lookup unavailable | Do not blindly append with a new ID or claim durable commit; mark commit status unknown and reconcile original operation | Persistence failure-injection integration |
| RH-14 | Tenant authorization revoked, retention expires, or deletion requested while history is read/appended | Apply explicit policy; no cross-tenant disclosure; do not silently violate retention/evidence dependencies | Auth/retention integration |

## Suggested record model (illustrative, not frozen)

A future report version should identify tenant/job/attempt, report ID, monotonically assigned report version, append operation ID, accepted evidence/event IDs and immutable evidence snapshot/reference, projection/schema/rules version, raw execution outcome, job disposition, report verdict, cleanup state, collection state, artifact-release state, canonical report content digest, bounded creation metadata, publication/commit state, and unresolved reconciliation marker.

Do not make report version number alone an authenticity guarantee. Integrity, access control, storage semantics and provenance must be defined separately.

## Persistence and transaction questions

Before implementation, select and document:
- store technology and exact transaction/isolation/unique-index/CAS guarantees;
- uniqueness scope for tenant/job/attempt/report_version and append operation IDs;
- sequence allocation semantics under concurrent writers;
- atomicity between evidence append, report version, and artifact manifest publication;
- crash recovery and orphan cleanup strategy;
- retention/deletion rules for reports, raw evidence, idempotency records, tombstones and artifacts;
- whether tamper evidence is required, its threat model, and its mechanism;
- read consistency guarantees for report history on multiple devices;
- how to reconcile a commit whose acknowledgement was lost.

If these are unspecified, report-history durability remains BLOCKED/UNKNOWN.

## Stop conditions

Do not claim durable append-only history if the only model is in-memory; issued report objects are mutated in place; version assignment uses read-then-increment without atomicity; concurrent writes can overwrite one another; a lost commit acknowledgement causes a new append identity; evidence references are mutable or not bound to tenant/job/attempt; contradictory/late events overwrite earlier observations; partial cross-store publication can expose inconsistent report/artifact states; ordinary persistence is described as tamper-proof without a threat model; or fake-only tests are described as persistence/restart proof.

## Evidence ladder

- **PURE/UNIT TESTED:** projection determinism, append identity checks, version comparison.
- **FAKE-ADAPTER TESTED:** coordinator retry and projection branches with synthetic stores.
- **PERSISTENCE INTEGRATION TESTED:** transactions, uniqueness, concurrent writers, crash/restart and commit ambiguity.
- **CROSS-STORE INTEGRATION TESTED:** report/artifact manifest publication and reconciliation.
- **DEVICE ACCEPTED:** history list shows stable prior versions, later reconciliations, and honest unresolved states.

## Traceability

- D-08 in AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md.
- COORD-10/12 and AI_COLLAB/COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md.
- AI_COLLAB/IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md (D-06) for durable append operation identity and ambiguous acknowledgements.
- AI_COLLAB/ARTIFACT_RELEASE_FALSIFICATION_CHECKLIST_20261029.md (D-07) for consistency between report and artifact release.
- LOOP-09/10/11; CASE-11/12/13/16.

**Current result:** SPECIFIED ONLY / NOT RUN. No store or implementation selected; no tests, account, billing, workload, merge, or deployment action performed.


## Cross-decision audit pointer — 2026-10-29
See [CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md](CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md) for cross-boundary invariants, unresolved interface questions, and the proposed G0-G7 evidence gate sequence. This pointer does not close owner decisions or promote specification/fake-test evidence to provider, persistence, HTTP, or device integration evidence.
