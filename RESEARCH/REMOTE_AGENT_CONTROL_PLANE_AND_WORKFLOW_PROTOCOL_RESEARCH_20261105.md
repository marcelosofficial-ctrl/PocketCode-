# Remote agent control planes and workflow protocols — 2026-11-05

**Status:** Focused desk and source-code research; no hands-on product tests.
**Purpose:** Extend the existing competitor work with newer mobile-first agent control planes and durable workflow protocols. This is not a new product direction or a runtime/provider selection.

## 1. Executive conclusion

PocketCode should **not pivot from its run/inspect/report/iterate hypothesis into a generic remote coding-agent control room**. Happier, Cretli and similar products already provide phone access to agents that continue running on a user's PC or server. They are important alternatives, but that model does not solve the four-month no-PC period unless a reachable host or separate hosted runner exists.

PocketCode's stronger product proof remains:
1. execute a bounded task in a deliberately selected environment;
2. observe truthful output, lifecycle, artifacts and cleanup;
3. create a compact, portable evidence receipt;
4. hand the evidence to the user's chosen AI;
5. review a proposed correction and rerun as a new attempt;
6. preserve task/result continuity without accidentally rerunning completed work.

The AI Workflow Director remains a supporting feature, not the core differentiator. Its future value is to reduce repeated context transfer and improve safe continuation across providers.

## 2. New competitor findings

| Project | What it offers | Why it matters | PocketCode decision |
|---|---|---|---|
| Happier | Desktop, web and mobile control surface for Claude Code, Codex, OpenCode, Pi and many more; connected machines, one session inbox, cross-agent delegation, approvals, voice and encrypted sync | Strongest direct comparison for mobile control of existing agents. It makes multi-agent continuity and approval UX expected capabilities, but still relies on an agent host. | Treat as a benchmark for optional remote-host/session adapters, not a substitute for PocketCode's actual execution proof. |
| Cretli | Self-hosted PWA with phone chat, terminal, files, Git, tasks, browser and pluggable AI harnesses; one live session shared across devices | Demonstrates the breadth of a mobile developer cockpit and workspace tools. It requires a reachable host and exposes a powerful shell. | Do not copy its full-shell model or present remote PC access as PC-less execution. Borrow workspace navigation and session concepts only. |
| agent-device | CLI, MCP server and typed Node API for controlling real devices/simulators and capturing accessibility snapshots and visual evidence | Useful for automated mobile UI testing, device regression and evidence capture. It does not run user code or prove sandbox/process termination. | Keep as an optional future QA adapter if actual iOS/Android UI test gaps are identified. Do not add to MVP dependencies. |
| OpenWOP | Provider-neutral workflow protocol for durable runs, event logs, interrupts, idempotency, replay/fork and conformance | Useful contract patterns for the secondary AI Workflow Director and future cross-provider workflows. | Borrow selected ideas; do not adopt the whole protocol or claim conformance. |

## 3. Happier source audit

Repository: happier-dev/happier, branch dev at inspection.
- README blob: 40da631916aa654cb786b81c68a548706c5795e9
- MIT license blob: da0b4ae30a42be8db9776eb887acb671b19699a0
- session transition cutover source blob: 5ab5524bb633144b8594917ec418a47cff62f5d5
- session forking documentation blob: b56cb175530521da7e69fad2ead7023e20452917
- attach-to-session documentation blob: 500d99fd25efc4d9a8b7af4f95b5451fb1db89fe

### Features worth benchmarking

- One inbox across agents and machines.
- Attach to the same running session from app or terminal rather than creating a duplicate.
- Provider-native attach/resume only when the provider declares and negotiates the needed capability.
- Explicit Native fork / Replay fork / New session strategy. If the user explicitly selects Native and it fails, do not silently substitute Replay.
- Replay seed applied once to a child session, parent transcript visible read-only, no inherited actionable approval controls.
- Permission approval cards are distinct from structured questions that resume the run.
- Stale historical questions are read-only.
- Windows interactive-host modes avoid assuming tmux is available.
- End-to-end encrypted relay is a useful model if PocketCode later adds remote-host control.

### Implementation lesson

The inspected cutover source deliberately commits one current-view write and then uses a separate canonical transcript-message writer. The two operations are not one transaction. It returns an explicit partial outcome if the first committed and the second failed. This is the correct lesson: expose partial state honestly rather than bypass a canonical writer to fake atomicity.

Do not copy the source's owner-only/reserved-ID access argument as a general security pattern. Every PocketCode action still needs its own authorization and host/runtime boundary.

### Product limitation

Happier controls agents running on the user's own machine. It is not a no-host execution environment. A phone can reconnect to an existing session, but the remote agent host still needs to exist and remain available.

## 4. Cretli source and security audit

Repository: cretli/cretli, commit c5e1db2ca77a6d15a2d93ee0796edb8acfebfab6.
- README blob: 04b9587cdce6a4eb65cbc52f78a44ba8c83deb7c
- MIT license blob: 11f9ca2d5115d60e6f0ac761a0795b316dab1010
- architecture blob: 4e8a569db9470890d346a27dec6322d8d2a7475c
- security policy blob: e7b1e47220ed509e96c106e7f930c7eef1b3607b
- delegation tree source blob: 3450f15dfa1d1e75332d2233dbc9d9f8a48c8d5e
- runtime worker source blob: dfe0fc66736a40d53a8d5c6fc5a4b82995213a62
- SQLite delegation store source blob: 25e0d1f2fe6fa78817b21f90ec77fec7f89975d8
- mailbox source blob: efe9ef8c5f168fc62ffd60ddd21a3d391094ef24

Useful patterns:
- explicit parent/child delegation tree, bounded depth and grant attenuation;
- separate progress messages and final reports, linked to attempt identity;
- a mailbox/outbox that avoids starting the parent again for an already acknowledged attempt;
- non-overlapping runtime ticks, dispatch-in-flight accounting, degraded health and bounded backoff;
- SQLite tables for delegations, attempts, outbox, mailbox and idempotency tombstones, with unique idempotency indexes and transactional writes;
- typed corrupt/I/O errors that must not be mistaken for an empty store.

Caveats:
- the JSON atomic-rename path is last-writer-wins across processes and does not merge concurrent writers;
- the in-memory promise-chain lock only serializes one process;
- SQLite is explicitly a single-host/WAL/busy-timeout design and depends on its owner-lock assumption;
- Cretli's security policy says a network-reachable terminal user can execute arbitrary shell commands as the host user;
- Plan mode is not a sandbox for every backend; Codex Plan is prompt-only with broad sandbox access;
- its browser policy explicitly documents residual SSRF/network limitations.

Decision: learn from its session/workspace and delegation UI, but do not adopt its shell exposure, browser boundary or persistence implementation as PocketCode's execution/security design.

## 5. agent-device source audit

Repository: callstack/agent-device, main at inspection.
- README blob: 17c0c4a8f7485290007aca52bd97664257fd81f8
- package.json blob: a39877d3eacfc1bfecd91a484bb76db865f4b8fb
- MIT license blob: e339c7e96e4f372b7f80d7ed7a19570dfc4f336d

The package exposes the same command surface through CLI, MCP and typed Node API. It uses accessibility snapshots and short-lived refs for interaction, then captures screenshots/video as evidence. This is useful for testing a mobile app's actual UI and avoiding screenshot-only agent navigation.

It requires Node 22.12+ and platform-specific helpers. It is not a user-code runner, sandbox, evidence receipt store or process supervisor. It should be evaluated only as a separate test adapter if it solves an identified device QA gap.

## 6. OpenWOP protocol audit

Repository: openwop/openwop, main at inspection.
- README blob: 7cb5e798d11f53ef4ff64cf91d7e8b712b059212
- Apache-2.0 license blob: 09000c90f40b3482291793ee9c850b3af34475da
- idempotency spec blob: 3cb7765c0ff81b68c2ca426974865477c2cb0260
- event spec blob: 0e7c936830c3907ed316bca630e16ce3adf55006
- replay spec blob: 2e51564fc0082a5b52bff6ae6d14e9a1c8e863c2
- conformance spec blob: 68fb2d17c8f1f643c10127ddbc320fd405e1f1b6
- known limits blob: 57703f469b35c69a5b642720e6af507361d1df3e
- durable execution qualification RFC blob: 38b58466f389088110e21a813a72219ad0a2a987

### Concepts useful to the AI Workflow Director

- request idempotency and side-effect/effect idempotency are separate;
- stable business effect identity survives retries; attempt counter is not part of identity;
- an effect is claimed atomically so concurrent duplicate execution cannot both win;
- event log is append-only; UI snapshots are projections;
- human approval, clarification, refinement and cancellation are typed interrupts;
- replay suppresses external effects and reuses recorded outcomes;
- conformance assigns stable requirement IDs and distinguishes blocked, skipped, inapplicable and executed-pass;
- capability discovery must advertise only behavior actually witnessed.

### Important limitations

OpenWOP's own known-limits document says no independent tier-3 host has certified a profile. The only durability rung witnessed was single-instance restart on the steward's reference host; peer resume, multi-instance and multi-region qualification were not witnessed. Some security/idempotency behavior also lacks major-2 behavioral legs.

Decision: use it as a design reference, not as a runtime dependency or evidence that PocketCode has durable orchestration.

## 7. Feature recommendations, in priority order

### P0: Preserve the current core product hypothesis

No pivot away from run/inspect/report/iterate. The differentiator is evidence quality and safe correction, not chat UI alone.

### P1: Evidence-first run history

- list attempts under one task identity;
- preserve exact input/source digest, runtime/environment identity and adapter version;
- show stdout, stderr, lifecycle, exit/outcome, artifacts and cleanup as separate facts;
- clearly mark unavailable/unknown rather than infer facts from client timeout or UI state;
- retain a portable receipt and its source provenance.

### P1: AI correction packet

- compact packet includes original task, exact failure evidence, environment constraints and relevant files;
- separate original run from each patch/retry attempt;
- patch preview and user approval before applying;
- verification run is a new attempt with linked lineage, not a rewrite of the original receipt.

### P2: Provider-neutral AI session continuity

- stable provider/session identity and explicit capability negotiation;
- reconnect to the same session using a durable event cursor;
- approval requests and user questions are different UI actions;
- native fork, replay fork and new session are explicit choices;
- provider fallback must be visible and never silently change a user-selected strategy.

### P2: Optional remote host adapter

Only if the fixed-task comparison shows remote execution genuinely helps. Treat the host as an execution authority; phone disconnect is not process termination. Use authenticated pairing, least privilege, encrypted transport, bounded commands and explicit host-side receipts. Never expose a full shell by default.

### P3: Device QA adapter

Evaluate agent-device only after a real UI regression/evidence gap exists. Keep it outside the user-code execution sandbox and outside the authoritative run journal.

## 8. Code reuse decision

No new upstream code was copied into PocketCode in this pass.

Reasons:
- Happier is a large TypeScript/Expo/Prisma product, not a small reusable runner component.
- Cretli's delegation-tree helper is small and MIT, but encodes Cretli-specific chat row fields and process environment. Porting its invariant is safer than copying it verbatim.
- Cretli's SQLite/outbox implementation is Node-specific and relies on a single-host owner-lock assumption.
- agent-device is an optional external Node test tool, not a PocketCode runtime component.
- OpenWOP's SDK/schema surface is much larger than PocketCode's current contract and its independent-host evidence is incomplete.

This is a deliberate no-copy decision, not a failure to inspect code. Reuse should reduce integration risk, not add a new framework or silently change product boundaries.

## 9. Current gates and non-actions

- PocketCode remains discovery/product-definition stage.
- No production runner, provider, cloud runtime, sandbox or paid service selected.
- $0 default budget remains.
- Fixed-task product comparison and AI Director evaluation remain NOT RUN.
- LOOP/CASE and AWD acceptance definitions remain unchanged.
- No app installed, user code executed, device test run, provider workload or cost incurred.
- No source/runtime/PR/Actions/deployment change. PR #2 and #3 remain protected and untouched.


### Additional OpenWOP secret-digest and assurance caveat

Inspected OpenWOP RFC 0229 at commit ec214ef38d1f515c275abc48194e4ec73ed9d3be, source blob d24e69b086f409a8019a5e644a394efc0ec1ec0b0. It documents a concrete host bug where run-supplied secret values entered a persisted idempotency request digest. The RFC treats a digest as a confirmation oracle and requires secret values to be excluded from persisted/derived digests, not merely hidden in logs. For PocketCode, keep user credentials and secret environment values out of receipts, cache keys, task fingerprints, event logs and AI debugging packets; preserve only safe references or an explicit redacted/unavailable marker.

The same RFC's status history records provisional acceptance pending retrospective review and a steward override of the protocol's own full comment-window rule for a certification/secret-material change. RFC 0156 separately documents the need for independent maintainers, external audit and Tier-3 implementation evidence. Therefore use OpenWOP's technical ideas selectively, but do not equate an Accepted RFC or large conformance corpus with independent security assurance.


## 10. Source-code pass: OpenHands retry/replay and Cline remote/scheduler internals — 2026-11-05

**Status:** Pinned upstream implementation review. This is desk/source inspection, not an integration test. OpenHands and Cline code was inspected on their current `main` refs as fetched on 2026-11-05; re-pin again before implementation.

### 10.1 OpenHands: lost-create-ack protection

Upstream: `OpenHands/software-agent-sdk`, current `main` at `e6c074fe5fd96c6ce0f7a52905d529e27d24bb7b`, MIT.

- `clients/typescript/src/client/conversation-client.ts`, blob `f5639275181c0eab78df2a6acbd894a5da0bb8d2`: conversation creation sends once. It retries after a non-HTTP transport error only when the caller supplied a stable conversation ID and a server-info capability probe confirms `idempotent_conversation_create_v1`. HTTP responses, missing caller ID, and unavailable capability probe surface the original error. A supported retry resends the same payload and ID.
- `clients/typescript/src/__tests__/conversation-create-retry.test.ts`, blob `afc865506466da9cc952097fdfaed5eaa0c3d366`: tests the commit-then-drop-response case, no-capability no-retry, missing-ID no-retry, and HTTP validation no-retry. Inspected, NOT RUN by PocketCode.
- PocketCode adoption: a small isolated adaptation is now in `RESEARCH/vendor/openhands/idempotent_create_retry.ts`; the adjacent README records provenance and limitations. It is reference-only, not imported by product code, and has not been compiled or tested in this pass.

**Mandatory PocketCode constraints around this pattern:** persist one operation ID and exact serialized request before send; same ID + same immutable request replays, while same ID + changed request is an integrity conflict. Retry only against the same server, authenticated principal, tenant/account and explicitly negotiated capability. The server must durably deduplicate the ID and bind it to a canonical request fingerprint that structurally excludes secrets. A client retry helper alone does not make an operation idempotent, and it does not prove exactly-once side effects.

### 10.2 OpenHands: event replay, live stream ordering and ownership

Source map:

| File | Blob | Relevant source-level behavior |
|---|---|---|
| `openhands-sdk/openhands/sdk/conversation/event_store.py` | `0a42fdf4a851109d6f60c990e621c6e1b654f035` | Append-oriented event log, stable on-disk sequence cursor, lookup/index, gaps are not reused, missing event warnings and recovery of surviving ancestry |
| `openhands-agent-server/openhands/agent_server/session_socket.py` | `7d6c7dfad52f1c4352ee339638516be387182ef4` | Replays durable frames with sequence; buffers concurrent live events while history drains; suppresses duplicates at the replay/live boundary; byte-bounded send queue disconnects slow consumers rather than silently dropping durable frames |
| `openhands-agent-server/openhands/agent_server/conversation_lease.py` | `195904d81f340d39480ec94f549892267561e371` | Owner + monotonically increasing generation + expiry, guarded writes, renewal, stale-owner rejection |

Useful design to adopt: durable event rows are the authority; stream frames are delivery. Reconnect by sequence cursor, replay retained history, buffer live delivery during replay, and discard any buffered event already included in the replay. If the stream queue reaches its byte budget, disconnect with a resumable cursor rather than dropping a durable event. Detect sequence gaps and request reconciliation. A snapshot is a current-state projection, not a replacement for event history.

Limits matter. OpenHands documents that `flock` locking for its local FileStore is not reliable on NFS/network filesystems. The inspected source does not establish universal fsync/power-loss durability. Its lease lock is a local coordination design, not proof of a database-backed distributed fencing primitive. Do not transplant this file store or claim its guarantees for OPFS, iOS, Android, Windows, or network storage.

### 10.3 Cline: SSH remote environment

Upstream: `cline/cline`, current `main` at `d3ecc4890e8f9bcb77182b96c77fa90575e8e145`, Apache-2.0.

- `sdk/packages/core/src/remote/remote-environments.ts`, blob `a632a03c10b07a314a2f5ed4bebe73708fd1b2a4`: connection profiles; remote OS/architecture inspection; content-hashed helper binary; temporary upload followed by permission change and rename; remote Hub loopback binding; SSH local tunnel; StrictHostKeyChecking, BatchMode and keepalive; profile file mode 0600 and fsync+rename; persisted cleanup records when remote shutdown cannot be confirmed.
- The source supports Linux/macOS x64/arm64 helper targets. It depends on Node process/filesystem APIs and local SSH. This is a useful remote-host architecture reference, not a ready-made iOS/Android implementation, Windows host implementation, or PocketCode dependency.
- It separates connection loss from remote execution completion. A broken SSH tunnel is not evidence that remote work stopped. The client must reconnect to the same host/session and reconcile status.

Adoption: optional remote-host adapter for PocketCode after a phone-native vertical slice proves its value. Keep the mobile client as observer/controller, and let the selected remote host own long-running work. Make SSH trust, identity binding, helper version/hash, workspace selection, and remote cleanup explicit. Do not auto-install a helper from the network. A later Windows RevDev host adapter must be independently designed and reviewed.

### 10.4 Cline: transactional scheduling and guarded run claims

Source map:

| File | Blob | Relevant behavior |
|---|---|---|
| `sdk/packages/core/src/cron/store/sqlite-cron-store.ts` | `b7e998154891cabcc211923599f75d3d9762e86d` | SQLite `BEGIN IMMEDIATE` claims, global/per-spec concurrency checks inside the write transaction, claim token + expiry, token-conditional renew/complete/requeue/session attachment; event transaction helper |
| `sdk/packages/core/src/cron/events/cron-event-ingress.ts` | `a8947d78724477aab40a3641db46ecbd14f9c76c` | Event acceptance, event deduplication and all matching-run materialization inside one transaction; rollback allows safe redelivery after a partial fan-out failure |
| `sdk/packages/core/src/cron/runner/cron-runner.ts` | `ac3cfc3551bb4ad9559030f6532c2d8cf6e8c593` | Polling separated from long-running execution; claim renewal; abort on lost lease; status is persisted before optional report creation; report-write failure is logged without replaying a completed agent turn |

Adopt concepts: atomic queue materialization; single-transaction global and per-project capacity checks; attempt-counted claims with a fresh ownership token; renew before expiry; condition every state transition on the current token; and persist canonical terminal status before writing a derived Markdown report or dashboard projection.

Do not overclaim. The claim token fences the scheduler database row, not arbitrary shell, filesystem, network or Git side effects. Abort is cooperative. The inspected scheduler does not establish idempotent session-start behavior after a start request reaches a remote runtime but its acknowledgement is lost. An expired lease can prevent stale database updates while a stale worker may still be completing a non-fenced external effect. PocketCode must reconcile the remote command identity and effect before dispatching anything again.

**Security rejection:** Cline's headless `buildToolPolicies` defaults to wildcard auto-approval when a schedule omits its tool list. Explicit tool lists disable the wildcard, but the no-list branch is too permissive for PocketCode/RevDev unattended execution. Do not copy that policy. Our unattended execution must be default-deny, with a bounded explicit capability list, exact target/workspace binding, policy revision binding and approval expiry. A missing policy is a block, not "approve all".

### 10.5 Cline: stale UI transition fencing

`apps/vscode/src/sdk/sdk-task-control-coordinator.ts`, blob `5054e8f18398160232264c59ea0197c870ff10f1`, increments a task-view generation before async history reads and checks the generation after awaited steps. Its cancel fence is raised synchronously before the abort request so late events from the old task view cannot overwrite the new state.

Adopt for PocketCode navigation/state projection: project switch, attempt selection, reconnect bootstrap and tab changes should allocate a generation synchronously; stale async results may be observed/logged but must not repaint or mutate the newly selected view. This is a UI consistency fence, not remote execution fencing or command idempotency.

### 10.6 Protocol interpretation: ACP and MCP Tasks

The live protocol documents clarify three distinct layers:

- ACP v2 `session/resume` restores an agent session and optionally replays retained conversation updates from a replay cursor. It requires a current-state snapshot before the resume response. This is a session/context adapter; it is not a durable PocketCode command identity or a guarantee that a side effect ran once. Unsupported replay cursors must be rejected, not silently downgraded. ACP `session/cancel` concerns foreground work; background work may continue, and clients should wait for the cancelled idle-state update before treating the cancellation as confirmed. [ACP session setup](https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/protocol/v2/session-setup.mdx) [ACP schema](https://github.com/agentclientprotocol/agent-client-protocol/blob/main/docs/protocol/v2/schema.mdx)
- MCP Tasks provides a durable server task handle, status polling and final result retrieval. Its cancellation acknowledgement is only an intent signal: processing is eventually consistent, the task may remain working, and cancellation is cooperative rather than guaranteed. Persist task IDs locally and reconcile; do not treat the cancel response as proof of termination. [MCP Tasks specification](https://modelcontextprotocol.github.io/ext-tasks/specification/2026-07-28/tasks.html)
- Neither should replace a product-level identity split between user command, remote execution, runner attempt, external effect, event observation and result receipt.

### 10.7 PocketCode contract direction

Before selecting an adapter, require the following transport-neutral behavior:

1. **Dispatch identity:** stable `CommandId` + immutable, secret-free request descriptor/body + target/account scope + workspace/checkpoint identity + policy revision. A unique `DispatchAttemptId` records each transmission. A server-issued `ExecutionId` is a different identity.
2. **Ambiguous acknowledgement:** after send may have reached the host but no durable acknowledgement was recorded, enter `DISPATCH_UNKNOWN`. Query by the same `CommandId`. Retry the exact same bytes and ID only if the host explicitly guarantees idempotent create for that scope. Never mint a replacement ID or silently replay a shell task.
3. **Execution evidence:** host reports monotonic sequence, execution lifecycle, heartbeat, cancellation request and observed result separately. Event rows and cursor advance commit atomically. Sequence gaps trigger replay/reconciliation, not a fabricated continuous stream.
4. **Transport recovery:** reconnect session, recover current snapshot, replay from supported durable cursor, merge live updates without duplicates. Stream overflow drops the connection with cursor retained; durable events are never silently skipped.
5. **Cancellation:** request, acknowledgement, observed termination and final result are separate facts. A client timeout, tunnel loss or cancel acknowledgement does not prove process termination.
6. **Result:** persist immutable execution receipt before deriving portable report. Artifact transfer/release acknowledgement is separate from execution completion.
7. **Capability negotiation:** explicit versioned flags for idempotent create, replay cursor, cancellation confirmation, result retention, and artifact resume. Unsupported means unavailable, not best-effort.

Candidate statuses remain design vocabulary, not frozen enum or acceptance IDs: `QUEUED_LOCALLY`, `DISPATCH_UNKNOWN`, `ACCEPTED_REMOTE`, `RUNNING_REMOTE`, `RUNNING_LOCAL_FOREGROUND`, `LOCAL_INTERRUPTED`, `AWAITING_RECONCILIATION`, `SUCCEEDED`, `FAILED`, `CANCELLED`, `OUTCOME_UNKNOWN`.

### 10.8 RevDev boundary reminder

Cline's queue/run store is not RevDev's GitHub publisher journal. A run claim, session ID, event cursor, or terminal Markdown report does not prove a Git ref moved. RevDev still needs a prepared immutable publication envelope, operation/effect identities, durable send-boundary observation, exact remote read-back, branch-head race handling and stale-writer fencing. Likewise, a successful Git commit/read-back does not prove a runner receipt or exactly-once mission execution. Preserve the existing RevDev P8U/P0-D/OD register and keep publication recovery separate from PocketCode command dispatch.

### 10.9 Evidence limits and non-actions

Upstream source and tests were inspected; no OpenHands/Cline test suite was run in this pass. The small OpenHands helper was added only under `RESEARCH/vendor/openhands/` with provenance. It is not product integration. No production source, product tests, runtime, provider, sandbox, runner, credential, remote host, device, job, queue, workflow, PR, release or deployment was touched. PocketCode fixed-task comparison and EVAL-06 remain NOT RUN. Canonical LOOP/CASE IDs and owner-open D-01…D-08 are unchanged.


### 10.10 Targeted upstream regression-test review

The following tests were inspected at the pinned repository heads, but were NOT run by PocketCode:

| Upstream test | Blob | What its assertions demonstrate |
|---|---|---|
| OpenHands `clients/typescript/src/__tests__/conversation-create-retry.test.ts` | `afc865506466da9cc952097fdfaed5eaa0c3d366` | Commit-then-drop acknowledgement retries only with the advertised ID-dedupe capability; no retry without capability, caller ID, or on HTTP validation error |
| OpenHands `tests/agent_server/test_session_socket.py` | `f172870f169bc4e1addcc307ee81eb7288b1da5b` | Durable sequence frames; no duplicate at replay/live boundary; sequence survives a lost event file; persisted state-update events are deduped; slow socket disconnects rather than stalls publisher |
| OpenHands `tests/agent_server/test_conversation_lease.py` | `c4b9083d3a2dc343b133046aa3a7f3f610cbad6f` | Lease renewal, live-owner rejection, takeover generation increment, stale owner blocked from guarded writes and old owner release cannot remove new owner lease |
| Cline `sdk/packages/core/src/remote/remote-environments.test.ts` | `4035684f7b22c82755079d059ba957549b36686c` | Process output limits/termination, delayed SSH diagnostics, cleanup persisted after tunnel loss, cleanup recovery after helper removal, private atomic profile writes, strict SSH flags, content-addressed helper, loopback tunnel, concurrent-connect reuse and failed switch rollback |
| Cline `sdk/packages/core/src/cron/events/cron-event-ingress.test.ts` | `91b7ebc263a7c514233b7c5c87e3f5b04e29ae94` | Injected first-run/second-run/status-write failures roll back event and fan-out; store is reopened before redelivery; only one complete fan-out remains; peer connection cannot observe partial acceptance |
| Cline `sdk/packages/core/src/cron/store/sqlite-cron-store.test.ts` | `368661d40f03f9af9f057db4192c984e1af88735` | Spec and run persistence, uniqueness and schema-migration regression cases. Further claim tests exist later in this file but were not fully enumerated in this pass |
| Cline `sdk/packages/core/src/cron/runner/cron-runner.test.ts` | `a9d11ef4cce1f86f653678472c0bb01a5411dd71` | Other schedules progress while one turn is pending; expired claim does not immediately duplicate same-spec work; normal success/error/report paths and concurrency capacity are exercised |

Additional Cline security evidence: the runner test explicitly asserts the default `toolPolicies["*"]` is `{ autoApprove: true }` for an unattended one-off run with no explicit tool list, and that the ASK tool is disabled. This is a concrete tested behavior, not an inference from naming. It is unsuitable for our security posture and is explicitly rejected above.

Test-coverage caution: the inspected `cron-runner.test.ts` normal path asserts a Markdown report exists. I did not find a specific injected report-writer-failure regression in the inspected test portions. The source ordering and changelog statement support the intended no-replay behavior, but the upstream failure-path test coverage is not established here. Treat it as an adoption test requirement, not as upstream-tested proof.

All test results above are upstream source assertions inspected only. They are not results run by us and do not prove platform parity, power-loss durability, provider correctness, production integration or our acceptance suites.


### 10.11 Final durability nuance and claim-test scope

A closer read of OpenHands' actual storage adapter tightens the durability statement:

- `openhands-sdk/openhands/sdk/io/local.py`, blob `b31d270068557f125b45e48095c7ebbc3c0825fc`, routes text writes through its `atomic_write_text` helper, then updates its in-memory cache. That helper writes a same-directory temporary file, flushes/fsyncs the file and replaces the target. It does not fsync the parent directory after rename. Binary writes use a direct `open(..., "wb")` + `write` path and are not atomic through this method.
- `EventLog.append` acquires the FileStore lock, writes one event file, updates in-memory indexes and then best-effort advances a sidecar length marker. Marker update errors are logged and swallowed; the marker is an optimization, and a later disk scan can recover the event file. This is not a multi-record transaction with a conversation snapshot, and it does not establish power-loss durability of the directory entry.
- `LocalFileStore.lock` uses `FileLock`; the code and base interface explicitly warn that flock/file locks do not work reliably on NFS/network filesystems. The implementation's cache assumes exclusive access to the files and can become stale under external modifications.

Conclusion: OpenHands is a useful local event-history/replay implementation, but do not copy its persistence layer as a durability proof. PocketCode must test the selected backend's actual write/rename/commit/fsync behavior on each supported platform, after process crash and power loss if those guarantees are required. Event ordering, event append, index rebuild, cursor retention, and durable commit are different properties.

Cline claim-test boundary:
- `sqlite-cron-store.test.ts`, blob `368661d40f03f9af9f057db4192c984e1af88735`, explicitly tests one due claim, then reclaims the same run after lease expiry with a new claim token and incremented attempt count. It also exercises the bun:sqlite capacity case via two sequential claim calls (`[1, 0]`), not a demonstrated simultaneous multi-process race in the test reviewed.
- `cron-runner.test.ts`, blob `a9d11ef4cce1f86f653678472c0bb01a5411dd71`, forces a live run's lease expiry while its turn is blocked and verifies another schedule can progress; it does not establish that a stale process's arbitrary external side effect is fenced.
- `cron-event-ingress.test.ts` does include a second SQLite connection and verifies no partial event/run fan-out becomes visible. That is useful transactional isolation evidence, but it is not a multi-host queue claim or publisher-target fencing test.

Do not call Cline's claim protocol distributed exactly-once execution. Its transaction and token semantics are strong inspiration for local shared-store claims, bounded concurrency and transactional ingress, but production multi-process/multi-host proof remains an implementation-specific acceptance requirement.
