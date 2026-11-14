# NEXT TASK: PocketCode

## Goal
Continue evidence closure without reopening the P39 implementation/adapter gate. No source/test work is authorized by the existing design or P40 evidence.

## Verified start snapshot (2026-11-14)
- Live branch HEAD at start of this continuation: `109a6e61b25922cf24e4522c87e4282e7207aef4`. Latest five: `109a6e6`, `9064c85`, `10935cd`, `4447193`, `6ca4aec`. Always fetch live ref; the checkpoint commit itself advances HEAD. Always fetch live ref and latest five before work.
- Compare from source-audited baseline `f02065853404b325e0f87ac7045807ad5fe3edfc`: nine commits ahead, zero behind; only `AI_COLLAB/CHECKPOINT.md`, `AI_COLLAB/NEXT_TASK.md` and `AI_COLLAB/STATE.md` changed. No source, tests, workflow or product assets changed.
- Exact-HEAD checks for `109a6e6`: zero attached statuses and zero PR-triggered workflow runs. Tests NOT RUN.
- Historical run #59 succeeded on pinned model target `319cffef121e327331aeaff59522ae279b112ecc`, 266/266 scripts. Not current-HEAD CI, adapter proof or CASE acceptance.

## Completed this pass
- Re-read BOOT, STATE, NEXT_TASK, CHECKPOINT and INBOX_chatgpt in order, then INDEX and the latest five branch commits.
- Reconfirmed exact-HEAD CI absence and nine-commit docs-only delta from the source-audited baseline.
- Inspected `prototypes/mobile-runner/README.md`, `prototypes/mobile-runner/index.html`, `scripts/check_mobile_prototype.py` and `scripts/test_check_mobile_prototype.py` as a distinct UI/prototype boundary review.
- VERIFIED: README and page identify the prototype as simulation-only; page source contains no submitted-code execution, file import, artifact creation, provider/runtime call or external dependency. Success/failure controls only select fixed expected fixtures. Clipboard writes are invoked only by explicit copy buttons; selectable-text fallback remains visible. No clipboard polling or automatic capture was found in the inspected source.
- VERIFIED limitation: checker and its unit-test fixture inspect source structure only. They do not execute browser JavaScript or prove clipboard, screen-reader, mobile browser, device, execution, storage or security properties. Treating their pass output as any of those proofs would be invalid. This limitation is stated in the README/checker; no new defect was established.
- No source-to-policy gap established in this seam. Existing journal-conflict/receipt-completeness gap remains the actionable model issue; do not duplicate prior receipt, dispatch/projection or prototype reviews.
- No code/tests/workflow changed. Tests, browser and device checks NOT RUN. P39 implementation/adapter gate remains CLOSED.

## Ranked next work
1. After separate owner authorization, resolve conflict attribution and receipt completeness: retain candidate scope/source identity in quarantine evidence or define conservative quarantine; include journal high-water and conflict uncertainty in receipt projection; add tests for same-attempt changed payload, cross-attempt collision, producer collision, receipt creation after conflict, and unrelated conflict isolation.
2. Until authorization, wait for a genuinely new owner task or new evidence that opens a distinct review seam. Do not repeat the receipt, dispatch/projection or mobile-prototype audits; do not edit source/tests/run model suites without authorization.
3. Keep the 33-case grant plan and 14-case report-v2 plan ready for a separately authorized model/test scope.
4. Device/browser acceptance requires approved synthetic-data build and exact target-device evidence. Preserve successful Pyodios summary.json; never rerun artifact-producing work.
5. Resolve shared github.io origin trust boundary before sensitive persistence. No host migration/deployment or stack choice without owner decision.

## Gate and constraints
- P39 implementation/adapter gate CLOSED. Obtain separate explicit authorization naming exact model-only source/test scope before scripts/tests, adapters or CI.
- D-005/D-006 $0. No provider, runtime, database, transport, storage engine or host selected. No deployment, DNS, PR #2/#3/#4 changes or external AI request.
- Preserve LOOP-01..14, CASE-01..16, D-IDs, OD-01..13. CASE-04 stays INCOMPLETE / timed_out.
- Preserve successful Pyodios `summary.json`; do not rerun artifact-producing work. Device acceptance needs exact-device evidence and approved synthetic data.
- On resume, read BOOT, STATE, NEXT_TASK, CHECKPOINT, INBOX_chatgpt, then fetch live branch HEAD and latest five commits. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
