# NEXT TASK: PocketCode

## Goal
Complete P39 reconciliation and owner gate. Implementation remains blocked.

## Evidence
- Claude P39: `P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md`; C1-C7 were run against a byte-verified copy, not repo CI.
- Gemini P39: `GEMINI_P39_REVIEW_RECONCILIATION_20261109.md`; report reconciled, tests NOT RUN.
- Combined findings: `P39_REVIEW_CONSENSUS_MATRIX_20261109.md`; sequence: `P39_GATE_CLOSURE_PLAN_20261109.md`.
- Owner decisions OD-01..OD-13: `P39_EXIT_OWNER_DECISION_REGISTER_20261108.md`, all OPEN. CASE-04 remains INCOMPLETE / timed_out.
- Claude inbox has one OPEN strategy assignment. Await any additional owner-supplied Claude artifact; do not create a competing assignment.

## Steps
1. If another Claude review arrives, pin repo/branch/SHA/blob hashes, scope, files read and tests run. Reconcile only evidence-backed changes.
2. Keep one conflict matrix with severity, source pin, model/adapter/owner layer, canonical trace, P39 test ID and evidence status. Preserve LOOP/CASE/D IDs.
3. Obtain OD-01..OD-13 explicitly: streaming; revocation lifecycle; clock/identity; receipt binding; exit/termination; client-byte evidence.
4. Before local persistence selection, verify the exact GitHub Pages URL/site type and sibling same-origin content. Resolve ORIGIN-01..10. If shared-origin exposure remains, obtain an owner threat-boundary decision or propose isolation without spending.
5. Freeze model semantics only after owner decisions; then seek explicit authorization for bounded model-only P40.
6. Run targeted P39 tests and full suite on exact SHA. Test durable adapter, concurrency, crash/restart/restore and transport separately. P39 tests never imply canonical CASE PASS.
7. Keep PR #2/#3/#4 untouched. No stack choice, spending, device/PWA implementation or source/test edits before gate clearance.
8. Refresh branch HEAD, latest five commits and exact-SHA Actions before checkpointing.

## Constraints
- P39/P40 gate CLOSED; OD-01..OD-13 OPEN.
- Preserve VERIFIED / INFERRED / UNKNOWN / NOT RUN and PASS / FAIL / NOT RUN.
- Historical 266/266 PASS applies only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.
- Keep RevDev evidence separate.

## Done when
All supplied reviews are reconciled, conflicts explicit, owner decisions recorded or deferred, and the owner authorizes a bounded next slice or the remaining blockers are documented.
