# PocketCode competitor capabilities and open-source adoption deep dive

**Date:** 2026-11-05  
**Owner-designated branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Status:** Public product research + pinned upstream source review + two isolated reference-code copies. No PocketCode runtime/provider selected; no product integration or mobile/device acceptance claimed.

## 1. Executive decision

PocketCode should not become a generic mobile IDE, generic agent cockpit, or cloud coding clone.

The most valuable product is a **phone-first, provider-neutral, evidence-first task runner and repair loop**:
1. Receive code and explicit inputs from any AI assistant.
2. Validate task scope and permissions before execution.
3. Run in a boundary whose limits and termination can actually be proven.
4. Preserve stable job/attempt identity with authoritative lifecycle events.
5. Present progress and outcome without converting missing evidence to PASS.
6. Verify, retain and separately authorize generated artifacts.
7. Produce a compact portable debugging report.
8. Accept a user-approved correction and run a new linked attempt.

Competitors have already solved many adjacent UX problems. We should adopt the smallest useful patterns, not their entire stacks.

**Decisions:**
- Adopt the concepts of Cline checkpoints, Goose task progress/approval/recipes, OpenCode durable resume claims, E2B's disconnect-vs-kill distinction, Aider's bounded repository map, and Scion's per-agent worktree isolation.
- Preserve the two small MIT/Apache-2.0 reference utilities already copied under `RESEARCH/vendor/`.
- Do not copy whole Cline, Goose, Scion, OpenHands, Replit, Happy or E2B runtimes into PocketCode. Their framework, database, credentials, provider, container and platform assumptions do not fit the current static prototype.
- Do not select Pyodide, E2B, remote PC, cloud execution or native Python runtime from this desk review.
- Do not alter canonical LOOP-01..14 / CASE-01..16 or owner decisions D-01..D-08.

## 2. What competitors actually offer

### 2.1 Cloud coding from a phone

**GitHub Copilot coding agent / GitHub Mobile**

GitHub documentation describes starting and tracking coding-agent sessions from GitHub Mobile: assign an issue, choose an environment and model/agent, let the agent work in the background on a branch, inspect changes and create a pull request. GitHub also documents mobile workflows for asking the agent to research/plan and make changes without immediately creating a PR, and for resolving merge conflicts on mobile. These are strong adjacent capabilities for a no-PC coding workflow. They remain tied to GitHub's hosted agent product, account/plan entitlements, repository permissions and PR workflow; they do not replace PocketCode's cross-provider, arbitrary-input-file, local/offline or execution-evidence goals. (GitHub’s official docs describe these mobile capabilities; see the linked product and changelog references below.)

Sources:
- https://docs.github.com/en/copilot/how-tos/use-copilot-agents/use-copilot-coding-agent
- https://github.blog/changelog/2026-04-08-github-mobile-code-agent-workflows/
- https://github.blog/changelog/2026-07-08-resolve-pull-request-merge-conflicts-from-github-mobile/

**Replit mobile**

Replit advertises starting and editing web projects with Agent, following progress, previewing and deploying a live website/app. It is a compelling "create something from a phone" competitor, particularly for web apps. Replit's mobile app is not a general arbitrary-code evidence runner; the full native iOS app workflow (Expo/React Native build/preview/App Store pathway) is described through Replit's web environment, not as a complete native mobile-app creation path within the mobile app itself. Cloud execution and Replit's own product/billing terms are central. (These are vendor descriptions, not hands-on device test results.)

Sources:
- https://replit.com/mobile
- https://docs.replit.com/replit-app/mobile

**PocketCode response:** do not duplicate a hosted browser IDE or PR agent. The useful niche is the portable workflow between AI assistants and execution: import/paste source and inputs, run under an explicit policy, verify what happened, export a useful report/artifact, and continue elsewhere. Consider optional GitHub issue/PR handoff later, not a required backend.

### 2.2 Phone as a remote control for a computer

**Happy**

Happy's phone experience is strong for inspecting and resuming agent sessions running on a user's own computer, with encrypted cross-device communication and support for several coding-agent harnesses. This is a good model for the *remote companion* use case. It does not remove the need for a computer to host the agent/runtime, so it does not solve PocketCode's no-PC-first requirement by itself.

Current project messaging has moved toward Happy Desktop; the older `happy` CLI is described as maintenance-mode. The source snapshot reviewed below is an older CLI-era pinned revision. Do not mistake its server/client layout for the newest desktop architecture. (This distinction reflects current Happy documentation and should not be projected backward onto the older CLI source snapshot.)

Sources:
- https://happy.engineering/
- https://happy.engineering/docs
- https://github.com/slopus/happy

**PocketCode response:** preserve remote PC/SSH/Tailscale as a later execution adapter, not the only path. Make remote control optional and visibly different from on-device/local execution. Every run report must identify where execution occurred and who controls the environment.

### 2.3 Mobile Python editors and local runtimes

Prior research covered Pyodios, Carnets, a-Shell, Pyto, Pythonista, Coilbook, Python Code Editor & IDE, Pydroid 3 and Termux. They demonstrate that local interpreter access, editing, notebooks, packages, console and file import/export are not unique.

A special lifecycle caution comes from Pyodios: its public FAQ describes a UI timeout that does not interrupt Python code already running. This is a concrete reminder that a displayed timeout is not proof of process termination. It uses Pyodide/WebAssembly and has mobile resource constraints; do not generalize its exact behavior to every Pyodide host or native interpreter.

Sources:
- https://pyodios.caffeinatedmath.com/faq
- https://apps.apple.com/us/app/carnets-jupyter/id1450994949
- https://apps.apple.com/us/app/a-shell/id1473805438
- https://pydroid.app/
- https://play.google.com/store/apps/details?id=ru.iiec.pydroid3

**PocketCode response:** don't rebuild a generic IDE. The editor and file chooser should be only as large as needed to complete the bounded task loop. Invest in accurate run evidence, artifacts and AI handoff.

## 3. Feature comparison: gaps that matter

| Feature | Competitor pattern | PocketCode current position | Recommended disposition |
|---|---|---|---|
| Phone-started coding work | GitHub Copilot Mobile, Replit Agent | Static prototype only; no real coding backend | Study the journey; do not recreate their cloud stack |
| Remote session control | Happy | Remote path is a proposal; no adapter | Later adapter; requires PC/agent online |
| Local Python editor/interpreter | Pyto, Pydroid, Pyodios, Carnets | Simulated UI, no runtime | Reuse native/browser capability only after proof; don't compete on IDE breadth |
| Structured plan/task progress | Goose tasks, Cline Plan/Act, Scion roles | Prototype has no real work plan/state machine | Adopt typed task IDs, declared steps, progress and status provenance |
| Approval boundaries | Goose Ask/Allow/Deny; Cline approvals | Contract proposal, no real execution boundary | Adopt operation-scoped consent; no blanket powers |
| Checkpoints/rollback | Cline shadow Git refs; OpenCode snapshots | Not implemented | High-value future feature after workspace model chosen |
| Durable crash resume | OpenCode claims; OpenHands event store | No real runner or coordinator | P0 architecture requirement before real execution |
| Repository context under token budget | Aider repo map; Mini-Coding-Agent workspace snapshot | No live repo context/phone import | Add bounded project summary and relevant-file map |
| Test/repair loop | Aider lint/test-after-edit, GitHub agent tasks | UI only | Explicit verify/repair stages in a bounded manifest |
| Multi-agent isolation | Scion containers/worktrees; Goose subagents | No concurrency/agents | Defer until durable independent workspaces exist |
| Artifact handling | E2B result streams, Replit deploy outputs | Example-only artifact panel | Exact bytes, size/hash, run association, quarantine/release |
| Cross-provider report | Portable result/report patterns | Proposed plain-text report | Core differentiator: provider-neutral, bounded, honest, copyable |

## 4. Pinned open-source source review

The following source references were inspected at exact commits. These are source-level observations, not runtime or product tests.

### 4.1 Cline: best checkpoint and undo reference

Repository: https://github.com/cline/cline  
Pinned commit: `d3ecc4890e8f9bcb77182b96c77fa90575e8e145`  
License: Apache-2.0; pinned LICENSE blob `05ae14a377caf4df24e26edde0c4f7b22ef3ef30`.

Reviewed:
- `sdk/packages/core/src/hooks/checkpoint-hooks.ts`, blob `5dd05ebe646fa02ef1b280b35c4898844f1639e8`.
- `sdk/packages/core/src/session/checkpoint-restore.ts`, blob `574acd5c1025316a1fb6134f3f1089e4b2d99923`.
- `sdk/packages/core/src/session/checkpoint-diff.ts`, blob `9c2d77ab6b61272fb010cb54985a40483435126b`.
- `sdk/packages/core/src/session/checkpoint-restore.test.ts`, blob `f5da1142b405f4950bc85c70504ccef6ea3dc9bd`.
- `docs/core-workflows/checkpoints.mdx`, blob `3c73cff2ae5dbd02807c73f3993a80ee2b7ab49b`.

Implementation:
- Cline creates Git stash-shaped checkpoints and anchors them under private refs, separate from the user's visible `refs/stash`.
- It uses a private persistent `GIT_INDEX_FILE` to snapshot untracked files across turns without altering the user's real Git index.
- Checkpoint metadata stores latest/history entries with ref, createdAt, runCount and kind.
- It distinguishes a new user run from continuation/restart using current message delta and durable checkpoint history, preventing a resumed old run from overwriting its pre-run checkpoint with already-mutated workspace state.
- Restore validates checkpoint existence and that HEAD is still at its original base. If commits were added after the checkpoint or the branch was rebased/switched, restore refuses instead of moving branch history backwards.
- Before destructive restore it captures the current worktree including untracked files to a private restore transaction ref, then can commit or roll back the restore operation.
- Diffing uses Git blob batches and tracks tracked and untracked files.
- Tests check refusal after later commits, branch divergence, restoration of tracked/untracked state and ignored-file behavior.

**Adopt conceptually:** every actual attempt can receive a workspace checkpoint with stable attempt association; compare and restore code independently of conversation history; preserve untracked/input files; refuse destructive rollback when newer commits or branch divergence are detected. Expose a "view changes" diff before rollback. Record checkpoint outcomes/duration without file contents.

**Do not copy the whole implementation now:** TypeScript and tightly bound to Cline SDK/session metadata/Git host. Git CLI availability is not guaranteed on iOS/browser/native Python. Shadow Git also has storage/performance cost. Select workspace/storage backend first.

### 4.2 OpenCode: durable execution claim and bounded restart recovery

Repository: https://github.com/anomalyco/opencode  
Pinned commit: `6838d9579564438d80e68ae28bd1e0629d28fe9f`  
License: MIT; pinned LICENSE blob `6439474beed8e0271df9862eff97ffd70ec2464c`.

Reviewed:
- `packages/core/src/session/execution.ts`, blob `ce11a7a0f97dc235bcd351eca3e60ebc02a02588`.
- `packages/core/src/session/execution/restart.ts`, blob `3bf4bae98888bd6cc3773b3350a28bfd14c8afe6`.
- `packages/core/src/session/store.ts`, blob `a46f5e04816d1dafc8592f818251b5ddef328468`.
- `packages/core/test/session-execution.test.ts`, blob `edc90d4495cdba3b85183caa9ef37adb71412835`.

Implementation:
- A durable execution claim is written at turn start in the same transaction as the started event.
- Terminal success/failure or user cancellation releases the claim; shutdown interruption preserves it so a later server start detects an orphan.
- Startup recovery runs only when the managed host confirms the previous process is dead and a registration lock ensures one managed server owns the database.
- A durable per-turn resume counter is incremented before recovery, so a repeated crash cannot reset the budget. After the configured maximum (default 10 in this snapshot), it emits terminal failure and releases the claim.
- Source explicitly calls recovery **at-least-once**: local coordination prevents concurrent drains, not repeated external side effects after a crash.

**Adopt the durability principle, not the whole loop:** persist intent/claim before dispatch; tie it to run/attempt identity; retain unresolved claim if a process dies; recover only after proving previous executor is gone; count crash resumes durably; fail visibly after an owner-approved retry budget. Directly relevant to PocketCode ambiguous dispatch and RevDev orphan recovery.

**Hard caution:** a resumed model turn may repeat external side effects. Durable claim is not exactly-once execution. Reconcile idempotent operations and side-effect ledgers before replay.

### 4.3 Goose: task progress, approvals and recipes

Repository: https://github.com/aaif-goose/goose  
Pinned commit: `bfe8ccd23de1d2c47a4cb2970d522f093ae7f2ba`  
License: Apache-2.0; pinned LICENSE blob `c83043d4494071fbd93ef245a14e573c5a8280c4`.

Reviewed:
- `crates/goose-agent/src/tool_approval.rs`, blob `abab06f25c71732277611ce66f09fde72dd5a047`.
- `crates/goose/src/agents/state_machine/tool_approval.rs`, blob `48c6b4da8956ff4cbf46f7a3ab83d137dad50df7`.
- `crates/goose/src/agents/tool_execution.rs`, blob `de531afe9b8bf90d41ae764cc73c789425dddd1c`.
- `crates/goose-cli/src/session/task_execution_display/mod.rs`, blob `8c9d3a7e3dbd94194541a6a6039d216d21902cb`.

Implementation:
- Approval contract is a small trait with Allow, Deny and Ask, a request ID and correlated response. User decline has an explicit "do not retry this tool" outcome.
- Task display uses typed tasks/statuses, task IDs, progress counters, start/finish times, durations, output and failures.
- Tool notifications use best-effort nonblocking `try_send` so slow UI does not stall tool execution. Durable result should remain separate from live notification.
- Recipes are YAML task definitions with extensions, sub-recipes and subagents; useful workflow composition mechanism.

**Adopt for RevDev:** stable step IDs and typed states (pending/running/completed/failed/skipped/degraded/inconclusive); per-step progress/bounded output; explicit approval decisions with operation scope and request ID; recipe-like templates for common verification/repair sequences. Durable operation log remains authoritative; UI update events can be dropped/coalesced and rebuilt from history.

**Adopt for PocketCode:** concise progress stepper and operation-scoped consent before export, network or file writes. "Ask once per exact capability/scope", not blanket auto-approve. User decline terminates action and must not trigger repeated model attempts.

**Do not port Goose's Rust tool dispatcher/extension framework:** too large for current PocketCode, and it does not solve execution safety.

### 4.4 Scion: isolation over coordination

Repository: https://github.com/GoogleCloudPlatform/scion  
Pinned commit: `f68ab9e4701fbc3d95aebea157765d329ffcc724` (2026-11-04).  
License: Apache-2.0; pinned LICENSE blob `c88d6409cfcd0c188bfa0cd8b6949804d8cbfc5e`.

Reviewed:
- `pkg/hub/agent_lifecycle_tx.go`, blob `7b9017f4abf2be9c9e0e0711acbe2ff29708bcc8`.
- `pkg/agent/nfs_worktree.go`, blob `d23fe0f3193085ea87ff9297f232ed19914c8c58`.
- `pkg/agent/state/state.go`, blob `deb128f93f79980107b3dd75e9f5143aeb10fa62`.
- `pkg/agent/run_restart_resolution_test.go`, blob `b1eb415db7a21cada768b516589210c23bc12727`.
- `pkg/hub/agent_run_scope.go`, blob `9a08578a54ee3180122513e84428b00afc946ea0`.

Implementation:
- Scion runs independent harnesses and supports separate Git worktrees/clones.
- Lifecycle hooks run inside a DB transaction; agent-row transition, delegation edges, hooks and audit record commit atomically. Network/process operations are prohibited inside the transaction hooks.
- Worktree-per-agent uses a validated agent slug and separate worktree path/branch.
- Durable state includes run identifiers and nonce-bearing readiness markers so stale readiness from a previous run cannot count as current.
- Restart tests verify explicit per-agent configuration survives restart rather than falling back to defaults.
- Agent token run-scope checks bind token to a run; superseded/unbound tokens can be refused. In inspected config run-scope setting supports off/observe, not arbitrary enforcement.

**Adopt for RevDev only if real parallel agents become justified:** isolated worktree per agent, unique branch/attempt identity, run-scoped credentials, lifecycle and cleanup. Never start independent coding agents in one shared working tree.

**Defer for PocketCode:** full Scion is a Go server/container/orchestration product, not a lightweight mobile SDK. Reuse its separation principle and lifecycle/nonce tests, not its host/cloud/Kubernetes architecture.

### 4.5 E2B: process handle semantics

Repository: https://github.com/e2b-dev/E2B  
Pinned commit: `b1f9a3e1ad88151dca200e3f925b8b01182ee445`; Apache-2.0.

Reviewed:
- `packages/js-sdk/src/sandbox/commands/commandHandle.ts`, blob `3a0f46b5440e73f8581a6253727da71f94e72f55`.
- `packages/js-sdk/tests/sandbox/abortSignal.test.ts`, blob `e1ee32ff0a0e6e70f682cf087b4604e3c92e8876`.

Implementation:
- `exitCode` is undefined while process is running; wait resolves only after terminal result; nonzero exit throws typed error carrying exit/stdout/stderr.
- `disconnect()` stops receiving output but does **not** kill the command; `kill()` is a separate provider-side operation.
- Output retention can be disabled; then stdout/stderr are undefined, not empty.
- Abort tests use a controlled mock server request-start signal, then abort. They also test already-aborted signal, avoiding timing-based sleeps.

**Adopt for PocketCode's contract:** distinguish not-yet-terminal code from unknown/absent code, empty captured stream from unavailable/unretained output, UI disconnect from cancellation request and confirmed process termination. Use request-gated tests, not arbitrary timer sleeps.

**Do not select E2B as the $0 backend.** The SDK fronts managed sandbox infrastructure. Permissive code license does not make the hosted service free or remove data/security review.

### 4.6 Mini-Coding-Agent and mini-SWE-agent

**Mini-Coding-Agent**
- Repo: https://github.com/rasbt/mini-coding-agent
- Commit: `717cae4ff10d01773bd12951f62a575825053414`
- Apache-2.0 license blob `1e79798da4aac546989b7ca4f26bf1acfea64864`.
- `mini_coding_agent.py` blob `1bf2403e5033227e24954faad7f7ba4442f7e4c2`; tests blob `5c6269391e2011032d13b37b12450d5b044c5dc4`.
- Useful small design: workspace summary, stable prompt prefix, structured tools, approval modes, transcript/distilled memory, output clipping, bounded delegation.
- Risks: shell and writes require a proven execution boundary; local session save is ordinary write_text, not durable atomic storage.

**mini-SWE-agent**
- Repo: https://github.com/SWE-agent/mini-swe-agent
- Pinned commit `04d809ceab9df28f9adaed044884180159172930`; MIT.
- The project documents a small linear agent loop with one Bash tool and independent subprocess calls, plus pluggable local/container/bwrap environments.
- Take the small loop, transcript transparency, independent command invocation and replaceable environment seam. Do not give arbitrary Bash to untrusted code without proven OS sandbox, egress policy, resource limit, process-tree teardown and artifact boundary. (See the upstream v2 README and environment documentation.)

### 4.7 Aider: bounded repository context and verification

Repository: https://github.com/Aider-AI/aider  
Reviewed pinned commit: `5dc9490bb35f9729ef2c95d00a19ccd30c26339c` (2026-05-22; older than this review).

The repo-map pattern ranks project symbols/files by relevance and dependency centrality while fitting a context budget. Aider also emphasizes automatic lint/test commands after edits. The inspected implementation is Python and uses internal abstractions plus parser/indexer dependencies; this is not a clean extraction. I did not copy Aider code because the license file was not established from the pinned source in this pass.

**Adopt the product pattern:** send AI a bounded map of relevant files/symbols plus exact changed-file diff and last verification result. Let user choose repository scope. After a patch, run predeclared verification commands in the same workspace/attempt lineage; don't let a model self-certify tests passed.

## 5. Two isolated code references copied into PocketCode

These are **reference-only**, not product integrations. No production code imports them.

### 5.1 OpenHands atomic text writer (MIT)

Paths:
- `RESEARCH/vendor/openhands/atomic_write_text.py`
- `RESEARCH/vendor/openhands/test_atomic_write_text.py`
- `RESEARCH/vendor/openhands/LICENSE`
- `RESEARCH/vendor/openhands/README.md`

Upstream:
- Commit `2b4d980b6a54ef6685e4337e7643c40ec24be1bb`
- Source blob `cdf2b7e6807d135d6386270e1988467009543701`
- License blob `b0bd86a6335a564bd3766666bebbf014fd6a8013`

Helper: same-directory temp file, owner-only POSIX mode where supported, UTF-8 write, flush and fsync the file, then atomically replace destination; cleanup temp on error.

Limits: no parent-directory fsync; no lock/CAS, journal, multiwriter transaction, schema/hash/identity validation, symlink-safe open handle or cross-store guarantee. Windows ACL semantics not proven. Candidate for individual local state-file replacement only after platform/runtime selection.

### 5.2 Mini-Coding-Agent workspace path guard (Apache-2.0)

Paths:
- `RESEARCH/vendor/mini-coding-agent/workspace_paths.py`
- `RESEARCH/vendor/mini-coding-agent/test_workspace_paths.py`
- `RESEARCH/vendor/mini-coding-agent/LICENSE`
- `RESEARCH/vendor/mini-coding-agent/README.md`

Upstream:
- Commit `717cae4ff10d01773bd12951f62a575825053414`
- Source blob `1bf2403e5033227e24954faad7f7ba4442f7e4c2`
- License blob `1e79798da4aac546989b7ca4f26bf1acfea64864`. The copied LICENSE was replaced with the complete upstream file and its blob equals the upstream license blob.
- Adapted PocketCode helper blob after adding the required Apache-2.0 modification notice: `d91b205e6c9a23732fb95a214ddcac0731b0c27f`.

The adaptation resolves the workspace root, resolves symlinks before containment check, checks nearest existing ancestor with samefile(), and permits creating a not-yet-existing file beneath an existing internal parent.

Limits: not a sandbox and does not prevent TOCTOU replacement after validation. Does not handle hard links, Windows reparse-point subtleties, ACLs, mount points, devices, archive extraction or file-handle races. Never claim hostile-code isolation.

**Verification:** reference files and project-authored test files are committed. Exact local Git blob hashes were computed for the helper and test files; they match the PocketCode source/test blobs. Both reference suites were executed on CPython 3.13.5/Linux on 2026-11-05: OpenHands helper 5/5 passed; workspace path helper 8/8 passed. This does not constitute mobile, Windows, app integration, hostile-code isolation, or product acceptance testing.

## 6. What should be built, in priority order

### PocketCode first proof

**P0: authoritative execution evidence**
- One coordinator-owned job identity and per-run attempt identity.
- Append-only authenticated lifecycle events, bound to job/attempt and source.
- Separate natural child exit, wrapper/supervisor exit, timeout/cancel request, termination confirmation and cleanup.
- Ambiguous start acknowledgements remain UNKNOWN; no automatic redispatch.
- Resolve report-verdict precedence only after independent review and owner approval; forced termination must not be mistaken for program failure.
- UI timeout or stopped event stream is not proof worker stopped.

**P0: one bounded runner boundary**
- Select only after fixed-task comparison on iOS/Android.
- Require hard wall-clock deadline, CPU/memory/process/disk/file/output limits, egress denied by default and independent termination/cleanup evidence.
- Distinguish trusted-user convenience execution from arbitrary untrusted code.
- Do not assume Pyodide, a worker, document picker or app sandbox alone proves arbitrary-code isolation.

**P0: artifacts and result handoff**
- Exact source/input digests and output sizes/digests.
- Separate execution verdict, artifact existence, integrity and current release authorization.
- Streams labeled complete/empty/unavailable/partial/truncated with provenance.
- Bounded copyable report: source/attempt IDs, runtime, status, exit when observed, duration, outputs, cleanup and uncertainty.
- Correction creates a new linked attempt, never overwrites past results.

**P1: useful UX**
- Cline-like checkpoint/diff/restore when workspace storage is chosen.
- Goose-like task progress with per-step IDs/status; never cosmetic-only progress.
- Aider-like repository map under token budget and explicit file scope.
- Recipes/workflow templates for recurring bounded tasks; declarative, not unchecked autonomy.
- Optional remote PC/SSH/Tailscale adapter later, separately labeled.

**Defer:** multi-agent/parallel execution, extension marketplace, generic package manager, unrestricted shell, arbitrary runtime images, cloud sandbox as default, automatic AI-to-AI loop, social feed, hosted team platform and broad IDE features.

### RevDev adoption backlog

**P0 publisher/recovery first:**
- Use OpenCode's durable run claim/restart recovery pattern but strengthen for external effects: persist dispatch/publish intent, typed outcome, original attempt identity and operation-specific idempotency; after lost acknowledgement reconcile exact target before retry.
- Use Cline's checkpoint/restore pattern for source edits only after workspace/repo preconditions; do not reset branch with newer commits.
- Use Goose task/status IDs for operation manifest and progress stepper; store durable operation events first, then send best-effort UI notifications. Slow UI must not block execution.
- Use Cline/Aider diff + verify/repair model: each operation declares expected files and verification command; green checks only from real test evidence.
- Keep grouped interaction-cycle consume/terminal/audio authority independent from publisher retries.

**P1 after P0:**
- Recipe library for recurring bounded packets (source parity, static audit, tests, build, evidence capture).
- Adaptive batch size based on task risk, complexity, free-tier/time budget and recent rework; never bypass provider quota limits.
- Per-project bulkheads and worktree-per-agent only if agents truly run concurrently and each has isolated working copy.
- Project map/context summary with explicit budget and file selection.

## 7. Adoption matrix

| Source | License | Reuse now | Product target | Stop condition |
|---|---|---|---|---|
| OpenHands atomic writer | MIT | Isolated reference copy only | PocketCode local file-store adapter | No production use until directory fsync, ACL/permissions, concurrent writes and recovery contract are settled |
| Mini-Coding-Agent path guard | Apache-2.0 | Isolated adapted reference copy only | PocketCode workspace import/export boundary | No hostile-code claim; TOCTOU/platform path tests required |
| Cline checkpoint | Apache-2.0 | Study/adapt later; no code copied | Both undo/checkpoint | Git/runtime availability and workspace ownership not selected |
| OpenCode resume claim | MIT | Pattern adopted in design only | Both durable recovery loops | At-least-once; cannot replay non-idempotent effects blindly |
| Goose task/progress/approvals | Apache-2.0 | Pattern adopted in design only | RevDev stepper and PocketCode permissions | Do not block execution on UI event delivery; authorization is scoped |
| Scion worktree isolation | Apache-2.0 | Pattern adopted in design only | RevDev future parallel agents | Requires isolated runtime/worktree/credentials and cleanup proof |
| E2B command handle | Apache-2.0 | Pattern adopted in contract only | PocketCode runner adapter semantics | Hosted sandbox cost/security not proven $0; no selection |
| mini-SWE-agent loop | MIT | Pattern reference only | Possible harness architecture | Bash requires a proven sandbox |
| Aider repo map | License not verified here | Concept only | Context reducer | No code copy until license/deps pinned |
| Replit/GitHub Copilot Mobile | Proprietary/product | Feature benchmark only | UX reference | No code copy or assumed equivalent pricing/security |
| Happy | MIT pinned source | UX/protocol study | Optional remote companion | Requires a computer; current source snapshot predates Happy Desktop messaging |

## 8. Immediate next work

1. Keep both vendor utilities isolated; verify exact file hashes and test command/results before adoption.
2. Review checkpoint strategy: Git not guaranteed on mobile; compare local document-provider storage, browser workspace snapshots and remote worktree adapter. Define portable snapshot metadata separately from backend.
3. Prepare RevDev task-manifest/progress model mapped to existing AWC/P8U requirements, without replacing mission envelope.
4. Obtain Claude review of Cline/OpenCode checkpoint/recovery transfer and Gemini red-team review of path guard/approval boundary.
5. Reassess after the exact PC installed-source inventory, not before.

## 9. Evidence limits and non-actions

- Product capability statements derive from public documentation and pinned upstream README/docs, not hands-on installations or device tests.
- Source observations are pinned to commits/file blobs above; re-pin before implementation.
- PocketCode prototype remains static/simulated. No execution runtime/provider/store selected.
- Two copied utilities are in research-only folders; no product integration.
- No implementation, provider workload, account, spend, test, build, browser/device acceptance, Actions, PR update, install, restart, host/queue, merge or deployment was performed in this research pass.
