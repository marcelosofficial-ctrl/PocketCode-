# STATE: PocketCode   (current state only; under 900 words)
Updated: 2026-11-09 by ChatGPT. Sources: live branch, GitHub API, P39 reconciliations and primary-source security/storage research. No source/tests or device tests run.

## Status
- Phase: Discovery/product definition. P39/exit-provenance gate CLOSED. No runtime/provider/database/transport selected.
- VERIFIED: Actions run 42365455316 on exact source/test SHA 744cb4dc7cd4994647c84ac7476d0c78a21f0540, workflow "PocketCode Python conformance tests", job unittest: 266/266 PASS. Historical source/test evidence only. Latest docs-only HEAD `920c7db9ff4c3740351840f71a3cf109699c197a` has zero check runs/statuses; CI is NOT RUN, not PASS/FAIL.
- COMMITTED: intent/proof separation, receipt-revision binding, grant recovery, concurrency/crash models and research.
- CLAIMED ONLY (not built): durable adapter; real concurrent processes; transactional outbox relay; durable crash recovery; production fencing; transport stream ownership and revocation; trusted policy authority; client receipt.
- Claude and Gemini P39 reviews are reconciled. Gemini attribution corrections: S1 is in release_grant_conformance.py, not event_journal.py; S2 names a nonexistent receipt function, but consume_event() trusts supplied digest; S3 misattributes FakeOutbox fencing, while grant-event relay lacks it; S4 is adapter/MVP scope. Receipt blob 0d1588f was separately checked. Gemini tests NOT RUN; Claude C1-C7 were against a byte-verified copy, not repo CI.
- Event journal (21/21) and fake coordinator (14 harness tests) are in-memory/test-double evidence only; no durable/authenticated adapter proof.
- Pyodios on the owner's iPhone (owner-reported): v1.1.0 build 7, Pyodide 314.0.5, Python 3.14.2. First Editor run showed only "[Bridge/executePython] PythonError"; Console probe NOT RUN; bridge cause UNKNOWN.
- Product, website and governance research is committed. No spending authorized.
- COMMITTED PWA research: PWA_LOCAL_STORAGE_AND_RECOVERY_CONTRACT_20261109.md defines IndexedDB atomic metadata, OPFS staging/readback, local fencing, service-worker recovery and 22 proposed PWA tests. NO_SPEND_PWA_PATH_20261108.md corrected: WebKit Home Screen origins are ITP seven-day exempt and isolated from Safari, but still face quota/pressure/user clearing; iOS 26 Add to Home Screen includes Open as Web App; qualifying EU browsers may use entitled alternative engines. Owner device iOS/Safari build, persist() result, quota and lifecycle behavior remain UNKNOWN. No storage engine selected.
- COMMITTED origin-security research: shared-host Pages paths are same-origin; sibling scripts may access IndexedDB/OPFS. Actual Pages URL/custom domain/sibling inventory/headers UNKNOWN. GitHub Pages custom response headers are not supported per GitHub staff response; meta CSP cannot apply CSP sandbox. No live exploit confirmed.
- COMMITTED deep research: `PHONE_FIRST_EXECUTION_AND_RECOVERY_REDTEAM_20261109.md` corrects seven prior weaknesses, defines execution modes, OPFS+IDB crash protocol and proposed ORIGIN/EXEC/PWA-ART tests. No implementation authorized.
- COMMITTED verification: `PAGES_AND_EXIT_PROVENANCE_VERIFICATION_20261110.md`. Repo metadata says Pages enabled, homepage null; main workflow deploys `prototypes/mobile-runner` and main tree has no CNAME. Exact URL/custom domain/deployed SHA/headers remain UNKNOWN. Python 3.15.2 docs exclude `subprocess` on iOS/Android/WASI; browser Worker termination has no returned exit code/ack event; Node exit and stdio-close are distinct. Adds PAGES-01..08 and EP-26..35 proposals; NOT RUN.

## Decisions
- D-001 unified PC-and-phone direction, separate development boundaries. D-002 GitHub is source of truth. D-003 no secrets in the public repo. D-004 validate before stack commitment. D-005 zero spend.
- D-006 (owner, 2026-11-08): no spending of any kind. No Apple Developer Program, TestFlight or App Store for now; distribution is the installable web app on GitHub Pages (NO_SPEND_PWA_PATH_20261108.md).
- README banner on main is done. PR #2/#3/#4 remain owner-controlled and untouched; PR #4 review recommends no merge as-is.
- OpenHands/Cline are references only; reject wildcard auto-approve. MCP Tasks/ACP do not replace PocketCode identity.
- No durable store selected. Event relay, PWA and origin research are contracts only; no database/runtime/provider dependency chosen.
- CASE-04 stays INCOMPLETE / timed_out; no precedence-only patch to scripts/report_contract.py until child-exit, wrapper-exit and termination provenance are resolved.
- 2026-11-07 (owner): old process rules may be revised; AGENTS.md carries tiered decision rights. 2026-11-08 (owner): PocketCode is considered for renaming to PoCo; the website design must not change; no claim beyond what is built. Nothing is renamed yet.

## Open items
- O-1 Owner: run the read-only Pyodios Console probe (PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md).
- O-2 Gemini's P39 report is received and reconciled in `GEMINI_P39_REVIEW_RECONCILIATION_20261109.md`; the combined review matrix and gate plan are committed. Await any additional Claude artifact supplied by owner. Do not create a competing Claude request while its strategy assignment is OPEN. Owner OD-01..OD-13 remain OPEN.
- O-3 Run the full Python suite in a real checkout or CI and record exact-SHA results.
- O-4 Pages is enabled and workflow is verified; still obtain exact Pages URL/custom domain/deployed SHA/live headers/sibling origin and finish storage threat model.
- O-5 Resolve typed child exit vs wrapper exit vs termination provenance; distinguish browser worker runner-observation from native child exit (NEXT_TASK.md).
- O-6 Recommended next slice P40: event chain and relay slice in the sequential model (P39 review section 7).
- O-7 PoCo name remains undecided; LinkedIn work waits for laptop/export.
- O-8 Remaining design/context/provider-cache research is a separate Claude lane.

## Known risks
- Chats can freeze on "Stopped thinking" while commits continue; check commits, not the chat (kit/docs/STUCK_CHAT_FORENSICS.md).
- The classification of older documents in INDEX.md is by filename and date, not by reading them.
