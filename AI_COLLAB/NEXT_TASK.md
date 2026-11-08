# NEXT TASK: PocketCode   (one task; under 350 words)

## Goal
Cross-check the P39 findings and proposed P39-POLICY/P39-STREAM tests against the immutable source and contract pins. Then prepare one reviewer reconciliation table for Claude and Gemini when their complete reports are available. No source-code changes until the P39 review gate clears.

## Files to read
- `P39_RESEARCH_REVIEW_DISPOSITIONS_20261108.md` (relevant sections only)
- `P39_CHATGPT_STATIC_AUDIT_ADDENDUM_20261107.md` (relevant sections only)
- `scripts/release_grant_conformance.py` and its tests only where needed for a specific claim
- `RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md` (relevant sections only)

## Constraints
- Mode: normal. About 350 lines per turn. Commit continuity work before summarizing.
- Keep the P39 source-edit freeze. No adapter/provider/database/runtime selection.
- No PR #2/#3/#4 changes. Do not change canonical LOOP, CASE or D IDs.
- Preserve VERIFIED / INFERRED / UNKNOWN and model-vs-adapter evidence boundaries.
- Do not claim tests passed unless an exact-SHA run provides output.

## Steps
1. Cross-check each P39 finding against its pinned source and contract references.
2. Ensure the new P39-POLICY/P39-STREAM tests do not duplicate or conflict with P37 IDs.
3. Prepare a finding-by-finding reconciliation structure for complete Claude and Gemini reviews.
4. Do not implement until independent review dispositions and owner decisions clear the gate.

## Done when
The remaining audit slice is source-pinned, checkpointed, and explicit about unresolved reviewer/adapter obligations.
