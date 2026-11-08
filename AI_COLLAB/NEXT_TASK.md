# NEXT TASK: PocketCode   (one task; under 350 words)

## Goal
Build a compact canonical acceptance traceability crosswalk for the new P39 adapter obligations and EP-01..EP-25 exit-provenance proposals. Identify which requirements are already covered by LOOP-01..14 / CASE-01..16, which are refinements of existing cases, and which are adapter-only obligations that must not be misrepresented as new canonical acceptance IDs.

## Files to read
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` at immutable blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`
- `AI_COLLAB/CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md` (relevant sections only)
- `AI_COLLAB/P39_SOURCE_PINNED_AUDIT_CROSSWALK_20261108.md`
- `AI_COLLAB/EXIT_PROVENANCE_RESOLUTION_20261108.md` and `EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md` (relevant sections only)

## Constraints
- Normal mode, about 350 lines per turn. Commit continuity updates before summarizing.
- No source/test changes, no canonical LOOP/CASE/D ID changes, no adapter/provider/database/runtime selection.
- Do not inflate product acceptance scope with implementation-only details.
- Keep VERIFIED / INFERRED / UNKNOWN / NOT RUN distinct.
- Preserve separate P37 and P39 test namespaces.

## Steps
1. Map each P39-S1..S8 finding and P39-EVENT/OUTBOX/STREAM/POLICY test family to the closest canonical LOOP/CASE requirements, if any.
2. Map EP-01..EP-25 to existing CASE coverage or explicitly label them as coordinator/adapter refinements.
3. Identify true uncovered product requirements separately from lower-level conformance tests.
4. Flag ambiguous mappings for owner review; do not invent canonical IDs.
5. Record the crosswalk and reviewer decision points.

## Done when
Every new proposed test has a traceable relationship (or explicit no-direct-canonical-mapping rationale), without changing canonical acceptance or authorizing implementation.
