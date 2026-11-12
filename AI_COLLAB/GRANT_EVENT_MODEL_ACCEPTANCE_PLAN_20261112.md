# Grant-event model acceptance plan (2026-11-12)

Status: proposed test-only scope; not authorised for implementation in this pass. This plan converts the grant-event-envelope/v1 contract into a deterministic model acceptance suite. No new canonical LOOP, CASE or D identifiers are created. Local scenario labels below are not canonical IDs.

## 1. Ranked purpose

1. Aggregate/event/outbox parity: current `record_progress()` advances aggregate_version without creating a matching event/outbox row, including equal-progress calls. This is the clearest reproducible contract violation.
2. First-delivery integrity and scope: current `consume_event()` trusts the supplied digest and does not recompute exact canonical bytes or validate full tenant/effect/attempt/receipt/object/policy scope.
3. Grant-event relay ownership: current `mark_outbox_delivered()` is a boolean with no lease/fence/stale-ack protection. Existing `FakeOutboxStore` fences effect dispatch, not grant-event publication.
4. Ordered consumer inbox: current consumer handles duplicate digest and a simple future gap, but does not bind the full immutable event envelope or atomically represent inbox + projection + downstream outbox.
5. Restore safety: current grant IDs and sequence state are in-memory counters; no backup/restore high-water proof exists.

## 2. Source baseline and boundaries

Read from active branch:
- `scripts/release_grant_conformance.py`: `Grant`, `GrantEvent`, `OutboxItem`, `WorkerLease`, `ReleaseGrantContractModel.record_progress()`, `consume_event()`, `mark_outbox_delivered()`.
- `scripts/test_release_grant_conformance.py`: existing reservation atomicity, receipt-head pinning, idempotency, worker fencing, progress bounds, consumer duplicate and gap cases.
- `scripts/fake_outbox.py` / `scripts/test_fake_outbox.py`: effect-dispatch lease/fence model. Reuse its testing discipline, not its fence semantics or state machine.
- `scripts/event_journal.py` / `scripts/test_event_journal.py`: append-only producer-input, event identity and quarantine model. Its `AuthenticatedProducer` is a supplied model value, not cryptographic authentication and not the grant-event ingress implementation.

P40 baseline: run #59 / 43126974602, full scripts suite 266/266 on exact target SHA 319cffef121e327331aeaff59522ae279b112ecc. This is historical model evidence only. Proposed lane 4 was BLOCKED / NOT TESTABLE because no grant-event relay-specific tests existed. This plan targets that missing model lane; it does not close P39 or CASE acceptance.

Allowed future scope, only after explicit owner gate:
- Deterministic in-memory model and standard-library `unittest` tests.
- Fake clock and injected failpoints; no sleeps, real threads or nondeterministic timing.
- Keep the current P40 source SHA as baseline and record the exact new commit/SHA before execution.
- No DB, broker, network, key store, signing algorithm, provider, adapter, hosting or mobile runtime.
- No changes to canonical IDs or owner decisions. No external dependencies added.

## 3. Proposed test grouping

### A. Transition parity and atomicity (required)

| Local case | Stimulus | Required assertions |
|---|---|---|
| A1 reservation parity | Reserve a new grant | Grant v1, one immutable v1 event, one outbox record; same event identity and canonical bytes |
| A2 fail before commit | Inject failure after staged grant, after staged event, and immediately before commit | No grant/event/outbox visible; allocator/high-water unchanged |
| A3 progress advance | Advance progress from 0 to 4 | Version advances exactly once; exactly one event/outbox for that version; event scope equals grant scope |
| A4 equal progress | Submit same progress value again | Semantic no-op; no version increment and no new event/outbox |
| A5 invalid progress | Regression, bool, negative, non-integer and above artifact length | Reject; aggregate, event list, outbox and sequence unchanged |
| A6 event uniqueness conflict | Force duplicate (grant_id, aggregate_version) or (source,event_id) | Entire aggregate transition rolls back; original immutable event remains |
| A7 idempotent retry after lost response | Commit then replay exact reservation/transition key | Return same grant/event identity; never mint a second transition |

### B. Envelope and first-delivery validation (required)

| Local case | Stimulus | Required assertions |
|---|---|---|
| B1 canonical digest | Valid envelope with exact canonical data bytes | Recomputed SHA-256 equals stored digest; accepted once |
| B2 body tamper | Change a byte but retain original digest | Reject/quarantine before projection |
| B3 attacker recomputes digest | Change body and update supplied digest | Digest passes only integrity comparison; trusted producer/scope validation still rejects |
| B4 duplicate JSON keys / non-canonical encoding | Submit ambiguous or non-canonical bytes | Reject before parsing into an accepted event |
| B5 schema validation | Unknown major version, missing required field, wrong type, empty identity, unknown critical extension | Reject/quarantine; no projection |
| B6 exact scope | Wrong tenant, grant, effect, attempt, receipt/revision, artifact/object version, operation or policy epoch | Reject/quarantine; no projection |
| B7 event identity collision | Same (source,event_id), exact same bytes and scope; then same identity with changed bytes/scope | First is duplicate; second quarantined; original remains immutable |

The in-memory test must state clearly that producer identity is a trusted test fixture. It may verify that an injected ingress decision is bound to exact bytes and scope; it cannot claim cryptographic authentication, key revocation, certificate validation or production trust.

### C. Relay lease/fence and recovery (required)

| Local case | Stimulus | Required assertions |
|---|---|---|
| C1 first claim | Claim pending event | Owner, expiry and relay_fence are committed together |
| C2 active lease | Second worker claims before expiry | Claim denied; no fence change |
| C3 expired takeover | Claim after expiry | New owner gets strictly higher relay_fence |
| C4 stale ack | Old owner acknowledges after takeover | Reject; current owner/lease/delivery state unchanged |
| C5 publish then crash | Broker-acceptance observation occurs, local ack absent | Lease recovery republishes exact same bytes and event ID; no new business event |
| C6 ack binding | Ack with wrong event ID, version, owner or fence | Reject without changing delivery state |
| C7 per-grant ordering | N+1 is pending while N unresolved | N+1 cannot be marked publisher-acknowledged first |
| C8 distinct fences | Advance worker transition fence while relay lease remains active, and vice versa | Each fence only authorizes its own state machine |

Use a deterministic fake clock and monotonic integer relay fence. Do not reuse `FakeOutboxStore.Lease` or `StaleLease` as the grant relay API; its state machine is for effect dispatch.

### D. Consumer inbox and restore (required)

| Local case | Stimulus | Required assertions |
|---|---|---|
| D1 ordered apply | Deliver N then N+1 | Each applies once; cursor advances monotonically |
| D2 future gap | Deliver N+1 before N | deferred_gap; no consumed inbox row or cursor advance |
| D3 gap recovery | Deliver N after D2, then retry N+1 | N then N+1 apply exactly once |
| D4 lost consumer ack | Apply event, simulate response loss, redeliver | Durable-model inbox identifies duplicate; no second projection/effect |
| D5 inbox/effect atomicity | Inject failure between staged inbox and projection/effect | Neither visible after rollback |
| D6 conflicting stale history | Unknown older version or identity mismatch | Quarantine; do not skip or overwrite |
| D7 restore rollback | Restore snapshot with event ID, aggregate version or relay fence high-water below known committed maximum | Publication/claims stop until reconciliation; no ID/fence reuse |

## 4. Exit criteria for the future model lane

The future lane is PASS only if:
- Every required case above is implemented and asserted, including both no-op and real-progress parity.
- All crash/failpoint cases prove before/after commit visibility, not merely raised exceptions.
- Digest validation recomputes over exact canonical bytes before schema application; producer trust remains a separate injected concern.
- Relay claim and acknowledgement use a relay-specific fence and reject stale owners after takeover.
- Publisher acknowledgement, consumer inbox acceptance and consumer effect application are separate observable states.
- Event ordering and backup-restore high-water failures fail closed.
- Full existing `scripts` unittest discovery still passes on the same exact commit under the recorded Python/SQLite/OS environment.
- A separate adapter/production gate remains CLOSED. Model PASS does not prove a durable transaction, cross-process race, authenticated principal, broker delivery, backup restore, or CASE acceptance.

Failure of any required case = lane FAIL. Unimplemented or untestable case = lane BLOCKED / NOT TESTABLE, never silently omitted. Record per-case output and exact source SHA.

## 5. Red-team traps the test author must avoid

1. **False atomicity:** Python dict mutation after a failpoint is not a database transaction. The model can prove its own staged/commit contract only.
2. **False authentication:** an `AuthenticatedProducer` fixture or caller-supplied boolean does not prove signatures, key status, identity binding or revocation.
3. **Fence conflation:** effect-dispatch fence, grant transition fence and grant-event relay fence are distinct; tests must demonstrate stale relay ack rejection independently.
4. **Digest laundering:** hashing attacker-modified bytes and trusting the newly supplied digest is not producer authentication.
5. **No-op ambiguity:** progress equal to current value must not increment aggregate_version; if repeated observations matter, model them separately from semantic state events.
6. **False exactly-once:** transport is at-least-once; consumer idempotency/inbox provides one logical application, not exactly-once network delivery.
7. **Fake durability:** an in-memory restore fixture is not a real backup/restore or crash-consistency proof.
8. **Test-count inflation:** lane totals overlap the full suite; report them separately and do not sum them into full-suite totals.

## 6. Research and reuse basis

The grant-event contract's primary research set remains the basis:
- AWS transactional outbox: aggregate update + outbox write in one transaction, duplicate-tolerant consumer and per-aggregate ordering.
- Debezium Outbox Event Router: immutable outbox row and aggregate key for partition ordering; Apache-2.0 project, no code reused.
- CloudEvents v1.0.2: source/id event identity, not producer authentication or payload integrity; Apache-2.0 specification repository.
- NATS JetStream: at-least-once/redelivery and explicit acknowledgement semantics; Apache-2.0 project, no broker selected.
- RFC 8785 JCS: deterministic canonical JSON bytes, with number and Unicode constraints.
- RFC 9421 HTTP Message Signatures: possible future integrity/authentication reference only; no signing mechanism or key format selected.

All are design references only. No third-party code or dependency is introduced. No infrastructure is selected.

## 7. Current gate

VERIFIED: existing model methods and tests were inspected from the active branch; the gaps listed above are present in the current reference model.
INFERRED: the four groups above are a sufficient minimum deterministic acceptance plan for a first grant-event model revision.
UNKNOWN: production transaction isolation, relay scheduler, transport, key/identity trust, restore semantics and adapter behaviour.
NOT RUN: every test in this plan. No source/test changes were made in this unit.
