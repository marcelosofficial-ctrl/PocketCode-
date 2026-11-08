# BOOT: PocketCode   (read this first; under 500 words)

## Identity
- Phone-first, provider-neutral "Agentic Orchestration Control Plane" for iOS and Android. Not a generic mobile Python IDE. MVP loop: explicit paste/import, bounded execution, truthful evidence and artifacts, a copyable report for any AI, a corrected rerun as a distinct attempt.
- Repo: marcelosofficial-ctrl/PocketCode- (PUBLIC). Active branch: pocketcode-ai-workflow-director-research-2026-10-28. Live HEAD seen 2026-11-07 14:23 UTC: c4c00f7bb1b84200060dcfb0bad89bfb8a109815 (re-fetch before relying on it).
- `main` is STALE (early discovery README). Do all work on the active branch. PR #2 and #3 are open drafts: do not modify them.
- AI_COLLAB/ holds 100+ docs (about 2.7 MB). Code and tests are in scripts/. CI: workflow "PocketCode Python conformance tests".

## Hard constraints
1. $0. No paid account, host, provider, workload or billing without separate owner approval (D-005).
2. Phone-first iOS and Android. Never assume a PC.
3. Provider-neutral. No runtime, provider, database, hosting or PWA-vs-native choice yet (D-004: validate before stack commitment).
4. Explicit, user-controlled context transfer. No clipboard polling, overlays or automatic capture.
5. Default-deny permissions; egress off by default; untrusted code needs disposable, externally constrained execution. Stock Pyodide/WASM is for trusted, light tasks only.
6. Keep distinct: CommandId, DispatchAttemptId, ExecutionId, ObservationSequence, ResultReceipt. Unknown or degraded evidence never becomes PASS or FAIL by inference.
7. Preserve LOOP-01..14, CASE-01..16 and D-IDs exactly (D-001 unified direction with separate dev boundaries; D-002 GitHub is source of truth; D-003 no secrets in the public repo; D-004; D-005). Never renumber.
8. PocketCode and RevDev stay separate: repos, roadmaps, adapters, runtimes, acceptance suites, release gates, security boundaries. Never import RevDev evidence.
9. Public repo: never commit secrets, tokens or private data.
10. Evidence honesty: VERIFIED / INFERRED / UNKNOWN / NOT RUN. A chat message is not proof; a commit and its CI run are.

## Read order
1. STATE.md  2. NEXT_TASK.md  3. INBOX_<your name>.md (messages from other AIs)  4. INDEX.md, only to locate files.
Never load a file over ~1,500 words whole. These are history, read one named section only: CHAT_START_HERE.md (51 KB), STATE_LEDGER_20261106.md (71 KB), CHAT_WORK_LOG.md (96 KB), CHAT_HANDOFF_20261029_POCKETCODE.md (109 KB), NEW_CHAT_HANDOFF_20261103.md and _20261105.md (74 and 87 KB), PROJECT_STATUS.md (84 KB).

## Working rules (full text: kit/docs/WORK_PROTOCOL.md)
- One chat = one task. Commit to GitHub BEFORE summarizing in chat. About 350 lines per turn. Overwrite CHECKPOINT.md after each unit. Normal mode; Think only if NEXT_TASK says so.
- Rapid pushes make some intermediate CI runs red by design. Judge by the latest commit. Never stack new work on a red latest commit.
- Move or archive, never delete; log every move in MOVES.tsv.
- Talk to other AIs through INBOX_<name>.md (see MAILBOX.md). The owner no longer has to relay.
- If you cannot read or write GitHub, say so at once and stop.

## Roles
Claude: lead developer and architecture/implementation reviewer. Gemini: co-developer and independent security/spec auditor. ChatGPT: continuity holder, evidence reconciler, acceptance architect, cross-project coordinator. One lead writer per branch or work item; others review or take disjoint files.
