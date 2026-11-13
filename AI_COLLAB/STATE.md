# STATE: PocketCode

Updated: 2026-11-13. Compact live state; use Git history and INDEX.md for older detail.

## Product and hard constraints

- Phone-first, provider-neutral AI workflow/control plane for iOS and Android. MVP: explicit paste/import -> bounded execution -> truthful evidence/artifacts -> copyable report for any AI -> corrected rerun as a distinct attempt.
- $0 only (D-005/D-006). No paid API, host, provider, workload, Apple Developer Program, TestFlight or App Store.
- No runtime, provider, database, transport, storage engine or new host selected. Owner-approved no-spend GitHub Pages preview only.
- Explicit user paste/import only; no clipboard polling, overlays or automatic capture.
- Untrusted code requires disposable, externally constrained execution. Stock Pyodide/WASM is for trusted light tasks only.
- Preserve CommandId, EffectId, DispatchAttemptId, ExecutionId, ObservationSequence, ResultReceiptId/revision and PublicationAttemptId as distinct identities. Unknown/degraded evidence never becomes PASS or FAIL by inference.
- Preserve LOOP-01..14, CASE-01..16, all D-IDs and OD-01..OD-13. Keep PocketCode separate from RevDev. PR #2/#3/#4 owner-controlled and untouched. No secrets/private user data in this public repo.

## Live repository and CI evidence

- Repo `marcelosofficial-ctrl/PocketCode-`; branch `pocketcode-ai-workflow-director-research-2026-10-28`.
- VERIFIED current live HEAD after this continuation: `f02065853404b325e0f87ac7045807ad5fe3edfc`. Latest five, newest first: `f020658` continuity reconciliation; `9de34da` risk delta research; `dcf76c8` atomic continuity records; `676cc03` checkpoint repair; `a9fba95` next-task baseline.
- VERIFIED compare from `b71315068ec33a0175fed46ef96912e954d87f9f`: 88 ahead / 0 behind / 20 changed paths, all AI_COLLAB; no application source/tests/workflow/product assets changed.
- VERIFIED exact-HEAD combined status has zero attached statuses and PR-triggered workflow-run lookup returned zero runs. CI/tests on this HEAD: NOT RUN, not pass or failure.
- Latest Actions run #59 / `43126974602`, SUCCESS, historical model target `319cffef121e327331aeaff59522ae279b112ecc`, full scripts suite 266/266. Not CI for this snapshot, adapter proof or canonical CASE acceptance.
- Tests in this documentation-only pass: NOT RUN. The atomic continuity commit itself is documentation-only and is not represented as tested.

## Current model and contract findings

- VERIFIED: grant model still has aggregate/event parity, canonical first-delivery digest, full producer/scope authentication, grant-event relay fencing and atomic inbox/restore gaps. Equal-progress updates can advance aggregate_version without an event; delivered marker is unguarded. The 33-case grant plan and source crosswalks are design/model evidence only.
- VERIFIED: grant ReceiptHead is not fully bound to receipt/artifact digests and quarantine state; separate result_receipts model has stronger hashes but is not integrated with grant reservation. Python sorted JSON is not proof of RFC 8785/JCS.
- VERIFIED: execution_projection.py and result_receipts.py are pure/in-memory models, not authenticated durable adapters. Separate child verdict, evidence/job disposition and artifact disposition. No authenticated lifecycle reducer, policy/egress barrier, authoritative termination proof or client-generated acknowledgement bound to exact artifact digest/version/range.
- VERIFIED: EventJournal's AuthenticatedProducer is a supplied model value, not cryptographic verification. report_contract format 1 lets a nonzero integer exit override timeout/cancel/rejection/infrastructure/nonterminal state; retain format 1 until gated format-2 migration.
- VERIFIED: opaque-origin protocol separates canonical ExecutionId and execution_instance_id. Worker action acknowledgement proves supervisor invoked terminate() on its Worker and closed the channel only; it does not prove native child exit or OS/renderer teardown. CASE-04 remains INCOMPLETE / timed_out.

## Device, origin and naming evidence

- Owner-reported Pyodios iPhone: app 1.1.0 Build 7, Pyodide 314.0.5, Python 3.14.2. Editor showed `[Bridge/executePython] PythonError`. Console probe NOT RUN; cause and worker topology UNKNOWN. Preserve matching `summary.json`; do not rerun main.py, wrapper or artifact-producing attempt. Owner-friendly instructions in `PHONE_DEVICE_VALIDATION_RUNBOOK_20261112.md`; optional/deferable.
- Pages preview last successful run #17 / `39433670146` deployed static simulation from main SHA `90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c`, not app runtime. PocketCode Pages and portfolio paths share one github.io origin; no credentials, tokens, private source or authority there. Live headers/scripts/device context UNKNOWN.
- Safari storage and Home Screen app research are not proof for installed app. IndexedDB/OPFS/SQLite-WASM remain unselected.
- O-7: official Catrobat Pocket Code app and POCO C++ are verified naming/search collisions. Xiaomi POCO official trademark scope UNKNOWN. No rename or PoCo publication before direct clearance.
- Owner's prior visual check is an informal observation; exact opened link ambiguous between commit and Pages preview. Not live Pages proof; do not repeat unless necessary.

## Decisions and gates

- D-001 unified PC/phone direction with distinct project boundaries; D-002 GitHub as durable source; D-003 no secrets in public repo; D-004 validate before stack commitment; D-005/D-006 $0.
- OD-01..OD-13 adopted 2026-11-11. No live/incremental artifact streaming in MVP; bounded download/share only after complete staging, integrity verification and fresh authorization. Policy adoption does not prove implementation.
- P39 product-policy gate CLEARED by owner delegation; P39 implementation/adapter conformance gate remains CLOSED. No source/test edits, provider calls, device tests, deployment, DNS/settings, PR changes or infrastructure selection without separate gate.
- CASE-04 remains INCOMPLETE / timed_out. Model PASS never closes adapter or canonical CASE acceptance.

## Ranked open work

1. Continue non-duplicative static integration review only where a concrete source-to-policy gap remains. The OD-02..OD-13 crosswalks and canonical model traceability addendum are now indexed.
2. Keep the 33-case grant plan and 14-case report-v2 plan ready for a separately authorized model/test scope. No source/test change until gate is reopened.
3. Browser/device tests require an approved synthetic-data build and exact target-device evidence. Pyodios Console probe remains optional; preserve summary.json and never rerun successful attempt.
4. Resolve shared-origin threat boundary before sensitive persistence. No host migration/deployment without owner decision.
5. O-7 official name clearance only if a naming decision is needed. Prove five-file fresh-chat resume protocol when practical.

Evidence labels: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests: PASS / FAIL / NOT RUN. Chat assertions are not proof.
