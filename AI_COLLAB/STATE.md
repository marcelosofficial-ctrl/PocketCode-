# STATE: PocketCode

Updated: 2026-11-12. This is the compact live state, not a historical ledger. Use Git history and INDEX.md for older detail.

## Product and hard constraints

- Phone-first, provider-neutral AI workflow/control plane for iOS and Android. MVP: explicit paste/import -> bounded execution -> truthful evidence/artifacts -> copyable report for any AI -> corrected rerun as a distinct attempt.
- $0 only (D-005/D-006). No paid API, host, provider, workload, Apple Developer Program, TestFlight or App Store.
- No runtime, provider, database, transport, storage engine or new host selected. Owner-approved no-spend GitHub Pages preview only.
- User-controlled context: explicit paste/import only; no clipboard polling, overlays or automatic capture.
- Untrusted code requires disposable, externally constrained execution. Stock Pyodide/WASM is for trusted light tasks only.
- Preserve CommandId, EffectId, DispatchAttemptId, ExecutionId, ObservationSequence, ResultReceiptId/revision and PublicationAttemptId as distinct identities. Unknown/degraded evidence never becomes PASS or FAIL by inference.
- Preserve LOOP-01..14, CASE-01..16, all D-IDs and OD-01..OD-13. Keep PocketCode separate from RevDev. PR #2/#3/#4 remain owner-controlled and untouched. No secrets/private user data in this public repo.

## Live repository and CI evidence

- Repo: `marcelosofficial-ctrl/PocketCode-`; branch: `pocketcode-ai-workflow-director-research-2026-10-28`.
- VERIFIED snapshot at start of this state-refresh unit: HEAD `3d635c5b0e0e14ee12a0ca1d65f55c0eee31ee9f`. Latest five then: `3d635c5` index scenario count; `4800374` storage receipt/artifact rebinding cases; `774660e` grant receipt-hash cross-model gap; `37a3fea` grant canonical digest binding; `22a6669` grant acceptance case. Re-fetch live HEAD on every continuation.
- VERIFIED compare from source-audit pin `b71315068ec33a0175fed46ef96912e954d87f9f`: 63 commits ahead, 0 behind, 15 changed paths, every path under `AI_COLLAB/`. No application source, scripts/tests, workflow or product assets changed in this interval.
- VERIFIED HEAD combined status at snapshot: `pending`, zero status entries. No check is attached; this is not a pass.
- Latest relevant Actions run #59 / `43126974602`, job `130881431566`, SUCCESS. Workflow-only commit `d93cd11e6873090cdb280fd18e45d9eeee9a973f` checked out historical model target `319cffef121e327331aeaff59522ae279b112ecc`. Full scripts suite 266/266; release-grant+consumer 26/26, FakeOutbox 22/22, EventJournal 27/27, receipts 59/59, execution projection 31/31. Python 3.12.16, SQLite 3.46.1, Ubuntu 26.04.1. Lane 4 BLOCKED / NOT TESTABLE; lane totals overlap the full suite. This is model-only evidence on that SHA, not current-HEAD CI, adapter proof or CASE acceptance.
- Tests in the current documentation pass: NOT RUN.

## Current model and contract findings

- VERIFIED: `ReleaseGrantContractModel.record_progress()` increments aggregate_version even for equal progress and changes only the grant; it adds no matching event/outbox row. `consume_event()` trusts supplied first-delivery payload_sha256 and lacks canonical-byte recomputation and full producer/scope checks. `mark_outbox_delivered()` flips a boolean; no grant-event relay lease/fence/stale-ack protection.
- VERIFIED: grant `ReceiptHead` stores effect/attempt/receipt ID/revision and artifact ID/object version/length, but not receipt SHA-256, artifact SHA-256 or quarantine state. `reserve()` binds identity/revision/object version and authorization fields, not those content proofs.
- VERIFIED: separate `result_receipts` model stores artifact SHA-256, integrity/quarantine state and ResultReceipt.receipt_sha256, and checks artifact digest/length at release. It is not wired into the grant ReceiptHead/reservation. Its receipt fingerprint uses Python `json.dumps(sort_keys=True, separators=...)`, which is not proof of RFC 8785/JCS cross-language canonicalization.
- VERIFIED documentation additions: grant-event-envelope/v1 now distinguishes data/receipt/artifact digests, states exact absent-vs-null field rules and safe-integer bounds; storage contract binds receipt head to receipt digest and artifact manifest content; the grant acceptance plan has 33 local cases (A1–A8, B1–B9, C1–C9, D1–D7) and a static current-coverage crosswalk. These are proposals, not implementation or tests.
- VERIFIED: opaque-origin protocol now binds canonical ExecutionId separately from parent-generated execution_instance_id in INIT and every channel message. Browser CANCEL_ACK is narrowly described as acknowledgement that the supervisor invoked terminate() on its exact Worker and closed the channel, not proof of native child exit, renderer/OS teardown or all side effects stopping.
- VERIFIED report issue: `report_contract.classify_verdict()` lets any nonzero integer exit code override timeout/cancel/rejection/infrastructure/nonterminal states. Do not patch precedence only. Keep format 1; versioned format-2 migration plan exists and remains gated.
- Other indexed contracts: opaque-origin execution; browser artifact storage/recovery; lifecycle/termination/receipt; Pages shared-origin audit; zero-budget origin comparison; phone/device validation runbook; grant model acceptance; report projection migration.

## Device, origin and naming evidence

- Owner-reported Pyodios iPhone: app 1.1.0 Build 7, Pyodide 314.0.5, Python 3.14.2. Editor showed `[Bridge/executePython] PythonError`. Console probe NOT RUN; cause and worker topology UNKNOWN. Preserve the existing matching `summary.json`; do not rerun main.py, wrapper or artifact-producing attempt. Owner-friendly Console instructions are in `PHONE_DEVICE_VALIDATION_RUNBOOK_20261112.md`; optional and may be deferred.
- Pages preview last successful run #17 / `39433670146` deployed static simulation from main SHA `90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c`. Not app runtime. PocketCode Pages and portfolio paths share the same github.io origin; do not store credentials, tokens, private source or security authority there. Live headers, current scripts and device context remain UNKNOWN.
- Safari storage behaviour, Home Screen app exception and browser eviction are research evidence, not proof for the installed app. IndexedDB/OPFS/SQLite-WASM remain unselected.
- O-7: official Catrobat Pocket Code app and POCO C++ project are verified naming/search collisions. Xiaomi POCO official trademark scope remains UNKNOWN. No rename or PoCo publication before direct clearance.
- Owner said a previously opened GitHub link looked okay; exact target remains ambiguous between commit page and Pages preview. Treat only as informal owner observation, not live Pages evidence. Do not ask to repeat unless necessary.

## Decisions and gates

- D-001 unified PC-and-phone direction with distinct project boundaries; D-002 GitHub as durable source of truth; D-003 no secrets in public repo; D-004 validate before stack commitment; D-005/D-006 $0.
- OD-01..OD-13 adopted 2026-11-11. No live/incremental artifact streaming in MVP; bounded download/share only after complete staging, integrity verification and fresh authorization. Policy adoption does not prove implementation.
- P39 product-policy gate CLEARED by owner delegation; P39 implementation/adapter conformance gate remains CLOSED. No source/test edits, provider calls, device tests, deployments, DNS/settings, PR changes or infrastructure selections without their separate gate.
- CASE-04 remains INCOMPLETE / timed_out. Model PASS never closes adapter or canonical CASE acceptance.

## Ranked open work

1. Continue static source-to-contract reconciliation of grant, receipt, authorization, lifecycle and artifact recovery; document concrete gaps only. Do not edit code/tests while P39 implementation/adapter gate is closed.
2. Keep the 33-scenario grant acceptance plan and three-projection report migration ready for a separately authorized model/test scope. Durable adapter, producer authentication, relay fencing and backup/restore proof remain UNKNOWN.
3. Device/browser work requires an approved synthetic-data build and exact target-device evidence. The Pyodios Console probe is optional; preserve summary.json and do not rerun the successful attempt.
4. Resolve shared-origin threat boundary before any persistent sensitive data; no host migration or deployment without owner decision.
5. Complete O-7 official name clearance only if a naming decision is needed.
6. Prove five-file fresh-chat resume protocol. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.

Evidence labels: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests: PASS / FAIL / NOT RUN. Chat assertions are not proof.
