# CLOUDCLI UI (siteboon/claudecodeui, formerly "Claude Code UI") vs POCKETCODE: flow comparison (strategy question 1, third entry)

Written 2026-11-23 by Claude. Sources, public, read 2026-11-23 as search-result excerpts of the project's README (github.com/siteboon/claudecodeui and its raw README) plus an Arch Linux package page and a GitHub list entry (secondary). Tags: VERIFIED (stated on a page named here), INFERRED, UNKNOWN, NOT READ. NOT READ: source code, the LICENSE text, docs site, releases, issue tracker; stars and activity were not read. Nothing here claims anything about PocketCode that is built.

## 1. What it is (VERIFIED from the README excerpts)
- A web UI (responsive, installable as a PWA) for Claude Code, Cursor CLI, Codex and Gemini CLI: session list, chat, file explorer, Git, MCP configuration, a shell terminal and a REST API. It reads and writes the same ~/.claude configuration the CLI uses, and discovers all existing sessions from that folder.
- Three ways to run it. (a) Self-hosted with npm (`npx @siteboon/claude-code-ui`, Node 22+): runs on your own machine; the machine must stay on; "mobile access: any browser on your network". (b) Docker sandbox, marked experimental: a microVM-isolated agent via the `sbx` CLI, also reached by any browser on your network. (c) CloudCLI Cloud: a managed container environment from $7 a month on top of your own AI subscriptions; the machine need not stay on; a native app is described as "coming".
- Safety default: all Claude Code tools are disabled until enabled in settings. A plugin system adds tabs from git repositories (examples listed: web terminal, scheduler, task queue, issues board).
- Positioning: the README argues it differs from Claude Code's own Remote Control feature, which it describes as limited to the one active session, needing the machine on and timing out after about ten minutes offline (a vendor-adjacent claim; not checked against Anthropic's documents).

## 2. Licence (VERIFIED, with a conflict)
- The README states AGPL-3.0-or-later, with additional terms under Section 7; the Arch package page agrees. An older awesome-list entry says GPL-3.0. Treat the current README as authoritative and the LICENSE text as NOT READ.
- Consequence (INFERRED): AGPL covers modified versions run as a network service. Code reuse in a PocketCode service or app is rejected by default (REUSE_BACKLOG rule); flow ideas only.

## 3. Compared with the others and with PocketCode
| Topic | CloudCLI | Happy / Vibe Kanban (earlier entries) | PocketCode (planned, not built) |
|---|---|---|---|
| Phone access | browser or PWA to a server you run, on your network; away from home needs your own tunnel or the paid Cloud | native apps with an encrypted relay (Happy); browser over a tunnel (Vibe Kanban) | the stated focus; hybrid direction |
| Where work runs | your machine, a local microVM, or their cloud | your machine | no remote lane chosen; local lane only a candidate (R-P2) |
| Cost | free self-hosted; Cloud from $7 a month | free (Happy core); free, company closed (Vibe Kanban) | $0 (D-006) |
| Approval model | tools disabled until enabled in settings | per-tool approvals on the phone (Happy) | release-grant and ResultReceipt research |

## 4. Implications for PocketCode (INFERRED; no claim about what PocketCode does)
- The common gap across all three is the same: an agent that runs on a computer the owner must keep on and reach. First-party phone access to Claude Code also exists in Anthropic's apps (UNKNOWN details; check Anthropic's documents before any comparison is published), so "control Claude Code from a phone" is not unique. Distinctive territory, if any, is what happens without a computer on (the local lane) and the review and receipt step; both need built, tested evidence before being claimed.
- A web UI that exposes a shell terminal on a home machine is an exposure risk the owner should understand; any PocketCode remote lane needs a threat model first (the existing relay-fencing and origin-isolation research applies).
- Pattern worth noting: sessions are discovered from the agent's own folder rather than a second store, which avoids a sync problem.

## 5. Next cheap steps
1. Read the LICENSE and the Section 7 additional terms if any code idea is ever considered.
2. Check Anthropic's documents on Claude Code from the mobile app so the comparison table can name it accurately.
3. Cline and Aider are covered in the next entry.
