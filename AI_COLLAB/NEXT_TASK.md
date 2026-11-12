# NEXT TASK: PocketCode

## Goal
Turn the remaining grant-event relay and untrusted-execution gaps into versioned, acceptance-ready contracts without crossing the closed implementation gate.

## Current evidence
- VERIFIED: Claude and Gemini P39 reviews are reconciled. Claude's provider/design strategy drafts were independently audited but are not P39 gate evidence.
- VERIFIED: P40 lanes 1,2,3,5,6 and full scripts suite PASS on exact target SHA `319cffef121e327331aeaff59522ae279b112ecc`; run `43126974602`. Totals: 26,22,27,59,31; full suite 266/266. Lane 4 remains BLOCKED / NOT TESTABLE. These are model-only results.
- OD-01..OD-13 ADOPTED under explicit owner delegation; see `P39_OWNER_DELEGATED_DECISIONS_20261111.md`. No live streaming in MVP; fully staged and verified bounded artifact download/share remains. Policy covers revocation, epoch consistency, authoritative time, durable identities, receipt binding, exit projection, termination and client acknowledgement.
- CASE-04 INCOMPLETE / timed_out. Pyodios Console probe NOT RUN. Live Pages response/headers and sibling script behavior UNKNOWN. Research and red-team results are in `FULL_POWER_GAP_RESEARCH_20261112.md`.
- CI workflow now prints Python/SQLite/OS versions and checks out the immutable P40 target; actual environment was Python 3.12.16, SQLite 3.46.1, Ubuntu 26.04.1. Node 20 deprecation warning remains on current action major versions.
- Claude C01.4: repository continuity has been used in practice; fresh-chat one-line resume remains unproven. ChatGPT repo creation UNKNOWN.

## Ranked steps
1. Specify the grant-event envelope, atomic aggregate/event parity, relay lease/fence, ordered publication, stale-ack rejection and consumer inbox atomicity. Separate producer authentication from CloudEvents identity/digest fields.
2. Specify opaque-origin browser execution and the bounded parent/sandbox message protocol; include no ambient authority, default-deny network, explicit file copies, teardown and resource-containment limits.
3. Owner-run the read-only Pyodios Console probe and record exact `sys.last_exc`/`sys.last_value` output.
4. Collect read-only Pages response/header/service-worker and portfolio-script evidence; no deploy/settings changes.
5. Plan fresh-chat resume proof and target-device storage/recovery matrix. Keep all model results distinct from adapter/CASE acceptance.

## Constraints
- D-005/D-006: $0. No API keys/provider calls, paid tests/hosting, Apple Developer Program, TestFlight or App Store.
- No runtime/provider/database/transport choice, source/test edits, device tests, deployment/settings/DNS changes, PR #2/#3/#4 changes or RevDev work without applicable owner authorization. The P40 workflow-only change is complete and limited to test execution.
- Preserve LOOP-01..14, CASE-01..16 and all D-IDs. OD policy is adopted by explicit delegation; do not infer implementation authorization from it.
- Evidence: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests: PASS / FAIL / NOT RUN.
- Commit before summarizing; checkpoint after each unit; keep files within their stated word limits.
