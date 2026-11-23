# CLINE and AIDER vs POCKETCODE: flow comparison, plus roll-up of strategy question 1

Written 2026-11-23 by Claude. Sources, public, read 2026-11-23 as search-result excerpts of the Cline README (raw.githubusercontent.com/cline/cline and github.com/cline/cline), cline.bot, and the Aider README (raw.githubusercontent.com/aider-ai/aider and package pages); several results were forks, which were ignored. Tags: VERIFIED (stated on a page named here), INFERRED, UNKNOWN, NOT READ. NOT READ: source code, LICENSE files, docs sites, release notes, and anything about pricing beyond what is quoted. Nothing here claims anything about PocketCode that is built.

## 1. Cline
- VERIFIED: "the open source coding agent in your IDE, terminal & desktop", Apache 2.0, © 2026 Cline Bot Inc. Products on one agent engine: SDK (`npm install @cline/sdk`), CLI (`npm i -g cline`; interactive or fully headless for CI), VS Code extension, a new desktop app, a JetBrains plugin (closed source), and a Kanban app named in the README.
- VERIFIED: Plan mode then Act mode; approve every step or switch on auto-approve; checkpoints with one-click undo; project rules in `.clinerules`; MCP servers and plugins; multi-agent teams; scheduled runs (cron syntax in the README).
- VERIFIED, relevant to phones: connectors to Telegram, Slack, Discord, Google Chat, WhatsApp and Linear, where each conversation thread maps to an agent session, with access control for who may talk to the agent (`cline connect slack ...`). UNKNOWN: where that process must run (almost certainly on a machine or server the user keeps on) and how permissions are shown in a chat.
- Marketing claims, not verified: "trusted by 11M+ developers"; the site header showed about 72k GitHub stars.

## 2. Aider
- VERIFIED: "AI pair programming in your terminal". Repo map of the codebase; every change is committed automatically with a sensible message, so ordinary git diff and undo work; lint and test loop after each edit; voice-to-code; "watch" mode where comments added in any editor trigger edits; images and URLs in the chat; cloud or local models; a browser copy-and-paste workflow with web chat UIs.
- UNKNOWN today: the licence (not shown in the excerpts; believed permissive, verify before any reuse) and whether any official phone or web UI exists (none mentioned).

## 3. Compared with PocketCode (INFERRED; no claim about what PocketCode does)
| Topic | Cline | Aider | PocketCode (planned, not built) |
|---|---|---|---|
| Phone route | chat connectors (Telegram, WhatsApp, Slack) to an agent running elsewhere | none documented | the stated focus |
| Approval model | per-step approval or auto-approve; checkpoints | edits applied, committed, undone with git | release-grant and ResultReceipt research |
| Evidence and rollback | checkpoints and timeline | one git commit per AI change | receipts bound to exact commands and results |
| Cost | free tool, bring your own model key | free tool, bring your own model key | $0 (D-006) |

- Ideas worth testing, not claiming: (a) a chat-thread-per-task phone route is the cheapest proven way to reach an agent from a phone, so PocketCode's own app must beat it on approvals and safety, not on reach; (b) "every AI change is a git commit" is a clean basis for rollback and for tying a receipt to an exact result; (c) the approval spectrum (approve each step, auto-approve) shows the product must state where it sits and why.

## 4. Roll-up of strategy question 1 (five tools read: Happy, Vibe Kanban, CloudCLI, Cline, Aider)
- INFERRED, limited to what I read: all five run the agent on a computer or server the owner controls and keep on; the phone is a window onto it. None of the excerpts documents an agent that keeps working with no computer on, or a receipt that binds an approval to an exact command and its result. Those two are the candidate differentiators; both are unbuilt, so neither may be claimed publicly yet. Absence in excerpts is not proof of absence in the products.
- Not unique, so do not claim: phone control of Claude Code and Codex (Happy, CloudCLI, Cline connectors, and first-party options), multi-agent orchestration (Happy, Vibe Kanban, Cline teams), a plan-then-act flow (Cline, Vibe Kanban), free bring-your-own-key use.
- Risk: the vendor behind Vibe Kanban shut down within a year of a large following; a $0 project should keep user data exportable and avoid depending on one hosted service.
- Open before any public positioning: read Anthropic's documents on Claude Code from the Claude mobile app, and the LICENSE files for Aider and CloudCLI (AGPL, Section 7 terms).
