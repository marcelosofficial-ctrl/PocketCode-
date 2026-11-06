# PocketCode Chat Start Here

**Last refreshed:** 2026-11-06 (final cross-project CI update)  
**Authority:** live PocketCode branch state plus canonical source/spec/test records. This file is the compact first-read entrypoint for every new PocketCode chat.

## First action

Read this file, verify the live branch/PR/CI state, and fetch only the linked task-specific evidence. Continue the active work. Do not restart discovery or ask the owner to reconstruct a prior chat.

## Repository and branch

- Repo: https://github.com/marcelosofficial-ctrl/PocketCode-
- Branch: `pocketcode-ai-workflow-director-research-2026-10-28`
- Last observed pre-entrypoint-refresh snapshot 2026-11-06: **738 ahead / 0 behind** main; branch head `3cfa3b7f75facb34ab86e2286be2b36a15fff443`; merge base `555840d8d83342513d9cd353d4d1522d46a5c82d`. Re-fetch before consequential work. Ahead count is branch-history divergence, not product progress.
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

PocketCode canonical LOOP/CASE/D suites remain unchanged. Preserve their IDs, expected text and semantics exactly. The current PocketCode-specific report-contract issue remains important: `classify_verdict()` currently checks nonzero exit before trusted lifecycle `timed_out`, while canonical CASE-04 requires timeout to be represented as INCOMPLETE/timed_out. The timeout test also needs the required evidence. Other known audit concerns include degraded collectors/teardown being conflated with execution verdicts and the need for a synchronous pre-execution network-isolation barrier.

Current device comparison:
- Pyodios is reported by the owner as installed on the iPhone.
- A fixed-task device baseline/protocol and exact fixture archive have been prepared.
- Fixture archive SHA-256: `706c6a87d07c496d5a461c9395fb0b967b961fa9c430c719d9799998df5b4099`.
- The embedded `main.py` matches canonical source SHA-256 `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7`.
- The owner/device comparison is AWAITING OWNER OBSERVATIONS; ChatGPT did not perform device execution. Do not claim a device test or runtime verdict.

## Current priority order

1. Re-fetch and inspect `scripts/report_contract.py` and its tests. Correct the trusted lifecycle/timeout classification ordering and add an exact CASE-04 regression without changing canonical wording.
2. Audit degraded collection, teardown, artifact and cleanup semantics so process execution facts remain distinct from report verdict.
3. Preserve the synchronous pre-execution network-isolation barrier; source-audit exact ordering and failure behavior.
4. Continue the Pyodios hands-on comparison only from owner-supplied observations, and keep documented product claims distinct from device-verified facts.
5. Narrow future work to one real vertical slice after the fixed-task comparison. Avoid broad competitor research unless it changes a concrete decision.

## Roles

- Claude: lead developer and architecture/implementation reviewer.
- Gemini: co-developer and independent security/spec auditor.
- ChatGPT: continuity holder, evidence reconciler, acceptance architect, cross-project coordinator.
- Owner forwards reviewer work manually. Do not claim direct AI-to-AI communication.

## Canonical detailed records

- Latest full handoff: [AI_COLLAB/NEW_CHAT_HANDOFF_20261105.md](NEW_CHAT_HANDOFF_20261105.md)
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
