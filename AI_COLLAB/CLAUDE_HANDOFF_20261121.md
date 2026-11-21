# Claude handoff for a fresh chat (2026-11-21)

Purpose: let a new Claude chat in the owner's RevDev project continue without the long history. Public-safe: no secrets, no private RevDev status (the private RevDev notes are in the private repository DevRelay-Missions, resume/revdev/INBOX_claude.md).

## Role and rules
- Claude is the reviewer and small-task worker; ChatGPT leads each project. Claude also writes exact "do this now" briefs, reads large files the ChatGPT chats cannot, and fixes small verified things.
- Projects: RevDev (private repo DevRelay-Missions), PocketCode (public repo PocketCode-), LingoMingle (repo LingoMingle, branch lingomingle-foundation-2026-11-10), plus the portfolio site (repo portfolio) and the profile README (repo marcelosofficial-ctrl).
- Owner goals: a remote job; GitHub and the site are a showcase; personal apps are for fun and learning. The owner delegated decisions to Claude ("you're the boss") and wants exact copy-paste text and exact phone menu paths in the chat, not pointers to repo files.
- Evidence tags VERIFIED / INFERRED / UNKNOWN / NOT RUN; never claim tests passed without output; no secrets; RevDev material stays out of public repos.

## How things work
- Claude's GitHub connector token covers every repository (since 2026-11-17). Writes replace whole files (no patch call): check the file size after each write (an unchanged size after a one-token edit is a good sign) and avoid rewriting files over about 15 KB unless the change is worth it.
- Pull requests: the connector's PR form fails on the owner's phone. For the portfolio, push a branch, give the owner the compare link (github.com/<owner>/portfolio/compare/main...<branch>?expand=1&title=...), the owner taps Create pull request, Claude reads the check run (pull_request_read get_check_runs), squash merges (owner pre-authorized portfolio merges once the build passes), then confirms the "Deploy portfolio" success email.
- CI evidence: Claude cannot read Actions logs. GitHub emails every run since 2026-11-16 ("Run succeeded" / "Run failed" / cancelled) to the owner's Gmail; search from:notifications@github.com plus the repo name (a subject: filter with a trailing hyphen name can miss). For PocketCode the exact-head job mirrors failing tests into issue #5 ("CI log mirror (exact-head lane)") of PocketCode-; read it with issue_read get_comments. Emails can arrive minutes late.
- ChatGPT chats: three, one per project, deliberately limited (3 commits or 5, 6 to 10 tool calls, 10-line replies); the startup files do not count toward the read limit (rule in AI_PLATFORM_INSTRUCTIONS.md). The owner's useful prompt is "Do the next unit now." Exact units go in each repo's INBOX_chatgpt.md; Claude's own notes go in INBOX_claude.md (do not overwrite CHECKPOINT.md or NEXT_TASK.md).
- Settings text for ChatGPT, Claude, Gemini and Grok: AI_PLATFORM_INSTRUCTIONS.md. The owner pasted the latest ChatGPT block on 2026-11-21. UNKNOWN whether the owner pasted the latest Claude block into the Project instructions.

## State on 2026-11-21 (see the files for detail)
- Portfolio: pull requests #28 to #31 merged and deployed. Left: the two home pages (exact edits in SITE_FIX_PLAN_20261116.md) and the résumé PDF (the owner must upload a new file). Profile README rewritten with a photo and gallery; VektorDeck README got a screenshot.
- LinkedIn: draft in LINKEDIN_DRAFT_20261118.md; the owner is entering headline, About, Open to Work, skills, featured and experience. Featured link thumbnails are poor (same site preview or GitHub's card): plan was one portfolio link plus uploaded screenshots.
- PocketCode: VERIFIED (GitHub run email "Run succeeded: PocketCode Python conformance tests ... (ae16948)", 2026-11-21): the workflow, including the exact-head job, is green at ae16948 after Claude changed the one stale expectation in scripts/test_result_receipts.py to (4, 3, (2,)); 280 tests were run in the earlier failing run. NEXT: the PocketCode chat records this run in STATE.md (INBOX MSG 2026-11-21-1) and continues NEXT_TASK (receipt creation from the live journal, then the fake outbox timestamp work).
- RevDev: the lead audited the broker-death tests; Claude's inbox message MSG 2026-11-20-1 says the takeover mechanism exists (take_recovery_slot in authority_lifecycle_integration.py) and gives the next test unit. P0 stays open; no Windows evidence yet.
- LingoMingle: the chat closed an architecture pass on 2026-11-18; Grok is doing a long research pass (due the evening of 2026-11-21); device tests wait on the owner. The repo was made public temporarily; the owner has a reminder to set it back to private.
- Strategy tracker: STRATEGY_PROGRAM_20261108.md. Still open for Claude: Apple design (remaining HIG pages) and the competitor comparison (Happy Coder first: MIT, end-to-end encrypted relay, wraps Claude Code and Codex on the user's computer).

## First message to send in the new chat
"Continue. Read AI_COLLAB/CLAUDE_HANDOFF_20261121.md in PocketCode- (branch pocketcode-ai-workflow-director-research-2026-10-28), then check the three inboxes and the latest CI emails, and carry on."
