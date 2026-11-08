# GitHub governance audit: PocketCode (research, 2026-11-08)

Scope: AGENTS.md as it was before 2026-11-07, the 2026-11-06 handoff procedure, CI workflows, branch and PR state, and the process documents named in INDEX.md. Read: AGENTS.md, GEMINI.md, NEW_CHAT_HANDOFF_20261106.md, RECONCILIATION_2026-11-07.md, both workflow files. NOT read: CLAUDE.md (18 KB), CHAT_CONTINUITY_AND_MULTI_CHAT_OPERATING_PROTOCOL_20261106.md, other process documents. RevDev governance is a separate audit in the private repository. Classes: KEEP, UPDATE, REMOVE, ADD.

| # | Rule or practice | Class | Evidence | Action |
|---|---|---|---|---|
| 1 | Repository contents and commits are the source of truth; chat is not proof | KEEP | AGENTS.md; the 2026-11-07 stuck-chat evidence shows chat state is unreliable | already central |
| 2 | Never claim tests or runtime behaviour without evidence | KEEP | AGENTS.md | none |
| 3 | No secrets in the public repository | KEEP | AGENTS.md; repo is public | add the signing-secret rules from the iPhone roadmap when CI signing starts |
| 4 | One primary implementer per task; others review | KEEP | AGENTS.md | none |
| 5 | "Do not rewrite history, force-push or delete owner content without explicit approval" | UPDATE | blunt; blocked useful archiving | replaced 2026-11-07 by tiered decision rights in AGENTS.md |
| 6 | New chats must read CHAT_START_HERE.md and STATE_LEDGER first (handoff prompt of 2026-11-06) | REMOVE | those files are 51 KB and 71 KB; a free chat holds about 16K tokens (reported); stalls match | replaced by BOOT, STATE, NEXT_TASK (AGENTS.md start-here section) |
| 7 | Many overlapping handoff and bootstrap files (CHAT_HANDOFF, NEW_CHAT_HANDOFF x4, NEW_CHAT_BOOTSTRAP, CURRENT_CHECKPOINT) | UPDATE | each 18-109 KB; later ones say they continue earlier ones | keep as history; INDEX marks them history; stop creating new full handoffs; update STATE.md instead |
| 8 | A new full-size handoff at the end of every working session | REMOVE | cost and duplication; state now lives in STATE and CHECKPOINT | rule 'write-ahead commit, 150-word CHECKPOINT' |
| 9 | Exact-SHA CI evidence demanded for every commit (RECONCILIATION counts "NOT RUN" for docs-only commits) | UPDATE | the workflow only runs for scripts/ changes by design (path filter), so docs commits never have a run | judge CI on the latest commit that touched scripts/; do not treat NOT RUN on docs commits as a gap |
| 10 | CI: path filter and cancel-in-progress on the Python workflow | KEEP | .github/workflows/pocketcode-python-tests.yml | none |
| 11 | Rapid-fire commit sequences by one assistant | UPDATE | caused red intermediate runs and failure emails (RECONCILIATION) | batch related edits into one push where possible; judge by the latest commit |
| 12 | Repeated near-identical reconciliation and audit documents per day | UPDATE | many dated audit, matrix and checklist files (20261028, 20261029, G01-G08) | one RECONCILIATION per day; supersede, do not duplicate |
| 13 | Draft PRs #2 and #3 untouched | KEEP (owner decision) | PROJECT rules | owner should decide whether to close, update or merge; not changed |
| 14 | Default branch main is stale (early discovery README) and the active branch is far ahead | UPDATE | README on main; BOOT.md notes it | owner decision: add a pointer banner to main or merge a milestone via PR |
| 15 | AIs relayed through the owner by copy and paste | REMOVE | owner overload | INBOX files and MAILBOX.md |
| 16 | ADD: write-ahead rule (commit before summarizing) | ADD | stuck-chat evidence | in WORK_PROTOCOL |
| 17 | ADD: loop guard (three identical commit messages in a row means stop) | ADD | observed in RevDev on 2026-11-08 | in WORK_PROTOCOL |
| 18 | ADD: final chat reply of at most 15 lines | ADD | streaming reliability and token cost | in WORK_PROTOCOL |
| 19 | ADD: third-party ledger (repo, commit, licence) before reusing code | ADD | licences differ (MPL, LGPL, AGPL, BSL found in research) | THIRD_PARTY.md on first adoption |
| 20 | ADD: size budgets for entry files and extracts for large documents | ADD | 12 files of 50-110 KB | in WORK_PROTOCOL; INDEX size classes |
| 21 | ADD: pre-commit secret scan for a public repository | ADD (optional) | secrets would be public immediately | evaluate a free scanner workflow; weigh email noise |
| 22 | ADD: decision rights tiers | ADD | owner delegation 2026-11-07 | in AGENTS.md |

Do not remove: security boundaries, acceptance identifiers (LOOP-01..14, CASE-01..16), D-001..D-005, the $0 rule, the public-repository rules, the separation from RevDev.

Open owner decisions from this audit: item 13 (draft PRs), item 14 (main banner or milestone merge), item 21 (secret scan).
