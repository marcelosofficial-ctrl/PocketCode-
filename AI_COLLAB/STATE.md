# STATE: PocketCode

Updated: 2026-11-14. Current facts only; use INDEX.md for source documents and older evidence.

## Product and hard constraints
- Phone-first, provider-neutral AI workflow/control plane for iOS and Android. MVP: explicit paste/import -> bounded execution -> truthful evidence/artifacts -> copyable report for any AI -> corrected rerun as a distinct attempt.
- $0 only (D-005/D-006). No paid API/provider/host/workload, Apple Developer Program, TestFlight or App Store.
- No runtime, provider, database, transport, storage engine or new host selected. GitHub Pages is an owner-approved no-spend preview only.
- Explicit user paste/import; no clipboard polling, overlays or automatic capture. Untrusted code needs disposable, externally constrained execution; stock Pyodide/WASM is trusted-light-task only.
- Preserve CommandId, EffectId, DispatchAttemptId, ExecutionId, ObservationSequence, ResultReceiptId/revision and PublicationAttemptId. Unknown/degraded evidence never becomes PASS/FAIL by inference.
- Preserve LOOP-01..14, CASE-01..16, all D-IDs and OD-01..13. PocketCode and RevDev remain separate. PR #2/#3/#4 owner-controlled and untouched. No secrets/private data in this public repo.

## Repository and CI
- Repo `marcelosofficial-ctrl/PocketCode-`; active branch `pocketcode-ai-workflow-director-research-2026-10-28`. Always fetch live HEAD and latest five commits.
- Latest verified unit-start HEAD (2026-11-14): `c20fd173fa9e457c2ae594ca1b7562ef0ce1555e`; latest five: `c20fd17`, `c3972a0`, `f1cf507`, `dec8b75`, `ecda8de`.
- Exact HEAD status endpoint: zero attached statuses; exact-SHA PR-triggered workflow-runs endpoint: zero runs. Tests NOT RUN. Empty status list is not an active job and not PASS/FAIL.
- Source-audited baseline `f02065853404b325e0f87ac7045807ad5fe3edfc`: 16 ahead / 0 behind. Seven changed paths are documentation only: BOOT, STATE, NEXT_TASK, CHECKPOINT, WORK_PROTOCOL, INDEX and the 2026-11-14 research note; no application source, tests, workflows or product assets changed.
- Historical Actions run #59 (`43126974602`) passed 266/266 on different model target SHA `319cffef121e327331aeaff59522ae279b112ecc`; not current-head CI, adapter proof or CASE acceptance.

## Accepted decisions and gates
- D-001 unified PC/phone direction with separate project boundaries; D-002 GitHub as durable source; D-003 no secrets in public repo; D-004 validate before stack commitment; D-005/D-006 $0.
- OD-01..OD-13 adopted 2026-11-11. No live/incremental artifact streaming in MVP; bounded download/share only after full staging, integrity verification and fresh authorization.
- P39 product-policy gate CLEARED by owner delegation; P39 implementation/adapter conformance gate CLOSED. No source/test edits, provider calls, device tests, deployment, DNS/settings, PR changes or infrastructure selection without separate scope authorization.
- CASE-04 remains INCOMPLETE / timed_out. Model PASS never closes adapter or canonical CASE acceptance.

## Current known gaps (model/design evidence, not production proof)
- Grant model: aggregate/event parity and no-op semantics; canonical first-delivery digest and producer/scope authentication; grant-event relay lease/fence/stale-ack; atomic consumer inbox/restore. 33-case plan is model-only.
- Journal/receipt: conflicts consume journal observation sequence but are omitted from accepted-event projection; conflict records omit attempted producer, effect/attempt/fence and timestamps; receipts have no structured journal high-water or conflict refs. INFERRED model integration gap, not proof of production exploit.
- Lifecycle/receipt: execution_projection.py and result_receipts.py are pure/in-memory. Child verdict, job/evidence disposition and artifact disposition remain separate; no integrated authenticated policy/egress barrier, authoritative termination proof or client-generated acknowledgement bound to exact artifact digest/version/range.
- EventJournal AuthenticatedProducer is supplied model input, not cryptographic verification. Report format 1 lets nonzero integer exit override timeout/cancel/rejection/infrastructure/nonterminal status; keep format 1 until gated format-2 migration.
- Opaque-origin Worker acknowledgement proves supervisor called terminate() on its Worker and closed the channel only, not native child exit or OS/renderer teardown. Not OD-12 proof.
- Dispatch/projection helpers were checked against their contract; trusted caller owns authentication, persistence, sequence ordering and deduplication. No helper defect established.
- Mobile runner is simulation-only; its static checker does not prove browser/device/accessibility/runtime/security behavior.

## Device, origin and naming
- Owner-reported Pyodios iPhone: app 1.1.0 Build 7, Pyodide 314.0.5, Python 3.14.2; Editor showed `[Bridge/executePython] PythonError`. Console probe NOT RUN; cause/worker topology UNKNOWN. Preserve matching `summary.json`; never rerun artifact-producing attempt.
- Pages preview last successful run #17 / `39433670146` was static simulation from main SHA `90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c`, not app runtime. PocketCode and portfolio Pages share one github.io origin. No secrets, tokens, private source or authority there; live headers/scripts/device context UNKNOWN.
- O-7: official Catrobat Pocket Code and POCO C++ naming/search collisions verified; Xiaomi POCO trademark scope UNKNOWN. No rename or PoCo publication pending direct clearance.

## Next priorities
1. Await separate owner authorization for any source/test or adapter work. The 2026-11-14 request authorized research/specification deliverables only.
2. Once authorized, first resolve journal conflict attribution and dual receipt watermarks; add focused model cases only within that approved scope.
3. Then address grant semantic no-op/event parity, authenticated canonical bytes, relay fencing and atomic consumer inbox; retain the 33-case plan as model-only until authorized.
4. Keep report-v2 migration gated; preserve format 1 and CASE-04 status.
5. Device/browser acceptance needs approved synthetic data and exact target-device evidence. Preserve Pyodios summary. Resolve shared-origin threat boundary before sensitive persistence.

Evidence: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests: PASS / FAIL / NOT RUN. Chat assertions are not proof.
