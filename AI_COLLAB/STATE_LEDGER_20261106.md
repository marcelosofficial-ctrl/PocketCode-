# PocketCode state ledger — 2026-11-06

**Repository:** marcelosofficial-ctrl/PocketCode-  
**Branch:** pocketcode-ai-workflow-director-research-2026-10-28  
**Last verified before this checkpoint:** f545974e5d76c8282968c3a86ae69d22cad81343  
**Compare before this checkpoint:** 840 ahead / 0 behind main; merge base 555840d8d83342513d9cd353d4d1522d46a5c82d. Ahead count is branch-history divergence, not product progress. Fetch live refs before consequential work.

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
- OpenHands and Cline are pattern references, not frameworks to adopt wholesale. MCP Tasks may inform async tool-task status; the legacy Agent Communication Protocol (ACP) was archived 2025-08-27 and merged into A2A. Evaluate current A2A for agent-to-agent interoperability, not archived ACP. MCP/A2A task IDs do not replace PocketCode command/attempt identity or trusted receipts. Reject wildcard auto-approval.
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


## 2026-11-06 — Prototype integrity and static regression recovery

- Reviewed the live prototype/checker changes through HEAD `c22d8108c9ceab3d003cfc92debbb99cd87e8a82`.
- The prototype remains simulation-only. Its displayed `main.py` is pinned to the canonical SHA-256 `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7` (1,939 bytes); initial CSV bytes are checked against the fixed success fixture.
- Red-team found malformed Python regex syntax in the first checker update and two test methods misplaced inside the `VALID_HTML` fixture. Corrected checker regexes, restored the canonical source guard in the fixture, moved tests into the class, and added roving-tabindex checks. Current checker/test blobs: `ec56e6084c4e0e6e8274734e259b12a17110ffb4` / `d22829c64235c2334561d7deb5b3110c7243ab4e`; 11 test methods.
- Focused Python assertions for canonical source length/hash and CSV extraction/equality passed. Full unittest suite, browser JS, clipboard, VoiceOver/TalkBack and mobile tests remain NOT RUN. Current exact-head CI status has zero checks and zero workflow runs, not PASS.
- EffectId wording corrected: same key/fingerprint permits lookup/reconciliation, not automatic replay. UNKNOWN forbids redispatch unless authoritative evidence or a documented provider idempotency contract permits it.
- No product runtime/provider, canonical acceptance ID, budget, PR, merge or deployment changed. Pyodios owner probe remains outstanding.


## 2026-11-06 — Prototype canonical-fixture alignment

- `prototypes/mobile-runner/index.html` now displays the frozen CSV-to-JSON task, exact canonical `main.py`, success and malformed-header examples, and explicit simulated-only receipt fields. No code runs and no artifact is created/downloaded.
- Embedded `main.py` was extracted and verified as 1,939 UTF-8 bytes with SHA-256 `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7`, matching the frozen worksheet/archive record. Initial `items.csv` success fixture is pinned with UTF-8/LF final newline.
- Static checker pins canonical source SHA and success input bytes; 11 regression test methods cover duplicate IDs, missing labels, fabricated timings, fake Run, tab relationships, prompt context, roving tabindex and fixture integrity.
- Local recreated 11-case Python harness passed 11/11; this was not execution of the exact repository test file or CI. Static checker passed against a reconstructed HTML fixture containing the exact pinned source/input. Real browser, screen reader, iOS and Android interaction remain NOT RUN.
- A checker indentation defect found during red-team review was corrected and read-back verified. The initial prototype remains simulation-only; no product runtime, provider, budget or acceptance ID changed.
- Pyodios saved-exception Console probe remains NOT RUN and is still the next owner action.


## 2026-11-06 — Fresh source maintenance gates

- Research note extended with Pyodide module-worker behavior, iOS app lifecycle constraints, SQLite WAL durability and WAL-reset bug, and MCP Tasks/A2A limitations.
- SQLite WAL selection is blocked until the bundled version is pinned at 3.51.3+ or supported backport (3.44.6 / 3.50.7), with the documented multi-connection write/checkpoint race tested. `synchronous=FULL` is required where power-loss durability is a requirement. WAL is not for network filesystems.
- MCP Tasks remain experimental (2025-11-25 spec); A2A v1.0.1 task streaming/history can omit updates/messages after disconnect. PocketCode's own receipt/event journal remains authoritative.
- Checker now accepts tab attributes regardless of class/id attribute ordering. Added a regression case for this. Test method count is 12; exact suite/CI not run.


## 2026-11-06 — Event history and provenance deepening

- Reviewed current OpenHands SDK EventLog/ConversationState implementation: one append chokepoint, parent-linked events, sequence assignment, cold-load projection rebuild, and explicit in-memory fallback when persistence is unconfigured. Reuse architecture pattern only; no durability/security guarantee inferred.
- Reviewed Cline task history and shadow Git checkpoint docs. Adopt source/input snapshot, compare/restore and interrupted-task UX ideas; explicitly keep checkpoints separate from execution receipts.
- Updated provenance references: in-toto Attestation v1.2 has predicate/statement/envelope/bundle separation; SLSA v1.2 is current and approved while v1.1 page is retired. Do not label unsigned receipts attestations or apply build provenance to arbitrary script execution.
- Research-only. No product runtime, provider, budget, canonical acceptance ID or schema changed.


## 2026-11-06 — Typed execution evidence and recovery contract

- Added AI_COLLAB/EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md, a design-stage contract for typed lifecycle/child/wrapper/embedded observations, verdict reconciliation, ambiguous dispatch, source-scoped event identity, receipt/artifact integrity and mobile lifecycle boundaries.
- Added isolated scripts/execution_projection.py and scripts/test_execution_projection.py. The helper is not integrated with report_contract.py or a trusted coordinator. Producer class strings are shape checks, not authentication.
- Local verification: 31 projection tests passed under CPython 3.13.5; both files compiled. GitHub exact read-back: source blob f32237c8c5ee5d62b0416b3dd867515ce567c21b; test blob cbd756cce1bc42a6aab0d5c48d8fac6f56cce7c1.
- Added research sections 13–17: official Python 3.14 mobile/WASM subprocess constraints; wrapper/signal/SystemExit distinctions; current OpenHands/Cline/Temporal release and licence metadata; provider-scoped idempotency versus transactional outbox; CloudEvents source-scoped IDs and OpenTelemetry dual timestamps; bounded code adoption and attestation limits.
- New source/design checkpoint commit: 3c6db063fe209396cab2d23b3f61c9daedd373ce. The following continuity checkpoint records the source commit and exact read-back. Fetch the live ref before further work.
- CASE-04 remains INCOMPLETE/timed_out on trusted timeout. scripts/report_contract.py remains unchanged. LOOP/CASE/D IDs, runtime/provider, storage, budget, canonical schema, PRs and deployment unchanged.
- PR #2/#3 remain untouched. No Actions, mobile, fake-adapter, persistence, provider, artifact-release, egress, crash or canonical acceptance tests were run by this source/design checkpoint.
- Pyodios artifact status remains owner-inspected exact oracle match; bridge root cause and native exit unknown. Next owner action is the previously supplied read-only sys.last_exc / sys.last_value Console probe. Preserve the project and do not rerun/overwrite it.


## 2026-11-06 — PC-2026-11-06-P24 — Dispatch reconciliation kernel started

- Began the next ranked gap after the typed exit projection: ambiguous provider acknowledgement and safe retry.
- Added local pure helper/test working copies for scripts/dispatch_reconciliation.py and scripts/test_dispatch_reconciliation.py. Actions are dispatch_first, adopt_existing, retry_same_attempt, poll_existing, hold_unknown, conflict and do_not_replay. The helper never generates new IDs, mutates durable state or sends requests.
- Bound lookups/idempotency capability to EffectId, DispatchAttemptId, request fingerprint, endpoint, account, provider, API version, region/zone scope, token (when present), retention and documented deduplication/mismatch behavior.
- Red-team found and fixed non-authoritative-found adoption and an unscoped authoritative-not-found retry. A provider token is optional for authoritative exact-lookup reconciliation but required for token-based replay.
- Local tests: 28/28 pass under CPython 3.13.5; both files compile. GitHub checkpoint commit 203628276e65909140bf4ed563071442c538548d created and read back: helper blob 2b0928002fdf690005711ea71f1a115a665490ef; tests blob f45eb831edb3cfdbcbf4284e3f81180eaee35f12. It is not a live adapter, outbox or exactly-once guarantee.
- Current project branch at the beginning of this slice was continuity commit 950387f766355825782072fdade057fe8caf5b8d. Earlier closeout compare was 842 ahead / 0 behind main, merge base 555840d83342513d9cd353d4d1522d46a5c82d. Exact-head Actions/check-runs were zero; aggregate status pending. PR #2/#3 remain open draft at original heads.
- Next: commit/read back the two helper files and contract/research updates, then build deterministic fake-store/outbox tests for crash points and fencing. Do not integrate with a provider or select storage yet.


## 2026-11-06 — P24 GitHub verification closeout

- Dispatch helper and 28-case test file are committed at 203628276e65909140bf4ed563071442c538548d and both were read back by exact Git blob SHA.
- Contract, research, start page, ledger and work log were also read back at the corresponding P24 checkpoint SHAs. P24 is no longer local-only.
- Exact-head verification: zero Actions runs, zero check-runs, combined commit status pending (no individual statuses). PR #2/#3 remain OPEN/DRAFT at original head SHAs eb8b7ea83cb0e8fe1880351276c485b761431791 and 0ddcc0bc97bac5d446aefedf3d71f99411bd841d.
- Branch compare at dispatch source commit: 843 ahead / 0 behind main, merge base 555840d8d83342513d9cd353d4d1522d46a5c82d. Ahead count is history divergence, not product progress.
- Next read first: this entrypoint, then EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md; inspect dispatch_reconciliation.py and its tests, then plan fake-store/outbox crash/fencing cases. Fetch live branch/PR/CI state before further edits.


## 2026-11-06 — P25 extended dispatch red-team

- Further correction: authoritative=True alone does not make not-found final. Eventual consistency or incomplete lookup coverage may hide an accepted/in-flight effect. The helper now requires separate absence_final=True before it may choose retry_same_attempt from a not-found response.
- Provider idempotency must be exact-operation/API-version scoped. Stripe API v1 and v2 semantics differ; AWS EC2 supports operation-specific token behavior with regional/zonal scopes. See research section 19.
- Latest helper/test Git objects: source 6760b3301e818956f71fdf02e369407e3b5cdaf7; tests f1949ebcfd525c5715af7fd9e022d5d35f8f1063 (33 test methods). They are not branch-durable until committed and read back.
- Local test execution of this expanded 33-case revision is NOT RUN in this pass. Previous 61/61 claim applies only to the earlier 30-case dispatch revision and must not be carried forward to this changed code.
- No runtime/provider/database selection, PR mutation, merge, deployment, budget or canonical ID change.


## 2026-11-06 — P25 malformed-input guard

- Added a string-type guard for ProviderLookup.outcome before set membership; malformed unhashable values now hold_unknown rather than raising TypeError.
- Added regression cases for non-string lookup outcome and non-string dispatch state. Latest test file contains 35 test methods. Execution NOT RUN for this latest revision.
- Latest helper/test blobs: 165d141bc6ab47ad9d19d1ba537ab0e3e39aa16d and e65968cc2162dca8eb75d446e10eec06c0ab9220. Branch checkpoint pending.
