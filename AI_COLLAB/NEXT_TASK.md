# NEXT TASK: PocketCode

## Goal
Complete the owner-approved P40 read-only run. Approval is recorded; execution is currently blocked because GitHub dispatch is not exposed and local checkout cannot reach GitHub.

## Current evidence
- VERIFIED: Claude and Gemini P39 reviews are reconciled. Claude's provider/design strategy drafts were independently audited but are not P39 gate evidence.
- VERIFIED: P40 six-lane protocol exists; NOT AUTHORIZED / NOT RUN. Historical 266/266 PASS applies only to SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.
- OD-01..OD-13 ADOPTED under explicit owner delegation; see `P39_OWNER_DELEGATED_DECISIONS_20261111.md`. No live streaming in MVP; fully staged and verified bounded artifact download/share remains. Policy covers revocation, epoch consistency, authoritative time, durable identities, receipt binding, exit projection, termination and client acknowledgement.
- CASE-04 INCOMPLETE / timed_out. Pyodios Console probe NOT RUN. Live Pages response/headers and sibling script behavior UNKNOWN.
- Claude C01.4: repository continuity has been used in practice; fresh-chat one-line resume remains unproven. ChatGPT repo creation UNKNOWN. Current CI has path filters/cancellation/Python 3.12 but no Python/SQLite version print.

## Ranked steps
1. Secure an execution path for the approved exact target SHA. Manual `workflow_dispatch` is not available because the workflow file is absent from default branch `main` (GitHub requires it there). The current GitHub connector supports reads/log retrieval but no dispatch; container clone failed DNS.
2. Ask owner before a narrowly scoped workflow-only change on the active branch that prints Python/SQLite versions and pins checkout to target SHA. The existing push path filter will trigger it. No workflow/config edits are currently authorized.
3. Alternatively, owner can run the exact commands in the authorization record at target SHA and supply complete output. Keep lane 4 BLOCKED and model results separate from adapter/CASE acceptance.
4. Obtain owner-run Pyodios Console evidence and reliable read-only Pages/origin evidence.
5. Prove fresh-chat resume. CI version printing is included only in the bounded run request, not a workflow change.

## Constraints
- D-005/D-006: $0. No API keys/provider calls, paid tests/hosting, Apple Developer Program, TestFlight or App Store.
- No runtime/provider/database/transport choice, source/test edits, device tests, deployment/settings/DNS changes, PR #2/#3/#4 changes or RevDev work without applicable owner authorization.
- Preserve LOOP-01..14, CASE-01..16 and all D-IDs. OD policy is adopted by explicit delegation; do not infer implementation authorization from it.
- Evidence: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests: PASS / FAIL / NOT RUN.
- Commit before summarizing; checkpoint after each unit; keep files within their stated word limits.
