# STATE: PocketCode   (current state only; under 900 words)
Updated: 2026-11-09 by ChatGPT. Sources: live branch files, GitHub API state, Claude/Gemini P39 reconciliations, owner decision register and primary-source browser-storage/origin research. No PocketCode source/tests or device tests were run in this pass.

## Status
- Phase: Discovery and product definition. P39/exit-provenance gate remains CLOSED. No runtime/provider/database/transport selected. Branch divergence from main is history, not product progress.
- VERIFIED: Actions run 42365455316 on exact source/test SHA 744cb4dc7cd4994647c84ac7476d0c78a21f0540, workflow "PocketCode Python conformance tests", job unittest: 266/266 PASS. Historical source/test evidence only. Latest documentation-only HEAD had no check run; CI there is NOT RUN, not PASS/FAIL.
- COMMITTED: intent/proof separation; exact receipt-revision authorization binding; current-grant recovery; concurrency and crash specification; sequential grant model and tests; research and red-team packet.
- CLAIMED ONLY (not built): durable adapter; real concurrent processes; transactional outbox relay; durable crash recovery; production fencing; transport stream ownership and revocation; trusted policy authority; client receipt.
- Claude's P39 review is reconciled in P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md. Gemini's report was received and reconciled in GEMINI_P39_REVIEW_RECONCILIATION_20261109.md. Gemini's four headline claims require correction: S1 maps to a real progress-version/event gap in release_grant_conformance.py, not event_journal.py; S2's claimed result_receipts.verify_receipt() does not exist, but consume_event() trusts supplied event digest; S3's fake_outbox.py claim is contradicted by its lease/fence implementation, while the grant-event outbox lacks relay fencing; S4 is an adapter/MVP boundary. The receipt module was separately checked at blob 0d1588f, outside Gemini's six-file manifest. Gemini ran no tests. Claude's C1-C7 were run against a byte-verified copy, not the repository suite.
- Event journal prototype: in memory, 21/21 local tests; producer identity is not cryptographic; fence check plus append is not atomic. Fake coordinator: 14 harness tests on test doubles. Both from the owner handoff.
- Pyodios on the owner's iPhone (owner-reported): v1.1.0 build 7, Pyodide 314.0.5, Python 3.14.2. First Editor run showed only "[Bridge/executePython] PythonError"; Console probe NOT RUN; bridge cause UNKNOWN.
- Product program (research only): STRATEGY_PROGRAM_20261108.md; website audit, governance audit, iPhone roadmap and the no-spend PWA path are committed. No spending is authorized.
- COMMITTED PWA research: PWA_LOCAL_STORAGE_AND_RECOVERY_CONTRACT_20261109.md defines IndexedDB atomic metadata, OPFS staging/readback, local fencing, service-worker recovery and 22 proposed PWA tests. NO_SPEND_PWA_PATH_20261108.md corrected: WebKit Home Screen origins are ITP seven-day exempt and isolated from Safari, but still face quota/pressure/user clearing; iOS 26 Add to Home Screen includes Open as Web App; qualifying EU browsers may use entitled alternative engines. Owner device iOS/Safari build, persist() result, quota and lifecycle behavior remain UNKNOWN. No storage engine selected.
- COMMITTED origin-security research: `GITHUB_PAGES_ORIGIN_ISOLATION_AND_LOCAL_DATA_SECURITY_20261109.md` identifies a HIGH-priority conditional risk: GitHub Pages project paths under the same `<owner>.github.io` host are same-origin because URL paths do not partition origin-scoped IndexedDB/OPFS. Sibling same-origin scripts may access app storage. Actual Pages URL, sibling inventory, CSP and worker scope remain UNKNOWN; no deployment settings were changed. Ten proposed ORIGIN acceptance cases added as research only. This is a deployment threat-model finding, not proof of an observed exploit.

## Decisions
- D-001 unified PC-and-phone direction, separate development boundaries. D-002 GitHub is source of truth. D-003 no secrets in the public repo. D-004 validate before stack commitment. D-005 zero spend.
- D-006 (owner, 2026-11-08): no spending of any kind. No Apple Developer Program, TestFlight or App Store for now; distribution is the installable web app on GitHub Pages (NO_SPEND_PWA_PATH_20261108.md).
- Owner-delegated README banner on main is done (commit 319d3da); main otherwise unchanged. PR #2/#3 stay open drafts and untouched. PR #4 remains open/draft and untouched. ChatGPT's review found seven files (not six), 11 commits ahead / 312 behind, recommends no merge as-is, and records per-file disposition in PR4_CONTINUITY_REFINEMENT_RECONCILIATION_20261109.md. Useful unique rules were selectively integrated into BOOT and WORK_PROTOCOL; owner controls close/merge.
- OpenHands and Cline are pattern references only; reject Cline's wildcard auto-approve default. MCP Tasks and ACP are optional adapters and never replace PocketCode command and attempt identity.
- No durable store is chosen until an atomic persistence contract is defined and tested. Patterns and current source checks are recorded in P39_EVENT_RELAY_AND_EXIT_BOUNDARY_RESEARCH_20261109.md and PWA_LOCAL_STORAGE_AND_RECOVERY_CONTRACT_20261109.md; these do not select Temporal, NATS, Redis, PostgreSQL, SQLite, IndexedDB wrappers or Pyodide as a product dependency.
- CASE-04 stays INCOMPLETE / timed_out; no precedence-only patch to scripts/report_contract.py until child-exit, wrapper-exit and termination provenance are resolved.
- 2026-11-07 (owner): old process rules may be revised; AGENTS.md carries tiered decision rights. 2026-11-08 (owner): PocketCode is considered for renaming to PoCo; the website design must not change; no claim beyond what is built. Nothing is renamed yet.

## Open items
- O-1 Owner: run the read-only Pyodios Console probe (PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md).
- O-2 Gemini's P39 report is received and reconciled in `GEMINI_P39_REVIEW_RECONCILIATION_20261109.md`; the combined review matrix and gate plan are committed. Await any additional Claude artifact supplied by owner. Do not create a competing Claude request while its strategy assignment is OPEN. Owner OD-01..OD-13 remain OPEN.
- O-3 Run the full Python suite in a real checkout or CI and record exact-SHA results.
- O-4 Define the atomic persistence contract a durable adapter must satisfy, including browser origin isolation and same-origin sibling threat model before storing user workspace data.
- O-5 Resolve typed child exit vs wrapper exit vs termination provenance (NEXT_TASK.md).
- O-6 Recommended next slice P40: event chain and relay slice in the sequential model (P39 review section 7).
- O-7 Owner decisions still open: the name PoCo (check App Store name, trademark and domain first, even though the App Store is deferred); LinkedIn work waits for a laptop or a LinkedIn data export (about one month).
- O-8 Strategy research still to do: Apple design engineering for the web app, PoCo context engineering and provider caching, remaining website audit. This remains a separate Claude work lane.

## Known risks
- Chats can freeze on "Stopped thinking" while commits continue; check commits, not the chat (kit/docs/STUCK_CHAT_FORENSICS.md).
- The classification of older documents in INDEX.md is by filename and date, not by reading them.
