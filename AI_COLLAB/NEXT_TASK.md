# NEXT TASK: PocketCode

## Goal

Continue evidence closure without reopening the P39 implementation/adapter gate. Design, source audit and model acceptance documents are prepared; no source/test work is authorized by them.

## Verified baseline at start of this update

- Branch: `pocketcode-ai-workflow-director-research-2026-10-28`; live snapshot before this update `22a2cf8ba2df5543ad0ca241d62228b185d1a4d6`.
- Latest five at snapshot: `22a2cf8` live STATE refresh; `af4a0f8` termination-evidence checkpoint; `a1a55c4` Worker-action vs termination-proof clarification; `d9d61c2` full policy/traceability checkpoint; `56789cb` owner-gated next-task plan.
- Source-audit compare pin `b71315068ec33a0175fed46ef96912e954d87f9f`: 80 ahead / 0 behind / 19 changed paths, all AI_COLLAB. No application source, scripts/tests, workflow or product assets changed.
- HEAD combined status at snapshot: pending with zero status entries. This is not a CI pass.
- Latest Actions run #59 / `43126974602` is SUCCESS only on historical model target `319cffef121e327331aeaff59522ae279b112ecc`, full scripts 266/266. Not current-HEAD CI or adapter/CASE proof.
- INDEX 655 words. All referenced Markdown basenames exist.

## Completed in the current full work pass

1. Restored missing `REPORT_PROJECTION_V2_MIGRATION_AND_ACCEPTANCE_20261112.md`; preserves format 1 and specifies a gated format-2/three-projection migration and 14 future regression cases.
2. Opaque-origin contract now binds canonical ExecutionId separately from parent-generated execution_instance_id through INIT and all channel messages. CANCEL_ACK is limited to supervisor invocation of terminate() on its exact Worker and channel closure, not native child exit or proof of OS/renderer teardown.
3. Grant envelope/storage contracts now define absent-vs-null fields, safe-integer ceilings, distinct event/receipt/artifact digests, canonical receipt binding and verified/non-quarantined artifact manifest requirements.
4. Grant plan now has 33 scenarios A1–A8, B1–B9, C1–C9, D1–D7 and a static source coverage table. It records missing event parity, canonical first-delivery digest/scope, relay fencing and inbox/restore proof.
5. Added `P39_OD02_OD08_MODEL_COVERAGE_CROSSWALK_20261112.md` with exact source pins and mapping for claim-time authorization, active revocation, recovery capability, policy epoch, time authority, restore high-water and receipt/artifact binding.
6. Added `P39_SUPPLEMENTAL_MODEL_CANONICAL_TRACEABILITY_20261112.md` mapping grant/report local scenarios to canonical LOOP/CASE obligations as supporting coverage only. Canonical IDs/meanings unchanged.
7. Added `P39_OD09_OD13_MODEL_COVERAGE_CROSSWALK_20261112.md` with exact pins and gaps for policy/egress barriers, separate projections, ExecutionId/identity reducer, termination acknowledgement and client-confirmed artifact receipt.
8. Updated device runbook to test both canonical ExecutionId and execution_instance_id and record the narrower Worker termination acknowledgement.
9. Condensed STATE.md and aligned INDEX.md. No application source/tests were changed.

Tests in this documentation pass: NOT RUN.

## Completed in the 2026-11-13 follow-up

- Reconciled OD-12 with the browser Worker protocol. `worker_termination_action_acknowledged` proves only the supervisor invoked `terminate()` on its exact Worker and closed the channel. It is not automatically the broader same-attempt `termination_acknowledged` required for cleanup/release. Lifecycle contract now preserves the distinction.
- Cross-checked OD-01..OD-13 against owner decisions, grant event, browser storage, opaque-origin and lifecycle contracts. No additional contradiction requiring a policy change was found. OD-03's missing transport cancellation/ack model and OD-02/04/05/06/07/08 model gaps remain explicitly open in the existing crosswalk.
- No source/test files changed; tests NOT RUN.

## Ranked next work

1. **Implementation/test gate:** wait for separate explicit owner authorization identifying exact model-only source/test scope. Until then do not touch scripts/tests or run CI.
2. **Device evidence:** owner may optionally perform the read-only Pyodios Console inspection in `PHONE_DEVICE_VALIDATION_RUNBOOK_20261112.md`. Preserve existing summary.json; do not rerun main.py or the artifact-producing attempt. If Console controls are unclear, stop.
3. **Browser/device acceptance:** only with an approved synthetic-data build and exact target-device evidence. No desktop/browser inference.
4. **Shared-origin boundary:** no sensitive persistence on github.io until origin separation or an owner-accepted threat model. No host/DNS changes or deployment.
5. **O-7 naming:** direct official clearance only if a naming decision is needed. No rename or PoCo publication before clearance.
6. **Fresh-chat continuity:** test the five-file resume protocol in a genuinely fresh chat when practical; never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
7. **Static review:** stop repeating completed crosswalk work unless a new concrete contradiction or source change appears.

## Constraints and stop conditions

- D-005/D-006 remain $0. No paid provider, hosting, Apple account, TestFlight, App Store or deployment.
- P39 implementation/adapter gate CLOSED. No source/test edits, adapters, DB/broker/key store, runtime/provider/host/storage selection, DNS/settings or PR changes without separate authorization.
- Preserve LOOP-01..14, CASE-01..16, all D-IDs and OD-01..OD-13. CASE-04 remains INCOMPLETE / timed_out.
- PocketCode and RevDev remain separate.
- Use INDEX.md to locate material. Never open files over 1,500 words whole; never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
- Re-fetch branch and SHAs after writes; overwrite CHECKPOINT after each unit; commit before summarizing.
- Evidence labels VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests PASS / FAIL / NOT RUN. Do not infer successful tests from status or documentation.
