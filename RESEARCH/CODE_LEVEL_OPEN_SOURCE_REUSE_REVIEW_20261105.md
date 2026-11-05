# Code-Level Open-Source Reuse Review — Mobile Execution, Recovery and Multi-Pass Work

**Review date:** 2026-11-05  
**Status:** Source-level research plus one isolated reference-code copy and test. No PocketCode product integration, runtime choice, provider choice, or implementation approval.  
**Scope:** Deepen the existing competitor survey by inspecting the implementation and tests behind durable task recovery, mobile execution, offline synchronization, task recipes, approvals, and correction loops.

## Executive decisions

1. **Keep PocketCode's execution contract provider-neutral.** Do not adopt an agent framework, execution host, or remote relay wholesale. The product still has no selected PWA/native framework, runtime, host, backend, or sandbox.
2. **Treat MCP Tasks as an optional adapter, not the product's task model.** Its client is a useful reference for durable remote task handles, resume identity checks, terminal-result retrieval, cancellation capabilities and polling cadence. Local runners and non-MCP backends must continue to work.
3. **Adopt Happy's durable-sync invariants, not its whole app or generic outbox.** Persist before send, acknowledge the exact mutation ID, commit snapshot and cursor together, and protect newer pending state from late acknowledgements. Do not coalesce or delete immutable execution/publication evidence.
4. **Adopt Goose's recipe and approval concepts, but constrain parallelism.** Parameterized, versioned task recipes are a strong fit for bounded multi-pass work. Separate contexts and typed outputs are useful. Parallel work must be explicitly bounded and restricted to independent work; shared workspace mutations remain serialized.
5. **Use A-Shell as a local-iOS execution comparison, not a security template.** Its relay has TLS, optional mutual TLS, bearer-token authentication and output limits, but source/docs expose no execution deadline or client cancellation. It executes with the app's permissions.
6. **Build PocketCode's differentiation around evidence and recovery.** Mobile Python, remote-control UI, task recipes, permission prompts and progress indicators all exist elsewhere. The stronger product hypothesis is a trustworthy, portable run receipt and safe continuation after interrupted work.

## 1. Source-level review and pinned references

The following source was retrieved from public GitHub repositories. Blob hashes pin the individual files; repository commits pin the reviewed tree. Upstream descriptions are distinguished from source/test observations.

| Project | Reviewed source | License | Useful area |
|---|---|---|---|
| MCP Tasks | `modelcontextprotocol/ext-tasks`, commit `cc9aaac1047a9440b07486e38f37060bbebeef4c`; `execution.ts` blob `60f097b5accc6e4582f57ac7d8c8215a2357202e`; `task-controller.ts` blob `2715ab00112ac33f4caac91f3bcc2d025b718b33` | Apache-2.0 | Long-running task references, polling, cancellation and resume |
| MCP Tasks tests | `task-resumption.test.ts` blob `c875436e52997ba8c2870c77193c65d767c61067`; `task-lifecycle-races.test.ts` blob `0760147a93132916687100397b2c87cc8b1acfb6` | Apache-2.0 | Persistence-before-detach, endpoint/generation/operation mismatch, lifecycle races |
| Happy | `slopus/happy`, reviewed main commit `f5816cb8cf0621a6499b71dc97fe840a0e0656c2`; `SyncStorage.swift` blob `d924f3b850d37a1a2af545eec5a9d9f35537e7bb`; `IntentOutbox.swift` blob `6b428b6a9f4f49e329c34f101fc9f909b5919194`; protocol blob `4701e53c71810652cae547454320713efcc44701` | MIT | Offline-first intent delivery, durable cursors, monotonic updates and optimistic concurrency |
| Goose | `aaif-goose/goose`, reviewed commit `bfe8ccd23de1d2c47a4cb2970d522f093ae7f2ba`; subrecipe guide blob `8064d1dafb2f8071c784d674358fa6c54f4af44f`; parallel guide blob `6100b3d462c553a5e4c6022aa84908f15edc984f` | Apache-2.0 | Parameterized recipes, delegated subrecipes, approvals and bounded parallel analysis |
| a-Shell | `holzschu/a-shell`; `Relay.swift` blob `46b2956a8085faa9578d365523685e8834e58cab`; `tests/relay.sh` blob `004e1e913ac8691a4b48bf4287402d1d16e9901c` | BSD-3-Clause | Local iOS terminal and optional authenticated command relay |
| Aider | `Aider-AI/aider`, reviewed main commit `5dc9490bb35f9729ef2c95d00a19ccd30c26339c`; `aider/linter.py` blob `d386696e50fdd2d75bdbc40184b4732b09f21a8b` | Apache-2.0 | Bounded lint/compile diagnostics and correction feedback |
| OpenHands | `OpenHands/OpenHands`; session activity store blob `91686f19e7b0840a350e0f349fe0a5399dbb9451` | MIT | Validated, bounded presentation history for task initialization/resumption |

## 2. MCP Tasks: durable remote work without making MCP mandatory

### What the code actually does

The versioned extension provides a client-facing task lifecycle for long-running MCP tool calls. The inspected task controller:
- negotiates task capability generation and selects the matching protocol path;
- exposes snapshot, result, cancellation and input-update operations only where the negotiated capability permits them;
- binds operations to the connected endpoint and task ID;
- uses abort signals around lifecycle-sensitive operations;
- polls until a terminal task state before attempting result retrieval;
- treats cancelled/failed task states distinctly from a successful terminal result.

The v1 code deliberately waits for a terminal state before reading the result because the v1 result endpoint can reject non-completed tasks. Calling it directly for a cancelled task could turn the true cancelled outcome into a misleading failure.

### Recovery tests worth adopting

The source tests are more useful than the protocol name alone:
- a serialized task reference must be persisted before the running client detaches; if persistence fails, detach does not occur;
- resume rejects endpoint, protocol-generation and original-operation mismatches before making a remote request;
- resumed work must not accidentally route new, evidence-free initiating input into the old task;
- lifecycle tests cover polling cadence, abort cleanup, single ownership of update streams and races during task settlement.

**PocketCode use:** an optional remote-task adapter can persist a stable handle, detach the UI, and later resume observation/result retrieval. Persist the handle and its binding before detaching. A resume operation must validate endpoint, protocol generation and original operation before dispatch. Resume observation; do not reissue the initiating tool call.

**Limit:** MCP Tasks does not execute code, provide a sandbox, prove process termination, or replace PocketCode's execution receipt. The extension is evolving and versioned. Its package must not become a mandatory dependency for local Python, browser/WASM or other non-MCP runners.

### Isolated copied helper

A small helper was copied into `RESEARCH/vendor/mcp-tasks/`:
- `task_poll_interval.ts`
- `task_poll_interval.test.mjs`
- `README.md`
- `LICENSE`

The copied source is only the upstream `MIN_TASK_POLL_INTERVAL_MS`, `DEFAULT_TASK_POLL_INTERVAL_MS` and `taskPollInterval` function, with provenance retained. It chooses a 1,000 ms default when no server hint exists and floors server-supplied hints at 10 ms. The upstream code explains that a 10 ms default would produce 100 requests per second per task.

Local isolated verification: Node.js 22.16.0, command `node --experimental-strip-types --test task_poll_interval.test.mjs`, **3 passed, 0 failed, 0 skipped**. The Node type-stripping warning is expected for that test command. The tests cover the extracted helper only.

Before any product use, validate the protocol hint at the adapter boundary as finite and non-negative, apply a platform timer ceiling separately, and use polling only when an authoritative push/event stream is unavailable. The copied helper does not validate untrusted data, cap very large values, schedule requests, retry, cancel, or create durable state. It is research-only and is not imported by product code.

## 3. Happy: durable synchronization patterns and the outbox trap

### High-value implementation details

The protocol separates persistent update events from ephemeral presence/usage. Persistent events carry monotonic sequence numbers; versioned mutable fields use `expectedVersion` and explicit version-mismatch responses.

The inspected SQLite/GRDB storage shows several concrete invariants:
- conversation snapshot data and its cursor are committed in one database write, so a restart cannot resume past data that was not persisted;
- a pending setting is written with a unique mutation ID before it is shown or sent;
- a late acknowledgement removes only the exact mutation ID it answers, so it cannot delete a newer local intent for the same key;
- a newly arriving older conversation cannot reclaim ownership from a newer conversation, and ownership validation is not separated from the SQLite write by an async suspension;
- message enqueue uses a stable ID and `INSERT OR IGNORE`, so a duplicate enqueue does not mutate the already stored payload.

Happy's intent outbox also uses a stable ID, an in-flight set, oldest-first delivery, typed permanent refusal, transient backoff and exact-ID removal after a successful delivery.

### What not to copy

Happy's outbox intentionally stores one action per logical slot. A newer rename/archive action can replace an older pending action in that slot, and acknowledged items are removed. That is sensible for coalescible user interface intents. It is **not** suitable as the authoritative journal for PocketCode execution attempts or RevDev immutable mission publication, where every attempt and every original terminal result must remain recoverable.

**Adopt the invariants, not the storage class:** durable-before-send, stable operation/mutation ID, acknowledgement scoped to the ID it answers, atomic snapshot/cursor persistence, monotonic version checks, and separate durable events from ephemeral presentation. For immutable results, keep append-only history and never coalesce.

## 4. Goose: recipes, approvals and parallel work

Goose's recipe docs describe reusable parameterized tasks. A main recipe can call subrecipes, each in a separate session with isolated conversation context. Parameters can be required, optional or fixed; predefined values take precedence over values inferred from conversation. Subrecipes cannot define further nested subrecipes.

Its documentation explicitly marks subrecipes and parallel subrecipe execution experimental. The parallel-work guide documents up to 10 concurrent isolated workers, but recommends sequential execution when shared resources, ordering or memory/CPU limits matter. Different subrecipes are sequential by default unless explicitly requested in parallel; repeated instances of the same subrecipe can run in parallel by default.

The inspected approval implementation separates:
- **Allow:** mark the exact tool request executable;
- **Deny:** return an error response with a reason;
- **Ask:** keep the request non-executable and emit an approval request tied to that request ID, tool name and arguments.

### PocketCode/RevDev application

A versioned task recipe is a better fit for the AI Workflow Director than copying a general-purpose coding agent. A recipe should declare:
- task goal and bounded scope;
- required and optional inputs with validation;
- allowed tools/actions and explicit deny/ask policy;
- maximum passes/steps and a cancellation condition;
- output schema and required evidence;
- dependencies among steps;
- whether each step is safe to run in parallel.

Use separate context for independent read-only analysis, security review or test-plan construction. Serialize modifications to a shared workspace and operations whose order matters. Never let a subagent's unverified statement become accepted evidence.

Every approval should bind to the exact operation ID, target resource, argument hash, session/task, current policy version and expiry. A stale approval must not authorize changed arguments.

## 5. a-Shell: real local iOS runner, useful capability baseline and warning

a-Shell demonstrates a practical local iOS development environment: terminal windows, command history/current directory, Python and other interpreters, document-picker bookmarks, user-configurable toolbar, Apple Shortcuts, and file transfer commands. This proves that local code execution and file workflows already exist on iOS; they are not PocketCode's differentiation by themselves.

Its optional relay is implemented in Swift, not merely described in marketing:
- HTTPS/TLS, configurable numeric bind address, bearer token and optional mutual TLS with an enrolled client CA;
- loopback bind and mutual TLS are the defaults in the inspected configuration;
- separate noninteractive execution session with stdin attached to `/dev/null`;
- stdout/stderr are captured separately, with an 8 MiB per-stream output limit;
- queue is bounded, with a maximum of eight outstanding requests;
- the shell test exercises success, non-zero status, piping, large output, missing/invalid token and missing client-certificate behavior.

The same source prints `execution timeout: none` in its status description. Its README states there is no execution timeout or client cancellation; a silent long-running command can occupy the queue, and disconnecting or turning off relay does not stop a command already running. The relay executes with the app's file and network permissions and is not a restricted shell or sandbox. An HTTP 200 response also carries a separate command `status`, so HTTP transport success is not the same as program success.

**Decision:** keep a-Shell in the fixed-task comparison as an iOS local-runner baseline. Do not copy its relay or claim it as a security pattern. A future PocketCode runner needs independently demonstrated execution deadline, cancellation/termination semantics, process isolation, output/resource caps and honest background behavior before it can claim those capabilities.

## 6. Aider and OpenHands: useful supporting patterns

Aider's inspected Python linter combines a syntax/tree-based check, Python compilation and selected Flake8 diagnostics. It returns file/line context so the coding agent can make a targeted correction. Its editing path asks before creating files or editing files that were not part of the active context; its shell-command path uses an explicit confirmation.

**Adopt:** after a user-approved change, run only a bounded set of available checks and return exact diagnostic output and file/line references to the correction step. A check that was unavailable or not run must remain visibly unavailable/not run. Preserve a visible diff and a reversible checkpoint before mutation.

OpenHands' inspected session-activity store validates recovered data, bounds history to 100 conversations, deduplicates repeated progress observations, and completes only the matching activity ID in the expected phase. It stores presentation activity in `sessionStorage`, not an authoritative durable execution journal.

**Adopt:** bounded progress UI, explicit pending/connecting/complete/failed phases and ID-scoped transitions. Do not elevate browser session history to authoritative run evidence.

## 7. Product feature priorities from this research

| Priority | Feature | Why it is genuinely useful | Evidence gate before adoption |
|---|---|---|---|
| P0 | Stable task/attempt/step/operation identity and append-only evidence | Prevents duplicate work, ambiguous recovery and unsupported "done" claims | Pure contract tests, crash/restart fixtures and operation-identity collision tests |
| P0 | Interrupted/unknown state with no blind replay | Protects side-effecting work when the app, network or host disappears | Demonstrate recovery after each durable-write boundary; unknown side effects must be reconciled |
| P0 | Durable-before-detach task handle | Lets the phone leave a long-running remote task and reconnect later without losing identity | Persistence failure blocks detach; resume rejects endpoint/protocol/operation mismatch |
| P1 | Offline-first user-intent outbox | Queues harmless user instructions and handoff actions through unreliable mobile connectivity | Stable IDs, exact-ID acknowledgement, bounded retry, visible refusal and no loss under concurrent enqueue |
| P1 | Parameterized task recipes and bounded substeps | Turns one instruction into a repeatable multi-pass workflow with less repeated prompting | Recipe schema, preflight, maximum steps, typed outputs, explicit per-step evidence |
| P1 | Operation-bound approvals and reversible workspace edits | Avoids stale approval and allows recovery without losing the reasoning context | Single-use approval binding and tested checkpoint/rollback for tracked and untracked files |
| P1 | Diagnostic feedback loop | Sends useful compiler/linter/test failures back to the correction phase | Actual bounded test output, exact file/line diagnostics, no invented pass |
| P2 | Realtime sync with cursor/backfill | Makes phone UI recoverable after backgrounding and reconnect | Atomic snapshot/cursor persistence, monotonic event order and stale-version conflict tests |
| P2 | Runner capability/diagnostics screen | Shows what a chosen runtime can really enforce | Each capability backed by a source/device test or marked unknown/unavailable |

### What should not be added yet

- A mandatory MCP server or MCP Tasks dependency.
- A full Goose, Happy, Aider, OpenHands, Cline or LangGraph framework dependency.
- A generic subagent swarm or unbounded parallel worker queue.
- A remote execution relay before the fixed-task comparison proves the need and a credible isolation design exists.
- More receipt fields that no selected runner can authoritatively populate.
- A provider API integration that would make the $0/manual AI handoff path second class.

## 8. Updated decision for the fixed-task comparison

Retain the existing fixed CSV-to-JSON task and existing evaluation worksheet. Do not add a new competing task fixture. Keep the current comparison focused on the same input and outputs across the already listed execution options.

Include a-Shell as an additional iOS local-runner reference only if a legitimate test device/app is available. Its documented lack of deadline/cancellation must be recorded as a capability limitation, not silently normalized away. Continue to distinguish:
- whether the task runs successfully;
- whether output and generated files are faithfully captured;
- how interruption/recovery behaves;
- what isolation and limits are actually enforced;
- setup effort and total cost.

A native or simulated screenshot is not execution evidence. A code-path review is not device verification. No new execution comparison was run during this research pass.

## 9. Non-actions and verification boundaries

- One MCP Tasks helper was copied with Apache-2.0 license and source provenance into `RESEARCH/vendor/mcp-tasks/`.
- Its isolated Node test passed 3/3. Existing OpenHands and mini-coding-agent helper test results remain separately recorded in `RESEARCH/vendor/REFERENCE_COPY_TEST_RESULTS_20261105.md`.
- No source product imports the copied helper.
- No PocketCode runtime, language framework, provider, backend or sandbox was selected.
- No device runner, browser runner, hosted service or actual AI assistant evaluation was executed.
- No canonical LOOP/CASE wording, expected value, test identity, release gate or protected PR was changed.
- No credentials, accounts, paid services, installations, workflows, PRs or deployments were used or modified.


## 10. November 5 competitor capability refresh: mobile agents are now a direct baseline

This refresh adds current official product documentation to the pinned source review above. These are public product capabilities, not hands-on tests.

### Claude Code mobile and remote control

Anthropic's current help material describes the Claude mobile app's Code tab, remote control of a local Claude Code session from phone/web, session teleport between mobile/web/desktop/terminal, and cloud-scheduled jobs. Availability differs by plan and CLI version. The important architecture distinction is that remote control exposes a session running on the user's computer; it does not make the phone an independent execution host.

**PocketCode decision:** remote PC/CLI control remains an optional adapter, not the product foundation. The phone-first workflow must still function with explicit paste-to-context and an approved local or remote runner. Do not claim a remote-controlled host is available when PC state is UNKNOWN.

Source: https://support.claude.com/en/articles/14554000-claude-code-power-user-tips

### GitHub Copilot coding agent on GitHub Mobile

GitHub documents starting coding-agent work from GitHub Mobile, selecting a repository and prompt, letting the agent work in the background, creating a draft PR, receiving a notification when ready, and tracking active agent tasks in a centralized Agents view. Current GitHub Copilot product material also describes per-task sessions, cross-surface continuation, scheduled/triggered automations and code review.

**RevDev decision:** adopt the product pattern of one visible durable task/session per bounded work packet, background progress, a centralized work queue and an explicit review gate before publication. A generated draft PR is not proof that the work is correct, accepted, merged or deployed. Keep current PR protection and explicit authorization boundaries intact.

**PocketCode decision:** a task inbox and resumable attempt list are useful only if they display the same authoritative task/attempt identity and evidence receipt as the runner. Do not add a cosmetic agent inbox that merely mirrors chat sessions.

Sources:
- https://github.blog/changelog/2025-09-24-start-and-track-copilot-coding-agent-tasks-in-github-mobile/
- https://github.com/features/copilot

### Replit mobile

Replit advertises a mobile app for building web apps with Agent, viewing progress, deploying to a live URL and continuing on desktop. Its current mobile page distinguishes native iOS app development, for which the full workflow is directed to the web/desktop path.

**Decision:** Replit demonstrates that mobile-first AI-assisted web-app creation and deployment are established features. It does not remove the gap PocketCode is testing: faithful execution evidence, portable results, recovery and controlled correction across arbitrary small tasks. Do not compete by copying its hosted web-app builder or deployment model.

Source: https://replit.com/products/mobile

### Goose recipes and bounded parallelism

Current Goose documentation describes recipes that bundle instructions, parameters, activities, extensions, model/provider settings, structured response schemas and subrecipes. Its parallel subrecipe execution is explicitly experimental, supports up to ten concurrent workers, and recommends sequential execution when shared resources, ordering or resource limits matter.

**Adopt the useful product shape, not the full Goose runtime:** a versioned task recipe should declare validated inputs, bounded steps, tool permissions, step dependencies, expected evidence, structured outputs, maximum pass count and whether a step is safe to parallelize. Independent read-only research/review may run concurrently; mutations to a shared workspace, branch, queue, immutable result or mutable pointer must be serialized or guarded by explicit concurrency policy. Every delegated result remains untrusted until reconciled against evidence.

Sources:
- https://goose-docs.ai/docs/guides/recipes/
- https://goose-docs.ai/docs/guides/recipes/recipe-reference/
- https://goose-docs.ai/docs/tutorials/subrecipes-in-parallel/

### Competitive conclusion and feature priority

The competitive floor has moved upward: mobile kickoff, background agent sessions, notifications, cross-device continuation, recipes and task tracking are no longer unique. The product distinction must be stronger and testable.

1. **PocketCode P0:** trustworthy attempt identity, real lifecycle/output/artifact evidence, honest unknown states, durable reconnect/recovery without re-execution, portable receipt and approved correction lineage.
2. **PocketCode P1:** declarative bounded recipes and a task inbox that is backed by durable state, not chat history.
3. **RevDev P0:** durable batch manifest, operation/step identity, append-only evidence, per-operation verification, repair continuation and publication recovery.
4. **RevDev P1:** recipe templates, dependency-aware batching, independent read-only parallel review, notifications and a single reviewable completion summary.
5. **Both:** separate planning from execution; approval binds to exact operation/arguments/policy version; progress events are projections of durable state; notifications are best-effort and never the source of truth.

No additional third-party code is copied in this refresh. The existing isolated reference copies remain the only copied utilities: OpenHands atomic text writer (MIT), adapted Mini-Coding-Agent path guard (Apache-2.0), and MCP Tasks poll interval helper (Apache-2.0). Reusing whole agent stacks would introduce framework/runtime assumptions and dependencies that are not justified by the current $0, provider-neutral, phone-first product constraints.

## 11. Next implementation-ready research questions

Before source implementation is considered:
- define a small provider-neutral recipe manifest and validation contract without importing Goose's provider/extension model;
- map each RevDev recipe step to existing AEC/AWC/P8U/P0-D assertions without creating or renumbering acceptance IDs;
- specify a durable task-inbox projection from task/attempt/step events, including stale/unknown/reconnect behavior;
- decide which operations may be parallelized and prove shared-resource isolation before enabling concurrency;
- add evidence-source mapping to each recipe output so a model-generated summary cannot become its own verification.

These are design tasks only. They do not authorize source changes, new acceptance IDs, PR changes, provider workloads or runtime selection.


## Happy Agent daemon source audit

The deeper PC-host agent review is now captured in [Happy Agent Daemon Source Audit](HAPPY_AGENT_DAEMON_SOURCE_AUDIT_20261105.md). It inspects the daemon's durable operation queue, event journal, process timeout/cancellation paths, permission system, sandbox OS coverage and database migration rules. The central warning is that the generic durable queue is at-least-once and deletes completed pending rows, so it is not an immutable execution or publication journal. No backend or runtime is selected.


## Cline checkpoint follow-up

The deeper source review of Cline's workspace checkpoint implementation and restore tests is recorded in [Cline Workspace Checkpoint and Restore Audit](CLINE_WORKSPACE_CHECKPOINT_AND_RESTORE_AUDIT_20261105.md). The recommendation is to add recoverable workspace checkpoints as a P1 PocketCode feature and as a safety precondition before any future unattended multi-file correction. Do not copy its Git implementation until PocketCode chooses between a separate shadow object store, protected refs in the workspace repository, and a non-Git manifest backend.

**MCP Tasks versioning caution:** the 2026-07-28 MCP Tasks extension source is explicitly marked Draft. Keep it an optional adapter and pin the protocol revision in any adapter; do not freeze PocketCode's core task model to draft wire semantics. The extension's cancellation is cooperative and cannot be treated as proof that remote execution stopped. See the [draft specification](https://modelcontextprotocol.io/specification/2026-07-28/extensions/tasks).
## 9. Additional source-level pass: editor state, Pyodide interruption, bounded agents and staged edits (2026-11-05)

This pass adds four implementation-level comparisons. These are pinned upstream source observations, not product integration or runtime selection.

### 9.1 Pyodide worker execution and interruption: useful architecture, strict limits

Pinned upstream:
- Repository: `pyodide/pyodide`
- Commit: `620c16a62d51be6613cb2208b563b2cf6f9f65d0` (2026-11-04)
- `docs/usage/webworker.md`, blob `95c694c95874c1bc57de1fb1df8f4ad0e5a7489f`
- `docs/usage/keyboard-interrupts.md`, blob `465611fe1aa24e5b4858f83bf68e562388f756fb`
- `src/js/api.ts`, blob `f08d4199bc0291d030034edc90ac3822b9e57b5d`
- `src/tests/test_pyodide.py`, blob `b324c98053f1a47e183fd208647d493cd76c85c5`
- License: MPL-2.0 (source tree license; review file-level notices before copying).

The official worker example loads Pyodide once in a module worker, sends each request with a unique ID, executes asynchronously, and returns result/error with the same ID. This is a credible UI-responsiveness pattern. It is not itself a complete runner contract: the sample has no durable attempt journal, bounded output, queue policy, request cancellation lifecycle, or restart-safe correlation.

The interrupt documentation is more important than the happy path:
- WebAssembly does not support native preemptive Python interruption.
- Pyodide's interrupt mechanism requires a worker and a shared `SharedArrayBuffer`.
- Deployment must provide the required cross-origin-isolation headers.
- The main thread writes the SIGINT marker; Pyodide raises `KeyboardInterrupt` when it processes the marker.
- The API source exposes `setInterruptBuffer`; upstream tests exercise the signal path.

**PocketCode decision:** retain Pyodide as a candidate for the browser/PWA Python lane, not as a selected runtime. A future adapter must expose separate facts for interrupt requested, Python acknowledged interruption, worker terminated, output drained, cleanup completed and final result captured. A client timeout or sent interrupt is not proof that execution stopped. If the worker is terminated to regain UI responsiveness, its in-memory interpreter state is lost and the attempt must be reconciled from durable evidence, not silently retried. The SharedArrayBuffer header requirement is a deployment gate that must be tested on actual supported iOS Safari/PWA contexts; do not assume it is available in every hosting mode.

Do not copy the documentation's simple worker wrapper as a production runner. It is a teaching example with no durability or resource policy.

### 9.2 CodeMirror state: immutable editor transactions, not an execution ledger

Pinned upstream:
- Repository: `codemirror/state`
- Commit: `9c801279cb83011e6f92af778f4443406e8f1200`
- `src/state.ts`, blob `f83d92f9f00cb4c9a5567728658c6602afcbdcd2`
- `test/test-state.ts`, blob `66317aa0b27cac964cc9170301638b3a249fc3ed`
- `LICENSE`, blob `9a91f48619f481743ffb278a3f0ac05176ad7102`
- License: MIT.

The source implements persistent/immutable editor state: updates are transactions that produce a new state rather than mutating the prior document. It also supports JSON serialization/deserialization of the document, selection and explicitly registered serializable state fields. The tests exercise state updates and serialization.

**PocketCode decision:** if CodeMirror 6 is selected for the editor, reuse its packages rather than copying editor internals. Use transaction/change sets for in-editor editing, undo/redo and mapping selections across changes. Do not treat editor state JSON or transaction history as the authoritative project/run journal. Persist project files and run attempts through a separate storage contract with explicit versions, atomicity, provenance and recovery. The editor's immutable in-memory model is not a crash-safe filesystem or checkpoint store.

### 9.3 mini-SWE-agent: strong bounded-loop and test patterns, unsafe environment default

Pinned upstream:
- Repository: `SWE-agent/mini-swe-agent`
- Commit: `04d809ceab9df28f9adaed044884180159172930` (2026-09-03)
- `src/minisweagent/agents/default.py`, blob `ca310e37d7c61888c576f73f5e1790ac769407b1`
- `tests/agents/test_default.py`, blob `cb8587475a25abd23612107dd655435187bb12d9`
- `src/minisweagent/environments/local.py`, blob `2b12d33ec90c8db7bb8a36002ba09706be6e7f45`
- `LICENSE.md`: MIT.

The agent loop enforces independent step, model-cost and wall-clock limits. It persists a serialized trajectory in a `finally` block after each step, records model call/cost metadata and versioned trajectory format, and has deterministic fake-model tests for successful completion, step limits, cost limits, timeout handling, partial output on timeout and multi-step continuation. The local environment uses a process group on POSIX and kills that group on timeout, then captures output.

Important limits found in the same source:
- The local environment executes shell commands directly on the host; it is not a sandbox.
- stdout and stderr are merged.
- Exceptions use a synthetic return code `-1`, so this is not a fully typed exit/termination receipt.
- The trajectory save uses a direct `Path.write_text` JSON replacement, not an atomic temp-file/fsync/rename protocol or append-only transaction journal. The per-step `finally` save is valuable but does not prove crash-safe persistence.
- The project tests are upstream tests inspected, not executed by PocketCode.

**PocketCode decision:** adopt the *shape* of the bounded director loop and deterministic fake-adapter tests: explicit step/cost/time budgets, save/checkpoint after every step, preserve partial output, and test continuation after timeout. Do not copy its local shell environment or elevate its trajectory file to canonical evidence. PocketCode still needs a provider-neutral budget policy that can operate with a $0 manual-AI workflow and does not imply hidden provider usage or quota bypass.

### 9.4 Plandex: reviewable staged edits are useful; its apply/rollback code is not a durability baseline

Pinned upstream:
- Repository: `plandex-ai/plandex`
- Last main commit observed: `e2d772072efadbe41d2946d97d79be55532dbab5` (2025-10-03). The repository appears stale relative to the 2026 review date; treat as a historical reference, not an actively maintained dependency.
- License: MIT, LICENSE blob `4aa379f2105798e6d6a8a4f1020ba272f23995f4`.
- `app/cli/lib/apply.go`, blob `067da509ae4d0a67717dab1921554737e695e064`
- `app/server/syntax/structured_edits_test.go`, blob `55b338acab1d8428a2292d3b35101e6983e70f30`
- `app/server/model/plan/build_structured_edits.go`, blob `1a0665246a95018aad30d79885bd08c850bbd97f`.

The structured-edit tests show a useful technique: preserve existing code around explicit insertion/replacement regions and verify the exact reconstructed file against fixtures. The product's cumulative diff review and separate apply action are good UX concepts.

However, the inspected apply implementation is not safe to copy as PocketCode's transactional workspace layer:
- It records prior file contents/modes in an in-memory rollback object, not a durable checkpoint.
- File writes/removals run concurrently.
- A failure can occur after some files have already changed; the caller's error path has its rollback call commented out in this pinned source.
- The shell apply script executes through the user's configured shell with inherited environment. This is not a sandbox.
- The rollback plan's project-path cleanup is broad enough that a future implementation must guard against concurrent workspace changes and must not delete files it did not create.
- The inspected test file validates structured text reconstruction; it does not prove crash-atomic multi-file apply/rollback.

**PocketCode decision:** adopt review-before-apply, structured edit fixtures and visible diff concepts. Do not import the Plandex apply/rollback code. Implement any future workspace checkpoint using a durable, content-addressed shadow store or another explicitly selected backend, with path containment, symlink handling, atomic per-file replacement, crash recovery and concurrent-edit protection tested separately. This is a design requirement, not an approved storage choice.

### 9.5 Net adoption ranking after this pass

| Candidate | Reuse decision | Why |
|---|---|---|
| CodeMirror 6 | Strong dependency candidate if web editor is chosen | MIT, mature immutable editor state and tested transaction model; not a run journal |
| Pyodide | Candidate runtime only | Useful worker and Python ecosystem; interrupt deployment constraints and no hard-stop proof |
| mini-SWE-agent | Pattern/reference only | Excellent bounded loop and deterministic tests; unsafe direct-shell default and non-atomic trajectory save |
| Plandex | UX/test-pattern reference only | Reviewable diff and structured edit fixtures; stale repository and weak apply/rollback durability |
| MCP Tasks | Optional adapter only | Draft/versioned remote task lifecycle; never core product task identity |
| Happy | Invariant reference only | Atomic cursor/snapshot and exact ack; generic outbox coalesces intents |

**Copy decision:** no additional upstream code is copied in this pass. The candidate components are not yet tied to a selected PocketCode application framework, storage engine, runtime or workspace model. Copying a runnable worker, editor internals or filesystem apply routine now would create an unowned integration surface and could falsely imply a tested product path. The existing isolated MCP polling helper remains the only research-only code extraction recorded above. No production code was changed.
## 10. Workspace durability deep dive: SQLite-backed recovery and browser OPFS (2026-11-05)

This pass targeted the gap left by Plandex: durable workspace checkpoints and restart recovery. It inspected implementation and tests from `tgbender/safe-fs-ops`, `openclaw/fs-safe`, `opfs-vfs/opfs-vfs`, and official `sqlite/sqlite-wasm`. No dependency was installed and no product code was changed.

### 10.1 safe-fs-ops: strongest end-to-end recovery reference

Pinned upstream:
- Repository: [tgbender/safe-fs-ops](https://github.com/tgbender/safe-fs-ops)
- Main commit observed: `d52afaaec4f6050bd2ac70219ac8bbd7bc9d652e` (2026-09-07)
- Package version `0.1.1`, MIT, Python >=3.12, SQLAlchemy >=2.0.49; alpha / pre-1.0.
- `src/safe_fs_ops/filesystem_ops/content_addressed.py`, blob `d1b099c390c8b3474b5e298b5a01b238c791f3f7`
- `src/safe_fs_ops/filesystem_ops/tree_backups.py`, blob `ea7b7f80dcf6d70e5e322a93e582723478814c3c`
- `src/safe_fs_ops/operation_journal/journal_batch.py`, blob `dda5c05a2a613b480d51204d6ac586121acbeb2f`
- `src/safe_fs_ops/operation_journal/filesystem_mutation_checkpoints.py`, blob `2f8a34e99f1832d78d41551aa2a6dfa1c5a1791e`
- `src/safe_fs_ops/operation_journal/recovery_runner.py`, blob `d2120bd6eb1db353c17152e287c4eb882383fa25`
- `src/safe_fs_ops/workspace_state/leases.py`, blob `b932378a7ee320a15768df56a1d1a5d7d7941df7`
- `docs/RECOVERY_MODEL.md`, blob `15756cca8da4d53659dd6fe840561600d95e8608`
- `docs/FILESYSTEM_PRIMITIVES.md`, blob `87557301644a695e6172b7580610bb4be142ab2b`
- `docs/SOURCE_REVIEW.md`, blob `eb348f21abd5a0d102eb3f79ee2fde4d9dfa10e8`.

Useful implementation patterns confirmed in source:
1. SHA-256 content-addressed objects at `sha256/<prefix>/<digest>`; stream hashing, source identity checks before/after capture, staged temp writes, fsync, hash verification and no-replace installation.
2. Explicit `backup_tree(root, relative_paths)` rather than claiming a full recursive filesystem snapshot. It captures regular files and symlink targets for named paths. Directory metadata and empty directories are not captured.
3. Restore preflight checks every entry and content reference before changing any destination. Default conflict policy is no-replace; replacement is opt-in. Content is reverified before copying.
4. SQLite journal records planned intent, idempotency key, lease identity/fencing token, before checkpoint, backup-artifact intent, durable artifact references, after checkpoint, failures, recovery intent and recovery action outcomes.
5. Partial content-addressed artifacts are checkpointed immediately as refs are created, so an interrupted backup can account for artifact cleanup debt.
6. Recovery actions have stable action IDs and append-only planned/attempting/succeeded/failed/skipped/manual-intervention statuses, tied to a specific recovery attempt. Re-running a terminal action does not repeat it.
7. Cross-process leases use a secret token and monotonically increasing fencing counter. Old workers cannot append after takeover. Python locks are not treated as the authority.
8. Recovery is proof-dependent: if the target no longer matches expected state, content is missing/tampered, path safety is unknown or restore partially fails, it requires manual intervention instead of overwriting.

Relevant upstream tests inspected (not run here):
- `tests/filesystem_ops/test_content_addressed.py`: object digest, deduplication, tamper rejection, symlinked store-root/prefix refusal.
- `tests/filesystem_ops/test_tree_backups.py`: explicit file restore, metadata, symlink capture, no-replace conflicts, unsupported safe symlink replacement.
- `tests/operation_journal/test_tree_backup_recovery.py`: partial artifact checkpointing, shared-store races, artifact cleanup revalidation, lease loss during failure recording, recovery.
- `tests/operation_journal/test_journal_store_recovery_fencing.py`: idempotent concurrent starts, invalid transitions, forged lease rejection, takeover fencing.
- `tests/operation_journal/test_recovery_runner.py`: action state progression, replay of terminal actions, interrupted attempting actions, slow-recovery tests.
- Docs state the default suite excludes opt-in stress and slow recovery tests; Windows, macOS and Linux are in the test workflow matrix. That is upstream's stated coverage, not independent execution or proof for PocketCode.

Limitations / adoption:
- Alpha API and broad implementation surface. It is Python 3.12 plus SQLAlchemy, not a drop-in mobile TypeScript library.
- Tree backups cover explicit file/symlink paths, not a whole-tree image; no empty dirs or directory permissions. This is a deliberate tradeoff but may not satisfy full project restore.
- Filesystem group operations remain non-transactional. The journal makes recovery explicit; it does not make a batch atomic.
- Not a sandbox. External tools can make unrecorded changes.
- No independent full audit or tests were run in this project.

**Decision:** best architecture and test-pattern reference found so far for RevDev's Python reference/evidence tooling. Do not add it as a PocketCode dependency. Reconsider a bounded pilot only if the product gains a supported Python backend and after the target OS/filesystem matrix is selected. For a TypeScript/mobile implementation, port the *contracts* (CAS blobs, explicit manifest, per-action journal, fencing, proof-based recovery), not this Python implementation.

### 10.2 openclaw/fs-safe: strong path-boundary primitives, not a workspace transaction system

Pinned upstream:
- Repository: [openclaw/fs-safe](https://github.com/openclaw/fs-safe)
- MIT; Node >=22; current package has platform-specific native bindings.
- `docs/security-model.md`, blob `5eb1f6881c0f590e2205cb7a491344ee16e09641`
- `docs/atomic.md` (upstream documentation) and `test/atomic-fault-matrix.test.ts`, `test/atomic-callback-substitution.test.ts`, `test/atomic-mutation-authority.test.ts`, `test/directory-durability.test.ts`, `test/file-lock-concurrency-stress.test.ts`.

Useful: capability-style root handles, path containment, symlink/hardlink defenses, identity checks, sibling-temp + rename, optional file and parent-directory fsync, sidecar locks, content hashing, and a large fault/adversarial test catalogue. Its docs explicitly distinguish Linux kernel-atomic native paths from best-effort macOS/Windows/JavaScript fallback paths. It explicitly says it is not a sandbox and per-call checks do not defeat an arbitrary same-UID process continuously racing namespace changes.

**Decision:** reference the threat model and atomic-write test cases. Do not add as a PocketCode dependency until Node runtime and native addon support are confirmed. Browser JS cannot use Node filesystem descriptors or these native bindings. It does not provide multi-file workspace transactions or durable mission semantics.

### 10.3 OPFS VFS: valuable crash testing, rejected dependency due licence

Pinned upstream:
- Repository: [opfs-vfs/opfs-vfs](https://github.com/opfs-vfs/opfs-vfs)
- Package `@opfs-vfs/opfs-vfs` version `2.1.0`.
- Package licence: **PolyForm-Noncommercial-1.0.0**. This is incompatible with our intended commercial product direction. Do not copy or depend on it.
- `packages/opfs-vfs/src/__tests__/physical-recovery.test.ts`, blob `4dd6e75d7ae26a23b1d11b34e71a8957f268f2a2`
- `packages/opfs-vfs/src/__tests__/data-wal.test.ts`, blob `65853e4680479b6e143e6571486d6b95ad22ead0`
- `packages/opfs-vfs/src/__tests__/crash-consistency-worker.ts`, blob `d5a51f2fa0112c544be34a422d9c1542fcae9c90`
- `packages/opfs-vfs/src/__tests__/crash-integrity-worker.ts`, blob `30ffbbf9a9d67acbc5968c0261b7c090c8c7b66f`
- `packages/opfs-vfs/src/__tests__/storage-fault-worker.ts`, blob `481c54444299c0cb904c74e075a9a288cd2db78d`.

The tests are unusually relevant: WAL frame checksums, partial trailing records, corruption offsets, physical mapping truncation, crash consistency/integrity, and persistence/recovery audit. They are useful as *test-design inspiration only*. Do not port source under the noncommercial licence.

### 10.4 Official SQLite Wasm + browser OPFS: better PocketCode candidate

Pinned upstream:
- Repository: [sqlite/sqlite-wasm](https://github.com/sqlite/sqlite-wasm)
- Main commit observed: `ccbb81134a3b5a824f8a3cc3c5d8edd6e799ab5a`
- npm package version `3.54.1-build1`, Apache-2.0 wrapper (SQLite core itself is public domain).
- `demos/sahpool-demo/src/workers/worker.ts`, blob `adbb157342c804388b947740b8fd9c6f2bc1f6be`
- `demos/opfs-demo/src/workers/worker.ts`, blob `176ebf02c4d506372621442293a1ede207be16eb`
- `src/__tests__/sqlite3-sahpool-vfs.browser.test.ts`, blob `f749c6a89e483cff6b224448e43b3bcde6cea3a2`
- `src/__tests__/workers/sqlite3-sahpool.worker.ts`, blob `2d8c3b5650921bd3831d12be384101b6cbcbc6f2`.

The official worker demo initializes SQLite inside a dedicated worker, installs the OPFS SyncAccessHandle Pool VFS, performs database operations, closes/reopens the database and verifies persistence. The test worker also exercises pause/unpause and checks that an active DB handle prevents pausing. This is a much smaller and more directly reusable foundation than adopting a full custom VFS.

Important tradeoffs from SQLite's official persistence documentation:
- OPFS only works from worker context.
- The regular `opfs` VFS supports more concurrency but needs COOP/COEP and has Safari sub-worker compatibility caveats for Safari <17.
- `opfs-sahpool` is intended to work across major browsers since March 2023 and does not need COOP/COEP, but does not support multiple simultaneous database connections/instances. It pre-allocates handles and locks them. A second app/tab instance can fail to initialize.
- `opfs-wl` uses Web Locks but requires `Atomics.waitAsync()`, so it is less portable.
- WAL mode on OPFS has special constraints: SQLite's WASM build lacks shared-memory APIs; WAL requires exclusive locking, which removes concurrency benefits. Do not assume conventional desktop SQLite WAL settings transfer unchanged.
- OPFS is private to the origin, subject to quota/eviction, and clearing site data deletes it. It is not a user-visible project folder. Important changes need an explicit storage sync/commit contract and an export/backup route.

**Decision:** strongest current dependency candidate for a *browser/PWA PocketCode local metadata/journal database*, conditional on confirming that the app is a web/PWA runtime. Use a dedicated worker and start by evaluating the SAHPool single-owner model. If multi-tab editing is required, design and test an explicit single-writer ownership/lock protocol before selecting a different VFS. Do not use OPFS database storage as the only copy of user project files; maintain export/backup and quota/eviction recovery. It is not a native iOS/Android storage choice and must not be assumed to work in an arbitrary WebView without device tests.

### 10.5 Proposed PocketCode storage split

If browser/PWA is the chosen client, the candidate design is:

- SQLite Wasm + OPFS: task/project metadata, immutable attempt/result index, event/journal rows, leases and checkpoint manifests.
- OPFS project object area: content-addressed immutable file blobs, named by SHA-256, with explicit project tree manifests and metadata.
- Atomic logical update: write/verify all new blobs, then commit one SQLite manifest/reference transaction. Old manifest remains the recoverable state until the commit is acknowledged.
- Startup recovery: inspect incomplete intent/attempt rows, verify referenced blob hashes, rebuild indexes from durable manifests, and expose missing/corrupt artifacts as recovery-required rather than silently emptying a project.
- User backup/export: produce a portable project bundle with manifest, blob digests, schema version and integrity check. Storage persistence request is advisory; never promise browser storage cannot be evicted.
- Single-writer owner: one worker/instance holds the DB. Other tabs communicate with it or fail closed with an actionable "workspace already open" state. A worker restart requires re-opening and reconciling journal state, not replaying unacknowledged writes blindly.

This is a candidate architecture, not an approved implementation. No SQLite schema, runtime or product acceptance ID is changed by this research.

### 10.6 Next validation gates

1. Confirm app runtime (native React Native, Capacitor/WebView, or browser/PWA) before choosing OPFS.
2. Test iOS Safari/PWA and Android Chrome on actual devices for OPFS, worker startup, SAH creation, quota, persistence, app background/suspend, force-kill and reopen.
3. Inject worker termination at each boundary: before blob write, after blob sync, before SQLite transaction, after transaction commit but before reply, and during export.
4. Test two tabs/app instances and verify exactly one owner; no silent fallback to two writers.
5. Verify export can reconstruct the project after OPFS is cleared or evicted.
6. Do not report a save as durable until the relevant database commit and blob sync contracts have succeeded and their exact acknowledgement is recorded.
### 10.7 SQLite durability configuration nuance

A further read of `safe-fs-ops/src/safe_fs_ops/sqlite_store/store.py` (blob `77208fef4c84c2e0241e4c480b8e74af8dd6a528`) and `persistence/sqlalchemy.py` (blob `f5b675e48fcc8e5e440d5ca007de3bc89753baae`) prevents a misleading conclusion:
- `SqliteEngineConfig`'s standalone dataclass default is `synchronous="NORMAL"` and `enable_wal=True`.
- But `SqliteStore` constructs the engine as `SqliteEngineConfig(self.path, synchronous=None)`, so this path does **not** issue a `PRAGMA synchronous=NORMAL`. It leaves the effective SQLite connection default in place. The custom connection-factory path also does not set synchronous explicitly.
- SQLite's own documentation says WAL + NORMAL preserves consistency but a just-committed transaction may roll back after power loss; WAL + FULL adds a WAL sync per commit for power-loss durability. The SQLite runtime default is normally FULL, but this must be queried on the actual connection rather than inferred from a config dataclass or docs.

**Required audit rule:** any future PocketCode SQLite backend must expose and record the effective `PRAGMA journal_mode` and `PRAGMA synchronous` at startup, select the mode explicitly for the product's durability promise, and test abrupt process termination separately from OS/power-loss assumptions. A successful SQL COMMIT under NORMAL is not proof of power-loss durability. For browser OPFS, validate the VFS `xSync`/flush behavior and actual device implementation; do not infer physical persistence solely from API success.
