# NEXT TASK: PocketCode   (one task; under 350 words)

## Goal
Close the independent-review and owner-decision gate for P39 and exit provenance. Do not implement until the gate is explicitly cleared.

## Current artifacts
- Claude P39 review: owner-supplied attachment, reconciled in P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md.
- Receipt subsystem/durable-adapter audit: P39_RECEIPT_SUBSYSTEM_AUDIT_20261108.md.
- Canonical traceability: P39_EP_CANONICAL_ACCEPTANCE_CROSSWALK_20261108.md.
- Consolidated owner decisions OD-01..OD-13: P39_EXIT_OWNER_DECISION_REGISTER_20261108.md. All OPEN; recommendations are not owner approvals.
- Exit provenance proposal/static audit: EXIT_PROVENANCE_RESOLUTION_20261108.md and EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md.
- Primary-source research and red-team corrections: P39_IMPLEMENTATION_GATE_RESEARCH_ADDENDUM_20261109.md. It does not alter OD decisions or authorize implementation.
- Gemini independent P39 review requested in INBOX_gemini.md MSG 2026-11-08-2.
- Claude exit-provenance review was requested in earlier INBOX_claude MSG 2026-11-08-3/4, but those entries were superseded by Claude's later inbox rewrite; no independent exit review is present in the current ChatGPT inbox. Re-request only if this review remains in scope.

## Steps
1. When Gemini's full report arrives, reconcile each finding against Claude and immutable source/test pins. Reject unsupported path/line claims; separate model defects from adapter obligations.
2. Confirm whether Claude's exit review remains required. If received, reconcile EP-01..25, the typed projection/renderer boundary, termination proof and CASE-04.
3. Obtain explicit owner dispositions for OD-01..OD-13. Do not infer decisions from silence or reviewer agreement.
4. Produce one conflict/consensus matrix and a bounded implementation proposal only after both reviews and owner decisions are reconciled.
5. Decide whether a model-only P40 slice is authorized. If any policy or security decision remains open, keep implementation gate closed.
6. Refresh branch HEAD, last five commits and latest Actions before checkpointing. Preserve the exact-SHA boundary: 266/266 applies only to 744cb4d, not documentation HEAD.

## Constraints
- No source/test changes until review gate and owner decisions clear.
- No database/provider/runtime/transport selection.
- No canonical LOOP/CASE/D changes; keep P37/P39 namespaces separate.
- Distinguish sequential model evidence from real adapter evidence.
- Preserve VERIFIED / CLAUDE-REPORTED / INFERRED / UNKNOWN / NOT RUN.

## Done when
Both independent reviews are reconciled, all owner decisions are explicit, and the next implementation slice is either authorized or blocked with exact reasons.
