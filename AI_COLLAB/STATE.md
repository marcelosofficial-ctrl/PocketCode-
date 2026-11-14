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
- Start of 2026-11-14 continuation: HEAD `0195910c3e686d3567411e4101f1f00c2be0a7e7`; latest five: `0195910`, `109a6e6`, `9064c85`, `10935cd`, `4447193`.
- Exact start HEAD: zero commit statuses and zero PR-triggered workflow runs; tests NOT RUN. Historical Actions run #59 (`43126974602`) passed 266/266 on different model target `319cffef121e327331aeaff59522ae279b112ecc`; not current-head CI, adapter proof or CASE acceptance.
- Source-audited baseline `f02065853404b325e0f87ac7045807ad5fe3edfc`: ten commits ahead, zero behind. Compare shows only STATE/NEXT_TASK/CHECKPOINT changed; no application source, tests, workflows or product assets changed.

## Accepted decisions and gates
- D-001 unified PC/phone direction with separate project boundaries; D-002 GitHub as durable source; D-003 no secrets in public repo; D-004 validate before stack commitment; D-005/D-006 $0.
- OD-01..OD-13 adopted 2026-11-11. No live/incremental artifact streaming in MVP; bounded download/share only after full staging, integrity verification and fresh authorization.
- P39 product-policy gate CLEARED by owner delegation; P39 implementation/adapter conformance gate CLOSED. No source/test edits, provider calls, device tests, deployment, DNS/settings, PR changes or infrastructure selection without separate scope authorization.
- CASE-04 remains INCOMPLETE / timed_out. Model PASS never closes adapter or canonical CASE acceptance.

## Current known gaps (model/design evidence, not production proof)
- Grant model: aggregate/event parity and no-op semantics; canonical first-delivery digest and producer/scope authentication; grant-event relay lease/fence/stale-ack; atomic consumer inbox/restore. 33-case plan is model-only.
- Journal/receipt: quarantined conflicts are outside accepted-event projection and can be omitted from receipt uncertainty/evidence; no explicit journal high-water in receipt. Attribution or conservative quarantine is needed. This is an INFERRED model integration gap, not proof of production exploit.
- Lifecycle/receipt: execution_projection.py and result_receipts.py are pure/in-memory. Child verdict, job/evidence disposition and artifact disposition remain separate; no integrated authenticated policy/egress barrier, authoritative termination proof or client-generated acknowledgement bound to exact artifact digest/version/range.
- EventJournal AuthenticatedProducer is supplied model input, not cryptographic verification. Report format 1 lets nonzero integer exit override timeout/cancel/rejection/infrastructure/nonterminal state; keep format 1 until gated format-2 migration.
- Opaque-origin Worker acknowledgement proves supervisor called terminate() on its Worker and closed the channel only, not native child exit or OS/renderer teardown. Keep this distinct from OD-12 proof.
- Dispatch/projection helpers were checked against their contract; trusted caller owns authentication, persistence, sequence ordering and deduplication. No helper defect established.
- Mobile runner is simulation-only; its static checker does not prove browser/device/accessibility/runtime/security behavior.

## Device, origin and naming
- Owner-reported Pyodios iPhone: app 1.1.0 Build 7, Pyodide 314.0.5, Python 3.14.2; Editor showed `[Bridge/executePython] PythonError`. Console probe NOT RUN; cause/worker topology UNKNOWN. Preserve matching `summary.json`; never rerun artifact-producing attempt.
- Pages preview last successful run #17 / `39433670146` was static simulation from main SHA `90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c`, not app runtime. PocketCode and portfolio Pages share one github.io origin. No secrets, tokens, private source or authority there; live headers/scripts/device context UNKNOWN.
- O-7: official Catrobat Pocket Code and POCO C++ naming/search collisions verified; Xiaomi POCO trademark scope UNKNOWN. No rename or PoCo publication pending direct clearance.

## Next priorities
1. After separate authorization, resolve journal-conflict attribution/quarantine and receipt completeness; then add focused model tests.
2. Until authorization, wait for a genuinely new owner task/evidence. Do not repeat completed receipt, dispatch/projection or mobile-prototype reviews.
3. Preserve 33-case grant and 14-case report-v2 plans for a separately authorized model/test scope.
4. Device/browser acceptance needs approved synthetic data and exact target-device evidence. Preserve Pyodios summary.
5. Resolve shared-origin threat boundary before sensitive persistence. No host migration/deployment or stack selection without owner decision.

Evidence: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests: PASS / FAIL / NOT RUN. Chat assertions are not proof.
