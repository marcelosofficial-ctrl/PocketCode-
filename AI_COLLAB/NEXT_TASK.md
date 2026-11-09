# NEXT TASK: PocketCode

## Goal
Complete P39 reconciliation and owner gate. Implementation remains blocked.

## Evidence
- Claude/Gemini P39 reconciliations and matrix: `P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md`, `GEMINI_P39_REVIEW_RECONCILIATION_20261109.md`, `P39_REVIEW_CONSENSUS_MATRIX_20261109.md`, `P39_GATE_CLOSURE_PLAN_20261109.md`.
- OD-01..OD-13 all OPEN; CASE-04 remains INCOMPLETE / timed_out.
- Pages/runtime: `PAGES_AND_EXIT_PROVENANCE_VERIFICATION_20261110.md`. Pages enabled, URL/deployment/headers UNKNOWN; Python subprocess unavailable on mobile/WASI; Worker termination is not child exit.
- Pyodide channel: `PYODIDE_WORKER_CONTROL_CHANNEL_REDTEAM_20261110.md`. Pyodide 314.0.5 FFI exposes worker globals; same-realm guest may spoof default Worker messages. Actual PocketCode topology UNKNOWN.
- Claude strategy assignment remains OPEN. Await owner-supplied Claude material; do not create a competing assignment.

## Steps
1. Ingest any new Claude artifact by exact repo/branch/SHA/blob pins and reconcile evidence only.
2. Maintain one conflict matrix with source pin, severity, model/adapter/owner layer, canonical trace, test ID and evidence status. Preserve LOOP/CASE/D IDs.
3. Obtain OD-01..OD-13 explicitly: streaming; revocation; clock/identity; receipt binding; exit/termination; client-byte evidence.
4. Finish PAGES-01..08 and ORIGIN-01..10: actual URL/custom domain, deployed SHA/environment URL, live headers and sibling-origin inventory. Never infer URL from metadata or absent CNAME.
5. Extend O-5 with Worker runner-vs-child evidence, termination request/ack, output close and PYO-CTRL-01..10 private-channel tests. Current branch inventory confirms the Pages prototype is simulation-only and has no Pyodide worker/bridge; do not call it vulnerable. Inspect the separately installed app only when its implementation is available. Do not freeze a schema or change canonical CASE IDs.
6. Freeze model semantics only after owner decisions; seek explicit authorization for bounded model-only P40.
7. Run targeted P39 and full suite on exact SHA; separately test durable adapter, concurrency, crash/restart/restore and transport.
8. Keep PR #2/#3/#4 untouched. No stack choice, spend, device/PWA implementation or source/test edits before gate clearance.
9. Refresh HEAD, latest five commits and exact-SHA Actions before checkpointing.

## Constraints
- P39/P40 CLOSED; OD-01..OD-13 OPEN.
- Preserve VERIFIED / INFERRED / UNKNOWN / NOT RUN and PASS / FAIL / NOT RUN.
- Historical 266/266 PASS applies only to source/test SHA `744cb4dc7cd4994647c84ac7476d0c78a21f0540`.
- Keep RevDev evidence separate.

## Done when
All supplied reviews are reconciled, conflicts explicit, owner decisions recorded or deferred, and the owner authorizes a bounded slice or remaining blockers are documented.
