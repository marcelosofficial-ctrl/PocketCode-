# New Chat Handoff: RevDev + PocketCode
Prepared: 2026-11-01. This is a continuation of the existing projects, not a fresh start.

## 1. Verified GitHub state at handoff

### PocketCode
Repository: https://github.com/marcelosofficial-ctrl/PocketCode-
Research/docs branch: pocketcode-execution-boundary-crosswalk-2026-11-01
Last verified HEAD: 8ce8b379f3a8323a2ef4e0aa5dccea3a1343a53e
Latest key documents:
- PROJECT_STATUS.md, blob b06380278aeb7797c1c2e29efe524ec0cfc834da. This is the accumulated history and should be read in full or searched for relevant sections.
- AI_COLLAB/SHARED_CONTRACT_GOLDEN_FIXTURE_CATALOGUE_20261101.md, blob 6b27791356ecf34d28e457030dd04a2b796cc6ca.
- AI_COLLAB/SHARED_CONTRACT_READINESS_AND_STATE_DOMAIN_CROSSWALK_20261101.md, blob 5d3fa6068f4979d404739cc5cedebd36452bea05.
- AI_COLLAB/REVDEV_POCKETCODE_ARCHITECTURE_CONVERGENCE_AND_GEMINI_RESEARCH_AUDIT_20261101.md, blob f6d76e0de6aecb8669eab3453966d863b1e21176.
- AI_COLLAB/END_TO_END_TRUST_CHAIN_GAP_MATRIX_20261101.md, blob 659913f33a238b24b9c1116575d242a2eb026c4a.
- AI_COLLAB/COORDINATOR_CRASH_WINDOW_AND_FENCING_AUDIT_20261101.md, blob 109465eecc9bd335541632d7a945a52a2aa85500.
- AI_COLLAB/CONSOLIDATED_LIFECYCLE_AND_REPORT_PATCH_SEQUENCE_20261101.md, blob 88c738421f921a8503b5042ab8a47bb5579b7af5.
- AI_COLLAB/POCKETCODE_EXECUTION_BOUNDARY_TRUST_CROSSWALK_20261101.md, blob 75968d42e90cc97e63223a970cadbcc0ddf188ce.
Re-fetch the current branch head before any work. These SHAs are handoff snapshots, not guarantees the branch has not moved.

### RevDev
Repository: https://github.com/marcelosofficial-ctrl/DevRelay-Missions
Last verified review branch: review/revdev-adaptive-ai-workshare-2026-10-27
Last verified HEAD: 6589ea90874a41ec4bce9d61ec003a05b73e89ad
Key handoff: resume/revdev/NEW_CHAT_HANDOFF_2026-10-29_REVDEV_POCKETCODE_CONVERGENCE.md, previously recorded blob 14e88707d34773ca156fe028735bfe2f0ec57e14. Re-fetch exact file and branch before relying on it.
Traceability supplement: resume/revdev/POCKETCODE_REVDEV_ACCEPTANCE_TRACEABILITY_SUPPLEMENT_2026-10-29.md.

### PocketCode PRs
- PR #2: https://github.com/marcelosofficial-ctrl/PocketCode-/pull/2, open, draft, unmerged. Chat checkpoints and report-contract regressions. Do not modify or merge without explicit authorization.
- PR #3: https://github.com/marcelosofficial-ctrl/PocketCode-/pull/3, open, draft, unmerged. Research baseline. Do not modify or merge without explicit authorization.
- Research branch remains separate. Do not merge it into PR #2/#3 or combine histories without explicit review and authorization.
- PR #3 explicitly records that the exact checked-in helper/test pair and full repository suite have NOT RUN. No provider, production security or runtime guarantees are validated.

## 2. Three-AI roles and Claude's upcoming report

- User is project owner and sets goals/constraints. User has delegated sensible administrative decisions to ChatGPT, not blanket permission for risky external actions.
- Claude is lead developer and primary implementation/architecture feasibility reviewer.
- Gemini is co-developer and independent security/spec/adversarial auditor.
- ChatGPT is continuity holder, evidence reconciler, test/acceptance architect, cross-project coordinator, and eventual deployment coordinator after explicit authorization and PC access.

A medium-sized Claude document containing substantial information is expected soon. It has NOT yet been received in this handoff. When it arrives, read it thoroughly, extract recommendations and evidence, compare it against Gemini and existing project goals, and record disagreements.

Critical: Do NOT let Claude's upcoming recommendations overwrite the project's goals, product direction or constraints merely because the report is newer or detailed. The recommendations are expected to be extremely valuable. Classify each as evidence-backed finding, architecture recommendation, optional alternative, open question, or unsupported/contradictory claim. Preserve project goals unless the user changes them or strong evidence justifies a correction. Explain trade-offs and propose amendments rather than silently replacing the plan.

## 3. Hard constraints and operating rules

- User is phone-only. PC/local access unavailable for approximately four months starting October 2026.
- Treat all PC source tree, installed binary, runtime, watcher, queue, publication, process, audio and host state as UNKNOWN until fresh PC evidence is provided. Historical paths/hashes are references only.
- Historical RevDev paths: source C:\Users\celo\source\repos\RevDev; runtime C:\Users\celo\DevRelay\automation\; installed binary %LOCALAPPDATA%\RevDev\app\RevDev.exe. Historical runtime files included watcher.ps1, queue-sync.ps1, mission-runner.ps1, DevRelay.Automation.psm1, launcher.ps1, project-manager.ps1. All current state UNKNOWN.
- Budget is $0. No paid provider, paid account, billing change, credits, cloud workload, live user-code/security workload or spending.
- No source/test implementation edits, workflow changes, Actions, queue mutation, mission replay, provider operation, account/credential creation, host mutation, install, restart, elevation, secrets, PR modification, merge, deployment or release unless explicitly authorized.
- Docs-only continuity updates on isolated research branch are permitted as previously authorized. Do not modify PR #2/#3 or default branch.
- Do not claim tests passed unless exact source/version/environment/results are evidenced. Pure helper/fake tests are not provider, persistence, Windows, iOS, HTTP, security or production proof.
- Preserve HOSTED_DENY and explicit authorization/guard semantics in RevDev. Parsed != policy-approved != authorized.
- Work in regular chat, not Work mode. Be efficient and thorough, do substantial work per pass, use GitHub as continuity store, minimize user requests, ask only essential questions.
- Do not address the user by name.

## 4. Goals and product direction

### Shared strategic direction
RevDev and PocketCode should converge toward one coherent PC-and-phone product/program while remaining distinct repositories, clients, execution adapters, authorization boundaries, persistence implementations, security policies and acceptance suites. The objective is not one universal runtime or weakening the stronger product's guarantees.

Likely reusable layer: language-neutral, versioned task/lifecycle/outcome/evidence/artifact/report contracts and fixtures. Keep coordinator, queue, execution engine, authorization, storage, provider integration, host controls and release gates product-specific unless evidence later justifies shared implementation.

### RevDev
Mission-driven Windows automation/orchestration and operator UI. Goals include reliable queueing/recovery/publication, project cards, recent/queued state, timer bubble, and non-flashing Queue Health. Reliability issues include multi-operation results, queue stalls, recovery without rerunning completed work, PowerShell 5.1 traps and AWAITING_CHAT_CONTINUATION. RevDev remains the authority over what executes on its Windows host. PocketCode may submit/direct work but must not bypass RevDev guards. P0 publisher/orphan/retry/recovery remains release-blocking. Work Coach is secondary to reliability P0.

### PocketCode
Phone-first AI coding/orchestration app for working with AI from anywhere. Original aspiration was running scripts on phone. Research reframed it toward an Agentic Orchestration Control Plane: local WASM/JSC for bounded/light tasks, remote SSH/Tailscale or cloud fallback for heavy work as future possibilities. No topology/provider/runner is approved. No system-wide overlays; accessory symbol bar; explicit paste-to-context only, no background clipboard polling. Must prove concrete advantage against ordinary AI chat, Pyodios, Carnets, browser Pyodide and remote execution. Fixed-task comparison is more valuable than feature creep. PocketCode naming collision with Catrobat's Pocket Code remains under investigation; no rename/legal conclusion.

## 5. Gemini open-source research and ChatGPT audit

Gemini supplied:
- “Comprehensive Open-Source Architecture and Technology Reuse Report for PocketCode and RevDev”
- A later “Master Research Strategy: Architecture, Code Reuse, and Platform Con...” response.

Candidate suggestions: Cline SDK/RuntimeHost separation; Aider repomap.py; River queue; MCP; DevPod SSH; isomorphic-git + LightningFS; Pyodide; nsjail/bubblewrap; OpenHands, Hatchet, Wasmtime and related references.

Current assessment in the architecture audit:
- Cline layering is a useful reference for agent loop/provider/host separation, not automatically a dependency or production-ready extraction.
- Aider repo map is worth testing only if repository navigation/context cost is a demonstrated bottleneck.
- River is a serious RevDev queue candidate, not selected. Source-level follow-up found its Go SQLite driver labels itself early testing with minimal real-world use, warns about SQLite single-operation concurrency/SQLITE_BUSY, suggests one-connection workaround and notes slower row-at-a-time completion/InsertMany versus Postgres. Root Go module uses separate riverpgxv5 driver. Do not call SQLite support production-ready.
- MCP is tool interoperability, not durable job orchestration or authorization.
- DevPod SSH is a remote-host pattern, not proof of phone-ready runtime.
- isomorphic-git/LightningFS is a candidate; LightningFS docs include crash-ordering/repository-corruption and CORS caveats.
- Pyodide is a bounded local experiment candidate; main-thread blocking, browser filesystem and memory behavior need direct device tests.
- nsjail/bubblewrap apply to remote Linux hosts, not iOS or Windows.
- Gemini's 9–14 month development-savings estimate is unsupported.
- Generic iOS memory thresholds, compressed-size claims, production-readiness claims, licensing generalizations and MCP-as-universal-architecture claims need source-level verification.
No candidate has been adopted. No dependency/provider/queue/runtime/database selection approved.

## 6. Cross-project contract conclusions

Read first:
1. AI_COLLAB/SHARED_CONTRACT_READINESS_AND_STATE_DOMAIN_CROSSWALK_20261101.md
2. AI_COLLAB/SHARED_CONTRACT_GOLDEN_FIXTURE_CATALOGUE_20261101.md
3. AI_COLLAB/REVDEV_POCKETCODE_ARCHITECTURE_CONVERGENCE_AND_GEMINI_RESEARCH_AUDIT_20261101.md
4. AI_COLLAB/END_TO_END_TRUST_CHAIN_GAP_MATRIX_20261101.md
5. AI_COLLAB/COORDINATOR_CRASH_WINDOW_AND_FENCING_AUDIT_20261101.md
6. AI_COLLAB/CONSOLIDATED_LIFECYCLE_AND_REPORT_PATCH_SEQUENCE_20261101.md
7. AI_COLLAB/POCKETCODE_EXECUTION_BOUNDARY_TRUST_CROSSWALK_20261101.md
8. PROJECT_STATUS.md

Do not flatten all state into one status field. Preserve distinct:
1. Execution outcome: what happened to work.
2. Coordination/job disposition: accepted, queued, dispatch uncertain, running, cancellation requested, reconciliation, retry, terminal.
3. Evidence capture/persistence: whether trusted required evidence was collected and durably retained.
4. Publication state: whether result/evidence/report was published and reconciled.
5. Release authorization: permission to disclose a specific immutable artifact to a principal under current policy.
6. Transfer/delivery: exact bytes transferred and client receipt/integrity verified.
7. User-facing verdict: derived from trusted execution evidence under product-specific acceptance policy, not authority for other axes.

Critical invariants:
- Execution PASS can coexist with publication PENDING_RETRY. Do not rerun execution merely because publication failed.
- Execution FAIL can coexist with publication PENDING_RETRY.
- Accepted/queued is not execution. Provider-start acknowledgement unknown is not proof of not-started or running.
- Cancellation request is not confirmed termination.
- Lease expiry does not prove an old worker/provider process stopped. Fencing rejects stale coordinator writes, but authentic late execution evidence still needs reconciliation.
- Same identity + same immutable content is idempotent; same identity + changed content/scope/policy/digest is conflict, never last-write-wins.
- Out-of-order completion remains bound to each attempt/result.
- Missing/contradictory terminal evidence cannot yield PASS.
- Runtime limit, collector truncation and report-display truncation are separate facts.
- Empty artifact list does not prove artifacts are not required. Trusted task definition must say NOT_REQUIRED.
- Evidence capture precedes destructive cleanup.
- Release authorization is not transfer start/completion. Server completion is not client-verified receipt without receipt/integrity evidence.
- Exact immutable result identity/hash is not mutable LATEST_RESULT pointer.
- Task/job/attempt/operation/event/evidence/artifact/release-decision/transfer identities have different scopes. Preserve native IDs and explicit mappings.

## 7. Shared golden fixture catalogue

SCF-001..018 are provisional semantic fixtures, not a frozen schema or executable fixture set:
1. Accepted, not started.
2. Dispatch intent committed, provider start acknowledgement unknown.
3. Duplicate request/event, same identity and content.
4. Same identity, conflicting content/metadata.
5. Execution PASS, publication pending retry.
6. Execution FAIL, publication pending retry.
7. Cancellation requested, execution still active.
8. Stale worker resumes after fencing takeover.
9. Out-of-order completion for distinct attempts.
10. Missing or contradictory terminal evidence.
11. Runtime limit vs collector truncation vs report display truncation.
12. Artifact-free success because artifacts are not required.
13. Cleanup attempted before durable evidence capture.
14. Release authorized, transfer not started.
15. Partial transfer/interrupted client delivery.
16. Report append acknowledgement lost.
17. Publication partially commits across stores.
18. Newer result advances latest pointer while older exact result is republished.

Catalogue maps scenarios conservatively to native tests/proof levels. Keep provisional until Claude and Gemini review it.

## 8. Acceptance suites stay distinct

PocketCode canonical LOOP-01..14 and CASE-01..16. AEC and AWC are additional distinct suites. Coordinator DR-*, COORD-* and proposed STALE-*, TOKEN-*, PUB-*, REL-*, LIFE-*, ADV-* are supplemental/proposed, not canonical replacements. Owner decisions D-01..D-08 remain open/blocked as recorded in PROJECT_STATUS.md. Do not silently decide them.

RevDev P8U-01..12, P0-D, RelayRef and native Windows/host acceptance remain distinct. P8U execution vocabulary: NOT_RUN/RUNNING/PASS/FAIL. Publication: NOT_ATTEMPTED/PENDING_RETRY/PUBLISHED/PERMANENT_ERROR. Remediation is separate. P8U spec is SPEC_ONLY_NOT_IMPLEMENTED; Windows/runtime acceptance not established. P8U-01: execution PASS remains PASS when publication pending; preserve exact local result identity/hash; do not execute again. P8U-08: older exact result publication must not regress LATEST_RESULT. P8U-09 no-local-terminal fallback has specific conditions. Gemini C# specs CS-SPEC-01..04 are proposed, not integrated. RelayRef v0.9 Python reference self-test 293/293 on Linux/Python 3.12.3, but C# NOT_RUN, Windows/product BLOCKED, golden v0.9 not regenerated.

Never claim shared fixture passes a canonical product acceptance just because scenarios are related.

## 9. Technical audit findings to preserve

- G-01: exact bool validation should cover limit_violated, output_truncated and contradictory_evidence; ordinary truthiness can suppress/fabricate conditions.
- Policy/fingerprint maps need recursive string-key validation and explicit JSON value schema; JSON key coercion can collapse malformed maps.
- G-07: Windows superscript device aliases COM¹/²/³ and LPT¹/²/³ may bypass ASCII-only reserved-name checks; test exact/extension/casing, not unrelated Unicode numerics.
- ReportHistory should reject whitespace-only job/evidence identifiers, preserving exact nonblank values unless normalization approved.
- Event reducer needs D-04 decisions for authenticated scope binding, immutable snapshots, top-level metadata, source namespace and sequence collision diagnostics. Mutable payload aliasing can alter accepted evidence.
- Redactor tests need configured maximum token length and beyond-max boundary. Redaction remains best-effort.
- Tombstone expiry needs trusted time and atomic semantics under D-08; caller-provided deleted_at is not trusted current time.
- Report formatter truncation metadata should be tri-state YES/NO/UNKNOWN. Separate runtime enforcement, collector truncation and display truncation.
- PR #2 formatter escapes controls/truncates but does not itself redact secrets or verify trust. No proven integration ensures every rendered field passed through trusted redactor/output collector.
- Output collection should use explicit states such as COMPLETE/PARTIAL/UNAVAILABLE/EMPTY/RUNTIME_LIMIT/DISPLAY_TRUNCATED with per-stream provenance.
- Cleanup must not destroy evidence before durable capture.
- See CONSOLIDATED_LIFECYCLE_AND_REPORT_PATCH_SEQUENCE_20261101.md. This is not authorization to change source/tests.

## 10. Priorities for the next chat

1. Refresh exact GitHub branch heads, project status, key docs and PR #2/#3 state.
2. Check whether Claude's promised medium-sized document has arrived in the current conversation or supplied files. If not, do not invent its contents.
3. When available, reconcile Claude's document against Gemini, the architecture audit and project goals. Classify recommendations, citations, confidence, implementation fit, cost, security boundary and disagreements. Preserve project goals unless evidence/user direction justifies change.
4. Ask Claude to review source-native feasibility/identity binding for SCF-001..018. Ask Gemini to red-team coverage, unsafe transitions and false acceptance equivalence.
5. Review fixture catalogue for internal contradictions and missing edge cases; do not change canonical acceptance IDs.
6. Resolve identity/state mapping and D-01..D-08 decisions before drafting schema. First create a field dictionary with required/optional/conditional/deferred status, source authority, trust boundary, unknown/null semantics, cardinality, size, retention, version and native mapping.
7. Continue fixed-task PocketCode local feasibility comparison. Pyodide 314.0.7 CSV/JSON foreground Safari task is a candidate only, not run.
8. Defer RevDev queue/host decisions until PC returns and fresh read-only source/runtime inventory is possible. River is a candidate only.
9. Make docs-only isolated-branch continuity updates when useful, verify created/updated files and exact branch head.

## 11. Explicit non-actions

No implementation/test file changed in the latest shared-contract pass. No schema/API/provider selected. No tests, Actions, provider calls, live workload, host operations, merge, deployment, billing or spend. PR #2/#3 were not modified. PC host/runtime/queue/publication/audio state remains UNKNOWN.

---

# COPY/PASTE BOOTSTRAP FOR THE NEXT CHAT

You are continuing the existing RevDev + PocketCode project. This is not a fresh project. Read this handoff and the linked GitHub documents before deciding what to do.

Roles: Claude is lead developer and a medium-sized research/architecture document with substantial information is expected soon. Gemini is co-developer and independent security/spec auditor. ChatGPT is continuity holder, evidence reconciler, acceptance/test architect and cross-project coordinator.

When Claude's report arrives, treat it as extremely valuable recommendations, but do NOT let it overwrite project goals, direction or constraints merely because it is newer or detailed. Compare it against Gemini, existing documents and evidence. Classify facts, recommendations, alternatives, open questions and unsupported claims. Preserve the goals unless the user changes them or strong evidence justifies an adjustment. Record disagreements and trade-offs.

Refresh exact GitHub state for PocketCode branch pocketcode-execution-boundary-crosswalk-2026-11-01, RevDev branch review/revdev-adaptive-ai-workshare-2026-10-27, and PocketCode PR #2/#3. Read PROJECT_STATUS.md and all shared-contract/research docs listed in this handoff.

Hard constraints: user is phone-only; PC unavailable for about four months from October 2026. All PC source, binary, runtime, watcher, queue, publication, process and audio state is UNKNOWN until fresh PC evidence. Budget $0. No paid provider/account/credits, billing, cloud or live security/user-code workload, Actions, source/test edits, queue mutation, mission replay, provider operation, PR modification, merge, deployment, release, install, restart, secrets or elevation without explicit authorization. Docs-only updates on isolated research branch are permitted. Do not modify PR #2/#3 or default branch.

Keep RevDev and PocketCode converging as one coherent product direction while preserving separate repos, clients, execution adapters, authorization, storage, security and acceptance suites. RevDev remains authority over execution on its Windows host; PocketCode must not bypass RevDev guards.

Never collapse execution outcome, coordination disposition, evidence persistence, publication, release authorization, transfer receipt and user-facing verdict into one status. Preserve product-native identities and canonical acceptance. PocketCode LOOP-01..14/CASE-01..16 and RevDev P8U-01..12/P0-D/RelayRef stay distinct. SCF-001..018 are provisional shared semantic fixtures, not canonical acceptance replacements.

First priorities: reconcile Claude/Gemini research; have both review SCF fixtures; resolve identity/state mapping and D-01..D-08 before any schema. Continue the fixed-task PocketCode local feasibility comparison; Pyodide 314.0.7 CSV/JSON foreground Safari test is a candidate, not run. RevDev queue/host decisions wait for PC access; River remains a candidate.

Work efficiently and thoroughly, make sensible administrative decisions within these boundaries, do substantial work per pass, update GitHub continuity when useful, verify every created/updated file and exact branch head, and ask the user only for essential missing information.


---

## 12. Continuation delta after the original 2026-11-01 handoff — refreshed follow-up

This section supplements the original handoff above. The original historical snapshot is preserved; the following is the later verified continuation state.

### 12.1 Refreshed repository and PR state

At the latest verification during this continuation:
- PocketCode research branch `pocketcode-execution-boundary-crosswalk-2026-11-01`: `66685aacfd3a5381455cdb7cbffaed10905b1bd5`.
- PocketCode `main`: `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- Compare: research branch 465 commits ahead, 0 behind. This is a documentation/research branch, not a merge target.
- PocketCode PR #2 remains open/draft/unmerged at `eb8b7ea83cb0e8fe1880351276c485b761431791`.
- PocketCode PR #3 remains open/draft/unmerged at `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`.
- RevDev review branch remains `6589ea90874a41ec4bce9d61ec003a05b73e89ad`; RevDev main remains `058f9025319d12e76195659c715ccb4afce133b8`.
- RevDev PR #1 remains open/draft/unmerged at `59f88dc0bd884872cf379c8aeb6272c9a70c71ce`.
- All three PRs remain untouched by this continuation.

Always refresh again before subsequent work; these are snapshots, not permanent branch guarantees.

### 12.2 New documentation added after the original handoff

1. `AI_COLLAB/SHARED_CONTRACT_GOLDEN_FIXTURE_CATALOGUE_CHATGPT_PRELIMINARY_REVIEW_20261101.md` — independent static review of SCF-001..018. Retains the 18 provisional IDs, identifies proof-precondition clarifications, preserves supplemental adversarial cases, and contains separate Claude/Gemini review instructions. Not owner-approved, not canonical acceptance, not schema freeze.
2. `AI_COLLAB/STATE_AND_IDENTITY_MAPPING_PREPARATION_20261101.md` — seven independent state axes, separate artifact expectation/operation records, identity-domain map, native suite namespace preservation and explicit D-01..D-08 stop rules. Not a schema or owner decision.
3. `AI_COLLAB/PYODIDE_314_0_7_MOBILE_RUNTIME_FEASIBILITY_REVIEW_20261101.md` — official-source desk review of the pinned browser-local candidate and LOC-01..24 refinements. Not device tested.
4. `AI_COLLAB/POCKETCODE_EXECUTION_BOUNDARY_TRUST_CROSSWALK_20261101.md` Section 11 now points to the existing canonical fixed-task worksheet instead of suggesting a competing CSV-cleaning task. Section 22 records the Pyodide 314.0.7 technical findings.
5. `PROJECT_STATUS.md` records these review/research deltas.

### 12.3 Fixed-task decision reinforced

The one canonical experiment remains the existing `PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md`: synthetic `items.csv` → real `summary.json`, Decimal-safe arithmetic, exact expected total 10.75 and malformed missing-`unit_price` failure. Do not replace it with a second CSV-to-CSV cleaning task. No hands-on comparison has occurred.

### 12.4 State and identity clarification

The current shared semantic preparation distinguishes seven independent state axes:
- execution outcome;
- coordination/job disposition;
- evidence persistence/integrity;
- publication;
- release authorization;
- transfer/delivery/receipt;
- derived user-facing verdict.

Artifact expectation remains a separate fact. Operation records for start, cancel, report append, publication, release and transfer remain distinct. Do not map RevDev MissionId/RunId, PocketCode runId, coordinator job/attempt, provider token, event, evidence, artifact, report, release-decision or transfer identifiers by name similarity.

Critical mapping rules:
- rejection before an attempt is request/admission disposition, not a fictitious process outcome;
- infrastructure failure without trusted child terminal evidence leaves execution outcome UNKNOWN;
- cancellation request/acknowledgement is not confirmed termination;
- PocketCode CASE-04's confirmed timeout remains INCOMPLETE / timed_out under the current canonical working default;
- RevDev P8U execution PASS/FAIL and publication NOT_ATTEMPTED/PENDING_RETRY/PUBLISHED/PERMANENT_ERROR remain RevDev-native;
- no shared fixture or schema replaces LOOP/CASE/AEC/AWC, COORD/DR, P8U/P0-D, RelayRef or other native acceptance namespaces.

### 12.5 Pyodide 314.0.7 official-source findings

- Version 314.0.7 is pinned; record exact runtime/assets rather than floating to latest/dev.
- It requires a module-type Web Worker; classic importScripts workers are unsupported.
- Documented cooperative KeyboardInterrupt requires Web Worker + SharedArrayBuffer + appropriate cross-origin-isolation headers. LOC-05 gates LOC-06.
- The current changelog lists maxMemoryBytes under Unreleased, not in 314.0.7. Do not assume a pinned-release hard WASM heap cap; no browser-process/OS resource guarantee follows.
- decimal.Decimal via C _decimal is available; _pydecimal is unavailable. threading, multiprocessing and sockets are nonfunctional.
- Safari path should use explicit file picker and Blob save/share; File System Access API is Chromium-only per Pyodide's official FAQ. Default MEMFS is lost on page reload.
- Worker.terminate is a host stop action only; it does not prove Python cleanup, output flush, exit status or terminal outcome.

The fixed task is still a narrow standard-library feasibility test, not a runtime selection or security acceptance. LOC-01..24 remain proposed and NOT RUN.

### 12.6 Claude report status

After the original handoff, the current PocketCode research branch tree and all eight listed PocketCode branches were refreshed/enumerated. A Claude-specific branch search returned no results. Repository commit search found the old `CLAUDE.md` entry-instructions commit, not the promised medium-sized research report. Therefore the report remains **NOT RECEIVED in the checked GitHub snapshot**. This does not establish whether Claude has prepared it elsewhere or whether it may arrive later.

Claude's dedicated SCF-001..018 implementation/identity review remains pending. Gemini's dedicated SCF-001..018 adversarial review remains pending. Gemini's existing architecture/open-source audit is not a substitute for that fixture-specific review.

### 12.7 Current next work

1. Receive and fully review Claude's medium-sized research document when supplied; classify evidence, recommendation, optional alternative, open question and unsupported claim. Compare against Gemini and existing goals; do not let recency/detail override the project direction.
2. Obtain Claude and Gemini's independent SCF reviews using the exact catalogue and review instructions. Reconcile disagreements.
3. Continue identity/state mapping and owner decision preparation without freezing schema. Lifecycle D-01..D-04 remain OPEN as recorded; D-05 remains BLOCKED; D-06..D-08 remain proposals requiring owner review and actual-boundary proof.
4. Continue the fixed-task phone feasibility plan. No install, device test, provider workload, account or spend unless explicitly authorized.
5. Keep RevDev PC host/queue decisions deferred until PC access returns and fresh read-only source/runtime evidence is possible.

### 12.8 Non-actions

All work after the original handoff was documentation-only on the isolated PocketCode research branch. No schema, canonical acceptance, source/test, PR #2/#3, main branch, provider/store, account, workflow, Actions, workload, billing, deployment, merge, PC host, runtime, watcher, queue or publication state was changed or exercised. No tests, provider integration or device execution occurred. RevDev PC state remains UNKNOWN.


## 13. Claude research master received and independently reconciled — 2026-11-01

Claude's complete "PocketCode + RevDev: Open-Source Research Master" was supplied in chat. The review is recorded in:
- [Independent reconciliation](CLAUDE_RESEARCH_MASTER_INDEPENDENT_RECONCILIATION_20261101.md)
- [Project status](../PROJECT_STATUS.md)

### 13.1 Main verdict

Treat Claude's report as a useful discovery and source-reading map, not as an approved adoption plan. Its P0 labels are recommendations, not owner decisions. No technology, dependency, runtime, storage design, protocol, sandbox, licence or product direction was adopted by this review.

### 13.2 Important primary-source checks

- Anthropic sandbox-runtime: Windows support is explicitly alpha. Current docs confirm Schannel-based HTTPS failures (PowerShell web requests, .NET HttpClient, NuGet, winget, etc.), persistent allowWrite ACL grants, cross-session read implications for kept roots, and stated WFP attribution gaps. Study only; no PC install/provisioning/elevation.
- MCP 2026-07-28: stateless core; Tasks is an optional `io.modelcontextprotocol/tasks` extension. It is not a durability, evidence, authorization or release guarantee. Use as a mapping vocabulary only.
- ACP docs: v1 is the latest published protocol; v2 is draft. ACP supports JSON-RPC sessions, optional session loading, permission requests, updates and cancellation, but does not supply durable PocketCode job lifecycle or remote transport security.
- OpenHands docs: append-only EventLog, state-only and event-based updates, FIFO locking/atomic update pattern and persistence/resume. This is a pattern reference, not proof that we should copy a per-event JSON layout or create a new RevDev journal.
- StreamJsonRpc and Polly: credible library candidates; neither supplies our trust boundary or durable recovery.
- Happy: source-level pairing/encryption/security has not yet been audited. No fork decision.

### 13.3 Candidate disposition

- Study now: srt Windows source/limitations, Codex Windows token/ACL/process creation, OpenHands EventLog/state.
- Mapping only: MCP Tasks.
- Deferred narrow spike: ACP read-only session viewer, only after current PocketCode milestone gates.
- Study source before decision: Happy pairing, crypto, self-hosting, revocation and permission flows.
- Conditional only: StreamJsonRpc, Polly, DSSE/in-toto formats, CodeMirror, Velopack, Job Objects, worktree tooling.
- No new SQLite journal until RevDev P8U and existing result/evidence contracts can be inspected on PC.
- Tailscale/Headscale remain owner-policy decisions; no assumption about current free-tier terms.
- Pyodide remains under the existing 314.0.7 review and fixed-task feasibility work; no device evidence exists.

### 13.4 Security and lifecycle guardrails

Parser tolerance may accept explicitly enumerated syntax variants with diagnostics, but must not infer missing ACK, nonce, identity, version authority, confirmation or guard. Parsed content is not thereby policy-approved or authorized. Preserve HOSTED_DENY and destructive-operation refusals.

Retry is not crash recovery. Never blindly retry an ambiguous side effect. Cancellation request, acknowledgement, process termination and verified terminal evidence are separate facts. Job Objects are process control, not a security sandbox or proof of terminal evidence.

Maintain PocketCode's existing product direction, fixed task, seven independent state axes and D-01..D-08 decision boundaries. Maintain RevDev's native acceptance IDs and state axes. RevDev PC source, binary, runtime, watcher, queue and publication state remain UNKNOWN.

### 13.5 Next passes

1. Obtain Gemini's independent SCF-001..018 review and Claude's fixture-by-fixture review; reconcile without replacing native acceptance IDs.
2. Delegate Gemini the Codex token/ACL/process creation and srt Windows policy/cleanup source reads.
3. Delegate Claude OpenHands EventLog/state/persistence and Happy pairing/encryption source reads with exact commits, paths and threat-model findings.
4. Continue identity/state mapping and owner-decision preparation without schema freeze.
5. Prepare a RevDev P8U/source inventory checklist; no journal proposal before PC evidence.
6. Continue only the existing PocketCode fixed-task phone-feasibility work.

### 13.6 Non-actions

No code, dependency, schema, canonical acceptance, source/test, PR #2/#3, provider, account, workload, billing, Actions, installation, device test, merge, deployment, host, watcher, queue, runtime or publication state was changed or exercised. No spend. Documentation-only continuity work on the isolated PocketCode research branch.


## 14. Windows sandbox source-audit continuation — 2026-11-01

Claude supplied a partial Windows sandbox audit after timing out. Read the full audit at:
- AI_COLLAB/WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md

### 14.1 Independent Codex source verification

ChatGPT independently fetched exact upstream Codex source at commit 06f3b4836ac6e4fecc1d75a09b8a9fa369b16635:
- codex-rs/windows-sandbox-rs/src/token.rs
- codex-rs/windows-sandbox-rs/src/elevated/command_runner_win.rs
- commit diff/message.

Correction to Claude's cautious classification: the exact CreateRestrictedToken flags DISABLE_MAX_PRIVILEGE | LUA_TOKEN | WRITE_RESTRICTED are verified in upstream source at that SHA, not merely in the third-party derivative. The same source verifies zero disabled SIDs, zero deleted privileges, restricting SID order (capabilities, extra restricting SIDs, logon, Everyone), zero SID attributes, default-DACL setup and re-enabling SeChangeNotifyPrivilege. The commit verifies that the elevated runner adds the token user SID for ReadOnly/WorkspaceWrite and explicitly leaves the unelevated path unchanged.

The commit documents an elevated named-pipe/Ninja hang caused by the missing sandbox user SID in the restricting list, and says the unelevated repro still hangs. This is a narrow compatibility finding, not a whole-sandbox validation.

### 14.2 srt PR #745 independently verified at the PR-description level

PR #745 merge commit 81145771c9bfc51c5669f071b515209321e0d078 describes an AppContainer WFP matching bypass and fix, additional token-shape probes, anonymous/deny-only residuals, lowered-integrity probe caveats, machine-wide loopback-open behavior and no automatic migration of old filter installations. It states Windows CI passed the described test legs but no manual Windows run was performed. The Rust implementation was not read; do not call this source-verified behavior.

### 14.3 Current disposition and next steps

- Codex: STUDY ONLY. Token source slice verified; full ACL, firewall, account setup, process/job-object containment, cleanup, default policy and stale-install behavior remain open.
- srt: STUDY ONLY, Windows alpha. README/PR design claims are documented evidence; Rust WFP/ACL/runner/install/probe/cleanup implementation remains unread.
- No winner, runtime, dependency, architecture or product decision. No sandbox install or host test. RevDev PC state remains UNKNOWN.
- PROP-ST-01..23 are proposed later test labels only, not native acceptance IDs.
- When Gemini returns, have it independently challenge this audit and read the missing Codex ACL/process and srt WFP/ACL/failure/cleanup sources at pinned SHAs.
- Claude's next separate bounded assignments remain OpenHands EventLog/state/persistence and Happy pairing/encryption. Do not repeat the broad candidate research sweep.
- Continue existing PocketCode fixed-task, identity/state and SCF work. Do not allow sandbox research to displace the canonical milestone.

### 14.4 Non-actions

Documentation-only update on the isolated PocketCode research branch. No source/test, schema, canonical acceptance, PR #2/#3, main branch, provider, account, workflow, Actions, workload, billing, deployment, merge, host, runtime, watcher, queue, firewall, WFP, ACL, installation, elevation or publication state was changed or exercised.


## 15. Deeper srt source audit continuation — 2026-11-01

Read the updated Windows sandbox audit document, especially Section 13:
AI_COLLAB/WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md

Additional pinned source findings at srt merge commit 81145771c9bfc51c5669f071b515209321e0d078:

1. **Token:** srt uses LUA_TOKEN | WRITE_RESTRICTED; disables BUILTIN\Administrators and logon SIDs; deletes all privileges except SeChangeNotifyPrivilege; restricts to capability SIDs, sandbox user SID, Everyone and RESTRICTED; reads back and verifies the resulting restricted-SID set and flag. This differs materially from the Codex token call.
2. **Process containment:** source verifies Job Object KILL_ON_JOB_CLOSE. Target process is created suspended, assigned to a runner-to-child job without breakaway, then resumed. UI restrictions, isolated desktop check, handle whitelist and process mitigations are present in launch source.
3. **ACL:** modify grants withhold FILE_DELETE_CHILD; denies add parent FILE_DELETE_CHILD denies; placeholder intermediate directories receive object-only DELETE denies. Per-user SQLite state tracks holders/ACE refs and file identity; a file lock serializes operations and recovery runs after holder death.
4. **Network:** WFP filters are only at ALE_AUTH_CONNECT IPv4 and IPv6 layers. Windows test suite explicitly documents ICMP ping is not fenced.
5. **WFP readiness:** current srt main at 98a4016d27609ed34dd1fb43d23ed6efb6eeeb77 still says installed if any block filter exists. Open issue #723 reports that a missing IPv6 block can be missed by status and by the default IPv4-only wrapper probe. Open PR #716 proposes a partial state and repair behavior, but is not merged. The PR branch still shows the default TypeScript probe binding IPv4 only.
6. **Shared machine:** install.rs comments explicitly accept BUILTIN\Users read/replace access to ProgramData CA key material to support self-heal, while denying the sandbox group. This requires shared-machine threat-model review.

The extra source work improves confidence in srt's token, ACL and job controls, but also reveals that its network fence is not all-protocol and its current readiness/status path can report healthy with a partial address-family filter set. srt remains STUDY ONLY; no winner or adoption decision. The exact audit has source paths, blob SHAs, line references and confidence distinctions.

Open issue/PR links for follow-up:
- https://github.com/anthropics/sandbox-runtime/issues/723
- https://github.com/anthropics/sandbox-runtime/pull/716
- https://github.com/anthropics/sandbox-runtime/pull/745

No runtime tests were run by ChatGPT. All RevDev PC state remains UNKNOWN.


## 16. Deeper Codex source audit continuation — 2026-11-01

Read Section 14 of AI_COLLAB/WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md for exact pinned source blobs and details.

At Codex commit 06f3b4836ac6e4fecc1d75a09b8a9fa369b16635, ChatGPT additionally inspected firewall.rs, acl.rs, setup_main_win.rs, sandbox_users.rs, dpapi.rs, helper_materialization.rs, process.rs, spawn_prep.rs and elevated/runner_pipe.rs.

New source findings:
- Offline outbound Firewall BLOCK is NET_FW_IP_PROTOCOL_ANY, non-loopback, all profiles and scoped to the offline account SID with LocalUserAuthorizedList read-back. UDP loopback is blocked; TCP loopback is blocked except proxy ports unless allow_local_binding removes those blocks.
- Codex workspace write grants include FILE_DELETE_CHILD. add_deny_write_ace writes a deny on the target but does not add a separate parent FILE_DELETE_CHILD deny. Parent-mediated delete/rename is a high-priority Windows test, not yet a proven bypass.
- dacl_has_write_deny_for_sid considers any overlapping deny bit enough; add_deny_write_ace returns Ok(false) on SetEntriesInAclW/SetNamedSecurityInfoW failure, so callers cannot distinguish a failed write from no change. setup_main_win only bails on accumulated ACL errors when refresh_only is true. These require independent security review.
- Codex uses machine-scope DPAPI for password blobs, with the sandbox secrets directory ACL-denied to the sandbox group. Helper freshness checks size+mtime, not cryptographic hash/signature; the helper directory is ACL-limited to sandbox read/execute.
- Elevated runner pipes use random 128-bit names, sandbox-user-only DACL and verify the connected PID.
- No Job Object/kill-on-close was found in the inspected Codex process launch path; descendant orphan behavior remains UNKNOWN.

These are source-level findings/review concerns, not demonstrated runtime exploits. Codex remains STUDY ONLY. No Windows tests or host operations were performed.


## 17. srt network-fence follow-up and current-main recheck — 2026-11-01

See Section 16 of AI_COLLAB/WINDOWS_SANDBOX_SOURCE_AUDIT_CLAUDE_20261101.md and Section 13 of AI_COLLAB/CLAUDE_RESEARCH_MASTER_INDEPENDENT_RECONCILIATION_20261101.md.

Current srt main snapshot: commit 98a4016d27609ed34dd1fb43d23ed6efb6eeeb77; WFP source blob c3af835ec1479ac19bb1b35181a23d89e5c55640; TS helper blob dbc7c23f4373c69403109429a41144018111941b.

Key new evidence:
- Current filter_status() says installed when ANY block-user filter exists, not when all v4/v6 required filters exist.
- Current default verifyWindowsWfpEgress() binds only 127.0.0.1.
- Issue #723 reports that deleting only the IPv6 block can leave IPv6 reachable while status and IPv4 probe pass; reporter's scope was one Windows 11 26200 machine, loopback tests, 3 repetitions per state, not broad internet testing.
- PR #716 remains open/unmerged. It proposes partial state and repair logic, with unit tests. It does not include the separate IPv6 runtime readiness-probe branch described in the issue comment.
- srt's own tests explicitly state ICMP is not fenced and show DNS Client service resolution outside the child's ALE_USER_ID. Anonymous and deny-only token forms remain warning residuals.
- srt ACL source confirms modify grants omit FILE_DELETE_CHILD, parent-FDC denies are applied for protected paths, and intermediate paths get object-only DELETE denies. State DB/persistence sources describe per-user refcounting, record-first writes, file-lock serialization and crash replay. Install source documents that BUILTIN\\Users can read/replace ProgramData CA-key material, while the sandbox group is denied.

Interpretation: the source supports stronger controls than a high-level summary suggests, but it does not justify complete network isolation. Separate the WFP installed-state bug, IPv6 probe omission, and intentional protocol/service gaps. srt remains ALPHA / STUDY ONLY. No PC or Windows tests, installs, ACL/WFP mutations, upstream PR actions, implementation or adoption decision.


## 18. OpenHands EventLog and Happy pairing source review — 2026-11-01

New detailed review: AI_COLLAB/OPENHANDS_EVENTLOG_AND_HAPPY_PAIRING_SOURCE_REVIEW_20261101.md.

Pinned refs:
- OpenHands/software-agent-sdk main 98849457621881ae2414719b82b8bc1cf535b4ab.
- slopus/happy main 323fb2e9fd0c9a44ceab9239fbc586c513f7f844.

Key OpenHands findings:
- EventLog is per-event JSON, append-only, with event ID, parent validation, durable disk sequence, marker/index refresh and gap reporting.
- LocalFileStore uses atomic text writes and filelock but caches reads; network/NFS locking is explicitly unsupported/unreliable.
- ConversationState writes event file then updates active leaf in separate base_state snapshot. Crash between them could leave a persisted but inactive event; this is an untested source-derived hypothesis.
- EventService uses owner ID/generation/expiry and holds lease lock across generation check plus guarded disk write. This fences persistence writes, not arbitrary external side effects. Event and HEAD writes are separately guarded, not transactional.

Key Happy findings:
- Android pairing derives a device token from ephemeral X25519 and transcript-bound HKDF, shows four emoji, requires user comparison and mutual HMAC proof, and only returns token after daemon proof.
- Fixed crypto vectors and client tests exist; PairingService tests use FakeDaemon.
- No daemon-side /v0/mobile-connector/handshake implementation was located in public repository source search. Replay/expiry/rate-limit/atomic transition semantics remain unknown.
- Android account credentials use Expo SecureStore; happy-agent CLI writes token+secret JSON without file encryption and only requests POSIX file modes. Windows ACL effect unverified.
- Happy's E2E content encryption and server-side third-party token encryption are distinct.

Cross-project interpretation:
- OpenHands informs D-04 event identity/order/evidence and the lease-vs-side-effect distinction, but is not a frozen contract or copy-ready store.
- Happy pairing could be a future device authorization UX layer only; it does not replace remote execution or OS policy enforcement.
- D-01..D-08, fixed-task worksheet, canonical acceptance, product direction and all RevDev roles remain unchanged.

No tests, builds, device runs, upstream changes, PR edits, schema/acceptance changes, provider, deployment, host action or spend. PC and RevDev runtime state remain UNKNOWN.


## 19. Crosswalk/state identity integration and Gemini challenge topics — 2026-11-01

The OpenHands and Happy source findings are now reflected in:
- Section 23 of AI_COLLAB/POCKETCODE_EXECUTION_BOUNDARY_TRUST_CROSSWALK_20261101.md
- Section 11 of AI_COLLAB/STATE_AND_IDENTITY_MAPPING_PREPARATION_20261101.md
- Section 14 of AI_COLLAB/CLAUDE_RESEARCH_MASTER_INDEPENDENT_RECONCILIATION_20261101.md
- AI_COLLAB/GEMINI_INDEPENDENT_REVIEW_PACKET_20261029.md (additional challenge topics)

Key identity guardrails:
- OpenHands EventID, disk sequence, dense in-memory index, parent_id, leaf_event_id and ConversationLease generation are separate concepts. None automatically maps to PocketCode job/run/attempt/operation/policy IDs.
- Happy QR pairing token, handshakeId, ephemeral keys/nonces, transcript hash, role MAC, derived deviceToken and deviceId are separate domains. Account linking is a different flow.
- OpenHands append-event and HEAD snapshot writes are separate; crash window is a hypothesis pending fault injection.
- OpenHands guarded_write fences protected persistence writes, not external side effects.
- Happy pairing daemon-side guarantees remain UNKNOWN because the public source search found client implementations/tests only.

State mapping Section 9's old report-availability statement is explicitly marked historical in new Section 11.4: Claude's research report and Windows audit follow-up have since been supplied in conversation and reconciled; the raw master report is not claimed to be a standalone committed file.

No owner decisions, canonical acceptance, schema, fixed task, PR, source or product direction changed.


## 20. OpenHands crash-window test plan — 2026-11-02

Created [OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md](OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md).

Purpose: falsify or confirm the OpenHands source-derived hypothesis that EventLog can durably contain a newly appended event while base_state still names the previous, still-existing active leaf after a crash. The plan is deliberately not a defect finding and has NOT been executed.

The plan defines OH-HEAD-FI-01..08 as local test-plan labels only (not PocketCode acceptance IDs): before append; during event write; immediately after event-file commit; after append returns but before leaf assignment; during base_state atomic replacement; after replacement; after both writes but before caller acknowledgement; and concurrent lease takeover around the two guarded writes. Each test requires abrupt process termination, fresh-process restore, raw persisted files/hashes, EventLog index/gap state, restored leaf and active ancestry. It separates event durability, discoverability, active HEAD, acknowledgement and lease ownership. It excludes NFS/network storage and warns that process-kill testing does not prove power-loss durability.

The plan includes same-ID/same-payload retry, same-ID/changed-payload conflict, new-ID logical retry, changed-parent and delayed replay cases. It explicitly distinguishes a missing saved leaf fallback from a still-existing old leaf.

Cross-project mapping: lifecycle D-04 remains OPEN; D-05 BLOCKED; D-06 and D-08 owner-open. No new acceptance ID, schema, field or owner decision. No tests, source changes, providers, PR changes, builds, deployment or host operations. RevDev PC state remains UNKNOWN.

Next useful reviewer action: ask Gemini to challenge the test boundaries and assertions using the updated independent-review packet. Claude follow-up is only warranted if it can run or inspect the exact pinned OpenHands source in a disposable test environment; no claim of execution without exact command/environment/results.


### 20.1 Important OpenHands source refinement — 2026-11-02

A second exact-ref source pass found an explicit OpenHands agent-server recovery path. At pinned commit `98849457621881ae2414719b82b8bc1cf535b4ab`, `openhands-agent-server/openhands/agent_server/event_service.py` lines 1424–1467:
- a restored conversation with persisted execution_status RUNNING is marked ERROR;
- recovery scans the full event log, not only active branch, for unmatched actions;
- if the first unmatched action has no ObservationBaseEvent with the same tool_call_id anywhere in the log, it appends a non-retryable internal AgentErrorEvent explicitly parented to the action;
- source comments state this avoids attaching the recovery result to stale HEAD as a sibling and leaving an orphan tool result.

SDK state.py lines 268–320 confirm a still-existing saved leaf is returned as active HEAD; missing-leaf repair only runs when the saved leaf event file is absent. Thus the append/HEAD gap remains real at the persistence layer, but it is not accurate to say the current agent-server has no recovery. The recovery has conditions and limitations: RUNNING status, first unmatched action only, log-wide tool_call_id suppression, and no proof about whether a side effect occurred before the crash. It must not be treated as safe provider retry.

The falsification plan now includes OH-HEAD-FI-09..14 for RUNNING/non-RUNNING restore, pre-existing observation suppression, multiple unmatched actions, mismatched action association and external side-effect-before-observation ambiguity. Plan remains NOT EXECUTED. See updated plan for exact test design. D-04 remains OPEN; D-05 BLOCKED; D-06 and D-08 owner-open. No acceptance IDs or owner decisions changed.


### 20.2 Existing OpenHands tests found, narrowing the gap — 2026-11-02

A targeted search of the pinned OpenHands source found:
- `tests/agent_server/test_event_service.py`, blob `fc6e589f71318ac36df92b72c1fd0225549d1436`, lines 2419–2678: mocked unit tests for RUNNING + unmatched action, RUNNING + no unmatched action, non-RUNNING skip, and observation suppression when tool_call_id matches but action_id differs. The inspected assertions do not verify recovery AgentErrorEvent.parent_id or real restored active ancestry.
- `tests/sdk/conversation/test_get_unmatched_actions.py`, blob `35798b1bccb60b0976cf0785682ef17181e4450b`: SDK helper matching for observation/rejection/error events by tool_call_id.
- F31.crash-tool-call in `.agents/skills/verify-agent-server/references/feature-map/F31-persistence-and-limits.md`, blob `5082730e1ba1d333daeaf321c21214ad4924cd12`, lines 191–220: documented SIGKILL-during-tool-call integration recipe asserting ERROR, one AgentErrorEvent, zero ObservationEvents and resumed model delivery. It does not assert parent_id or active ancestry; the broader recipe includes a DeepSeek API key/model precondition.

The next useful gap is therefore not more mocked branch tests. It is a real local persistence/restore crash test that asserts action → recovery error active ancestry, plus a direct parent_id assertion. Also challenge full-log observation suppression, multiple unmatched actions and side-effect ambiguity. Existing test sources were inspected, not run. Avoid paying for the DeepSeek recipe; a stub-only equivalent is a future feasibility question, not a claimed substitute.


### 20.3 Final test-plan refinement: EventLog marker ordering — 2026-11-02

Pinned EventLog source at `event_store.py` lines 288–297 writes event JSON first, updates in-memory indexes/length, then advances the sidecar marker. Marker update at lines 320–330 deletes the old marker before writing the new one, so interruption should leave no marker rather than a stale marker claiming the new length. `LocalFileStore.write` for strings uses atomic_write_text (`local.py` lines 63–68). The plan now includes crashes after event-file replacement, during in-memory/marker progression, after marker deletion and during fresh index/marker rescan. Atomic replacement/process-kill survival must not be called power-loss durability without fsync/storage evidence.

Existing recovery coverage is now mapped. Do not duplicate the mocked EventService unit tests or the F31 SIGKILL recipe. Remaining highest-value gap: real local persisted-file crash/restore asserting action → recovery error active ancestry and `parent_id=action.id`, plus focused full-log suppression/multiple-unmatched cases. The expanded plan is in Section 11–12 of OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md. All test plans remain NOT EXECUTED.


### 20.4 OpenHands priority escalation: parallel action batches and navigation — 2026-11-02

A deeper source pass found two more important supported paths. Exact plan and evidence are in `AI_COLLAB/OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md`, Section 13.

**Parallel/multi-action crash:** `event/base.py` lines 181–200 confirms multiple ActionEvents per LLM message. `response_dispatch.py` lines 224–255 emits all ActionEvents before executing; `_ActionBatch.aprepare` waits for the complete batch, and `_ActionBatch.emit` only then emits results (`agent.py` lines 695–716 and 327–381). `parallel_executor.py` lines 128–191 uses `asyncio.gather`. Startup recovery currently writes only one AgentErrorEvent for `unmatched_actions[0]` (`event_service.py` lines 1436–1467). The interrupt path, by contrast, writes synthetic errors for every active-branch orphan (`local_conversation.py` lines 2777–2805). Test whether startup recovery leaves later tool calls detached/unanswered. FI-15..18 added.

**Navigate/rewind:** `LocalConversation.navigate_to` lines 988–1011 keeps abandoned events in the EventLog but moves HEAD; remote wrapper lines 1914–1943 and EventService lines 2358–2372 expose it; F10 docs confirm the behavior. Startup recovery scans full log and suppresses a recovery error when any observation-like event matches tool_call_id, even if the observation is outside active ancestry. This is a concrete test target, though not yet a confirmed defect. Reconcile with the comment that remote branching is unsupported (#3749). FI-19..22 added.

**F31 stub note:** crash-tool-call T uses a local `llm-stub` endpoint and placeholder key in its inline agent. The wider F31 setup also runs `llm preset deepseek`, so do not claim the full family is provider-free. Whether the preset can be omitted for isolated F31.crash-tool-call is not yet verified.

All FI-15..22 labels are local plan labels, not PocketCode acceptance IDs. No upstream tests run/changed; no owner decision changes.


### 20.5 OpenHands recovery message may overstate external outcome — 2026-11-02

Startup recovery AgentErrorEvent text says the tool execution “did not complete” (`event_service.py` lines 1458–1462), with INTERNAL / retryable=False classification. But the source cannot prove no external side effect occurred before the crash. In a multi-tool batch, one tool can finish an external side effect while another blocks; results are emitted only after the whole batch returns. Thus a crash may leave completed side effects without observations. Treat this as an important PocketCode design warning: missing result/evidence means external outcome UNKNOWN unless independently verified; non-retryable is not proof of non-execution. See crash-window plan Section 14. No PocketCode owner decision changed.


### 20.6 OpenHands #3749 citation contradiction to resolve

The startup recovery comment says remote branching is unsupported and cites #3749. But issue #3749 itself is closed and titled “Conversation history tree: agent-server HTTP exposure (fork/navigate/schema)”; its body defines the `/navigate` HTTP route and says event search continues to return all branches after navigation. This is consistent with pinned `navigate_to` source and F10 docs. Gemini should inspect linked PR/merge and distinguish unsupported concurrent/multi-writer branching from supported in-place navigate/re-root and separate forked conversations. Do not accept the comment's citation at face value. The full plan includes FI-19..22; not a confirmed defect yet.


### 20.7 Issue #2298 is fixed; new concern is full-log vs active-branch mismatch

OpenHands issue #2298 is CLOSED. The old bug was AgentErrorEvent not matching ActionEvent during pending-action detection, causing duplicate execution after resume. Pinned `state.py` lines 713–752 now match AgentErrorEvent by tool_call_id and tests cover it. Do not report the old bug as current.

New hypothesis: startup recovery checks the full EventLog; ordinary pending-action detection checks only active_branch (`agent.py` lines 747–756). After supported navigation, an observation may remain in the full log but outside active ancestry. That observation can suppress recovery while the action remains pending on the active branch. The detailed test sequence is crash-window plan Section 16. Gemini must establish RUNNING lifecycle reachability and intended replay semantics before calling this a defect.


### 20.8 Direct unit-test proof for abandoned branches

Pinned `tests/sdk/conversation/local/test_conversation_tree.py`, blob `9086af335ea59d267939ba0302d524f0594df3c1`, lines 117–141, contains `test_navigate_then_emit_creates_sibling_branch`: after navigating to root and appending B1, abandoned A1/A2 remain in EventLog but are absent from active view; A1 and B1 are siblings. This directly proves the full-log/active-branch split. It does not alone prove the full FI-19 server restart sequence. Keep that final lifecycle as an integration test, not a source-only conclusion.

## 20.9 OpenHands recovery issue/fix chronology update — 2026-11-02

The OpenHands review now distinguishes the crash/recovery issue history:
- #3045 was closed by #3063 (merged 2026-05-05, b6c63d0): restart recovery skips creating a synthetic AgentErrorEvent if an ObservationBaseEvent already exists for the action tool_call_id in the loaded state.
- #4591 was closed by #4932 (merged 2026-09-23, dd8d9f6): ToolCallMatchingProperty manipulation-index calculation tolerates orphan observations whose ActionEvent is absent from the view; duplicate-result detection remains separately enforced.
- The #4932 review history identifies a separate incremental-view duplicate-observation path. Do not assume rebuilding/enforcing views cover every incremental append.
- #6289 (opened 2026-10-28 against SDK 1.58.2 / main 46b1fa5) reports post-Finish tool calls left unmatched and executed on a later turn. Keep separate from crash recovery; verify whether it is present in the pinned commit.

The detailed test separation FI-23..FI-26 and Gemini challenges are in AI_COLLAB/OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md Section 18 and AI_COLLAB/GEMINI_INDEPENDENT_REVIEW_PACKET_20261029.md. No OpenHands tests were run; no source/tests, PocketCode acceptance IDs, owner decisions, PRs or main branch changed. RevDev PC state remains UNKNOWN.

### Gemini A–F independent verdict update — 2026-11-02

Gemini's independent review at pinned OpenHands commit 98849457621881ae2414719b82b8bc1cf535b4ab classifies multi-action startup recovery (A/C) as confirmed defective: multiple ActionEvents can be persisted before batch execution, but startup recovery emits one AgentErrorEvent for unmatched_actions[0], potentially moving the active leaf to a branch that excludes later actions. Acceptance must inspect actual leaf/ancestor IDs and every interrupted action, not only parent_id.

Gemini also classifies full-log observation suppression (B) as a defect. ChatGPT retains this as a strong but qualified candidate until realistic tool_call_id reuse is demonstrated; the #3063 guard intentionally suppresses duplicate recovery when a matching observation is already present. Distinguish active-branch semantics from synthetic ID-reuse tests.

Other Gemini findings: non-RUNNING recovery guard confirmed, but PAUSED-with-in-flight-tool reachability remains to prove; recovery error wording overstates external non-completion; local stub crash test appears feasible but is not executed; EventLog power-loss durability is NOT ESTABLISHED absent exact fsync/storage proof.

For a safe multi-action recovery ancestry, if actions are A1 -> A2 -> A3, one possible test topology is E3 parented to A3, then E2 parented to E3, then E1 parented to E2, leaving E1 as leaf and all actions in its ancestor chain. This is a topology proposal for falsification, not an adopted PocketCode decision.

Detailed reconciliation and exact Gemini follow-up requirements are in AI_COLLAB/OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md Section 19. No upstream source/tests were run or modified; no PocketCode source/tests/schema, canonical acceptance IDs, owner decisions, PR #2/#3 or main changed. Current working branch comparison: 567 ahead, 0 behind. PR #2/#3 remain open/unmerged. RevDev PC/host/queue state remains UNKNOWN.


## 22. ChatGPT continuation update — OpenHands Gemini A–F correction (2026-11-02)

Read Section 21 of `AI_COLLAB/OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md` before continuing. It is the authoritative latest independent source reconciliation and supersedes the earlier Gemini A–F interpretation where conflicting.

Critical correction: the alleged multi-action branch-detachment is not established. In pinned `event_service.py`, startup recovery creates one AgentErrorEvent without explicit parent_id and sends it through LocalConversation._tree_stamping. ConversationState._stamp_parent_id defaults the parent to the current active leaf. For Prompt → A1 → A2 → A3, expected ancestry after one recovery error is Prompt → A1 → A2 → A3 → E1, not Prompt → A1 → E1. The code comment says explicit action parent but the constructor does not supply it. Test incomplete multi-tool batch/model-history behavior, not the unsupported detached-tree explanation. Do not implement reverse-order errors based on Gemini's proposed topology.

Other unresolved tasks: PAUSED may be persisted while tool execution is in flight; startup recovery skips PAUSED; prove resume dispatch semantics. Trace the full LocalFileStore write helper before claims about atomic replace/fsync. Provider ID uniqueness scope is not proven. F31 isolated stub/no-DeepSeek setup is unverified. Missing observation does not prove no external side effect. Keep #2298 fixed.

Fresh repo status: working branch is 569 ahead, 0 behind main; PR #2 and #3 remain open draft and unmerged. Documentation-only continuity work on this isolated branch remains permitted. Do not touch either PR or main. No source/tests/schema/acceptance changes, provider workload, Actions, merge, deployment, spend, or host/queue operations. PC/RevDev state remains UNKNOWN.


## 23. Critical OpenHands multi-action recovery correction (2026-11-02)

Read AI_COLLAB/OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md Section 21.8 and PROJECT_STATUS.md's OpenHands correction before continuing. They supersede the earlier Section 22 statement and the contrary paragraph in plan Section 21.

The earlier ChatGPT conclusion was wrong. At pinned OpenHands commit 98849457621881ae2414719b82b8bc1cf535b4ab, startup recovery explicitly constructs one AgentErrorEvent(parent_id=first_action.id, ...) for unmatched_actions[0]. ConversationState._stamp_parent_id preserves explicit parent IDs; append moves the active leaf to the error. Tool calls in one model response are converted to ActionEvents in a loop before batch execution. Therefore, for three unmatched actions A1→A2→A3, the recovery event E1 is attached to A1 and becomes active leaf; A2/A3 remain in the full EventLog but are outside active ancestry. Source-level multi-action branch detachment is CONFIRMED.

Current tests have a one-unmatched-action startup recovery case and separate multi-tool execution tests, but no located test combining a multi-action batch with crash/restart and resumed request reconstruction. The next task is to specify/run (only if explicitly authorized) a targeted integration test that checks event IDs/parents, active leaf, full log versus active branch, model-facing history, partial completions and side effects. Do not implement a fix or adopt reverse-order error emission from source reasoning alone. Preserve #2298 matching behavior and treat missing observations as external outcome UNKNOWN.

The F31 crash-tool-call uses a local llm-stub with placeholder key; the broad F31 setup mentions DeepSeek for a separate real-model case. Isolated no-provider feasibility is plausible but not fully bootstrap-verified; no workload run. EventLog helper fsync correction remains as in plan Section 21.7. PAUSED startup recovery skip remains source-confirmed; duplicate redispatch on resume remains unresolved. Provider tool_call_id uniqueness across turns remains unproven.

Claude is currently timed out. This correction is independently source-grounded; when Claude returns, ask it to specifically challenge the explicit parent_id=first_action.id and active-branch consequence. Do not treat the prior pending Claude prompt's contrary premise as valid.

No OpenHands source/tests modified or executed; no provider workload, spend, PR, merge, deployment, PocketCode source/schema/canonical acceptance, PR #2/#3, main, or RevDev host/queue action. RevDev PC/runtime/installed binary/queue/publication state remains UNKNOWN.


### 23.1 PAUSED crash/replay path (2026-11-02)

Plan Section 21.9 adds a second source-confirmed OpenHands risk: pause() can set PAUSED after a blocking tool has begun; startup recovery only handles RUNNING; on resume LocalConversation resets PAUSED to RUNNING and Agent._step executes unmatched actions on the active branch before calling the LLM. Therefore a PAUSED conversation killed before its observation is persisted can re-dispatch the action on resume. The existing pause test proves the pause-during-tool window is reachable in the SDK. Full server SIGKILL/restart integration and actual external duplicate side effect remain to be tested. Keep interrupt() separate: it sets cancellation token/cancels async task and has a synthetic orphan-error path.


### 23.2 Latest GitHub continuity status (2026-11-02)

Working branch pocketcode-execution-boundary-crosswalk-2026-11-01 compares 580 ahead, 0 behind main (base 555840d8d83342513d9cd353d4d1522d46a5c82d). PR #2 and PR #3 were rechecked and remain OPEN; neither was modified. Recent branch commits are documentation-only OpenHands evidence corrections. Main and both PRs remain untouched.


### 24. OpenHands PAUSED lifecycle correction — 2026-11-03

Read Section 21.10 of `AI_COLLAB/OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md` and `AI_COLLAB/OPENHANDS_PINNED_RECOVERY_EVIDENCE_RECONCILIATION_ADDENDUM_20261102.md` before continuing. This supersedes the broad wording in Section 23.1 that says the existing pause test proves PAUSED can persist while an already-running tool remains in flight.

The existing test `test_pause_while_running_continuous_actions` uses synchronous `conversation.run()`. The state lock is held over the tool step; `pause()` waits for the step/result before persisting PAUSED. The test proves a pause request stops later iterations, not that it persists PAUSED during the already-running tool.

A narrower async race remains source-supported: `Agent._astep()` releases the state lock while awaiting `llm.agenerate()`. A normal pause can persist PAUSED during that LLM wait. When a tool-call response returns, the inspected async dispatch path does not recheck PAUSED before action creation/tool execution. If the process is killed during that newly dispatched tool before its result event is persisted, startup recovery skips it because startup repair only handles RUNNING. An explicit resume then reaches the unmatched-action path on the active branch and may dispatch again.

Use the following status:
- Synchronous pause during an already-running tool leaves PAUSED-until-step-completes unsupported by the current lock/test evidence. The call waits.
- Async pause during outstanding LLM I/O, followed by tool-call dispatch after PAUSED, is a source-confirmed race path; deterministic persisted restart test NOT RUN.
- Startup skips PAUSED: source-confirmed.
- Resume can dispatch an unmatched active-branch action: source-confirmed path; complete server restart integration NOT RUN.
- Actual duplicate external side effect: UNKNOWN until independently observed.

Keep `interrupt()` separate: it cancels the async run and has a synthetic orphan-error path. Do not infer that a missing ObservationEvent proves no external side effect.

No upstream source/tests were changed or run. No provider workload, spend, PR, merge, deployment, PC/host or queue action occurred.


## 25. 2026-11-03 continuation: current local comparator, shared fixture reviews and RevDev validation

### 25.1 PocketCode local-execution comparison

The current [fixed-task comparison worksheet](PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md) now contains a dated public-source refresh:

- Pyodios is the strongest no-cost iPhone-local candidate identified for the canonical small CSV-to-JSON task. Its current public listing says free, iOS 26+, v1.1.0 and 42.9 MB; official documentation describes local Python 3.14.2 / Pyodide 314.0.5, a project folder, script/notebook/REPL workflow, file import/export and CSV/JSON inspection.
- Its important reliability constraint is that active Python cannot be interrupted. The documented 120-second timeout does not stop execution; a later run waits until the session is restarted. Its Python process state is ephemeral across launches.
- Carnets remains a credible free on-device Jupyter alternative, but it is a much larger download and must be evaluated as a notebook workflow, not assumed to be a drop-in script IDE.
- Pyto is an optional third candidate only if its free feature coverage is useful for comparison.

No app was installed. No code was run in any candidate. The canonical CSV-to-JSON success/malformed-input comparison remains NOT RUN. Execution location is still undecided. Do not describe Pyodios or Carnets as a chosen backend.

The key product question is now narrower: code execution itself is already available through free local alternatives. PocketCode must demonstrate value through a trustworthy run-bound receipt, honest timeout/cancellation and side-effect semantics, source/input/output identity, explicit permission/egress controls, and a portable report that improves AI correction through explicit share/copy/paste. These are hypotheses to test, not proven PocketCode capabilities or validated demand.

### 25.2 Shared contract fixture review queue

The existing [Shared Contract Golden Fixture Catalogue preliminary review](SHARED_CONTRACT_GOLDEN_FIXTURE_CATALOGUE_CHATGPT_PRELIMINARY_REVIEW_20261101.md) now contains separate review assignments for:
- Gemini: security, evidence-oracle completeness, false-PASS and identity/replay adversarial review of SCF-001..018.
- Claude: architecture and implementation-feasibility review of durable state, identity, CAS/fencing, lifecycle ordering, publication, release/transfer/receipt and fixture testability.

Keep SCF-001..018 unchanged. These are provisional shared fixtures, not owner-approved acceptance, a schema freeze, or a replacement for native AEC/LOOP/CASE/COORD/DR/P8U/P0-D/AWC/RelayRef suites. No schema was drafted or frozen. Neither review response is yet recorded as received in this handoff.

### 25.3 RevDev AWC fixture-manifest validation checkpoint

A separate documentation-only checkpoint was added to RevDev's research branch:

- [RevDev CURRENT_GOALS](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/CURRENT_GOALS.md), latest blob `7d420c793be303fe4d8ed381d643f52c8b982234`.
- AWC manifest blob `c2d4cba6c836f725f7bc4585f91e02d443fe89e1`.
- AWC manifest schema blob `d7436f5b9df8c34b29ad7453e105b7c0270fbe65`.
- Draft 2020-12 schema meta-validation and the current 18-fixture manifest structural validation passed under Python 3.13.5 / `jsonschema` 4.26.0.
- Current AWC-001..018 IDs are sequential and unique. The schema does not reject a deliberately duplicated fixture ID, so a separate semantic ID uniqueness assertion is required in a future harness. No schema or fixture ID was changed.

This is not Work Coach semantic-validator execution, evidence authenticity, model trial or product acceptance. The latest 33-method semantic validator suite remains NOT RUN. RevDev P8U/P0-D runtime acceptance remains NOT RUN and the P0 publisher/orphan/retry/recovery defect remains release-blocking.

### 25.4 RevDev owner-decision boundary

OD-06 remains OPEN for the accepted-dispatch/intent-but-no-runner-start gap. P8U-09 currently means the runner starts and then crashes before a local terminal result is written. Do not silently expand P8U-09 or invent a new canonical P8U ID. The absence of runner-entry evidence is UNKNOWN unless a complete authoritative oracle proves no runner entered during the relevant interval.

### 25.5 OpenHands recovery correction

The current authoritative study documents are:
- [Pinned recovery evidence reconciliation addendum](OPENHANDS_PINNED_RECOVERY_EVIDENCE_RECONCILIATION_ADDENDUM_20261102.md), commit `df26c91d9df2d06c31ef01b6d1b0b326caabe9ef`.
- [Crash-window falsification plan](OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md), Section 21.10 contains the corrected pause lifecycle.
- This handoff, Section 24, contains the correction in summary.

Multi-action recovery explicitly parents one error to the first unmatched action and can detach later actions from active ancestry; stale full-log observation suppression can disagree with active-branch pending-action detection after navigation; EventLog local writes fsync the temp file before replace, while power-loss durability remains unproven; and missing observations do not prove no external side effect. The normal synchronous pause test does not prove PAUSED while a tool is already executing. The narrower async LLM-I/O pause race remains source-supported. Full crash/restart integration scenarios remain NOT RUN. #2298/#2300, #3045/#3063 and #4591/#4932 remain merged historical fixes; #6289/#6290 is separate and unmerged at the last check.

### 25.6 Next bounded sequence

1. Send the two shared-fixture review prompts to Gemini and Claude; reconcile concrete counterexamples against the exact catalogue and native acceptance. Do not freeze a shared schema.
2. Continue the same canonical CSV-to-JSON comparison only through source research until a hands-on attempt is separately authorized. Pyodios is the first local candidate, Carnets second. The fixed task remains NOT RUN.
3. Close the OpenHands source review only with the targeted combined regression specifications and any independent Claude challenge. Do not modify OpenHands or PocketCode source/tests.
4. Keep RevDev product P0 first. No PC runtime or publisher work is possible until fresh PC access and an authorized read-only inventory.
5. Refresh exact branch/main refs and PR #2/#3 before further consequential work.

No source/test/acceptance change, schema freeze, PR action, provider workload, account, billing, install, Actions, merge, deployment, PC host, queue or runtime operation occurred. PR #2/#3 remain open draft and untouched; main remains unchanged; budget remains $0.


## 26. OpenHands server-path and F31 source follow-up — 2026-11-03

See Section 21.11 of the [crash-window plan](OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md) and Section 10 of the [pinned recovery addendum](OPENHANDS_PINNED_RECOVERY_EVIDENCE_RECONCILIATION_ADDENDUM_20261102.md).

- Pinned `EventService.run()` explicitly selects native `await conversation.arun()` when the conversation and agent have async overrides. The normal `LocalConversation` + `Agent` combination meets those conditions. Thus the pause-during-LLM-I/O race is relevant to the ordinary agent-server route, not only a direct SDK invocation.
- The existing pause test still proves the synchronous pause-during-tool case waits for the current step/result; it does not prove PAUSED is persisted during that tool.
- The narrow async race remains: while `Agent._astep()` has released the lock awaiting LLM I/O, normal pause can persist PAUSED; the returned tool-call response may then dispatch without checking PAUSED. Startup only repairs RUNNING. End-to-end persisted server test remains NOT RUN.
- F31's `TOOL_AGENT` explicitly targets a local `openai/qa-stub` endpoint at `$TOOL/v1` with a placeholder key and zero retries. The documented DeepSeek key requirement is tied to a separate `F31.no-plaintext-at-rest` real-model run; a reduced no-DeepSeek bootstrap for crash-tool-call is plausible but not fully command-verified.

No OpenHands source/tests or workloads changed or ran. No provider request, spend, Actions, host/queue operation, PR change, merge or deployment occurred.


## 27. OpenHands regression sequence consolidated — 2026-11-03

The detailed, non-duplicative test sequence is now recorded in [OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md](OPENHANDS_EVENTLOG_HEAD_CRASH_WINDOW_FALSIFICATION_PLAN_20261102.md), Section 21.12.

Priority order:
1. Extend the existing one-action EventService startup unit test to assert explicit `parent_id` and active ancestry.
2. Add real LocalFileStore restore coverage for a three-action unmatched batch and inspect both full EventLog and provider-facing active history.
3. Deterministically exercise pause during outstanding native async LLM I/O, response release, tool dispatch, process termination, EventService restore and resume.
4. Add navigation/stale-observation, partial-completion, interrupt-control and independently observed side-effect cases.
5. Keep process-kill and power-loss durability as separate test claims.

The existing tests and F31 scenario are controls, not substitutes for the missing combined cases. No fix is selected. Reverse-order error chaining is not accepted without proving tool-call order, partial observations, late results and provider-facing history. All tests remain NOT RUN; no OpenHands source/tests, PocketCode source/acceptance, provider workload, Actions, PR #2/#3 or host operation occurred.


## 28. Complete cross-project handoff — 2026-11-03

The authoritative new-chat entry point is now the complete handoff in the RevDev repository:

[NEW_CHAT_HANDOFF_REVDEV_POCKETCODE_2026-11-03.md](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/NEW_CHAT_HANDOFF_REVDEV_POCKETCODE_2026-11-03.md)

Read it fully before continuing. It consolidates both product goals, separate repository/acceptance/security boundaries, three-AI roles, PC-free/$0/authorization constraints, current RevDev P0/P8U/OD-06 status, Work Coach manifest validation gap, PocketCode owner decisions and fixed-task research, pinned OpenHands findings and OH-RCV-01…08 test sequence, shared SCF review status, exact repository/PR snapshot and ordered next actions.

**Live-count supersession:** latest 2026-11-03 compare is RevDev 447 ahead / 0 behind main and PocketCode 598 ahead / 0 behind main. Earlier notes in this handoff recording 445/0 and 595/0 predate the last continuity commits and are superseded. PR #2 and #3 remain open draft and untouched. No PR action, source/test execution, provider workload, Actions, host/queue operation or deployment occurred.
