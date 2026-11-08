# STATE: PocketCode   (current state only; under 900 words)
Updated: 2026-11-08 by Claude. Sources: RECONCILIATION_2026-11-07.md (ChatGPT), NEW_CHAT_HANDOFF_20261106.md, owner handoff text, Claude's own reads of the release-grant files. Claude has not run the repository test suite.

## Status
- Phase: Discovery and product definition. No runtime or provider selected. The branch is hundreds of commits ahead of main; that is history, not progress.
- VERIFIED (per RECONCILIATION): GitHub Actions run 42365455316 on commit 744cb4d, workflow "PocketCode Python conformance tests", job unittest: 266/266 PASS. Earlier intermediate commits that evening were red and fixed by later commits; the failure emails were those runs. The result for the current HEAD must be checked, not assumed.
- COMMITTED: intent/proof separation; exact receipt-revision authorization binding; current-grant recovery; concurrency and crash specification; sequential grant model and tests; research and red-team packet.
- CLAIMED ONLY (not built): durable adapter; real concurrent processes; transactional outbox relay; durable crash recovery; production fencing; transport stream ownership and revocation; trusted policy authority; client receipt.
- Claude's independent P39 review (2026-11-08, delivered to the owner as CLAUDE_P39_INDEPENDENT_REVIEW_2026-11-08.md, not committed at ChatGPT's request): P39-S1, S2, S3 CONFIRMED (blocking for use of the sequential model as an adapter oracle), S4 refined (contract gap, not a model defect). New findings: caller-supplied clock in lease logic (BLOCKING), revocation checked on a stale snapshot, non-unique grant IDs across restarts. Evidence: counterexamples executed against a byte-verified copy of scripts/release_grant_conformance.py at 744cb4d. Not reviewed: result_receipts.py and tests, durable adapter contract, PROJECT_STATUS, ROADMAP, STATE_LEDGER.
- Event journal prototype: in memory, 21/21 local tests; producer identity is not cryptographic; fence check plus append is not atomic. Fake coordinator: 14 harness tests on test doubles. Both from the owner handoff.
- Pyodios on the owner's iPhone (owner-reported): v1.1.0 build 7, Pyodide 314.0.5, Python 3.14.2. First Editor run showed only "[Bridge/executePython] PythonError"; Console probe NOT RUN; bridge cause UNKNOWN.
- Product program (new, research only): iPhone-only App Store roadmap, website audit and PoCo page plan, governance audit; tracker in STRATEGY_PROGRAM_20261108.md.

## Decisions
- D-001 unified PC-and-phone direction, separate development boundaries. D-002 GitHub is source of truth. D-003 no secrets in the public repo. D-004 validate before stack commitment. D-005 zero spend.
- OpenHands and Cline are pattern references only; reject Cline's wildcard auto-approve default. MCP Tasks and ACP are optional adapters and never replace PocketCode command and attempt identity.
- No durable store is chosen until an atomic persistence contract is defined and tested.
- CASE-04 stays INCOMPLETE / timed_out; no precedence-only patch to scripts/report_contract.py until child-exit, wrapper-exit and termination provenance are resolved.
- 2026-11-07 (owner): old process rules may be revised; AGENTS.md now carries tiered decision rights.
- 2026-11-08 (owner, brief): PocketCode is officially considered for renaming to PoCo; the existing website design must not change; no PoCo claim beyond what is built. Nothing is renamed yet.

## Open items
- O-1 Owner: run the read-only Pyodios Console probe (PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md).
- O-2 ChatGPT: decide ACCEPT / REJECT / NEEDS-OWNER on each finding of CLAUDE_REVIEW_RELEASE_GRANT_RESEARCH_20261108.md and the full P39 review; Gemini's independent review pending.
- O-3 Run the full Python suite in a real checkout or CI and record exact-SHA results.
- O-4 Define the atomic persistence contract a durable adapter must satisfy.
- O-5 Resolve typed child exit vs wrapper exit vs termination provenance (NEXT_TASK.md).
- O-6 Recommended next slice P40: event chain and relay slice in the sequential model (see the full P39 review section 7).
- O-7 Owner decisions for the product program: the name PoCo (check App Store name, trademark and domain first), whether to spend US$99 on the Apple Developer Program, LinkedIn text, whether to put a pointer banner on main.
- O-8 Strategy research still to do: Apple design engineering, PoCo context engineering and provider caching, the rest of the website audit.

## Known risks
- Entry files from before 2026-11-07 are far too large for a free chat. Start from BOOT, STATE, NEXT_TASK, CHECKPOINT, INBOX only.
- Chats can freeze on "Stopped thinking" while commits continue; check commits, not the chat (kit/docs/STUCK_CHAT_FORENSICS.md).
- The classification of older documents in INDEX.md is by filename and date, not by reading them.
