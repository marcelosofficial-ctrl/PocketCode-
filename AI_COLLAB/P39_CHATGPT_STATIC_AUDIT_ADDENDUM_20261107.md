# P39 supplemental static audit and source research — 2026-11-07

**Purpose:** Add a ChatGPT source-pinned static audit to the existing P39 review package. This is not Claude's or Gemini's independent report, does not replace either report, and does not authorize implementation.

**Repository:** https://github.com/marcelosofficial-ctrl/PocketCode-  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Branch HEAD when prepared:** `4c9d17b818fd823eff5e183e6728655262446336`  
**Reference implementation and tests:** `744cb4dc7cd4994647c84ac7476d0c78a21f0540`  
**P39 documentation snapshot:** `04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0`  
**Review brief:** `4c9d17b818fd823eff5e183e6728655262446336`  
**Prepared:** 2026-11-07

## 1. Scope and status

This pass re-read the live `BOOT.md`, `STATE.md`, `NEXT_TASK.md`, `CHECKPOINT.md`, `AI_COLLAB/STATE_LEDGER_20261106.md`, `PROJECT_STATUS.md`, P39 review brief, P37 concurrency contract, P39 research packet, durable adapter contract, and the exact pinned reference code.

All code findings below are **VERIFIED model facts** at source SHA `744cb4dc`. Their production impact is **INFERRED** unless a durable adapter exists and is tested. No production adapter, durable database, concurrent multi-process test, stream transport or relay implementation was found in this scope. No code was changed and no test was run in this pass.

## 2. Ranked source findings

### P39-S1 — Aggregate versions can advance without an event/outbox record

**Severity:** HIGH — event-chain correctness and recovery  
**Status:** VERIFIED model gap; production adapter behavior UNKNOWN  
**Source:** `scripts/release_grant_conformance.py`, `record_progress()` at lines 269–293; `GrantEvent` at 51–59; initial event/outbox creation in `reserve()` before line 240; consumer at 295–313.  
**Related contract:** `AI_COLLAB/RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md`, §§5, 8A.

**Observed behavior:** `record_progress()` replaces the grant with `aggregate_version + 1` and a new progress value, then returns. It does not create a `GrantEvent` or `OutboxItem`. The initial reservation creates version 1 only.

**Reproducible schedule:**
1. Reserve a grant. The model contains grant version 1 and one initial event/outbox item for version 1.
2. Claim a worker lease.
3. Call `record_progress(lease, now=1, progress_bytes=5)`.
4. Observe grant version 2 while the event and outbox collections still contain only version 1.
5. Consume version 1.
6. Submit a legitimate future version 3 event. `consume_event()` returns `deferred_gap` because version 2 is absent.
7. No version 2 event can be relayed from the model's outbox.

**Impact:** The model's aggregate version sequence and event sequence diverge as soon as progress is recorded. Any projection that requires contiguous event versions cannot reconstruct the aggregate from its event stream. A future durable adapter must not publish a terminal version 3 while version 2 has no corresponding event.

**Required correction:** Every externally observable aggregate transition that increments the aggregate version must atomically append an immutable event and its outbox row in the same transaction as the grant update. If progress is intentionally coalesced, define a separate monotonic progress cursor and explicitly distinguish it from event aggregate version; do not silently increment the event version without an event. Add tests for reservation → multiple progress updates → completion, crash at each write boundary, and consumer rebuild from events.

### P39-S2 — Consumer trusts a caller-supplied digest and does not bind event metadata to it

**Severity:** HIGH — event integrity and false deduplication  
**Status:** VERIFIED model gap; exploitability in production UNKNOWN  
**Source:** `GrantEvent` at lines 51–59; `consume_event()` at lines 295–313; initial digest construction in `reserve()`.

**Observed behavior:** `GrantEvent` contains metadata and a `payload_sha256` string, but no canonical payload bytes. `consume_event()` trusts that digest. It neither recomputes the digest from a canonical event envelope nor checks that the event ID encodes or otherwise binds the supplied grant ID and aggregate version.

**Reproducible schedule:**
1. Reserve a grant and retrieve its version-1 event.
2. Consume that event once.
3. Construct another `GrantEvent` with the same `source`, `event_id`, and `payload_sha256`, but change `grant_id`, `aggregate_version`, and/or `state`.
4. Submit the changed event. The consumer returns `duplicate` because it compares only the supplied digest for an already-seen identity.

A first-delivery variant is also possible: construct a new identity with an arbitrary digest and inconsistent metadata. The consumer can accept it if its aggregate version is next in sequence.

**Impact:** The dedupe check proves only that the caller repeated a digest string, not that the immutable event facts are the same. The test `test_consumer_rejects_same_event_identity_with_changed_payload` changes only the digest; it does not test metadata changes while keeping the digest constant.

**Required correction:** Store canonical immutable payload bytes (or a canonical serialization of every semantically relevant field), compute SHA-256 inside the trusted event append/consumer boundary, and compare both bytes and digest. Bind the event to an existing grant, tenant, source allowlist, aggregate version and event type. Treat event identity and aggregate ordering as separate coordinates. Add tests for same identity/same digest/changed grant, changed version, changed state, forged first-delivery digest, unknown grant, cross-tenant grant reference, and wrong source.

### P39-S3 — Grant-event outbox delivery has no relay claim, lease or fencing lifecycle

**Severity:** HIGH — stale relay can mutate delivery state  
**Status:** VERIFIED model gap; production adapter behavior UNKNOWN  
**Source:** `mark_outbox_delivered()` at lines 315–321; `OutboxItem` at lines 61–64; `ReleaseGrantContractModel.__init__()` at lines 69–80.

**Observed behavior:** The grant-event model's `mark_outbox_delivered(source, event_id)` accepts only the event identity and changes `delivered` to true. The grant-event model has no relay lease, owner, expiry, claim token or fence. This is distinct from `scripts/fake_outbox.py`, which models a separate effect-dispatch outbox with a worker lease/fence and provider acknowledgement state. That separate model does not supply a grant-event relay implementation.

**Reproducible schedule:** Relay A publishes an event, pauses, and loses ownership. Relay B takes over and publishes the same event. B marks the row delivered. A resumes and calls `mark_outbox_delivered()`; the model accepts it because there is no owner/fence argument to validate.

**Impact:** The model cannot demonstrate the P37 stale-relay invariant. At-least-once publication means duplicate sends remain possible after publish-before-mark crashes; the durable state transition marking delivery must nevertheless reject stale owners.

**Required correction:** Model a grant-event relay claim with monotonic per-event or per-aggregate fencing, owner and expiry. Mark delivered using a conditional update that checks the current fence and state. Keep publish-before-mark recovery at-least-once and require idempotent consumers. Test stale acknowledgement after takeover, duplicate publication after crash, ordering of N/N+1, and a late acknowledgement after lease expiry.

### P39-S4 — State fencing does not stop an already-open transfer stream

**Severity:** HIGH — external side-effect/revocation boundary  
**Status:** VERIFIED contract limitation; concrete transport behavior UNKNOWN  
**Source:** `record_progress()` validates the worker fence before a state update. No streaming transport implementation exists in the reviewed source.

**Observed behavior:** A current fence protects the model's grant state. It cannot retract bytes already sent and does not itself terminate a network stream opened by an old worker. The P37 contract already acknowledges this distinction; the model has no transport-level proof.

**Required correction:** The transport must bind the stream to a short-lived, narrowly scoped capability and validate it at a defined enforcement point (for example, each bounded chunk or resumable range), with explicit cancellation propagation and a documented maximum in-flight chunk after revocation. Define whether revocation prevents new chunks, closes the stream immediately, or allows a bounded grace period. Record bytes sent before revocation separately from client-confirmed receipt. Do not claim that lease expiry or a database fence alone revokes an established connection.

## 3. Additional audit observations

### 3.1 Event journal trust boundary is correctly labelled, but remains an adapter obligation

**VERIFIED:** `scripts/event_journal.py` explicitly says `AuthenticatedProducer` is supplied by a trusted adapter and that this module does not verify credentials or signatures. It computes SHA-256 from exact payload bytes and compares payload bytes on duplicate identity. It also checks source authorization and an expected audience.

**VERIFIED limitation:** `advance_fence()` and `append()` are separate in-memory operations. The journal's own documentation says a durable implementation must atomically compare-and-advance fence state with event append. The Python value object is constructible by callers and is not proof of authentication.

**Required adapter rule:** Never accept `AuthenticatedProducer` from an app/provider payload. Construct it only after verifying issuer, subject, credential/key status, audience, source authorization, revocation and replay policy. Atomically validate fence and append in the durable store.

### 3.2 Existing fake outbox is useful, but must not be mistaken for the grant-event relay

**VERIFIED:** `scripts/fake_outbox.py` models an effect-dispatch outbox. Its `claim()`, `_require_current_lease()`, `mark_dispatching()` and `acknowledge()` check lease/fence state. Its `resolve_reconciliation()` deliberately says caller trust is not verified there.

**Correction to earlier shorthand:** Saying “the outbox has fencing” or “the outbox lacks fencing” without naming which outbox is ambiguous. The effect-dispatch fake has worker fencing; the separate grant-event outbox model does not have a relay-claim/fence lifecycle. Keep these as separate state machines and acceptance suites until an explicit integration contract is approved.

### 3.3 Consumer gap deferral is not a complete event-integrity check

**VERIFIED:** `consume_event()` defers future aggregate versions and does not record them as consumed. It rejects versions at or below the last applied version when the identity was not already seen. This is useful ordering behavior.

**Limitation:** Gap handling does not authenticate the event producer, validate the event digest, validate grant existence, validate tenant binding, or prove that the event metadata is the data that was hashed. These checks must not be inferred from the existence of source-scoped deduplication.

## 4. Research: primary-source patterns and legitimate reuse

Checked 2026-11-07. The recommendations below reuse documented patterns, not copied implementation code. No project, service, database, broker or workflow engine is selected.

| Reference | Verified current evidence | Reusable pattern | Limitation for PocketCode |
|---|---|---|---|
| PostgreSQL 18 | Official docs describe row locks; `SELECT FOR UPDATE` blocks conflicting writers/lockers until transaction end. | Stable receipt-head row lock, then re-read current head and write grant/event/outbox in one transaction. | Row locks do not create a missing head row. Bootstrap uniqueness and transaction retry/deadlock handling remain necessary. |
| AWS transactional outbox guidance | Explains the dual-write failure, duplicate delivery, ordering and rollback constraints. | Atomic state + outbox write; at-least-once relay; idempotent consumer; preserve per-aggregate order. | Guidance is a pattern, not a service guarantee for an unspecified PocketCode topology. |
| Debezium Outbox Event Router | Official docs describe an outbox row with event ID and aggregate ID; aggregate ID becomes the Kafka key, helping preserve order within a partition. Current docs label 3.7 latest stable and 3.8 development. Debezium code is Apache-2.0. | Stable event ID plus aggregate key; CDC can relay committed outbox rows without application dual-write. | Requires a compatible database/CDC/broker deployment; ordering is partition-scoped and must be configured/verified. It is not a $0/mobile MVP choice by default. |
| CloudEvents | Latest core release listed is v1.0.2. The spec requires source + id uniqueness for distinct events and permits the same identity for a retransmitted duplicate. | Keep event identity `(source,id)` separate from aggregate version and transport delivery identity. | CloudEvents does not authenticate producers, guarantee ordering or provide exactly-once delivery. |
| NATS JetStream | Official server release page lists v2.15.2 released 2026-10-26; server repository declares Apache-2.0. Consumer docs describe ack-timeout redelivery and warn that a late acknowledgement from an earlier delivery may still be considered after redelivery. | Stable message identity, explicit acknowledgements, redelivery handling and idempotent consumers. | Broker acknowledgement is not a substitute for PocketCode's conditional durable state update or consumer idempotency. |
| Temporal | Official server releases include v1.32.2 dated 2026-11-02; server repository declares MIT. | Durable workflow history, deterministic orchestration and idempotent Activities for external side effects. | Adds a server and persistence/operations footprint; no reason to select it before workflow volume, hosting and $0 constraints are validated. |
| etcd | Official releases list v3.6.16 dated 2026-10-22; repository declares Apache-2.0. API docs describe linearizable operations by default, with watch ordering/revision caveats. | A coordinator-generated monotonic revision can act as a fencing generation if the protected resource checks it. | Requires an operational consensus cluster; a lease alone does not fence an external stream or arbitrary storage writes. |
| gRPC cancellation | Official guide says long-lived server handlers must periodically check cancellation and cease work; library cancellation does not automatically interrupt arbitrary application handler code. | Propagate cancellation and check it inside long-running stream handlers. | Cancellation is cooperative and cannot retract already emitted bytes; transport capability/revocation remains a separate contract. |

### Source links

- PostgreSQL 18 explicit locking: https://www.postgresql.org/docs/current/explicit-locking.html
- AWS transactional outbox: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html
- Debezium outbox router: https://debezium.io/documentation/reference/transformations/outbox-event-router.html
- Debezium license: https://github.com/debezium/debezium.github.io/blob/develop/license.asciidoc
- CloudEvents specification and releases: https://github.com/cloudevents/spec and https://github.com/cloudevents/spec/releases
- NATS JetStream consumers: https://docs.nats.io/nats-concepts/jetstream/consumers
- NATS releases/license: https://github.com/nats-io/nats-server/releases and https://github.com/nats-io/nats-server/blob/main/LICENSE
- Temporal releases/license: https://github.com/temporalio/temporal/releases and https://github.com/temporalio/temporal/blob/main/LICENSE
- etcd releases/license/API guarantees: https://github.com/etcd-io/etcd/releases, https://github.com/etcd-io/etcd, https://etcd.io/docs/v3.5/learning/api_guarantees/
- gRPC cancellation: https://grpc.io/docs/guides/cancellation/

### Reuse decision

Reuse the *semantics*: atomic outbox, stable event identity, aggregate partition key, conditional writes, monotonic fencing, idempotent side effects and cooperative cancellation. Do not copy code or choose Debezium, NATS, Temporal, etcd, PostgreSQL or any other dependency in this pass. Verify exact version, transitive dependencies, licence notices and operating cost at the time of any future adoption.

## 5. Red-team corrections to prior ChatGPT work

1. **Missed digest-to-metadata binding:** The previous static audit identified absent grant validation but did not test the stronger case where an event reuses the same digest string while changing grant/version/state metadata. This pass adds P39-S2 and a concrete duplicate-bypass schedule.
2. **Ambiguous “outbox fencing” wording:** The earlier audit discussed the grant-event `mark_outbox_delivered()` gap but did not clearly distinguish it from `FakeOutboxStore`, which has a separate dispatch lease/fence lifecycle. This pass explicitly separates the two state machines.
3. **P39 review links are not all immutable:** The P39 brief names a pinned docs SHA but several Markdown links target the moving branch; its fake-outbox and event-journal links also target the moving branch rather than the tested source SHA. The review brief itself was added after the pinned docs snapshot. This makes the prose pins stronger than the actual hyperlinks. Section 6 supplies immutable replacements.
4. **Stale continuity count:** The prior checkpoint recorded 25 documentation-only commits from source SHA 744cb4d to docs snapshot 04f4db2. The live branch is now 27 commits ahead of 744cb4d. The 27-commit comparison lists only AI_COLLAB/continuity documentation paths, not `scripts/**` or workflow paths. The old 25 count remains valid only for the earlier pinned snapshot, not live HEAD.
5. **Temporal version became stale:** The earlier research packet named v1.32.1. The official release page now lists v1.32.2, released 2026-11-02. No architecture decision depends on either version; the research note now records the newer release and retains Temporal as a pattern reference only.

## 6. Immutable P39 reference correction

The P39 prompt currently states:
- docs snapshot: `04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0`;
- source/test SHA: `744cb4dc7cd4994647c84ac7476d0c78a21f0540`;
- review brief HEAD: `4c9d17b818fd823eff5e183e6728655262446336`.

For a truly immutable review, reviewers should use these exact URLs rather than branch-floating links:

**Pinned documentation snapshot 04f4db2**
- Research/red-team packet: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0/AI_COLLAB/RELEASE_GRANT_ADAPTER_RESEARCH_AND_REDTAM_20261107.md
- Concurrency/crash contract: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0/AI_COLLAB/RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md
- Durable adapter contract: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0/AI_COLLAB/DURABLE_ADAPTER_CONTRACT_20261106.md
- Project status: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0/PROJECT_STATUS.md
- Roadmap: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0/ROADMAP.md
- State ledger: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0/AI_COLLAB/STATE_LEDGER_20261106.md

**Pinned source and tests 744cb4d**
- Grant model: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/744cb4dc7cd4994647c84ac7476d0c78a21f0540/scripts/release_grant_conformance.py
- Grant tests: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/744cb4dc7cd4994647c84ac7476d0c78a21f0540/scripts/test_release_grant_conformance.py
- Receipt model: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/744cb4dc7cd4994647c84ac7476d0c78a21f0540/scripts/result_receipts.py
- Receipt tests: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/744cb4dc7cd4994647c84ac7476d0c78a21f0540/scripts/test_result_receipts.py
- Fake effect-dispatch outbox: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/744cb4dc7cd4994647c84ac7476d0c78a21f0540/scripts/fake_outbox.py
- Event journal: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/744cb4dc7cd4994647c84ac7476d0c78a21f0540/scripts/event_journal.py

**Review brief**
- P39 prompt itself: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/4c9d17b818fd823eff5e183e6728655262446336/AI_COLLAB/P39_INDEPENDENT_REVIEW_PROMPT_20261107.md

The live branch HEAD is a continuity locator, not a substitute for either pinned snapshot. The 27 commits after 744cb4d are documentation-only according to the GitHub compare response, but reviewers should still use the exact source/test and docs pins above.

## 7. Minimum acceptance additions before any durable adapter is accepted

1. **EVENT-01:** Every aggregate version increment has exactly one immutable event and one outbox row committed atomically.
2. **EVENT-02:** Consumer recomputes digest from canonical immutable payload bytes and rejects metadata/payload mismatch.
3. **EVENT-03:** Event source and ID are unique; event identity binds grant, tenant, aggregate version and event type.
4. **EVENT-04:** Unknown grant, cross-tenant grant, wrong source and changed metadata under a reused identity are rejected or quarantined.
5. **OUTBOX-01:** Grant-event relay claim is leased and fenced; stale delivered-mark after takeover fails.
6. **OUTBOX-02:** Crash after publish before delivered-mark can redeliver but produces one logical consumer effect.
7. **OUTBOX-03:** Per-grant N+1 cannot be published/accepted before N is durably resolved; gap deferral is persisted or deterministically retried.
8. **STREAM-01:** Revocation/cancellation is tested during an open stream, between chunks and after worker takeover.
9. **STREAM-02:** Test report distinguishes bytes accepted by transport, bytes emitted, bytes observed by client and bytes acknowledged by client.
10. **RECOVERY-01:** Restart/rebuild from durable grant, event, outbox, lease/fence and consumer state produces the same aggregate without event gaps or duplicate logical effects.

These are proposed adapter-conformance additions, not new canonical LOOP/CASE IDs. Do not alter canonical IDs until the independent review reconciliation explicitly approves the mapping.

## 8. Disposition and next gate

**Static design disposition: ACCEPT WITH CHANGES.** The overall direction (transactional reservation, stable intent identity, separate authorization provenance, at-least-once outbox, source-scoped event identity, monotonic fences and explicit stream revocation policy) is sound as a design direction. The current grant reference model does not yet satisfy its own event-chain and relay-fencing requirements, and the consumer digest check is too weak for the stated integrity contract.

**Next step:** complete Claude's and Gemini's independent reviews against the immutable pins in §6. Then reconcile all findings. After that, correct the sequential reference model and its tests before adapter implementation planning. Do not select a database, broker, workflow engine, provider, runtime or host in this step.

## 9. Assumptions and unknowns

- Production topology, database, queue, transport protocol, authentication provider and deployment model remain UNKNOWN.
- Whether progress events must be emitted individually or may be coalesced is a contract decision still to be made; either choice must preserve a gap-free, rebuildable event history.
- The gRPC reference is a transport example, not a recommendation to use gRPC.
- The external reviewers' reports may exist outside the repository; this audit only establishes that no matching reviewer-report files were found in the inspected repository tree.
- No code or tests were executed locally during this pass.
