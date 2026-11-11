# NEXT TASK: PocketCode

## Goal
Resolve the owner-controlled P39 decisions and prepare a properly scoped P40 model-only run. Implementation remains blocked.

## Current evidence
- **VERIFIED:** Claude's provider caching/context and AI-lane drafts are in the active branch. Their exact commits are recorded in STATE. The CSS Dynamic Type correction is present.
- **VERIFIED:** independent audit `CLAUDE_PROVIDER_AND_LANES_INDEPENDENT_AUDIT_20261111.md` opens current Anthropic, OpenAI, Gemini, Aider and MCP sources; corrects outdated provider caching claims; defines an instrumentation contract; and red-teams the role/dispatch proposal.
- **VERIFIED:** INDEX now measures 520 whitespace-delimited words, below its 1,200-word ceiling.
- OD-01..OD-13 remain OPEN. CASE-04 remains INCOMPLETE / timed_out. P39/P40 implementation gate CLOSED.
- P40 six-lane protocol is prepared but NOT AUTHORIZED / NOT RUN. Historical 266/266 applies only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.
- OD-01 is live/incremental streaming only; it does not automatically exclude bounded staged download/share. If bounded release stays in MVP, OD-02..05 still require revocation and recovery semantics.
- Pages last located successful deployment remains run 39433670146, main SHA `90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c`. Public `portfolio` Pages shares the PocketCode origin. Current live response/headers and generated portfolio script remain UNKNOWN.
- Pyodios iPhone error cause and Worker topology remain UNKNOWN; Console probe NOT RUN.

## Ranked next actions
1. **Owner gate:** resolve OD-01..OD-13 or explicitly defer them. Resolve OD-01 with a precise distinction between live streaming and bounded artifact release. Then decide the OD-02..05 lifecycle as one unit.
2. **Claude P39/exit material:** ingest any additional artifact the owner supplies, pin exact repo/branch/SHA/blob hashes, and reconcile evidence. The provider/design drafts audited this pass are not P39 gate evidence.
3. **After gate clearance only:** obtain explicit authorization for the six-lane P40 model run in `P40_MODEL_ONLY_EXECUTION_PROTOCOL_20261110.md`. Pin source/test SHA and environment; keep model tests separate from canonical CASE acceptance.
4. **Current code confidence:** run the full Python suite in real checkout/CI on exact SHA after authorization; historical 266/266 is not current.
5. **Device and origin evidence:** owner runs the read-only Pyodios Console probe; separately verify live Pages deployment/headers/service-worker scope and portfolio generated script. No deployment, settings or domain changes.

## Hard constraints
- D-005/D-006: $0. No API keys, provider calls, paid caching tests, paid hosting, Apple Developer Program, TestFlight or App Store.
- No provider/runtime/database/transport selection, source/test edits, schema freeze, device tests, Pages deployment/settings/DNS changes, PR #2/#3/#4 changes or RevDev work before applicable explicit owner authorization.
- Preserve LOOP-01..14, CASE-01..16, D-IDs and all existing canonical IDs.
- Evidence labels: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Test outcomes: PASS / FAIL / NOT RUN.
- Python CI path filter covers `scripts/**` and its workflow, plus manual dispatch; docs-only commits do not trigger the source/test workflow.
- Keep PocketCode and RevDev completely separate.

## Done when
Owner decisions are explicit or deferred; Claude reviews are reconciled; model/adapter/product acceptance boundaries are clear; and a bounded implementation or test slice is explicitly authorized.


## 2026-11-11 execution note
- Current active HEAD at last refresh: `cac5abc0fc10eeebca971c670c2b7f9f91a23408`; latest five are docs-only. No source/test drift.
- A read-only browser open of the two known Pages URLs was unavailable. Do not infer live state from this tool failure. The remaining Pages work requires a reliable browser/network probe or owner-provided response/header evidence; no deployment/settings change is authorized.
- With OD-01..OD-13 still OPEN and no owner authorization, no meaningful P40 test execution or source change is permitted. Continue only non-invasive evidence reconciliation; do not manufacture additional documentation to simulate progress.
