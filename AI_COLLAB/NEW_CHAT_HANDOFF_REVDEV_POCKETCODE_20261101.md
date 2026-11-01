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
