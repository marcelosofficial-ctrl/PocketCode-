# STATE: PocketCode
Updated: 2026-11-12. Reconciled against branch source through b71315068ec33a0175fed46ef96912e954d87f9f; this update records four completed design units and housekeeping.

## Status and evidence
- Phase: discovery/product definition and acceptance-contract refinement. P39 product-policy gate CLEARED by owner delegation; P39 implementation/adapter conformance gate remains CLOSED. No runtime, provider, database, transport, host or storage engine selected.
- VERIFIED current P40 PASS: Actions run #59 / 43126974602, job 130881431566, workflow-only commit d93cd11e6873090cdb280fd18e45d9eeee9a973f; checkout log confirms exact target SHA 319cffef121e327331aeaff59522ae279b112ecc. Full scripts suite 266/266; lanes: release-grant + consumer 26/26, FakeOutbox 22/22, EventJournal 27/27, receipts 59/59, execution projection 31/31. Python 3.12.16, SQLite 3.46.1, Ubuntu 26.04.1 / Linux 7.0.0-1019-azure x86_64. Lane 4 BLOCKED / NOT TESTABLE. Model-only evidence, not adapter/CASE acceptance.
- Historical PASS: Actions run 42365455316, 266/266 on source/test SHA 744cb4dc7cd4994647c84ac7476d0c78a21f0540; historical only.
- Current branch immediately before this state reconciliation: b71315068ec33a0175fed46ef96912e954d87f9f. Recent work is documentation-only; no application or test source changed.
- VERIFIED model defects: equal grant progress increments aggregate_version without matching event/outbox; grant-event consumer trusts first-delivery digest and lacks full grant/source/producer/tenant/attempt binding; grant-event delivery has no relay lease/fence/stale-ack protection. FakeOutbox fencing covers effect dispatch only. EventJournal.AuthenticatedProducer is a typed adapter input, not cryptographic authentication.
- VERIFIED documentation deliverables committed on this branch:
  - GRANT_EVENT_ENVELOPE_AND_RELAY_CONTRACT_20261112.md: grant-event-envelope/v1, atomic aggregate/event parity, canonical bytes, trusted producer ingress, separate relay fence, ordered at-least-once delivery and consumer inbox.
  - OPAQUE_ORIGIN_EXECUTION_PROTOCOL_20261112.md: opaque iframe, source-bound handshake, narrow wildcard bootstrap, supervisor-owned MessageChannel, CSP restrictions, bounded explicit input/output and termination semantics.
  - BROWSER_ARTIFACT_STORAGE_RECOVERY_CONTRACT_20261112.md: origin trust, staged writes/read-back verification, manifest commit, eviction recovery, explicit export and durability vocabulary.
  - LIFECYCLE_TERMINATION_RECEIPT_ACCEPTANCE_20261112.md: typed child/wrapper/interpreter evidence, same-attempt termination, three projections and receipt acceptance matrix.
  All four are proposals/specifications, not implemented or tested.
- VERIFIED code issue: report_contract.classify_verdict() checks any nonzero exit before timeout/cancel lifecycle, so a caller-supplied wrapper code 137 can yield FAIL. Do not apply a precedence-only patch; the renderer needs an authenticated typed projection and preserved raw observations.
- Pyodios iPhone (owner-reported): app 1.1.0 Build 7, Pyodide 314.0.5, Python 3.14.2. Editor returned [Bridge/executePython] PythonError; Console probe NOT RUN; cause and worker topology UNKNOWN.
- Pages: VERIFIED last successful preview run #17 / 39433670146 (2026-10-20) deployed main SHA 90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c. Current main prototype/workflow blobs match deployment; artifact contains README.md + simulation-only index.html. No runtime/worker/service worker/manifest/backend/login in that subtree. Portfolio repo uses same scheme/host/port under /portfolio and its BaseLayout reads localStorage. Treat the github.io host as one trust domain; no sensitive user data until origin isolation or accepted threat model. Current live response/headers/Pages settings remain UNKNOWN. See PAGES_READ_ONLY_SOURCE_AUDIT_20261112.md.
- Storage: WebKit documents a 7-day script-writable storage cap in Safari under stated conditions, but explicitly exempts first-party Home Screen web-app domains from that cap and isolates their data from Safari. This is not backup or a guarantee against other loss. Safari, Home Screen app and WKWebView behaviour in the actual installed app remains UNKNOWN. IndexedDB, OPFS and SQLite-WASM remain unselected.
- Name clearance / O-7: VERIFIED official Catrobat page describes Pocket Code as a smartphone programming app for Android/iOS, creating a direct same-category naming/confusion risk. VERIFIED official POCO C++ project page reports current 1.15.4 release and ongoing development; official About page states Boost Software License 1.0. UNKNOWN whether reported Xiaomi POCO trademark registrations/classes apply; aggregator claims were not confirmed in an official trademark record. Do not rename repo/docs/site or publish PoCo before a direct clearance search.
- Fresh-chat one-line resume remains NOT YET PROVEN. Actual production coordinator, durable adapter, provider and device integration remain UNKNOWN.

## Decisions and constraints
- D-001 unified PC-and-phone direction with separate project boundaries; D-002 GitHub source of truth; D-003 no secrets in public repo; D-004 validate before stack commitment; D-005 $0.
- D-006 owner decision (2026-11-08): no spending; no Apple Developer Program, TestFlight or App Store; installable web app on GitHub Pages for now.
- OD-01..OD-13 ADOPTED 2026-11-11. No live/incremental artifact streaming in MVP; bounded downloads/shares only after complete staging, integrity and fresh authorization. See P39_OWNER_DELEGATED_DECISIONS_20261111.md. These are policy decisions, not implementation proof.
- Preserve LOOP-01..14, CASE-01..16 and all D-IDs. PR #2/#3/#4 owner-controlled and untouched. Keep PocketCode and RevDev separate. No provider calls, spending, source/test edits, device tests, deployments, settings/DNS changes or PR changes without applicable authorization.
- No candidate name approved. Do not rename or publish PoCo before name clearance.

- VERIFIED: grant-event model-only test plan committed at GRANT_EVENT_MODEL_ACCEPTANCE_PLAN_20261112.md. It specifies four test groups (transition parity, envelope validation, relay fencing, consumer inbox/restore), 29 local scenarios, and strict model-vs-adapter evidence limits. Proposed only; no test/source implementation or execution.

## Open items
1. Owner: run the read-only Pyodios Console probe in PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md; preserve existing summary.json and do not rerun the successful artifact-producing attempt.
2. Owner: open https://marcelosofficial-ctrl.github.io/PocketCode-/ on phone and confirm what actually loads; capture a screenshot if it differs from the static sample. If possible, inspect response headers and service-worker registrations for both /PocketCode-/ and /portfolio/.
3. Before any persistent user data, resolve the shared github.io origin threat boundary; do not store credentials/private source/artifacts there. After a separately approved implementation scope, add model-level grant-event parity, first-delivery validation, relay fencing, stale-ack, consumer inbox and restore-high-water adversarial tests. Current contracts are NOT implementation.
4. Verify opaque-origin/CSP protocol on target iOS Safari/WKWebView and Android versions, including worker termination, no-network paths and explicit file copies. No device tests run.
5. Run the browser storage/recovery matrix: cold launch, force-close, quota, persist grant/denial, inactivity eviction, multi-tab CAS, export/import and artifact read-back.
6. Resolve child/wrapper/termination provenance with authoritative same-attempt evidence and a versioned typed report projection. CASE-04 remains INCOMPLETE / timed_out.
7. O-7: complete direct candidate-name clearance across intended app stores, GitHub, domains/social handles and official trademark databases. Do not rename or publish PoCo until resolved.
8. Prove fresh-chat one-line resume using the five-file startup sequence. Do not open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.

Evidence labels: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests: PASS / FAIL / NOT RUN. Model test PASS never closes adapter or canonical CASE acceptance.
