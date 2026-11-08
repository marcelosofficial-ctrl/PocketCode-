# Plugin and competitor lessons for our work method

What we studied, what we adopted, what we skipped. Tags: [V] read on a primary page this session, [S] secondary or vendor claim.

| Source | Idea | Decision |
|---|---|---|
| Ponytail (lazy senior developer skill; ships rule files for AGENTS.md, .cursor, .clinerules and others) [V README via a mirror] | reuse before writing, standard library first, no speculative features, tiny diffs | ADOPTED as the lean rules in WORK_PROTOCOL section 3. Its benchmark (about 54% less code) is the author's own; independent JetBrains testing credited about 10% [S] |
| Caveman (terse speech skill) [S] | cut output tokens about 65% (vendor claim) | SKIPPED as a style. In Ponytail's benchmark the terse-prose control used slightly MORE tokens and cost [V README]. We keep the lean output contract (15-line replies) in plain language instead |
| rtk (CLI proxy that filters command output before the model sees it) [S] | do not let raw logs reach the model | ADOPTED as a rule: read only the first failing assertion of a failed CI job; never paste logs. The tool needs a CLI hook, so it does not apply to free chat |
| codegraph (pre-indexed SQLite code graph served over MCP) [S] | give the AI a map instead of files | ADOPTED as INDEX.md and extracts now; Aider-style repo map is a backlog item (REUSE_BACKLOG.md) |
| context-mode (keeps big tool output and session memory outside the context window) [S] | memory outside the chat | ADOPTED: the repo is the memory (STATE, CHECKPOINT, INBOX) |
| tokless (one-command installer for the above) [S] | wiring is the cost | NOT NEEDED: our wiring is plain files |
| Cline Memory Bank [V docs] | small fixed set of docs rebuilt into context; activeContext holds current state, not a log | ADOPTED with word budgets and tiers instead of "read every file every time" |
| AGENTS.md convention [V repo] | one entry file every tool reads | ADOPTED: AGENTS.md points at BOOT.md |

Not yet tried: running a repo-map generator in CI; a code-graph index. See REUSE_BACKLOG.md.
