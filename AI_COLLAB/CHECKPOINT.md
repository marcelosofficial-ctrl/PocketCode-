# CHECKPOINT — 2026-11-11

**Unit:** Claude provider-cache/context and AI-lane research audit; index budget repair; state/next-task refresh.  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`.  
**Starting HEAD:** `2247851a8bcff798609c27bec78e2dd72b0dd11b`.  
**Claude research commit:** `3b73e2cc8a8371508b80d1e65393375f986b3760`.  
**ChatGPT audit commit:** `1a8efd485d8f762906d26979e8730e78d8267073`.  
**INDEX commit:** `3585703f544ce75b17f51db930894e0ccf37862c`.

## Mandatory resume
- Read in order: BOOT.md, STATE.md, NEXT_TASK.md, CHECKPOINT.md, INBOX_chatgpt.md.
- Latest five commits before this checkpoint update:
  1. `d6f5be1d` docs(checkpoint): pin latest five commit lineage
  2. `9fc34ebd` docs(checkpoint): capture provider audit and index repair
  3. `753fcd70` docs(next-task): rank owner gate and provider audit followups
  4. `2b96c970` docs(state): record Claude research audit and current head
  5. `3585703f` docs(index): restore word budget and index independent audit

## Work completed
- Reconciled Claude's new provider/context and AI-lane research in the active branch. Source commit `3b73e2c` adds `PROVIDER_CACHING_AND_CONTEXT_ENGINEERING_20261110.md`, `RED_TEAM_CORRECTIONS_CLAUDE_20261110.md`, `kit/docs/AI_LANES_AND_DISPATCH.md`, and index rows. Commit `2247851` fixes the Dynamic Type CSS override and qualifies the Safari `linear()` wording.
- Created `CLAUDE_PROVIDER_AND_LANES_INDEPENDENT_AUDIT_20261111.md` (129 added lines). It verifies current Anthropic/OpenAI/Gemini cache semantics, exact usage fields, model/API limits, provider-specific prompt ordering, current schema restrictions, Aider/MCP reuse/license facts, and a normalized cache measurement contract.
- Red-teamed seven issues: OpenAI's model-generation split and cache-key semantics; cache-prefix versus 128-token reporting; Gemini model/API support and minimums; telemetry field guesses; universal prefix ordering; AI-lane role conflict; unsupported dispatch thresholds.
- **VERIFIED:** OpenAI GPT-5.6+ supports implicit/explicit cache breakpoints, 1,024 visible token minimum, 30m/12h TTL; earlier models differ and use implicit breakpoints. Anthropic uses tools → system → messages prefix order, four total breakpoint slots, model-dependent minimums and documented cache usage fields. Gemini explicit caching is Beta on v1beta, supported for Gemini 2.5/3 but not Gemini 4; Interactions API only supports implicit caching.
- **VERIFIED:** Aider repo map is a useful graph-ranked context pattern; Aider is Apache-2.0, latest listed release v0.86.0 published 2025-08-09, repository last push 2026-05-22. MCP repo describes TypeScript-first and JSON Schema outputs, README states MIT; no dependency or code was adopted.
- Updated `AI_COLLAB/INDEX.md`. Previous count was 1,232 whitespace-delimited words, exceeding the stated 1,200 ceiling. New measured count is 520.
- Updated `STATE.md` and `NEXT_TASK.md`. No owner decision, canonical ID, provider, runtime, database, transport or implementation gate changed.

## Highest-value open gaps
1. OD-01..13 owner decisions remain open; they gate policy/contract choices.
2. P40 six-lane model run remains NOT AUTHORIZED / NOT RUN; current full suite is not established.
3. Pyodios Console/Worker/device evidence remains NOT RUN / UNKNOWN.
4. Live Pages response/headers and sibling portfolio script behavior remain UNKNOWN.
5. Claude's further P39/exit-provenance material from owner remains awaited; the new strategy drafts do not close P39.

## Verification and limits
- **VERIFIED:** all changes since prior checkpoint `ba1d3dd` are documentation-only: Claude's research/design drafts plus the audit/index/state/next/checkpoint updates. No `scripts/` or test paths changed.
- **VERIFIED:** branch tip before this checkpoint update was `d6f5be1d1aacaa613cc1281cb34f30d59a5a992a`; index measured 520 words.
- Exact-SHA combined status for pre-checkpoint HEAD `d6f5be1d1aacaa613cc1281cb34f30d59a5a992a` returned no statuses. Workflow-run connector returned no PR-triggered runs; source/test workflow not expected for docs-only changes. CI NOT RUN.
- **NOT RUN:** full Python suite, P40 lanes, provider API/cache calls, device/browser tests, live Pages/header checks and Pyodios Console probe.
- D-005/D-006 no-spend preserved. No API key, provider, runtime, database, transport, dependency or paid service selected. PR #2/#3/#4 untouched. No RevDev work.
- Historical 266/266 PASS remains tied only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.

## Next
1. Resolve or explicitly defer OD-01..OD-13, keeping live streaming distinct from bounded artifact download/share.
2. Ingest additional Claude P39/exit artifact when owner supplies it; pin exact sources.
3. After gate clearance, request authorization for the six-lane P40 model run and exact-SHA full suite.
4. Separately obtain Pyodios and live Pages evidence without changing deployment/settings.
