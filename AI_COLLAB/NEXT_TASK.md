# NEXT TASK: PocketCode   (one task; under 350 words)

## Goal
Perform a separate source-pinned consistency audit of `EXIT_PROVENANCE_RESOLUTION_20261108.md` against the immutable report helper, its tests, canonical execution-loop acceptance and provenance matrix. Identify any missing/contradictory EP cases and prepare a precise reviewer checklist. This is a ChatGPT static check only, not a substitute for Claude's independent review or owner resolution.

## Files to read
- `EXIT_PROVENANCE_RESOLUTION_20261108.md` (relevant sections only)
- `scripts/report_contract.py` and `scripts/test_report_contract.py` at their recorded immutable blob/source pins
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` at its recorded immutable pin
- `AI_COLLAB/VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md` (relevant sections only)
- `AI_COLLAB/P39_SOURCE_PINNED_AUDIT_CROSSWALK_20261108.md` only if needed for shared evidence-boundary terminology

## Constraints
- Normal mode, about 350 lines per turn. Commit continuity updates before summarizing.
- No source/test changes; no verdict precedence patch.
- Preserve CASE-04 as INCOMPLETE / timed_out until child/wrapper/termination provenance is resolved.
- Do not change canonical LOOP, CASE or D IDs.
- Keep VERIFIED / INFERRED / UNKNOWN / NOT RUN distinct.
- Do not select a runtime, provider, database or adapter.

## Steps
1. Re-fetch and verify every immutable source/test/acceptance pin before relying on it.
2. Cross-check every EP-01..EP-20 case against helper behavior, current tests and canonical acceptance.
3. Identify missing adversarial combinations: contradictory child/wrapper observations, delayed/stale exit, signal/forced termination, timeout/cancel races, missing evidence, cleanup degradation and attempt/command misbinding.
4. Record only demonstrable gaps and exact source lines; avoid duplicating existing CASE tests.
5. Prepare a reviewer reconciliation checklist for Claude and owner decisions.

## Done when
The static consistency audit and reviewer checklist are committed and indexed, with source/test execution status stated honestly. The independent review gate remains open until Claude's report and owner disposition arrive.
