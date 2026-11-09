# CHECKPOINT — 2026-11-09

Unit complete; pre-checkpoint HEAD: `124ab64bdc8ddac9ff0942928ef2a63c981c9086`.

**Work completed:** Deep primary-source review of PocketCode's $0 GitHub Pages/PWA local-data boundary. Added `AI_COLLAB/GITHUB_PAGES_ORIGIN_ISOLATION_AND_LOCAL_DATA_SECURITY_20261109.md` and indexed it. The key new finding is conditional but high priority: GitHub Pages project sites under the same `<owner>.github.io` host are same-origin despite different repository paths. Same-origin sibling scripts may access IndexedDB/OPFS storage. The actual deployment URL and sibling inventory are UNKNOWN, so this is a threat-model finding, not a confirmed live exploit.

**Contract updates:** `STATE.md` records the finding and expands O-4. `NEXT_TASK.md` adds an origin verification gate and ORIGIN-01..10 acceptance cases. State is 887 words; NEXT_TASK is 306 words. Both within their limits.

**Research conclusions:** IndexedDB strict durability remains a user-agent hint, not a backup/power-loss guarantee. OPFS flush persists file writes but does not make an atomic transaction with IndexedDB. Keep unique immutable per-attempt staging paths and publish only through a current-fence metadata transaction. SQLite WAL/FULL durability and the fixed WAL-reset bug remain evaluation guardrails only; no database selected.

**Gate and scope:** P39/P40 CLOSED; OD-01..OD-13 OPEN. Claude strategy assignment remains OPEN; await owner-supplied additional Claude material. No source/tests, runtime, provider, database, transport, hosting setting, canonical IDs or PRs changed. No tests or device checks run.

**Evidence:** Primary sources and verification limits are in the new research document. Historical 266/266 PASS remains tied only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`. No fresh CI on documentation commits; current HEAD status must be refreshed after this checkpoint.

**Next:** Verify the actual GitHub Pages URL/site type and same-origin sibling content before any local persistence implementation. Keep owner decisions and additional Claude review as separate gates.
