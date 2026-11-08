# STATE: PocketCode   (current state only; under 900 words)
Updated: 2026-11-08 by ChatGPT. Sources: pinned GitHub source/test reads at 744cb4d; P39 review dispositions and source-pinned crosswalk. Claude did not re-run tests.

## Status
- Phase: Discovery and product definition. No runtime or provider selected. Branch is hundreds of commits ahead of main; that is history, not progress.
- VERIFIED: GitHub Actions run 42365455316 on source/test SHA 744cb4d, workflow "PocketCode Python conformance tests", job unittest: 266/266 PASS. This is not a fresh run on current documentation HEAD.
- Earlier intermediate commits were red during rapid pushes; later source/test SHA 744cb4d produced the 266/266 result. Judge the latest commit's actual CI, never infer from older runs.
- COMMITTED: intent/proof separation; exact receipt-revision authorization binding; current-grant recovery; concurrency and crash specification; sequential grant model and tests; research/red-team packet; P39 interim dispositions; exit-provenance proposal; P39 source-pinned audit crosswalk.
- CLAIMED ONLY (not built): durable adapter; real concurrent processes; transactional grant-event relay; durable crash recovery; production fencing; transport stream ownership/revocation; trusted policy authority; client receipt.
- VERIFIED model gaps at pinned source/test SHA 744cb4d: P39-S1 aggregate version advances without matching event/outbox; S2 consumer trusts caller digest without canonical metadata binding; S3 grant-event outbox has no relay lease/fence; S5 consumer does not bind event to an existing tenant-scoped grant; S6 journal authentication/fence atomicity are adapter-supplied; S7 bare P37/P39 test IDs collide; S8 post-commit revocation transition is absent.
- VERIFIED boundary limitation: P39-S4 worker-state fencing cannot stop bytes already emitted on an open stream. No transport implementation was found in reviewed source. Production behavior for S1-S8 remains UNKNOWN.
- VERIFIED: P39-POLICY-02..04 and P39-STREAM-01..03 are in a source-pinned crosswalk; all P39 tests use P39-prefixed IDs. No canonical LOOP/CASE/D IDs changed.
- VERIFIED: exit-provenance EP-01..20 were checked against immutable helper/test/acceptance pins. Current format_report() recalculates verdict from status + generic exit_code, so it cannot emit proposed INCOMPLETE for program_failed+child-zero or succeeded+child-nonzero while preserving those facts. EXIT_PROVENANCE_RESOLUTION_20261108.md §6 now records this compatibility limit, EP-21..25 and owner decisions for EP-18/24. No code change authorized.
- Event journal prototype: in memory, 21/21 local tests per owner handoff; producer identity is not cryptographic; fence check plus append is not atomic. Fake coordinator: 14 harness tests on test doubles, not canonical. Not re-verified in this pass.
- Pyodios on owner's iPhone (owner-reported): v1.1.0 build 7, Pyodide 314.0.5, Python 3.14.2. First Editor run showed "[Bridge/executePython] PythonError". Console probe for sys.last_exc: NOT RUN. Bridge cause and child exit status: UNKNOWN. Export/read-back, relaunch persistence and malformed-input test: NOT RUN.

## Decisions
- D-001 unified PC-and-phone direction, separate development boundaries. D-002 GitHub is source of truth. D-003 no secrets in public repo. D-004 validate before stack commitment. D-005 zero spend.
- OpenHands and Cline are pattern references only; reject Cline wildcard auto-approve default. MCP Tasks and ACP are optional adapters and never replace PocketCode command/attempt identity.
- No durable store (SQLite, PostgreSQL, Redis, cloud) is chosen until an atomic persistence contract is defined and tested.
- CASE-04 stays INCOMPLETE / timed_out. No precedence-only patch to scripts/report_contract.py until child-exit, wrapper-exit and termination provenance are resolved.
- 2026-11-07 (owner): old process rules may be revised for efficiency. AGENTS.md carries revised decision rights.

## Open items
- O-1 Owner: run the read-only Pyodios Console probe (steps in PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md). Blocks device evidence.
- O-2 Independent adversarial review status: Claude's full P39 source/model report was received as an uploaded file and reconciled in P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md. Claude did not read result_receipts.py/tests or the durable adapter contract and did not run the repository suite. Gemini's complete source-pinned P39 review remains outstanding; supplied plan is not sufficient. Claude's separate exit-provenance review remains requested.
- O-3 Run full Python suite in a real checkout or CI and record exact-SHA results.
- O-4 Define and test atomic persistence contract in a real candidate adapter; current DURABLE_ADAPTER_CONTRACT is proposed only.
- O-7 Decide post-commit/retry-resume policy gate and streaming MVP scope; model APIs do not enforce current policy during transfer resume.
- O-5 EXIT_PROVENANCE_RESOLUTION_20261108.md contains typed child-vs-wrapper exit and termination rules plus EP-01..EP-20. Static consistency audit is in EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md; EP-04/05 need a resolved-verdict/renderer contract, EP-21..25 are proposed additions, and EP-18/24 need owner mapping. Claude review and owner resolution remain pending; no code change authorized.
- O-6 Compare one free local path (a-Shell or Carnets) only if it adds information.
- P39 gate: Claude's full independent review received and reconciled in P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md. Confirms/refines S1-S3; S4 is a contract/MVP scope gap, not a sequential-model defect; adds trusted-clock, pre-commit revocation epoch, ID continuity and RG-O findings. A bounded audit of result_receipts.py/tests and DURABLE_ADAPTER_CONTRACT is committed in P39_RECEIPT_SUBSYSTEM_AUDIT_20261108.md. It confirms receipt/artifact digest/quarantine coverage in the richer model, but finds process-local IDs, no current-policy gate in transfer resume methods, caller-supplied times, and no concurrent/durable evidence. Gemini review and owner decisions remain open. No source/test changes until gate clears.
- CI boundary: recent commits are documentation/continuity updates; verify latest HEAD Actions rather than assuming a run. Prior 266/266 remains the latest source/test evidence at 744cb4d.

## Known risks
- Old entry files are too large for a free chat; start from BOOT, STATE and NEXT_TASK only.
- Rapid-fire commits create red intermediate CI runs and email noise; check commit history and latest CI.
- INDEX classification of older docs is by filename/date, not by reading.
