# Happy Agent Daemon: Code-Level Architecture and Reuse Audit — 2026-11-05

**Reviewed upstream revision:** slopus/happy-agent commit 4c1c2727e9259eb46f29829133144be55754f807  
**License:** MIT  
**Status:** Public source and test inspection. This is a research/design reference, not a PocketCode runtime selection, backend adoption, security certification, or product integration.

## Executive decision

Happy Agent is the most relevant current reference for the **PC-hosted execution side** of the combined PocketCode/RevDev product direction. It is a headless local daemon that presents one API to desktop, web and paired mobile clients, while sharing session, permissions, persistence, compute and event machinery across several provider/harness paths.

Do not copy Happy Agent wholesale and do not make it a mandatory dependency. It is a Node/Bun desktop daemon, not an iPhone-native runner. Its provider credentials are the user's existing local installations and subscription/API access. It does not provide a free-tier bypass. Its codebase is large and tightly coupled to its own packages, database layer, sandbox supervisor, provider integrations and lifecycle model.

The best reuse strategy is **contract and invariant extraction**:
1. Database-first durable session/event state.
2. Stable operation IDs with a clearly documented at-least-once execution model.
3. Operation-level locks for conflicting work, while allowing independent work in parallel.
4. Bounded output with byte counts and explicit omitted-byte counts.
5. Explicit separation between one-shot command timeout and long-running session observation timeout.
6. Permission decisions based on the exact tool invocation, with allow/deny/unproven outcomes.
7. Fail-closed sandbox setup and acceptance tests that mark a skipped boundary as unproven, not passed.
8. One provider-neutral host API with adapters for provider-native agents and protocols.

The strongest direct code reuse already in PocketCode remains the very small MCP Tasks poll-interval helper. The Happy Agent ideas are architectural patterns, not small drop-in files.

## 1. What Happy Agent actually is

Happy Agent is a long-running headless daemon, typically running on the user's own computer. It owns sessions, agents, tools, permissions, sandboxing, persistence, subagents, MCP, terminals and a public API. Clients connect through a local Unix socket or network transport using HTTP, Server-Sent Events and WebSockets. The original Happy mobile app can pair with the daemon and interact with the same primary sessions.

The README describes a model/harness split:
- Its own agent loop can speak model-native interfaces for Codex/GPT, Claude and Grok.
- It can also delegate the whole agent loop to other installed agents, including Codex CLI, Claude Code, Antigravity/Gemini, OpenCode and ACP-compatible harnesses.
- Goose can be configured as an ACP harness.
- Mobile messages enter the same session and permission boundary, not an alternate remote-control privilege path.

Provider access uses credentials already managed by local tools or explicit local configuration. The user remains responsible for provider terms, subscriptions, quotas and credentials. A phone-only user without a PC or already-authenticated host cannot run this daemon independently.

**PocketCode implication:** this is a strong reference for a future optional PC companion/host agent behind a stable PocketCode protocol. It is not a substitute for PocketCode's phone-first interface, local iOS runner, report contract, or manual AI handoff. It is also not evidence that PocketCode needs to adopt this exact daemon architecture.

## 2. Pinned source map

All paths below are from commit 4c1c2727e9259eb46f29829133144be55754f807.

| Component | Source file | Blob SHA | Key behavior |
|---|---|---|---|
| Architecture | docs/architecture.md | 5676e776ffc7024e0cd39753086941a9f4638047 | Daemon, session model, persistence and package boundaries |
| Permission and sandbox policy | docs/permissions-and-sandbox.md | b80ba8d74e5185b707427bd7641b32d871e60b8e | Four modes, per-tool review, OS boundaries |
| Agent storage | packages/happy-agent-base/sources/AgentStorage.ts | 88712e24a531f0327f2c663cfd87b840f90e8a44 | Exclusive DB ownership, ordered atomic migrations |
| SQLite process lock | packages/happy-agent-base/sources/AgentSQLiteProcessLock.ts | 75903c259d0d57549a097807162caa1145c06966 | Kernel-backed process-lifetime DB lock |
| Durable function executor | packages/happy-agent-modules/sources/durableFunctions/DurableFunctionsModule.ts | 4d897e3fb1bc91e400318e128c95d4a3a4502eef | Pending-call recovery and explicit at-least-once semantics |
| Durable call storage | packages/happy-agent-modules/sources/durableFunctions/SqliteDurableFunctionsStorage.ts | fb45ec6d7314c9ca1ca250928764119ea3cabee1 | Unique pending operation ID and SQLite transaction storage |
| Durable functions documentation | packages/happy-agent-modules/sources/durableFunctions/README.md | 7ffddbba324fafb8015aab780658a2c1d8b77874 | Idempotency, lock keys, limits and replay warning |
| Durable recovery tests | packages/happy-agent-modules/tests/durableFunctions/DurableFunctionsCompletionAndRecovery.test.ts | 9acf951780667c1f1c2d1ef8cab4c6aff95c5f15 | Restart replay, KV recovery, terminal behavior |
| Operation-ID tests | packages/happy-agent-modules/tests/durableFunctions/DurableFunctionsInvocation.test.ts | 663e4e37c232c5778e7a5299c5c2dbe9c67f2338 | Duplicate pending operation returns original call ID |
| Lock/cancel tests | packages/happy-agent-modules/tests/durableFunctions/DurableFunctionsLocksAndCancellation.test.ts | 3b583b7d6286e883595f45160b4a63b7d9fe4e29 | FIFO conflicts, disjoint concurrency and cancellation |
| Durable event store | packages/happy-agent-modules/sources/events/EventsDatabase.ts | 625e57ef8fd5c2182a6bec6f9378c4e7b134639e | Event IDs, cursor replay and bounded retention |
| Event store module | packages/happy-agent-modules/sources/events/EventsModule.ts | 6a267193015d9cebc3dc86d1348eb30b852439d5 | Append-only durable event window and replay |
| Event store tests | packages/happy-agent-modules/tests/events/EventsModule.test.ts | 6ce2dda8f4482e719487c2967294f4bd1c43247a | Retention, rollback and restart consistency |
| Host compute | packages/happy-agent-compute/sources/host/createHostCompute.ts | 7a6743b02b100efe3c0981a80464c18386f6d4af | Composes filesystem, shell, process, network and cleanup |
| Host shell | packages/happy-agent-compute/sources/host/createHostShell.ts | 6e3b4dfd84afce3c21a10e41145603751b3a3ce5 | One-shot command and background session lifecycle |
| Process manager | packages/happy-agent-compute/sources/processes/NativeProcessManager.ts | d5ef7ab5839962cd6b2b8ee05d51e7f8ff22ccc4 | Timeout, cancellation, process trees and output retention |
| Process tree killer | packages/happy-agent-compute/sources/processes/impl/killProcessTree.ts | ba7587a209dee5119f8ebe603aed05dda8456888 | POSIX groups and Windows taskkill /T |
| Host process limits | packages/happy-agent-compute/sources/host/impl/hostSessionLimits.ts | 1e519f54d1496cfc00109bc59f97e6aa30307cca | 120-second default, output and session caps |
| Host process tests | packages/happy-agent-compute/tests/host/createHostProcesses.test.ts | 4ffaaa55a54026b0116f9fdd3d13583c0a8eb868 | Real command, process-group signal and Windows terminal tests |
| Host shell tests | packages/happy-agent-compute/tests/host/createHostShell.test.ts | ec9a9d60fffff50e0493fe1e505eb20b8f85c021 | Timeout/background distinction, output deltas and process-tree kill |
| Sandbox boundary tests | packages/happy-agent-compute/tests/host/hostSandboxBoundary.test.ts | b59c6626b80b6dd0fb8e9082bd436edff8e9b69b | Outside-workspace writes, explicit roots and fail-closed expectations |
| Permission argument snapshot | packages/happy-agent-modules/sources/permissions/impl/snapshotPermissionArguments.ts | 8f44e0eacdc072abc0695f3e72c533e5c8268464 | Detached, bounded, immutable approval argument snapshot |

The source review is pinned to the commit above. The source tree, not a README feature matrix, is the basis for these findings.

## 3. Durable functions: a useful queue, but at-least-once

The durable functions module writes a pending call inside the caller's database transaction. It starts dispatch only after the outermost transaction commits. On daemon restart it enumerates pending rows and resumes them. Its SQLite schema uses:
- a call row with primary-key call ID;
- a UNIQUE operation ID while a call is pending;
- serialized arguments and lock keys;
- a per-call key-value state area for executor checkpoints.

A duplicate invocation using the same operation ID while the row is pending returns the existing call ID and does not write another pending row. The test deliberately changes the arguments on the duplicate invocation and confirms the executor starts once. This is useful protection against duplicate enqueue while the original work is pending.

But the implementation is explicit: **this is at-least-once execution, not exactly-once side effects**. If the process completes external work and crashes before its completion transaction deletes the pending call, restart runs the executor again. Executors and success handlers must be idempotent. A terminal executor throw or invalid result is deleted without a module retry. Calls have no result API. Completion deletes the pending row and associated KV state; the operation ID may be reused after the pending row is gone.

The lock implementation acquires a call's complete set of lock keys together. Overlapping calls are FIFO by creation time and durable insertion order; disjoint calls can run concurrently. The README caps a call at 64 lock keys. The lock set exists in the single-owner process, not across independent daemon processes.

### Direct application to RevDev

This is an excellent reference for bounded background tasks and duplicate-dispatch suppression, but it must **not** replace the RevDev immutable publication ledger.

A suitable RevDev design can borrow:
- stable publication operation ID;
- unique pending-operation constraint;
- write-pending-inside-transaction, dispatch-after-commit;
- explicit resource lock keys;
- FIFO for overlapping mutable resources and parallelism for independent work;
- per-operation checkpoint state.

It must add the guarantees Happy Agent's generic durable function queue does not provide:
- append-only attempts and exact prepared payload bytes survive completion;
- immutable published mission results are not deleted when the pending call completes;
- after an ambiguous external write, recover by exact target read-back, never blindly re-execute mission work;
- the same operation ID cannot silently bind different prepared arguments or payload bytes;
- side effects are idempotent or reconciled, not assumed exactly-once.

**Key lesson:** an idempotent pending enqueue is not proof of idempotent external execution. A durable queue alone cannot prevent a duplicate external side effect across the crash-after-side-effect-before-ack window.

## 4. Event journal: durable replay is not a permanent evidence archive

Happy Agent's event module records ordered UUIDv7 event IDs, timestamps, type and payload. It supports replay by cursor and loads a retained suffix on restart. Its event stream distinguishes persistent events from streamed text fragments, which are not all journaled. The default event window is bounded to 10,000 events and 32 MiB of encoded payload. Individual event payloads have a 5 MiB bound. Old event rows are trimmed as the window advances. The API journal also returns an unavailable result for a cursor that has fallen outside its retained window.

The architecture explicitly states canonical conversation history is independent from the bounded event replay journal. The system uses separate History storage for the exact durable transcript; the event journal is a reconnect/replay mechanism.

### PocketCode and RevDev application

Use a separate event stream for client continuity and progress updates, with:
- stable event IDs and per-session or per-attempt cursor;
- oldest-first replay and bounded page size;
- explicit cursor-expired/retention-gap response;
- duplicate/out-of-order handling on reconnect;
- database-first state mutation and then client presentation;
- snapshot + cursor committed atomically where they represent one checkpoint.

Do not store the only copy of a run receipt, terminal result, stdout/stderr or publication envelope in a bounded event stream. Keep canonical attempt/evidence history in a separate durable record or artifact store. A client must know whether it has caught up or whether a gap requires a fresh authoritative snapshot.

## 5. Process execution: timeout means different things in different APIs

This is one of the most valuable source-level findings, and a common trap if we read only the docs.

### One-shot command path

The host shell's run() calls NativeProcessManager.run(), supplying a default 120,000 ms timeout and a default retained-output cap of 512,000 bytes per stream. The process manager sets a timer; when it expires it sends SIGTERM, then schedules a SIGKILL after the configured grace (normally one second for the generic process manager or two seconds in host-session stop configuration). The result reports timedOut, aborted, and killed separately, in addition to exit code and signal. Output snapshots retain byte totals and omitted-byte counts rather than silently pretending to have complete output.

### Long-running session path

The shell's startSession() creates a background process and returns a stable session ID. Its timeoutMs is **not a kill deadline**. It marks the session as timed out while the command continues. The included test sets timeoutMs to 0, observes timedOut: true, and then verifies the still-running command later completes with the output survived. A client can read deltas, send stdin, stop the session, and recover the final result while the session is retained.

This is intentionally different from the one-shot run() path. UI wording must say whether a wait was exceeded or whether the process was actually terminated.

### Other actual limits

- Host session defaults: 64 active sessions and 64 retained sessions.
- Host one-shot default: 120-second process timeout.
- Host shell retained output default: 512,000 bytes per stream, with total and omitted bytes reported.
- Stopping gives the process tree a grace period before forceful termination (2 seconds in the host-session path).
- Native process kill uses POSIX negative process-group signalling or Windows taskkill /T (with /F for force).
- On session cap, the oldest active background session is evicted and termination is requested; the slot is released immediately while the session remains readable.
- The lower-level host-process adapter has a distinct output delivery buffer and pauses source output when its buffer fills. Do not conflate its 1 MiB chunk delivery threshold with the higher-level shell's retained result cap.

### PocketCode/RevDev application

Represent at least these independent facts:
1. client wait deadline reached;
2. runner deadline fired;
3. cancellation requested;
4. termination signal sent;
5. process or process tree confirmed exited;
6. result collector drained stdout/stderr;
7. cleanup completed;
8. result/artifacts durably committed.

Do not map a phone-side timeout or network disconnect to process termination. A remote PC process continues unless the PC-side supervisor confirms it stopped. Preserve timed_out, aborted/cancelled, killed, and natural exit as separate fields.

## 6. Permissions and sandbox: excellent boundary design, platform-specific proof

Happy Agent centralizes permission behavior. Each tool declares:
- whether its exact invocation must be reviewed in Auto;
- whether approval permits this one execution to run outside the regular sandbox;
- whether it cannot be contained and is unavailable in restricted modes;
- a human-readable description of the exact action;
- whether a read-only reviewer can inspect it.

The four modes are Read only, Workspace write, Auto, and Full access. Auto defaults to workspace-write restrictions and asks a reviewer for selected actions. An allow can elevate only the exact execution where the tool says it needs that privilege; the mode is rechecked immediately before execution and restored afterward. Full access explicitly means restrictions are removed.

Reviewer input is not treated as user authorization. It receives a role-aware transcript; only actual user messages and trusted answers to interactive questions count as authorization. Repository text, assistant text, tool output, arguments and generated summaries do not. Permission arguments are cloned into a bounded immutable snapshot before review. Outcomes distinguish rejected, timed out/unproven and unavailable; they must not all collapse into denial or permission to proceed. A refusal circuit breaker stops an agent that continues trying denied actions.

Sandbox implementations:
- macOS: Seatbelt with closed-by-default rules and writable-root restrictions.
- Linux: Bubblewrap, read-only root, private temp, user/PID/network namespaces, explicit writable roots and managed proxy bridge.
- Other platforms: fallback to Anthropic's sandbox runtime.
- Missing restricted-execution dependencies cause failure with a readable error rather than silent unrestricted fallback.
- MCP calls are treated as external to the local filesystem sandbox and always reviewed in Auto.

### Important testing discipline

The sandbox test file explicitly says that if a nested sandbox cannot even start under the test runner, it is **unproven**, not a pass. It skips the boundary assertions by default but has HAPPY_AGENT_COMPUTE_REQUIRE_SANDBOX=1 to make a probe failure fail the suite in environments where the sandbox is expected to run. Its concrete tests include outside-workspace write denial, in-workspace write allow, explicitly allowed external write roots, and deny-root precedence.

The observed test suite gates restricted sandbox execution on macOS or Linux. It does not claim the same test establishes Windows boundary enforcement. Windows uses the documented fallback path, which needs its own explicit test evidence before we borrow any security claim.

This is a strong model for PocketCode's acceptance semantics: unsupported environment or missing enforcement should be reported as NOT_RUN/UNPROVEN/BLOCKED, never as PASS. Do not copy the sandbox itself before inspecting its platform dependency, licensing, threat model and actual test coverage.

## 7. Database lifecycle and migration patterns

Happy Agent's storage abstraction has additional useful practices:
- one exclusive process-level owner for the durable store;
- database-backed lock, not just an in-memory mutex;
- migration key and success marker committed in the same transaction;
- migration keys form an exact immutable prefix, preventing reorder or rewrite of applied migrations;
- it checks every module migration ledger before applying any migration;
- it refuses to open a database migrated by a newer build instead of silently downgrading;
- before applying migrations, a host callback can record what a rollback/older build must know.

The SQLite process lock is held in a sibling file using a kernel-backed SQLite write transaction. The file can remain after crash, but the actual lock is released by the kernel when the process exits. The path is canonicalized and permissions are restricted. This is a useful pattern for local PC/daemon state. For phone/cloud multi-writer state, a local SQLite lock is not a distributed lock.

**Adopt:** immutable migration history, atomic migration plus marker, preflight whole migration plan, reject unknown newer schema, explicit exclusive store ownership, and restart/crash migration fixtures. For local-only SQLite, process lock should be OS-backed. For remote coordination, use a server transaction or compare-and-swap with explicit conflict behavior.

## 8. Prioritized feature roadmap implications

| Priority | Candidate for PocketCode/RevDev | Reuse basis | Guardrail |
|---|---|---|---|
| P0 | Stable attempt, task and operation identity; event cursor plus authoritative state | Happy session/event identity, MCP Tasks resume handles | The canonical result is not the bounded event stream |
| P0 | Operation-ID duplicate enqueue prevention | Happy Durable Functions unique pending operation | At-least-once after crash; preserve completed immutable history independently |
| P0 | Typed execution timeout, wait timeout, cancellation and confirmed termination | NativeProcessManager + HostShell distinct paths | Never infer process kill from client wait timeout |
| P0 | Exact action-bound permission decision and fail-closed unknown | PermissionsModule + bounded argument snapshot | No stale approval reuse; reviewer unavailable is unproven |
| P0 | Bounded stdout/stderr with raw byte totals and omitted-byte counts | BoundedOutputBuffer + host result | Capture-state is separate from exit outcome |
| P1 | Resource lock keys and dependency-aware bounded concurrency | DurableFunctions lock scheduler | Shared workspace/queue operations serialized; independent read-only analysis may parallelize |
| P1 | Resumable event stream with retention-gap detection | EventsModule cursor replay | Canonical transcript/results remain in durable records |
| P1 | Optional PC daemon API and typed mobile client | Happy Agent headless API architecture | Keep phone useful without PC and preserve adapter/provider neutrality |
| P1 | Explicit workflow recipes and agent harness adapters | Goose recipes + ACP harness matrix in Happy Agent | No automatic untrusted cross-agent delegation or quota bypass |
| P2 | Immutable, versioned schema migrations and DB ownership | AgentStorage / process lock | Do not apply local lock semantics to distributed writes |
| P2 | Remote terminal replay and bounded scrollback | Ghostty remote terminal protocol | A terminal stream is not a task result or verified artifact |

## 9. What we should not adopt

- Do not import the Happy Agent workspace wholesale or couple PocketCode to its package internals.
- Do not use its durable function table as immutable evidence storage. Pending rows are deleted on completion.
- Do not call its task dispatch exactly-once. It explicitly replays work after a crash in the external-side-effect-before-ack window.
- Do not treat its 120-second default as a universal execution deadline. The long-running session path uses timeout as a wait/session marker and keeps the process running.
- Do not treat the bounded event stream as complete permanent history.
- Do not claim the same sandbox proof on Windows as macOS/Linux based only on the cited restricted-command tests.
- Do not import provider-specific prompt/tool implementations or credential readers without an explicit provider strategy and user authorization.
- Do not require a desktop daemon for PocketCode's phone-first/free-tier path.
- Do not rely on Happy Agent's service/team deployment, account system, cloud, or provider usage to meet the $0 default budget.

## 10. Practical next implementation sequence (not authorized in this pass)

1. Keep the PocketCode core task/attempt/result contract provider-neutral and platform-neutral.
2. Add a pure idempotent pending-operation repository contract with operation_id, payload hash, arguments hash, and status. A same-ID/different-payload collision must be conflict, not duplicate success.
3. Add a separately append-only attempt/result journal that outlives pending-work completion.
4. Define local DB transaction semantics for state + event cursor + pending dispatch record.
5. Add crash fixtures at each durable boundary: before commit, after commit/before dispatch, after side effect/before ack, after ack/before projection, and during retention cleanup.
6. Define per-resource concurrency keys and dependency graph. Parallelize independent read-only research, serialize writes to one repo/workspace/branch/queue.
7. Define client wait timeout vs runner timeout vs cancellation vs confirmed process termination as separate contract facts.
8. Implement runner-specific adapters only after the fixed-task comparison selects a legitimate target and its actual capabilities can be tested.
9. Review the resulting architecture with Claude and Gemini before changing a product boundary.

## 11. Verification and non-actions

- Source review only at upstream commit 4c1c2727e9259eb46f29829133144be55754f807.
- The cited upstream tests were inspected, not re-run in this environment. Their presence is source evidence, not independent test execution by this project.
- No Happy Agent files were copied into PocketCode product code.
- No runtime, host daemon, database, provider, sandbox, framework, language adapter or mobile technology was selected.
- No iPhone/Android/Windows/macOS/Linux device execution was conducted.
- No product test suite, paired AI evaluation, live runner comparison or user acceptance experiment was run.
- No protected PR, GitHub Action, deployment, install, account, credential, secret, remote host or paid service was changed or used.
