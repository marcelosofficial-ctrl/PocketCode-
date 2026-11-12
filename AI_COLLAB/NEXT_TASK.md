# NEXT TASK: PocketCode

## Goal

Continue evidence closure and acceptance-contract refinement without reopening the P39 implementation/adapter gate. Prefer source-pinned, non-duplicative work. No source/test implementation or infrastructure selection from design documents alone.

## Verified baseline at start of this planning update

- Branch: `pocketcode-ai-workflow-director-research-2026-10-28`; snapshot HEAD `b06b6e41f7aa07c271aca53ab6459bb4f0823373`.
- Latest five at snapshot: `b06b6e4` state condensation; `3d635c5` INDEX count; `4800374` storage rebinding cases; `774660e` grant cross-model digest gap; `37a3fea` grant canonical digest binding.
- Compare from source-audit pin `b71315068ec33a0175fed46ef96912e954d87f9f`: 63 ahead / 0 behind / 15 changed paths; all paths AI_COLLAB-only. No app source, scripts/tests, workflows or product assets changed.
- HEAD status is pending with zero attached status entries. Latest relevant Actions run #59 / `43126974602` remains SUCCESS only on workflow commit `d93cd11e6873090cdb280fd18e45d9eeee9a973f`, which checked out historical model SHA `319cffef121e327331aeaff59522ae279b112ecc`; 266/266 full scripts suite. Model-only, not current-HEAD CI or adapter/CASE proof.
- INDEX is 608 words; all 87 referenced Markdown basenames exist. The report-projection migration document is present and indexed.

## Completed in the current full pass

1. Reconciled the startup files with current branch evidence and condensed STATE.md to 1,088 words, removing stale snapshots from the live summary while keeping older history in Git.
2. Opaque-origin protocol now carries both canonical ExecutionId and a distinct parent-generated execution_instance_id in INIT and every post-handshake message. CANCEL_ACK is narrowly described as a supervisor Worker.terminate() action acknowledgement, not native child exit or proof of OS/renderer teardown.
3. Grant-event v1 now defines strict absent-versus-null field rules and safe-integer bounds. Overflow must fail closed; no rounding, wrap or reuse.
4. Grant/storage contracts now bind ReceiptHead ID/revision to receipt SHA-256 and artifact ID/object-version/length to artifact SHA-256 plus verified/non-quarantined manifest state. Digest subjects are distinct. A digest does not authenticate a producer.
5. Static source crosswalk found a gap: result_receipts has receipt SHA, artifact hash and quarantine fields, but release_grant_conformance ReceiptHead/reserve do not bind these values. The separate Python fingerprint is not proof of JCS cross-language canonicalization.
6. Grant acceptance plan expanded to 33 local scenarios (A1–A8, B1–B9, C1–C9, D1–D7), including receipt/artifact binding and serialization boundaries. INDEX count updated. No canonical LOOP/CASE/D IDs changed.

Tests in this pass: NOT RUN. All current changes are documentation-only.

## Ranked next passes

1. **OD-to-source traceability:** inspect the grant reservation, worker claim, progress, authorization and transfer model against OD-02..OD-08. Map each policy to exact current code/test coverage and identify only the missing model cases. Static inspection only; do not implement.
2. **Canonical acceptance mapping:** map the 33 grant-event cases and format-2 report cases to existing LOOP/CASE obligations without changing canonical IDs or claiming CASE closure. Reuse existing crosswalks; do not create duplicate history.
3. **Receipt/lifecycle integration review:** reconcile ResultReceipt revision/head CAS, artifact manifest integrity/quarantine, termination/cleanup evidence and publication/client acknowledgement. Keep execution verdict, job disposition and artifact disposition separate.
4. **Browser acceptance readiness:** check opaque-origin protocol, storage recovery and device runbook for exact scope/version/identity alignment. Device tests require an approved synthetic-data build and available target devices; no desktop inference.
5. **Owner/device evidence:** the Pyodios Console probe remains optional and may be deferred. Preserve the existing matching summary.json; never rerun the successful artifact-producing attempt. No need to request it again unless the owner volunteers output.
6. **O-7 naming:** direct official clearance only if a product naming decision is required. No rename or PoCo publication beforehand.

## Constraints and stop conditions

- D-005/D-006 remain $0. No paid provider, hosting, Apple account, TestFlight, App Store or deployment.
- P39 implementation/adapter gate CLOSED. No source/test edits, adapter, database, broker, key store, runtime, provider, host, storage selection, DNS/settings or PR changes without separate authorization.
- Preserve LOOP-01..14, CASE-01..16, D-IDs and OD-01..OD-13. CASE-04 remains INCOMPLETE / timed_out.
- Keep PocketCode and RevDev wholly separate. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
- Use INDEX.md to locate material; no file over 1,500 words opened whole. Re-fetch branch and SHAs after every write. Update CHECKPOINT.md after each unit and commit before summarizing.
- Evidence labels VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests PASS / FAIL / NOT RUN. Never claim tests passed without output.
