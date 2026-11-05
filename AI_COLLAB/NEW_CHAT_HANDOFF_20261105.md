# PRIMARY NEW-CHAT HANDOFF — PocketCode + RevDev — 2026-11-05

**Purpose:** Transfer the live programme to a new ChatGPT conversation without restarting discovery, losing owner constraints, confusing proposals with verified evidence, or changing protected project state. This document supersedes earlier handoff snapshots for current status. Earlier handoffs remain useful for detailed historical reasoning and are linked below.

**Owner operating mode:** phone-first; no reliable PC/local access planned until approximately 2027-02-28.  
**Budget:** $0 default.  
**Current work mode:** source research, evidence reconciliation, and documentation continuity only.

## 0. Read-first instructions for the next ChatGPT

You are continuing the existing PocketCode + RevDev programme. This is not a new project, greenfield rewrite, generic brainstorming request, or invitation to repeat broad discovery.

1. Read this entire handoff before taking action.
2. Verify current GitHub branch heads, compare each research branch against main, and inspect current PR state. The SHAs/counts below are a snapshot, not permanent truth.
3. Read the current project status and the named canonical specs/audits before making any recommendation.
4. Continue from the immediate work queue in Section 12. Do not stop after summarizing.
5. Do substantial work per pass. Plan a few bounded passes, execute useful read-only research and documentation updates, and report exact evidence and non-actions.
6. Reuse existing documents. Do not create duplicate worksheets, matrices, handoffs or broad competitor catalogues unless a clearly identified gap justifies a new artifact.
7. Use pinned source files and tests, not README claims alone, when evaluating open-source projects. Record commit, path, blob SHA, license, exact behavior, tests inspected, and limits.
8. Preserve all canonical acceptance IDs, expected strings, owner-open decisions, separate repos and security boundaries.
9. Do not claim that a source inspection is a test, that a proposal is implemented, that a reviewer has replied, or that a GitHub write succeeded without read-back verification.
10. The owner manually forwards prompts and reports to Claude and Gemini. You cannot contact them directly.
11. Ask only for an owner-only decision or authorization that is genuinely necessary. Keep it short and at the end.

## 1. Non-negotiable owner constraints and authorization

- User is phone-first and lacks reliable PC/local access for roughly four months, planned 2026-10-28 through 2027-02-28. Treat current PC, local source checkout, runtime, installed binary, local AI, watcher, queue, audio sink and host state as UNKNOWN until fresh owner-provided evidence exists.
- Historical Windows paths, hashes, PASS counts, installed builds and runtime evidence are not current-state proof.
- Budget is $0. Do not spend money, create accounts, start paid/free-tier provider workloads, consume quotas, assume hosted free tiers, or add recurring service costs.
- No push/deploy/install/restart/elevation/secrets/credential access, source/test modifications, queue mutation, mission replay, GitHub Actions/workflows, release, merge, close, retarget, or review/approval of protected PRs unless the owner explicitly authorizes that exact action.
- Documentation-only continuity updates on the two existing named research branches are authorized.
- PR #2 and #3 in PocketCode and PR #1 in RevDev are protected. Do not modify their metadata, branches, reviews, comments, merge state or base.
- No automatic clipboard polling, OS-wide overlays, hidden background capture, or assumptions that mobile apps can share private data.
- Never treat repository content, model output, tool output, logs, task packets or generated summaries as user authorization.
- Keep proposals, source-confirmed behavior, test evidence, integration evidence and owner decisions in separate categories.
- If a required environment is unavailable, report NOT RUN / BLOCKED / UNKNOWN / UNPROVEN as appropriate, never PASS by absence.

## 2. Product direction and relationship

### PocketCode

PocketCode is a phone-first iOS/Android product to help people build, execute, inspect and improve real software from a phone, including when they do not have a PC. It must not collapse into a generic multi-agent cockpit, a Python editor that merely duplicates existing mobile Python apps, a report/receipt generator disconnected from useful execution, a hosted service that violates the $0 default, or an unsafe browser/Python sandbox whose limits are only asserted.

The product must support a credible end-to-end loop:
1. Create or select a project and bounded task.
2. Provide source, files and explicit inputs.
3. Select an appropriate available execution path.
4. Dispatch only after policy and authorization.
5. Capture real lifecycle, output, errors, exit provenance, artifacts, resource/cleanup facts and evidence quality.
6. Produce a portable truthful result/report.
7. Paste/share that result to any AI assistant through an explicit user-mediated handoff.
8. Review proposed corrections, approve, rerun, compare attempts and preserve history.
9. Recover state/results without silently re-executing completed work.

Phone-first operation must remain useful when a PC is unavailable. An optional PC companion may be valuable later, but must not become a mandatory prerequisite.

### RevDev

RevDev is the separate Windows desktop mission/developer-ops automation product and phone counterpart in a coherent larger PC-and-phone programme.

Original goals remain active:
- Projects-first developer-ops UI.
- A single “done” starts a substantial bounded batch of scripts/operations plus verification and repair, reducing repeated AI “done” exchanges.
- Progress stepper with per-operation green/red states.
- Adaptive batch sizing based on complexity, model capability, context and free-tier limits.
- Terminal pass/fail sound.
- Return-to-AI continuation loop.
- Durable state and evidence.
- Reliable publication, recovery, grouped interaction cycles and accurate completion semantics.

### Convergence boundary

PocketCode and RevDev should converge in product direction, vocabulary and selected conceptual foundations: provider-neutral AI workflows, durable task packets and operation identity, bounded multi-pass work, lifecycle/result semantics, evidence provenance, compact checkpoints, review/approval and recovery patterns.

But remain separate repositories, roadmaps, clients, adapters, runtimes, acceptance suites, release gates and platform-specific security boundaries. No repository merge, shared runtime, common privileged process, or security-boundary change is implied. Any actual shared implementation or protocol requires a separate evidence-based decision.

## 3. Three-AI collaboration model

Current owner-approved roles:
- **Claude:** lead developer and architecture/implementation reviewer.
- **Gemini:** co-developer and independent security/spec auditor.
- **ChatGPT:** continuity holder, evidence reconciler, acceptance architect, cross-project coordinator.

The owner manually forwards work. Do not say you contacted Claude or Gemini. Use independent review when it can challenge a real decision, not as a ritual. Give one primary owner for each work item, request focused counterexamples and evidence, then reconcile. Do not automatically accept any AI's architectural recommendation. Owner goals and canonical contracts take precedence.

## 4. Current verified GitHub snapshot (2026-11-05)

### PocketCode
- Repository: marcelosofficial-ctrl/PocketCode-
- Research branch: pocketcode-ai-workflow-director-research-2026-10-28
- Current branch head fetched from GitHub: e382a73f4468eaa6b13c63d212e0ed25c6c96a4e
- Compare against main: ahead 650, behind 0.
- Merge base: 555840d8d83342513d9cd353d4d1522d46a5c82d.
- PR #2: open, titled “Add chat checkpoints and harden report-contract regressions”. Current search result did not expose draft/head metadata. Do not infer those fields.
- PR #3: open, titled “Draft: Add evidence-led PocketCode research baseline”. Current search result did not expose draft/head metadata. Do not infer those fields.
- Neither PR was modified in this work.

### RevDev
- Repository: marcelosofficial-ctrl/DevRelay-Missions
- Research branch: review/revdev-adaptive-ai-workshare-2026-10-27
- Current branch head fetched from GitHub: 9deaf93c56d61ad112e2f71ab678e2c95770e60d
- Compare against main: ahead 555, behind 0.
- Merge base: 058f9025319d12e76195659c715ccb4afce133b8.
- PR #1: open, titled “docs(revdev): add RelayRef continuity handoff (2026-10-27)”. Current search result did not expose draft/head metadata.
- PR #1 was not modified in this work.

Large ahead counts are not a quality signal and do not imply merge readiness. Do not merge, rebase, squash or clean up branches as a routine action. Re-fetch current state before consequential work.

## 5. Current status and work completed in this continuation

### 5.1 PocketCode source-level competitor/code research

Created and verified:
- RESEARCH/HAPPY_AGENT_DAEMON_SOURCE_AUDIT_20261105.md
- GitHub blob SHA: 766bdac59bcff345dbb9564f6a9c590d429b952a
- 253 lines.
- Pinned upstream Happy Agent commit: slopus/happy-agent@4c1c2727e9259eb46f29829133144be55754f807.
- MIT license.

This source audit examines Happy Agent's daemon, durable function queue, SQLite storage, event journal, process/session manager, timeout and cancellation behavior, permissions, sandbox and database migration code/tests. It is a PC-host architecture reference, not a chosen PocketCode runtime, provider or mandatory dependency.

Key findings:
- Happy Agent is a headless Node/Bun daemon, with clients connecting through local/network APIs. It is not an iPhone-native runner and cannot solve phone-only execution without a PC.
- Provider access uses local tool credentials or configured access. It is not a free-tier bypass.
- Its durable function queue uses unique operation IDs while a call is pending, commits before dispatch and replays pending work after restart. It explicitly has at-least-once side-effect semantics. A crash after an external side effect but before completion can execute the operation again. Completion deletes the pending call and per-call KV state. Therefore it is not an immutable execution/publication ledger.
- Its event replay journal is bounded (default 10,000 events / 32 MiB, with per-event bounds) and separate from canonical conversation history. Cursor expiration must be explicit; a bounded replay stream is not the only permanent evidence archive.
- It distinguishes one-shot command timeout, which requests process termination, from long-running session wait timeout, which can mark a session timed out while the process continues. Its tests inspect the continued output after a session wait timeout. This reinforces that a phone/client wait timeout is not proof of runner termination.
- Process results include timeout/abort/killed distinctions and bounded output byte/omission information.
- Permission decisions are bound to exact tool arguments; reviewer-unavailable/unproven is not permission. Approval must not be reused after material arguments/target/policy change.
- Missing sandbox prerequisites fail closed. Sandbox tests skipped because the environment cannot run the boundary are unproven, not passed. OS support and test coverage differ; do not generalize Linux/macOS evidence to Windows.
- SQLite migration history is immutable/ordered, migration marker is transactional, newer schema is rejected, and a kernel-backed process lock is used for exclusive local ownership.
- Best adoption is pattern/contract extraction, not importing the whole package.

High-value pinned source map is in the audit. Important upstream files include:
- packages/happy-agent-modules/sources/durableFunctions/DurableFunctionsModule.ts
- packages/happy-agent-modules/sources/durableFunctions/SqliteDurableFunctionsStorage.ts
- packages/happy-agent-modules/sources/events/EventsDatabase.ts
- packages/happy-agent-modules/sources/events/EventsModule.ts
- packages/happy-agent-compute/sources/host/createHostShell.ts
- packages/happy-agent-compute/sources/processes/NativeProcessManager.ts
- packages/happy-agent-compute/sources/host/createHostCompute.ts
- packages/happy-agent-modules/sources/permissions/impl/snapshotPermissionArguments.ts
- packages/happy-agent-base/sources/AgentStorage.ts
- packages/happy-agent-base/sources/AgentSQLiteProcessLock.ts

The upstream tests were inspected, not rerun by PocketCode. No Happy Agent code was copied into product code.

Existing companion research that should be read rather than duplicated:
- AI_COLLAB/COMPETITOR_FEATURE_AND_OPEN_SOURCE_REUSE_DEEP_DIVE_20261105.md
- RESEARCH/CODE_LEVEL_OPEN_SOURCE_REUSE_REVIEW_20261105.md
- RESEARCH/OPEN_SOURCE_AGENT_ARCHITECTURE_AND_CODE_ADOPTION_REVIEW_2026-11-05.md
- RESEARCH/MOBILE_RUNNER_EVIDENCE_SOURCEABILITY_MATRIX_20261105.md
- AI_COLLAB/VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md
- AI_COLLAB/MOBILE_RUNNER_TASK_ALIGNED_RECEIPT_SPEC_20261103.md
- AI_COLLAB/PROVIDER_NEUTRAL_RECIPE_AND_DURABLE_TASK_MANIFEST_PROPOSAL_20261105.md
- AI_COLLAB/CROSS_PROJECT_CONTINUATION_ADDENDUM_20261105.md

Current source-level research also covers MCP Tasks, Happy mobile/agent, Goose recipes, a-Shell, Aider, OpenHands, Cline, OpenCode, LangGraph and related projects. Reuse only small, license-compatible, source-reviewed components with clear boundaries. Existing isolated copied reference helpers/tests must not be mistaken for production integration.

### 5.2 PocketCode product proof remains unvalidated

- Canonical fixed task and worksheet exist. The task is a bounded CSV-to-JSON Python transformation with valid and malformed-input cases.
- Worksheet: AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md.
- Canonical main.py fixture SHA previously recorded: 70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7.
- Isolated Python sanity check passed fixture logic only.
- Actual iPhone runner comparison, Safari/PWA, Pyodide, remote PC and hosted provider comparisons remain NOT RUN.
- EVAL-06 is a comparison of baseline versus the complete Workflow Director bundle, not an isolated-feature ablation.
- The paired report-correction experiment compares native raw evidence versus the portable report/handoff. It is designed but NOT RUN.
- Keep model/settings and input identical, counterbalance/randomize order, record context and usage, blind scoring where possible, and avoid confounding order/time/free-tier changes.
- Product differentiation remains UNVALIDATED. Local mobile Python already exists; execution alone is not a differentiator.

### 5.3 PocketCode evidence/verdict work

The verdict matrix AI_COLLAB/VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md contains candidate VP-01..20 cases. It distinguishes pure projection tests from fake-adapter/integration/host/product evidence. No cases have been run.

Keep separate: raw execution facts; child exit code versus wrapper exit code; policy authorization; outcome/verdict projection; evidence quality/completeness; cleanup; artifact release; report/handoff.

Canonical CASE-04 requires trusted timeout to be INCOMPLETE / timed_out. A generic nonzero exit code may conflate a natural child exit with wrapper/forced termination. Preserve natural child exit, wrapper exit, timeout, cancellation, signal, termination confirmation, collection and cleanup as distinct evidence. Contradictory program_failed + exit_code 0 remains a case requiring explicit treatment. D-01..D-08 remain owner-open/proposed, not approved.

scripts/report_contract.py pure helper currently treats valid integer nonzero exit or program_failed as FAIL; succeeded + 0 as PASS; otherwise INCOMPLETE. This pure behavior is not proof of correct mobile/host integration.

### 5.4 RevDev P8U publication recovery work

Created/updated and verified:
- resume/revdev/P8U_PUBLICATION_OPERATION_STATE_MACHINE_AND_FAULT_INJECTION_PLAN_2026-11-05.md
  - current blob SHA: a8a3cbac94bbc7133f9f53a0941837ba558307e0
  - 226 lines.
- resume/revdev/R5_MAINTENANCE_PUBLISHER_CONSOLIDATED_SOURCE_FINDINGS_20261105.md
  - current blob SHA: 037e662b4b87d07ab1992a7661940c18227e86c2
  - 247 lines.
- resume/revdev/P8U_OWNER_DECISION_REGISTER_2026-10-29.md
  - blob SHA: ffc8a39c69644d59e5674bc8529b065951a47613.
- Canonical P8U acceptance JSON SHA: e60c506d00e6ef6e1f1279b40e124a5cff354a6b, unchanged.

The candidate state machine is design-only. It proposes stable publication operation identity, append-only typed attempts, capture of exact local terminal result, prepare publication bytes once, classify target before write, reconcile ambiguous acknowledgement by exact read-back, then reconcile mutable views and close. It maps fault-injection points to P8U-01..12. It does not alter canonical acceptance IDs, expected wording, owner decisions or implementation approval.

Key source findings:
- P8U-04: same project/mission/runId collision accepted as idempotent existing without exact bytes/hash check.
- P8U-05: different runId at same immutable mission path treated as duplicate mission suppressed rather than integrity conflict.
- Existing result is preserved, not overwritten, but source evidence is insufficient to prove identity correctness.
- Historical local terminal result SHA: bc9af36bf5deb9602325cb9515af347e4f9c37aa2d6f0102430c5b4aa9a1a58b.
- Historical remote serialized result SHA: 577a1b14e5cab19f04c366a2e3847072388202bc4f1c75c897cd65c77a4f61d7. Difference is due to publication enrichment/serialization; it is not by itself proof of semantic loss.
- Three-layer identity is required: (A) exact original terminal bytes, (B) semantic projection of product result, (C) exact outbound publication envelope bytes. Capture prepared outbound bytes/hash and reuse them on retry. Do not rebuild with changing timestamps/metadata/serializer under the same operation identity.
- P8U-03: publisher wrapper returns ExitCode/Text/Json, not typed HTTP status/headers. Retry is fixed 150 ms × attempt, max 5, only for branch-ref PATCH failure. No explicit Retry-After/primary reset metadata. Earlier retry failure trace can be lost.
- P8U-06: access/absence classification relies on text matching 404/not found, not typed HTTP status/header. Authenticated gh status does not prove exact repo/branch/endpoint/operation permission. A 404 may hide inaccessible private resources.
- P8U-08: local named mutex is not cross-machine coordination. A stale writer could potentially overlay old payload on retry under some writer topologies, but reachability is not proven. Treat as conditional hypothesis, not confirmed live defect.
- Publisher uses Add-Member -Force for metadata fields. Collision with legitimate source fields is a risk question, not a proven historical collision.
- Current installed publisher parity, writer topology, PC state and live queue remain UNKNOWN.

P8U state-machine invariants:
- Publication retry never re-executes mission work.
- Matching IDs alone are insufficient for idempotent success.
- Ambiguous acknowledgement requires exact read-back/reconciliation.
- Access failure is not product failure.
- Mutable “current” views are separate from immutable history.
- No duplicate consume/terminal/audio effects.
- No newer result overwritten by older publication.
- No silent close of wrong interaction cycle.

### 5.5 RevDev open decisions and release gates

OD-01..OD-08 all remain OPEN. Register is a static owner decision record, not a policy or acceptance spec. Do not infer or silently choose values:
- OD-01 retry ceilings and elapsed-time budget.
- OD-02 server-directed retry deadline, clock skew and malformed Retry-After.
- OD-03 reservation reuse where durable send evidence is absent.
- OD-04 whether transient pointer/ledger regression is forbidden or only final-state correctness matters.
- OD-05 measurable no-log-flood limit/window.
- OD-06 accepted dispatch intent with no runner start, and whether a new/additive acceptance case is needed.
- OD-07 P8U-09 fallback dependency-failure scope.
- OD-08 sink/audio acceptance layer: logical intent, sink delivery call, acknowledgement/receipt, or physical audible effect.

Canonical P8U remains 12 ordered scenarios / 38 expected assertions. P8U-01..12 and P0-D 1–10 remain NOT RUN. Product P0 remains OPEN/release-blocking. Installed UI/audio acceptance remains BLOCKED. No mission replay.

RevDev acceptance suite IDs remain separate: AEC-001–012, AWC-001–018, P8U-01–12, P0-D 1–10.

PocketCode canonical IDs remain separate: LOOP-01–14, CASE-01–16.

Do not merge, renumber or remap any of these suites.

## 6. Open-source research and adoption policy

The user explicitly wants us to study competitors and reuse open-source work rather than reinventing it. Continue that, but do it rigorously.

Adoption rules:
1. Inspect actual source and tests at pinned commit.
2. Record license and any mixed notices.
3. Copy only small, isolated, useful code when it fits the current language/platform and can be independently tested.
4. Keep upstream headers/notices and record provenance.
5. Do not import large frameworks or runtime dependencies before platform, security, maintenance and licensing review.
6. Do not claim copied reference code is product-integrated.
7. Do not use an upstream green test as proof of our adapter/platform path.
8. For security boundaries, test the actual target OS and fail closed when prerequisites are absent.

Relevant competitor/reference decisions:
- **Happy Agent:** strongest reviewed PC-host daemon reference; durable tasks are at-least-once; event journal bounded; session timeout can differ from process termination. Do not adopt wholesale.
- **MCP Tasks:** useful durable task lifecycle, polling, result retrieval and recovery semantics. MCP must remain optional, not the only extension model.
- **Goose:** recipe/workflow composition and approval patterns are useful. Add explicit canonical-root containment, symlink/race protection, cycle/depth limits. A free-form shell retry hook is not safe to copy as an implicit action.
- **Cline:** workspace checkpoint/restore and compare-and-swap guard are useful patterns. Do not confuse destructive worktree reset with immutable publisher recovery. Preserve user changes and ignored/untracked data under explicit policy.
- **OpenCode:** per-tool permission patterns; approvals should bind to a stable action descriptor, canonical arguments, resolved target, workspace identity, policy version and bounded expiry.
- **LangGraph:** task-level pending writes and partial completion are useful, but storage writes need failure injection and fresh-process read-back. A method throwing does not prove no partial persistence.
- **Aider:** repository context maps, architect/editor separation, bounded context packet and token estimates are useful future product features.
- **OpenHands:** useful recovery patterns but inspect action-batch/observation and EventLog crash boundaries; no unreviewed fix adoption.
- **a-Shell and other iOS Python apps:** prove local phone Python execution already exists; PocketCode must prove value beyond execution.
- **Pyodide 0.31.4 / 314.0.7 source findings:** empty jsglobals does not remove pyodide_js, FS/runtime APIs, persistent IDBFS, JS evaluation or cached proxies. Restrictive CSP test is expected-fail on Safari due wasm-unsafe-eval support. Do not call stock Pyodide a hostile-code sandbox. A trusted-bootstrap attenuation idea remains unproven and may require a fork.
- Prior Happy Agent Linux strict-service review is a useful containment reference, not a selected dependency. Windows adapter unsuitable as-is due broad filesystem read and inherited environment credentials. Gaps include trusted absolute deadline, CPU/disk quota, input/special-file/egress/parent-death proof.

## 7. Technical semantics that must remain distinct

Across both projects, preserve these separate facts:
- user intent;
- policy decision;
- authorization;
- dispatch accepted;
- runner started;
- child process natural exit;
- wrapper/supervisor exit;
- wait deadline;
- execution deadline;
- cancellation requested;
- termination signal sent;
- process tree confirmed exited;
- stdout/stderr collection complete or truncated;
- cleanup attempted/completed/failed;
- artifact captured/validated/released;
- result committed;
- report projected/published;
- remote acknowledgement known/unknown;
- recovery/reconciliation outcome.

A client disconnect, phone-side timeout, provider response timeout or missing log does not prove the runner stopped or that an operation did not happen.

Use conservative semantics:
- trusted enforced timeout follows PocketCode canonical CASE-04: INCOMPLETE / timed_out, with cause separately recorded.
- provider/wrapper failure without trustworthy child exit is INCOMPLETE/UNKNOWN unless confirmed failure evidence exists.
- optional diagnostics are distinct from case-required evidence.
- result, cleanup and artifact release are separate.
- execution facts are not policy authorization.
- a PASS requires all evidence required by that canonical case and a trustworthy terminal record.
- missing, inaccessible, unsupported or skipped boundary evidence is NOT RUN / UNKNOWN / UNPROVEN / BLOCKED, not PASS.

## 8. PC-return plan

When the owner regains reliable PC access, do not immediately run the old workflow or replay the mission.

### RevDev read-only inventory first
- Fingerprint installed publisher, maintained source, installer payload, watcher/reconciler, queue, local result and relevant logs.
- Establish source-installed parity and exact hashes.
- Identify writer topology and whether multiple machines/processes can publish.
- Inspect original local terminal result and historical publication evidence.
- Confirm actual GitHub CLI/API status/header behavior with safe read-only probes.
- Establish whether current queue contains an orphan or newer result.
- Only after a separate authorization, design isolated synthetic transport/fault injection. Never replay the recovered P8U mission.

### PocketCode
- Identify actual available iOS/Android/PC execution paths and app state.
- Run only the authorized fixed-task protocol, capture raw evidence and exact environment.
- Test evidence collection, cleanup and artifact release independently.
- Conduct the paired baseline/full-Director comparison with counterbalanced order and blinded scoring where possible.
- Do not claim hostile-code isolation until the exact platform boundary is independently tested.

## 9. Immediate next work queue for the new chat

Execute in this order, adjusting only if fresh evidence changes priority:

### Pass A — Finish continuity and reviewer packets
- Confirm both new handoff files and cross-links read back correctly.
- Prepare two concise copy-ready review requests:
  1. Claude architecture challenge of RevDev publication operation state machine, especially crash windows, operation identity, immutable payload, outbox and cross-writer behavior.
  2. Gemini security/spec challenge of the same design, especially identity collision, auth/absence ambiguity, retry deadline, stale approval, cross-machine coordination, event/audio side effects and evidence gaps.
- Ask each to identify concrete counterexamples, exact source lines, required invariants and which proposed state transitions are unsafe. No broad redesign request.
- Keep owner decisions OD-01..OD-08 OPEN.

### Pass B — PocketCode EVAL-06 and receipt sourceability
- Inspect existing fixed-task worksheet and evidence sourceability matrix.
- Audit whether EVAL-06 is actually fair: identical source/input/model/settings, randomized/counterbalanced order, context and usage capture, scoring blindness, repeated trials feasible within free-tier constraints.
- If there is a real gap, update the existing worksheet, not create a duplicate.
- Map each proposed receipt field to an actual source path, whether it is mandatory, optional, unavailable or derived. Do not assume mobile runner capabilities.
- Preserve the distinction between pure report-projection tests and real runner/host/device evidence.

### Pass C — RevDev state machine consistency
- Re-read the exact canonical P8U JSON and OD-01..OD-08.
- Check every proposed state/transition/fault injection against canonical scenario wording and expected strings.
- Mark any state/transition that could accidentally imply a new acceptance policy as proposal-only.
- Do not change canonical JSON, IDs, expected strings, owner register or implementation.
- Reconcile Happy Agent at-least-once queue behavior against the immutable publication ledger design. A pending queue is not a result archive.

### Pass D — Only then consider further upstream research
- Search for a narrow missing feature that materially improves the product (e.g. durable outbox, cross-process lock/CAS, task-level partial completion, mobile-to-host reconnect).
- Inspect source and tests at pinned commits.
- Avoid another broad catalogue. Do not add a framework just because it is popular.
- If no material decision remains, stop research and consolidate the implementation-ready backlog.

### Pass E — PC-return prep
- Keep one compact read-only inventory/checklist and exact commands/scripts prepared.
- Do not execute local commands until the owner has access and authorizes the relevant steps.

## 10. Exact important files and links

### PocketCode
- Prior detailed handoff: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/NEW_CHAT_HANDOFF_20261103.md
- Fixed-task worksheet: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md
- Evidence/verdict matrix: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md
- Mobile receipt spec: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/MOBILE_RUNNER_TASK_ALIGNED_RECEIPT_SPEC_20261103.md
- Sourceability matrix: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/RESEARCH/MOBILE_RUNNER_EVIDENCE_SOURCEABILITY_MATRIX_20261105.md
- Happy Agent source audit: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/RESEARCH/HAPPY_AGENT_DAEMON_SOURCE_AUDIT_20261105.md
- Competitor deep dive: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/COMPETITOR_FEATURE_AND_OPEN_SOURCE_REUSE_DEEP_DIVE_20261105.md
- Cross-project addendum: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/CROSS_PROJECT_CONTINUATION_ADDENDUM_20261105.md
- Provider-neutral recipe/task proposal: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/PROVIDER_NEUTRAL_RECIPE_AND_DURABLE_TASK_MANIFEST_PROPOSAL_20261105.md

### RevDev
- Prior detailed handoff: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/NEW_CHAT_HANDOFF_REVDEV_POCKETCODE_2026-11-03.md
- Current goals: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/CURRENT_GOALS.md
- P8U operation state machine: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/P8U_PUBLICATION_OPERATION_STATE_MACHINE_AND_FAULT_INJECTION_PLAN_2026-11-05.md
- Consolidated publisher findings: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/R5_MAINTENANCE_PUBLISHER_CONSOLIDATED_SOURCE_FINDINGS_20261105.md
- Owner decisions: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/P8U_OWNER_DECISION_REGISTER_2026-10-29.md
- Upstream adoption decision record: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/UPSTREAM_ADOPTION_AND_IMPLEMENTATION_DECISIONS_2026-11-05.md

## 11. Explicitly not done / do not overclaim

- No source or product tests were changed or run in this continuation.
- No PocketCode iPhone/Android/Windows/macOS/Linux product execution.
- No paired EVAL-06 or report-correction experiment.
- No hostile-code sandbox proof.
- No Happy Agent product integration or dependency selection.
- No PocketCode runtime, provider, framework or backend selected.
- No RevDev production code change, P8U/P0-D execution, mission replay or live queue mutation.
- No PC state inspection, install, restart, deployment or secrets access.
- No Claude/Gemini review response received in this work.
- No PR modified, merged, closed, retargeted, reviewed or approved.
- No GitHub Action run.
- No canonical acceptance IDs, expected strings, D-01..D-08 or OD-01..OD-08 closed.

## 12. Copy/paste prompt for the next ChatGPT conversation

Paste the entire block below as the first user message in the new chat. It is intentionally self-contained, but the linked GitHub handoff and named project docs remain the source of truth for details.

---

You are continuing my existing PocketCode + RevDev programme. Do not restart discovery or treat this as a new project. Read this complete instruction and the linked current handoff first:

https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/NEW_CHAT_HANDOFF_20261105.md

Also read the RevDev companion handoff:

https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/NEW_CHAT_HANDOFF_REVDEV_POCKETCODE_2026-11-05.md

**Your job:** Continue the existing programme efficiently. Plan several useful passes, execute them, and make sensible executive decisions that reduce uncertainty and advance the product. Do not stop at a recap. Do not ask me to repeat context. Use GitHub to preserve continuity and read back any documentation changes.

**Product goals:** PocketCode is a phone-first iOS/Android coding product for creating/selecting projects, supplying code and files, executing bounded tasks in a real appropriate environment, inspecting actual results/errors/artifacts, producing truthful evidence-rich reports, handing those reports to any AI assistant, reviewing corrections and rerunning while preserving attempt history. It must work usefully without a PC and must prove value beyond local Python editors. RevDev is the separate Windows desktop developer-ops/mission product: Projects-first UI, one “done” starts a bounded multi-operation batch with verification/repair, adaptive batch sizing, per-operation progress, terminal pass/fail sound, AI continuation, durable state/evidence and reliable publication/recovery. The products converge conceptually but keep separate repos, roadmaps, clients, adapters, runtimes, acceptance suites, release gates and security boundaries.

**Three AIs:** Claude is lead developer and architecture/implementation reviewer. Gemini is co-developer and independent security/spec auditor. ChatGPT is continuity holder, evidence reconciler, acceptance architect and cross-project coordinator. I manually forward requests/reports. You cannot contact the other AIs directly. Do not claim you did.

**Phone-only and budget:** I do not have reliable PC/local access until approximately 2027-02-28. Treat PC, source checkout, runtime, installed binary, local AI, watcher, queue, audio sink and host state as UNKNOWN. Budget is $0. Do not spend, create accounts, start provider workloads, consume paid quotas, or assume free-tier availability.

**Authorization:** Documentation-only continuity updates on the two existing research branches are authorized. Do not push/deploy/install/restart/elevate/access secrets, change source/tests, mutate queues, replay missions, run Actions, merge/close/retarget/review/approve protected PRs, or weaken security boundaries without my explicit authorization. PocketCode PR #2/#3 and RevDev PR #1 are protected. Preserve all canonical acceptance suites and owner decisions. No new runtime/provider/framework is selected.

**Current branches:** PocketCode repo marcelosofficial-ctrl/PocketCode-, branch pocketcode-ai-workflow-director-research-2026-10-28. RevDev repo marcelosofficial-ctrl/DevRelay-Missions, branch review/revdev-adaptive-ai-workshare-2026-10-27. Verify exact current branch heads, ahead/behind counts and PR state before consequential work. Last verified snapshot is in the handoff.

**Canonical acceptance:** PocketCode LOOP-01..14 and CASE-01..16. RevDev AEC-001..012, AWC-001..018, P8U-01..12, P0-D 1–10. Never merge, renumber or remap them. PocketCode D-01..D-08 and RevDev OD-01..OD-08 remain owner-open/proposed. Preserve CASE-04 trusted timeout as INCOMPLETE / timed_out. Separate child exit, wrapper exit, client wait timeout, runner deadline, cancellation, confirmed termination, collection, cleanup, artifact release and report projection. Missing/inaccessible/unproven evidence is not PASS.

**Current PocketCode state:** Fixed CSV-to-JSON task and worksheet exist. The isolated fixture sanity check passed, but actual product-path runner comparison is NOT RUN. EVAL-06 compares baseline against the full Workflow Director bundle, not one isolated feature. Paired raw-evidence versus report correction experiment is designed but NOT RUN. Product differentiation remains UNVALIDATED. Use identical task/model/settings, counterbalance order, capture context/usage, blind scoring where possible and respect $0/free-tier constraints. The verdict/provenance matrix has candidate VP-01..20 tests, none run. Receipt fields must be traced to actual evidence sources; do not assume mobile runner capabilities.

**Current RevDev state:** RelayRef v0.9 Python reference self-test 293/293, Python-only. C#/Windows/product NOT RUN/BLOCKED. P8U focuses on orphan-result recovery and grouped interaction-cycle reliability. Current source findings include P8U-04 same-ID collision accepted without exact bytes/hash; P8U-05 different runId at same immutable path treated as duplicate suppression; P8U-03 fixed retry behavior and missing typed server retry metadata; P8U-06 text-based 404/access classification; P8U-08 conditional cross-writer risk, not confirmed reachable/live. A candidate publication operation state machine and fault-injection plan exists. It is design-only. Three identities are required: exact local terminal bytes, semantic product-result projection, exact outbound publication envelope bytes. Ambiguous acknowledgement requires exact target read-back. Retry must never rerun mission work. P8U/P0-D remain NOT RUN; P0 is release-blocking. OD-01..OD-08 all OPEN. Never replay the historical mission.

**Latest open-source decision:** Happy Agent daemon was inspected at pinned MIT commit 4c1c2727e9259eb46f29829133144be55754f807. It is a strong PC-host architecture reference, not a phone-native runner or selected dependency. Its durable queue is at-least-once and deletes pending rows on completion; it is not an immutable result ledger. Its bounded event journal is not permanent canonical history. It distinguishes one-shot kill timeout from long-session wait timeout that leaves the process running. Its permission and sandbox tests distinguish proven from unproven boundaries. Read RESEARCH/HAPPY_AGENT_DAEMON_SOURCE_AUDIT_20261105.md. Other reviewed projects include MCP Tasks, Goose, Cline, OpenCode, LangGraph, Aider, OpenHands and a-Shell. Adopt small proven patterns, not whole frameworks.

**Immediate tasks:**
1. Verify handoff files and all cross-links on GitHub.
2. Prepare focused copy-ready Claude architecture challenge and Gemini security/spec challenge for the RevDev publication state machine. Ask for concrete counterexamples, exact source evidence and unsafe transitions. Do not close OD decisions.
3. Audit PocketCode EVAL-06 fairness in the existing fixed-task worksheet. Fix only real gaps in that existing doc.
4. Audit the receipt/sourceability matrix against actual evidence sources. Separate mandatory, optional, unavailable and derived fields.
5. Reconcile RevDev candidate state machine and Happy Agent at-least-once semantics against exact P8U JSON and OD register. Do not alter canonical acceptance or owner decisions.
6. Prepare concise PC-return read-only inventory/checklist. Do not run it now.
7. Continue narrow source research only where it changes a decision. Avoid broad repeated competitor catalogues.
8. Update GitHub continuity with exact blob/commit SHAs and read-back.

Be proactive and thorough, but conservative with claims. Distinguish source-inspected, test-inspected, test-run, integration-proven and owner-approved. Do more useful work per pass. If an owner-only decision or authorization is necessary, ask briefly at the end. Start by verifying current GitHub state, then execute task 2 and task 3 rather than merely describing them.

---

## 13. Handoff maintenance rule

When the next chat materially advances the work, update this primary handoff and the RevDev companion handoff on their existing research branches, preserve prior history, and read both back. Do not generate a new handoff every few turns. A new handoff is warranted only when the chat is genuinely long or the project reaches a meaningful transfer point.


## 14. Continuation update — 2026-11-05 (post-handoff work)

### GitHub state refreshed

The live research branch refs and comparisons were re-fetched after the work below. Snapshot immediately before this handoff refresh commit:
- PocketCode branch `pocketcode-ai-workflow-director-research-2026-10-28`: HEAD `b616510ae5a9062f56c6208d2b30cdec231db9c7`; ahead 657 / behind 0 from `main`; merge base `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- RevDev branch `review/revdev-adaptive-ai-workshare-2026-10-27`: HEAD `0d18b232935dd53a462446d513b562c01f8a02ac`; ahead 563 / behind 0 from `main`; merge base `058f9025319d12e76195659c715ccb4afce133b8`.

The previous §4 snapshot (PocketCode e382… / 650 ahead; RevDev 9dea… / 555 ahead) was stale by five commits per branch. These counts are branch divergence, not quality or merge-readiness signals. Re-fetch before consequential work.

Protected PRs were re-fetched through GitHub's pull-request API:
- PocketCode PR #2: OPEN / DRAFT / UNMERGED; head `chat-continuity-report-regressions-2026-10-26` at `eb8b7ea83cb0e8fe1880351276c485b761431791`, base `main`.
- PocketCode PR #3: OPEN / DRAFT / UNMERGED; head `pocketcode-pass0-audit-2026-10-26` at `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`, base `main`.
- RevDev PR #1: OPEN / DRAFT / UNMERGED; head `continuity/relayref-handoff-2026-10-27` at `59f88dc0bd884872cf379c8aeb6272c9a70c71ce`, base `main`.

No protected PR was modified, reviewed, approved, retargeted, merged or closed.

### Completed documentation-only passes and read-back

1. **EVAL-06 fairness audit** appended to `AI_COLLAB/AI_WORKFLOW_DIRECTOR_EVALUATION_KIT_20261028.md`; blob SHA `a0047790b93c8a1502271536831481f209f30220`. It defines the estimand as the complete hand-authored Director prompt bundle versus baseline, adds EVAL-06-specific scoring anchors, cross-chat memory/personalization parity, order/blinding controls, confound handling and ceiling/sample-size limits. It explicitly distinguishes EVAL-06 from the separate CSV-to-JSON product-path worksheet. EVAL-06 remains NOT RUN.
2. **Mobile receipt sourceability classification** appended to `RESEARCH/MOBILE_RUNNER_EVIDENCE_SOURCEABILITY_MATRIX_20261105.md`; blob SHA `73cecc15eac55f27ad4ff26f6ddfc59565860176`. It separates mandatory representation from conditional/optional/unavailable/derived facts and maps each receipt concept to its authority. It also records the gap between receipt evidence and durable history/publication proof.
3. **RevDev P8U/OD reconciliation audit** appended to `resume/revdev/P8U_PUBLICATION_OPERATION_STATE_MACHINE_AND_FAULT_INJECTION_PLAN_2026-11-05.md`; blob SHA `c5d33f2cf9366f00a4ec326f711d00fb2da1c05a`. It maps P8U-01…12 and OD-01…08 without changing canonical JSON, IDs or owner choices. It identifies unresolved send-boundary/OD-03, no-runner-start/OD-06, fallback dependency/OD-07, audio layer/OD-08, log-flood metric/OD-05, and CAS/writer-topology proof gaps.
4. **Claude/Gemini review packet refinement** appended to `resume/revdev/THREE_AI_REVIEW_PACKET_DURABLE_PUBLISHER_AND_ORCHESTRATION_2026-11-05.md`; blob SHA `cf18bb3fd98eb793b13cab253fa0dcdf6e33b362`. The overlay focuses both reviewers on the exact publication state machine, with distinct architecture and adversarial security tasks and required evidence format. READY TO SEND; no reviewer response received.
5. **PC-return read-only inspection plan** created at `resume/revdev/PC_RETURN_READ_ONLY_INSPECTION_PLAN_2026-11-05.md`; blob SHA `c95e4f9092515db99291ec7eee5ae2f8eb171758`. It covers source/installed parity, writer topology, queue/result identity, safe GitHub GET-only observation, stop conditions and prohibited mutations. It is NOT EXECUTED and is not an authorization to inspect the PC.

Every file above was fetched again after the write; the appended sections and expected content were present. The SHA values are blob IDs, not test evidence.

### Reconciled evidence and non-actions

- EVAL-06 fairness is suitable only for an exploratory comparison of the complete hand-authored prompt bundle. It cannot isolate profile effects or prove a future PocketCode implementation. Ceiling performance is plausible; if baseline and Director tie, report no demonstrated bundle advantage.
- Receipt sourceability remains design-only. No mobile runner is selected; no iOS/Android/browser/hosted receipt was produced or tested. An unavailable process/exit/termination fact must remain unavailable/unknown, not be inferred from a UI or HTTP response.
- RevDev state machine remains design-only. P8U-01…12 and P0-D 1–10 remain NOT RUN; P0 remains OPEN/release-blocking; OD-01…08 remain OPEN. Happy Agent's at-least-once queue remains unsuitable as an immutable result archive.
- No source/test changes or test execution, no provider workload, PC inspection, mission replay, queue/host/API/sink mutation, install/restart, GitHub Actions, deployment or release occurred.

The next work should be to forward the focused review packet to Claude and Gemini, then reconcile their actual responses against the unchanged P8U JSON and OD register. Do not repeat broad competitor discovery.


## 15. Follow-on tightening pass — 2026-11-05

After the previous continuation update, the exact EVAL-06 manual run sheet and human-authored reference fixture were fetched and cross-checked against the new fairness audit. The existing EVAL-06 task is specifically compact-checkpoint continuation, not the separate CSV-to-JSON fixed-task execution-path worksheet. Its exact supplied facts are: input rows already validated; decision to export UTF-8 with header; escaping/quoting and large-file behavior unchecked; next step is define acceptance checks before editing. The Balanced Director prompt adds only the assigned profile instruction plus the run sheet's portable behavior rules and compact report headings.

The evaluation kit received §9.5, cross-checking the run sheet/reference fixture. It now explicitly says to save both raw answers before consulting the human reference, keep the hidden scoring checklist out of both chats, preserve canonical scoring over any new anchor interpretation, record memory/project/custom-instruction parity as SAME/DIFFERENT/UNKNOWN, and retain confounded/interrupted pair counts without pooling incomparable results. New blob SHA: `ec408b648727f362f51b15fc3a19bd327dfbb568`. EVAL-06 remains DESIGNED / NOT RUN.

No user experiment was run. No additional account, provider spend or quota workaround was used.
## Follow-on source research — 2026-11-05

The latest code-level reuse review now includes a source-pinned pass over Pyodide, CodeMirror 6, mini-SWE-agent and Plandex:
- `RESEARCH/CODE_LEVEL_OPEN_SOURCE_REUSE_REVIEW_20261105.md`, blob `a7eb9692b748815c3f2ad16f8663c3dd727ae23b`.
- Pyodide main commit `620c16a62d51be6613cb2208b563b2cf6f9f65d0`: worker execution example and SharedArrayBuffer interrupt mechanism. Interrupt requested is not proof of process/worker termination; deployment requires cross-origin isolation headers.
- CodeMirror state commit `9c801279cb83011e6f92af778f4443406e8f1200`: immutable EditorState transactions and JSON serialization. Good editor dependency candidate if CodeMirror is selected, not a project/run journal.
- mini-SWE-agent commit `04d809ceab9df28f9adaed044884180159172930`: bounded step/cost/wall-clock loop and deterministic fake-model tests. Its direct-shell environment is not a sandbox and its trajectory save is not an atomic durable journal.
- Plandex commit `e2d772072efadbe41d2946d97d79be55532dbab5` (last main commit observed 2025-10-03): reviewable diff and structured edit fixtures are useful, but its inspected apply/rollback implementation is not crash-atomic or safe to copy.
- No additional upstream code was copied. The existing isolated MCP polling helper remains the only research-only extraction. No product source/test was changed.

Current PocketCode research branch head after this work: `95d75bd2954aada7bef57d2d01a83fc05e21370b`. Research branch remains 660 ahead / 0 behind main at the pre-write comparison snapshot; re-fetch before further work. PR #2/#3 remain open draft unmerged and untouched.




## 2026-11-05 continuation: focused remote-agent and workflow-protocol research

Added `RESEARCH/REMOTE_AGENT_CONTROL_PLANE_AND_WORKFLOW_PROTOCOL_RESEARCH_20261105.md` (commit `dfe5c0bae5169bfc6623adc8b211ff56dc355795`). This is a narrow source-level update to the earlier competitor research, not a new product direction.

Findings:
- Happier is a strong mobile/multi-agent control-plane competitor: unified session inbox, provider adapters, attach/resume, cross-agent delegation, approval and structured question flows, native/replay fork choice, and encrypted multi-device sync. It still needs a running host. Its source explicitly reports partial commit when two canonical writers cannot share a transaction.
- Cretli demonstrates phone terminal/chat/files/Git/browser/workspace breadth and has useful delegation/mailbox/worker patterns. Its own security policy says a reachable terminal grants arbitrary shell as the host user; Plan mode is not a sandbox for all harnesses. Its JSON atomic rename is last-writer-wins across processes and its promise lock is process-local.
- agent-device is a MIT-licensed CLI/MCP/typed Node API for cross-platform UI/device automation, accessibility snapshots and evidence capture. Optional QA adapter only, not a runner or sandbox.
- OpenWOP contributes request/effect idempotency separation, stable effect identity, typed interrupts, event/replay semantics and witness-based conformance. Its known-limits page says no tier-3 independent host profile certification and no multi-instance/multi-region durability witness.

Decision: keep PocketCode's core run/inspect/report/iterate hypothesis. Do not pivot into a generic remote control room; remote-host control remains optional and cannot solve no-host execution. Keep AI Workflow Director secondary. No code copied because each candidate is either a large monorepo, runtime-specific, or a separate QA tool. Do not add dependencies or provider costs.

No production runner/provider/cloud/sandbox selected; $0 default budget remains. Fixed-task product comparison and AWD evaluation remain NOT RUN. LOOP/CASE unchanged. No app installed, user code run, device test run, provider workload or spend. PR #2/#3 remain untouched. See the research document for pinned source blobs, license evidence, security caveats and prioritized feature recommendations.

Follow-on security note: OpenWOP RFC 0229 source blob `d24e69b086f409a8019a5e644a394efc0ec1ec0b0` records a concrete secret-in-persisted-digest oracle. PocketCode must exclude secret values from durable fingerprints, caches, receipts and AI debugging packets before hashing/serialization. Its own RFC history records provisional acceptance and a steward override of the comment-window rule; do not equate Accepted status with independent security assurance. The PocketCode research note was updated to blob `bdc17692e25e9938bbca94d6b8be1ab0613dc196`.
## Workspace durability and browser storage research — 2026-11-05

The source-level reuse review was extended with SQLite-backed recovery and OPFS:
- PocketCode source review blob: `7bb2f46619377ca7d84a451ddcdbe23d4154d336`.
- Official SQLite Wasm: `sqlite/sqlite-wasm` main commit `ccbb81134a3b5a824f8a3cc3c5d8edd6e799ab5a`, package `3.54.1-build1`, Apache-2.0 wrapper. Dedicated worker demo uses OPFS SAH Pool VFS and reopens the DB to verify persistence. SAH Pool is single-owner/no simultaneous instance; OPFS VFS alternatives have COOP/COEP and Safari <17 caveats; WAL on OPFS has exclusive-lock constraints.
- `opfs-vfs/opfs-vfs` has excellent WAL/crash/fault test patterns but package `2.1.0` is PolyForm Noncommercial 1.0.0. Do NOT adopt/copy its code for the commercial product direction.
- `tgbender/safe-fs-ops` main commit `d52afaaec4f6050bd2ac70219ac8bbd7bc9d652e`, MIT, alpha, Python 3.12/SQLAlchemy. It has SHA-256 content objects, explicit backup manifests, partial-artifact checkpoints, SQLite journal/idempotency, fenced leases, append-only recovery actions and proof-based restore. Best architecture reference, not a mobile dependency.
- `openclaw/fs-safe` MIT Node >=22 offers root-bounded paths, symlink/hardlink defenses and atomic writes, but native bindings/Node filesystem assumptions make it unsuitable for browser/mobile until the runtime is confirmed.
- Proposed only: if browser/PWA runtime is selected, evaluate SQLite Wasm + OPFS for metadata/journal and content-addressed OPFS blobs with a single writer and mandatory export/backup. OPFS is origin-private, quota/eviction prone and deleted with site data. No runtime/framework choice or acceptance ID changed.
- No dependency installed or code copied. No product code/tests changed.

PocketCode research commit: `b045710958d6ea1631add4bfac18b96160212a68`.

### SQLite durability nuance added

A final source check corrected a possible over-inference: safe-fs-ops' SqliteEngineConfig dataclass says NORMAL by default, but SqliteStore passes synchronous=None when constructing the engine, so the helper does not set that pragma on its standard path. Effective runtime PRAGMA synchronous must be queried, not inferred from the dataclass. SQLite WAL + NORMAL may lose a recent commit on power loss; WAL + FULL adds a sync per commit. PocketCode's future storage layer must expose effective journal/sync mode and distinguish app-crash recovery from power-loss durability. Source review blob now `0a30f35e0eed6a1dd48325ebe40d2ad9a55c5260`.
## Workspace checkpoint contract pass — 2026-11-05

Extended `RESEARCH/CLINE_WORKSPACE_CHECKPOINT_AND_RESTORE_AUDIT_20261105.md` with §8, a backend-neutral checkpoint storage contract. Latest blob SHA: `5260729e4af0bd8ef9fe0f09dc9fc0a5825e49aa`.

The contract reconciles Cline's Git checkpoint/restore safeguards with safe-fs-ops' immutable content objects, durable journal, per-action recovery and fencing patterns. It defines distinct workspace/checkpoint/capture/restore identities; explicit capture coverage and COMPLETE/PARTIAL/FAILED/UNKNOWN semantics; blob-before-manifest publication ordering; restore preflight and conflict detection; mandatory complete pre-restore capture; per-action journal and crash reconciliation; backend-specific Git/blob/OPFS constraints; and proposed fault-injection tests.

Decisions:
- P1 user-visible checkpoint/diff/selective restore feature.
- P0 safety precondition before unattended destructive multi-file repair: verified COMPLETE preimage or explicit user confirmation.
- No runtime, storage backend, schema or implementation selected. No code/tests changed or run.
- Canonical LOOP-01..14, CASE-01..16 and D-01..D-08 unchanged.
- The design does not replace execution receipts, dispatch reservations, artifact release, or RevDev's remote publisher journal.
## Mobile process-death and reconnect research — 2026-11-05

Added §9 to `RESEARCH/CLINE_WORKSPACE_CHECKPOINT_AND_RESTORE_AUDIT_20261105.md`. Latest blob SHA `68a0077b0cc9b587fec9481094fa3613839c9247`. It records a pinned Happy Coder source audit at commit `7e32e09454c26aa78e86df0d378b1e49375b743d` (MIT), iOS/Android source and test paths, Apple/Android background execution constraints, a command/remote-execution/local-runner/observation-sync/result/checkpoint separation, fault-injection proposals, and staged P0/P1/P2 implementation gates.

Executive decisions:
- Do not promise arbitrary local coding-agent work continues in background or after process death.
- Remote host owns long-running execution where selected; phone owns durable command intent, local drafts, credentials and observation/reconciliation.
- Use a durable outbox with stable command ID and immutable payload. Ambiguous dispatch acknowledgement becomes DISPATCH_UNKNOWN and is reconciled by the same ID, never blind-resubmitted.
- Commit event rows and event cursor atomically. Sequence gaps require replay/reconciliation.
- Happy's native Swift/Kotlin code is not a drop-in dependency. Reuse protocol patterns and test cases; no code copied, dependencies installed, or upstream tests run.
- Do not transplant its generic retry behavior to non-idempotent shell/file/code execution.
- Existing canonical LOOP-01..14, CASE-01..16 and D-01..D-08 unchanged. Runtime/backend remain unselected.
Additional Happy source-review caveat: its iOS IntentOutbox uses best-effort storage removal/update calls (try?) and updates its in-memory projection. If durable acknowledgement deletion fails after remote success, a stale row may be retried after relaunch. Idempotent endpoints can tolerate this; arbitrary execution commands cannot. PocketCode should persist and verify an acknowledgement/tombstone before declaring a command durably consumed; otherwise retain DISPATCH_UNKNOWN and reconcile with the original command ID. This is a source-level inference, not a reproduced upstream failure.

## Mobile interruption recovery and native sync research — 2026-11-05

Added `RESEARCH/MOBILE_INTERRUPTION_RECOVERY_AND_OPEN_SOURCE_SYNC_AUDIT_20261105.md`, latest blob `5798d090a078c653712b6eeffe7ac58351d745b6`.

Current official platform findings:
- iOS `beginBackgroundTask` is a short finite extension, not a durable compute host. `BGProcessingTask` is interruptible and device-idle only. Background URLSession can keep file-backed HTTP(S) transfers alive across ordinary system suspension/termination, but user force-quit cancels transfers and blocks automatic relaunch until the user opens the app.
- Android WorkManager persists eligible work across app restart/reboot but is not an immediate/unlimited compute guarantee. Android 16 applies job quotas to long-running workers that use foreground services. UIDT is for user-initiated data transfer, not arbitrary code execution.
- Expo BackgroundTask wraps WorkManager/BGTaskScheduler for deferrable sync. It is not an execution runtime; TaskManager work must be globally registered and is not available on web.

Competitor sources inspected at code level:
- Happy Coder native iOS/Android, MIT, reviewed main `7e32e09454c26aa78e86df0d378b1e49375b743d`: SQLite snapshot+cursor, durable message/action outbox, stable IDs, exact acknowledgements, disk-first UI, foreground/reconnect catch-up, per-session locks. iOS and Android source blobs and test SHAs are pinned in the research doc.
- Critical Happy caveats: its generic intent queue coalesces set-like actions and must not be used for immutable run/command/attempt/evidence; selected storage errors are swallowed by `try?` in iOS IntentOutbox, so PocketCode must not copy this aspect. An outbox is transport state, not immutable evidence archive. At-least-once retries need receiver idempotency.
- OpenHands Mobile MIT, reviewed commit `47f815b1d111b6a71b405dcb77acb3682da59b85`: good REST-history/WebSocket/version-handshake and host/direct separation patterns, but the inspected React hook reuses an initial timestamp anchor and has no durable outbox/cursor. The retry counter resets on socket open, making immediate-close reconnect churn a source-level risk hypothesis, not a reproduced defect.

Executive decision: durable intent + authoritative execution + resumable observation. Separate phone lifecycle, transport lifecycle and runner lifecycle. Persist request+outbox before dispatch; on ambiguous ack reconcile same ID rather than blind redispatch. Apply each event projection and cursor in one transaction; cursor gaps require snapshot catch-up; terminal receipts stay outside bounded event logs. Phone background APIs are for transfer/sync only, not untrusted code execution. Distinguish “Reconnect to this run” from “Run again”.

No upstream code was copied because PocketCode still has no selected client stack and no application source tree. Happy's native code is not drop-in; OpenHands' hook is not durable enough. The design and tests are adopted as a compatibility-neutral contract, with code adaptation conditional on stack selection. $0 budget, no provider/run/device test, no product code/test edit. Canonical LOOP/CASE/AWD/D unchanged; PR #2/#3 untouched.

### Mobile recovery source audit and three-AI review packet — 2026-11-05

The mobile interruption research report was extended with §10 acceptance traceability. Latest report blob: `4e8cfafb4563f7e8948e73ec10b4d519e51e27ff`. The mapping uses existing LOOP/CASE only; no new IDs. In particular, mobile app background expiration is NOT CASE-04 timeout; a Cancel tap is NOT CASE-05 termination; a socket reconnect is not CASE-11 recovery until the same run is read back; and transfer success is not LOOP-03 PASS.

Created `AI_COLLAB/MOBILE_INTERRUPTION_RECOVERY_REVIEW_PACKET_20261105.md`, blob in initial create commit `77c2b2744d81f14d5df0be5005cb8ecc54864aa3`. It is READY TO SEND to Claude and Gemini, reviews not received. It asks Claude for lifecycle/architecture/crash-window review and Gemini for adversarial identity/idempotency/cursor/storage/OS security review. No implementation authority is implied.

Latest PocketCode branch HEAD at this update: `77c2b2744d81f14d5df0be5005cb8ecc54864aa3`. Review the two mobile research artifacts before implementation planning. No product code/tests or canonical acceptance changed.


## 2026-11-05 continuation: Cline/OpenHands source audit and programme status

Read [RESEARCH/REMOTE_EXECUTION_EVENT_RECOVERY_AND_SCHEDULER_COMPETITOR_AUDIT_20261105.md](../RESEARCH/REMOTE_EXECUTION_EVENT_RECOVERY_AND_SCHEDULER_COMPETITOR_AUDIT_20261105.md) before further architecture work. It pins Cline main commit d3ecc4890e8f9bcb77182b96c77fa90575e8e145 (Apache-2.0) and OpenHands software-agent-sdk main commit 7dab3f2f461ffc848d5fab7036badc552a385f43 (MIT), with exact file/test blob SHAs.

Key additions:
- Cline remote environment service is a useful future SSH adapter reference: profile and connection lifecycle, remote inspection, bounded command/transfer/tunnel timeouts, output cap and cleanup tracking. It is Node/desktop oriented and does not establish mobile support, sandboxing, safe egress or remote process termination.
- Cline SQLite scheduler is a useful bounded-work claim/lease reference for RevDev scheduling: durable run identity, claim tokens, renewal, stale-worker rejection, concurrency and tests. SQLite local claims are not distributed coordination; lease expiry does not make external side effects exactly-once. Its headless auto-approval defaults must not be copied.
- OpenHands supports same-ID create retry only when server advertises idempotent_conversation_create_v1. Its test covers server commit followed by dropped acknowledgement. This is a conversation-create guarantee, not command idempotency. PocketCode needs its own explicit command dedupe/query capabilities.
- OpenHands event store has useful stable IDs/sequences/cursors but bridges missing ancestry in some paths and has a test expecting storage listing errors to appear as an empty log. Do not copy either behavior into authoritative PocketCode or RevDev evidence. Empty, unavailable, corrupt and partial are distinct states.
- No code was copied; upstream tests were inspected, not run.

### Current programme assessment (planning estimate, not a test result)

**Overall dependable combined product progression: approximately 20%.** This is a qualitative estimate of the product journey, not code completion. Requirements, acceptance semantics, source research and risk analysis are ahead of implementation, integration and hands-on validation.

PocketCode: static/simulated UI prototype and extensive design/acceptance/research baseline exist. No real execution backend, selected execution path, mobile runner integration, durable real receipt or demonstrated end-to-end run/inspect/report/correct/re-run loop exists. A usable MVP is not close yet. The next meaningful milestone is one real, bounded vertical slice, not more feature breadth.

RevDev: historical Windows product/source exists, but current PC checkout, installed binary, runtime, publisher parity, queue and writer topology are UNKNOWN. P0 publisher recovery remains OPEN/release-blocking; P8U-01…12 and P0-D 1…10 remain NOT RUN; OD-01…08 remain OPEN. No implementation claim can be made from the research branch.

Progress is smooth in research and contract clarification, but not in executable product delivery. The current bottleneck is intentional: no reliable PC access, no selected PocketCode execution path, and no current RevDev host inventory. Reduce scope creep by stopping broad competitor catalogues and prioritize the first end-to-end proof when the relevant environment is available.

### Fresh GitHub verification on 2026-11-05

- PocketCode research branch head before this handoff refresh: 0cea0c183ef8d6649f7266b21d1952afa04981d5; compare against main: 684 ahead / 0 behind; merge base 555840d8d83342513d9cd353d4d1522d46a5c82d.
- RevDev research branch head before its paired update: a73337083d07462086d8b5c008f305a3e9e259f5; compare against main: 648 ahead / 0 behind; merge base 058f9025319d12e76195659c715ccb4afce133b8.
- PocketCode PR #2 and #3 remain OPEN / DRAFT / UNMERGED; RevDev PR #1 remains OPEN / DRAFT / UNMERGED. All are protected and untouched.
- Ahead counts reflect accumulated research-branch history, not functional feature completion. Re-fetch before future consequential work.

### Immediate next work order

1. Stop adding broad competitor lists. Investigate only implementation gaps that could alter the chosen first slice.
2. Prepare the existing fixed-task execution-path comparison and make the path decision only with explicit cost/security/availability evidence.
3. Define the minimum command capability contract: stable command ID, same-ID dedupe, status lookup, ordered event replay, cancel semantics, termination confirmation and artifact transfer.
4. After an execution path is selected, prove project/input -> explicit authorization -> real execution -> output/exit provenance -> artifact integrity -> durable receipt -> AI handoff -> reviewed correction -> linked rerun.
5. Keep LOOP/CASE/D IDs unchanged. No provider, host, app installation, test, source change, PR update, Actions or spend without the required authorization.


## 2026-11-05 source-level remote-agent recovery follow-up

A focused implementation pass inspected live upstream OpenHands and Cline source rather than relying on feature pages. The durable decision record is:
- [Remote agent control-plane and workflow-protocol research](../RESEARCH/REMOTE_AGENT_CONTROL_PLANE_AND_WORKFLOW_PROTOCOL_RESEARCH_20261105.md)
- [OpenHands isolated reference-copy README](../RESEARCH/vendor/openhands/README.md)
- [OpenHands idempotent-create retry helper](../RESEARCH/vendor/openhands/idempotent_create_retry.ts)

### Pinned source findings

**OpenHands** — current main inspected at `e6c074fe5fd96c6ce0f7a52905d529e27d24bb7b`, MIT.
- TypeScript `ConversationClient.createConversation()` retries an opaque transport failure only when the caller supplied a stable conversation ID and the server advertises `idempotent_conversation_create_v1`; HTTP responses, missing IDs and failed capability probes do not retry.
- Its regression tests model server commit followed by dropped acknowledgement, plus no-capability, missing-ID and HTTP-400 cases. Tests inspected, NOT RUN in this continuation.
- EventLog uses stable durable sequence cursors; session socket buffers history/live overlap and disconnects slow consumers rather than silently dropping durable frames; ConversationLease uses owner/generation/expiry and guarded writes.
- The local FileStore lock explicitly does not guarantee correct locking on NFS/network filesystems. The reviewed EventLog source does not prove universal fsync/power-loss durability.

**Cline** — current main inspected at `d3ecc4890e8f9bcb77182b96c77fa90575e8e145`, Apache-2.0.
- SSH remote environment stages a content-hashed helper, binds the remote Hub to loopback, uses strict SSH host-key checking and a local tunnel, and persists failed cleanup for retry. The shipped helper targets are Linux/macOS x64/arm64 and the implementation uses Node/process/filesystem APIs; this is not a ready-made mobile or Windows adapter.
- Its scheduler performs claim/capacity checks inside SQLite write transactions, uses per-claim tokens and lease renewal, and transactionally accepts events plus schedule-run fan-out.
- It persists terminal run status before writing its derived Markdown report. A report write failure is logged and does not replay a completed agent turn.
- The claim token fences scheduler rows, not arbitrary shell/network/filesystem effects; abort is cooperative. The reviewed path does not prove idempotent remote session-start after a lost acknowledgement.
- Security rejection: Cline's headless cron `buildToolPolicies` defaults to wildcard auto-approval when a schedule omits its tool list. Do NOT copy this behavior. PocketCode remains default-deny with explicit bounded tools/capabilities and policy revision binding.

**Protocols**
- ACP v2 session resume is a context/history reconnect with optional replay cursor and a required current-state snapshot. It does not create a stable execution-command idempotency guarantee. Its cancellation covers foreground work; background work may continue.
- MCP Tasks supplies a durable task handle and polling/result retrieval, but cancellation is cooperative and its empty acknowledgement is not termination proof.
- Keep protocol sessions, command identity, remote execution identity, attempts, event cursors and result receipts separate.

### Isolated code copy

Added `RESEARCH/vendor/openhands/idempotent_create_retry.ts`, an attributed, MIT-compatible small adaptation of OpenHands' capability-gated create retry decision. It takes an already serialized immutable request string plus a stable operation ID, only retries once for a transport-only failure after a capability probe succeeds, and resends the identical string and ID. The full MIT license was already present in the folder; README provenance has been updated.

This is a research reference only. It is not imported by product code, was not compiled or tested in this continuation, and is unsafe unless the exact target/auth scope implements durable same-ID deduplication and same-ID/different-body conflict detection. It does not provide an outbox, result reconciliation or exactly-once side effects.

### Decisions and status

- PocketCode transport-neutral direction now explicitly separates CommandId, DispatchAttemptId, ExecutionId, ordered ObservationId/sequence, result receipt and artifact release.
- A lost acknowledgement after a possibly accepted dispatch becomes `DISPATCH_UNKNOWN`; query the same ID; retry exact bytes only after negotiated idempotency. Never mint a new ID or silently replay a side-effecting command.
- Reconnect through durable event cursor + history/live overlap reconciliation; treat a stream overflow as disconnect, not permission to drop durable events.
- Cancellation request/acknowledgement/observed termination/result are distinct facts.
- This work does not select ACP, MCP Tasks, OpenHands, Cline, SSH, Pyodide, a cloud runtime, or an execution provider as PocketCode's product stack.
- LOOP-01…14 and CASE-01…16 unchanged; D-01…D-08 remain open. Fixed-task comparison and EVAL-06 remain NOT RUN.
- No product source/tests, integration, build, upstream test, device test, provider workload, credential, host, queue, workflow, deployment, or protected PR action occurred.

The source-level recommendations are not implementation evidence. Re-pin these upstream commits before any later code adoption. The owner remains the authority for product/runtime decisions and restricted actions.


### Final GitHub verification correction — 2026-11-05

The earlier branch snapshot in this handoff is superseded. Immediately before this correction, PocketCode branch head was 27a89fbed6a5b1c4d3a44e5398026fc220f918d6 and RevDev branch head was 9c5037625b27e2d35a5ee786964a34fe85f93e46. Live compare results: PocketCode 691 ahead / 0 behind main; RevDev 664 ahead / 0 behind main. Merge bases remain PocketCode 555840d8d83342513d9cd353d4d1522d46a5c82d and RevDev 058f9025319d12e76195659c715ccb4afce133b8. These are documentation/research branch commit counts only, not product progress.

PR state rechecked: PocketCode #2 and #3 OPEN / DRAFT / UNMERGED; RevDev #1 OPEN / DRAFT / UNMERGED. Their heads and metadata were not modified. The latest PocketCode competitor audit is read-back verified at blob 79be3b0c5e09c2c441465e18d82574a0360ea3a2; latest PocketCode status blob before this correction is f82fa983fdd28e9e5e184e5a4978ae0ae2926c80. Latest RevDev competitor audit blob 5bf366e529f78d5eb264db0d9094b2a1249b645f; current goals blob 1ad5109c72475a5fe4bacd90f7b4862d55ab2d32; review packet blob 8c36e593339fe99e5c626fb721e906f4c35c8819. Re-fetch live heads after this commit and before consequential work.


## 2026-11-05 latest executive checkpoint

Read [PROJECT_PROGRESS_AND_NEXT_EXECUTION_GATES_2026-11-05.md](PROJECT_PROGRESS_AND_NEXT_EXECUTION_GATES_2026-11-05.md) first. Current PocketCode estimate is approximately **20% toward a dependable MVP**, qualitative only. Static/simulated UI and extensive research exist, but no selected real execution backend, mobile runner integration, durable real receipt, or end-to-end run/inspect/report/correct/rerun proof. The first usable MVP is not close yet. Next priority is the existing fixed-task execution-path comparison, followed by one bounded vertical slice. Do not broaden features.

Fresh GitHub verification: branch 690 ahead / 0 behind main, observed head `27a89fbed6a5b1c4d3a44e5398026fc220f918d6`; PR #2/#3 OPEN / DRAFT / UNMERGED, untouched. The progress document is commit `843b4bab96d8d0f41141d2062bf3a6c5d484ba84`. Branch divergence is not implementation progress.


### Last live branch/PR check — 2026-11-05

Immediately before this entry, PocketCode research branch head was cdf80d50ae5732008caad44500579a3aa2736c51, 695 ahead / 0 behind main. RevDev research branch head was 6fc3b515d2b2bd65ba5fea7d414d087e6ad514c0, 669 ahead / 0 behind main. Merge bases remain 555840d8d83342513d9cd353d4d1522d46a5c82d and 058f9025319d12e76195659c715ccb4afce133b8 respectively. These are accumulated documentation/research histories only.

PR #2/#3 PocketCode and PR #1 RevDev were re-read: all OPEN / DRAFT / UNMERGED, bases main, original PR heads unchanged. No PR was modified.


### Upstream fault-test inspection addendum

The remote-agent audit was extended after inspecting targeted upstream test files:
- OpenHands session stream tests verify replay/live ordering, no duplicate durable frames, stable sequence across a lost event file, and slow-consumer disconnect.
- OpenHands lease tests verify takeover generation increments and stale-owner guarded writes fail.
- Cline SSH tests verify strict host-key checking, content-addressed helper bootstrap without network download, loopback-only tunnel, concurrent connection reuse, failure cleanup, and recovery of persisted cleanup after tunnel loss.
- Cline cron ingress tests inject partial fan-out/status failures, verify transaction rollback, reopen SQLite before redelivery, and ensure another connection cannot see partial acceptance.
- Cline runner tests verify work isolation/progress for a blocked schedule and explicitly assert wildcard auto-approval when the tool list is omitted. This is a tested unsafe default and is rejected by PocketCode.
- We did not find a targeted report-writer-failure regression in the inspected portions of Cline's runner tests. The source writes terminal state first, but that particular failure path is not treated as upstream-test-proven.

All source test files were inspected only. No upstream suite was run by PocketCode. Exact paths and blob SHAs are recorded in Section 10.10 of the linked [remote-agent audit](../RESEARCH/REMOTE_AGENT_CONTROL_PLANE_AND_WORKFLOW_PROTOCOL_RESEARCH_20261105.md).


### Last storage-boundary clarification

The deeper OpenHands read shows its LocalFileStore text writes use same-directory temp + file fsync + rename, but the helper does not fsync the parent directory. EventLog's event append precedes in-memory indexing, and its length-marker advance is best-effort. Its FileLock/flock is explicitly unreliable on NFS/network filesystems. Treat OpenHands as an event replay and ordering reference, not proof of portable power-loss or distributed-storage durability.

Cline's SQLite tests prove expiry reclaim with a new token and a sequential bun:sqlite capacity check, not a demonstrated multi-process claim race. Its separate event ingress tests do verify atomic fan-out visibility across a peer SQLite connection. These are different claims. See Sections 10.10–10.11 of the remote-agent audit for exact files and SHAs.
