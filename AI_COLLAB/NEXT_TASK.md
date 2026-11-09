# NEXT TASK: PocketCode

## Goal
Close independent-review and owner-decision gate for P39/exit provenance. No implementation until explicitly cleared.

## Evidence
- Claude review: `P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md`.
- Source/acceptance maps: `P39_SOURCE_PINNED_AUDIT_CROSSWALK_20261108.md`, `P39_EP_CANONICAL_ACCEPTANCE_CROSSWALK_20261108.md`.
- Owner decisions OD-01..OD-13: `P39_EXIT_OWNER_DECISION_REGISTER_20261108.md`, all OPEN.
- Exit provenance: `EXIT_PROVENANCE_RESOLUTION_20261108.md`, `EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md`; CASE-04 stays INCOMPLETE / timed_out.
- P39 research: `P39_IMPLEMENTATION_GATE_RESEARCH_ADDENDUM_20261109.md`, `EXECUTION_BOUNDARY_DURABILITY_AND_EVIDENCE_RESEARCH_20261109.md`, `P39_EVENT_RELAY_AND_EXIT_BOUNDARY_RESEARCH_20261109.md`.
- PWA research only: `PWA_LOCAL_STORAGE_AND_RECOVERY_CONTRACT_20261109.md`, corrected `NO_SPEND_PWA_PATH_20261108.md`; no device test or storage choice.
- PR #4: `PR4_CONTINUITY_REFINEMENT_RECONCILIATION_20261109.md`; keep OPEN/DRAFT, no merge/close without owner.
- Gemini request OPEN in `INBOX_gemini.md`: MSG 2026-11-08-2 and ADDENDUM 2026-11-09-1 pin six blobs at source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`, define nine review topics and explicitly exclude RevDev evidence.

## Steps
1. Reconcile Gemini's full report finding-by-finding against immutable pins and Claude; separate model defects, adapter obligations and owner policy.
2. Claude exit-provenance review remains desirable for EP-01..25/CASE-04. Claude has one OPEN strategy assignment; do not create a second ask until owner reprioritizes.
3. Obtain explicit OD-01..OD-13 decisions. Reviewer agreement is not owner approval.
4. Produce consensus/conflict matrix and bounded implementation proposal only after review and owner decisions. Keep P40 closed if security/policy issues remain.
5. Before PWA implementation, create device packet and test storage, export/import, quota/eviction, multi-tab fencing and worker interruption on supported iOS/Android browsers.
6. Leave PR #2/#3 untouched; PR #4 is not mergeable as-is. No database/provider/runtime/transport selection or canonical LOOP/CASE/D changes.
7. Refresh HEAD, latest five commits and exact-SHA Actions before checkpointing.

## Constraints
- No source/test changes until P39 review and owner-decision gate clears.
- Keep P37/P39 namespaces distinct.
- Preserve VERIFIED / CLAUDE-REPORTED / INFERRED / UNKNOWN / NOT RUN.
- 266/266 PASS applies only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`, not later documentation HEADs.

## Done when
Both independent reviews are reconciled, all owner decisions are explicit, and next implementation slice is authorized or blocked with exact reasons.
