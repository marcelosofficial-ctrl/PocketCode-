# NEXT TASK: PocketCode

## Goal
Continue evidence closure without reopening the P39 implementation/adapter gate. No source/test work is authorized by the existing design or P40 evidence.

## Verified start snapshot (2026-11-13)
- HEAD at this continuation's start: `9de34daec63546f45f79a88f8f50f5ee9756884a`.
- Latest five: `9de34da`, `dcf76c8`, `676cc03`, `a9fba95`, `b828418`.
- Compare from `b71315068ec33a0175fed46ef96912e954d87f9f`: 88 ahead / 0 behind / 20 AI_COLLAB paths; no app source, tests, workflow or product assets changed.
- Exact-HEAD status has zero attached statuses and PR-triggered workflow lookup returned zero runs. Current-HEAD CI: NOT RUN.
- Historical run #59 succeeded on pinned model target `319cffef121e327331aeaff59522ae279b112ecc`, 266/266 scripts. Not current-HEAD CI, adapter proof or CASE acceptance.

## Completed this pass
- Re-read required startup records and latest five commits.
- Added `RESEARCH_DELTA_AND_RED_TEAM_20261113.md`, indexed. It ranks five open risk areas, researches current primary sources, records reuse/licence boundaries, gives acceptance tests and corrects four weak claims.
- Corrected the stale snapshot baseline. The previous commit was internally aligned to its parent, not the live branch; a coherent parent snapshot is not current HEAD.
- No code/tests/workflow changed. Tests/device checks NOT RUN.

## Ranked next work
1. Untrusted execution isolation: prove opaque-origin boundary, default-deny egress and bounded I/O on target devices.
2. Grant atomicity and relay fencing: atomic aggregate/outbox, per-aggregate order, current-generation fence and stale-ack rejection.
3. Event trust: authenticate producer/scope, recompute canonical payload digest and atomically persist inbox plus state.
4. Lifecycle/receipt: separate child verdict, evidence and artifact state; prove same-attempt termination and exact client receipt.
5. Browser durability/origin: resolve shared github.io trust boundary and prove export/recovery under eviction/restart.

## Gate and constraints
- P39 implementation/adapter gate CLOSED. Obtain separate explicit authorization naming exact model-only source/test scope before scripts/tests, adapters or CI.
- D-005/D-006 $0. No provider, runtime, database, transport, storage engine or host selected. No deployment, DNS, PR #2/#3/#4 changes or external AI request.
- Preserve LOOP-01..14, CASE-01..16, D-IDs, OD-01..13. CASE-04 stays INCOMPLETE / timed_out.
- Preserve successful Pyodios `summary.json`; do not rerun artifact-producing work. Device acceptance needs exact-device evidence and approved synthetic data.
- On resume, read BOOT, STATE, NEXT_TASK, CHECKPOINT, INBOX_chatgpt, then fetch live branch HEAD and latest five commits. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
