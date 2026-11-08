# REUSE BACKLOG: PocketCode   (open-source code and patterns to adopt instead of writing from scratch)
Updated 2026-11-07 by Claude. Tags: [V] checked on a primary page, [S] secondary, [K] from memory, not re-checked. Source: Claude's open-source research master (2026-11-01) and review of Gemini's report. Reconcile with COMPETITOR_FEATURE_AND_OPEN_SOURCE_REUSE_DEEP_DIVE_20261105.md and OPEN_SOURCE_REUSE_AUDIT_20261029.md before acting (Claude has not read them).

Rules for every adoption: pin repo and commit; read the LICENSE file; record it in AI_COLLAB/THIRD_PARTY.md (create on first adoption); prototype only under prototypes/; no dependency enters scripts/ without a D-decision; $0 only; patterns first, code second.

| ID | Candidate | Licence | What it gives PocketCode | First small step (phone-doable) | Gate |
|---|---|---|---|---|---|
| R-P1 | CodeMirror 6 | MIT [K] | touch-capable editor; Replit moved its mobile IDE to it, Monaco lacks touch support [V reports] | spike page in prototypes/ editing one file on iPhone Safari | none |
| R-P2 | Pyodide in a Web Worker (terminate, memory guard) | MPL-2.0 [K] | local lane for light tasks. Pyodios reports ~300 MB heap, no interrupt [S] | wait for O-1 device evidence, then decide in-app vs competitor path | owner device test |
| R-P3 | Agent Client Protocol (agentclientprotocol, SDKs TS/Py/Rust/Kotlin/Java) | Apache-2.0 [S] | one client for many agents; permission prompts map to phone approvals | read-only session viewer design note; stays an optional adapter, never replaces PocketCode command identity | provider-neutral boundary contract |
| R-P4 | slopus/happy (Expo app, CLI wrapper, E2E sync) | MIT [V] | closest prior art: pairing, E2E, push approvals | read packages/happy-app pairing and crypto code; write a 1-page comparison | none |
| R-P5 | isomorphic-git + LightningFS | MIT; all deps MIT [V licenses.dev]. NOT @isomorphic-git/pgp-plugin: LGPL-3.0+ [V] | git on the phone, no PC | clone/diff spike in prototypes/ | none |
| R-P6 | Aider repo map (aider/repomap.py: tree-sitter tags, PageRank, token budget) | Apache-2.0 [V] | a ranked, token-budgeted code map for AI context; directly helps small-context chats | stdlib-only ast map of scripts/ as an EXTRACT file to test value | none |
| R-P7 | Cline SDK: packages/core/src/cron/ SQLite claim/renew queue; hub auth token; compaction with hash-validated state | Apache-2.0 [S]; design read in sdk/ARCHITECTURE.md [V] | atomic claim and renew pattern for the durable adapter contract (open item O-4) | read cron/ source and write a 1-page note mapping to the release-grant model | none |
| R-P8 | Anthropic sandbox-runtime (srt) or bubblewrap | Apache-2.0 / LGPL-2.0+ [V/K] | remote Linux sandbox policy shape (filesystem and egress allowlist) | note only; remote execution not chosen | owner decision on remote lane |
| R-P9 | DSSE envelope + in-toto Statement | Apache-2.0 [K]; spec files checked [V] | integrity format for ResultReceipt and artifact digests | map ResultReceipt fields to an in-toto Statement in a note | none |
| R-P10 | Tailscale free tier + SSH | proprietary free tier [S] | $0 transport to a home machine; plan limits vary by source | note only | owner decision |

Rejected for PocketCode: Monaco on mobile; CloudCLI code (AGPL-3.0); Restate server (BSL) and Temporal as dependencies; MinIO (archived, AGPL); River (Go library, wrong stack).
