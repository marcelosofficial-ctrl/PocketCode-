# NEXT TASK: PocketCode

## Goal
Continue evidence closure without reopening the P39 implementation/adapter gate. No source/test work is authorized by existing design or P40 evidence.

## Verified start snapshot (2026-11-14)
- Branch HEAD: `dec8b755870d5f70bcf4a7d2109d26fa2282320e`; latest five: `dec8b75`, `ecda8de`, `22ac837`, `0195910`, `109a6e6`. Fetch live ref and latest five on every resume.
- Thirteen ahead / zero behind source-audited baseline `f02065853404b325e0f87ac7045807ad5fe3edfc`; changed paths are BOOT, STATE, NEXT_TASK, CHECKPOINT and WORK_PROTOCOL only.
- Exact-HEAD statuses and PR-triggered runs: zero. Tests NOT RUN. Historical run #59 passed 266/266 on another SHA; not current-head CI or acceptance.

## Completed
- Read required startup files, INDEX and latest five commits; inbox has no new task.
- Reconciled stale resume metadata: BOOT now explicitly includes itself first; WORK_PROTOCOL includes CHECKPOINT in the startup sequence and states continuity budgets.
- Prior static mobile-runner review confirmed simulation-only scope; it did not prove browser/device/runtime/security behavior.
- Prior dispatch/projection review found no helper defect. Journal conflict-to-receipt propagation remains the known model integration gap.

## Next
1. Until separate authorization, wait for a genuinely new owner task/evidence. Do not repeat receipt, dispatch/projection or prototype audits.
2. After scoped authorization, address journal-conflict attribution/quarantine and receipt high-water/uncertainty; only then add focused model tests.
3. Keep grant 33-case and report-v2 14-case plans ready. P39 implementation/adapter gate CLOSED.

## Constraints
- $0; no provider/runtime/database/transport/storage/host choice, deployment, DNS, PR #2/#3/#4 changes or external AI request.
- Preserve LOOP-01..14, CASE-01..16, D-IDs, OD-01..13. CASE-04 remains INCOMPLETE / timed_out.
- Preserve successful Pyodios summary.json; no artifact rerun. Device/browser acceptance requires approved synthetic data and exact-device evidence.
- Resume: BOOT, STATE, NEXT_TASK, CHECKPOINT, INBOX_chatgpt; then live HEAD/latest five; use INDEX after startup. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
