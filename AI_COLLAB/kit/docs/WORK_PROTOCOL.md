# WORK PROTOCOL (universal: any AI, any tier, any project)

Goal: a brand-new chat, on a free account with a small context window, can resume work in one message and never has to "catch up" on a huge file.

## 1. Tiers (what gets loaded, in order)
- Tier 0 BOOT.md (<=500 words): identity, hard constraints, read order.
- Tier 1 STATE.md (<=900) + NEXT_TASK.md (<=350): current state, the one task.
- Tier 2 INDEX.md (<=1,200): find the one file a task needs. Read sections only.
- Tier 3 everything else, including ARCHIVE/ and the work log: on demand, never whole.
Total start-up load is about 1,750 words (roughly 2.5k-3k tokens). `ctx_kit.py capsule` builds this as one paste-able block for chats with no repo access.

## 2. Session rules
1. One chat = one task = one commit-sized result. Finished task? Close and start a new chat.
2. Boot: read the capsule only. Open nothing else until it is read.
3. Turn size: about 350 lines of new text per turn; files written in chunks of <=200 lines; <=6 files per commit. Use patches or section edits, not whole-file rewrites.
4. Mode: default to normal mode. Use "Think" only for architecture challenge, security review, or a bug that survived two normal attempts. Give Think the NEXT_TASK card and at most 3 files, never "read everything and continue".
5. Checkpoint after every unit of work and always before a Think request or a long output: commit, or overwrite CHECKPOINT.md (<150 words).
6. Close: update STATE (slim), write the next NEXT_TASK, overwrite CHECKPOINT, list changed paths and evidence status.

## 3. Error runbook (free ChatGPT and others)
- "Streaming interrupted. Waiting for the complete message": the connection dropped. Do not resend. Stay in the app, wait 60 seconds, then reopen the chat. If the answer appeared, continue. If not, send RESUME_AFTER_ERROR once.
- "The operation couldn't be completed" or "could not load this conversation": force-close and reopen the app, or open the same chat on the web. Check status.openai.com. If the chat will not open after two tries, abandon it: start a new chat with START_NEW_CHAT. Nothing is lost because state lives in the repo.
- Two failures in one chat: abandon the chat. Long chats fail more often.
- Never retry the identical request a third time. Shrink the task, drop Think, or move to a new chat.
- While a Think request runs, keep the app in the foreground and the screen on.

## 3b. "Stopped thinking", silent failures and lost chats
- Treat every chat as disposable and GitHub as the truth. See STUCK_CHAT_FORENSICS.md.
- Write-ahead rule: a finding or a change is committed to a repo file BEFORE you summarize it in chat. The chat message is only a notification.
- One commit per unit of work, each under about 10 minutes of model time. Commit message: "[chat-<id>] <what>". Open the commit list, not the chat, to see progress.
- Red CI rule: if the latest CI run on the branch is red, the first task is to fix it or to record exactly why it is red. Never stack new work on a red commit.
- After any "Stopped thinking" or a chat that goes silent: wait 60 seconds, then check the branch commits. If a new commit appeared, the work continued. If nothing for 15 minutes, send RECONCILE_AFTER_STUCK in a NEW chat.
- Long Think and Work runs are the most exposed. Use them only for a short, bounded task card, and keep the app open.

## 4. Stall detection
Two identical outputs, diffs or errors in a row means stop. Write the symptom into CHECKPOINT, then change something: smaller task, normal mode, fresh chat, different AI.

## 5. Lean rules (YAGNI ladder; inspired by the Ponytail skill, which an independent JetBrains test credited with only ~10% savings, so treat it as hygiene, not magic)
Before writing anything: (1) does the platform or standard library already do it? (2) does the repo already have it? (3) is there a maintained open-source piece with a compatible licence? (4) only then write the smallest version. Do not build for needs nobody has stated.

## 6. Honesty and evidence
VERIFIED = you opened it or ran it and can show output. INFERRED = reasoning. UNKNOWN = not checked. Test results are PASS / FAIL / NOT RUN, with the pasted output. A chat message is never proof that a file changed: look at the commit.

## 7. No-loss rule (nothing is ever deleted)
- Never delete, never rewrite history. Move old material to `ARCHIVE/` and add a row to `MOVES.tsv` (old<TAB>new).
- Leave a one-line pointer where the content used to be.
- IDs (decisions, tests, acceptance criteria) are permanent; never renumber.
- Before and after any reorganisation: `ctx_kit.py manifest`, then `ctx_kit.py verify`. Any LOST line blocks the commit.
- Extract, do not paraphrase: STATE, INDEX and NEXT_TASK point to originals instead of replacing them.

## 8. Rotation
STATE.md holds current state only. When it passes 900 words, move closed items to ARCHIVE/STATE_<date>.md and leave a pointer. The work log is append-only and read by its last 30 lines.

## 9. Multi-AI lanes
Same BOOT for every assistant. One primary implementer per task; others review. Provider files (CLAUDE.md, GEMINI.md, AGENTS.md, custom instructions) only point at BOOT.md and add nothing that contradicts it.

## 10. Tier compatibility
- Free ChatGPT, no connector: paste CAPSULE.txt. Works with a 16K-token window (reported free-tier figure; verify in your account).
- Paid ChatGPT, Claude, Gemini, Copilot, Cursor and similar: same files; point their rules file at BOOT.md.
- Any chat: if you cannot reach the repo, say so and work from the pasted capsule only.
