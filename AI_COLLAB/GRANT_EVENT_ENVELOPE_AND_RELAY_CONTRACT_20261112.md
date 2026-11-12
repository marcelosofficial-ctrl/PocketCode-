# Grant-event envelope and relay contract

Date: 2026-11-12
Status: proposed, versioned design contract. No application/test implementation, adapter approval, transport, database or cryptographic mechanism selected.
Contract version: grant-event-envelope/v1. This is a document protocol version, not a new canonical LOOP, CASE or D-ID.
Source baseline: active branch 1ec716a75ee6a05ebbe4d8f6a2eb570837ea4f13.
Scope: release-grant aggregate transitions, immutable event/outbox creation, relay publication, consumer inbox and recovery.

## 1. Ranked problem and current source evidence

Rank 1 for this pass: a committed grant state and the durable evidence of that state must never disagree. Without event/version parity, downstream reports and recovery may skip a real state transition or wait forever for an event that cannot exist.

VERIFIED from scripts/release_grant_conformance.py and its tests:
- reserve() stages an initial grant, v1 event and outbox item at one in-memory commit point. Its failpoints test that in-memory staging is invisible before the commit.
- record_progress() increments aggregate_version for every accepted call, including a call that repeats the same progress_bytes, but does not append an event or outbox item.
- consume_event() uses the supplied GrantEvent.payload_sha256 as the first-delivery digest. It does not recompute a digest from canonical event bytes, authenticate the producer, or validate the event's full tenant/effect/attempt/receipt scope.
- mark_outbox_delivered() sets a boolean with no relay lease, fence, expiry, ownership check or stale-ack rejection.
- Current IDs use an in-memory counter. This does not establish OD-07 restore-safe high-water or uniqueness after backup restore.
- P40's 266/266 full scripts result did not include these missing adversarial assertions. Existing tests prove the current model's stated behaviours only.

INFERRED: an aggregate version that has no corresponding immutable event is a broken audit cursor even if the immediate UI reads the grant row correctly. A consumer that trusts sender-provided digest on first delivery cannot detect an altered event body merely by comparing the same supplied digest later.

## 2. Invariants

1. Every committed semantic aggregate transition advances aggregate_version by exactly one and creates exactly one immutable event/outbox row for that version in the same transaction.
2. A semantic no-op does not advance aggregate_version and creates no state-transition event. Repeated progress with the same value returns the current aggregate unchanged. If an audit fact is needed, record it in a separately versioned observation stream; do not fake a state transition.
3. An aggregate transition and its event are inseparable. If either cannot commit, neither becomes visible.
4. Event identity is immutable. Re-delivery preserves the exact event_id, source, canonical payload bytes and digest.
5. Producer authentication, event identity and payload integrity are separate proofs. A source/id pair, schema version or SHA-256 digest is not producer authentication.
6. Aggregate worker fencing and relay worker fencing are separate monotonic generations with separate owners and purposes. Do not reuse a transfer fence as a relay fence.
7. Authoritative time and high-water values are coordinator/adapter-owned. Worker timestamps are observations, not lease authority.
8. Publication is at-least-once. Exactly-once transport is not claimed; consumer effects are idempotent and atomically recorded with inbox identity.
9. Events for a grant are applied in aggregate_version order. A missing predecessor is deferred, never silently skipped.
10. Outbox publication acknowledgement is not consumer application acknowledgement and neither proves client receipt.

## 3. Envelope: grant-event-envelope/v1

Keep the current source namespace: urn:pocketcode:release-grants. The stable event identity is (source, event_id). Event IDs must be globally collision-checked and restore-safe under OD-07; their generation mechanism is intentionally unselected.

Required envelope fields:
- specversion: "1.0" when using the CloudEvents-compatible mapping.
- source: urn:pocketcode:release-grants.
- id: globally unique immutable event_id.
- type: com.pocketcode.release-grant.transition.v1.
- subject: grant_id.
- time: coordinator/adapter-assigned transition observation time in RFC 3339 form. It is metadata, not the ordering authority.
- datacontenttype: application/json.
- data_sha256: SHA-256 digest of the exact canonical data bytes.
- data: strict version-1 domain object described below.

Required data fields:
- schema_version: integer 1.
- tenant_id, grant_id, effect_id and attempt_id: non-empty immutable identity strings.
- aggregate_version: positive monotonic integer, exactly predecessor + 1.
- from_state and to_state: explicit states. Initial reservation uses from_state absent and to_state reserved; do not encode a fake prior state.
- receipt_id and receipt_revision: exact immutable receipt binding used by the grant.
- receipt_sha256: SHA-256 of the exact canonical immutable receipt bytes, obtained from the ReceiptHead binding or an authenticated immutable reference that resolves to those exact values. The receipt's versioned schema must define the canonical byte encoding (JCS or an independently reviewed exact equivalent).
- artifact_id and object_version: exact immutable artifact object binding where the transition concerns artifact transfer.
- artifact_sha256: SHA-256 of the exact artifact bytes in the bound receipt manifest, required for artifact-transfer transitions.
- operation: download or share where applicable.
- policy_epoch: current policy epoch where authorization affects the transition; otherwise explicitly absent by schema rule, never guessed.
- transition_fence: current worker/coordinator fence for a transition that requires a live claim. The initial coordinator reservation event is the sole no-worker-fence exception.
- progress_bytes: present only for a progress transition; bounded by the pinned artifact length and monotonic. Equal progress is a no-op.

Conditional field presence:
- The initial reservation omits the `from_state` property entirely; it does not encode `null`, an empty string or a synthetic prior state. All later transitions include the exact prior `from_state` and new `to_state` values.
- Conditional fields such as `operation`, `artifact_id`, `object_version` and `policy_epoch` are either present with a valid value or omitted only where that transition type explicitly permits omission. `null` is not an alternate spelling of omission. The per-event-type schema must define required, optional and forbidden fields before implementation.

Version-1 numeric bounds:
- Every integer counter, sequence, fence, version or byte length represented as a JSON number MUST be an ECMAScript safe integer (absolute value no greater than 9,007,199,254,740,991). Field-specific rules still apply: aggregate_version and applicable fences are positive; progress_bytes is non-negative.
- This applies to `aggregate_version`, `transition_fence`, mutable `relay_fence`, and `progress_bytes`, and to any other numeric sequence/high-water field added to this v1 envelope or relay metadata. Boolean values are not integers for schema validation.
- If a required counter cannot be advanced without exceeding the safe-integer bound, fail closed before mutation or publication. Never round, wrap or reuse it. A decimal-string representation requires an explicitly versioned schema revision and coordinated consumer migration; do not silently change v1 types.

Mapping rules:
- attempt_id is the existing DispatchAttemptId value. Do not merge it with EffectId, ExecutionId, CommandId, ObservationSequence, ResultReceiptId or PublicationAttemptId.
- relay_fence, relay_owner and relay lease expiry are relay-control metadata, not immutable business event data.
- Never place credentials, bearer tokens, raw signing secrets or private keys in an envelope.
- Reject unknown major schema versions. A consumer may retain and quarantine unsupported envelopes but must not apply them.
- Required fields are all present and type-checked. Use a strict schema; no implicit coercion, duplicate JSON keys or unrecognised security-sensitive extension fields.

Canonical bytes and integrity:
- Serialize the data object using RFC 8785 JSON Canonicalization Scheme (JCS) or an independently reviewed exact equivalent; compute SHA-256 over those exact UTF-8 bytes. Persist the bytes and digest together.
- Do not parse and re-serialize with an arbitrary JSON serializer when verifying a digest. Verify digest against the received canonical bytes first, then parse and validate the schema.
- JCS follows I-JSON / ECMAScript-number semantics. Represent identifiers and counters that may exceed the exact IEEE-754 integer range as decimal strings in a future schema revision; do not silently round them. JCS does not normalize Unicode; equivalent-looking strings remain distinct unless the domain schema defines normalization explicitly.
- `data_sha256`, `receipt_sha256` and `artifact_sha256` are three different digests with different subjects; none substitutes for another.
- The current Python receipt model computes its fingerprint with `json.dumps(sort_keys=True, separators=...)`; that is model-local deterministic serialization, not proof of RFC 8785/JCS cross-language canonicalization. A future adapter must follow the selected receipt schema's exact canonical byte rule and pin its version.
- Receipt and artifact digests must be recomputed or resolved from trusted immutable records, not accepted from request fields. Before reservation, verify the exact receipt ID/revision/digest and the exact artifact ID/object-version/length/digest; require the manifest integrity state to be `verified` and quarantine to be false.
- A digest detects byte changes relative to a trusted expected digest. It does not identify who created the event and does not make a caller-supplied digest trustworthy.

Producer authentication:
- A trusted ingress/adapter must authenticate the actual producer before accepting or relaying a worker-originated transition. Verify issuer, subject, key/credential status, audience, revocation, authorized source, tenant, grant, attempt, event type, policy epoch and time/replay bounds.
- The authentication result must be bound to the exact canonical data bytes and security-critical envelope fields. If a message-signature design is later selected, its covered components must include body integrity and the routing/scope fields used for authorization. Algorithm, key store, certificate format and signature protocol remain UNKNOWN and unselected.
- EventJournal.AuthenticatedProducer is a model input object, not a signature or authenticated production principal. Do not use its constructor as an ingress trust boundary.
- CloudEvents source+id provides interoperable event identity, not producer authentication, payload integrity or authorization.

## 4. Aggregate commit and outbox creation

For a state transition:
1. Read the current grant under a transaction/compare-and-swap boundary.
2. Validate exact grant, tenant, effect, attempt, receipt ID/revision/receipt SHA-256, artifact ID/object version/artifact length/artifact SHA-256, verified non-quarantined manifest state, allowed transition, policy epoch and current worker fence where applicable. The current authorization decision must bind the same receipt digest, artifact digest, operation and scope. The receipt and artifact proofs are resolved from trusted immutable content, never from caller-supplied digest claims.
3. Determine whether the request changes semantic state. If not, return the current aggregate and event cursor without incrementing the version.
4. Build the next aggregate with aggregate_version = prior + 1.
5. Build and canonicalize exactly one event for that next version. Compute the digest from those exact bytes.
6. Insert the immutable outbox event and commit the aggregate version/state update together. The event identity and version must be unique.
7. Return only after the transaction confirms commit. A lost response is recovered by reading the same aggregate and event identity, never by generating another transition.

Required future storage constraints, technology-neutral:
- Unique (grant_id, aggregate_version).
- Unique (source, event_id).
- Conditional aggregate update against expected prior aggregate_version.
- Immutable event bytes, digest and domain identity after insert.
- Durable, restore-safe event ID and aggregate version high-water values.
- Mutable delivery attempts/leases stored separately from immutable event contents, or in independently controlled delivery metadata that cannot rewrite event data.

If a transition is split across independent stores, it is not atomic. A separately reviewed transactional outbox/inbox protocol and visible intermediate state are required. Do not claim cross-store atomicity.

## 5. Relay state machine and fencing

Relay state for one immutable event:

pending -> leased(owner, expires_at, relay_fence) -> publication_acknowledged

An expired lease may be reclaimed as leased by a new owner with relay_fence strictly greater than every previously committed fence. A cancelled/quarantined disposition is an explicit terminal delivery-control state; it does not alter the business event.

Claim:
- Claim only the lowest not-yet-acknowledged aggregate_version for that grant, unless a prior event has an explicit durable quarantine/gap disposition authorised by policy.
- Compare lease state and authoritative adapter time atomically. An unexpired lease cannot be stolen.
- Increment relay_fence in the same commit that installs the new owner/expiry.
- The worker receives immutable (source, event_id, aggregate_version, exact bytes, digest) plus its relay claim token.

Publish:
- Publish the same immutable bytes and event identity on every retry.
- A broker's finite dedupe window is an optimization only. It cannot replace durable consumer inbox deduplication.
- If the process dies after broker acceptance but before local acknowledgement, lease recovery may publish the exact same event again. The consumer must treat it as a duplicate.
- Do not mark N+1 acknowledged while N remains unresolved for the same aggregate. Preserve per-grant order.

Acknowledge:
- Compare-and-set the delivery row against exact (source, event_id, aggregate_version, owner, relay_fence) and authoritative time.
- Reject an expired, superseded, mismatched or stale relay acknowledgement even if the broker accepted the message.
- A stale acknowledgement never mutates the current lease or delivery marker. The current owner can safely republish the same immutable event.
- Record publisher/broker acknowledgement separately from any consumer inbox/application acknowledgement.

Relay fencing is not effect/transfer fencing. The grant worker's transition_fence authorizes the business transition; relay_fence authorizes only delivery metadata. Neither can substitute for the other.

## 6. Consumer inbox and ordered application

Before first application:
1. Authenticate the publishing/producer trust chain using a trusted channel or signed envelope verification; validate exact source and tenant/grant authorization. A broker connection alone does not automatically authenticate the original business producer.
2. Verify SHA-256 against exact canonical data bytes. Reject non-canonical bytes, duplicate JSON properties, unknown critical fields or unsupported schema versions.
3. Validate grant_id, tenant_id, effect_id, attempt_id, receipt/object binding, allowed transition, predecessor version and applicable policy epoch/fence.
4. In one consumer transaction, insert inbox identity (source, event_id, digest, grant_id, aggregate_version) and apply the state projection/effect, or durably defer it without marking it consumed.
5. Commit inbox receipt and consumer state/cursor together. If processing creates another external effect, write a consumer-side outbox in that same transaction.

Disposition rules:
- Same source+id and same recomputed digest: duplicate; return the already accepted outcome.
- Same source+id with different bytes or digest: quarantine as an integrity conflict; never overwrite the first accepted event.
- Version = last_version + 1 and all validation succeeds: apply atomically.
- Version > last_version + 1: deferred_gap; do not write a consumed inbox receipt. Retry after predecessor or quarantine explicitly.
- Version <= last_version without an identical prior inbox identity: stale/conflicting history; quarantine, do not silently skip.
- Unknown grant, tenant mismatch, attempt mismatch, wrong source, stale policy epoch or invalid transition: reject/quarantine and retain evidence.
- A broker duplicate arriving after its dedupe retention expires remains safe because the consumer inbox identity is durable for the retention lifetime of the grant's evidence, not just the broker's short window.

A sender-provided digest compared only with a later sender-provided digest is insufficient. First delivery must be checked against the actual immutable canonical bytes and trusted producer authority.

## 7. Crash/recovery and observability

| Crash point | Required recovered state |
|---|---|
| Before aggregate/outbox commit | Neither new aggregate version nor event visible |
| After commit, before response | Read same aggregate version and event identity; do not create another |
| Relay claim before publish | Expired claim may be reclaimed with higher relay_fence |
| Broker accepts, process dies before local ack | Republish same event identity/bytes; consumer deduplicates |
| Lease takeover, then old relay ack arrives | Reject stale ack; current relay retains authority |
| Consumer receives N+1 before N | Defer without consumed inbox marker |
| Consumer applies event, response to broker lost | Redelivery is duplicate; no second state mutation |
| Restore from backup | Detect identity/sequence/fence rollback and collisions; do not resume publication until high-water safety is reconciled |

Keep separate timestamps for transition occurrence, coordinator observation, relay claim, publish attempt, publisher acknowledgement, consumer receipt and consumer application. No one timestamp proves all later stages.

## 8. Acceptance matrix for a future model-only change

| Test case | Expected result |
|---|---|
| New grant reservation | Grant v1 + one immutable v1 event + one outbox row in one commit |
| Fail before transaction commit | No aggregate, event, outbox or sequence increment visible |
| Real progress advance | Version increments once; exactly one matching event/outbox row |
| Equal progress replay | No version increment and no new event; existing cursor returned |
| Progress regression or above artifact length | Reject; aggregate and outbox unchanged |
| Event insertion conflict at same grant/version | Entire aggregate transition rolls back |
| First delivery body bytes altered but supplied digest unchanged | Recomputed digest mismatch; quarantine |
| Supplied digest altered to match tampered bytes | Producer/signature or trusted-ingress validation still fails; digest alone is not authority |
| Wrong tenant, grant, effect, attempt, receipt or object version | Reject/quarantine before projection |
| Unknown schema major or duplicate JSON keys | Reject/quarantine; no state effect |
| Same event ID and same exact bytes | Duplicate; one consumer effect |
| Same event ID and changed bytes | Quarantine; preserve first accepted event |
| Relay worker dies before publishing | Expired lease takeover with higher relay_fence |
| Publish accepted but local ack lost | Exact same event is retried; consumer inbox deduplicates |
| Old relay ack arrives after takeover | Stale-fence rejection; current delivery state unchanged |
| Event N+1 arrives before N | deferred_gap; no inbox-consumed marker |
| Event N arrives after deferred N+1 | Apply N then N+1 once, in order |
| Restore rolls sequence or fence backward | Stop and reconcile high-water; no new event claims or publication |

These are specification acceptance cases, not tests executed in this pass.

## 9. Research, reuse, and licence review

Sources opened 2026-11-12:
- AWS Prescriptive Guidance, Transactional outbox: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html. Atomic business update plus event, duplicate tolerance and ordering. Pattern only; no code copied.
- Debezium Outbox Event Router: https://debezium.io/documentation/reference/transformations/outbox-event-router.html. Immutable INSERT outbox rows, event identity and aggregate key for ordering. Debezium is Apache-2.0; no dependency or code reused.
- CloudEvents specification: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md. v1.0.2 core identity semantics; next draft is not a released replacement. Repository Apache-2.0; envelope mapping is optional and no code copied.
- NATS JetStream consumer/acknowledgement docs: https://docs.nats.io/nats-concepts/jetstream/consumers and https://github.com/nats-io/nats.docs.v2/blob/main/learn/jetstream/acknowledgment.md. At-least-once/redelivery and explicit ack semantics; NATS project Apache-2.0; no broker selected.
- RFC 8785 JCS: https://www.rfc-editor.org/rfc/rfc8785.html. Deterministic JSON canonicalization and its number/Unicode limits; specification reference, no code copied.
- RFC 9421 HTTP Message Signatures: https://www.rfc-editor.org/rfc/rfc9421.html. Message integrity/authentication pattern requiring careful component coverage and key verification; no signature scheme selected.
- PocketCode model sources and tests: scripts/release_grant_conformance.py, scripts/test_release_grant_conformance.py, scripts/event_journal.py. Project files only; model limitations are explicitly preserved.

Reuse decision: adopt atomic aggregate/outbox, immutable event identity, per-aggregate ordering, canonical bytes, durable inbox and fenced relay as technology-neutral patterns. Do not adopt AWS, Debezium, NATS, Kafka, a database, schema registry, signing key format or transport.

## 10. Red-team corrections to prior work

1. Earlier work identified aggregate/event parity as a requirement but did not make semantic no-op behaviour explicit. Fix: equal progress is a no-op with no version increment; an actual progress change must create one matching event.
2. Earlier work could be read as treating a payload digest as sufficient consumer integrity. Fix: first delivery recomputes the digest from exact canonical bytes and separately authenticates producer/source/tenant/scope.
3. Earlier work named relay fencing but did not distinguish business transition fence from delivery relay fence. Fix: separate immutable transition_fence from mutable relay_fence and require compare-and-set acknowledgement.
4. Earlier work did not separate broker publication acknowledgement from consumer application. Fix: separate publisher ack, consumer inbox receipt and consumer effect commit.
5. Earlier tests did not assert event/version parity or stale relay ack. Fix: the acceptance matrix explicitly adds no-op parity, first-delivery tamper, stale ack, out-of-order and restore rollback cases. No tests were run or claimed.

## 11. Gate and evidence boundary

VERIFIED: source findings above were read from the active branch. External sources listed above were opened on 2026-11-12.
INFERRED: this contract is a sufficient design target for a future isolated grant-event model revision.
UNKNOWN: durable adapter, database isolation level, event broker, authentication mechanism, signature format, restore strategy and production concurrency behaviour.
NOT RUN: new model tests, adapter tests, database/crash tests, broker integration or production conformance.

This document does not close the P39 implementation/adapter gate, authorise source/test edits, select infrastructure or change any LOOP, CASE, OD or D identifier. CASE-04 remains INCOMPLETE / timed_out.
