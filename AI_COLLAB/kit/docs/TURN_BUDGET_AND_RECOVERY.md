# Turn budget and crash recovery (hard rules for chat-based AI workers)

Status: RULES. Adopted 2026-11-14 for RevDev (budget 3 commits, 6 tool calls, 3 files read per turn) and applied to PocketCode with a looser budget (5 commits, 10 tool calls, 3 files read) because PocketCode chats fail less often. Tags: OBSERVED = seen in the RevDev repository; SECONDARY = public issue reports; INFERRED = reasoning.

## 1. What the evidence shows
- **OBSERVED (RevDev branch, 2026-11-14):** one ChatGPT working session made 25 commits between 01:58:50 and 02:19:04 UTC, about one every 50 seconds, alternating test and checkpoint commits: one long autonomous run of dozens of tool calls without a reply to the owner.
- **SECONDARY:** public reports describe the same failure shape: tool steps are saved, the final answer is never saved, and the chat shows "Stopped thinking" or loses the reply (openai/codex issues 54974 and 58943).
- **INFERRED:** the work is not lost; the commits and the checkpoint are in GitHub. What is lost is the chat's own record of what it did, so the next turn does not know where the new commits came from and gets confused. The longer the run, the more the platform can drop it.

## 2. Rules
**T1 Budget per turn (hard).** RevDev: at most 3 commits, 6 tool calls, 3 files read. PocketCode: at most 5 commits, 10 tool calls, 3 files read. Each commit touches at most 2 files and about 200 changed lines. Never reconstruct or rewrite a large file; create a new small file or use a range-preserving edit.
**T2 Mode.** No Think, Work or agent mode for repository work. No autonomous loops.
**T3 In-progress marker.** The first action of a turn overwrites CHECKPOINT.md with: `IN PROGRESS: <unit> | files: <paths> | <time>`. The last action overwrites it with: `DONE: <what landed, commit SHAs> | next: <one step>`. Then reply in at most 10 lines and STOP.
**T4 Recovery on resume.** If CHECKPOINT.md says IN PROGRESS, or any commit is newer than CHECKPOINT.md: list the last 10 commits with their changed paths, write at most 10 lines in CHECKPOINT.md beginning `RECOVERED:` (what landed, what is unfinished), then do ONE unit.
**T5 Mechanical work.** Repetitive work (for example migrating many tests one at a time) is planned in NEXT_TASK.md as a numbered list of units; each turn does the next one or two and ticks them off in the repository, so the plan survives a lost chat.
**T6 The owner's "continue" is the loop.** Short turns are the design.
**T7 If a turn dies anyway.** Do not retry the same prompt in the same chat. Open a NEW chat and send "Continue working on <project>"; T4 applies.
**T8 Side effects.** Fewer commits per turn also means fewer red intermediate CI runs and failure emails.

## 3. Measure
Count dead turns (turns whose reply never arrived) per week in AI_LANE_LOG.tsv. The target is a steady fall; if it does not fall, shrink T1 further.
