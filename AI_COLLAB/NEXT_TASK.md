# NEXT TASK: PocketCode   (one task; under 350 words)

## Goal
Continue the P39 independent audit without Claude availability. Focus on the policy-revocation and transport stream/cancellation boundary, then reconcile Claude's complete review when supplied. No source-code changes until the P39 review gate clears.

## Files to read
- `AI_COLLAB/P39_RESEARCH_REVIEW_DISPOSITIONS_20261108.md` (relevant sections only)
- `AI_COLLAB/P39_CHATGPT_STATIC_AUDIT_ADDENDUM_20261107.md` (relevant sections only)
- `scripts/release_grant_conformance.py` and its tests only where needed for a specific claim
- `AI_COLLAB/RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md` (relevant sections only)

## Constraints
- Mode: normal. About 350 lines per turn. Commit continuity work before summarizing.
- Keep the P39 source-edit freeze. No adapter/provider/database/runtime selection.
- No PR #2/#3/#4 changes. Do not change canonical LOOP, CASE or D IDs.
- Preserve VERIFIED / INFERRED / UNKNOWN and model-vs-adapter evidence boundaries.
- Do not claim tests passed unless an exact-SHA run provides output.

## Steps
1. Audit policy revocation and transport-level cancellation/revocation as separate enforcement boundaries.
2. Identify missing adversarial schedules and the exact adapter evidence required.
3. Update the P39 disposition note only with source-pinned findings.
4. When Claude's complete review arrives, reconcile finding by finding before any implementation.

## Done when
The remaining audit slice is source-pinned, checkpointed, and explicit about unresolved reviewer/adapter obligations.
