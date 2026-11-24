# BOOT: PocketCode (read first; under 500 words)

## Identity
- Phone-first, provider-neutral Agentic Orchestration Control Plane for iOS and Android, not a generic mobile Python IDE.
- MVP: explicit paste/import → bounded execution → truthful evidence/artifacts → copyable report for any AI → corrected rerun as a distinct attempt.
- Repo: marcelosofficial-ctrl/PocketCode- (PUBLIC). Active branch: `pocketcode-ai-workflow-director-research-2026-10-28`. Always fetch live HEAD; no saved SHA is authoritative.
- `main` is stale. Work on the active branch. PR #2 and #3 are open drafts; do not modify them.
- Code/tests: `scripts/`. CI workflow: "PocketCode Python conformance tests". Docs: `AI_COLLAB/`. Every bare path below (STATE.md, kit/docs/WORK_PROTOCOL.md, INDEX.md) is relative to AI_COLLAB/; for example the full path of the work protocol is AI_COLLAB/kit/docs/WORK_PROTOCOL.md (a read at the repository root returns 404).
- Name: the project name stays PocketCode (owner decision 2026-11-11 after name research; PoCo is not adopted).

## Hard constraints
1. **$0:** no paid account, host, provider, workload or billing (D-005/D-006).
2. **Phone-first:** never assume PC access.
3. **No stack choice:** provider-neutral; no runtime, provider, database, host or PWA/native choice beyond the owner-approved no-spend PWA path (D-004).
4. **User-controlled context:** explicit paste/import only; no clipboard polling, overlays or automatic capture.
5. **Security:** default-deny permissions and egress; untrusted code requires disposable, externally constrained execution. Stock Pyodide/WASM is for trusted light tasks only.
6. **Identity:** keep CommandId, DispatchAttemptId, ExecutionId, ObservationSequence and ResultReceipt distinct. Unknown/degraded evidence never becomes PASS or FAIL by inference.
7. **Acceptance:** preserve LOOP-01..14, CASE-01..16 and D-IDs exactly. Never renumber or silently change meanings.
8. **Separate projects:** PocketCode and RevDev keep separate repos, roadmaps, adapters, runtimes, security boundaries, suites and release gates. Never import RevDev evidence.
9. **Public repo:** no secrets, tokens or private data.
10. **Evidence:** VERIFIED / INFERRED / UNKNOWN / NOT RUN. A chat assertion is not proof; source pins and CI output are.

## Read and resume (no handoff message is ever needed)
Read in order: BOOT.md (this file) → STATE.md → NEXT_TASK.md → CHECKPOINT.md → INBOX_<your name>.md → live branch HEAD and latest five commits. If CHECKPOINT.md says IN PROGRESS, or commits post-date it, RECOVER first (kit/docs/TURN_BUDGET_AND_RECOVERY.md, rule T4): inspect their messages and changed paths, write a RECOVERED note, then do one unit. Use INDEX.md only after this sequence to locate other docs. Never load a file over ~1,500 words whole; read large history by section.

## Working rules
- **TURN BUDGET v2 (owner request 2026-11-24 to get more done per turn; replaces the numbers in kit/docs/TURN_BUDGET_AND_RECOVERY.md, whose recovery rules still apply):** per turn at most 2 units, 6 commits, 12 tool calls and 5 files read; each commit at most 2 files and about 300 changed lines; never rewrite or reconstruct a large file. Start the second unit only if the first ended DONE, its CHECKPOINT is written and no CI result is pending. No Think, Work or agent mode, no autonomous loops. First action: overwrite CHECKPOINT.md with `IN PROGRESS: unit, files, time`; last action: `DONE` plus commit SHAs and the next step; reply in at most 12 lines and stop. 25 commits in one run is what crashed chats; 6 is the ceiling.
- **Owner trigger words:** "continue" = read the startup set, recover if needed, then do one unit. "do the next unit now" = same, exactly one unit. "do the next two units now" = same, up to two units within the budget above. This project's chat handles PocketCode only; text about another project (for example RevDev or LingoMingle) is not PocketCode work and must not be written into this CHECKPOINT.md.
- Commit to GitHub before summarizing; chat replies can vanish, commits do not.
- Owner decisions and canonical specs outrank proposals and history. One lead writer per shared work item; re-fetch branch and file SHAs after concurrent writes or rejected updates. See `kit/docs/WORK_PROTOCOL.md` sections 11–13.
- Keep CI claims tied to exact workflow/run/branch/SHA/job/environment/test totals. NOT RUN is neither failure nor success.
- Move/archive rather than delete; log file moves in MOVES.tsv.
- Coordinate through INBOX_<name>.md (MAILBOX.md). If GitHub read/write is unavailable, say so and stop.

## Roles
Claude: reviewer and small verified tasks, and since 2026-11-24 also whole units the owner assigns (Claude reads CI results from Gmail run emails). Gemini: independent security/spec auditor. ChatGPT: lead, continuity, evidence reconciliation, acceptance architecture and cross-project coordination. One lead writer per branch/work item; other AIs review or take disjoint files.
