# STATE: PocketCode   (current state only; under 900 words)
Updated: 2026-11-11 by ChatGPT. At the start of the 2026-11-11 lineage refresh, the active branch HEAD was `3d3102f36fbc575206e89e3a65e0c0d22270f16d`. This pass added metadata commits `6e7624ed013213bac40015c837c4fa159ab89018` (STATE) and `24c540bc82f307f6c26ba75e104e2116560c9fb3` (CHECKPOINT). Latest research/content commit remains `5794fa175d1639290a8af9e1b86d4252e24ef466`. The three commits after audited HEAD `3545c1e15da6041906bf9cf886c9acdd0a5e7e07` changed documentation only; the ten pinned source/test blobs remain unchanged. Exact-SHA workflow/status queries for pre-refresh HEAD returned no associated workflow runs and no statuses; CI NOT RUN. No source/test/device tests were run.

## Status
- Phase: Discovery/product definition. P39/exit-provenance gate CLOSED. No runtime/provider/database/transport selected.
- VERIFIED: historical Actions run 42365455316 on source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`, workflow "PocketCode Python conformance tests", job unittest: 266/266 PASS. Historical source/test evidence only.
- COMMITTED: intent/proof separation, receipt binding, grant recovery, concurrency/crash models, PWA/origin/exit-provenance research, worker-channel red-team, full-power gap research, and the 2026-11-11 source-pinned P40 coverage/Pages origin audit.
- CLAIMED ONLY (not built): durable adapter; real concurrent processes; transactional grant-event relay; durable crash recovery; production fencing; transport stream ownership and revocation; trusted policy authority; client receipt.
- Claude and Gemini P39 reviews are reconciled. The source-pinned audit confirms: grant progress increments aggregate_version even for equal progress and emits no matching event/outbox; grant-event consumer trusts first-delivery digest and lacks grant/source/producer binding; FakeOutbox fencing protects effect dispatch, not grant-event publication; EventJournal producer identity is adapter-verified input, not cryptographic authentication.
- Event journal and fake coordinator remain in-memory/test-double evidence only. No durable/authenticated adapter proof.
- Pyodios on owner's iPhone (owner-reported): v1.1.0 build 7, Pyodide 314.0.5, Python 3.14.2. First Editor run showed only "[Bridge/executePython] PythonError"; Console probe NOT RUN; bridge cause UNKNOWN.
- PWA storage research defines IndexedDB metadata, OPFS staging/readback, local fencing and recovery. No storage engine selected; target iOS/Safari build, persist() result, quota and lifecycle behavior UNKNOWN.
- VERIFIED Pages: last located successful deploy run 39433670146 on 2026-10-20 used main SHA `90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c`, with environment URL `https://marcelosofficial-ctrl.github.io/PocketCode-/`. Workflow auto-deploy is main-only and path-filtered. Main now at `03e65ef35d8b22cb4337ac7097b2a31247c3721e`; no later Pages workflow run found in 75 Actions runs.
- VERIFIED shared origin: public `portfolio` repo also has Pages enabled at `https://marcelosofficial-ctrl.github.io/portfolio/`. Same scheme/host/port as PocketCode; paths do not isolate origin storage. This is a concrete shared-origin trust boundary, not proof of exploit. No secrets in localStorage/IndexedDB.
- UNKNOWN: out-of-band deploy after 2026-10-20; live headers/redirects/current response; generated portfolio script behavior; target-device storage; actual Pyodios worker topology.
- `P40_MODEL_ONLY_EXECUTION_PROTOCOL_20261110.md` revised to six lanes with exact existing test methods. Known model gaps are marked FAIL/BLOCKED rather than described as passing coverage. NOT AUTHORIZED / NOT RUN.
- `P40_SOURCE_PINNED_COVERAGE_AND_PAGES_ORIGIN_AUDIT_20261111.md` pins model/test blobs, corrects seven prior claims, records exact Pages deployment and portfolio sibling origin, and reviews W3C/WPT/OWASP reuse/licences.
- VERIFIED current-branch continuity at start of refresh: HEAD `3d3102f` was three documentation-only commits after audited HEAD `3545c1e`; compare output listed only `AI_COLLAB/` documentation paths. The audit's source/test pins therefore remained applicable.

## Decisions
- D-001 unified PC-and-phone direction, separate development boundaries. D-002 GitHub is source of truth. D-003 no secrets in public repo. D-004 validate before stack commitment. D-005 zero spend.
- D-006 (owner, 2026-11-08): no spending of any kind. No Apple Developer Program, TestFlight or App Store for now; distribution is installable web app on GitHub Pages.
- PR #2/#3/#4 remain owner-controlled and untouched. No durable store, provider, runtime or transport selected.
- CASE-04 stays INCOMPLETE / timed_out. No precedence-only patch to scripts/report_contract.py until trusted child/wrapper/termination provenance is resolved.
- 2026-11-07 owner: old process rules may be revised; AGENTS.md carries tiered decision rights. 2026-11-08 owner: PocketCode considered for renaming to PoCo; website design must not change; nothing renamed.

## Open items
- O-1 Owner: run read-only Pyodios Console probe in `PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md`.
- O-2 Await any additional Claude artifact supplied by owner. Do not create a competing request while Claude's strategy assignment remains OPEN. OD-01..OD-13 remain OPEN.
- O-3 Run full Python suite in a real checkout/CI and record exact-SHA results.
- O-4 Confirm current live Pages response/settings/headers and audit the shared `portfolio` origin's generated script behavior. Deployment URL and last workflow SHA are known; current live state is not.
- O-5 Resolve typed child exit vs wrapper exit vs termination provenance and receipt ordering.
- O-6 P40 six-lane protocol prepared; execution still gated by owner decisions and explicit authorization.
- O-7 PoCo name remains undecided; LinkedIn work waits for laptop/export.
- O-8 Apple design/context/provider-cache and website strategy work remain Claude's lane.

## Evidence limits
- Historical 266/266 PASS applies only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.
- Current P40 scenarios, durable adapter, browser/device, live origin exploit, transport and full-suite checks are NOT RUN.
- Keep PocketCode and RevDev evidence strictly separate.
