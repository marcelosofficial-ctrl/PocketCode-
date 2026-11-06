# PocketCode state ledger — 2026-11-06

**Repository:** marcelosofficial-ctrl/PocketCode-  
**Branch:** pocketcode-ai-workflow-director-research-2026-10-28  
**Last verified before this checkpoint:** 4446135bf1345f37aa5d221d27c0eabbdbcef5c7  
**Compare before this checkpoint:** 820 ahead / 0 behind main; merge base 555840d8d83342513d9cd353d4d1522d46a5c82d. Ahead count is branch-history divergence, not product progress. Fetch live refs before consequential work.

## Goal
Build a phone-first, provider-neutral Agentic Orchestration Control Plane that makes AI-generated technical tasks executable from iOS/Android and returns truthful, portable evidence for AI correction. It is not a generic Python IDE. RevDev and PocketCode are intended to converge into one PC-and-phone product/program while retaining separate repos, roadmaps, clients, adapters, runtimes, security boundaries, acceptance suites and release gates.

## Current device evidence
- Owner-reported app: Pyodios 1.1.0 / Build 7; Pyodide 314.0.5; Python 3.14.2; WASM. Device model/iOS version UNKNOWN.
- Owner ran unchanged canonical main.py with items.csv in one project. Editor displayed exactly [Bridge/executePython] PythonError.
- Owner inspected existing summary.json; it exactly matches canonical oracle: grand total string 10.75, 2 line items, notebook 7.00, pen 3.75.
- Owner checked More → Settings → Error Log → View Error Log. Only Editor: PythonError; no traceback.
- Classification: ARTIFACT-LEVEL FUNCTIONAL SUCCESS / BRIDGE ERROR UNRESOLVED / FULL RUN INCONCLUSIVE. Native process exit, stderr, bridge root cause UNKNOWN. Export/read-back, relaunch persistence, malformed-input and PocketCode acceptance NOT RUN.
- Next exact action: in the existing Pyodios session, run the read-only sys.last_exc / sys.last_value probe in PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md. Preserve the success project. Do not rerun/overwrite, restart/reset, clear variables/logs or run GC. If no exception is available, record unavailable evidence.

## Product decisions and constraints
- $0 default; no paid provider, host, account, workload or billing without separate owner decision.
- No runtime/provider/cloud host selected; Discovery/product definition phase. No PC requirement for PocketCode.
- Explicit paste-to-context; no clipboard polling or intrusive overlays. SSH/Tailscale and optional cloud remain adapters/research only.
- Stock Pyodide/WASM is not a hostile-code sandbox. Default-deny permissions; egress off by default for untrusted code; disposable externally constrained execution required.
- No secrets/private data in public repo. No product claims beyond verified evidence.
- D-001 unified PC/phone direction with separate development boundaries; D-002 GitHub durable source; D-003 public repo has no secrets; D-004 validate before stack commitment; D-005 $0 default.

## Product shape and architecture
- MVP: explicit paste/import → bounded execution → honest status and actual stdout/stderr/exit evidence where available → real artifact list/export → compact copyable report → user-mediated AI correction → distinct preserved attempts.
- Later candidates: file conversion/batch processing, CSV/JSON validation, tests, downloadable artifacts, multi-file workspaces, remote SSH/Tailscale, optional cloud adapters. GUI automation, arbitrary package install/open internet and direct AI integrations are not first-MVP commitments.
- Preserve identity chain: CommandId → DispatchAttemptId → ExecutionId → ObservationSequence → ResultReceipt. Session IDs/task handles are not command IDs.
- Separate child execution facts, wrapper/supervisor facts, lifecycle/disposition, verdict, cleanup, artifact integrity/release and AI correction lineage. Preserve idempotency, replay, fencing and provenance.
- PASS requires trusted terminal success and child exit 0; FAIL requires confirmed program/runtime failure; INCOMPLETE for timeout/cancel/rejection/infrastructure/missing/contradictory evidence. UI timeout does not prove process termination.
- Keep canonical LOOP-01..14, CASE-01..16 and D IDs unchanged. CASE-04 remains INCOMPLETE/timed_out when trusted timeout. Do not precedence-patch scripts/report_contract.py until typed child-exit vs wrapper-exit vs termination provenance is resolved. EVAL-06 is separate checkpoint experiment.

## Three-AI roles
- Claude: lead developer and architecture/implementation reviewer.
- Gemini: co-developer and independent security/spec auditor.
- ChatGPT: continuity holder, evidence reconciler, acceptance architect and cross-project coordinator.
- Owner forwards reports manually. No direct AI-to-AI communication assumed. One lead writer per branch/work item; other AIs review read-only or take disjoint scopes.

## Research references and current open work
- OpenHands and Cline are pattern references, not frameworks to adopt wholesale. MCP Tasks may inform async tool-task status; the legacy Agent Communication Protocol (ACP) was archived 2025-08-27 and merged into A2A. Evaluate current A2A for agent-to-agent interoperability, not archived ACP. MCP/A2A task IDs do not replace PocketCode command/attempt identity or trusted receipts. Neither replaces PocketCode command/attempt identity or trusted receipts. Reject wildcard auto-approval.
- After Pyodios probe: malformed-header fixture in separate fresh project; then export/read-back and natural relaunch persistence as separate tests. Do not overwrite success project.
- Source work next: typed CASE-04 exit provenance; degraded collector/teardown/artifact release; synchronous pre-execution network-isolation barrier. Use fake adapters/processes and exact-SHA tests; no live services or spend.

## Repository state
- PR #2 and #3 are OPEN/DRAFT, unmerged, unchanged; they are separate branches. Do not merge or modify absent explicit authorization.
- Actions run query for active branch returned no items; this is not proof no CI activity exists.
- Latest pass changes documentation/continuity only; no PocketCode product code/tests/runtime/provider/fixture/schema/acceptance/PR/merge/deployment changed.
- Read first: AI_COLLAB/CHAT_START_HERE.md, then this ledger, then AI_COLLAB/PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md and AI_COLLAB/NEW_CHAT_HANDOFF_20261106.md.


## 2026-11-06 — Cross-project working-method upgrade

Authority: owner-provided RevDev working-method decision. Applies to PocketCode continuity and engineering process only; does not replace product goals, revise runtime/security/budget boundaries, or transfer RevDev code, architecture or acceptance evidence.

- GitHub is durable project memory; chats are replaceable workers. New chats resume from live GitHub state, not hidden context.
- Read compact entrypoint, latest ledger and active handoff first. Retrieve only task-specific source/tests/review packets; search/index large records before expanding. Avoid duplicate master documents and historical rereads without a concrete question.
- Use bounded substantial passes with objective, scope, expected result, evidence requirements and stop condition. Prefer a verified vertical slice over many open threads.
- Batch independent read-only operations in modest groups. Serialize dependent work and shared writes. Keep outputs compact. Verify every write by exact read-back.
- On interruption/tool failure, do not assume success or failure. Re-fetch live branch and target objects, inspect commits and exact blobs, reconcile whether the operation happened, then resume. Never blindly replay a possibly completed mutation.
- Durable operation model: stable EffectId across retries; fresh AttemptId per actual attempt; exact input/argument hashes; explicit dependencies and authorization scope; durable operation history; per-operation progress/evidence; heartbeats/leases; fencing; bounded retries; exact reconciliation of ambiguous external effects.
- Keep execution outcome, collection state, lifecycle/job disposition, cleanup, publication and final acceptance distinct. Successful execution is not automatically a published or accepted result.
- Checkpoint every 2–3 meaningful passes and immediately after consequential implementation, testing, review, CI or architectural decisions. Update entrypoint and ledger, append work log, pin exact branch/source/test hashes, and rotate before context becomes unhealthy.
- Roles remain Claude lead developer/reviewer; Gemini co-developer and independent security/spec auditor; ChatGPT continuity/evidence/acceptance/cross-project coordinator. Owner forwards reports manually; one lead writer per shared work item.
- RevDev and PocketCode remain one PC-and-phone product direction with separate repos, roadmaps, clients, adapters, runtimes, security boundaries, acceptance suites and release gates. Share provider-neutral concepts only; never transfer acceptance evidence.

Verification at checkpoint start: branch HEAD 4446135bf1345f37aa5d221d27c0eabbdbcef5c7; main 555840d8d83342513d9cd353d4d1522d46a5c82d; compare 820 ahead / 0 behind. PR #2 head eb8b7ea83cb0e8fe1880351276c485b761431791 and PR #3 head 0ddcc0bc97bac5d446aefedf3d71f99411bd841d remain OPEN/DRAFT. Branch-filtered Actions query returned zero runs; exact-head status/check-runs have no individual checks. Current branch CI is UNKNOWN, not PASS. No product code, tests, device state, schema, acceptance IDs, budget or runtime/provider decision changed.

Next task: owner runs only the read-only Pyodios sys.last_exc / sys.last_value Console probe in the existing successful session. Preserve exact-match summary.json; do not rerun, overwrite, restart, clear, GC or run the wrapper there. After device evidence, continue typed child/wrapper/termination/lifecycle provenance before any CASE-04 formatter change.


## 2026-11-06 — Task/evidence/recovery research decision

- Added `AI_COLLAB/POCKETCODE_TASK_EVIDENCE_RECOVERY_RESEARCH_20261106.md`, source-backed across mobile execution, competitors, event/task protocols, artifact provenance and durable local journaling.
- Recommended differentiation: provider-neutral task packets, boundary-aware host observations, durable attempt history, immutable receipts/artifacts, no-rerun recovery and user-mediated AI correction. Do not build another general phone Python IDE.
- Critical platform correction: iOS embedded Python cannot spawn subprocesses/multiprocessing/IPC. In-process return/exception must not be reported as child exit. Separate embedded, browser-worker, external-child and remote-supervisor evidence.
- CASE-04 remains INCOMPLETE/timed_out on trusted timeout. Reject precedence-only formatter change; generic `exit_code` cannot distinguish child, wrapper, forced termination, stale or contradictory evidence.
- Protocol correction: legacy ACP is archived; A2A v1.0.1 is current successor for agent-to-agent interoperability. MCP Tasks is a task-handle/status pattern. Neither replaces PocketCode identities or receipt ledger.
- SQLite is a candidate local journal, with explicit WAL/synchronous durability and target-device crash tests. It cannot make a remote side effect exactly-once; use outbox/idempotency/reconciliation.
- No runtime/provider, budget, canonical ID, product source, test, acceptance, PR or deployment decision changed. Owner Pyodios saved-exception probe remains NOT RUN; artifact preserved.
