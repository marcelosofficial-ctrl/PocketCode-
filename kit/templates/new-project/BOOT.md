# BOOT: <PROJECT> (read first; under 500 words)

Template. Copy the six files of kit/templates/new-project/ into AI_COLLAB/ of the project repo (INBOX_TEMPLATE.md becomes INBOX_chatgpt.md and INBOX_claude.md). Replace every <...>. Anything not proven by the repo or stated by the owner stays UNKNOWN. Delete this paragraph when done.

## Identity
- <PROJECT>: <one-line product description>. Source: owner / repo / UNKNOWN.
- Repo: marcelosofficial-ctrl/<REPO> (<PUBLIC or PRIVATE>). Active branch: <BRANCH>. Always fetch live HEAD; no saved SHA is authoritative.
- Code and tests: <paths or UNKNOWN>. CI workflow: <name or NONE>. Docs and AI state: AI_COLLAB/.

## Hard constraints
1. **Budget:** UNKNOWN until the owner states it. Do not assume any paid account, host, provider or billing.
2. **Owner device:** assume phone only; never assume PC access until the owner says so.
3. **Separate projects:** never import evidence, decisions or acceptance IDs from RevDev or PocketCode. Each project has its own repo, roadmap and release gates.
4. **Visibility:** if the repo is PUBLIC, no secrets, tokens or private data.
5. **Evidence:** VERIFIED / INFERRED / UNKNOWN / NOT RUN. A chat assertion is not proof; source pins and CI output are. Never claim tests passed without output. NOT RUN is neither failure nor success.
6. **Decisions:** owner decisions outrank proposals and history. Log each in STATE.md with its date.
7. **Acceptance:** UNKNOWN until defined. Once defined, give stable IDs and never renumber or silently change meanings.

## Read and resume (no handoff message is ever needed)
Read in order: BOOT.md (this file), STATE.md, NEXT_TASK.md, CHECKPOINT.md, INBOX_<your name>.md, then live branch HEAD and the latest five commits. Never load a file over ~1,500 words whole; read large files by section.
**Recovery:** if CHECKPOINT.md says IN PROGRESS, or commits post-date it, first read those commit messages and changed paths, write a `RECOVERED:` note in CHECKPOINT.md saying what landed and what did not, then do one unit.

## Working rules
- **Turn budget (hard):** at most 5 commits, 10 tool calls and 3 files read per turn; each commit at most 2 files and about 200 changed lines; never rewrite or reconstruct a large file. No Think, Work or agent mode, no autonomous loops. First action: overwrite CHECKPOINT.md with `IN PROGRESS: unit, files, time`. Last action: `DONE` plus commit SHAs and the next step. Reply in at most 10 lines and stop; the owner says "continue".
- Commit before summarizing; chat replies can vanish, commits do not.
- One lead writer per branch or work item; other AIs review or take disjoint files. Re-fetch file SHAs after a rejected update.
- Move or archive rather than delete.
- Coordinate through INBOX_<name>.md. If GitHub read or write is unavailable, say so and stop.

## Roles
ChatGPT: lead, continuity, evidence reconciliation. Claude: reviewer and small verified tasks. Gemini and Grok: reviewers without repo access; they work from files the owner pastes and answer with TASK, RESULT, FILES CHANGED, NEXT, OPEN QUESTIONS.
