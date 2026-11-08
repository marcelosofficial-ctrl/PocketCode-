# NEXT TASK: PocketCode   (one task; under 350 words)

## Goal
Complete the independent-review and owner-decision reconciliation gate for P39 and exit provenance, without implementing source changes prematurely.

## Inputs to reconcile
- Claude P39 review: owner-supplied attachment, reconciled in P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md.
- Gemini independent P39 review requested in INBOX_gemini.md MSG 2026-11-08-2; keep it independent and do not treat the earlier research plan as the review.
- Claude exit-provenance review requested in INBOX_claude.md MSG 2026-11-08-3/4.
- ChatGPT source audits: P39_SOURCE_PINNED_AUDIT_CROSSWALK_20261108.md, P39_RECEIPT_SUBSYSTEM_AUDIT_20261108.md, EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md.
- Canonical mapping: P39_EP_CANONICAL_ACCEPTANCE_CROSSWALK_20261108.md.

## Constraints
- No source/test changes until the review gate and owner decisions clear.
- No database/provider/runtime/transport selection.
- Do not change canonical LOOP/CASE/D IDs.
- Preserve separate P37/P39 namespaces.
- Distinguish sequential model tests from real adapter evidence.
- Keep VERIFIED / CLAUDE-REPORTED / INFERRED / UNKNOWN / NOT RUN distinct.

## Steps
1. When Gemini's full report arrives, reconcile finding-by-finding with Claude and immutable source/test pins. Reject unsupported path/line claims and separate overlapping findings.
2. When Claude's exit review arrives, reconcile EP-01..25 and the formatter/projection boundary.
3. Prepare one owner decision table for streaming MVP scope, pre-commit revocation consistency, post-commit/in-flight revocation, EP-18, EP-24, and compact ReceiptHead digest binding.
4. Decide whether P40 model-only implementation can be authorized; do not begin it without explicit gate clearance.
5. Refresh branch HEAD, last five commits and Actions before checkpointing.

## Done when
Both independent reviews are reconciled, owner decisions are explicit, and the next implementation slice is either authorized or clearly blocked with exact reasons.
