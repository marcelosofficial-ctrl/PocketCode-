# PocketCode Chat Work Log

Append-only continuity ledger. Keep entries concise; detailed evidence remains in canonical records.

## 2026-11-06 — PC-2026-11-06-P01 — Multi-chat continuity system

**Purpose:** make PocketCode resumable across hundreds of temporary chats without requiring an end-of-context handoff.

**Completed:**
- Adopted GitHub as durable project memory and chats as replaceable workers.
- Added a compact live entrypoint, reusable operating protocol, and append-only work log.
- Reconciled live branch compare: 710 ahead / 0 behind main; merge base `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- Rechecked open PRs #2 and #3; both remain OPEN and unchanged.
- Recorded OpenAI's current context-full explanation: user and assistant messages consume current conversation context; no fixed message count.

**Changed paths:**
- `AI_COLLAB/CHAT_START_HERE.md`
- `AI_COLLAB/CHAT_CONTINUITY_AND_MULTI_CHAT_OPERATING_PROTOCOL_20261106.md`
- `AI_COLLAB/CHAT_WORK_LOG.md`
- `PROJECT_STATUS.md`
- `AI_COLLAB/NEW_CHAT_HANDOFF_20261105.md`

**Verification:** GitHub file writes/read-backs to follow. No PocketCode execution, device tests, fixed-task comparison or runtime/provider decision was performed by this continuity update.

**Next:** inspect `scripts/report_contract.py` and exact tests for CASE-04; continue Pyodios device comparison only from owner-supplied observations.


### 2026-11-06 — post-write branch recheck

After all continuity files and status/handoff updates were committed, live compare reported PocketCode at **715 ahead / 0 behind** main. Merge base unchanged. The earlier 710 count above was the pre-update snapshot. Ahead count is branch-history divergence, not product progress.


## 2026-11-06 — PC-2026-11-06-P02 — Cross-project continuity improvements

**Purpose:** make PocketCode work smoother across hundreds of future chats while keeping the product boundary independent from RevDev.

**Updates:**
- Clarified that the live entrypoint and append-only work log replace giant end-of-context transcripts.
- Added checkpoint cadence of two or three meaningful passes and rotation before context exhaustion.
- Adopted a single-commit multi-file checkpoint using Git Data API blobs/tree/commit and an expected-head ref lease, followed by exact read-back. Use Contents API for single-file edits.
- Added tool-failure recovery: inspect confirmed GitHub state before deciding whether a write happened; recover and report rather than silently stopping.
- Clarified that ChatGPT may lead bounded implementation when tools/source are available; Claude and Gemini provide scoped independent review/co-development. One lead writer per branch/work item.
- Recorded the RevDev CI discovery only as a continuity/process lesson. No RevDev publisher implementation, acceptance suites, schemas or test verdicts are adopted into PocketCode.

**PocketCode next task:** continue the PocketCode-specific CASE-04 timeout/report-contract correction, then audit degraded collection/teardown and the synchronous pre-execution network-isolation barrier.

**Verification:** this documentation batch is committed in one Git tree checkpoint and read back. No PocketCode code, device test, runtime/provider selection, workload, CI or PR change is part of this process update. PR #2/#3 remain untouched.


## 2026-11-06 — PC-2026-11-06-P03 — RevDev CI process lesson corrected

**Purpose:** keep PocketCode's live continuation page aligned with the completed cross-project workflow research while preserving separate product evidence.

**Update:** RevDev's push-triggered Windows PowerShell 5.1 workflow was found through the repository Actions runs API. After source/test corrections, run #13 passed 15/15 on Pester 5.7.1 at commit `77fc32587d61f086bbcaafd479b52dd85e091629`: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42130948334. This supersedes the earlier in-progress observation recorded at the time of PC-P02. The process lesson is to inspect actual workflow runs/jobs/logs by head SHA when a connector status view is partial.

**PocketCode impact:** process-only. No RevDev publisher implementation, schema, P8U/AWC/P0-D contract or verdict has been imported. PocketCode remains prioritizing CASE-04 in `scripts/report_contract.py`; no runtime/provider selection, device test, product code or PR change occurred.

**Live branch snapshot:** PocketCode 723 ahead / 0 behind main; RevDev 732 ahead / 0 behind. These are history divergence counts, not product progress. PR #2/#3 and RevDev PR #1 remain open drafts and untouched.

## 2026-11-06 — PC-2026-11-06-P03 — Streaming interruption resilience

Owner reports recurring iOS “Streaming interrupted. Waiting for complete message” during longer, higher-thinking project turns. Root cause is UNKNOWN; the assistant cannot inspect client transport/generation logs. The current OpenAI status page reports a ChatGPT Work and Dots incident under monitoring, but that is not evidence it caused this ChatGPT interruption. OpenAI Help Center guidance recommends status checks, trying a new chat/restarting, switching networks/devices and collecting timestamps/request IDs for Support if persistent.

**Process changes:** added explicit interrupted-response recovery to PocketCode's continuity protocol. Re-fetch live GitHub head/files before replaying any write; treat missing user-visible tool output as ambiguous; verify commits/read-back; query CI by exact SHA; keep write batches bounded and operate on one repository at a time. This is process-only. PocketCode's CASE-04, phone-first product, security boundaries, no-runtime-selected status and $0 budget remain unchanged.

**Next PocketCode task:** resume the existing PocketCode-specific CASE-04 timeout/report-contract correction. Do not adopt RevDev publisher code or test suites.

## 2026-11-06 — PC-2026-11-06-P04 — RevDev CI lesson final result

RevDev's current typed HTTP parser/publisher preflight source passed GitHub Actions run #17: 24 tests discovered, **24 passed, 0 failed**, Windows PowerShell 5.1 / Pester 5.7.1, head `c559aa7db595cb890981544184807381991e7490`. URL: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42132258538. This supersedes the earlier pending #17 observation and prior #13 15/15 result. The result is RevDev-only test evidence. PocketCode reuses only the process lesson to query workflow runs/jobs/logs at exact head SHA when connector status is partial.

PocketCode implementation was not changed by this cross-project status update. Its next exact task remains CASE-04 in `scripts/report_contract.py`; inspect existing tests and evidence first, correct the timeout verdict ordering, add tests for timed-out + nonzero exit and degraded collector/teardown outcomes, then run the repo's actual CI. Preserve all canonical LOOP/CASE/D strings and separate project boundaries.


## 2026-11-06 — PC-2026-11-06-P06 — Cross-project fake-process testing lesson

RevDev's transport harness now invokes a real child-process boundary through a controlled fake `.cmd` executable, testing HTTP status/body, native exit code, stdout/stderr and rate-limit headers. 
PocketCode can reuse the test technique, not the code: place its own provider/execution boundary behind injectable adapters and deterministically test timeout, cancellation, partial output, collector degradation, teardown failure and cleanup. Do not select a runtime/provider or claim product acceptance from these RevDev tests. PocketCode's CASE-04 remains its own next implementation task; device comparison remains awaiting owner observations.


## 2026-11-06 — RevDev fake-process test result (process lesson only)

RevDev run #21 `42133707971` is now verified **34/34 passed, 0 failed, 0 skipped** on Windows PowerShell 5.1 / Pester 5.7.1 at `65d9b95ed346c42ed22bd920d70cb4e5c4429a26`: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42133707971. This supersedes the earlier pending status. PocketCode impact is methodology only: use controlled fake adapters for deterministic failure-path tests, but no RevDev code or acceptance transfer. CASE-04 remains next.


## 2026-11-06 — PC-2026-11-06-P07 — Exact-SHA CI evidence and regression recovery

RevDev process integration initially passed 34/34 at run #21. A subsequent hardening pass surfaced a genuine PowerShell automatic-variable scoping defect when a function-local sentinel shadowed the global `$LASTEXITCODE` written by a native process. The source fix now uses a global sentinel/read and restores the previous global value; Pester also asserts restoration. Commits: transport `94b552a56653a18504ee0291152634a7dabdda02`; tests `264692600e589c4a8fd3198e1ab930da80e5b4f0`. Run #26/#27 were pending/in progress at last observation. This is RevDev-only and must not be reported as PocketCode test evidence.

**Process improvement:** every chat handoff must pin current branch head and exact test-run SHA, query Actions runs/jobs/logs directly when connector summaries are incomplete, preserve failures as useful evidence, and never let a previous green run stand in for a later revision. End every meaningful pass with a GitHub checkpoint and a user-facing result/status. Chat rotation is triggered by meaningful milestones or early context pressure, not by waiting until a conversation is full.


## 2026-11-06 — PC-2026-11-06-P08 — RevDev CI verification update

RevDev run #29 verified **36/36** Windows PowerShell 5.1 / Pester 5.7.1 tests at exact commit 5c0435d6e9412f3a1dc72410be6495a61acaeceb. It confirms the fake process harness and LASTEXITCODE lifecycle fix. A subsequent RevDev pass tightened 404 absence proof to require gh exit code 1, a complete parse-clean 404 and expected JSON Not Found body; auth exit 4 and cancellation exit 2 remain distinct. Current RevDev commit 144d0aa361343277aed9af76ad5736969c29abc9 contains 42 tests; run #30 42136315313 was in progress at last observation. Official gh exit-code reference: https://cli.github.com/manual/gh_help_exit-codes.

PocketCode implementation was not changed by this cross-project update. The reusable lesson is exact-SHA CI, process-level fakes, and never treating malformed/ambiguous errors as proof of absence. CASE-04 remains PocketCode's next task.


## 2026-11-06 — PC-2026-11-06-P09 — Static guard must follow abstraction changes

RevDev run #30 had 41/42 tests pass; the single failure was a stale static assertion that searched for the old inline 404 condition after it had been extracted into Test-GhApiConfirmedNotFound. The guard now locates the helper call, and two additional malformed-body cases were added. Latest RevDev test commit 5a18ba76860be7ab466fc0fe6b43ebd3aa0349c6 contains 44 tests; run #31 42136717748 was in progress. PocketCode lesson: prefer behavioral/semantic assertions and update source guards when an implementation is intentionally refactored. Do not import RevDev implementation or acceptance.


## 2026-11-06 — PC-2026-11-06-P10 — RevDev recovery work and chat-rotation protocol

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


## 2026-11-06 — Cross-project RevDev and continuity handoff

Added `AI_COLLAB/CROSS_PROJECT_UPDATE_REVDEV_2026-11-06.md` and linked it from `AI_COLLAB/CHAT_START_HERE.md`. It records RevDev's atomic local-result persistence/discovery, digest-bound publication, request-identity binding, typed HTTP absence proof, fake native-process test approach, quarantine hardening and exact-SHA CI discipline. It explicitly prohibits copying RevDev code or treating RevDev test results as PocketCode acceptance.

The note also reinforces the GitHub-backed multi-chat operating method: live start page + append-only work log + canonical detailed docs; checkpoint after every meaningful pass; rotate after 2–3 passes or earlier on context exhaustion; incoming chats verify exact live branch/CI state; never rely on a last-minute giant handoff; recover and report after tool/stream interruption. PocketCode's CASE-04 timeout/report-contract correction remains the next project task.


## 2026-11-06 — PC-2026-11-06-P11 — RevDev 81-case CI closeout

RevDev run #42 `42180012296` completed **81 passed, 0 failed, 0 skipped** on Windows PowerShell 5.1 / Pester 5.7.1 at exact source/test commit `40a8698060b50b3a94f946fe443caf201fd0f168`. Run: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42180012296. It covers 59 publisher identity/transport cases plus 22 local-result/recovery/quarantine cases. This is maintenance-source CI evidence only, not live network/queue/watcher/mission execution, installed-PC parity, or P0/P8U acceptance. The RevDev branch has docs-only commits after the tested source SHA.

PocketCode must continue its own CASE-04 timeout/report-contract work. No RevDev implementation, test count, or acceptance transfers. Reusable method: exact-SHA CI, fake process boundaries, semantic contract assertions, explicit UNKNOWN/INCOMPLETE outcomes, review partial-failure paths, and update GitHub before rotating chats.


## 2026-11-06 — PC-2026-11-06-P12 — Pyodios bridge triage and CASE-04 provenance correction

**Owner evidence:** first green Editor run of the unchanged canonical `main.py` with `items.csv` displayed only `[Bridge/executePython] PythonError`. Record as ATTEMPT OBSERVED / underlying exception UNKNOWN / artifact outcome UNKNOWN. No PASS/FAIL assigned.

**Research:** verified Pyodide 314.0.5 exception conversion; Python 3.14 `SystemExit` and `runpy`; Pyodios project file-copy rules, timestamped Error Log, log privacy warning, and no-interrupt/120-second timeout behavior. Unhandled `SystemExit` crossing the editor bridge is plausible but unconfirmed. Missing input visibility and other exceptions remain possible. Pyodios docs list bundled third-party licences but do not prove that the app/bridge source is open; no bridge code adopted.

**Deliverables:** added `AI_COLLAB/PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md`; updated the 2026-11-06 device protocol, continuation handoff, `PROJECT_STATUS.md` and `CHAT_START_HERE.md`. A separate guarded runpy wrapper checks inputs/output before execution, catches `SystemExit` as a script-requested exit (not an OS exit status), prints other tracebacks and compares the JSON oracle. CPython 3.13.5 local harness passed 2/2 success/malformed checks. Pyodios/Pyodide device execution of the wrapper is NOT RUN. Wrapper is diagnostic-only and not a sandbox.

**Red-team corrections:** (1) `PythonError` is the JS-side exception type for a Python exception crossing the bridge, not a root-cause label; (2) prior fixture instructions omitted CLI `SystemExit` semantics under an embedded interpreter; (3) vendor docs say reopen the project after external file additions, not pull-to-refresh; (4) direct CASE-04 precedence reorder conflicts with the exit-provenance matrix; (5) device status changed from no observation to observed/inconclusive.

**Decision:** no edit to frozen `main.py`, `report_contract.py`, tests, LOOP/CASE/D suites, provider/runtime, PR #2/#3 or Actions. The provenance matrix says child exit, wrapper exit, forced termination, stale and contradictory facts must be reconciled before changing the pure classifier. Preserve CASE-04 as INCOMPLETE/timed_out. $0 remains.

**Immediate next action:** owner inspects current project `summary.json`, then the Pyodios Settings → Diagnostics → Error Logs entry around the attempt; redact source/private paths before sharing. Do not rerun canonical script yet.

## 2026-11-06 — RevDev installer dependency-closure lesson

Updated `AI_COLLAB/CROSS_PROJECT_UPDATE_REVDEV_2026-11-06.md` with RevDev's discovery that runtime module dependencies must be traced through the clean installer/package path, not only unit-tested in their source folder. RevDev's 91-case suite is pending exact CI run #48 at this note. Transferable lesson only: test dependency closure, backup/rollback and one immutable source commit for multi-file installs. No RevDev code or acceptance transfers. PocketCode CASE-04 remains immediate priority.


## 2026-11-06 — RevDev installer-aware CI closeout

RevDev run #48 `42181302862` passed 91/91 at exact source/test head `935108a6937f15b76f75850ebdbe70c69000be32` under Windows PowerShell 5.1 / Pester 5.7.1. The suite includes publisher/transport, local-result/recovery/quarantine and installer dependency/source-pin tests. This is RevDev-only maintenance-source evidence, not live install or product acceptance. Updated `AI_COLLAB/CROSS_PROJECT_UPDATE_REVDEV_2026-11-06.md`. PocketCode CASE-04 remains immediate priority.


## 2026-11-06 — PC-2026-11-06-P12 continuation — saved-exception probe and handoff repair

Rechecked live project records after the previous response stalled. Confirmed the triage note and device protocol now use a read-only Console probe checking `sys.last_exc` first, then legacy `sys.last_value`. Verified Pyodide 314.0.5 documentation says the original Python exception is retained as `sys.last_value`, while Python 3.14 prefers `sys.last_exc`. Checked exact Pyodide 314.0.5 `src/core/error_handling.c`: `SystemExit` handling depends on `PyConfig.inspect`; Pyodios does not publish this runtime flag. Therefore the `SystemExit` hypothesis remains unconfirmed.

Red-team correction: the 2026-11-06 handoff still contained an older generic instruction to run the success fixture, conflicting with the newer no-rerun instruction. Replaced it with the current artifact → Error Log → saved-exception probe → guarded wrapper sequence. Updated `CHAT_START_HERE.md` to point to the 2026-11-06 handoff. Added the probe/handoff clarification to `PROJECT_STATUS.md`.

Latest verified branch snapshot before this log entry: `37d381fbacd14c6ab9b5204d07a7dfc1889f9cc2`, 777 ahead / 0 behind `main`. PR #2 and PR #3 remain OPEN/DRAFT and untouched. Ahead count is branch divergence, not completed product work.

No fixture, product source, acceptance suite, runtime/provider, security boundary, PR, deployment or budget changed. Device exception and artifact remain UNKNOWN; no device rerun occurred.

## 2026-11-06 — PC-2026-11-06-P12 addendum — Python 3.14 probe and diagnostic re-verification

Refined the Pyodios diagnostic procedure using exact Pyodide 314.0.5 type-translation docs: the bridge's original Python exception is retained in `sys.last_value`; CPython 3.14 prefers `sys.last_exc`, and `last_value` remains a deprecated fallback. The read-only probe now checks `last_exc` first. This probe passed a local smoke test with both no-exception and synthetic saved-exception cases; it has NOT run on the phone.

Checked exact upstream Pyodide `src/core/error_handling.c` at tags 314.0.5 and 314.0.7. The inspected `SystemExit` / `PyConfig.inspect` comment and wrapping block are the same. Upstream marks 314.0.7 Latest (2026-09-14), while Pyodios v1.1.0 docs still pin 314.0.5 / Python 3.14.2. Do not manually replace the runtime; the newer release is not evidence this app's bridge issue is fixed.

Expanded wrapper verification to 4/4 local checks: exact success JSON; malformed input outputs its missing-column diagnostic on stderr and creates no JSON; existing `summary.json` causes a no-run refusal and is preserved byte-for-byte; missing `items.csv` causes a no-run refusal. A first assertion pass incorrectly searched stdout only for the malformed diagnostic; corrected the harness to inspect stdout plus stderr and reran all checks. This was a harness assertion bug, not a fixture failure.

Navigation verified against current Pyodios iPhone docs: More → Settings → Error Log → View Error Log. The log can include user Python source; inspect/redact before sharing. Project import synchronization also remains project-reopen based.

## 2026-11-06 — Pyodios triage correction: Files list versus Python working folder

Correction to the preceding red-team note: it was wrong to say pull-to-refresh was unsupported. The Pyodios Files guide explicitly documents pull-down to refresh the Files browser list after external changes. The Projects guide separately says external file additions are not visible to Python until the project is reopened. These are distinct layers: refresh the Files list if that view is stale, then reopen the project to refresh the Python session's working-folder copy. The device protocol and triage note now state this distinction. Sources: https://pyodios.caffeinatedmath.com/guide/files and https://pyodios.caffeinatedmath.com/guide/projects.

The canonical task attempt remains preserved. Inspect `summary.json`, then the Error Log and saved exception before another run. On iPhone the documented navigation is More → Settings → Error Log → View Error Log; the main triage note has the corrected path and privacy warning.

## 2026-11-06 — PC-2026-11-06-P13 — Pyodios artifact-level success confirmed

Owner inspected the existing Pyodios project Files tab after the Editor displayed `[Bridge/executePython] PythonError`. `summary.json` exists and exactly matches the canonical oracle: grand total `10.75`, 2 line items, notebook total `7.00`, pen total `3.75`.

**Finding:** execution produced the correct artifact. The bridge error remains unexplained. Revised classification: artifact-level functional success (owner-inspected) / bridge error unresolved / full run inconclusive. This supersedes the earlier UNKNOWN artifact outcome. No claim of trusted child exit status, stderr capture, export/read-back, relaunch persistence or PocketCode acceptance.

**Actions:** updated the Pyodios triage note, device protocol, new-chat handoff, project status and chat start page. Preserved canonical fixture and existing artifact. No rerun, overwrite, product source/test/schema/acceptance change, runtime/provider selection, PR change, merge or deployment.

**Next:** owner inspects the timestamped Pyodios Error Log and shares only the redacted exception/traceback. If unhelpful, use the read-only `sys.last_exc` / `sys.last_value` probe. Do not rerun or overwrite the success project. Once diagnostic evidence is captured, test malformed input in a separate fresh project. `SystemExit` remains a hypothesis, not a confirmed root cause.


## 2026-11-06 — PC-2026-11-06-P14 — Error Log yielded no traceback

Owner inspected the Pyodios Error Log for the canonical success attempt. The complete available entry was only `Editor: PythonError`; no underlying exception or traceback was exposed. This leaves the bridge root cause unknown. The existing `summary.json` still exactly matches the frozen oracle, so artifact-level functional success remains established while the overall Editor attempt is inconclusive. Next: run only the read-only Console probe for `sys.last_exc` / `sys.last_value`; do not rerun the canonical script or alter the successful project. If no exception is saved, classify the probe as unavailable and consider a guarded diagnostic wrapper only in a separate disposable project after preserving current evidence.


## 2026-11-06 — PC-2026-11-06-P13 — RevDev installer-aware CI and rollback lesson (method only)

RevDev run #48 42181302862 passed 91/91 at exact source/test SHA 935108a6937f15b76f75850ebdbe70c69000be32 under Windows PowerShell 5.1 / Pester 5.7.1. It covers 59 publisher/transport, 22 local-result/recovery/quarantine and 10 installer dependency/source-pin tests. No installer or PC/live runtime action occurred.

RevDev then found its clean installer overwrote R5_INSTALLED.txt without including it in rollback. It added backup/restore and remove-new-marker behavior, plus two tests. Latest RevDev source SHA a6defbb0e8b0902e8ecc20777d0a10dc25ae344b, 93 authored tests, run #49 42182731390 pending. This is not PocketCode evidence.

Transferable lesson: package/install/update/rollback are part of the execution boundary. Trace every imported runtime dependency through the actual installer and include mutable provenance markers in rollback. For any multi-file update, fetch all files from one immutable source commit. Continue CASE-04 independently; no RevDev implementation or acceptance transfers.


## 2026-11-06 — PC-2026-11-06-P15 — Pyodios bridge source triage and test-boundary red-team

**Objective:** continue from the owner-reported Pyodios Editor attempt, resolve artifact and bridge evidence without overwriting the successful fixture, and reconcile stale guidance.

**Ranked gaps worked:** (1) bridge root cause remains unknown after Error Log exposed only `Editor: PythonError`; next read-only session exception probe; (2) embedded interpreter versus CLI `SystemExit`; (3) project folder versus Python working-folder synchronization; (4) generic `exit_code` provenance before CASE-04 classifier change; (5) Pyodios no-interrupt / UI timeout does not prove termination.

**Primary-source research:** opened Pyodide 314.0.5 type conversion docs and exact source `src/core/error_handling.c`; reviewed Python 3.14 `sys.last_exc` and `SystemExit`; compared exact Pyodide source logic at 314.0.5 and 314.0.7; reviewed Pyodios v1.1.0 Editor, Projects, Files, Settings/Error Log and FAQ docs. `SystemExit` remains only a plausible bridge lead because Pyodios does not document `PyConfig.inspect`. Python 3.14 probe reads `sys.last_exc` first then `sys.last_value`; absence of either is unavailable evidence, not proof there was no exception.

**Red-team fixes:** (1) define `PythonError` as JS-side Python-boundary exception, not root cause; (2) preserve canonical CLI fixture and isolate `SystemExit` catch in a separate diagnostic wrapper; (3) distinguish Files-list pull-to-refresh from reopening the project to synchronize external additions into the Python session; (4) replace stale CASE-04 precedence-only instruction with typed provenance-first rule; (5) correct device state to owner-inspected exact artifact success with bridge/full-run inconclusive; (6) correct stdout-only test assertion to inspect stderr for malformed-input diagnostic; (7) correct Error Log navigation and log privacy warning; (8) correct old handoff instructions to prohibit rerunning the successful project.

**Deliverables:** expanded `AI_COLLAB/PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md`; refreshed device baseline/protocol, continuation handoff, `PROJECT_STATUS.md`, `CHAT_START_HERE.md` and this log. Separate wrapper retained as a conversation attachment only, not product source. Local CPython 3.13.5 wrapper verification: **4/4** (success oracle, malformed input/stderr, existing-output refusal with unchanged sentinel, missing-input refusal). Read-only exception probe smoke test passed locally. Neither wrapper nor probe is tested on Pyodios.

**Latest device evidence:** success `summary.json` exact-match was owner-inspected. Error Log was then checked; its only entry was `Editor: PythonError`, without traceback. Current classification remains **ARTIFACT-LEVEL FUNCTIONAL SUCCESS / BRIDGE ERROR UNRESOLVED / FULL RUN INCONCLUSIVE**. Next: run only the read-only `sys.last_exc` / `sys.last_value` Console probe in the existing session. Preserve success artifact. Do not rerun, overwrite, restart session, clear variables/logs or run GC. Malformed-input case comes later in a separate fresh project.

**CASE-04 decision:** no `report_contract.py` or test patch. Resolve typed child exit vs wrapper exit vs forced termination, lifecycle evidence and contradictions at the coordinator boundary first. Preserve CASE-04 INCOMPLETE/timed_out and all canonical LOOP/CASE/D IDs.

**Repository snapshot before this pass record:** branch `b18fc0c5b58825b54fe98c5486cfee48cecbbb56`, 805 ahead / 0 behind `main`; merge base `555840d8d83342513d9cd353d4d1522d46a5c82d`. PR #2 and #3 OPEN/DRAFT and unchanged. Ahead count is history divergence, not product progress.

**Boundaries:** $0 default retained. No product implementation, fixture, schema, suite, runtime/provider, PR, Actions, deployment, merge or PC-side operation changed.

## 2026-11-06 — PC-2026-11-06-P14 — RevDev 93-case CI closeout (method only)

RevDev Actions run #49 `42182731390` completed SUCCESS at exact source/test SHA `a6defbb0e8b0902e8ecc20777d0a10dc25ae344b`: **93 passed, 0 failed, 0 skipped, 0 inconclusive, 0 not run** in 5.45 seconds under Windows PowerShell 5.1 / Pester 5.7.1. It validates the installation-marker rollback tests added after the 91-case run #48. No installer was executed and no PC/live runtime was touched. This is RevDev-only evidence.

Transferable method: include mutable provenance markers in rollback; test install dependency closure and immutable source pins; verify CI at the exact SHA; preserve explicit limits between source CI and installed runtime. PocketCode remains independent. CASE-04 remains immediate priority; preserve the Pyodios success artifact and do not rerun it.


## 2026-11-06 — PC-2026-11-06-P15 — Cross-project continuity method and forwardable chat brief

Owner requested that the PocketCode chat receive the latest RevDev progression and adopt the improved multi-chat workflow. Created `AI_COLLAB/REVDEV_CONTINUITY_UPDATE_20261106.md` with: GitHub-as-durable-memory principle; 2–3-pass checkpoint cadence; start page + append-only work log + canonical docs; early chat rotation; readback/recovery after tool failures; one lead writer; focused exact-SHA three-AI reviews; RevDev's 93/93 CI result as method-only evidence; explicit no-transfer rules; PocketCode's unchanged constraints and immediate priorities; and a copy/paste message for the PocketCode chat.

RevDev CI run #49 passed 93/93 at exact SHA `a6defbb0e8b0902e8ecc20777d0a10dc25ae344b`. This is not PocketCode code/device/acceptance evidence. PocketCode remains independent. CASE-04 timeout/report-contract provenance remains immediate priority. Pyodios status remains artifact-level functional success / bridge error unresolved / full run inconclusive; preserve exact-match summary.json and use only the read-only saved-exception probe next. No rerun, overwrite, restart or reset. PR #2/#3 remain untouched.


## 2026-11-06 — PC-2026-11-06-P16 — Pyodios diagnostic checkpoint and full chat handoff

**Objective:** close the current Pyodios diagnostic stage as far as available phone evidence permits, reconcile stale instructions, and make the next chat independently resumable.

**New owner evidence:** Error Log was checked at More → Settings → Error Log → View Error Log. Its only available detail was Editor: PythonError; no traceback or underlying exception was exposed. Existing summary.json remains owner-inspected and exactly matches the frozen oracle. Classification stays ARTIFACT-LEVEL FUNCTIONAL SUCCESS / BRIDGE ERROR UNRESOLVED / FULL RUN INCONCLUSIVE.

**Exact next action:** run only the read-only Console probe for sys.last_exc with sys.last_value fallback in the existing Pyodios session. Do not rerun/overwrite main.py, restart/reset the session, clear variables/logs, run GC, or run the diagnostic wrapper in the success project. If no saved exception is exposed, classify that as unavailable evidence. Malformed-input test must be a separate fresh project after the diagnostic.

**Handoff and continuity:** reconciled stale handoff instructions and device status; updated live entrypoint, triage, device protocol and project status; added AI_COLLAB/STATE_LEDGER_20261106.md as a compact source-of-truth ledger; added a complete copy/paste bootstrap prompt to the handoff. Product direction, fixed decisions, three-AI roles, architecture identity chain, acceptance IDs and guardrails are preserved.

**Verification:** source documents read from live branch. PR #2 and #3 checked OPEN/DRAFT, unmerged, unchanged. Actions run query for this branch returned an empty list; this does not prove no other workflow source or CI activity exists. No PocketCode code/test/device operation was executed in this pass. No product source, fixture, schema, acceptance suite, runtime/provider, budget, PR, merge or deployment changed.

**Next:** owner runs the saved-exception probe once and shares its output (redacted). Then continue the typed CASE-04 exit-provenance contract and degraded collection/teardown/network-isolation audit. Keep CASE-04 INCOMPLETE/timed_out and all canonical IDs.


## 2026-11-06 — PC-2026-11-06-P17 — RevDev working-method upgrade incorporated

Objective: adopt the owner-approved cross-project continuity and orchestration method without repeating product research or changing PocketCode product boundaries.

Completed:
- Re-read the live compact entrypoint and state ledger; fetched current work-log tail.
- Re-fetched live branch and compared against main: branch HEAD 4446135bf1345f37aa5d221d27c0eabbdbcef5c7, main 555840d8d83342513d9cd353d4d1522d46a5c82d, 820 ahead / 0 behind.
- Rechecked PR #2/#3: both OPEN/DRAFT, separate heads, untouched.
- Queried branch-filtered Actions: zero runs returned. Exact-head combined status/check-runs contain no individual checks; current branch CI remains UNKNOWN, not PASS.
- Added bounded-pass, modest batching, serialized writes, exact read-back, interruption reconciliation, durable EffectId/AttemptId and fencing principles to continuity guidance.
- Preserved existing active task and all product/acceptance boundaries.

Changed paths: AI_COLLAB/CHAT_START_HERE.md, AI_COLLAB/STATE_LEDGER_20261106.md, AI_COLLAB/CHAT_WORK_LOG.md.

Verification required: one atomic multi-file commit using expected-head lease, then exact read-back of all three files and branch head. No PocketCode product source/tests/device/runtime/provider/schema/acceptance/PR/merge/deployment changed. No RevDev code or acceptance evidence imported.

Next: await owner-provided read-only Pyodios saved-exception probe output; preserve the successful project. Then resolve typed child-exit vs wrapper-exit vs forced-termination and lifecycle provenance before CASE-04 code changes.


## 2026-11-06 — PC-2026-11-06-P18 — Task/evidence/recovery research and red-team correction

**Completed:**
- Re-read live entrypoint, ledger, handoff, status, execution acceptance, decisions, zero-budget plan, Pyodios triage/device protocol, report formatter/tests, lifecycle regression plan, execution-boundary matrix and iOS competitor baseline.
- Opened primary sources for Python-on-iOS, Apple background/file protection, Pyodios/Pyodide, Cline, OpenHands, MCP Tasks, A2A, in-toto and SQLite; reviewed public competitor claims for a-Shell, Carnets, Pyto, Coilbook and Replit.
- Added `AI_COLLAB/POCKETCODE_TASK_EVIDENCE_RECOVERY_RESEARCH_20261106.md` with competitor comparison, reuse/licence notes, architecture decision, boundary-specific observation model, recovery design, regression scenarios and source register.
- Corrected five weaknesses: CASE-04 is not a precedence patch; legacy ACP is archived and A2A is current successor; iOS embedded Python cannot produce a child-process exit code; hashes do not prove producer authenticity; SQLite cannot make a remote side effect exactly-once.
- Updated live entrypoint and ledger with research decision/protocol correction.

**Decision:** PocketCode should own task/evidence/recovery/correction orchestration and interoperate with existing runners. Cline/OpenHands/MCP/A2A/in-toto/SQLite are scoped pattern references, not wholesale dependencies. No runtime/provider selected.

**Verification:** source research opened; live branch/PR/CI state checked. Documentation writes are grouped in one atomic Git commit and read back. No product source, tests, runtime, provider, schema, canonical acceptance IDs, account, workload, budget, PR, merge or deployment changed. Starting HEAD had zero checks/runs; this research commit's CI must be queried once after checkpoint.

**Next:** owner runs the read-only Pyodios `sys.last_exc` / `sys.last_value` probe in the existing session; source work defines typed boundary-specific observations before any CASE-04 formatter patch.


## 2026-11-06 — PC-2026-11-06-P19 — Prototype integrity and static regression recovery

**Reviewed:** live branch commits after the task/evidence research checkpoint, including the simulation prototype redesign, canonical fixture pinning, EffectId correction and tab navigation changes.

**Defects found and corrected:** initial canonical-fixture checker update contained invalid regex string syntax; two new test methods were inserted inside the HTML fixture literal instead of the test class; the test fixture did not include the same tab-stop state as the prototype. Corrected checker parsing, restored the canonical source block/guard, moved tests into the test class, aligned fixture tabindex and `setTab` behavior, and added two roving-tabindex regression cases. The test file now contains 11 test methods.

**Focused verification:** canonical source fixture measured 1,939 UTF-8 bytes and SHA-256 `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7`; regex extraction and initial CSV byte comparison passed in a local Python check. Full unittest suite and browser interaction were NOT RUN. Exact branch head `c22d8108c9ceab3d003cfc92debbb99cd87e8a82` reported zero CI checks and zero workflow runs.

**Architecture correction:** matching EffectId/fingerprint means same-effect lookup/reconciliation only. No blind redispatch after ambiguous acknowledgement. Require authoritative no-acceptance evidence or provider-documented idempotent start for the exact same key/fingerprint.

**No product runtime, provider, schema, canonical acceptance, budget, PR, merge or deployment changed.** Prototype is simulation only. Pyodios saved-exception probe remains NOT RUN.


## 2026-11-06 — PC-2026-11-06-P20 — Canonical prototype fixture and checker recovery

**Completed:**
- Replaced the former sales/summary.txt demonstration with the frozen CSV-to-JSON task and the canonical source/input fixtures. The two controls select success/malformed-header expectations; they do not run code.
- Removed invented durations, generic Python 3.x runtime claims, sample download and fake Run behavior. Added separate stdout/stderr capture labels, fixture-only exit expectations, explicit job disposition, NOT MEASURED runtime/duration/cleanup/release fields, artifact expectation and provenance labels, plus selectable text fallback.
- Added complete tab/panel relationships, arrow/Home/End keyboard navigation and roving tabindex behavior.
- Pinned the displayed canonical `main.py` in the static checker by exact 1,939-byte SHA-256 and pinned success `items.csv` contents.
- Red-team found a malformed indentation around the aria-live checker guard after the roving-tabindex update. Fixed it in `scripts/check_mobile_prototype.py` and verified the exact GitHub read-back.

**Verification and limits:**
- Extracted source from the committed HTML: 1,939 UTF-8 bytes; SHA-256 matched `70c66ad3a0132923cbf3190eb3546093fcc2c61c1bdcbf3b171696e1ae7521e7`.
- Static checker passed against a reconstructed fixture containing those exact source bytes and success input bytes.
- A locally recreated 11-case regression harness passed 11/11. This is not a claim that the exact repository test file or GitHub CI ran. Exact repository CI currently has no reported check runs; browser/mobile/screen-reader interaction remains NOT RUN.
- No runtime/provider, account, workload, paid usage, product execution, artifact release, canonical acceptance ID, PR, merge or deployment changed.

**Next:** continue with the owner-supplied Pyodios read-only saved-exception probe; then use the typed boundary-specific contract before changing CASE-04 classification.


## 2026-11-06 — PC-2026-11-06-P21 — SQLite/protocol release gates and checker hardening

- Added primary-source maintenance constraints to research: SQLite WAL-reset fix floor (3.51.3 or supported backports 3.44.6/3.50.7), FULL sync for power-loss durability, same-host WAL limitation, MCP Tasks experimental status, and A2A v1.0.1 streaming/history gaps.
- Confirmed static checker now handles class/id attribute order for tab buttons; added a regression case. Test methods: 12. Exact repository test suite and CI remain NOT RUN.
- No runtime/provider or canonical acceptance decision changed.


## 2026-11-06 — PC-2026-11-06-P22 — OpenHands/Cline and provenance model review

- Read current OpenHands SDK source for EventLog append path, parent-linked events, sequence assignment, cold-load view rebuild and in-memory fallback. Adopt only the append/projection architecture pattern, not claims of immutable/tamper-proof or remote exactly-once behavior.
- Read Cline task history and shadow Git checkpoint documentation. Reuse task-scoped history, snapshot, compare/restore and resume UX; keep workspace snapshots distinct from execution receipts.
- Deepened artifact trust model using in-toto Attestation v1.2 and current SLSA v1.2. Corrected version status: SLSA v1.1 provenance page is marked retired; v1.2 is current/approved. Unsigned local receipts remain integrity records, not authenticated attestations.
- No product code/runtime/provider/schema/acceptance/budget/PR/merge/deployment change.


## 2026-11-06 — PC-2026-11-06-P23 — Typed execution evidence and recovery boundary

**Objective:** resolve the highest-risk semantic gap before changing CASE-04 classification. Preserve the existing report formatter and canonical acceptance IDs.

**Completed:**
- Re-read live entrypoint, state ledger, current research, exit provenance matrix, canonical execution acceptance, report formatter/tests, adapter envelope and Pyodios triage at branch start SHA f545974e5d76c8282968c3a86ae69d22cad81343.
- Researched Python 3.14 mobile and WebAssembly subprocess constraints, Python/Bash/Linux signal and exit semantics, Google AIP-155, AWS idempotency tokens and transactional outbox, Temporal at-least-once Activities, CloudEvents producer-scoped event IDs, OpenTelemetry source/observed timestamps, and current OpenHands/Cline/Temporal release/license metadata.
- Added a pure typed exit projection helper and 31 regression tests for child natural exit, wrapper code, signal termination, embedded SystemExit/exception, stale attempt, malformed fields and contradictory terminal evidence.
- Added AI_COLLAB/EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md and expanded task/evidence/recovery research with source-level corrections and implementation gates.

**Red-team corrections:**
1. A shell status such as 137 does not identify a natural child exit; preserve wrapper and signal evidence independently.
2. The report tests lacked program_failed plus child exit zero and timeout plus nonzero wrapper scenarios; both are now covered by the isolated projection suite.
3. Producer strings do not authenticate evidence; this helper's caller must authenticate and authorize before projection.
4. CloudEvents event IDs are unique only within source/producer scope; retain source plus ID and reject payload conflicts.
5. Event source time and collector observation time are distinct; durable coordinator sequence, not wall clock, orders accepted events.
6. Idempotency-token scope/retention varies by provider and operation; same token does not promise universal exactly-once side effects.
7. A worker protects UI responsiveness, not hostile-code isolation or mobile process durability.

**Verification:** isolated projection suite passed 31/31 under CPython 3.13.5; both files compiled. Exact GitHub read-back returned helper SHA f32237c8c5ee5d62b0416b3dd867515ce567c21b, test SHA cbd756cce1bc42a6aab0d5c48d8fac6f56cce7c1, contract SHA 7530c628dfbc868c79e90185bb096b8f92ef3c32, research SHA 1496b427d1ccf6ebfe2d02e30bd33774972505cb. Source/design commit 3c6db063fe209396cab2d23b3f61c9daedd373ce.

**Not run:** exact repository-wide test suite, GitHub Actions, browser/iOS/Android tests, authenticated coordinator, fake adapter, chosen persistence, provider workloads, termination/cleanup, egress, artifact release, crash/power-loss, canonical LOOP/CASE acceptance.

**No change:** existing report formatter, canonical LOOP/CASE/D IDs, runtime/provider/storage choice, $0 budget, owner Pyodios project, PR #2/#3, merge or deployment. The helper is unintegrated design-stage code.

**Next:** verify post-checkpoint branch and PR/CI states; keep owner Pyodios saved-exception probe outstanding; then implement authenticated boundary and fake-adapter reservation/reconciliation tests before any production formatter wiring.


## 2026-11-06 — PC-2026-11-06-P24 — Ambiguous dispatch reconciliation kernel

**Started after P23's closeout:** convert the highest-ranked dispatch-recovery rules into a pure testable decision helper.

**Completed locally:**
- Added dispatch context, provider lookup, exact idempotency contract and pure action decision types.
- Decision actions: dispatch_first, adopt_existing, retry_same_attempt, poll_existing, hold_unknown, conflict, do_not_replay.
- Bound found/not-found responses to effect, attempt, fingerprint, endpoint, account, provider, API version, region scope and token where used.
- Token-based retry requires exact documented capability, active retention, exact endpoint/account/provider/API/region/token/fingerprint scope, same-request deduplication and parameter mismatch rejection.
- Lookup-based reconciliation can work without a provider idempotency token only when an authoritative exact-scope lookup binds the exact request and attempt.

**Red-team corrections:**
1. Non-authoritative "found" must not be adopted.
2. Authoritative "not found" is not sufficient unless it binds the exact effect, attempt, fingerprint and provider scope.
3. Idempotency retention expiration must stop replay authorization.
4. A changed provider, API version or region scope invalidates capability reuse.
5. An absent provider token cannot be treated as an idempotency promise; it can only use a separate authoritative exact lookup path.

**Verification:** 28/28 local tests passed under CPython 3.13.5; both files compile. The helper is pure and local at this point, with no product integration, live provider, durable outbox or storage selection.

**Next:** commit and verify helper plus tests and update contract; then create fake-store/outbox tests for reservation, crash-before-send, lost-ack, duplicate delivery, stale lease/fencing and artifact publication. Preserve $0 default and all canonical IDs.


## 2026-11-06 — PC-2026-11-06-P24 — GitHub checkpoint verified

- Committed dispatch helper, 28-case tests, contract/research additions and updated continuity docs at source commit 203628276e65909140bf4ed563071442c538548d.
- Read-back verified dispatch helper blob 2b0928002fdf690005711ea71f1a115a665490ef and test blob f45eb831edb3cfdbcbf4284e3f81180eaee35f12; contract/research/start/ledger/worklog blobs also read back.
- Final CI snapshot at source commit: 0 workflow runs, 0 check-runs, aggregate status pending with no individual statuses. Do not claim green CI.
- PR #2 and #3 remain OPEN/DRAFT at their original head SHAs. No merge, PR mutation, deployment, provider workload or account was created.
- Branch compare at source commit: 843 ahead / 0 behind main; merge base unchanged. Ahead count reflects branch-history divergence.
- Next work: fake durable store/outbox model for crash/recovery/fencing; then authenticate observation producers and integrate only after exact test + source review.


## 2026-11-06 — PC-2026-11-06-P25 — Provider-finality and API-specific idempotency correction

- Additional red-team correction: authoritative=True alone is not enough to treat provider not-found as proof of non-acceptance. Added separate absence_final condition; only a trusted adapter may assert it from documented provider consistency/coverage semantics.
- Research section 19 records primary-source differences: Stripe API v1/v2 idempotency semantics, AWS EC2 operation/regional/zonal token scope, Google AIP-155 response/timeframe guidance, AWS transactional outbox duplicate delivery, Temporal retry boundaries, Python 3.14 mobile/WASI subprocess unsupported, Apple background suspension limits and CloudEvents main-branch 1.0.3-wip status.
- Latest helper/test Git objects are source 6760b3301e818956f71fdf02e369407e3b5cdaf7 and tests f1949ebcfd525c5715af7fd9e022d5d35f8f1063 (33 test methods). Branch commit and read-back pending.
- The 33-case expanded suite was NOT RUN. Previous 61/61 applies only to earlier code; do not claim it for this revision.
- Architecture: local atomic outbox and provider idempotency/final-absence are independent gates. If neither provider proof exists, remain hold_unknown.


## 2026-11-06 — PC-2026-11-06-P25 — Malformed input guard

- Added explicit string validation for ProviderLookup.outcome before set membership, preventing TypeError for unhashable malformed values.
- Added two regression tests: non-string lookup outcome and non-string dispatch state. Latest dispatch test file contains 35 methods.
- Latest 34-case test revision NOT RUN. Exact source/test blobs 165d141bc6ab47ad9d19d1ba537ab0e3e39aa16d and e65968cc2162dca8eb75d446e10eec06c0ab9220. This is a defensive pure-helper revision, not a provider integration.


## P25 test-file deduplication correction

- Final source review found the same test method name was defined twice in the expanded dispatch suite. Python unittest would silently replace the earlier method in the class namespace, so a regex-based method count overstated unique coverage.
- Removed the duplicate definition. The final test file now has 34 test methods and 34 unique method names. The 34-case suite remains NOT RUN after this correction.
- Final test blob: 7bcfa95c5a077b3a5d31825f0db73f593ac4d6a9. This supersedes the earlier P25 test blob SHA.


## P25 final closeout — 2026-11-06

- Latest verified branch checkpoint: 25a2083e6509d9fee2ad4ce7727405a70558813a.
- Final dispatch helper blob: 165d141bc6ab47ad9d19d1ba537ab0e3e39aa16d.
- Final dispatch tests blob: 7bcfa95c5a077b3a5d31825f0db73f593ac4d6a9. Read-back confirms 34 test methods with 34 unique names; duplicate method removed. Latest 34-case suite NOT RUN.
- Contract, research, entrypoint, ledger and work log were read back at their exact blob SHAs in this checkpoint.
- Exact-head Actions runs: 0; check-runs: 0; combined status pending with no individual statuses.
- PR #2/#3 remain OPEN/DRAFT at their original head SHAs. No PR mutation, merge, deployment, provider execution, billing or runtime/storage selection.
- Branch compare: 847 ahead / 0 behind main; merge base 555840d8d83342513d9cd353d4d1522d46a5c82d. Ahead count is history divergence, not product progress.
- Next: implement a deterministic fake outbox/store with atomic reserve + outbox, duplicate delivery, lease fencing, crash-point recovery and event dedupe. Keep it isolated and explicitly non-production until a real durable store is selected and crash-tested.


## 2026-11-06 — PC-2026-11-06-P26 — Chat retrieval failure investigation and fake outbox model

**ChatGPT error investigation**
- Investigated the exact reported iOS error string: APIClientInterface.ConversationDetailError.DetailError error 1.
- Public OpenAI documentation does not identify this internal error code. Conversation-detail retrieval is the best layer hypothesis from the symbol names, not a confirmed diagnosis.
- OpenAI's official incident history includes elevated ChatGPT conversation errors on 2026-10-30, resolved. This establishes that service-side conversation failures occur, but does not prove correlation with this user's event.
- Added AI_COLLAB/CHATGPT_IOS_CONVERSATION_DETAIL_ERROR_RUNBOOK_20261106.md with controlled comparison steps (same conversation on web, short chat in app, alternate network, status timestamp) and Support evidence requirements.
- Decision: no claim that PocketCode can repair OpenAI's client/backend. Mitigation is durable GitHub checkpoints, replaceable chats, concise bootstrap and exact-head recovery after interrupted writes.

**Fake outbox implementation**
- Added scripts/fake_outbox.py and scripts/test_fake_outbox.py; documented in AI_COLLAB/FAKE_OUTBOX_MODEL_20261106.md.
- Implemented synchronous in-memory model for reservation/dispatch-intent atomic commit point, EffectId across attempts, explicit new-attempt authorization, lease fencing, crash-before-send recovery, post-dispatch reconciliation, exact-found adoption, final-absence retry gate and receiver duplicate handling.
- Red-team correction: a stable EffectId must not be conflated with one AttemptId. Model now stores attempts independently and only permits a new attempt after prior terminal state and explicit authorization.
- Local CPython 3.13.5: 19/19 tests passed; py_compile passed. The fake store is not durable and the test failpoint is not a power-loss/transaction test. No provider adapter or runtime integration.
- No canonical IDs, report formatter, CASE-04, runtime/provider/storage decision, budget, PR, merge or deployment changed.

**Verification and current state**
- Verified branch handoff HEAD d62429cbb246b181ecaf5862b49169cc95bee1c2.
- Committed runbook, fake model and test artifacts in follow-on commits; latest pre-doc checkpoint 56bcc7167b33554a29b68c8fdccc448b9383b6b6.
- Exact-head Actions and combined status must be checked after the documentation checkpoint. PR #2/#3 remain OPEN/DRAFT and untouched.
- Next: append-only event journal/provenance model and durable-store test boundary. Pyodios read-only saved-exception probe remains the owner action; preserve existing success project and do not rerun/overwrite.
