# CHECKPOINT — 2026-11-12

Completed units 1–3: grant-event envelope/relay, opaque-origin execution, browser artifact storage/recovery.
Branch: pocketcode-ai-workflow-director-research-2026-10-28
Unit 1 commit: 0db55f439ff7429e12ab6d0327aa74b95d18d98c
Unit 2 commit: e8c46a73ced696ebcbb0bcefe11e204f7057ccbe
Unit 3 parent: e8c46a73ced696ebcbb0bcefe11e204f7057ccbe
Unit 3 new document: AI_COLLAB/BROWSER_ARTIFACT_STORAGE_RECOVERY_CONTRACT_20261112.md
Scope remains documentation/spec only: no application/test edits, device tests, implementation gate changes or infrastructure selection.

Unit 1 (grant-event-envelope/v1): event/version parity; no-op does not advance version; canonical bytes and recomputed digest; independent producer authentication; separate business transition and relay fences; ordered at-least-once publisher; durable consumer inbox; stale-ack and restore-roll-back acceptance cases.

Unit 2 (opaque-origin-execution/v1): allow-scripts-only opaque iframe; source-bound handshake; null-origin nuance and narrowly scoped wildcard bootstrap; MessageChannel retained by supervisor; untrusted worker has no parent port/credentials; CSP network deny; explicit bounded file copies; truthful cancellation and resource limits.

Unit 3 (browser-artifact-recovery/v1): separates produced, locally stored, read-back verified, manifest committed, exported, transport emitted, client observed and client acknowledged. Defines origin trust/no-secrets, immutable staged writes, read-back digest, manifest commit, recovery/reopen, quota/persist signals, Safari inactive-origin eviction and explicit export. IndexedDB, OPFS, SQLite-WASM and Cache API remain unselected. Acceptance matrix includes crash points, quota, eviction, same-origin sibling, multi-tab CAS and import/export.

Research sources opened 2026-11-12: AWS, Debezium, CloudEvents, NATS, RFC 8785/9421, WHATWG, MDN messaging/CSP/storage/durability/Worker, W3C Permissions Policy, Pyodide, WebKit, SQLite and OWASP. Licences checked where relevant; no source code or dependencies copied.

Housekeeping: INDEX now indexes name collision/provider context/Claude red-team files and all three new contracts; AI_LANES_AND_DISPATCH remains indexed once. P39 and P40 rows compacted. Name collision remains open: no rename or PoCo publication before clearance; specific trademark evidence remains UNKNOWN.

P40 remains PASS: Actions run #59 / 43126974602, exact target 319cffef121e327331aeaff59522ae279b112ecc, full scripts 266/266; lane 4 BLOCKED. Model-only. Docs-only commits do not trigger CI path filters.
Next: update STATE.md, NEXT_TASK.md, INDEX/INBOX status, final CHECKPOINT, then verify branch commits and relevant CI. Tests NOT RUN in units 1–3. CASE-04 remains INCOMPLETE / timed_out.
