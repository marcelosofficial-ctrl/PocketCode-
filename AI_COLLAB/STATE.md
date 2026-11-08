# STATE: PocketCode   (current state only; under 900 words)
Updated: 2026-11-08 by ChatGPT. Sources: RECONCILIATION_2026-11-07.md (ChatGPT), NEW_CHAT_HANDOFF_20261106.md, owner handoff text. Claude did not re-run tests.

## Status
- Phase: Discovery and product definition. No runtime or provider selected. Branch is hundreds of commits ahead of main; that is history, not progress.
- VERIFIED (per RECONCILIATION): GitHub Actions run 42365455316 on commit 744cb4d, workflow "PocketCode Python conformance tests", job unittest: 266/266 PASS.
- Several earlier commits that evening were red (933c732, 89bc1aa, e99c67c, b3bd2d2, 2504eb1: assertion, KeyError and TypeError failures in the release-grant model tests) because commits were pushed in quick sequences and fixed by later commits. The failure emails were these intermediate runs. The run result for the current HEAD must be checked, not assumed.
- COMMITTED: intent/proof separation; exact receipt-revision authorization binding; current-grant recovery; concurrency and crash specification; sequential grant model and tests; research and red-team packet.
- CLAIMED ONLY (not built): durable adapter; real concurrent processes; transactional outbox relay; durable crash recovery; production fencing; transport stream ownership and revocation; trusted policy authority; client receipt.
- Event journal prototype: in memory, 21/21 local tests; producer identity is not cryptographic; fence check plus append is not atomic. Fake coordinator: 14 harness tests on test doubles, not canonical. Both from the owner handoff, not re-verified by Claude.
- Pyodios on the owner's iPhone (owner-reported): v1.1.0 build 7, Pyodide 314.0.5, Python 3.14.2. First Editor run showed only "[Bridge/executePython] PythonError". The existing summary.json exactly matches the success oracle (owner-inspected). Error Log shows only "Editor: PythonError". Console probe for sys.last_exc: NOT RUN. Bridge cause and child exit status: UNKNOWN. Export/read-back, relaunch persistence and malformed-input test: NOT RUN.

## Decisions
- D-001 unified PC-and-phone direction, separate development boundaries. D-002 GitHub is source of truth. D-003 no secrets in the public repo. D-004 validate before stack commitment. D-005 zero spend.
- OpenHands and Cline are pattern references only; reject Cline's wildcard auto-approve default. MCP Tasks and ACP are optional adapters and never replace PocketCode command and attempt identity.
- No durable store (SQLite, PostgreSQL, Redis, cloud) is chosen until an atomic persistence contract is defined and tested.
- CASE-04 stays INCOMPLETE / timed_out. No precedence-only patch to scripts/report_contract.py until child-exit, wrapper-exit and termination provenance are resolved.
- 2026-11-07 (owner): old process rules may be revised for efficiency. AGENTS.md now carries the revised decision rights.

## Open items
- O-1 Owner: run the read-only Pyodios Console probe (steps in PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md). Blocks the device evidence.
- O-2 Independent adversarial reviews (Claude, Gemini) of RELEASE_GRANT_ADAPTER_RESEARCH_AND_REDTAM_20261107.md and the P39 static audit, before any adapter selection. Messages are in INBOX_claude.md and INBOX_gemini.md.
- O-3 Run the full Python suite in a real checkout or CI and record exact-SHA results.
- O-4 Define the atomic persistence contract a durable adapter must satisfy.
- O-5 Drafted EXIT_PROVENANCE_RESOLUTION_20261108.md with conservative typed-observation rules and EP-01..EP-20 proposed tests. Pending independent Claude review and owner resolution; no code change authorized.
- O-6 Compare one free local path (a-Shell or Carnets) only if it adds information.

## Known risks
- Old entry files are far too large for a free chat (see BOOT). New chats must start from BOOT, STATE and NEXT_TASK only.
- Rapid-fire commits create red intermediate CI runs and email noise; ChatGPT chats can freeze on "Stopped thinking" while work continues. Always check commits, not the chat (kit/docs/STUCK_CHAT_FORENSICS.md).
- The classification of older documents in INDEX.md is by filename and date, not by reading them.
