# CHECKPOINT — 2026-11-12

Unit: full-power research, P40 workflow runner and exact-SHA test execution.
Branch: `pocketcode-ai-workflow-director-research-2026-10-28`.
Workflow commit: `d93cd11e6873090cdb280fd18e45d9eeee9a973f`.
P40 checkout target: `319cffef121e327331aeaff59522ae279b112ecc`.

Required startup reread completed in order: BOOT, STATE, NEXT_TASK, CHECKPOINT, INBOX_chatgpt. Startup latest five at beginning of pass:
1. `6b28b5afd59e404b8d2bda9d7cf4a99001a6cd34`
2. `ce9238d47ec0bc537bfaebfbd5176e4b6d9a02c9`
3. `35cb8881f66f519d365858520cc3e8c4b12a61bb`
4. `0c2096c1e82cc5f7b4d51918889b86a8a4fa387f`
5. `c937efbd9a15b8693357d9e60944ab40c6a22b30`

Research:
- Ranked five gaps: untrusted execution isolation, grant-event/outbox consistency, browser origin/storage durability, typed lifecycle/receipt evidence, exact-SHA P40 execution.
- Opened AWS transactional outbox, Debezium Outbox Event Router, CloudEvents v1.0.2, NATS JetStream acknowledgements, OWASP HTML5 Security, MDN storage quotas/eviction, SQLite WASM persistence, Pyodide docs and Open WebUI CVE-2026-59214 advisory.
- Wrote `AI_COLLAB/FULL_POWER_GAP_RESEARCH_20261112.md` (2,800+ words) with concrete design contracts, competitor patterns, licence/reuse review, acceptance matrix and six red-team corrections.

P40 run:
- Workflow-only update committed at `d93cd11e6873090cdb280fd18e45d9eeee9a973f`; exact target checkout pinned.
- Actions run #59: `43126974602`; job `130881431566`; conclusion SUCCESS.
- Log confirms checkout `319cffef121e327331aeaff59522ae279b112ecc`.
- Environment: Ubuntu 26.04.1, Python 3.12.16, SQLite 3.46.1, Linux 7.0.0-1019-azure x86_64.
- Lane totals: release-grant+consumer 26/26; FakeOutbox 22/22; EventJournal 27/27; receipts 59/59; execution projection 31/31. Full scripts suite 266/266. No failed tests.
- Lane 4 BLOCKED / NOT TESTABLE. Known model gaps remain: no-op aggregate/event parity, first-delivery producer/envelope auth, grant-event relay fencing. Model PASS does not equal adapter or CASE acceptance.
- Node 20 deprecation warning surfaced for actions/checkout@v4 and setup-python@v5; no test failures.
- CASE-04 remains INCOMPLETE / timed_out.

No application/test source changes, no provider/device tests, deployment, PR changes, spending or stack selections. P40 report, authorization record, STATE, NEXT_TASK and research addendum updated in this commit.

Next unit: write versioned grant-event envelope/relay state-machine contract, then opaque-origin sandbox protocol. Owner-run Pyodios Console probe and read-only Pages evidence remain open.


## Final repository refresh — 2026-11-12
- Latest five commits after recording run evidence:
  1. `cd1be18b4fb523060d231db7980503c119cc34eb` docs(p40): record exact-SHA model run results and next gaps
  2. `d93cd11e6873090cdb280fd18e45d9eeee9a973f` ci(p40): run pinned model lanes and record runtime versions
  3. `d6ff1276664edb9127867dd3974a4dc901ef08cb` docs(research): rank and red-team PocketCode execution gaps
  4. `6b28b5afd59e404b8d2bda9d7cf4a99001a6cd34` docs(p40): clarify exact-SHA runner path and dispatch blocker
  5. `ce9238d47ec0bc537bfaebfbd5176e4b6d9a02c9` docs(p40): record approved run blocked by unavailable runner
- Latest docs-only commit has no check runs because the workflow is path-filtered to scripts/workflow changes. Latest relevant CI is run #59 on workflow commit `d93cd11e`, SUCCESS.
- Compare target `319cffef121e327331aeaff59522ae279b112ecc` to current branch: 11 ahead, 0 behind. Changed paths are the workflow and AI_COLLAB documentation only; no application or test source.
