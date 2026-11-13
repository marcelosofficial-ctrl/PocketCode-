# STATE: PocketCode

Updated: 2026-11-12. Compact live state; use Git history and INDEX.md for older detail.

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
- VERIFIED live snapshot at 2026-11-13: HEAD `e1c7e27996354dbb98913eca8408a1f72afa2e4d`. Latest five, newest first: `e1c7e27` OD12 consistency/live-state checkpoint; `e8c7085` owner-gated next-task priorities; `22a2cf8` STATE live-head refresh; `af4a0f8` termination-evidence checkpoint; `a1a55c4` lifecycle Worker-action/termination-proof distinction.
- VERIFIED compare from source-audit pin `b71315068ec33a0175fed46ef96912e954d87f9f`: 83 ahead / 0 behind / 19 changed paths, every path under `AI_COLLAB/`. No application source, scripts/tests, workflow or product assets changed in this interval.
- VERIFIED exact-HEAD CI check-runs: 0; combined commit status: `pending`, zero attached statuses. No current-HEAD CI has run. Pending with zero entries is not a pass or failure.
- Latest Actions run #59 / `43126974602`, SUCCESS, checked out historical model target `d93cd11e6873090cdb280fd18e45d9eeee9a973f` (run metadata head SHA), which in turn recorded the pinned model target `319cffef121e327331aeaff59522ae279b112ecc`. Historical full scripts suite 266/266. It is not current-HEAD CI, adapter proof or canonical CASE acceptance.
- Tests in the current documentation-only pass: NOT RUN.

## Current model and contract findings

- VERIFIED: `ReleaseGrantContractModel.record_progress()` increments aggregate_version even for equal progress and changes only the grant; no matching event/outbox row. `consume_event()` trusts supplied first-delivery payload_sha256 and lacks canonical-byte recomputation and full producer/scope checks. `mark_outbox_delivered()` flips a boolean; no grant-event relay lease/fence/stale-ack protection.
- VERIFIED: grant `ReceiptHead` stores effect/attempt/receipt ID/revision and artifact ID/object version/length, but not receipt SHA-256, artifact SHA-256 or quarantine state. `reserve()` does not bind those proofs.
- VERIFIED: separate `result_receipts` model stores artifact SHA-256, integrity/quarantine state and ResultReceipt.receipt_sha256, checks artifact digest/length at release, and tracks immutable receipt revisions. It is not wired into grant ReceiptHead/reservation. Its Python `json.dumps(sort_keys=True, separators=...)` receipt fingerprint is not proof of RFC 8785/JCS cross-language canonicalization.
- VERIFIED: grant event contract defines distinct data/receipt/artifact digests, absent-vs-null field rules and safe-integer bounds. Storage contract binds receipt head to receipt digest and artifact manifest; only verified/non-quarantined artifacts are eligible. These remain design contracts.
- VERIFIED: grant model plan has 33 local cases A1–A8, B1–B9, C1–C9, D1–D7. Static current-source crosswalk identifies missing parity, envelope, relay and inbox/restore coverage. Model plan does not prove durable atomicity or authentication.
- VERIFIED: `execution_projection.py` distinguishes natural child exit, wrapper exit, signal termination and embedded interpreter result. It is pure and only attempt-bound; no canonical ExecutionId/CommandId/EffectId/tenant fields, authenticated ingress, ordered-stream reducer, policy/egress barrier or durable persistence. Tests cover selected typed projection cases only.
- VERIFIED: `result_receipts.py` stores execution outcome, collection state, lifecycle disposition, cleanup state, evidence, artifacts and uncertainty, and has a separate synchronous artifact-release/transfer model. It has no termination request/ack authority or authenticated client receipt bound to artifact digest/object version/range. `PublicationAttempt` is based on caller-supplied boolean success, not receiver acknowledgement.
- VERIFIED: event journal takes a supplied `AuthenticatedProducer` model value; it does not verify keys, signatures, certificates, sessions or external credentials.
- VERIFIED documentation work: `P39_OD02_OD08_MODEL_COVERAGE_CROSSWALK_20261112.md` maps reservation, claim, recovery, policy epoch, time, restore high-water and receipt/artifact binding; `P39_OD09_OD13_MODEL_COVERAGE_CROSSWALK_20261112.md` maps policy barriers, three projections, coordinator identity, termination and client acknowledgement; `P39_SUPPLEMENTAL_MODEL_CANONICAL_TRACEABILITY_20261112.md` maps local grant/report scenarios to canonical LOOP/CASE obligations as supporting coverage only.
- VERIFIED: opaque-origin protocol carries canonical ExecutionId separately from parent-generated execution_instance_id in INIT and all channel messages. Browser CANCEL_ACK is only `worker_termination_action_acknowledged`: supervisor invoked terminate() on its exact Worker and closed the task channel. Lifecycle acceptance now explicitly says this is not OD-12's broader `termination_acknowledged` without a separately accepted execution-model-specific authority rule. It does not prove native child exit, renderer/OS teardown or all side effects stopping. Device runbook preserves this distinction.
- VERIFIED report issue: `report_contract.classify_verdict()` allows any nonzero integer exit to override timeout/cancel/rejection/infrastructure/nonterminal status. Keep format 1; format-2 migration plan exists. Do not patch precedence only.

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
