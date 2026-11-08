# NEXT TASK: PocketCode   (one task; under 350 words)

## Goal
Create a canonical acceptance traceability crosswalk for the reconciled P39 findings, receipt-subsystem audit, and EP-01..EP-25 exit-provenance proposals. Separate product-level requirements already covered by LOOP-01..14 / CASE-01..16 from lower-level model/adapter conformance tests and unresolved owner policy decisions.

## Files to inspect
- PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md at immutable blob c6714c27db52b2962fe8d1c7e6a16829d46a8338
- AI_COLLAB/CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md (relevant sections only)
- AI_COLLAB/P39_SOURCE_PINNED_AUDIT_CROSSWALK_20261108.md
- AI_COLLAB/P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md
- AI_COLLAB/P39_RECEIPT_SUBSYSTEM_AUDIT_20261108.md
- AI_COLLAB/EXIT_PROVENANCE_RESOLUTION_20261108.md and EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md (relevant sections only)

## Constraints
- Normal mode, about 350 lines per turn. Commit continuity updates before summarizing.
- No source/test changes, no canonical LOOP/CASE/D ID changes, no adapter/provider/database/runtime selection.
- Do not inflate product acceptance scope with implementation-only details.
- Preserve P37/P39 test namespaces and distinguish sequential-model tests from production-adapter tests.
- Keep VERIFIED / CLAUDE-REPORTED / INFERRED / UNKNOWN / NOT RUN distinct.

## Steps
1. Map each P39-S1..S8 and RG-B1..B3/H1..H4/O1..O10 finding to the closest canonical LOOP/CASE requirements, if any.
2. Map RCP-01..05 to receipt/recovery/authorization/stream acceptance; identify adapter-only requirements.
3. Map EP-01..25 to existing CASE coverage or explicitly label them as coordinator/adapter refinements.
4. Identify genuine uncovered product requirements separately from implementation-level tests.
5. Flag owner decisions: pre/post-commit revocation, streaming MVP scope, EP-18/24, and compact ReceiptHead digest binding.
6. Record the crosswalk without inventing canonical IDs.

## Done when
Every proposed test has a traceable relationship or explicit no-direct-canonical-mapping rationale; reviewer and owner gates remain accurately open.
