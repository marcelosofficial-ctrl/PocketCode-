# NEXT TASK: PocketCode   (one task; under 350 words)

## Goal
Close the evidence gap Claude explicitly left: independently audit the receipt-head implementation and its tests, plus the durable-adapter contract, against P37/P39 receipt identity, immutable fingerprint, concurrency and recovery claims. Claude did not read these files, so do not assume RG-O1/O2/O3 or RACE-01..06 describe the whole receipt subsystem.

## Files to inspect (bounded reads only)
- `scripts/result_receipts.py` at source SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`, in focused line ranges (never whole file; it is ~35 KB).
- `scripts/test_result_receipts.py` at the same SHA, focused test ranges only (~40 KB).
- `AI_COLLAB/DURABLE_ADAPTER_CONTRACT_20261106.md`, relevant sections only.
- `AI_COLLAB/RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md`, relevant sections only.
- `AI_COLLAB/P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md` and `P39_SOURCE_PINNED_AUDIT_CROSSWALK_20261108.md`.

## Constraints
- Normal mode, about 350 lines per turn. Commit continuity updates before summarizing.
- Use line-range reads and search; never open a file over 1,500 words whole.
- No source/test changes, no database/provider/runtime selection, no canonical ID changes.
- Distinguish model behavior from real concurrent/durable adapter evidence.
- Keep VERIFIED / CLAUDE-REPORTED / INFERRED / UNKNOWN / NOT RUN distinct.

## Steps
1. Verify blob pins for both receipt source and tests at 744cb4d.
2. Map functions and test names for seed/advance/head CAS, receipt identity reuse, digest/quarantine, same-key replay, idempotency fingerprint and concurrency.
3. Check whether tests assert stored state after races, and whether barriers/independent connections exist or only sequential simulation.
4. Cross-check durable-adapter clauses for atomicity, restore, retention, crash windows and uniqueness.
5. Reconcile Claude RG-O1..O4 and missing-test proposals with actual coverage; correct or reject any overreach.
6. Commit a bounded source-pinned receipt audit and update the reviewer/owner reconciliation table.

## Done when
The previously unread receipt subsystem and durable-adapter contract have a precise evidence map, with all claims scoped to what the code/tests can actually establish.
