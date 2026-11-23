# VIBE KANBAN (BloopAI/vibe-kanban) vs POCKETCODE: flow comparison (strategy question 1, second entry)

Written 2026-11-23 by Claude. Sources, all public, read 2026-11-23: the repository README page (github.com/BloopAI/vibe-kanban), search snippets of the company's shutdown post (vibekanban.com/blog/shutdown, "Goodbye bloop", 2026-04-10), the GitHub releases page, the AI Engineer organisation page and two third-party write-ups (aiidelist.com, agentsroom.dev; both secondary). Tags: VERIFIED (read today on a page named here), INFERRED, UNKNOWN, NOT READ. NOT READ: source code, docs/, mobile-testing.md, the full shutdown post (only snippets). Nothing here claims anything about PocketCode that is built.

## 1. Status (the most important fact)
- VERIFIED: bloop, the company behind it, announced its shutdown on 2026-04-10; the project "will live on, open source and community maintained". Subscriptions ended and recent invoices were refunded; hosted services were to end after 30 days and the product move to a fully local design (AI Engineer page; third-party pages agree).
- VERIFIED: the repository stays online, Apache-2.0, about 28.1k stars, 3k forks, 2,080 commits. The README opens with "Vibe Kanban is sunsetting". Release v0.1.44 (tag dated 2026-04-24) includes "Sunset project routes to an export-only page". An open pull request titled "chore: disable shutdown banners" shows community members working on the repo.
- UNKNOWN: who maintains it now, how often it ships, and whether any fork has taken over. Third-party sources say "community maintained" without naming maintainers.

## 2. What it is (VERIFIED from the README)
- A planning and review layer above coding agents, not an agent: kanban issues become workspaces; each workspace gives an agent its own git worktree and branch, a terminal and a dev server.
- Diff review with inline comments sent back to the agent; a built-in browser preview with devtools and device emulation; pull-request creation with generated descriptions, then merge on GitHub.
- Runs locally with `npx vibe-kanban`; agents supported include Claude Code, Codex, Gemini CLI, GitHub Copilot, Amp, Cursor, OpenCode, Droid, CCR and Qwen Code.
- Remote use: run it on a server and reach the web UI through a tunnel (the README names Cloudflare Tunnel and ngrok) with SSH-based editor links; environment variables for a relay tunnel mode exist (`VK_TUNNEL`, relay API base). UNKNOWN: whether the relay still works after the hosted services ended, and whether it is end-to-end encrypted (NOT READ).
- Privacy: analytics is a build-time option (PostHog key empty means off); a third-party note says to treat agent credentials and worktree shell access as sensitive. Agents run on the user's machine with the user's own logins.

## 3. Compared with Happy and with PocketCode
| Topic | Vibe Kanban (VERIFIED unless marked) | Happy (see COMPETITOR_FLOW_HAPPY_20261122.md) | PocketCode (planned, not built) |
|---|---|---|---|
| Role | board, isolated workspaces, review | phone remote for agents on a computer | phone-first control plane; hybrid execution direction |
| Where work runs | the user's computer or a server the user runs | the user's computer | no remote lane chosen; local lane only a candidate (R-P2) |
| Phone story | browser UI over a tunnel; mobile-testing.md exists (NOT READ) | native apps, push approvals, encrypted relay | the stated focus |
| Business | company shut down; free, community-maintained | free core, paid voice | $0 (D-006) |

## 4. Implications for PocketCode (INFERRED; nothing here is a claim about what PocketCode does)
- The "plan, isolate, review, merge" flow drew 28k stars, so the category is real; the vendor failing shows a free tool is hard to fund. A $0 open-source plan is realistic only if it stays small and the maintenance cost is honest.
- A board that plans work is not a differentiator for PocketCode; the review step is where a phone helps most (approve or reject a diff on a phone). Candidate differentiator to test, not to claim: an exact-bound approval plus result receipt on that review step (release-grant and ResultReceipt research).
- Reuse: Apache-2.0 permits reuse with attribution and NOTICE handling. The upstream is unmaintained or thinly maintained, so adopt patterns (worktree per task, inline diff comments fed back to the agent, export-only sunset page) rather than depend on the code. Read LICENSE and NOTICE, and pin a commit, before taking any code (REUSE_BACKLOG rules).
- Risk to record: a tool the owner relies on can disappear with 30 days' notice; PocketCode should keep user data exportable.

## 5. Next cheap steps (each one turn)
1. Read docs for the relay and tunnel design and mobile-testing.md (phone behaviour).
2. Continue question 1 with the same format: CloudCLI (AGPL, flow comparison only), then Cline and Aider.
3. Update the tracker row and add a short summary table across the four tools once all four are done.
