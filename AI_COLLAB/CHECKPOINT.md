# CHECKPOINT — 2026-11-12

Completed units 1–2: grant-event envelope/relay contract and opaque-origin browser execution protocol.
Branch: pocketcode-ai-workflow-director-research-2026-10-28
Unit 1 commit: 0db55f439ff7429e12ab6d0327aa74b95d18d98c
Unit 2 parent: 0db55f439ff7429e12ab6d0327aa74b95d18d98c
Unit 2 new document: AI_COLLAB/OPAQUE_ORIGIN_EXECUTION_PROTOCOL_20261112.md
Scope: documentation/spec only. No application/test edits, device tests, implementation gate changes or infrastructure selection.

Unit 1 verified model defects:
- Equal progress increments aggregate_version without event/outbox.
- Consumer trusts a supplied first-delivery digest and does not validate full tenant/grant/effect/attempt/producer scope.
- Grant-event delivery marker has no lease/fence/stale-ack protection.
Deliverable defines grant-event-envelope/v1, canonical bytes/digest, authenticated ingress, atomic aggregate+outbox parity, separate transition and relay fences, ordered at-least-once publication, durable consumer inbox and 18 acceptance cases.

Unit 2 deliverable defines opaque-origin-execution/v1:
- sandboxed iframe allow-scripts only; no allow-same-origin.
- exact WindowProxy source binding, opaque origin null nuance, one-time nonce and narrowly scoped wildcard bootstrap to exact child only.
- MessageChannel held only by trusted supervisor; task Worker receives no parent port or credentials.
- default-deny CSP, bounded explicit file copies, parent-side digest verification, no MVP streaming.
- distinct task-reported result, controller teardown acknowledgement, child exit evidence and job/artifact disposition.
- missing same-attempt acknowledgement remains UNKNOWN/INCOMPLETE; browser hard memory quota remains UNKNOWN.
Research sources opened include WHATWG HTML, MDN postMessage/CSP/Worker.terminate, W3C Permissions Policy, Pyodide docs, OWASP and Open WebUI advisory. No code/dependencies copied.

Housekeeping: INDEX includes name collision, provider cache/context and Claude red-team docs; AI_LANES_AND_DISPATCH remains indexed once. P39/P40 grouped and INDEX budget reduced. Do not rename PocketCode or publish PoCo pending name clearance; exact trademark specifics not verified.

P40 remains PASS: Actions run #59 / 43126974602, exact target 319cffef121e327331aeaff59522ae279b112ecc, full scripts 266/266; lane 4 BLOCKED. Model-only, not adapter/CASE acceptance. Docs-only commits do not trigger current CI path filters.
Next unit: browser artifact storage/recovery contract (IndexedDB transaction and durability hints, Safari storage eviction, export/recovery), then update STATE/NEXT_TASK/INBOX and final checkpoint. Tests NOT RUN in units 1–2. CASE-04 remains INCOMPLETE / timed_out.
