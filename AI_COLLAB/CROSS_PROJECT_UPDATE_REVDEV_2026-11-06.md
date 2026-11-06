# Cross-project update from RevDev — 2026-11-06

Purpose: give the PocketCode lead chat current RevDev progress and the improved multi-chat working method. This is process and research context only. PocketCode remains a separate product, repository, roadmap, client, runtime, adapter set, security boundary, acceptance suite and release gate.

## RevDev progress worth knowing

RevDev's working branch is `review/revdev-adaptive-ai-workshare-2026-10-27` in `marcelosofficial-ctrl/DevRelay-Missions`.

Recent verified work:
- Added a create-only atomic local result writer for `queue-result.json`, with UTF-8 no-BOM output and SHA-256.
- Added strict local result discovery by project, mission, protocol, schema, run ID/directory and result state. It refuses to select the newest when multiple results match. Ambiguous or incomplete discovery blocks automatic publication.
- The mission runner writes the result atomically. The watcher forwards the discovered SHA-256. The publisher re-reads and verifies the exact digest before its first GitHub API call.
- Publisher request identity is now explicitly checked: the CLI Project/Mission arguments must exactly match the local result object's own project/mission before any GitHub API request. This prevents publishing a result under the wrong immutable path.
- Publisher transport was isolated and tested through a fake native child process under Windows PowerShell 5.1. Tests cover process exit code, stdout/stderr, HTTP 200/404/429, rate-limit headers, missing executable and correct preservation/removal of global `LASTEXITCODE`.
- A remote mission path is treated as absent only with a complete, parse-clean GitHub 404, expected `message=Not Found`, and the documented general failure exit code. Authentication, cancellation, malformed response and unknown status do not count as absence.
- Remote post-publication readback compares exact prepared-envelope bytes, not merely project/mission/run identity.
- Watcher quarantine paths now include a GUID, do not use `Move-Item -Force`, and use atomic create-only metadata writes. The move plus metadata remains a multi-step operation, not a transaction.

CI evidence:
- RevDev run #37 passed 73/73 on Windows PowerShell 5.1 / Pester 5.7.1 at exact older head `c483d8b5c21c362d4236b521b8958572fb223f8f`: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42178716235
- The next RevDev change adds publisher request-identity tests and quarantine safeguards. Current exact source/test head `40a8698060b50b3a94f946fe443caf201fd0f168` has 81 authored Pester cases (59 publisher + 22 local-result/recovery/quarantine). Run #42 `42180012296` completed SUCCESS with **81 passed, 0 failed, 0 skipped, 0 inconclusive, 0 not run** under Windows PowerShell 5.1 / Pester 5.7.1: https://github.com/marcelosofficial-ctrl/DevRelay-Missions/actions/runs/42180012296. Later commits in RevDev's branch were documentation-only at this checkpoint. Do not interpret this as live product or canonical P8U/P0-D acceptance.
- These are RevDev maintenance-source tests only. No live GitHub API, queue/watcher/mission execution, installed-PC parity or canonical P8U/P0-D acceptance is claimed. P0 remains open.

## Transferable engineering lessons for PocketCode

1. Test the real boundary with a controlled fake when possible, not just a parser or a static source-text assertion. Keep tests hermetic and do not issue real network writes.
2. Pin every CI result to its exact commit SHA. A previous green run does not validate a later revision.
3. When implementation moves behind an abstraction, update tests to assert behavior at the current boundary rather than stale source spelling.
4. Treat missing, malformed, partial and ambiguous observations as UNKNOWN/INCOMPLETE, not absence or success.
5. Bind local result identity, digest and requested operation before external effects.
6. Make create-only immutable writes and explicit recovery states preferable to overwriting or guessing.
7. A failed tool call or interrupted chat must not leave work uncheckpointed.

Do not copy RevDev PowerShell code, assumptions or acceptance results into PocketCode. Apply the principles only where PocketCode's own architecture supports them.

## Multi-chat continuity method

GitHub is durable project memory. A ChatGPT conversation is a temporary worker, not the source of truth.

- Start every PocketCode chat at `AI_COLLAB/CHAT_START_HERE.md`. Fetch the live branch head first, verify the working tree/PR/CI status, then read only task-specific docs.
- Keep three layers current: (1) compact live start page, (2) append-only `CHAT_WORK_LOG.md`, (3) canonical detailed design/spec/evidence documents.
- At the end of every meaningful pass, update the relevant canonical document, append the work log, refresh the start page if the next chat needs a new next action, then read back the exact changed content.
- Do not wait for context to reach its limit. Rotate after roughly 2–3 meaningful engineering/research passes, or immediately after a source/test/CI/reviewer/decision milestone. Rotate earlier if answers become repetitive, tools fail, or the assistant starts losing continuity.
- The outgoing chat should not create a huge one-off handoff from memory. It should point to the live start page and append a short checkpoint: exact branch head, files/commits changed, tests and exact CI result, what remains NOT RUN/BLOCKED/UNKNOWN, and one next action.
- The incoming chat should verify the links and exact live state, not blindly trust the previous chat's summary.
- Keep work bounded: each pass should produce a source/test change, a decision-changing research result, an adversarial review packet, or a clearly recorded blocker. Avoid repeated rediscovery and long speculative research that does not change a decision.
- One lead writer per repo/branch/work item at a time. Other AIs can review read-only or work on disjoint files. Re-fetch before writes, serialize same-path edits, and read back after writes.
- If a tool call errors or streaming is interrupted, recover from the last confirmed GitHub commit, inspect whether the attempted write actually landed, then finish with a durable checkpoint and user-facing result. Never silently stop.
- Keep the three-AI roles: Claude lead developer/architecture reviewer; Gemini co-developer/security/spec auditor; ChatGPT continuity/evidence/acceptance/cross-project coordinator. The owner manually forwards work between chats.

## PocketCode next action remains independent

Continue PocketCode's own highest-value task: inspect and fix `scripts/report_contract.py` CASE-04 timeout classification so trusted `timed_out` evidence wins over a nonzero exit code and produces INCOMPLETE/timed_out, with a complete evidence fixture. Reconcile Gemini's concern that degraded collectors/teardown cannot produce PASS/FAIL. Then run PocketCode's own exact suite and update its own evidence. Do not let the RevDev work displace CASE-04.



## CI verification closeout

RevDev's run #42 exact source/test revision passed 81/81. This supersedes the pending status earlier in this note. The next RevDev step is independent Claude/Gemini review of local-result discovery, digest/request identity binding, READ_ONLY RUN_ONCE policy, quarantine multi-step failure semantics, and PowerShell native process state. PocketCode should continue CASE-04 independently.


## 2026-11-06 — RevDev installer integration finding (CI pending)

A further RevDev integration review found that the R5 watcher/runner/publisher import four sibling modules that the previous clean installer did not stage. The RevDev review branch now updates the clean installer to stage, parse, hash, back up, install and roll back those modules, validate exports/import dependency, bind the publisher self-test to a local result digest, require exact remote-byte verification, and record module hashes in the installation marker. It also resolves main once and fetches all source files by that exact commit SHA to prevent mixed-revision installation.

Exact RevDev installer blob `d28470e818f356c5379430f2f9b53c473559752d`; installer tests blob `0007bd4d50e0413c0d2cfbc89a1c2be396b0dcae` (10 cases). Full RevDev suite is 91 cases. Actions run #48 `42181302862` targets source/test head `935108a6937f15b76f75850ebdbe70c69000be32` and was still in progress at the Pester installation step. Do not claim 91/91 until exact CI completion.

This is RevDev-only. Its redirector/installer still fetch production files from main; review-branch changes do not reach the PC without deliberate merge. No installer was executed and no PC/live API/queue operation occurred. PocketCode should not copy its PowerShell code or delay CASE-04. Transferable method: trace every new runtime dependency through the real installer/package path, test install/rollback behavior, and pin one immutable source revision for a multi-file install.
