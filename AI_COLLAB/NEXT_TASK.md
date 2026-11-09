# NEXT TASK: PocketCode

## Goal
Close the independent-review and owner-decision gate for P39 and exit provenance. Do not implement until explicitly cleared.

## Current evidence
- Claude P39 review reconciled: `P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md`.
- Source findings and traceability: `P39_SOURCE_PINNED_AUDIT_CROSSWALK_20261108.md`, `P39_EP_CANONICAL_ACCEPTANCE_CROSSWALK_20261108.md`.
- Receipt/durable adapter audit: `P39_RECEIPT_SUBSYSTEM_AUDIT_20261108.md`.
- Owner decisions OD-01..OD-13: `P39_EXIT_OWNER_DECISION_REGISTER_20261108.md`. All OPEN.
- Exit provenance proposal/audit: `EXIT_PROVENANCE_RESOLUTION_20261108.md`, `EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md`. CASE-04 stays INCOMPLETE / timed_out.
- Primary-source P39 research: `P39_IMPLEMENTATION_GATE_RESEARCH_ADDENDUM_20261109.md`, `EXECUTION_BOUNDARY_DURABILITY_AND_EVIDENCE_RESEARCH_20261109.md`, `P39_EVENT_RELAY_AND_EXIT_BOUNDARY_RESEARCH_20261109.md`.
- No-spend PWA storage/lifecycle contract: `PWA_LOCAL_STORAGE_AND_RECOVERY_CONTRACT_20261109.md`; corrected owner path: `NO_SPEND_PWA_PATH_20261108.md`. Research only; no device test or storage choice.
- PR #4 file-by-file review: `PR4_CONTINUITY_REFINEMENT_RECONCILIATION_20261109.md`. Leave PR #4 OPEN/DRAFT; no merge/close without owner.
- Gemini source-pinned P39 review request remains OPEN in `INBOX_gemini.md` MSG 2026-11-08-2.

## Steps
1. When Gemini's full report arrives, reconcile each finding against immutable source/test pins and Claude; reject unsupported line claims and separate model defects from adapter obligations.
2. Claude exit-provenance review remains desirable for EP-01..25 and CASE-04. Claude has one OPEN strategy-program assignment in `INBOX_claude.md`; do not create a second ask until the owner reprioritizes that lane.
3. Obtain explicit owner dispositions for OD-01..OD-13. Recommendations and reviewer agreement are not approvals.
4. Produce a consensus/conflict matrix and bounded implementation proposal only after reviews and owner decisions are reconciled. Keep P40 closed if any policy/security issue remains.
5. Before any PWA implementation, create a device work packet and test storage, export/import, quota/eviction, multi-tab fencing and worker interruption on supported iOS/Android browsers. The current research does not authorize implementation or establish device behavior.
6. PR #2/#3 remain untouched; PR #4 is not mergeable as-is. No database/provider/runtime/transport selection and no canonical LOOP/CASE/D changes.
7. Refresh HEAD, last five commits and exact-SHA Actions before checkpointing.

## Constraints
- No source/test changes until P39 review and owner-decision gate clears.
- Keep P37/P39 namespaces distinct.
- Preserve VERIFIED / CLAUDE-REPORTED / INFERRED / UNKNOWN / NOT RUN.
- 266/266 PASS applies only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`, not later documentation HEADs.

## Done when
Both independent reviews are reconciled, all owner decisions are explicit, and the next implementation slice is either authorized or blocked with exact reasons.
