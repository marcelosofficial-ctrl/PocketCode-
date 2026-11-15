RECOVERED: inspected the latest 10 commits; this turn's only new project work before recovery was the IN PROGRESS marker.
Earlier commits landed the snapshot model/seal/import/scope tests (`9f0ade8`, `af0c770`, `91c0d12`, `a4e27bb`) and checkpoint docs (`1af5096`, `59344ef`, `5ccc9a8`, `284bc8b`, `6ba850c`).
Concurrent parent `10274bd` only changes `AI_COLLAB/BOOT.md` and adds `AI_COLLAB/kit/docs/TURN_BUDGET_AND_RECOVERY.md`; it records PocketCode naming and hard turn budgets. No product IDs or technical gates changed.
Ten-commit path diff: `AI_COLLAB/BOOT.md`, `AI_COLLAB/CHECKPOINT.md`, `AI_COLLAB/NEXT_TASK.md`, `AI_COLLAB/STATE.md`, `AI_COLLAB/kit/docs/TURN_BUDGET_AND_RECOVERY.md`, `scripts/test_result_receipts.py`.
Latest five before marker: `15ea602`, `10274bd`, `6ba850c`, `284bc8b`, `5ccc9a8`. Live HEAD at recovery marker: `15ea602`.
Unfinished: prior checkpoint overstated the private snapshot seal; CI run #63 did not test the pushed source; stored STATE/NEXT_TASK had stale head references and literal `\n` text.
Current work: red-team snapshot provenance and exact-head CI; then one bounded source/test correction and accurate evidence checkpoint.
Constraints retained: $0, model-only, no workflow edits, no adapters/providers/devices/PRs, no CASE/LOOP/D/OD changes. P39 adapter gate CLOSED.
