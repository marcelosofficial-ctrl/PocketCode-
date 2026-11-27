# NEXT TASK: PocketCode — validate receipt live-journal migration and close snapshot race

## Work completed (VERIFIED source commits)
- `scripts/result_receipts.py`: create_receipt now accepts `journal: Optional[EventJournal]`; it derives snapshot fields inside the method. Detached snapshot and scalar evidence parameters removed; no-journal receipt retains zero watermarks.
- `scripts/test_result_receipts.py`: helper now returns live journal; watermark test migrated; late-conflict regression creates predecessor receipt, appends conflict to SAME journal, then creates successor and asserts new conflict refs plus predecessor digest immutability; obsolete detached/supplied evidence tests updated.
- Tests were NOT RUN this turn. Exact-head Actions result pending.


## Remaining
1. Run exact-head unittest-head and inspect logs; test may expose API migration regressions.
2. EventJournal receipt snapshot still not synchronized. Decide and implement locking for append/receipt_snapshot/fence mutation, with a deterministic concurrency/coherence test if feasible; preserve append sequencing/fence semantics. This is a research model only.
3. Verify no downstream callsites in scripts still pass journal_snapshot or legacy scalar kwargs; migrate any affected files if necessary, ≤2 files/commit.
4. Update STATE only after exact evidence; no adapter/device/runtime claims.

## Guardrails
No provider/adapter/runtime/storage/workflow/PR changes. Preserve identifiers/contracts and explicit model-only scope. Record VERIFIED / INFERRED / UNKNOWN / NOT RUN accurately.