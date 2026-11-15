STATUS: DONE

## This pass
- Recovered the interrupted checkpoint chain. The only commit after the prior DONE checkpoint was the new IN PROGRESS marker; it changed only this file.
- Re-read BOOT.md, STATE.md and NEXT_TASK.md. CHECKPOINT.md was read to establish the marker. INBOX_chatgpt.md was not read: the three-file content-read budget was exhausted by the required startup documents plus checkpoint recovery.
- Confirmed the latest five commits at startup: f96446c (IN PROGRESS marker), e772138 (prior DONE), 67edd52 (prior marker), 24bb469 (receipt API compatibility revert), 87b2e64 (research corrections).
- Latest successful Actions run #68 (43681167497) is tied to 24bb469 but checks out pinned historical P40 SHA 319cffef; it does not verify that branch source. Current checkpoint commit f96446c has zero check runs/status contexts. Exact-tree tests NOT RUN.
- No source/test changes: the 3-file read cap was consumed by startup/recovery. No PR, workflow, provider, adapter, infrastructure or canonical acceptance changes.

## State
VERIFIED: detached snapshot provenance/freshness is the highest-priority model gap; previous source refactor was reverted to preserve test/API compatibility. P39 adapter conformance remains CLOSED. CASE-04 remains INCOMPLETE / timed_out. Report format 1 retained.

## Next
1. In a fresh bounded pass, inspect EventJournal, receipt API and all affected tests; migrate API and tests together to derive fresh journal evidence at receipt creation.
2. Add regression cases for late scoped conflicts, attempted forged snapshot construction and exact effect/attempt scope.
3. Keep exact-tree test status NOT RUN until output exists. Do not alter CI workflow without separate authorization.

Constraints retained: $0; preserve all LOOP/CASE/D/OD IDs; preserve Pyodios summary artifact; no PR #2/#3/#4 changes; no adapter/provider/device/deployment work.
