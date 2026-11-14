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
- Latest source/test commits: grant model `45cb200`; grant regression correction `ed4d821`; journal/receipt snapshot model `9f0ade8`; snapshot seal `af0c770`; package-mode import correction `a4e27bb`. Latest source/test commit `a4e27bb` adds snapshot scope-isolation and immutable-capture tests. Latest branch head after docs: `1af50969da7681b848da80e97afe9ca60b574f6a`.
- `ed4d821` corrects the stale future-event fixture to use a canonical event, makes the changed-payload test use a valid recomputed digest with the same event identity, and adds malformed-envelope rejection coverage. The focused grant test file now contains 30 test methods (static count only).
- Latest source-triggered Actions run #63 (`43627117644`) on commit `9f0ade8` completed SUCCESS, 266/266, Python 3.12.16 on Ubuntu. However, workflow step `Check out immutable P40 target` checks out fixed historical SHA `319cffef121e327331aeaff59522ae279b112ecc`; run #63 therefore did not execute any journal snapshot changes. Latest head `1af5096` has zero Actions runs and zero status contexts (pending); exact-tree snapshot tests remain NOT RUN. The workflow is non-verifying for current branch source until its checkout policy is separately authorized and corrected.
- Historical Actions run #59 (`43126974602`) passed 266/266 on different model target SHA `319cffef121e327331aeaff59522ae279b112ecc`; not current-head CI, adapter proof or CASE acceptance.

## Accepted decisions and gates
- D-001 unified PC/phone direction with separate project boundaries; D-002 GitHub as durable source; D-003 no secrets in public repo; D-004 validate before stack commitment; D-005/D-006 $0.
- OD-01..OD-13 adopted 2026-11-11. No live/incremental artifact streaming in MVP; bounded download/share only after full staging, integrity verification and fresh authorization.
- P39 product-policy gate CLEARED by owner delegation; P39 implementation/adapter conformance gate CLOSED. Owner separately authorized the bounded model-only journal/receipt source and test slice. No provider calls, device tests, deployment, DNS/settings, PR changes, adapter work or infrastructure selection authorized.
- CASE-04 remains INCOMPLETE / timed_out. Model PASS never closes adapter or canonical CASE acceptance.

## Current known gaps (model/design evidence, not production proof)
- Grant model (VERIFIED in source at `45cb200`, regression tests corrected at `ed4d821`): identical progress is a semantic no-op; changed progress advances the aggregate and appends matching versioned event/outbox records at one in-memory commit point; consumer recomputes canonical event digest and validates source/event identity/version before accepting. Tests now exercise valid-digest identity collisions and malformed envelope rejection; NOT RUN. The model still is not durable/atomic across processes, and producer authentication, relay leases/fences, stale acknowledgements and consumer inbox/restore remain adapter obligations. 33-case plan remains model-only.
- Journal/receipt model (VERIFIED in source at `97b302f`, extended at `9f0ade8`, hardened at `af0c770` and `91c0d12`, scope-tested at `a4e27bb`): conflicts retain attempted producer issuer/subject/key ID, effect/attempt/fence and timestamps. EventJournal now emits an immutable, effect/attempt-scoped `JournalReceiptSnapshot` containing journal-global observation/accepted-event high-waters and matching conflict sequence references. Receipt creation requires this typed snapshot for nonzero journal evidence, checks exact effect/attempt identity, rejects caller-supplied scalar claims and binds derived values into the immutable fingerprint. A private module seal rejects ordinary caller-constructed snapshot dataclasses. Regression coverage includes cross-effect/attempt conflict isolation and snapshot immutability after later appends. This remains an in-memory Python model, not durable/cryptographic journal-store binding; hostile code in the same Python process can inspect module internals, and adapters must still establish trust, persistence and atomicity.
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
1. Run exact-tree focused tests when a network-capable execution path is available; current test status is NOT RUN and the pinned workflow is non-verifying.
2. Red-team and close the journal-to-receipt composition boundary: conflict sequence references are still caller-supplied and are not resolved against an EventJournal instance.
3. Extend grant model coverage for envelope identity, transition replay/order and outbox delivery semantics. Keep relay fencing, atomic inbox adapters and provider integrations gated.
4. Keep report-v2 migration gated; preserve format 1 and CASE-04 status.
5. Device/browser acceptance needs approved synthetic data and exact target-device evidence. Preserve Pyodios summary. Resolve shared-origin threat boundary before sensitive persistence.

Evidence: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests: PASS / FAIL / NOT RUN. Chat assertions are not proof.
\n\n## 2026-11-14 journal snapshot update\n- `JournalReceiptSnapshot` now derives journal-global watermarks and conflict sequences scoped to the exact effect/attempt. `ResultReceiptStore.create_receipt` consumes this snapshot, checks scope, rejects legacy scalar claims and fingerprints the derived evidence. Added a private seal and regression tests for matching scope, immutable successor evidence, rejection of caller-supplied values, mixed inputs and ordinary unsealed construction.\n- Source/test commits: `9f0ade8`, `af0c770`, `91c0d12`, `a4e27bb`. Static review only for these commits; NOT RUN. The CI run #63 associated with `9f0ade8` checked out pinned historical `319cffef` and ran 266/266 successfully, so it is not evidence for these changes.\n