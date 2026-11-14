# BOOT: PocketCode (read first; under 500 words)

## Identity
- Phone-first, provider-neutral Agentic Orchestration Control Plane for iOS and Android, not a generic mobile Python IDE.
- MVP: explicit paste/import → bounded execution → truthful evidence/artifacts → copyable report for any AI → corrected rerun as a distinct attempt.
- Repo: marcelosofficial-ctrl/PocketCode- (PUBLIC). Active branch: `pocketcode-ai-workflow-director-research-2026-10-28`. Always fetch live HEAD; no saved SHA is authoritative.
- `main` is stale. Work on the active branch. PR #2 and #3 are open drafts; do not modify them.
- Code/tests: `scripts/`. CI workflow: "PocketCode Python conformance tests". Docs: `AI_COLLAB/`.

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

## Read and resume
Read in order: BOOT.md (this file) → STATE.md → NEXT_TASK.md → CHECKPOINT.md → INBOX_<your name>.md → live branch HEAD and latest five commits. If commits post-date the checkpoint, inspect their messages and changed paths first. Use INDEX.md only after this sequence to locate other docs. Never load a file over ~1,500 words whole; read large history by section.

## Working rules
- One chat = one task. Commit to GitHub before summarizing. About 350 lines per turn; overwrite CHECKPOINT.md after each unit. Normal mode unless NEXT_TASK says otherwise.
- Owner decisions and canonical specs outrank proposals and history. One lead writer per shared work item; re-fetch branch and file SHAs after concurrent writes or rejected updates. See `kit/docs/WORK_PROTOCOL.md` sections 11–13.
- Keep CI claims tied to exact workflow/run/branch/SHA/job/environment/test totals. NOT RUN is neither failure nor success.
- Final chat reply: at most 15 lines (done, CI, next, owner actions). Move/archive rather than delete; log file moves in MOVES.tsv.
- Coordinate through INBOX_<name>.md (MAILBOX.md). If GitHub read/write is unavailable, say so and stop.

## Roles
Claude: lead developer and architecture/implementation reviewer. Gemini: co-developer and independent security/spec auditor. ChatGPT: continuity, evidence reconciliation, acceptance architecture and cross-project coordination. One lead writer per branch/work item; other AIs review or take disjoint files.
