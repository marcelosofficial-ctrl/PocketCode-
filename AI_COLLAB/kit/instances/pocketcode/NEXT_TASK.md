# NEXT TASK: Continue P39 source-pinned adversarial audit

## Goal
Continue independent ChatGPT review of the release-grant model and contracts while Claude is unavailable. Keep the source-edit freeze in force. The final P39 reconciliation gate still requires the complete independent Gemini report and completion of Claude's assigned review scope; do not wait idle if source-backed audit work remains.

## Current evidence
- Source/test pin: `744cb4dc7cd4994647c84ac7476d0c78a21f0540`
- Documentation snapshot: `04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0`
- Latest branch HEAD before this continuity update: `2c8dee79e2e0ef6988f2134f327fb8a046fcec59`
- Claude partial review: `AI_COLLAB/CLAUDE_REVIEW_RELEASE_GRANT_RESEARCH_20261108.md` (research packet only).
- Interim dispositions: `AI_COLLAB/P39_RESEARCH_REVIEW_DISPOSITIONS_20261108.md`.
- ChatGPT static audit: `AI_COLLAB/P39_CHATGPT_STATIC_AUDIT_ADDENDUM_20261107.md`.

## Next ChatGPT audit slice
1. Verify tenant/principal/request-key binding and cross-tenant lookup isolation.
2. Verify first receipt-head bootstrap and successor race assumptions against the model, tests and P37 contract.
3. Verify authorization replay, policy revocation and the distinction between returning a grant and authorizing bytes.
4. Inspect event-to-tenant binding, producer trust and journal fence atomicity.
5. Record only new source-backed findings, with exact pins, counterexample schedules and model-vs-adapter boundaries.

## Reviewer inputs
- Claude has reviewed only `RELEASE_GRANT_ADAPTER_RESEARCH_AND_REDTAM_20261107.md`. Remaining Claude scope: source model/tests, P37 concurrency contract and P39 static audit addendum.
- Gemini's owner-supplied chat response is a research/implementation plan, not a complete source-pinned review. The independent review request remains open; do not infer its completion.
- Owner-mediated review only. Do not assume direct AI-to-AI communication.

## Constraints
No source-code edits before full review reconciliation. No PR #2/#3/#4 changes, merges, deployment, provider calls, paid services, runtime/database selection or canonical LOOP/CASE/D ID changes. Preserve $0 default and PocketCode/RevDev separation. No tests are claimed unless output exists.

## Done when
The ChatGPT source audit is complete and source-pinned; Gemini's complete independent report is reconciled when available; Claude's remaining review scope is reconciled when available; all material findings have explicit dispositions; and one bounded implementation task is recorded. Until the independent reviews are complete, P39 remains OPEN / BLOCKED.
