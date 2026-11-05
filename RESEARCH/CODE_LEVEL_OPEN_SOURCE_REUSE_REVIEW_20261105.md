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
