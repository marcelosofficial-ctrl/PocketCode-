# P39 implementation-gate research addendum

**Date:** 2026-11-09  
**Scope:** External primary-source research to sharpen the existing P39 owner/reviewer gate. This is a design-evidence addendum, not an owner decision, implementation authorization, stack selection, or production claim.

## 1. Ranked gaps

1. **P39 review and owner-decision gate:** the safe path to implementation is to reconcile Gemini's independent review and explicit OD-01..OD-13 decisions. These are governance blockers, not coding tasks.
2. **Atomic grant, receipt-head and outbox commit:** current sequential models cannot prove multi-process serialization, durable atomicity, crash recovery or ordered relay behavior.
3. **Policy revocation at commit, claim and byte-transfer boundaries:** revoking a credential does not prove every server has observed the revocation or that an already-started transfer stopped.
4. **Exit provenance and termination proof:** child exit, wrapper result, timeout request, process termination, cleanup and artifact disposition are separate facts. A renderer cannot safely infer one from another.

## 2. Atomic grant, receipt head and outbox

### Verified external evidence

- **AWS Prescriptive Guidance, transactional outbox:** the dual-write failure exists when a database update and event notification are separate operations. AWS recommends writing the outbox row in the same transaction, expects duplicate delivery, recommends idempotent consumers, and calls out event ordering and rollback behavior. Opened 2026-11-09: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html
- **Debezium Outbox Event Router:** the official documentation describes an insert-oriented outbox table with a unique event ID and an aggregate key. The event ID can support deduplication; the aggregate key preserves ordering within Kafka partitions. Its router expects INSERT operations and filters DELETE operations. Opened 2026-11-09: https://debezium.io/documentation/reference/transformations/outbox-event-router.html
- **Debezium maintenance/version:** the official release page listed 3.7.1.Final as latest stable on 2026-11-09, released 2026-11-06, and 3.8.0.Alpha1 as development, dated 2026-11-02. Code is Apache License 2.0; Debezium trademarks remain separately protected. Sources: https://debezium.io/releases/ and https://debezium.io/license/
- **PostgreSQL 18 transaction semantics:** current official documentation says SERIALIZABLE may abort a transaction with serialization_failure when concurrent read/write dependencies cannot be serialized. Applications must retry the whole transaction. The docs identify PostgreSQL 18 as current and PostgreSQL 19 RC 1 as a development release as of 2026-11-09. Opened 2026-11-09: https://www.postgresql.org/docs/current/sql-set-transaction.html
- **PostgreSQL row locking:** FOR UPDATE locks selected rows against conflicting writers/lockers until transaction end. It does not create a lock on a not-yet-existing receipt-head row. Opened 2026-11-09: https://www.postgresql.org/docs/17/explicit-locking.html

### Adaptation for PocketCode

The existing concurrency contract's stable head anchor is the right abstraction to preserve. Keep it storage-neutral. The important invariant is not "use a particular lock API"; it is that receipt-successor creation and grant reservation serialize through the same durable anchor, and that the first anchor is created under a unique key so two initializers cannot both win.

The grant, initial grant event and outbox record must commit atomically. The relay is at-least-once, not exactly-once. Give each event a stable ID, each aggregate a monotonic version, and each consumer a durable deduplication record. Do not mark a future aggregate version consumed before its predecessor is applied. Relay lease ownership must be fenced at the delivered-mark write, not only at claim time.

A database's SERIALIZABLE label is not sufficient evidence by itself. The selected adapter must run deterministic two-connection/process races and crash injection against its actual schema, isolation level, migration and deployment topology. Retry SQLSTATE 40001 by restarting the complete transaction with the same request identity; do not retry only the last statement or generate a new idempotency key.

### Reuse and licence decision

Debezium is a useful implementation reference, not a PocketCode dependency recommendation. Its Apache-2.0 code licence is permissive, but its outbox router is coupled to change-data-capture infrastructure and Kafka-oriented event routing. No code was copied. Do not add Debezium, Kafka or PostgreSQL to the product stack from this research. The current $0 constraint and unselected-stack decision remain in force.

## 3. Revocation and in-flight transfer

### Verified external evidence

- **IETF RFC 7009, OAuth 2.0 Token Revocation:** this is a 2013 Standards Track RFC. It specifies token invalidation, but explicitly acknowledges propagation delay where some servers know about revocation while others do not. Clients must stop using a token after a successful revocation response. Opened 2026-11-09: https://www.rfc-editor.org/rfc/rfc7009
- **Amazon S3 presigned URLs:** AWS documents that expiration is checked when the HTTP request begins. A large download started before expiration can continue after expiration; a dropped connection cannot be restarted after expiry. A presigned URL can be used multiple times until expiration. Opened 2026-11-09: https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-presigned-url.html
- **Google Zanzibar paper:** the 2019 USENIX paper describes authorization decisions that respect causal ordering of user actions and object changes, providing external consistency. This is a research precedent, not a PocketCode-ready service or licence grant. Opened 2026-11-09: https://research.google/pubs/zanzibar-googles-consistent-global-authorization-system/

### Adaptation for PocketCode

Do not describe token revocation as instantaneous global cancellation. Separate at least four events: policy revocation committed, a worker/transport observes the new policy epoch, the transport stops accepting or emitting further bytes, and termination/cancellation is acknowledged. Bytes already delivered cannot be recalled. Server-emitted bytes do not prove client-observed or client-acknowledged bytes.

If OD-01 keeps streaming out of MVP, do not build a stream-revocation subsystem now. The MVP should stage a complete immutable artifact, verify its digest and quarantine state, then expose a bounded handoff with clearly stated expiry semantics. Do not imply that expiry cancels a download already in progress. If streaming is later approved, require a stream-scoped capability, a defined policy-consistency boundary, bounded chunk/range authorization, separate byte counters, and same-attempt cancellation acknowledgement. A worker fence alone cannot retract bytes emitted by a stale worker.

Zanzibar's causal-consistency lesson supports binding decisions to a policy revision/epoch and making the commit boundary explicit. It does not justify choosing Zanzibar, a hosted authorization service, or a distributed database.

## 4. Exit provenance, termination and recovery

### Verified external evidence

- **OpenTelemetry CLI semantic conventions:** the opened CLI page describes process name, PID and process.exit.code separately, and classifies nonzero process exit as an error for CLI execution spans. The page labels the CLI conventions Development, while the general error-recording conventions are separate. Treat this as telemetry vocabulary, not a complete job-verdict contract. Opened 2026-11-09: https://opentelemetry.io/docs/specs/semconv/cli/cli-spans/
- **Kubernetes Pod lifecycle:** normal termination attempts TERM with a grace period, then KILL for remaining processes. Forced deletion removes the API object without waiting for kubelet confirmation; Kubernetes warns the process may continue running indefinitely. Thus an API deletion or cancellation request is not proof of process termination. Opened 2026-11-09: https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/
- **Temporal workflow history:** Temporal documents a complete ordered event history as the source of truth for replay. Workflow code is replayed against recorded events; external side effects belong in Activities, whose recorded results are reused during replay. This is a durable-history pattern, not a guarantee that arbitrary external side effects are exactly once. Opened 2026-11-09: https://docs.temporal.io/workflows
- **Temporal licence and maintenance signal:** the Temporal server repository identifies an MIT licence. The official organization repository listing showed active repositories updated in September 2026; the current workflow docs were opened on 2026-11-09. No exact latest server release was verified in this pass. Sources: https://github.com/temporalio/temporal and https://github.com/orgs/temporalio/repositories

### Adaptation for PocketCode

Keep the typed coordinator projection and pure renderer boundary. Preserve raw child observation, wrapper observation, termination cause, termination acknowledgement, cleanup/evidence state and artifact disposition as separate fields. The coordinator resolves the verdict from trusted evidence; the renderer displays that resolved projection and does not authenticate or reclassify it. The existing two-field helper must not be patched with precedence rules to force EP-04/05 into INCOMPLETE.

A timeout request, SIGTERM/SIGKILL request, wrapper exit, API object deletion or disconnected client is not, alone, proof that the child process stopped. Require a termination observation tied to the same ExecutionId and DispatchAttemptId. If it is absent, retain UNKNOWN termination and INCOMPLETE result; do not release artifacts whose policy requires confirmed termination/cleanup. Preserve CASE-04 as INCOMPLETE / timed_out.

Temporal demonstrates the value of a durable ordered history and replay-safe time. It is not a recommendation to adopt Temporal for PocketCode: it introduces a server/workflow platform that conflicts with the current unselected-stack and $0-default constraints unless a later cost and deployment review explicitly approves it. No Temporal code was copied.

## 5. Red-team corrections to prior work

1. **Branch-head drift:** an earlier STATE revision and intermediate checkpoint referred to e643d59 as current HEAD, while the live branch had advanced to 6a11dc2. The live branch API now verifies HEAD 6a11dc2b91daf046c96fce0094df7e41de0efbca. This addendum records the exact SHA and the latest five commits in the checkpoint.
2. **Duplicate INDEX row:** INDEX contained two rows for P39_SOURCE_PINNED_AUDIT_CROSSWALK_20261108.md. Keep one canonical row; the second description is merged into it.
3. **Revocation overclaim risk:** RFC 7009 allows propagation delay, and S3 explicitly permits an already-started download to continue after URL expiry. The safe wording is "stop future authorized transfer at the enforceable boundary"; never claim instant global cancellation or recall of emitted bytes.
4. **Telemetry-spec overreach:** OpenTelemetry CLI conventions are marked Development. They provide useful process attributes, not normative product semantics for wrapper/child contradictions, timeout, cleanup or artifact release. Keep EP verdict semantics in PocketCode's own versioned contract.
5. **Termination evidence gap:** Kubernetes force deletion may occur without confirmation that the process stopped. Keep cancellation request, process termination observation and cleanup completion distinct.

## 6. Bounded acceptance additions for a future authorized adapter

These refine existing RACE/CRASH/FENCE and EP cases. They do not create canonical LOOP/CASE/D IDs and are not authorization to implement.

| Proposed test | Required setup and assertion |
|---|---|
| P39-OUTBOX-01 | Commit grant, initial event and outbox row in one transaction; inject failure after each insert and before commit; assert either all three persist or none do. |
| P39-OUTBOX-02 | Publish event, crash before delivered mark, reclaim under a higher relay fence; assert duplicate delivery has one consumer effect and stale relay cannot mark delivered. |
| P39-HEAD-01 | Race two first-head initializers for the same EffectId/DispatchAttemptId; assert one stable head and one receipt root. |
| P39-HEAD-02 | Race grant reservation and receipt successor on independent processes; assert only the serialization winner's receipt can be granted. |
| P39-POLICY-07 | Revoke policy while a transfer is active; separately record revocation commit, transport observation, final emitted byte and cancellation acknowledgement. No claim of client receipt without client acknowledgement. |
| P39-TERM-01 | Issue cancellation/force-delete request while child remains alive; assert status remains termination UNKNOWN until same-attempt process termination evidence arrives. |
| P39-EXIT-01 | Child exits zero, wrapper collection fails; preserve child execution fact separately from overall evidence/artifact disposition. Expected overall verdict remains owner-gated under OD-10. |

All tests must use the P39- namespace to avoid P37/P39 collisions. Adapter tests require independent processes/connections and the real selected adapter; sequential fakes are insufficient.

## 7. Decision impact

- No OD-01..OD-13 decision is made by this document. Existing recommendations remain proposals.
- The review gate remains CLOSED pending Gemini's source-pinned review, any still-required Claude exit review, and explicit owner decisions.
- No provider, runtime, database, host, transport or workflow engine is selected.
- No source/test changes, no tests run, no new dependencies, no canonical IDs changed.
- Evidence status: external references above are VERIFIED by opening the cited primary sources; application-level conclusions are INFERRED design recommendations; real adapter, concurrent-process, device and transport behavior remain UNKNOWN / NOT RUN.

## 8. Source register: maintenance and licence checks

| Project/source | Evidence checked | Maintenance/version signal | Licence status | Use decision |
|---|---|---|---|---|
| Debezium | Official Outbox Event Router docs and licence page | 3.7.1.Final latest stable on 2026-11-09; 3.8.0.Alpha1 development | Code Apache-2.0; marks separately protected | Pattern reference only; no code copied |
| Temporal | Official workflow docs and server repository | Docs current when opened 2026-11-09; exact latest server release not verified | Server repository MIT | Event-history/replay reference only; no dependency or code copied |
| PostgreSQL | Official PostgreSQL 18 docs | PostgreSQL 18 current; 19 RC 1 announced 2026-10-15 | No code copied; database licence not relevant to this design-only review | Transaction semantics reference only; no database selected |
| RFC 7009 | RFC Editor Standards Track page | Published August 2013 | IETF standards text; no code copied | Normative revocation caveat |
| OpenTelemetry CLI conventions | Official semantic-conventions page | Convention page marked Development | Specification, not copied code | Vocabulary reference only |
| Kubernetes | Official current lifecycle docs | Current docs include Kubernetes 1.37 navigation | No code copied | Termination-proof counterexample |

**Verification:** research/documentation only. No source or test files changed or executed.
