# STATE: PocketCode
Updated: 2026-11-11. Unit began at active branch HEAD: `163eef5f004b39360a37fcf89aca22018ea235d4`.

## Status and evidence
- Phase: discovery/product definition. P39/exit-provenance and P40 implementation gates CLOSED. No runtime, provider, database, transport or storage engine selected.
- Historical PASS: Actions run `42365455316`, workflow "PocketCode Python conformance tests", 266/266 on source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`. Historical only, not current.
- Current branch latest five: `163eef5f`, `5038739b`, `b7b01782`, `cac5abc0`, `2b2f8b45`. All documentation-only; no scripts/tests changed.
- Ten P40 source/test pins last revalidated exact: release-grant model/tests, FakeOutbox/tests, EventJournal/tests, execution projection/tests, receipt store/tests. No later source/test drift.
- Exact HEAD combined status: no statuses. CI and full suite: NOT RUN, not PASS. P40 six-lane protocol prepared but NOT AUTHORIZED / NOT RUN.
- Model findings: equal grant progress increments aggregate_version without matching event/outbox; grant-event consumer lacks grant/source/producer binding; FakeOutbox fencing covers effect dispatch, not grant-event publication; EventJournal producer identity is adapter-verified input, not cryptographic authentication. These are model/test-double findings, not durable production proof.
- Pyodios iPhone (owner-reported): app 1.1.0 Build 7, Pyodide 314.0.5, Python 3.14.2. Editor returned "[Bridge/executePython] PythonError"; Console probe NOT RUN; cause and worker topology UNKNOWN.
- Pages: last located successful deploy run `39433670146` (2026-10-20), main SHA `90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c`, URL `https://marcelosofficial-ctrl.github.io/PocketCode-/`. Public portfolio Pages URL `https://marcelosofficial-ctrl.github.io/portfolio/` shares scheme/host/port; paths do not isolate origin storage. This is a trust boundary, not proof of exploit. Current live response, headers, out-of-band deployment and generated sibling script behavior UNKNOWN.
- PWA research covers IndexedDB metadata, OPFS staging/readback, local fencing and recovery; no storage engine selected. Target iOS/Safari behavior, persist(), quota and lifecycle UNKNOWN.
- Claude and Gemini P39 reviews reconciled. Claude's provider-cache/context and AI-lane drafts were independently audited in `CLAUDE_PROVIDER_AND_LANES_INDEPENDENT_AUDIT_20261111.md`; strategy drafts are not P39 gate evidence.
- Claude C01.4 (2026-11-10) reports the five-file continuity system has been used for repository reads, updates and commits. Fresh-chat one-line resume test is explicitly NOT YET PROVEN. New-repository creation by ChatGPT is UNKNOWN; assume owner creates repos. Claude reports recurring app stalls, large-file/upload limits, connector 403/CI-log limits and large-push JSON escaping failures; mitigations are recorded in the supplied C01.4 response.
- Current CI workflow `.github/workflows/pocketcode-python-tests.yml` uses branch/path filters, cancel-in-progress, Python 3.12 and unittest discovery. It does not print Python/SQLite versions. Version-baseline step is a future proposal only, not implemented.
- CASE-04 INCOMPLETE / timed_out. No precedence-only patch to `scripts/report_contract.py` until child/wrapper/termination provenance is resolved.

## Decisions and constraints
- D-001 unified PC-and-phone direction with separate project boundaries; D-002 GitHub source of truth; D-003 no secrets in public repo; D-004 validate before stack commitment; D-005 $0.
- D-006 owner decision (2026-11-08): no spending of any kind; no Apple Developer Program, TestFlight or App Store; installable web app on GitHub Pages for now.
- OD-01..OD-13 OPEN. OD-01 is live/incremental streaming only; NO does not automatically exclude bounded artifact download/share. If bounded release remains MVP, OD-02..05 need grant/revocation/recovery semantics. OD-13 governs client-receipt claims. No decision inferred.
- Preserve LOOP-01..14, CASE-01..16 and all D-IDs. PR #2/#3/#4 remain owner-controlled and untouched. Keep PocketCode and RevDev separate. No provider calls, spending, source/test edits, device tests, deployment/settings/DNS changes or PR changes without applicable authorization.
- 2026-11-07 owner: AGENTS.md carries tiered decision rights. 2026-11-08 owner: possible PoCo rename undecided; website design must not change. Nothing renamed.

## Open items
1. Owner: resolve or explicitly defer OD-01..OD-13.
2. Owner: run read-only Pyodios Console probe in `PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md`.
3. Await further Claude P39/exit-provenance artifact from owner; do not issue competing request.
4. After gate clearance and explicit authorization, run six P40 lanes and full Python suite on exact pinned SHA; keep model tests separate from CASE acceptance.
5. Obtain reliable read-only live Pages/header/service-worker and portfolio-script evidence; no deployment or settings changes.
6. Resolve typed child exit vs wrapper exit vs termination provenance and receipt ordering. PoCo name undecided; LinkedIn work waits for laptop/export.

Evidence labels: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Keep current test outcomes distinct from historical results.