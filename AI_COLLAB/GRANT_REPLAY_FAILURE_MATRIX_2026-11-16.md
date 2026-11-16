# Grant / outbox replay failure matrix
Date: 2026-11-16
Status: model-level acceptance design; no adapter, broker, database or runtime selected.

## 1. Purpose and boundary

This packet turns the existing grant transition and outbox model into a deterministic replay contract. It does not claim durable atomicity, transport delivery, authenticated producer identity, consumer inbox persistence, relay fencing, or exactly-once external effects. The current source model has one in-memory commit point only. The tests below are intended to validate that model's deterministic state transitions and expose the exact adapter obligations that remain.

Preserve all existing IDs and names: CommandId, EffectId, DispatchAttemptId, ExecutionId, ObservationSequence, ResultReceiptId/revision, PublicationAttemptId; LOOP-01..14; CASE-01..16; D-IDs; OD-01..13. Do not assign new canonical acceptance IDs here.

## 2. Verified patterns and what they actually guarantee

| Pattern / source | Verified behavior | Limit / PocketCode consequence |
|---|---|---|
| AWS transactional outbox | Aggregate mutation and outbox row are inserted in the same database transaction; publisher may deliver duplicates; consumers should be idempotent; event order must be preserved. | The transaction is the key guarantee. An in-memory append is not equivalent. |
| Debezium Outbox Event Router | Standard table shape includes unique event ID, aggregate type, aggregate ID, type and payload. Event ID is emitted in a header; aggregate ID becomes the message key to preserve per-aggregate partition order. Outbox rows are expected to be INSERT-only. | Reuse the metadata separation and stable key concepts, not Debezium or Kafka. No dependency selected. |
| CloudEvents | `source + id` identifies a distinct event; redelivery may reuse the same ID. | Identity is not authentication. Same identity with a different canonical digest must be quarantined by PocketCode's stricter policy. |
| Azure Service Bus duplicate detection | Sender-supplied MessageId is remembered only for a configured bounded time window (default 10 minutes, max 7 days); only MessageId is considered. Receive-side redelivery still requires idempotent consumer logic. | Broker dedupe is not a permanent consumer inbox and not an exactly-once external side-effect guarantee. Basic tier does not support this feature; not compatible with $0 assumption. |
| Amazon SQS FIFO | Producer deduplication IDs suppress duplicate sends within a 5-minute interval. Message groups serialize order; visibility timeout expiry can make messages visible again. | Even FIFO's bounded send dedupe does not replace consumer-side durable idempotency or prove a downstream external effect ran once. AWS infrastructure is not selected. |
| Apache Kafka 4.4 | Exactly-once consume-transform-produce can atomically commit output topics and consumer offsets in Kafka transactions. External destination effects require that destination to cooperate with the transaction or atomically store output and progress. | No broker can make an arbitrary external side effect exactly once without cooperation at the effect boundary. |

## 3. Normative model semantics

### 3.1 Producer transition

Given aggregate key K, current version V, command C and canonical transition payload P:

1. Validate command identity, effect/attempt scope, authorization assertion and expected aggregate version before mutation.
2. Derive canonical event bytes and digest from validated transition data. Do not accept a caller-supplied digest as proof of payload integrity.
3. If the command is a semantic no-op, return the existing disposition without advancing aggregate version, observation sequence or outbox event count.
4. If it is a legal state change, compute V+1 exactly once and derive one immutable event identity. The event records aggregate key K, version V+1, event ID, canonical digest and the relevant command/effect/attempt correlation.
5. In the current in-memory model, update aggregate state and append the matching outbox row at one model commit point. If validation or append fails before that point, no partial model mutation is visible.
6. A future durable adapter may claim aggregate/outbox atomicity only if both are committed in one durable transaction. A journal entry written after a separate database commit is not sufficient.

### 3.2 Sender / relay

- An outbox event's logical identity and canonical bytes are immutable across every send attempt.
- Every retry reuses the same event ID and digest; PublicationAttemptId changes for each actual publication attempt.
- A send timeout or lost acknowledgement means outcome UNKNOWN. Do not mint a new logical event and do not assume absence.
- A sender may mark an event delivered only from provider evidence bound to that exact event identity and publication attempt. A local "send called" flag is not provider acceptance.
- If the provider cannot resolve an ambiguous send, preserve UNKNOWN and require the provider-specific recovery rule. Do not automatically resend a potentially non-idempotent effect.

### 3.3 Consumer inbox

For a durable adapter, inbox uniqueness key is `(source, event_id)`; store the canonical digest and aggregate key/version alongside it.

- First-seen identity + valid digest + expected next aggregate version: apply business mutation and insert inbox record in the same destination transaction.
- Same identity + same digest: duplicate; return original disposition and do not reapply.
- Same identity + different digest: identity collision; quarantine/reject without changing aggregate state or accepted-event high-water.
- New identity + stale version: stale; no mutation.
- New identity + future version: gap; buffer or reject without advancing projection. Apply only after missing predecessor is resolved.
- Inbox record and business mutation in separate transactions leave a crash window and cannot claim exactly-once effect.
- Inbox retention must cover the maximum redelivery and operator replay horizon. If operators can replay indefinitely, either retain a durable compact identity tombstone indefinitely or define a bounded replay horizon and reject older events explicitly. Broker dedupe windows are not substitutes for this rule.

## 4. Crash and ambiguity matrix

| # | Failure injection | Expected model/adapter state | Required retry/recovery | Forbidden claim |
|---|---|---|---|---|
| F01 | Invalid command before transition | Aggregate, event and outbox unchanged | Correct input; new attempt only if semantics require | "Partially committed" |
| F02 | Process stops before aggregate/outbox durable transaction commit | Neither visible after restart | Retry command using stable CommandId/EffectId policy | "Outbox saved" |
| F03 | Aggregate and outbox transaction commits; process stops before sender sees row | Both survive restart; row discoverable | Relay resumes from durable outbox cursor | "Delivered" |
| F04 | Sender transmits; provider rejects before acceptance | Provider final rejection tied to same attempt | Correct/re-authorize; do not mutate logical event | "Accepted" |
| F05 | Provider accepts; response is lost | Outcome UNKNOWN locally | Query exact provider operation/scope; if provider lacks final resolution, preserve UNKNOWN | "Failed, safe to resend" |
| F06 | Provider accepts; sender crashes before recording acknowledgement | Provider may have effect; local delivery state uncertain | Reconcile using stable provider idempotency key or authoritative lookup | "No effect occurred" |
| F07 | Same event redelivered after consumer commit but before broker acknowledgement | Inbox and business mutation already committed | Duplicate lookup returns original result; ack message | "Second application" |
| F08 | Consumer commits business mutation but crashes before inbox record | This must be impossible in a correct transactional inbox design | Put both writes in same transaction; otherwise duplicate side effect remains possible | "Exactly once" |
| F09 | Consumer records inbox marker then crashes before business mutation | This must be impossible in a correct transactional inbox design | Same transaction; otherwise event can be permanently lost | "Processed" |
| F10 | Same source+event ID, changed payload digest | Conflict/quarantine; no state or high-water advance | Investigate producer identity collision | "Duplicate" |
| F11 | Version V+2 arrives before V+1 | No projection advance over gap | Buffer/reject; retry after predecessor | "In order" |
| F12 | Version V+1 arrives after projection already at V+1 | Stale/duplicate no-op depending identity | Return original disposition | "New transition" |
| F13 | Inbox dedupe record expired; old event replayed | Replay is no longer safely deduplicable unless permanent tombstone exists | Reject beyond declared replay horizon or retain tombstone | "Safe indefinite replay" |
| F14 | Broker dedupe window expires before sender retries | Broker may accept duplicate send | Consumer inbox must still dedupe | "Broker guarantees no duplicates" |
| F15 | Dead-letter message is manually resubmitted long after normal retry window | Treat as replay under same identity; consult durable inbox/tombstone | Preserve original event ID/digest; require operator reason | "New event" |
| F16 | Aggregate outbox rows delivered out of order | Consumer detects version gap and does not mutate | Resolve predecessor, then apply contiguous sequence | "Ordering guaranteed by ID" |

## 5. Deterministic regression cases for the existing model

These cases are model-only and must not imply adapter conformance.

1. `test_identical_transition_is_semantic_noop`: same aggregate state and canonical payload produce no new version, event or outbox record.
2. `test_changed_transition_advances_once_and_emits_matching_event`: one valid change advances exactly one version; event version, aggregate key and digest match the transition; exactly one corresponding outbox record is present.
3. `test_transition_rejects_stale_expected_version_without_mutation`: stale compare version leaves aggregate, event list and outbox unchanged.
4. `test_event_digest_is_recomputed_from_canonical_payload`: mutate payload while preserving a claimed digest; consumer rejects.
5. `test_same_source_event_identity_same_digest_is_duplicate`: repeated delivery returns the first disposition; accepted state and high-water do not advance twice.
6. `test_same_source_event_identity_changed_digest_is_conflict`: altered canonical payload with same identity is rejected; no consumer mutation.
7. `test_different_source_same_event_id_is_distinct_identity`: source participates in identity; same ID under another source is not silently deduplicated.
8. `test_future_version_does_not_advance_consumer_projection`: V+2 before V+1 does not alter projected state or accepted high-water.
9. `test_stale_version_does_not_mutate_consumer_projection`: V already applied; stale duplicate is no-op.
10. `test_lost_send_ack_reuses_logical_event_identity`: publication attempt changes, event identity and canonical digest do not.
11. `test_outbox_sequence_matches_aggregate_transition_order`: emitted event versions are strictly increasing for one aggregate; no global order is inferred across unrelated aggregates.
12. `test_failed_validation_leaves_aggregate_event_outbox_unchanged`: compare complete before/after state.
13. `test_boolean_is_not_accepted_as_integer_version`: reject Python bool where integer sequence/version is required.
14. `test_duplicate_disposition_is_stable`: duplicate delivery returns the same terminal disposition as the original accepted event, not a newly invented result.
15. `test_unknown_send_outcome_is_not_reclassified_as_rejection`: model preserves UNKNOWN and does not auto-retry absent authoritative provider resolution.

### Adapter-only tests (remain gated)

- Crash after durable aggregate/outbox commit and before relay scan; restart discovers exactly one logical outbox event.
- Crash after provider acceptance and before local acknowledgement; reconciliation queries exact event/effect/attempt scope.
- Two relay workers race; lease/fence prevents stale worker from overwriting newer publication state.
- Consumer inbox uniqueness and business mutation share one durable transaction.
- Crash injection at both orderings of inbox insert and business mutation demonstrates rollback of both.
- Restore from backup preserves inbox identities and outbox sequence; replay does not reapply committed effects.
- Dead-letter/operator replay respects permanent tombstone or declared replay horizon.
- Concurrent consumer deliveries for same identity serialize or conflict safely.

## 6. Acceptance and implementation order

1. First run current model tests against the exact source SHA; they are currently NOT RUN.
2. Add or correct deterministic model regressions without changing canonical LOOP/CASE/D/OD meanings.
3. Review the consumer's identity and digest rules against the actual current source; no model behavior is claimed implemented by this document.
4. Only after a separate adapter design/authorization, specify durable transaction boundaries, inbox retention, relay fencing and restore tests.
5. Do not choose a broker/database or introduce paid services. No AWS, Azure, Kafka, Debezium, Temporal or external framework is selected.

## 7. Red-team clarifications

- A transport's bounded duplicate-detection window is not a durable consumer inbox.
- A broker's exactly-once terminology is scoped to its documented boundary; downstream external effects require destination cooperation.
- Ordering keys preserve order only within the broker's documented partition/group scope; they do not create global order.
- Stable event identity is not producer authentication.
- An in-memory aggregate/outbox append is not crash durability.
- An inbox record without atomic business mutation can cause either duplicate effects or lost effects depending on write order.
- A dedupe retention policy is part of correctness, not housekeeping.

## 8. Sources opened and disposition

- AWS transactional outbox: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html
- Debezium 3.4 Outbox Event Router: https://debezium.io/documentation/reference/3.4/transformations/outbox-event-router.html
- CloudEvents core: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
- Azure Service Bus duplicate detection: https://learn.microsoft.com/en-us/azure/service-bus-messaging/duplicate-detection
- Azure Service Bus loss and duplicates: https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-loss-and-duplicates
- Amazon SQS FIFO exactly-once processing: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html
- Amazon SQS FIFO delivery logic: https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-understanding-logic.html
- Apache Kafka 4.4 delivery semantics: https://kafka.apache.org/44/design/design/
- Microsoft idempotent consumer pattern: https://learn.microsoft.com/en-us/azure/architecture/patterns/idempotent-consumer

All findings are research references, not selected infrastructure. Exact implementation and test status remain UNKNOWN / NOT RUN.
