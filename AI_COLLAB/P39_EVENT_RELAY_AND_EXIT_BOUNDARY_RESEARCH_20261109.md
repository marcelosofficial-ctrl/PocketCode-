# P39 event relay and execution-boundary research

**Date:** 2026-11-09  
**Status:** VERIFIED research / proposed contract guidance / NOT IMPLEMENTED / NOT RUN  
**Scope:** The unresolved P39 event, outbox, idempotency, clock/fencing and exit-provenance seams. This supplements, and does not replace, `P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md`, `P39_EXIT_OWNER_DECISION_REGISTER_20261108.md`, `EXIT_PROVENANCE_RESOLUTION_20261108.md`, or the 2026-11-09 execution-boundary research.  
**Authority:** No owner decision is made here. No source/test edit, adapter/runtime/database/provider/transport selection, budget change or canonical LOOP/CASE/D change is authorized.

## 1. Ranked gaps

1. **Trusted event/version chain:** the sequential grant model can advance aggregate version without a matching event/outbox row, and consumer digest/source/grant binding is incomplete. This makes it unsafe as an adapter oracle until corrected.
2. **Durable relay ownership:** the grant-event delivered marker lacks claim/lease/fence/order enforcement. Two relay actors can race; stale delivery markers are not rejected.
3. **Authorization and replay boundary:** pre-commit and post-commit revocation are separate policy moments. An idempotent replay must recover original intent without becoming a fresh permission to transfer bytes.
4. **Execution-boundary-specific exit evidence:** Python subprocess APIs are not supported on Android, iOS or WASI; a web worker has an abort/termination algorithm but no native process return code. A single generic `exit_code` is not a cross-platform evidence model.
5. **Durable adapter proof:** restart-safe IDs/fences, authoritative time, atomicity under crash and actual cancellation/termination acknowledgements remain adapter obligations, not demonstrated by the sequential reference model.

## 2. Research findings and reusable patterns

### 2.1 Transactional outbox: atomic state transition, at-least-once publication

**VERIFIED:** AWS's transactional-outbox guidance addresses the dual-write failure between a database update and an event notification. The aggregate update and outbox record are committed in the same transaction; publishing happens after commit. AWS explicitly warns that duplicate messages can occur, that consumers should be idempotent, that notification order matters, and that no notification should escape a rolled-back transaction. Sources: [AWS transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) and its [implementation guidance](https://docs.aws.amazon.com/en_en/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html).

**PocketCode adaptation (INFERRED):**
- A logical aggregate transition must atomically commit the grant state/version, immutable canonical event and outbox row.
- A transition that does not change semantic state must not increment the aggregate version or create a state-change event.
- The dispatcher reads only committed outbox rows and publishes outside the transaction.
- A crash after publish but before delivered-marker commit is expected to produce a duplicate. The consumer must deduplicate durably by event identity *and* verify the canonical payload digest and scope.
- Per-aggregate ordering is an invariant. A later version cannot pass a missing, malformed or uncommitted predecessor.
- A poison predecessor moves that aggregate to an explicit HOLD/quarantine state with retained evidence and an audited repair/replay path. Never silently skip a sequence number.

This pattern addresses the dual-write boundary. It does not prove a transaction spans independent stores, a message broker, a provider API or a remote execution process.

### 2.2 Temporal: replayable history is not exactly-once external effects

**VERIFIED:** Temporal documents workflow replay as rebuilding state from recorded history; workflow code must make the same decisions for the same history. It warns against unrecorded time such as `Date.now()`, randomness and network calls in workflow logic. It also documents that Activities with side effects can execute more than once, including when the worker loses the response after the external operation completed. Its MCP integration specifically says side-effecting tools must be idempotent and that an Activity timeout does not cancel an MCP request already running on the Worker. Sources: [Workflow replay and deterministic APIs](https://docs.temporal.io/workflows), [Temporal MCP integration](https://docs.temporal.io/develop/python/integrations/mcp), [Activity failure and retry model](https://docs.temporal.io/encyclopedia/detecting-activity-failures).

**PocketCode adaptation (INFERRED):**
- Keep an append-only, identity-bound observation history from which a coordinator can reconstruct the accepted state.
- Record authoritative timestamps/decisions once; do not recompute them from a caller clock on replay.
- Use stable EffectId/request identity for one logical external effect and a fresh AttemptId for each actual attempt.
- An orchestrator timeout means the caller stopped waiting or the task timed out. It does not prove the remote request or side effect stopped.
- Before retrying an ambiguous external effect, query/reconcile using the same immutable intent and effect identity. Only a documented downstream idempotency contract can make a retry safe.
- A retry response or workflow replay is not a second authorization decision and not proof that the side effect happened exactly once.

**Do not adopt Temporal as a dependency.** Its workflow/event-history concepts are useful; the complete server/worker orchestration platform is outside the current phone-first/$0 scope.

### 2.3 NATS JetStream: delivery dedupe is bounded, not a permanent operation ledger

**VERIFIED:** JetStream provides persistence and at-least-once delivery. A message not acknowledged in time is redelivered. The NATS `Nats-Msg-Id` header is deduplicated within a configured Duplicate Window, not as a permanent idempotency ledger. The NATS release notes describe 2.15 as latest and 2.14 as maintained; 2.12 is EOL. Sources: [JetStream delivery semantics](https://docs.nats.io/concepts/jetstream), [message ID/deduplication header reference](https://github.com/nats-io/nats.docs/blob/master/nats-concepts/jetstream/headers.md), [NATS supported release lines](https://docs.nats.io/release-notes).

**PocketCode adaptation (INFERRED):**
- Transport/broker deduplication may reduce duplicate publication, but it must not replace PocketCode's durable command, attempt, event and receipt identities.
- Keep a permanent business-level idempotency record for the required retention horizon.
- Treat publish acknowledgement, consumer acknowledgement, outbox delivered-marker commit and external side-effect completion as separate observations.
- A short broker duplicate window cannot prove that a much later replay is harmless.

**Do not adopt NATS as a dependency.** It is a server-side message broker, not a mobile client execution primitive.

### 2.4 Fencing and database concurrency: enforce at the protected write

**VERIFIED:** Redis's official distributed-lock guidance explicitly recommends fencing tokens for long-running work and warns that its TTL expiry uses a non-monotonic wall clock, so wall-clock shifts can permit overlapping lock holders. PostgreSQL documents row locks held through transaction completion; its serializable failure guidance requires retrying the whole transaction logic after a serialization failure, not only the final write. Sources: [Redis fencing guidance](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/), [PostgreSQL row locks](https://www.postgresql.org/docs/17/explicit-locking.html), [PostgreSQL serialization failures](https://www.postgresql.org/docs/16/mvcc-serialization-failure-handling.html).

**PocketCode adaptation (INFERRED):**
- Expiry controls takeover/liveness; a monotonic durable fence is the stale-writer safety condition.
- Every protected write checks the current fence atomically with the mutation. A pre-check separated from the write is insufficient.
- Lease expiry uses an authority-owned store/coordinator clock. Worker timestamps remain untrusted observations.
- On serialization/concurrency conflict, reload current authorization, receipt head, grant state and fence, then recompute the complete decision in a new transaction. Do not retry only the last SQL statement.
- Durable ID and fence high-water authority must not reset when a grant row is deleted, restored or migrated.

Redis and PostgreSQL illustrate distinct mechanisms, not a selected PocketCode architecture. No database or distributed-lock implementation is selected.

## 3. Exit evidence must describe the actual execution boundary

### 3.1 Python subprocess is not a mobile/WASM portability layer

**VERIFIED:** Python 3.14's subprocess reference explicitly says the module is unavailable on Android, iOS and WASI and is not supported on mobile or WebAssembly platforms. Its mobile-platform introduction adds useful nuance: Android subprocess creation may be technically possible but is officially unsupported; iOS prohibits subprocess, multiprocessing and IPC from an app, and attempts can lock or crash the creating process. Sources: [Python 3.14 subprocess availability and return codes](https://docs.python.org/3.14/library/subprocess.html), [Python mobile-platform notes](https://docs.python.org/3.14/library/intro.html).

The same subprocess reference distinguishes a natural child return code from signal termination: on POSIX, `-N` means signal N; with `shell=True`, the reported status belongs to the shell and can be a mapped value such as `128+N`. A shell/wrapper code is therefore not interchangeable with a submitted child's natural exit.

**Consequence:** a generic PocketCode claim that “the mobile Python runner launches a child and captures its exit code” is unsupported for the current iOS/WASM path. On iOS or WASI, embedded execution must report embedded-runtime return/exception and host observations, not invented child-process facts. Android's unsupported capability must not be treated as a portable contract.

### 3.2 Browser Worker termination is an abort operation, not a child exit receipt

**VERIFIED:** The WHATWG HTML Living Standard, updated 2026-11-06, defines worker termination by setting the closing flag, discarding queued tasks, aborting the script currently running, and emptying the dedicated worker's port queue. It does not define a native child process exit code or a synchronous proof object returned to the caller. Source: [HTML Standard, worker termination](https://html.spec.whatwg.org/multipage/workers.html#terminate-a-worker).

**Consequence (INFERRED):** record that a host termination action was invoked and separately record any subsequent host-observed worker lifecycle event. Do not synthesize `child_exit=0`, do not claim an OS process was terminated, and do not mark artifact collection/cleanup complete solely because the worker was terminated. If the host cannot independently confirm termination/cleanup, retain UNKNOWN or NOT_CONFIRMED.

### 3.3 Proposed typed boundary, without freezing a wire schema

The coordinator should resolve a typed observation set before invoking the pure renderer. The exact field names and schema remain PROPOSED.

| Dimension | Required value families | What it must not imply |
|---|---|---|
| Execution boundary | embedded runtime; browser worker; native child; remote supervisor; WASM guest | No boundary is a generic native child by default |
| Submitted-code outcome | natural return; exception/runtime failure; natural child exit; not observed; unknown | Wrapper/worker exit is not child return |
| Host/wrapper outcome | completed; failed; terminated; disconnected; not observed; unknown | Wrapper success does not prove submitted-code success |
| Termination | not requested; requested; action invoked; confirmed by boundary authority; not confirmed; unknown | Request/disconnect is not acknowledgement |
| Signal/kill cause | signal, deadline, cancellation, resource limit, host failure, unknown | Numeric status alone does not identify the actor/cause |
| Provenance/binding | source, command, attempt, execution, event sequence, observation time/authority | Unbound or stale observations do not participate in verdict projection |
| Evidence quality | consistent; missing; contradictory; stale; unbound | Arrival order or numeric precedence must not erase contradictions |
| Cleanup/artifacts | pending; confirmed; failed; unknown; quarantined; release allowed/blocked | Execution success does not automatically release artifacts |

Keep the existing chain: `CommandId → DispatchAttemptId → ExecutionId → ObservationSequence → ResultReceipt`. Add adapter-specific execution-boundary metadata without collapsing those identities or changing canonical LOOP/CASE/D IDs.

### 3.4 Coordinator and renderer split

1. The adapter emits immutable raw observations with provenance and attempt/execution binding.
2. A trusted coordinator validates identity, source authority, freshness, ordering and policy-barrier evidence.
3. The coordinator produces a bounded resolved projection containing raw observations, resolved execution verdict, overall job/evidence disposition, termination state, cleanup state and artifact disposition.
4. The pure renderer displays that projection. It does not authenticate, reclassify or guess facts.
5. A legacy two-field helper that accepts lifecycle status plus generic `exit_code` cannot faithfully represent contradictory typed evidence. Keep it unchanged until an owner-approved versioned projection contract exists.

CASE-04 remains exactly **INCOMPLETE / timed_out**. Shell-shaped values such as 137/143 must not be guessed to mean natural child failure. EP-18 and EP-24 remain owner-dependent mappings. EP-21 through EP-25 stay proposed provenance cases until the owner/reviewer gate resolves them.

## 4. Reconciled acceptance worklist

These are not new canonical IDs. Reuse the existing P39/EP references in the crosswalk; do not invent a parallel numbering scheme or rename LOOP/CASE/D IDs.

| Existing reference | Scenario to prove | Required result/evidence |
|---|---|---|
| P39-S1 / RG-B1 / P39-EVENT-05 | Reserve → multiple progress transitions → terminal transition; rebuild state from events | Every committed version has exactly one immutable corresponding event/outbox; no-op does not increment; versions are contiguous |
| P39-S2 / RG-B2 / P39-EVENT-06 | Same event identity and claimed digest with changed tenant/grant/version/state; forged first event for unknown grant/source | Recompute digest over canonical bytes; validate source and tenant/grant relationship; reject or quarantine mismatch |
| P39-S3 / RG-H1 / P39-OUTBOX-04 | Relay A claims and pauses; B takes over and publishes; A attempts stale delivered mark | A's stale fence cannot mutate; duplicate publish is safe at consumer |
| P39-OUTBOX-05 | Version N+1 is ready while N is unacknowledged or poisoned | N+1 stays blocked; poison N enters HOLD/quarantine, never silently skipped |
| P39-CLOCK-01 / RG-B3 | Worker supplies future or backdated time to claim/extend a lease | Only authority clock controls lease eligibility; current fence controls mutation |
| P39-ID-01 / RG-H4 | Fresh model instances, process restart, restore, deleted grant and migration | Identity collision is detected; fence high-water and tombstone retention survive recovery |
| P39-POLICY-05 / RG-H3 | Allow at policy epoch P; revoke to P+1; attempt grant commit | Apply only the owner-selected consistency rule; strict revocation requires a proven linearization mechanism |
| P39-POLICY-02..04 / P39-S8 | Revoke after commit, before claim, during transfer and on resume | Apply owner-selected in-flight policy; recovered grant is not permission to emit more bytes |
| P39-IDEMP-01 / RG-O3 | Same request key is retried after receipt head advances | Original immutable intent/grant is recovered; no new grant or bytes; only new key resolves latest head |
| P39-RACE-06B / RG-O1 | Reuse an earlier receipt ID as a new successor | Reject previously used ID in the relevant scope |
| P39-RECEIPT-01 / RG-O2 | Mutate receipt/artifact bytes or quarantine state after reservation | Exact immutable receipt identity/revision/digest binding is checked before authorization |
| P39-CRASH-04 | Consumer commits effect; relay delivered marker is lost; event is redelivered | Consumer deduplicates the committed event/effect; relay then marks delivered under current fence |
| P39-ORDER-04 / RG-O6 | Permanent malformed/missing predecessor | Aggregate enters bounded, visible HOLD; original evidence is retained; only audited resolution can advance |
| EP-21 | Termination is requested/invoked but no acknowledgement arrives | INCOMPLETE; termination and cleanup remain unconfirmed; required artifacts stay quarantined |
| EP-22 | Wrapper exits 0 but submitted-code exit is absent | INCOMPLETE; never infer child success from wrapper exit |
| EP-23 | Child receives signal/resource termination | Preserve cause and platform-specific status separately; do not turn it into a natural program exit |
| EP-24 | Child exits 0; required collection/cleanup fails | Preserve both facts; exact verdict/release mapping awaits OD-10 |
| EP-25 | Deadline and nonzero child observation conflict in timing/provenance | INCOMPLETE unless trusted ordering resolves what happened |

The table reuses reviewed IDs and proposed EP cases already in the exit-provenance packet. It does not add, renumber, or redefine canonical acceptance IDs.

## 5. Maintenance, versions and licences checked 2026-11-09

These are source snapshots, not recommendations to adopt. Release/version claims were checked against official release or project pages; licences against project licence statements/files.

| Project | Latest visible release / date | Licence | Maintenance evidence and relevance |
|---|---|---|---|
| SQLite | 3.54.1, 2026-10-16 | Core library public domain | Official release history marks 3.52.0 withdrawn. 3.54.1 fixes a 3.54.0 heap-buffer overflow on 32-bit builds; 64-bit builds are not affected by that issue. Pin the exact library bundled by any future runtime and compile options. |
| Pyodide | 314.0.7, 2026-09-14 | MPL-2.0 | Official repository/release page lists 314.0.7 as latest stable; owner-reported Pyodios baseline is 314.0.5. This does not prove a defect or authorize a vendor-side manual upgrade. |
| NATS Server | 2.15.2, 2026-10-26 | Apache-2.0 | Official release notes say 2.15 latest and 2.14 maintained; 2.12 EOL. Its server and client dependencies need a full licence/dependency audit before redistribution. |
| Temporal Server | 1.32.2, 2026-11-02 | MIT | The official release page now lists 1.32.2 as latest and includes security fixes for the 1.32 line. This corrects the earlier research note that listed 1.32.1. The server is a substantial service, not a phone-side library. |

**Corrections to stale version notes:**
- Temporal Server 1.32.1 is no longer the latest visible release; 1.32.2 was released 2026-11-02.
- SQLite 3.54.1 is the latest visible version in the official release history; 3.52.0 is explicitly withdrawn. Do not write “3.51.3 and later” as a substitute for a pinned library version.
- Pyodide 314.0.7 is upstream latest stable while the owner-reported vendor build contains 314.0.5. Update only through the app vendor's supported path and validate the exact bundled runtime.

**Licence boundary:** this checks the core projects' declared licences only. It does not audit transitive dependencies, platform SDKs, bundled fonts, optional codecs, build scripts, or vendor-specific modifications. A redistribution decision requires a per-binary bill of materials and notice review.

## 6. Red-team corrections to prior reasoning

1. **Generic subprocess assumption corrected.** A process-oriented exit contract cannot be copied unchanged to iOS/WASI/Pyodide. Python 3.14 says subprocess is unsupported there; embedded-runtime and worker observations must be typed separately.
2. **Worker termination overclaim prevented.** The HTML Standard specifies abort/discard semantics, not a native process return code or proof of cleanup. “Terminate called” must not be mapped to child-exit success or termination confirmation.
3. **Temporal release record corrected.** Prior note named 1.32.1; live release page shows 1.32.2 (2026-11-02) latest.
4. **SQLite maintenance statement tightened.** Use 3.54.1 and explicit withdrawal of 3.52.0, not a vague “3.51.3 and later” statement; pin what the app actually bundles.
5. **Broker dedupe overclaim prevented.** NATS deduplication is scoped to a configured duplicate window; it cannot be PocketCode's permanent EffectId/AttemptId or receipt ledger.
6. **Timeout/cancellation overclaim prevented.** Temporal's MCP integration states an Activity timeout does not cancel an already-running MCP request. PocketCode must retain uncertainty and reconcile rather than claim the effect stopped.
7. **PR #4 stale snapshot corrected.** Its body says six files; the live PR API reports seven. Its process branch is 11 commits ahead and 312 behind the current working branch. It is not a safe direct merge candidate.

## 7. Decisions and explicit non-decisions

- No owner OD-01..OD-13 disposition is inferred or accepted by this report.
- P39/P40 implementation gate remains **CLOSED**.
- No source, tests, adapter or schema changed; no test ran.
- No database, message broker, workflow engine, runtime, sandbox, transport or hosting choice is made.
- No live adapter, concurrent-process, power-loss, restore, mobile-host, worker-termination or device test is claimed.
- No canonical LOOP-01..14, CASE-01..16 or D-ID changes are proposed.
- Existing command/attempt/execution/observation/receipt identity chain remains authoritative.
- The research patterns are candidates to translate into PocketCode's own provider-neutral contracts, not third-party framework adoption.

## 8. Primary source register

All sources below were opened or their official release/licence result was inspected on 2026-11-09. The linked page's current state may change; preserve the dates and versions stated above.

1. AWS Prescriptive Guidance, [Transactional outbox pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) (atomic aggregate/outbox, duplicate delivery, order, rollback).
2. Temporal, [Workflow replay](https://docs.temporal.io/workflows) (determinism, recorded time/history).
3. Temporal, [Python MCP integration](https://docs.temporal.io/develop/python/integrations/mcp) (retries, idempotent side effects, timeout does not cancel in-flight request).
4. Temporal, [Activity failure handling](https://docs.temporal.io/encyclopedia/detecting-activity-failures) (worker failures, retries, heartbeat and timeouts).
5. Temporal, [Server releases](https://github.com/temporalio/temporal/releases) and [MIT licence](https://github.com/temporalio/temporal/blob/main/LICENSE).
6. NATS, [JetStream](https://docs.nats.io/concepts/jetstream) (at-least-once redelivery), [message ID header source](https://github.com/nats-io/nats.docs/blob/master/nats-concepts/jetstream/headers.md) (configured duplicate window), [release policy](https://docs.nats.io/release-notes), [server releases](https://github.com/nats-io/nats-server/releases), and [Apache-2.0 licence](https://github.com/nats-io/nats-server/blob/main/LICENSE).
7. Redis, [Distributed locks](https://redis.io/docs/latest/develop/clients/patterns/distributed-locks/) (fencing and wall-clock caveat).
8. PostgreSQL 17, [Explicit locking](https://www.postgresql.org/docs/17/explicit-locking.html); PostgreSQL 16, [Serialization failure handling](https://www.postgresql.org/docs/16/mvcc-serialization-failure-handling.html).
9. Python 3.14, [subprocess](https://docs.python.org/3.14/library/subprocess.html) (platform availability, signal and shell status), [mobile platform introduction](https://docs.python.org/3.14/library/intro.html).
10. WHATWG, [HTML Living Standard: Web workers](https://html.spec.whatwg.org/multipage/workers.html#terminate-a-worker) (last updated 2026-11-06; worker termination).
11. SQLite, [3.54.1 release notes](https://www.sqlite.org/releaselog/3_54_1.html), [release history](https://www.sqlite.org/changes.html), and [public-domain statement](https://www.sqlite.org/copyright.html).
12. Pyodide, [314.0.7 release](https://github.com/pyodide/pyodide/releases), [314.0.7 changelog](https://github.com/pyodide/pyodide/blob/main/docs/project/changelog.md), [repository and MPL-2.0 declaration](https://github.com/pyodide/pyodide).

**Source limits:** The official AWS, Temporal, Redis, PostgreSQL, Python, WHATWG and SQLite pages were opened. Temporal's separate Activity Definition URL was inaccessible in one fetch; Activity retry claims above rely instead on the opened Temporal MCP integration and failure docs. NATS duplicate-window detail was inspected in the official NATS documentation source; the current documentation-site URL redirects and did not expose the old header name in the page body. No claim about a production PocketCode integration is based on these sources.
