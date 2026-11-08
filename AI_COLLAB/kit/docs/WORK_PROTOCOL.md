# WORK PROTOCOL v2 (any AI, any tier, any project)

Goal: a brand-new chat on a free account resumes from about 1,700 words of context, and any chat can die at any moment without losing work.

## 1. Context tiers
- Tier 0 BOOT.md (500 words max). Tier 1 STATE.md (900) + NEXT_TASK.md (350) + your INBOX file (600). Tier 2 INDEX.md (1,200): locate files. Tier 3 everything else, by section only.
- Never load a file over ~1,500 words whole. If your tool can only return whole files, do not open files marked L or XL in INDEX.md; use an extract instead.
- Extract once, then read the extract: when a big document is needed more than once, write EXTRACT_<name>.md (500 words max, with pointers to the sections) next to it and add it to INDEX.md. Extract, do not paraphrase away facts.
- Start-up load is about 1,700 words (roughly 2.5k to 3k tokens), which fits a 16K-token free chat (reported free-tier size; check your account).

## 2. Session rules
1. One chat = one task = one commit-sized result. Finished? Close and start a fresh chat.
2. Boot: BOOT, STATE, NEXT_TASK, INBOX only. Open nothing else until they are read.
3. Write-ahead: commit work to GitHub BEFORE summarizing it in chat. The chat is a notification; the commit is the record.
4. About 350 lines per turn; files in chunks of at most 200 lines; at most 6 files per commit.
5. Normal mode by default. Think only for architecture challenge, security review, or a bug that survived two normal attempts, with the task card and at most 3 files.
6. Overwrite CHECKPOINT.md after every unit of work (under 150 words).
7. Close: update STATE (slim), write the next NEXT_TASK, overwrite CHECKPOINT, list changed paths and evidence status.

## 3. Lean rules (adapted from the Ponytail skill and similar token-saving plugins)
- Before writing anything: (1) does the platform or standard library already do it? (2) does the repo already have it? (3) is there a maintained open-source piece with a compatible licence? (4) only then write the smallest version. No speculative features, surgical diffs, no new framework or dependency without a one-line reason.
- Lean output contract: the final chat reply is at most 15 lines: DONE (paths and commit sha), CI (latest commit), NEXT, OWNER ACTIONS (max 3). Never restate project context. Plain language, not telegraphic "caveman" speech.
- Filter tool output: for a failed CI run read only the first failing assertion of the failing job; never paste logs into chat.
- Ponytail's own benchmark claims about 54% less code and 22% fewer tokens; an independent JetBrains test credited about 10%. Treat the numbers as hygiene, not a promise.

## 4. CI and commits
- Many quick pushes create red intermediate runs and failure emails. Judge by the latest commit. Never stack new work on a red latest commit; the first task is to fix it or record exactly why it is red.
- Commit message: "[chat-<id>] <what changed>". A commit that changes nothing is a loop. Three consecutive commits with the same message mean stop and write the blocker in CHECKPOINT.md.
- NOT RUN (no workflow run for that exact commit) is not evidence of failure, and never evidence of success.

## 5. Stuck chats and errors (see STUCK_CHAT_FORENSICS.md)
- "Streaming interrupted": do not resend. Wait 60 seconds, reopen the chat, then check the branch commits.
- "The operation couldn't be completed" or "Could not load this conversation": force-close and reopen, try the web, check status.openai.com. Two failures in one chat: abandon it and start a fresh one; nothing is lost because the repo holds the state.
- "Stopped thinking" with no error: the work may still be running. After 15 minutes with no new commit, treat the chat as dead.
- Keep the app in the foreground during Think or long runs.
- Stall rule: two identical outputs, diffs or errors in a row means change something (smaller task, normal mode, fresh chat, another AI).

## 6. Honesty and evidence
VERIFIED = opened or ran it and can show output. INFERRED = reasoning. UNKNOWN = not checked. Tests are PASS / FAIL / NOT RUN with pasted output. Do not claim a device, PC or product test that was not run.

## 7. Nothing is lost
- Never delete content that exists nowhere else. Move old material to ARCHIVE/, leave a pointer, log old and new path in MOVES.tsv.
- IDs (decisions, tests, acceptance criteria) are permanent. Never renumber.
- The repo's AGENTS.md or BOOT.md defines who may do what; irreversible actions (force-push, history rewrite, deleting unique content) always need the owner's explicit OK.

## 8. Rotation
STATE.md holds current state only. Over 900 words: move closed items to ARCHIVE/STATE_<date>.md with a pointer. Work logs are append-only and read by their last 30 lines.

## 9. Multi-AI lanes
Same BOOT for every assistant. One lead writer per work item; others review or take disjoint files. Messages between AIs go in INBOX_<name>.md (MAILBOX.md). Provider files (CLAUDE.md, GEMINI.md, AGENTS.md, ChatGPT custom instructions) only point at BOOT.md.

## 10. Tier compatibility
Free ChatGPT, paid ChatGPT, Claude, Gemini, Copilot, Cursor: same files. With no repo access: paste BOOT.md, STATE.md and NEXT_TASK.md as the start message and say so.
