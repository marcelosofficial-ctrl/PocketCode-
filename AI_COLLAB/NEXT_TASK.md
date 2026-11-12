# NEXT TASK: PocketCode

## Goal

Continue evidence closure and contract refinement while the P39 implementation/adapter gate stays CLOSED. Prefer source-pinned, non-duplicative work. Do not implement or select infrastructure from these specifications alone.

## Verified baseline at start of this update

- Active branch: `pocketcode-ai-workflow-director-research-2026-10-28`; snapshot HEAD `56910c4cb45df5805b0986eec620f0e1160de24e`.
- Latest five: `56910c4` INDEX crosswalk row; `99f16b3` OD-02..OD-08 source coverage audit; `73b0a24` next-pass plan; `b06b6e4` condensed STATE; `3d635c5` grant-plan count.
- Compare from source-audit pin `b71315068ec33a0175fed46ef96912e954d87f9f`: 68 ahead / 0 behind / 16 changed paths, every path under `AI_COLLAB/`. No application source, scripts/tests, workflow or product assets changed.
- HEAD combined status: pending, zero attached status entries. Latest relevant CI remains run #59 / `43126974602`, SUCCESS on historical target `319cffef121e327331aeaff59522ae279b112ecc`, full scripts 266/266. Not current-HEAD CI or adapter/CASE proof.
- INDEX 622 words; all 88 referenced Markdown basenames exist.

## Completed in this pass

1. Bound canonical ExecutionId separately from parent-generated execution_instance_id across opaque-origin INIT and post-handshake messages. Narrowed browser CANCEL_ACK to a Worker.terminate() action acknowledgement, not native child exit or proof of renderer/OS teardown.
2. Defined grant-event v1 exact absent-vs-null field rules and safe-integer ceilings. Overflow fails closed; no rounding, wrapping or reuse.
3. Aligned grant/storage contracts with OD-08: ReceiptHead binds receipt ID/revision to receipt SHA-256; artifact ID/object-version/length bind to artifact SHA-256 and a verified, non-quarantined manifest. Digest subjects remain distinct.
4. Expanded grant event model plan to 33 scenarios (A1–A8, B1–B9, C1–C9, D1–D7), including receipt/artifact binding, canonicalization and numeric boundaries. Added static source coverage.
5. Added `P39_OD02_OD08_MODEL_COVERAGE_CROSSWALK_20261112.md`: exact source pins and policy-to-method/test coverage for claim authorization, revocation, recovery, policy epoch, clock authority, restore high-water and receipt/artifact content.
6. Condensed STATE.md to 1,088 words. Restored the missing report-projection migration plan in the preceding pass.

Tests in these documentation passes: NOT RUN. No code or canonical acceptance changes.

## Ranked next passes

1. **Canonical acceptance mapping:** trace the 33 grant-event scenarios and 14 report-v2 cases to existing canonical LOOP/CASE obligations. Reuse existing crosswalks; preserve all IDs and meanings. Identify unowned cases without declaring canonical acceptance closed.
2. **Receipt/lifecycle integration:** map OD-09..OD-13 to ResultReceipt, execution_projection, artifact release and publication/client acknowledgement. Verify the split between execution verdict, overall job disposition and artifact disposition.
3. **Browser acceptance readiness:** reconcile opaque-origin protocol, storage recovery, same-origin Pages boundary and device runbook. Device tests require an approved synthetic-data build and exact target-device evidence; no desktop inference.
4. **Evidence closure:** when authorized source/test scope exists, pin the exact code/test SHA, run deterministic model cases, retain per-case outputs and full-suite results. Keep durable adapter and CASE acceptance separate.
5. **Owner/device evidence:** Pyodios Console probe is optional and may be deferred. Preserve the existing matching summary.json; never rerun the successful artifact-producing attempt.
6. **O-7 naming:** official candidate clearance only if a naming decision is needed. No rename or PoCo publication beforehand.

## Constraints

- D-005/D-006 remain $0. No paid provider, hosting, Apple account, TestFlight, App Store or deployment.
- P39 implementation/adapter gate CLOSED. No source/test edits, adapter, database, broker, key store, runtime/provider/host/storage selection, DNS/settings or PR changes without separate authorization.
- Preserve LOOP-01..14, CASE-01..16, D-IDs and OD-01..OD-13. CASE-04 remains INCOMPLETE / timed_out.
- Keep PocketCode and RevDev wholly separate. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
- Use INDEX.md to locate material; no file over 1,500 words opened whole. Re-fetch branch and SHAs after every write. Update CHECKPOINT.md after each unit and commit before summarizing.
- Evidence: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests: PASS / FAIL / NOT RUN. Never claim tests passed without output.
