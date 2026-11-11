# NEXT TASK: PocketCode

## Goal
Resolve or explicitly defer the owner-controlled P39 decisions; keep implementation and P40 execution gated until then.

## Current evidence
- VERIFIED: Claude and Gemini P39 reviews are reconciled. Claude's provider/design strategy drafts were independently audited but are not P39 gate evidence.
- VERIFIED: P40 six-lane protocol exists; NOT AUTHORIZED / NOT RUN. Historical 266/266 PASS applies only to SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.
- OD-01..OD-13 OPEN. OD-01 is live streaming only, not bounded artifact release. If bounded release remains MVP, decide OD-02..05 grant/revocation/recovery together. OD-13 governs client receipt.
- CASE-04 INCOMPLETE / timed_out. Pyodios Console probe NOT RUN. Live Pages response/headers and sibling script behavior UNKNOWN.
- Claude C01.4: repository continuity has been used in practice; fresh-chat one-line resume remains unproven. ChatGPT repo creation UNKNOWN. Current CI has path filters/cancellation/Python 3.12 but no Python/SQLite version print.

## Ranked steps
1. Owner resolves or explicitly defers OD-01..OD-13.
2. Ingest any further Claude P39/exit artifact supplied by owner; pin repo, branch, commit and blob SHAs, then reconcile.
3. Only after gate clearance and explicit authorization, pin and run the six P40 model lanes and full Python suite separately from canonical CASE acceptance.
4. Obtain owner-run Pyodios Console evidence and reliable read-only Pages/origin evidence.
5. Prove fresh-chat resume with a new chat using only the one-line instruction and repository boot sequence; record outcome. Treat CI Python/SQLite version printing as a proposal, not an authorized workflow change.

## Constraints
- D-005/D-006: $0. No API keys/provider calls, paid tests/hosting, Apple Developer Program, TestFlight or App Store.
- No runtime/provider/database/transport choice, source/test edits, device tests, deployment/settings/DNS changes, PR #2/#3/#4 changes or RevDev work without applicable owner authorization.
- Preserve LOOP-01..14, CASE-01..16 and all D-IDs. No inference of owner decisions.
- Evidence: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests: PASS / FAIL / NOT RUN.
- Commit before summarizing; checkpoint after each unit; keep files within their stated word limits.
