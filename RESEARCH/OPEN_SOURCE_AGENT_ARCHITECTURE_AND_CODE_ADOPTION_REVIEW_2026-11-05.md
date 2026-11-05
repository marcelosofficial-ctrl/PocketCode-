# Open-source agent architecture and code-adoption review

**Research date:** 2026-11-05  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Status:** Source-reviewed desk research and adoption recommendations. No hands-on competitor benchmark. No PocketCode runtime/framework/provider selected. No code copied into production paths.

## Executive decision

PocketCode must not compete as another generic mobile coding agent. The strongest direct competitor found in this pass, AndroidHarness, already advertises a no-PC Android coding agent with a local Linux toolchain, editable projects, shell/Git/Python/Node, browser tools, subagents, inspectable tool-call cards, persistent task recovery, and privacy-conscious diagnostic reports. Atlan independently describes a mobile engineering cockpit with deterministic verification, build automation, and a diagnostic Doctor. These are substantial overlaps with the proposed PocketCode loop.

The opportunity is narrower and still unproven: a cross-platform, provider-neutral, execution-evidence workflow that chooses an appropriate local/remote execution boundary, preserves truthful run/attempt semantics, and makes correction/reverification unusually low-friction. The iOS path and a no-PC path matter, but must be proved on the same fixed task against existing local and remote alternatives.

**Code-adoption decision:** do not transplant a whole agent, Android shell, remote relay, cryptographic implementation, or checkpoint subsystem yet. The repository README still defines PocketCode as discovery/product definition and explicitly says no production runtime, cloud provider, framework, pricing model, or supported-language commitment is finalized. Copying Kotlin, TypeScript, Rust or Node implementation into the product now would create unintegrated code and silently select a stack. Instead, pin the exact reusable source candidates below and adopt the underlying designs in our contracts. Once the vertical-slice architecture is selected, copy only the smallest isolated component whose dependencies and security properties can be tested.

This is not reluctance to reuse open source. It is a deliberate guard against accumulating vendor code that cannot be built, tested or maintained.

## 1. Competitive capability findings

### 1.1 AndroidHarness — strongest direct Android overlap

Repository: https://github.com/Sanuu7/AndroidHarness  
Reviewed commit: `1e1fe4c55c6d6386f5b482ef5d88ba71f960969e`  
License: MIT; LICENSE blob `9e091b187b79d6db3ec787b1ffbb32f58be30b73`  
README blob: `e1efad21c7bdd4066ee3973492555a236fae4463`

Its README advertises a native Kotlin/Jetpack Compose Android agent with no PC/root requirement; local file editing; shell, Git, Python and Node; browser control; subagents; inspectable tool-call cards; long-run recovery; queued prompts; context-window meter; provider flexibility; plugins/MCP; and fixed-whitelist diagnostic reports.

The recovery implementation is especially relevant:
- `TaskControlStore` persists task settings/state using a temp file, file sync and rename before publishing the new in-memory state.
- Disk restoration changes a previously `running` task to `interrupted`.
- `RunRecovery.missingResults` synthesizes an explicit error result for assistant tool calls without a tool result, marking their outcome unknown.
- `RecoveryLedger` reuses successful prior tool results and blocks replay when the prior result is missing/unknown.
- `TaskBudget` carries token, cost and time budgets in coroutine context.
- The test suite includes a basic completed-write reuse and uncertain-write block test.

Important source limitation: `RecoveryLedger` maps tool calls by `tool name + normalized JSON arguments`, not by a durable operation ID. The map uses `associateBy(signature)`, so repeated identical calls can collide; semantically identical JSON with different property ordering can also produce different serialized signatures. The current focused test checks one call, one completed result, one unknown result and one changed argument. It does not demonstrate correctness for two distinct identical calls, reordered JSON keys, nested side effects, or a crash between side effect and result persistence. This is a candidate pattern, not a recovery implementation to copy unchanged.

Security is unusually candid. Its SECURITY.md explicitly says workspace/path checks and shell policy are not a complete filesystem/process sandbox; normal commands run as the app UID; project folders do not isolate interpreters; symlink/path checks do not contain arbitrary code; remembered shell grants are command-prefix grants; full access skips normal denylist/path controls; root/Shizuku expand access. This is useful honesty and a warning against describing an Android workspace as a sandbox.

Key source files:
- `app/src/main/java/com/androidharness/app/agent/TaskControl.kt`, blob `2d66ffefc6f49c5345b36addd381c2ca36615906`
- `app/src/main/java/com/androidharness/app/ui/settings/DiagnosticReport.kt`, blob `3f70d794f72a5ea7eba0a76ec1809dc8242ac7df`
- `app/src/test/java/com/androidharness/app/ui/settings/DiagnosticReportTest.kt`, blob `f3d79cb915458d0980b22cf0940a21fea61ec8bd`
- `SECURITY.md`, blob `e615de928015a5414bace75ebdb5812757cd28b8`

**Adopt:** the explicit interrupted/unknown operation state; do not replay unknown side effects; write-before-advance; fixed-whitelist diagnostics; test that permission alone does not imply a subsystem is ready; explicit capability labels.

**Do not copy unchanged:** signature-only recovery ledger, broad shell execution, Android-specific Shizuku/Termux integration, or claims that app-UID workspace routing is isolation.

### 1.2 Atlan — strongest phone workstation / deterministic verification reference

Repository: https://github.com/Atlansdaddy/atlan  
Reviewed commit: `234cf1552fe06e14a1a4733a9262af54a5c92088`  
License: Apache-2.0; LICENSE blob `d645695673349e3947e8e5ae42332d0ac3164cd7`  
README blob: `118c83d8313317f41591c9f41e00f19f6ccfbf26`

Atlan describes a Termux/proot Ubuntu environment on capable Android devices, a browser cockpit, multiple agent engines, a persistent warm CLI session, chat-to-project handoff, build automation, test/verification, a Doctor and copyable diagnostic report. It explicitly says iOS is cloud-client-only, and Android local setup is a power-user Termux/proot route. Its README reports device-specific confinement measurements and acknowledges tier-dependent limits. Treat those as project claims, not independent validation.

Source review of `server/src/sandbox/confine.js`, blob `090d8efd21b30976dfcf3cd3da3f31b5d7c5f79d`, is valuable because it documents both covered and uncovered process-launch points. It distinguishes the model client process from shell child processes, explains why the former cannot simply have egress disabled, and explicitly lists other unwrapped launch paths. The design probes device capabilities and refuses a requested tier if the device cannot establish it. The policy is passed over a file descriptor rather than a path to avoid a TOCTOU swap.

**Adopt:** truthful capability tiers; preflight before claiming a sandbox; enumerate every process spawn and every egress path; fail closed when a declared boundary cannot be established; a Doctor that states exactly what was checked and what it did not prove.

**Do not copy:** native confinement code into PocketCode without a selected host/runtime, OS-specific threat model, independent review and device tests. A Linux proot is not equivalent to iOS local execution or a hosted sandbox.

### 1.3 Happy — strongest cross-device remote-session and protocol reference

Repository: https://github.com/slopus/happy  
Reviewed commit: `a0ba0979325ec5437ab6ad3f0904c0286b904f42`  
License: MIT; LICENSE blob `da0b4ae30a42be8db9776eb887acb671b19699a0`  
README blob: `4233039fae6fa3d19827afc8d0821756530c971e`

Happy provides native iOS and Android clients, desktop apps, remote agent harnesses, encrypted sync, provider flexibility and collaborative sessions. It is a strong model for continuing a running remote session from a phone, not proof that code executes locally on the phone.

The protocol is more reusable than its UI:
- Persistent `update` events carry monotonic sequence numbers; ephemeral presence/usage events are separate.
- Versioned mutable fields use `expectedVersion` and explicit version-mismatch responses.
- Session-scoped, machine-scoped and user-scoped connections separate update audiences.
- Most session content is encrypted client-side and opaque to the server.
- HTTP is used for reads/actions and Socket.IO for realtime sync; reconnectable state is distinguished from transient presence.

The protocol doc itself recommends keeping the API surface small and adding a new event only when it creates a durable sync primitive. The encryption code has both legacy NaCl and newer per-record AES-256-GCM data keys. Do not transplant cryptographic code without a crypto design, dependency audit, key lifecycle review and cross-platform test vectors.

Key source references:
- `docs/protocol.md`, blob `4701e53c71810652cae547454320713efcc44701`
- `docs/encryption.md`, blob `4a249bde6ac9b9ddc8457b815fd5253367cb680a`
- `packages/happy-cli/src/api/encryption.ts`, blob `6d5a4891f666924106f7cd840717bf2a2de75fc3`
- Android key unwrap: `packages/happy-android/crypto/.../AccountEncryption.kt`, blob `01d7db3bd2de5ee61703c76f45a5b2f0173a7795`

**Adopt:** durable vs ephemeral event separation; monotonic cursor; optimistic concurrency; reconnect backfill; per-session scoping; encrypted opaque payloads as a future architecture option.

**Do not copy:** the Happy relay/server or cryptographic routines as a shortcut to a PocketCode backend.

### 1.4 Pairlet — mobile control plane for a user's existing computer

Repository: https://github.com/heypandax/pairlet  
License: MIT; LICENSE blob `6abcf33521b0479afab4447889929db6f6e5121d`

Pairlet offers Watch, Approve, Continue and Inspect across phone/tablet/desktop. It streams agent output and tool events, routes permission requests to the phone, supports in-place session takeover and reconnect backfill, and uses a relay with encrypted frames. Its README also documents backend-specific limitations honestly: one backend runs Full access without enforceable interactive approvals; other backends have incomplete diff/usage/timeout capabilities.

**Adopt:** capability matrix per backend, explicit inability to enforce an approval, reconnect backfill and a safe default deny when an approval expires.

**Positioning implication:** a phone client for a remote PC is already a strong substitute, but it does not solve the no-PC job when the host is unavailable.

### 1.5 Cline — reversible workspace edits and Plan/Act workflow

Repository: https://github.com/cline/cline  
Reviewed commit: `d3ecc4890e8f9bcb77182b96c77fa90575e8e145`  
License: Apache-2.0; README and license checked.

Cline offers Plan and Act modes, approval for file edits and terminal commands, MCP, subagents, scheduled routines, and workspace checkpoints. The checkpoint docs distinguish restoring task and workspace together, task only, or workspace only. This separation is useful: users may want to undo code while retaining the conversation that explains the change.

The implementation is not a trivial `git reset`: it handles tracked, staged, unstaged and untracked files, uses stash-shaped commits, private refs and restore transactions, and provides rollback if checkpoint restoration fails. It also has dedicated tests for these cases.

Key sources:
- `docs/core-workflows/checkpoints.mdx`
- `sdk/packages/core/src/session/checkpoint-restore.ts`, blob `574acd5c1025316a1fb6134f3f1089e4b2d99923`
- `sdk/packages/core/src/hooks/checkpoint-hooks.ts`
- `sdk/packages/core/src/session/checkpoint-restore.test.ts`

**Adopt:** a future optional workspace checkpoint with explicit restore scopes and rollback transaction. Do not use destructive reset/clean commands without capturing untracked state and a tested rollback path.

### 1.6 Goose — reusable recipes, subrecipes and bounded parallel work

Repository: https://github.com/aaif-goose/goose  
Reviewed commit for recipe source: `bfe8ccd23de1d2c47a4cb2970d522f093ae7f2ba`  
License: Apache-2.0; LICENSE blob `c83043d4494071fbd93ef245a14e573c5a8280c4`  
README blob: `44c960f0193de1ccd3a13721cfe2daf5e7707ac5`

Goose is a general-purpose local agent with desktop/CLI/API, provider adapters, MCP extensions, reusable parameterized recipes, subrecipes, and parallel subrecipe workflows. Recipes package instructions, extensions, parameters, provider/model choices and output schemas.

**Adopt:** recipe templates as reusable, versioned task packets; typed parameters; preflight validation; bounded subrecipes; explicit allowed tools/extensions; structured outputs; per-subtask result/evidence. Parallelize only independent read-only or isolated tasks. Serialize shared mutable workspace operations.

### 1.7 OpenCode — granular permissions and specialized agents

Repository: https://github.com/anomalyco/opencode  
Reviewed permission source commit: `893e8dc43f05e872d4cac603486ce8a7181170fa`  
License: MIT; current dev branch LICENSE blob `6439474beed8e0271df9862eff97ffd70ec2464c`  
Reviewed `packages/core/src/permission.ts`, blob `b78a674d27777f5cc71f53cf0213af679dee3bd8`.

OpenCode distinguishes a read-only Plan agent from a full Build agent and supports per-tool allow/ask/deny rules, wildcard resources, session/agent permissions, pending approval requests, and saved rules. Its evaluator uses last matching rule semantics. The code also has a lifecycle for pending permission requests and emits asked/replied events.

**Adopt:** a central operation permission evaluator, explicit action/resource, deny precedence, pending request identity, and separate Plan/Build modes.

**Caution:** permission persistence is subtle. Public issue #30779 describes project-scoped “always allow” rules inherited by forked sessions. Another newly filed issue #61645 questions race-safe, single-use admission around hooks and current policy. These issues are reports, not proof of all current versions, but they demonstrate why approvals must bind to the exact operation, current policy version, session and resource at execution time. A stale UI approval must not authorize a changed command.

### 1.8 Aider — Architect then Editor and automatic lint/test loop

Repository: https://github.com/Aider-AI/aider  
License: Apache-2.0; LICENSE.txt blob `d645695673349e3947e8e5ae42332d0ac3164cd7`  
README blob: `816c876cb67021fa9f8d37267c8e57923eabdb07`

Aider provides codebase maps, Git integration, broad model support, voice input, copy/paste with web chat, automatic lint/test after edits, and an Architect mode where one model proposes a solution and a separate editor model applies it after confirmation. The inspected `ArchitectCoder` is a short orchestrator but depends on Aider's coder/model abstractions; it is not a drop-in standalone component.

**Adopt:** separate planning/review from execution; make the proposed diff visible before mutation; automatically run bounded lint/tests after an edit; route the actual failure output back to the correction stage.

### 1.9 LangGraph SQLite checkpoint — durable workflow reference, not a PocketCode framework choice

Repository: https://github.com/langchain-ai/langgraph  
License: MIT; LICENSE blob `fc0602feecdd6748623c852ab534e1ca612673c7`  
Reviewed SQLite checkpointer at commit `302a4d4caf7fa90d78efa4e9f0636a6d72d24ac8`.

LangGraph documents thread-keyed checkpoints, resumable interrupts, state history and durability modes. The SQLite saver uses WAL and tables for checkpoints and pending writes; its own source calls the synchronous saver lightweight and not multi-thread scalable. The project documentation warns about safe deserialization configuration for checkpoint data.

**Adopt:** durable workflow cursor, explicit interrupt payload, resumable state and a deliberate durability/performance choice. Do not adopt LangGraph wholesale before a framework decision; its checkpoint package is coupled to LangGraph schemas and serializer.

### 1.10 Pyodide — candidate local iOS/browser Python engine

Repository: https://github.com/pyodide/pyodide  
License: MPL-2.0; LICENSE blob `a612ad9813b006ce81d1ee438dd784da99a54007`  
README blob: `97230a6826c5da37fc8a2834460244e7f74cd80b`.

Pyodide is CPython compiled to WebAssembly for browser/Node. It supports pure-Python wheels and a subset of packages compiled for WASM, and exposes browser Web APIs. It is a viable candidate for bounded local Python tasks, not a general Linux environment or automatically a security boundary. Package compatibility, memory, startup, browser API exposure, file import/export, interruption and persistence need a fixed-task proof.

## 2. What the competitor landscape means for PocketCode

| Capability | Existing evidence | Product implication |
|---|---|---|
| Mobile coding agent with local execution | AndroidHarness | No-PC Android agent is not a unique claim |
| Mobile developer cockpit with deterministic build/verification | Atlan | A test/repair loop is already marketed and implemented elsewhere |
| Mobile control of remote agents | Happy, Pairlet, Codeg | Remote PC control is a strong substitute, but not PC-free |
| Plan/Act and permissioned changes | Cline, OpenCode, Goose | Approval UI alone is not a differentiator |
| Workspace checkpoints and undo | Cline | Reversibility is expected in mature coding agents |
| Durable recovery and operation result reuse | AndroidHarness, OpenHands | Recovery needs stronger semantics than “continue prompt” |
| Reusable workflows/subtasks | Goose | Parameterized recipes can reduce repeated prompting |
| Local Python in browser | Pyodide/Pyodios | Narrow local execution can avoid hosted cost for compatible tasks |
| Cross-device encrypted sync | Happy, Pairlet | A remote client/relay is not novel; the execution evidence contract is the harder part |

The product hypothesis should now be tested against AndroidHarness, Atlan, Pairlet/Happy, and a local Pyodide path using the existing fixed CSV-to-JSON task. Measure setup time, success, time-to-first-result, error fidelity, output-file fidelity, resume after interruption, permission correctness, network policy, privacy, data export and total cost. Do not use feature checklists as proof of superiority.

## 3. Specific architecture patterns to bring into our contracts

### A. Operation identity and recovery (highest priority)

Do not deduplicate side effects by tool name plus arguments. Introduce a stable operation identity at the coordinator boundary and bind it to:
- task/run ID and attempt ID;
- ordered step ID;
- tool/action name and exact canonical argument hash;
- policy/authorization version;
- execution boundary/provider identity;
- started/finished timestamps and terminal evidence;
- side-effect state: not-started, started, completed, failed, unknown;
- durable result/evidence reference and content hash.

On recovery:
1. Reuse a result only when the exact operation identity and exact result content are confirmed.
2. If the operation is started but has no durable result, mark UNKNOWN and inspect/reconcile before retry.
3. If the result exists but the action's postconditions no longer hold, preserve the historical result and report current-state drift; do not silently rerun.
4. A different operation with identical arguments remains a different operation unless an explicit idempotency contract says otherwise.
5. A repeated operation ID with changed arguments is an integrity conflict.

This is the main lesson from AndroidHarness recovery plus OpenHands event history and our existing PocketCode lifecycle work.

### B. Persistent vs ephemeral sync

For a future remote/mobile session:
- durable updates require a monotonic sequence and reconnect backfill;
- presence/typing/usage heartbeats are ephemeral and cannot advance durable execution state;
- mutable records use expected-version compare-and-swap;
- every update is scoped to account/session/machine;
- server-held content should be opaque where end-to-end encryption is selected;
- the user-facing UI must distinguish stale/offline from current/confirmed.

Do not implement a relay until the fixed task shows that local execution/manual copy-paste cannot meet the job.

### C. Permission admission

Every action must be evaluated against current policy at the moment it is dispatched, not merely when a card was rendered. Approval must be single-use and bound to the exact operation ID, action, resource, argument hash, session and policy version. Timeout, disconnect, stale version or unknown approval outcome must fail closed. “Always allow” must have explicit scope, expiry/revocation and visible inheritance; default to session/task scope, not project-wide inherited authority.

### D. Bounded recipes and subagents

A recipe is a versioned task template with typed parameters, prerequisites, tool allowlist, resource/time/cost budget, output schema and terminal acceptance criteria. Subtasks should declare input/output artifacts and dependencies. Parallelize only when writes are isolated or read-only. The coordinator owns terminal state and verifies every sub-result before the whole batch passes.

### E. Checkpoints and undo

A checkpoint must include tracked, staged, unstaged and untracked workspace state. Restore is a transaction with a pre-restore snapshot and tested rollback. Keep task conversation and workspace state as separately selectable restore dimensions. A checkpoint is not a backup unless durability and recovery have been tested.

### F. Diagnostics and evidence

Use a fixed allowlist of status facts. Never export credentials, raw command output, private paths, hostnames, endpoints or full environment/config by default. State what a diagnostic actually proves: e.g. provider catalog reachable does not prove model generation or quota. Include explicit “not checked”, “unknown”, “blocked” and “failed to collect” states. Tests must assert absence of secrets, not just presence of useful fields.

## 4. Code adoption register

| Candidate | License | Direct code reuse decision | Why |
|---|---|---|---|
| AndroidHarness RecoveryLedger | MIT | **Do not copy unchanged** | Signature collision risk; Android/Kotlin types; not sufficient for distributed exactly-once effects |
| AndroidHarness DiagnosticReport.kt | MIT | Keep as future Android UI reference | Small and useful whitelist pattern, but no native Android app/framework selected and iOS also required |
| Happy crypto and protocol | MIT | Reuse protocol concepts only; no crypto copy | Security-critical key lifecycle and cross-platform interoperability need dedicated design |
| Atlan sandbox launcher | Apache-2.0 | No copy | Linux/Android-specific native confinement; host-dependent probes; no PocketCode runtime selected |
| Cline Git checkpoint implementation | Apache-2.0 | No copy yet | Complex Git transaction with untracked files; only relevant if local worktree editing/checkpointing becomes an MVP requirement |
| Goose recipe parser/runner | Apache-2.0 | Reuse recipe concept, not Rust runner | RevDev/PocketCode current stacks do not select Rust or Goose dependencies |
| OpenCode permission engine | MIT | Reuse rule semantics, not Effect/TypeScript service | Runtime and policy model not selected; requires current-policy revalidation and operation binding |
| Aider ArchitectCoder | Apache-2.0 | Reuse two-stage pattern, not class | Coupled to Aider model/coder framework |
| LangGraph SQLite saver | MIT | Reuse checkpoint semantics, not package | Coupled to LangGraph schema/serializer; no framework decision |
| Pyodide | MPL-2.0 | Evaluate as dependency/runtime, not source-copy | A runtime distribution, not a small embeddable utility; MPL obligations require review if modified |

No source files were copied into PocketCode in this pass. This is intentional and does not block future adoption. Before a component is copied, record the exact upstream commit, file path, file hash, license text, copyright header, required NOTICE, transitive dependencies, modifications and tests. Avoid copying code from a moving branch or from a source file whose license has not been checked.

## 5. Prioritized work packages

| Priority | Work package | Deliverable | Gate |
|---|---|---|---|
| P0 | Recovery operation identity | Operation/attempt/side-effect/result identity contract and collision test cases | Independent Claude/Gemini review before code |
| P0 | Trusted evidence ingress | Producer authentication, run/attempt binding, event ordering, terminal authority, collector/teardown degradation | No report verdict from caller-controlled fields |
| P0 | Fixed-task competitor benchmark | Run existing CSV-to-JSON worksheet against AndroidHarness, Atlan if available, Pairlet remote host, Pyodide and manual baseline | No paid provider; record unavailability rather than guess |
| P1 | Permission admission | Exact-operation approval and current-policy revalidation contract | Fail closed on stale approval, disconnect and timeout |
| P1 | Durable sync protocol | Monotonic durable events, ephemeral events, expectedVersion | Only if remote execution/client path wins comparison |
| P1 | Bounded recipes | Provider-neutral versioned task packet with typed parameters and subtask graph | Must not become generic autonomous agent without budget/acceptance |
| P2 | Workspace checkpoint | Tracked + untracked snapshot and transactional restore | Only if user-editing workspaces enters MVP |
| P2 | Local WASM proof | Pyodide capability, package, memory, startup and file round-trip test | Only for supported bounded Python task |
| P2 | UX feature validation | tool cards, context meter, queued prompts, resume card, output artifact browser | Test on actual phone and screen reader/accessibility |

## 6. Questions that remain open

- Is the MVP an execution/report utility, a mobile coding agent, or a remote-agent client? Do not try to ship all three.
- Can a narrow Pyodide workflow satisfy the existing fixed task on iOS and Android without a server?
- Does AndroidHarness's no-PC local workflow outperform the proposed PocketCode loop for Android users?
- Is Atlan's Termux/proot setup acceptable for power users but not beginners?
- Is there an audience willing to pay for a cross-platform evidence/verification workflow when free coding agents already include recovery, diagnostics and report export?
- Which app/runtime framework will actually be selected? Until that is decided, code transplantation is premature.

## 7. Evidence register

- AndroidHarness README: https://github.com/Sanuu7/AndroidHarness/blob/1e1fe4c55c6d6386f5b482ef5d88ba71f960969e/README.md
- AndroidHarness SECURITY.md: https://github.com/Sanuu7/AndroidHarness/blob/1e1fe4c55c6d6386f5b482ef5d88ba71f960969e/SECURITY.md
- AndroidHarness TaskControl.kt: https://github.com/Sanuu7/AndroidHarness/blob/1e1fe4c55c6d6386f5b482ef5d88ba71f960969e/app/src/main/java/com/androidharness/app/agent/TaskControl.kt
- AndroidHarness DiagnosticReport.kt: https://github.com/Sanuu7/AndroidHarness/blob/1e1fe4c55c6d6386f5b482ef5d88ba71f960969e/app/src/main/java/com/androidharness/app/ui/settings/DiagnosticReport.kt
- Atlan sandbox launcher: https://github.com/Atlansdaddy/atlan/blob/234cf1552fe06e14a1a4733a9262af54a5c92088/server/src/sandbox/confine.js
- Happy protocol: https://github.com/slopus/happy/blob/a0ba0979325ec5437ab6ad3f0904c0286b904f42/docs/protocol.md
- Pairlet: https://github.com/heypandax/pairlet
- Cline checkpoint restore: https://github.com/cline/cline/blob/d3ecc4890e8f9bcb77182b96c77fa90575e8e145/sdk/packages/core/src/session/checkpoint-restore.ts
- Goose recipe subrecipes: https://github.com/aaif-goose/goose/blob/bfe8ccd23de1d2c47a4cb2970d522f093ae7f2ba/documentation/docs/guides/recipes/subrecipes.md
- OpenCode permissions: https://github.com/anomalyco/opencode/blob/893e8dc43f05e872d4cac603486ce8a7181170fa/packages/core/src/permission.ts
- Aider ArchitectCoder: https://github.com/Aider-AI/aider/blob/main/aider/coders/architect_coder.py
- LangGraph SQLite checkpointer: https://github.com/langchain-ai/langgraph/blob/302a4d4caf7fa90d78efa4e9f0636a6d72d24ac8/libs/checkpoint-sqlite/langgraph/checkpoint/sqlite/__init__.py
- Pyodide: https://github.com/pyodide/pyodide

## 8. Verification and scope

- Source reviewed: public README, security policy, selected implementation files, selected tests and license files as listed above.
- Competitor claims are source/documentation claims, not hands-on benchmark results.
- No PocketCode source or tests changed or executed.
- No provider, paid workload, CI, device, sandbox, relay, deployment or account action performed.
- PR #2 and PR #3 untouched.
- This is research and a proposal, not an accepted architecture or product decision.


## 9. Additional source-level caveats found during test review

### AndroidHarness recovery test scope

The pinned `TaskControlTest.kt` blob is `bc1c4814c441ed5ce55ea78755f1de5d625cdc34`. Its recovery test verifies one assistant message with two different tool calls, one completed result, and one missing result. The `RecoveryLedger` test verifies one call reused under a new call ID, one missing result blocked, and one changed argument not matched. It does not test two distinct identical tool calls in the same recovery history, JSON key-order equivalence, or two independent store instances/processes writing the same task file.

`TaskControlStore` uses `@Synchronized` methods on one store instance, writes a temp file, calls `FileDescriptor.sync()`, then renames it. The synchronization shown is instance-local. The tests exercise concurrent appends through one store object, not multiple processes or store instances. The inspected write helper does not show a parent-directory fsync. Therefore the source supports atomic-replacement and same-instance concurrency claims, not multi-process coordination or full power-loss durability claims.

These are test-coverage boundaries and questions for independent validation, not proof that the app loses data in production.

### Goose subrecipes are explicitly experimental

The pinned Goose subrecipe documentation blob is `8064d1dafb2f8071c784d674358fa6c54f4af44f`. It labels the feature experimental, states each subrecipe runs in a separate session with its own context, and says subrecipes do not share conversation history, memory or state with the parent or sibling subrecipes. Nesting is not supported in the described version. This isolation is useful for context control, but it means RevDev/PocketCode must pass explicit typed inputs and collect explicit outputs rather than assume shared state.

### OpenCode permission defaults and precedence

The pinned OpenCode permission docs blob is `a33cab7c01ef51c4ca0869a0a4f00feccf59b286`. They document last-matching-rule-wins semantics and permissive defaults for most tools unless overridden. The `always` action in this doc is described as session-scoped, while public issue #30779 describes a v2 project-scoped persistence behavior. These are version/system-specific differences; never transfer a permission scope claim between versions without checking the exact implementation. For our projects, default deny/ask for mutation is safer than inheriting a permissive default.

### Cline checkpoint cost

Cline's checkpoint docs explicitly warn that snapshots after each tool use can consume significant storage and slow large repositories. If adopted, RevDev should checkpoint at meaningful transaction boundaries or before risky mutation groups, not automatically snapshot every tiny tool event without measuring cost.
