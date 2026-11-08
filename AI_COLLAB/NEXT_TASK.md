# NEXT TASK: PocketCode   (one task; under 350 words)

## Goal
Reconcile the exit-provenance proposal with the static consistency audit, then prepare a precise independent review request for Claude and an owner decision list. Resolve the report projection boundary on paper only. No source-code or test changes until Claude's review and owner decisions clear the gate.

## Files to read
- `EXIT_PROVENANCE_RESOLUTION_20261108.md` (relevant sections only)
- `EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md` (relevant sections only)
- `scripts/report_contract.py` and `scripts/test_report_contract.py` only at their immutable pins if needed
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` at its immutable pin
- `AI_COLLAB/INBOX_claude.md` for the existing review request

## Constraints
- Normal mode, about 350 lines per turn. Commit continuity updates before summarizing.
- No source/test changes and no verdict-precedence patch.
- Preserve CASE-04 as INCOMPLETE / timed_out.
- Do not change canonical LOOP, CASE or D IDs.
- Preserve raw lifecycle, child exit, wrapper exit, termination, cleanup and artifact facts separately.
- Keep VERIFIED / INFERRED / UNKNOWN / NOT RUN distinct.

## Steps
1. Clarify that EP-04/05 cannot be rendered by the current two-field classifier without a pre-resolved verdict/renderer contract or an explicitly documented compatibility limitation.
2. Decide whether EP-21..25 are distinct required cases and merge overlaps without losing assertions.
3. Record owner decisions required for EP-18 (policy/egress barrier violation) and EP-24 (child success plus wrapper/cleanup failure).
4. Update the Claude review request with exact pins, static-audit findings and questions.
5. Keep the implementation gate closed pending independent review and owner disposition.

## Done when
The proposal, static audit and reviewer request agree on unresolved semantics and a concrete acceptance path, with no source/test changes.
