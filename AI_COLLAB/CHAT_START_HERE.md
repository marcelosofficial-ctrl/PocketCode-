# PocketCode Chat Start Here

## Mandatory interruption-resistant working protocol (2026-11-06)

GitHub is the durable project state. Do not rely on a last-minute full-chat handoff. Every work pass must end with a user-visible result, even when a tool fails or CI remains pending.

- Fetch the live branch head once at the start. This entrypoint already directs new chats to fetch live state, so do not refresh its own head line after every docs commit.
- Load only task-specific source, tests and review packets. Avoid full goals-ledger downloads and repository-tree dumps unless a specific task requires them.
- Use bounded passes: one objective, one implementation/research increment, relevant tests and one checkpoint. Prefer a few meaningful operations over many tiny commits.
- Batch related documentation updates into one atomic multi-file commit when practical. Do not make separate entrypoint, status and worklog commits for one checkpoint.
- Check CI once after a reasonable interval. If pending, record run ID + exact SHA and return. Never poll indefinitely.
- Keep tool output compact: paths, blob/commit SHAs, relevant excerpts, test totals and failures. Avoid dumping entire large files.
- On write/tool failure, stop and re-fetch branch head and target blobs before deciding whether a write applied. Never blindly retry.
- At each checkpoint record implemented/tested/verified/not-run/blocked separately, the next action and exact source/test pins.
- If context appears near exhaustion, stop starting new engineering work, checkpoint immediately and tell the user to rotate chats using this entrypoint. Do not wait for a handoff request.
- Keep detailed evidence in topic-specific packets. The entrypoint should remain a short route map, not a duplicate of the whole project history.

**Response closure is mandatory:** never leave the user with tool narration only. Explain what changed, what did not change, verification scope, remaining unknowns and the next step.

**Important limitation:** this protocol reduces avoidable context pressure and tool stalls; it cannot prevent platform context limits, service outages or execution failures. The goal is graceful interruption with no lost project state.


**Last refreshed:** 2026-11-06 (mobile execution, competitor, recovery and protocol research incorporated)  
**Authority:** live PocketCode branch state plus canonical source/spec/test records. This file is the compact first-read entrypoint for every new PocketCode chat.

## Current cross-project note

Read [RevDev progress and multi-chat continuity update](CROSS_PROJECT_UPDATE_REVDEV_2026-11-06.md) for transferable engineering lessons and the current RevDev status. This does not transfer RevDev implementation or acceptance evidence into PocketCode. PocketCode's immediate active work is resolving the first owner-reported Pyodios Editor attempt, followed by the typed CASE-04 exit-provenance contract. Do not make a precedence-only formatter patch.

## Latest research decision (2026-11-06)

Read [PocketCode task, evidence and recovery research](POCKETCODE_TASK_EVIDENCE_RECOVERY_RESEARCH_20261106.md). Key correction: iOS embedded Python has no child process, so do not fabricate child exit codes. CASE-04 is not a precedence patch; resolve typed child/wrapper/termination provenance first. PocketCode's differentiator is portable task/evidence/recovery/AI-correction orchestration, not another phone Python IDE. No runtime/provider selected.

## First action

Read this file, verify the live branch/PR/CI state, and fetch only the linked task-specific evidence. Continue the active work. Do not restart discovery or ask the owner to reconstruct a prior chat.

## Repository and branch

- Repo: https://github.com/marcelosofficial-ctrl/PocketCode-
- Branch: `pocketcode-ai-workflow-director-research-2026-10-28`
- Historical pre-checkpoint snapshot: `e7abaabff55f3bc25a793f2e814852d8e7aa246d` (807 ahead / 0 behind at that earlier time). This is not current. Fetch live refs before consequential work; ahead count is branch-history divergence, not product progress.
- Open PR #2: [Add chat checkpoints and harden report-contract regressions](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/2), OPEN/DRAFT from branch `chat-continuity-report-regressions-2026-10-26`.
- Open PR #3: [Draft: Add evidence-led PocketCode research baseline](https://github.com/marcelosofficial-ctrl/PocketCode-/pull/3), OPEN/DRAFT from branch `pocketcode-pass0-audit-2026-10-26`.
- PR #2/#3 are not this active research branch and were not modified. Do not infer the active branch's commits are included in either PR.

## Product direction and current phase

PocketCode remains a phone-first Agentic Orchestration Control Plane for iOS and Android. It is the phone counterpart in a broader PC-and-phone product direction with RevDev, but it remains a separate repository, roadmap, client, adapters, runtime, security boundary, acceptance suite and release gate.

**Phase:** Discovery / product definition. The principal differentiator is not another generic local Python IDE. It is a provider-neutral task/evidence/recovery/AI-correction workflow with truthful execution receipts, resumable attempts and safe user-mediated correction.

No real execution backend, runner, provider, cloud host, or sandbox has been selected. The UI prototype is simulated. A full end-to-end PocketCode run has not been demonstrated.

Boundary policy: project boundaries are revisable when evidence shows a benefit. Do not preserve temporary safeguards as permanent restrictions. Record any revised authority, risks and verification controls. The $0 default budget remains unless separately changed.

## Owner constraints and boundaries

- $0 default budget. No paid provider, host, service, account, workload or subscription without a separate budget decision.
- Phone-first; no owner-PC dependency for the PocketCode product.
- Preserve explicit user paste-to-context. No clipboard polling or intrusive overlays.
- SSH/Tailscale and optional cloud execution remain adapters/research directions.
- Local WASM/Pyodide/JSC may be convenience execution for suitable trusted/light tasks, not assumed hostile-code containment. Stock Pyodide is not approved as a hostile-code sandbox.
- Preserve separation between command/dispatch, execution, observations, immutable receipt, artifacts, cleanup state and AI correction lineage.
- Unknown/degraded evidence must not be converted into product PASS/FAIL.
- Do not treat RevDev evidence, source, or acceptance verdicts as PocketCode proof.

## Canonical suites and evidence status

PocketCode canonical LOOP/CASE/D suites remain unchanged. Preserve their IDs, expected text and semantics exactly. The current report-contract issue is a typed-provenance problem, not a safe precedence-only fix. The 2026-11-05 `VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md` explicitly says not to patch `classify_verdict()` until generic `exit_code` is distinguished as child exit versus wrapper, forced-termination, stale or contradictory evidence. Preserve canonical CASE-04 as INCOMPLETE/timed_out. Also retain degraded collector/teardown semantics and synchronous pre-execution network-isolation barrier as open concerns.

Current device comparison:
- Pyodios is reported by the owner as installed on the iPhone.
- A fixed-task device baseline/protocol and exact fixture archive have been prepared.
- Fixture archive SHA-256: `706c6a87d07c496d5a461c9395fb0b967b961fa9c430c719d9799998df5b4099`.
- The embedded `main.py` matches canonical source SHA-256 `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7`.
- One owner-reported Editor attempt displayed only `[Bridge/executePython] PythonError`. The owner later inspected the existing `summary.json` and confirmed it exactly matches the canonical success oracle. Current classification: ARTIFACT-LEVEL FUNCTIONAL SUCCESS / BRIDGE ERROR UNRESOLVED / FULL RUN INCONCLUSIVE. Native process exit status and root cause remain UNKNOWN. Preserve the artifact; do not rerun or overwrite the success project.

## Current priority order

1. Preserve the exact-match `summary.json`. The owner already checked **More → Settings → Error Log → View Error Log**; only `Editor: PythonError` appeared, without traceback. Next run only the read-only `sys.last_exc` / `sys.last_value` Console probe in the existing session. Do not rerun, overwrite, restart, clear or reset the success project. See `PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md`.
2. Resolve typed child-exit / wrapper-exit / termination / lifecycle projection before changing `scripts/report_contract.py`; preserve CASE-04 INCOMPLETE/timed_out and all existing IDs.
3. Audit degraded observation collection, teardown, artifact integrity/release and cleanup semantics separately from execution outcome.
4. Source-audit the synchronous pre-execution network-isolation barrier for exact ordering and fail-closed behavior.
5. After the first device path is understood, complete malformed-input, export/read-back and normal-relaunch checks; compare only one free alternative if it adds decision value.

## Roles

- Claude: lead developer and architecture/implementation reviewer.
- Gemini: co-developer and independent security/spec auditor.
- ChatGPT: continuity holder, evidence reconciler, acceptance architect, cross-project coordinator.
- Owner forwards reviewer work manually. Do not claim direct AI-to-AI communication.

## Canonical detailed records

- Current state ledger: [AI_COLLAB/STATE_LEDGER_20261106.md](STATE_LEDGER_20261106.md)
- Latest full handoff and copy/paste bootstrap prompt: [AI_COLLAB/NEW_CHAT_HANDOFF_20261106.md](NEW_CHAT_HANDOFF_20261106.md)
- Pyodios bridge diagnostic: [AI_COLLAB/PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md](PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md)
- Current project status/history: [PROJECT_STATUS.md](../PROJECT_STATUS.md)
- Fixed-task worksheet and interruption/reconnect protocol: retrieve from the repository's existing evaluation/acceptance records; do not create a new fixture or redefine the task.
- Pyodios device baseline/protocol: [PYODIOS_DEVICE_BASELINE_AND_HANDS_ON_PROTOCOL_20261106.md](PYODIOS_DEVICE_BASELINE_AND_HANDS_ON_PROTOCOL_20261106.md)
- Remote agent and workflow protocol research: [Remote Agent Control Plane and Workflow Protocol Research](../RESEARCH/REMOTE_AGENT_CONTROL_PLANE_AND_WORKFLOW_PROTOCOL_RESEARCH_20261105.md)
- Execution readiness/competitor audit: [Remote Execution, Event Recovery and Scheduler Competitor Audit](../RESEARCH/REMOTE_EXECUTION_EVENT_RECOVERY_AND_SCHEDULER_COMPETITOR_AUDIT_20261105.md)

## Continuity protocol

Read [CHAT_CONTINUITY_AND_MULTI_CHAT_OPERATING_PROTOCOL_20261106.md](CHAT_CONTINUITY_AND_MULTI_CHAT_OPERATING_PROTOCOL_20261106.md) and [CHAT_WORK_LOG.md](CHAT_WORK_LOG.md).

A new conversation is a replaceable worker. Checkpoint after two or three meaningful passes or any important source/test/review/decision event. Keep this page current and append the work log before context exhaustion.

## Bootstrap prompt

```text
Continue PocketCode from GitHub. Read AI_COLLAB/CHAT_START_HERE.md on branch pocketcode-ai-workflow-director-research-2026-10-28, verify live branch/PR/CI state, and continue the highest-value bounded task. GitHub is the source of truth, not this chat's memory. Do not restart discovery or ask me to recreate context. Implement and test where the environment permits; be explicit about evidence status. Update CHAT_START_HERE.md and append CHAT_WORK_LOG.md after meaningful work so this conversation can be replaced safely. Keep PocketCode separate from RevDev, preserve canonical LOOP/CASE/D suites, and keep the default budget at $0.
```


## 2026-11-06 cross-project continuity and workflow improvements

The owner is coordinating work across months and potentially hundreds of ChatGPT conversations. PocketCode must remain resumable without asking an almost-full chat to create a giant handoff.

Use the same continuity method now used by RevDev, but keep all PocketCode product work independent:
- GitHub is durable memory; each chat is a replaceable worker.
- Start with this file, re-fetch the live branch/PR/CI state, then read only task-specific source/evidence.
- Checkpoint every two or three meaningful passes, and immediately after important code/test/review/decision events.
- Append the work log and update this entrypoint as soon as active status or next action changes. Never wait for a context-full warning.
- Keep one lead writer per branch/work item. Other AIs can review read-only or work on disjoint files.
- For several related files, prefer one Git Data API blob/tree/commit with an expected-head ref lease, followed by exact read-back. This avoids intermediate partially updated states and unnecessary CI runs.
- On tool/script failure, re-fetch the confirmed GitHub state, determine whether the attempted mutation occurred, recover and close the response. Never silently stop or claim an unverified write/test.
- ChatGPT may lead a bounded implementation task when source/tools are available; Claude and Gemini remain scoped independent reviewers/co-developers. Owner forwards their reports manually.

RevDev-only update (context, not PocketCode implementation): the Windows PowerShell 5.1 Actions workflow was located through the push-triggered Actions API. Run #10 failed 13/14 because a static test expected an obsolete helper name; a source ordering defect was also fixed. Updated source/test runs #11/#12 were IN_PROGRESS at the last poll. This demonstrates why actual workflow runs must be queried rather than inferred from an incomplete connector status view. Do not copy RevDev publisher source, schemas, P8U/AWC/P0-D acceptance or verdicts into PocketCode.

PocketCode remains on its own priority: CASE-04 timeout classification and report-contract integrity in `scripts/report_contract.py`, then degraded collector/teardown semantics and the synchronous pre-execution network isolation barrier. No runtime/provider is selected, the device comparison is still awaiting owner observations, and the $0 default budget remains.

## Streaming interruption recovery

If a long response is interrupted, resume from this entrypoint and live GitHub state. The continuity protocol now has an explicit recovery sequence: re-fetch branch/file state before replaying writes, verify commits/read-back, inspect CI by exact head SHA, and report the last confirmed checkpoint. The assistant cannot diagnose or repair the ChatGPT iOS stream itself. Do not assume a missing final response means GitHub changes failed or succeeded. This is process-only and does not change PocketCode product architecture or acceptance.

## 2026-11-06 — Final cross-project CI process update (RevDev only)

RevDev's typed GitHub HTTP parser and publisher preflight source increment is now CI-verified: GitHub Actions run #17 completed **24/24** Windows PowerShell 5.1 / Pester 5.7.1 tests at commit `c559aa7db595cb890981544184807381991e7490`: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42132258538. This supersedes the prior run #13 15/15 status and the #17 pending note. Test scope is RevDev's tracked maintenance source/parser/static fixtures only, not live GitHub networking, installed product, P0 or canonical P8U/P0-D acceptance.

PocketCode should reuse only the CI-discovery and checkpoint lessons: query actual repository Actions runs/jobs/logs at the exact head SHA when a partial connector status view hides push runs; update the live entrypoint/work log with the verified result; keep implementation and acceptance evidence separate. Do not adopt RevDev source, schemas, or test results.

PocketCode's next product work remains CASE-04 timeout classification and report-contract correction in `scripts/report_contract.py`, followed by degraded collector/teardown semantics and synchronous pre-execution network isolation. Keep the $0 budget, phone-first model, explicit paste-to-context, no runtime/provider decision, owner-observation device test status, and separate LOOP/CASE/D contracts unchanged.


## 2026-11-06 — RevDev fake-process test method (process lesson only, CI pending)

RevDev has moved beyond parser-only tests by extracting its `gh` transport into a module and invoking it with a temporary fake Windows `.cmd` child process. The harness covers 200 JSON, 404 with nonzero exit, 429 with Retry-After headers, stderr-only failure and HTTP 200 with nonzero process exit. 
PocketCode process lesson: apply deterministic fake adapters at PocketCode's own execution/provider boundary. Exercise timeout, cancellation, collector failure, partial output, teardown failure and cleanup without network or real execution side effects. This must preserve PocketCode's separate CASE/LOOP/D contracts. CASE-04 timeout/report-contract remains the immediate PocketCode-specific correction. No RevDev implementation or acceptance is imported.


## 2026-11-06 — RevDev fake-process test result (process lesson only)

RevDev run #21 (`42133707971`) has now completed successfully: **34/34 passed, 0 failed, 0 skipped**, Windows PowerShell 5.1 / Pester 5.7.1, exact test commit `65d9b95ed346c42ed22bd920d70cb4e5c4429a26`. Exact run: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42133707971. This is RevDev-only test evidence. PocketCode may reuse the method of deterministic fake adapters/processes for timeout, cancellation, partial output, collector and teardown degradation, but must preserve its own CASE/LOOP/D acceptance and no-runtime-selection decision. CASE-04 remains PocketCode's next implementation task.


## 2026-11-06 — RevDev CI scoping regression and continuity lesson

After the successful RevDev process-harness run #21 (34/34 at `65d9b95ed346c42ed22bd920d70cb4e5c4429a26`), the next hardening pass added a fail-closed missing-executable check and unknown-exit handling. Windows CI then exposed a PowerShell module-scope issue: native child-process completion updates the global automatic variable `$LASTEXITCODE`, while a function-local sentinel can shadow it. The correction now sets/reads/restores `$global:LASTEXITCODE`, and a test asserts that the caller's prior global value is restored. Exact correction commits: transport `94b552a56653a18504ee0291152634a7dabdda02`, test `264692600e589c4a8fd3198e1ab930da80e5b4f0`. Runs #26/#27 were pending/in progress at last observation. Re-fetch before quoting a result; do not treat run #21's 34/34 as validation of these later changes.

**Transferable workflow lesson:** keep test evidence pinned to exact commit SHA, read the job logs for failures, and distinguish old-green from current-head-green. A new test that catches a real boundary defect is useful progress, even when the first CI run fails. Record the regression, exact fix, and current verification status in GitHub before rotating chats. Avoid silent stops: finish each pass with a durable checkpoint, explicit NOT RUN/BLOCKED/IN_PROGRESS status, and a concise user-facing summary.

PocketCode remains independent. Reuse only this testing/continuity method, not RevDev's PowerShell implementation or acceptance evidence. CASE-04 remains the immediate PocketCode task.


## 2026-11-06 — RevDev latest CI and fail-closed 404 classification (method only)

RevDev run #29 completed SUCCESS with **36/36** tests at exact source/test commit 5c0435d6e9412f3a1dc72410be6495a61acaeceb, Windows PowerShell 5.1 / Pester 5.7.1: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42135733497. This verified the native process harness and correct preservation/removal of the global LASTEXITCODE variable.

RevDev then tightened immutable mission-path absence classification. It now requires gh's documented general failure exit code 1, a complete parse-clean HTTP 404 and JSON message Not Found; authentication exit 4 and cancellation exit 2 cannot be mistaken for absence. This follows the official gh exit-code reference: https://cli.github.com/manual/gh_help_exit-codes. Current RevDev commit 144d0aa361343277aed9af76ad5736969c29abc9 contains 42 Pester cases; Actions run #30 42136315313 was IN_PROGRESS at last observation. Re-fetch before quoting its outcome.

PocketCode may reuse the fail-closed classification/testing principle only at its own boundary. No RevDev code or acceptance transfers. PocketCode remains separate, CASE-04 remains next, and runtime/provider selection remains open.


## 2026-11-06 — RevDev 404 classifier CI correction (method only)

RevDev run #30 at commit 144d0aa361343277aed9af76ad5736969c29abc9 completed **41 passed / 1 failed**. The failure was a stale static test locator still searching for the removed `$existing.HttpStatus -ne 404` expression, not a classifier test failure. The guard was updated to locate `Test-GhApiConfirmedNotFound -Response $existing`; two more tests now cover invalid JSON and a 404 body without the expected message field. Current RevDev source/test commit is 5a18ba76860be7ab466fc0fe6b43ebd3aa0349c6 with 44 Pester cases; run #31 42136717748 was in progress at last observation. Re-fetch before quoting its outcome.

This is a process lesson only: static guards must assert behavior through the current abstraction boundary, not stale source text. PocketCode should use semantic contract tests and avoid brittle checks against implementation spelling. No RevDev code or test evidence transfers to PocketCode.


## 2026-11-06 — RevDev R5 recovery expansion and no-silent-stop protocol

This is a cross-project progress/process update only. PocketCode remains a separate product, codebase, runtime, security boundary, roadmap and acceptance suite. Do not import RevDev PowerShell code, test counts or acceptance conclusions.

RevDev's current branch has advanced beyond the previous transport-only work. Latest observed branch head: `e00e20d44f240b24faa769f558c9d61b99bdffb1`. The immediately preceding source checkpoint `40a8698060b50b3a94f946fe443caf201fd0f168` adds:
- Atomic create-only local result persistence and strict discovery. Only one validated matching result is accepted; multiple candidates are AMBIGUOUS; malformed, partial or unreadable discovery is DISCOVERY_INCOMPLETE. No newest-timestamp heuristic.
- Runner writes `queue-result.json` atomically and exposes SHA-256; watcher forwards the expected digest.
- Publisher verifies the local bytes/digest and binds the requested Project/Mission to the identity inside the result before any GitHub request.
- Typed process + HTTP response handling, exact remote prepared-envelope byte readback, and stricter 404 absence proof.
- Recovery quarantine uses GUID destinations, avoids `Move-Item -Force`, and writes metadata atomically. Partial failure reports the destination because the source may already have moved.
- Fake native process harness tests stdout/stderr, HTTP 200/404/429, process exit/status conflicts, missing executable, and PowerShell 5.1 LASTEXITCODE lifecycle.

At source checkpoint `40a8698060b50b3a94f946fe443caf201fd0f168`, the test target is 59 publisher tests + 22 local-result/quarantine tests = 81. Run #42 `42180012296` targets that exact source commit and was still in progress during Pester installation at last observation. Current branch head has a docs-only follow-up commit; re-fetch exact run state before quoting a result. Prior run #37 passed 73/73 at an earlier revision only. Do not call the current 81 tests green until run #42 finishes.

**Transferable PocketCode lessons:**
1. Keep CI evidence exact-SHA scoped. An older green run never validates a later commit.
2. Query repository Actions runs, match workflow path, branch, event and SHA, inspect jobs and retrieve logs for actual test counts. Do not rely on incomplete PR-only summaries.
3. Test real process boundaries with controlled fake executables/adapters where applicable, without live network or writes.
4. Prefer semantic contract assertions over brittle static string checks; when an abstraction moves, update the guard to test the new boundary.
5. Treat ambiguity as UNKNOWN/INCOMPLETE, never as absence or success. This principle is portable; implementation details are not.
6. A failing test is evidence. Trace it to source/fixture/contract, preserve the finding, fix only after confirming the intended behavior.
7. If a tool call fails or a chat appears to stop, recover from the last confirmed GitHub state and close the pass with a user-visible status. Never silently stop.

**Chat lifecycle:** GitHub is durable memory and each chat is a replaceable worker. Do not wait for a maximum-context warning or a huge final handoff. Every 2–3 meaningful passes, or after any meaningful source/test/review/decision event, append the project work log and refresh the start page with branch head, exact pins, CI status, next action and unresolved risks. Rotate chats while context remains. New chats should read the start page, fetch live branch/PR/CI state, then read only task-specific canonical docs. Keep one lead writer per repo/branch/work item; parallelize independent read/review tasks, serialize writes to shared paths, re-fetch before writing and read back after. A multi-file Git tree commit with expected-head protection is preferred where available.

**PocketCode priority unchanged:** continue CASE-04 timeout/report-contract integrity in `scripts/report_contract.py`; preserve LOOP/CASE/D IDs and meanings; device comparison awaits owner observations; $0 budget, phone-first, no PC requirement, explicit paste-to-context and no clipboard polling/overlays remain. Do not change architecture or select a runtime based on RevDev work. PR #2/#3 remain untouched.


## 2026-11-06 — RevDev recovery suite CI closeout (method only)

RevDev run #42 `42180012296` completed **81 passed, 0 failed, 0 skipped** on Windows PowerShell 5.1 / Pester 5.7.1 at exact source/test commit `40a8698060b50b3a94f946fe443caf201fd0f168`. Run: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42180012296. It covers 59 publisher identity/transport cases plus 22 local-result/recovery/quarantine cases. This is maintenance-source CI evidence only, not live network/queue/watcher/mission execution, installed-PC parity, or P0/P8U acceptance. The RevDev branch has docs-only commits after the tested source SHA.

PocketCode must continue its own CASE-04 timeout/report-contract work. No RevDev implementation, test count, or acceptance transfers. Reusable method: exact-SHA CI, fake process boundaries, semantic contract assertions, explicit UNKNOWN/INCOMPLETE outcomes, review partial-failure paths, and update GitHub before rotating chats.


**Latest Pyodios result (2026-11-06):** the owner confirmed the existing `summary.json` exactly matches the fixed success oracle despite the Editor showing `[Bridge/executePython] PythonError`. The Error Log was checked and contained only `Editor: PythonError`, no traceback. Classification: artifact-level functional success, bridge error unresolved, full run inconclusive. Preserve the success project. Next run only the read-only saved-exception probe in the existing session. See `PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md`, `STATE_LEDGER_20261106.md` and `NEW_CHAT_HANDOFF_20261106.md`.

**Latest Pyodios diagnostic:** Error Log inspection yielded only `Editor: PythonError`, no traceback. Root cause remains unknown. Next use the read-only `sys.last_exc` / `sys.last_value` Console probe. Preserve the exact-match success artifact and do not rerun the canonical task. See the triage note and 2026-11-06 handoff.


## 2026-11-06 — RevDev installer-aware recovery update (method only)

RevDev run #48 42181302862 passed **91/91** at exact source/test SHA 935108a6937f15b76f75850ebdbe70c69000be32 under Windows PowerShell 5.1 / Pester 5.7.1: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42181302862. The suite covers publisher/transport, local-result recovery/quarantine, and installer dependency/source-pin checks. The clean installer was not executed; no PC, live API, queue or mission was touched.

A follow-up source review found the install marker itself was not rolled back. RevDev added backup/restore/removal logic and two tests. Current RevDev source SHA a6defbb0e8b0902e8ecc20777d0a10dc25ae344b, 93 authored tests, run #49 42182731390 IN_PROGRESS at last check. Do not call the latest 93-case revision green until the exact run completes. This is a method-only update, not PocketCode code or acceptance evidence.

PocketCode's own immediate priority remains CASE-04 timeout/report-contract evidence provenance, with the Pyodios PythonError attempt preserved as artifact-level functional success / bridge error unresolved / full run inconclusive. Do not rerun or overwrite the preserved success project.


## 2026-11-06 — RevDev latest CI closeout (method only)

RevDev run #49 `42182731390` passed **93/93** at exact source/test SHA `a6defbb0e8b0902e8ecc20777d0a10dc25ae344b`, Windows PowerShell 5.1 / Pester 5.7.1: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42182731390. It adds two tests for rollback of the R5 installation marker on top of the previous 91-case installer-aware suite. No installer or PC/live runtime operation occurred. This is RevDev-only source/test evidence. PocketCode remains on its independent CASE-04 and Pyodios diagnostic track.


## 2026-11-06 — Cross-project continuity method update

Owner explicitly requested that PocketCode adopt the improved multi-chat operating method. Read [RevDev continuity update for PocketCode](REVDEV_CONTINUITY_UPDATE_20261106.md) before the next substantial pass. GitHub is durable project memory; each chat is a replaceable worker. Checkpoint every 2–3 meaningful passes or after source/test/review/decision events, keep this entrypoint current, append the work log and rotate before context exhaustion. The forwardable note includes a complete copy/paste instruction for a new PocketCode chat and method-only RevDev lessons. No RevDev code, architecture, runtime, acceptance or security decision transfers.

RevDev run #49 passed 93/93 at exact SHA `a6defbb0e8b0902e8ecc20777d0a10dc25ae344b` (Windows PowerShell 5.1 / Pester 5.7.1): https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42182731390. This is RevDev-only method evidence. PocketCode priorities remain CASE-04 provenance and the read-only Pyodios saved-exception probe. Preserve the exact-match success artifact; do not rerun/overwrite. PR #2/#3 remain untouched.


## Bounded work, operation identity and interruption recovery

Each pass has one objective, bounded scope, expected result, evidence requirements and stopping condition. Prefer completing a useful vertical slice over opening many unfinished tasks. Batch independent read-only work in modest groups; serialize dependent reads and shared writes. Keep outputs compact. For mutations, preserve stable EffectId across retries, a fresh AttemptId per actual attempt, exact input/argument hashes, dependencies and authorization scope. Maintain durable operation history, per-operation progress/evidence, heartbeats/leases, fencing, bounded retries and exact reconciliation of ambiguous external effects. Never replay a possibly completed mutation before re-fetching and reconciling live state. Keep execution outcome, observation/collection, lifecycle disposition, cleanup, publication and acceptance distinct. Checkpoint every 2–3 meaningful passes and immediately after consequential implementation, tests, reviews, CI or decisions. Rotate chats before context becomes unhealthy. Operation count is not completion: completion requires receiving, interpreting and verifying the outcome. These are working-method controls, not changes to PocketCode product identity or acceptance contracts.
