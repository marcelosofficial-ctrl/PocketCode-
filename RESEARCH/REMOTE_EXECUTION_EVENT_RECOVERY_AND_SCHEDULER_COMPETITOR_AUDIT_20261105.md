# Remote execution, event recovery and scheduler competitor source audit - 2026-11-05

**Status:** Source-level research and design recommendations only. No product integration, package addition, test execution or runtime selection.
**Decision:** Reuse small, proven protocol patterns and test scenarios. Do not import either framework wholesale.

## 1. Executive result

1. OpenHands caller-selected conversation identity plus capability-negotiated retry is a strong model for handling a lost create acknowledgement without creating a duplicate conversation. The client retries only when server info advertises idempotent_conversation_create_v1, reusing the same conversation_id. Its test simulates the server committing the first POST and dropping the response. This is a design pattern for PocketCode command dispatch, not command-level idempotency.
2. OpenHands event storage demonstrates stable event IDs, durable sequence numbers, cursor lookup and parent/branch history. It also bridges missing parent files in some history traversal paths, and its tests expect a file-store listing exception to yield an empty event log. Neither behavior is acceptable for authoritative execution evidence. Missing, corrupt or unavailable history must be an explicit evidence gap, never an empty-history or success inference.
3. Cline's SSH remote environment service provides a concrete remote-host adapter pattern: profiles, connectivity states, host inspection, SSH process/tunnel management, bounded command execution, output limits and cleanup tracking. It is desktop/Node code, not a mobile-ready dependency or security proof.
4. Cline's SQLite scheduler is the strongest bounded-work orchestration reference in this pass: durable run rows, atomic claims, claim tokens/leases, renewal, concurrency limits, state transitions and tests for competing claimers and stale claims. It is useful for RevDev's future scheduler and PocketCode's optional host-side bounded job queue. It is not a replacement for RevDev's immutable GitHub publication journal.
5. Competitor feature breadth is not the objective. MVP remains one end-to-end safe run/inspect/report/AI-correction workflow with trustworthy recovery.

## 2. Pinned source provenance and licenses

### Cline
- Repository: https://github.com/cline/cline
- Reviewed main commit: d3ecc4890e8f9bcb77182b96c77fa90575e8e145
- License: Apache-2.0; license blob 05ae14a377caf4df24e26edde0c4f7b22ef3ef30
- Remote environment: sdk/packages/core/src/remote/remote-environments.ts, blob a632a03c10b07a314a2f5ed4bebe73708fd1b2a4
- Remote environment tests: sdk/packages/core/src/remote/remote-environments.test.ts, blob 4035684f7b22c82755079d059ba957549b36686c
- SQLite scheduler store: sdk/packages/core/src/cron/store/sqlite-cron-store.ts, blob b7e998154891cabcc211923599f75d3d9762e86d
- Scheduler store tests: sdk/packages/core/src/cron/store/sqlite-cron-store.test.ts, blob 368661d40f03f9af9f057db4192c984e1af88735
- Scheduler runner: sdk/packages/core/src/cron/runner/cron-runner.ts, blob ac3cfc3551bb4ad9559030f6532c2d8cf6e8c593
- Scheduler runner tests: sdk/packages/core/src/cron/runner/cron-runner.test.ts, blob a9d11ef4cce1f86f653678472c0bb01a5411dd71

### OpenHands Agent SDK
- Repository: https://github.com/OpenHands/software-agent-sdk
- Reviewed main commit: 7dab3f2f461ffc848d5fab7036badc552a385f43
- License: MIT; license blob b0bd86a6335a564bd3766666bebbf014fd6a8013
- Event store: openhands-sdk/openhands/sdk/conversation/event_store.py, blob 0a42fdf4a851109d6f60c990e621c6e1b654f035
- Event store tests: tests/sdk/conversation/test_event_store.py, blob 5d7eee2924de4d0ba0fa7f4fa640b324b3d663ac
- TypeScript client: clients/typescript/src/client/conversation-client.ts, blob f5639275181c0eab78df2a6acbd894a5da0bb8d2
- Capability declaration: openhands-agent-server/openhands/agent_server/server_details_router.py, blob c293a4b8db031e52b8c8cd0d64410cfc55f26e5a
- Lost-ack retry test: clients/typescript/src/__tests__/conversation-create-retry.test.ts, blob afc865506466da9cc952097fdfaed5eaa0c3d366

Upstream tests were inspected as source evidence. They were not run in this project or environment. Re-pin before implementation.

## 3. Cline SSH remote environments

The service models saved remote profiles and connection states: disconnected, testing, available, connecting, connected and error. A profile includes host/user/port and an optional identity-file path. The service inspects remote platform/architecture/home, starts and owns an SSH tunnel, connects to a remote Hub endpoint, reports connection loss, disconnects and tracks pending remote cleanup. Its command API accepts an executable plus argument array and optional working directory, with bounded process time and output. Source defaults include a 30-second SSH connect timeout, 60-second command timeout, 5-minute upload timeout, 40-second tunnel wait, 2-second Hub shutdown timeout and an 8 MiB combined output cap.

The tests use fake tunnels and injected dependencies, which is useful: connection logic can be tested without a real remote host. They cover connection lifecycle, command construction and cleanup paths.

Adopt:
- provider-neutral remote-host profile separated from task/run record;
- explicit connection state and failure reason;
- distinguish host reachable, runner ready and task accepted;
- bounded command, transfer and tunnel deadlines;
- explicit disconnect/cleanup outcome and pending-cleanup state when remote cleanup is unconfirmed;
- dependency-injected transport, clock and process adapters for deterministic failure tests;
- optional user-owned PC adapter later, never a mandatory PocketCode dependency.

Do not copy or claim:
- Node/desktop implementation with Linux/macOS helper targets is not an iOS/Android implementation;
- SSH success does not prove isolated runner, resource limits, safe workspace or egress policy;
- stdout/stderr/exitCode alone do not satisfy PocketCode's provenance, termination, cleanup, artifact integrity and release contract;
- SSH transport success does not solve command idempotency after lost response;
- profile persistence requires separate mobile keychain/keystore, host-key verification, key rotation, revocation and account-isolation review;
- local tunnel/process timeout does not prove remote process stopped;
- Cline cron runner has unattended tool-policy defaults, including auto-approval when tools are unspecified. Do not transplant this policy into either product.

## 4. Cline SQLite scheduler and bounded claims

The scheduler persists schedule specs, revisions, run rows, status, session linkage and event-ingress records in SQLite. The store exposes claimDueRuns, renewClaim, attachSessionIdToRun and completeRun. Claims carry a token and expiry; the runner periodically renews leases and aborts its active execution path when renewal fails. Store transitions use claim-token conditions so a stale worker cannot legitimately complete a run using an obsolete token. The runner has configurable polling, lease duration, global concurrency and per-spec limits. It persists state transitions and writes a report for completion/failure.

The source uses SQLite transactions, including BEGIN IMMEDIATE around selected multi-step updates. Tests cover peer claim exclusion, lease expiry/takeover and stale claim-token rejection. This is stronger than an in-memory queue or UI-only progress list.

Adoption for RevDev's future bounded-work scheduler:
- immutable RunId distinct from schedule/spec identity;
- durable claim token/fencing generation on every state-changing transition;
- lease expiry and renewal separate from execution status;
- concurrency limits enforced by the store, not only runner loop;
- worker/session association written only if current claim still owns the run;
- stale worker completion rejected after lease takeover;
- durable event/report creation separated from best-effort UI notifications;
- tests with two store clients against the same database and stale claim tokens.

PocketCode relevance is only an optional remote host's bounded queue. Phone command outbox and host execution ledger remain separate.

Limits:
- SQLite is local coordination, not cross-machine coordination. Cline does not prove distributed multi-host fencing.
- Leases do not make external side effects exactly-once. If a worker performs a shell/file/code side effect and crashes before completion is recorded, next worker must reconcile or require idempotency.
- Runner Promise/abort/timeout state is not proof a child or remote process terminated.
- Schedule run record/session ID is not an immutable output receipt or artifact release.
- Unattended permission defaults are unsuitable. Authorization must bind exact task, source, args, workspace, target and policy revision.

## 5. OpenHands event identity, replay and lost-create-ack recovery

The event store assigns durable sequence numbers and exposes get_seq/index_after_seq for cursor continuation. Events have stable IDs and parent IDs for conversation branches. The TypeScript client retrieves events by ID, counts events, sends events, pauses/interrupts/runs conversations and queries final response. The server advertises capabilities through server info.

The create retry is particularly valuable. The TypeScript client probes server capabilities and retries a failed create with the same caller-supplied conversation_id only when the server advertises idempotent_conversation_create_v1. Its test server commits the first POST and drops the response, then checks that retry does not create a duplicate. If capability is absent or cannot be established, client does not assume retry is safe.

Critical caveats:
- Event ancestry traversal can bridge a missing parent event by falling back to preceding surviving event. Useful for conversational context, invalid for authoritative execution evidence. Missing ancestry must be explicit gap/incomplete.
- Event-store tests include a case where file-store listing exception results in a zero-length log. Unsafe for authoritative journal. Storage unavailable, corrupt, partial and genuinely empty must be distinct.
- Event store warns flock locking is unreliable on NFS/network filesystems. Do not infer multi-host correctness from process lock.
- Conversation-create idempotency is not command idempotency. Conversation ID does not identify a user execution command, side effect, attempt or result artifact.
- Cursor is not permanent archive. Retain immutable terminal receipts and artifact refs separately from bounded/rebuildable event streams.

## 6. Provider-neutral PocketCode contract recommendation

Keep six identities/stores distinct:
1. Command outbox: stable CommandId, exact immutable payload digest, workspace/checkpoint ref, target/host identity, idempotency scope, authorization ref and append-only dispatch attempts.
2. Remote execution: HostExecutionId, owner/fencing generation, authoritative execution state, monotonic event sequence, heartbeat, cancellation request and cancellation/termination evidence.
3. Local runner: LocalAttemptId, process/runtime identity, platform scheduling state, interruption reason, checkpoint/resume capability and side-effect uncertainty.
4. Observation sync: per-run cursor, event rows, sequence-gap detection, snapshot catch-up and transactionally committed cursor.
5. Result receipt: immutable terminal observations, raw output/artifact refs, digests, provenance, cleanup evidence and release decision.
6. Workspace checkpoint: snapshot identity, exact coverage and integrity metadata, independent from execution and receipt.

A transport/host adapter should advertise versioned capabilities, for example:
- command_dedupe_by_client_id_v1
- query_command_by_client_id_v1
- ordered_event_replay_v1
- event_cursor_gap_detection_v1
- cancel_request_v1
- termination_confirmation_v1
- artifact_upload_resume_v1
- workspace_snapshot_ref_v1

Missing capability means do not assume behavior. If dispatch acknowledgement is ambiguous and dedupe/query is unavailable, preserve DISPATCH_UNKNOWN / OUTCOME_UNKNOWN and reconcile rather than issuing a fresh command ID or blindly repeating a non-idempotent command.

## 7. Revised cross-project priority

PocketCode P0 before implementation: finish the smallest provider-neutral command/receipt contract, select one viable first execution path only after fixed-task comparison, and prove one vertical slice with real runner observations. Do not expand into multi-agent or generic remote-control features.

PocketCode P1: durable command outbox, authoritative run lookup, replayable observations, result receipts, artifact integrity/release, local interruption and reconnect recovery.

PocketCode P2: optional SSH/remote-PC adapter, schedules/recipes, richer diff review, repository context map and multiple execution backends.

RevDev P0 remains publisher recovery and evidence correctness. Cline claim/lease tests can improve scheduler/worker ownership design, but do not solve immutable publication identity, prepared envelope, GitHub target CAS, accepted-write/lost-ack reconciliation or grouped interaction-cycle correctness. Do not close OD-01…08 or alter P8U/P0-D.

## 8. Product progression and implementation-readiness assessment

This is a planning assessment, not a test result or earned completion percentage.

- PocketCode has a responsive static/simulated UI, requirements/acceptance baseline, provider-neutral draft lifecycle and extensive source-level competitor/security research. It does not have a real runner, production backend, mobile app integration, real execution receipts, selected execution path or demonstrated end-to-end task loop.
- RevDev has a large existing Windows product/repository history and detailed recovery/acceptance investigation, but current PC checkout, installed binary, runtime, publisher parity, queue and writer topology are UNKNOWN. P0 publisher recovery is OPEN and release-blocking; P8U/P0-D are NOT RUN.
- Research branch commit counts are not implementation progress. Design or test proposal is not passing product test.

Indicative programme bar: **about 20% toward a dependable combined product**, with discovery/contract definition substantially ahead of implementation/integration/validation. This is not a claim that 20% of code or features are complete.

PocketCode first usable MVP is **not close yet**. The interface prototype exists, but defining behavior is real guarded execution plus truthful evidence, correction and recovery. Largest blockers are execution-path choice, security/termination proof, durable storage/outbox/receipt, mobile lifecycle integration and hands-on acceptance. Phone-only period makes source research and contract work productive, but prevents device/host verification needed to move those gates.

## 9. Next work order and stop conditions

1. Stop adding broad competitor inventories. Deepen only sources that can change an implementation decision or close a known gap.
2. Prepare a one-page execution-path decision table using existing fixed task: iPhone-native local, browser/Pyodide, user-owned remote PC, hosted sandbox (blocked by $0/no-consent) and manual fallback.
3. Keep UI prototype honest and small. Do not build broad IDE features before a real execution path is selected.
4. After path selection, implement one vertical slice only: project/input -> explicit approval -> run -> actual stdout/stderr/exit provenance -> output artifact -> durable receipt -> AI handoff -> reviewed correction -> linked rerun.
5. Gate every step with existing LOOP/CASE IDs. Do not invent or renumber canonical acceptance IDs.
6. For RevDev, wait for PC-return read-only inventory before backend selection or source edits. P0 publisher remains first.

No code was copied into product code. No upstream tests, product tests, builds, device tests or provider workloads were run by this audit.
