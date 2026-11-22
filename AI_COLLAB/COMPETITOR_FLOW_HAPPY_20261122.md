# HAPPY (slopus/happy) vs POCKETCODE: flow comparison (REUSE_BACKLOG R-P4; strategy question 1)

Written 2026-11-22 by Claude. Sources, all public, read on 2026-11-22: the repository page and README, docs/encryption.md, docs/permission-resolution.md, docs/api.md and PRIVACY.md (last updated 2026-10-08) in slopus/happy; App Store listing text from search snippets. Tags: VERIFIED (read today), INFERRED, UNKNOWN, NOT READ. NOT READ: all source code (encryption.ts, auth.ts, runClaude.ts, the pairing screens), so everything below about behaviour is what the documents say, and documents can drift from code. Nothing here claims anything about PocketCode that is built.

## 1. What Happy is now (it has grown since the 2026-11-19 note)
- VERIFIED: MIT licence, 24.7k stars, 2.1k forks, 5,104 commits. Description: "Orchestrate Claude, Codex and Grok in one app"; reuses subscriptions the user already pays for.
- VERIFIED: agents run on the user's own computer. Three entry points: the original CLI wrapper (`happy claude`, `happy codex`; a session restarts in remote mode when the phone takes control, any key returns it), a desktop app for macOS, Windows and Linux on the Happy Agent runtime, and the mobile app (iOS, Android, web). Models: Claude, Codex, Grok, Gemini (through Antigravity), OpenCode and any Agent Client Protocol agent. Sessions can be shared with another person ("multiplayer").
- VERIFIED: components are a relay server (Postgres), a push server (Cloudflare Worker for APNs and FCM) and native Swift and Kotlin apps per the README package list. UNKNOWN which mobile app ships today: docs still cite an Expo app at packages/happy-app, and the README list does not include it. R-P4's pointer to packages/happy-app is therefore unverified.
- VERIFIED: the store app is free with in-app purchases (one listing shows "Plus Monthly USD 19.99"); PRIVACY.md says the subscription is for the optional voice feature. UNKNOWN what Plus unlocks beyond that.
- Correction to the 2026-11-19 note: "wraps Claude Code and Codex on the user's computer" is now only the original CLI. Happy is moving into multi-model orchestration, which is the space PocketCode describes itself in.

## 2. Flow (from the documents)
- Pairing: the computer makes a keypair and posts an auth request (`POST /v1/auth/request`); the signed-in phone approves it (`POST /v1/auth/response`). The account is a public key proved by signature; no email. VERIFIED. UNKNOWN: what the approval `response` carries (NOT READ in code).
- Session: the computer creates the session and encrypts metadata, agent state and messages before upload; the server stores opaque blobs and fans them out by WebSocket; the phone sends encrypted messages back. VERIFIED.
- Approvals: pending tool requests live in encrypted agent state as {tool, arguments}; decisions are approved, approved_for_session, denied or abort. Modes: default, acceptEdits, bypassPermissions, plan, read-only, safe-yolo, yolo. VERIFIED.

## 3. Crypto, trust and privacy (documents; code NOT READ)
- VERIFIED: two variants. Legacy: NaCl secretbox (XSalsa20-Poly1305) with a shared 32-byte key. Newer: AES-256-GCM with a per-session or per-machine data key, wrapped with tweetnacl.box and an ephemeral keypair. The server is designed to be blind to content.
- VERIFIED, not encrypted: ids, tags, versions and timestamps; push tokens; device and session ids.
- VERIFIED, not end-to-end: GitHub OAuth tokens and vendor tokens (openai, anthropic, gemini) are stored on the server, encrypted under a server master secret. Whoever runs the server can use them.
- VERIFIED: PRIVACY.md documents PostHog product analytics (pseudonymous, opt-out in Settings), RevenueCat, and voice through ElevenLabs outside the end-to-end boundary; voice context can include pending permission requests with tool name and arguments. Copies of the older README in forks say "No telemetry, no tracking"; the current slopus README does not, so do not repeat that line about Happy.
- VERIFIED inconsistency: the README says the push server replaces Expo push; PRIVACY.md still names Expo. UNKNOWN which is current.

## 4. Where PocketCode differs, and what it must not claim yet
| Topic | Happy (VERIFIED unless marked) | PocketCode (planned or researched, not built) | Implication (INFERRED) |
|---|---|---|---|
| Where the agent runs | the user's computer; phone is the remote | hybrid direction; no remote lane chosen; local lane only a candidate (R-P2) | a "no computer needed" claim needs built, tested evidence first |
| Approval authority | the phone sends a permission mode inside each message; the CLI uses it when no sandbox is on, and yolo maps to bypassPermissions (documented; code NOT READ). Anyone holding the session key can request it | release-grant and ResultReceipt design from the P39 and P40 research | the candidate differentiator is an exact-bound grant plus a result receipt, not "approvals on a phone", which Happy already has. Claim only after it is built and tested |
| Server trust | opaque blobs, but vendor tokens and plaintext metadata on the server | no server chosen; $0 | if PocketCode ever relays, keep vendor tokens off the server and ids opaque |
| Price | core flow free, optional paid voice | D-006: spend nothing | no price differentiation |
| Breadth and maturity | six model families, desktop apps, sharing, large community | one owner, pre-product | do not compete on breadth; "orchestration" alone is not a differentiator |

## 5. Adopt and avoid (INFERRED; pin repo and commit and read LICENSE before any code is taken, per REUSE_BACKLOG rules)
- Adopt as patterns: public-key accounts with no email; request-and-approve terminal pairing; encrypted agent state holding pending-request objects; versioned optimistic updates (`expectedVersion`) on metadata and state; per-session data key wrapped by a box.
- Avoid: honouring a client-supplied permission mode as-is; storing vendor tokens server-side; plaintext identifiers and timestamps where avoidable; sending permission requests to a third party for voice.
- Licence: MIT shown on the repository page (VERIFIED); the LICENSE file text was not opened. No commit is pinned yet; none is needed until code is adopted.

## 6. Next cheap steps (each one turn)
1. Read packages/happy-cli/src/api/encryption.ts and the server auth module to check the documents, and read the pairing approval payload.
2. Settle which mobile app ships (happy-app or the native packages) and update R-P4.
3. Continue question 1 with the same format: Vibe Kanban, CloudCLI (AGPL, reuse rejected, flow comparison only), Cline, Aider. A Happy fork named Happier (Claude, Codex, Gemini, OpenCode; shared sessions) exists; not read beyond its store text.
