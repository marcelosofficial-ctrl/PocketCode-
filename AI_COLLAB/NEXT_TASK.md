# NEXT TASK: PocketCode

## Goal
Complete P39 review reconciliation and owner-decision gate. No implementation until explicitly cleared.

## Evidence
- Claude P39: `P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md`; C1-C7 were Claude-reported runs against a byte-identical copy, not the repository suite.
- Gemini P39: `GEMINI_P39_REVIEW_RECONCILIATION_20261109.md`; independent report received and source-reconciled. Gemini tests NOT RUN.
- Integrated sequence: `P39_GATE_CLOSURE_PLAN_20261109.md`; finding-level consensus/conflict matrix: `P39_REVIEW_CONSENSUS_MATRIX_20261109.md`.
- Canonical traceability: `P39_SOURCE_PINNED_AUDIT_CROSSWALK_20261108.md`, `P39_EP_CANONICAL_ACCEPTANCE_CROSSWALK_20261108.md`.
- Owner decisions OD-01..OD-13: `P39_EXIT_OWNER_DECISION_REGISTER_20261108.md`, all OPEN.
- Exit provenance: `EXIT_PROVENANCE_RESOLUTION_20261108.md`, `EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md`; CASE-04 remains INCOMPLETE / timed_out.
- Claude inbox: one OPEN strategy-program assignment. Await any additional Claude artifact supplied by owner; do not create a competing assignment.

## Steps
1. If an additional Claude review arrives, pin its repo/branch/SHA/blob hashes, scope, files read and tests run. Reconcile each claim against the existing matrix and canonical crosswalk; do not create a competing Claude assignment.
2. Complete one finding-level consensus/conflict matrix with severity, exact source pin, model/adapter/owner classification, canonical trace, P39 test ID and evidence status. Merge overlaps; do not duplicate tests or alter LOOP/CASE/D IDs.
3. Obtain explicit OD-01..OD-13 decisions. Resolve streaming first; revocation lifecycle together; clock/identity; receipt binding; exit verdict/termination/cleanup; client-byte evidence.
4. Freeze versioned model semantics only after owner decisions. Then seek explicit authorization for a bounded model-only P40 slice.
5. Prove model behavior with targeted P39 tests and full suite on exact SHA. Test durable adapter, concurrency, crash/restart/restore and transport separately. Supporting P39 tests never imply canonical CASE PASS.
6. Keep PR #2/#3/#4 untouched. No stack/provider/database/runtime/transport choice, paid service, device/PWA implementation or source/test edits without gate clearance.
7. Refresh branch HEAD, latest five commits and exact-SHA Actions before checkpointing.

## Constraints
- P39/P40 implementation gate CLOSED; OD-01..OD-13 OPEN.
- Preserve VERIFIED / INFERRED / UNKNOWN / NOT RUN and PASS / FAIL / NOT RUN.
- Historical 266/266 PASS applies only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.
- Keep RevDev evidence separate.

## Done when
All supplied reviews are reconciled, conflicts are explicit, owner decisions are recorded or deliberately deferred, and the owner authorizes a bounded next slice or the exact blockers remain documented.
