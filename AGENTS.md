# PocketCode Shared AI and Contributor Instructions

These rules apply to ChatGPT, Claude, Gemini, human contributors, and automation. This file is the common entry point; provider-specific instruction files should link here rather than contradict it.

## Start here (read this before anything else)
1. Read `AI_COLLAB/BOOT.md` on the active branch, then `AI_COLLAB/STATE.md`, `AI_COLLAB/NEXT_TASK.md` and your own `AI_COLLAB/INBOX_<name>.md`. Together they are under 2,000 words. Use `AI_COLLAB/INDEX.md` to find anything else.
2. Do not open the large history files (`CHAT_START_HERE.md`, `STATE_LEDGER_*.md`, `CHAT_WORK_LOG.md`, `NEW_CHAT_HANDOFF_*.md`, `PROJECT_STATUS.md`) whole; they exceed a free chat's context. Read a named section only.
3. The active branch is named in BOOT.md. `main` is stale.

## Source of truth

1. Current repository contents and commit history are authoritative for implementation state.
2. AI_COLLAB/STATE.md records current state and open items; PROJECT_STATUS.md is long history.
3. PRODUCT_SPEC.md, ARCHITECTURE.md, SECURITY.md, and ROADMAP.md record current proposals and constraints.
4. DECISIONS.md records decisions and their rationale.
5. Chat messages are discussion, not proof that repository changes or tests happened. The commit and its CI run are the proof.

Inspect relevant files and the current branch before claiming knowledge of project state.

## Working style

- Prefer a small number of substantial, verifiable tasks over many tiny speculative changes.
- Never claim tests, builds, deployments, or runtime behavior passed without evidence.
- Separate verified facts, assumptions, proposals, and open questions.
- Check existing files, issues, branches, and recent commits to avoid duplicate work.
- Do not introduce a large framework or paid service without explaining why it is needed.
- Do not mix PocketCode work with RevDev or other repositories.
- Keep the product provider-neutral unless a documented decision changes that direction.
- Optimize for an owner who may have only an iPhone and no PC access for an extended period.
- Keep chats small: one chat, one task; commit to GitHub before summarizing in chat; about 350 lines per turn (see AI_COLLAB/kit/docs/WORK_PROTOCOL.md).

## Git and public repository rules

- This repository is public. Never commit credentials, API keys, tokens, private user data, or secret configuration. No exceptions.
- Read existing files before replacing them and preserve owner-authored material unless asked to replace it.
- Do not add invented test results or placeholder success claims.
- Prefer focused commits. Rapid sequences of commits are fine, but judge CI by the latest commit and do not stack new work on a red latest commit.

### Decision rights (revised 2026-11-07; the owner delegated repository organization to Claude)
- Do freely: additive commits on the active branch; new docs, tests and branches; archiving or reorganizing documents when the full content stays in the repo (copy to ARCHIVE/ or new path, leave a pointer, log in AI_COLLAB/MOVES.tsv); opening new PRs; merging a PR into the active branch when its CI is green.
- Tell the owner first in one line, then proceed: merging into `main`; renaming or restructuring top-level folders; removing a file whose complete content is preserved elsewhere in the repo.
- Needs the owner's explicit OK each time: force-push or history rewrite; deleting a branch or any content not preserved elsewhere; changing visibility; publishing a release; enabling paid infrastructure; touching draft PR #2 or #3.

## Task protocol

1. Inspect relevant files and repository state.
2. State the goal and acceptance criteria.
3. Make the smallest coherent change.
4. Run available tests or clearly state why tests could not be run.
5. Inspect the diff/result.
6. Update AI_COLLAB/STATE.md, CHECKPOINT.md and decision documents when state meaningfully changes.
7. Report exact changed paths, commit/PR references, test evidence, and remaining risks.

## Cross-agent collaboration

- Assign one primary implementer per task.
- Other agents review requirements, edge cases, tests, and diffs rather than independently implementing the same task.
- AIs message each other through AI_COLLAB/INBOX_<name>.md (see AI_COLLAB/MAILBOX.md); the owner does not have to relay.
- Use branches and pull requests for meaningful code changes when possible.
- Share findings with evidence and file/line references.
- Resolve conflicts through documented decisions, not by having multiple agents overwrite the same file.
- Keep CLAUDE.md and GEMINI.md aligned with this file.

## Product discipline

- Treat product direction as a hypothesis until validated.
- Do not implement a public code runner without reviewed isolation and abuse controls.
- Do not promise broad runtime support before a tested execution contract exists.
- Favor exportability, honest limitations, mobile usability, and verifiable execution evidence.
