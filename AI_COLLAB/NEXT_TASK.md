# NEXT TASK: PocketCode

## Goal
Continue evidence closure without reopening the P39 implementation/adapter gate. No source/test work is authorized by the existing design or P40 evidence.

## Verified start snapshot (2026-11-14)
- Live branch HEAD at last resume: `943a4034a774b2f5efd49e42d6efd811447fa858`. Latest five: `943a403`, `95280a4`, `0b1a435`, `f020658`, `9de34da`. Always fetch live ref and latest five before work.
- The tail since source-audited baseline `f020658` is documentation-only; no application source, tests, workflow or product assets changed.
- Exact-HEAD checks for `943a403`: zero attached statuses and zero PR-triggered workflow runs. Tests NOT RUN.
- Historical run #59 succeeded on pinned model target `319cffef121e327331aeaff59522ae279b112ecc`, 266/266 scripts. Not current-HEAD CI, adapter proof or CASE acceptance.

## Completed this pass
- Re-read BOOT, STATE, NEXT_TASK, CHECKPOINT and INBOX_chatgpt in order, then INDEX and the latest five branch commits.
- Repeated source-to-contract validation on the pinned grant, outbox, journal, coordinator, execution projection and receipt models.
- NEW INFERRED integration gap: journal quarantine conflicts are not carried into FakeCoordinator verdict/report/receipt projections. QuarantinedConflict omits effect/attempt scope; projection methods enumerate accepted events only. The existing test checks rebuilt dispatch state only, not receipt/verdict uncertainty. Exact source pins: `scripts/event_journal.py` `371a175739b9cb65cd4d59bb4cd5b3c1c4953564`; `scripts/fake_coordinator.py` `651921ffe07d27f7d1b7371eb4d36777e39d94ed`; `scripts/test_event_journal.py` `333cf5ec856d4244c3f84da9e82bb2fa126607b5`; `scripts/test_fake_coordinator.py` `b06a4f7af870922003345e3c5f119344302f8c78`.
- Existing docs define changed source/event identity as quarantine, but do not specify how a quarantined collision affects the corresponding attempt receipt. Treat this as an unresolved model/contract integration question, not a proven production exploit.
- No code/tests/workflow changed. Tests/device checks NOT RUN. P39 implementation/adapter gate remains CLOSED.

## Ranked next work
1. After a separate owner authorization, resolve conflict attribution and projection semantics: add effect/attempt/source identity to quarantine evidence or define a conservative quarantine boundary; ensure conflicting source/event IDs are visible in uncertainty/evidence and cannot silently yield an unqualified PASS receipt. Add tests for same-attempt changed payload, cross-attempt collision, producer collision, receipt creation after conflict, and unrelated conflict isolation.
2. Until authorization, perform only non-duplicative static contract review and record concrete evidence; do not edit source/tests or run model suites.
3. Keep the 33-case grant plan and 14-case report-v2 plan ready for a separately authorized model/test scope.
4. Device/browser acceptance requires approved synthetic-data build and exact target-device evidence. Preserve successful Pyodios summary.json; never rerun artifact-producing work.
5. Resolve shared github.io origin trust boundary before sensitive persistence. No host migration/deployment or stack choice without owner decision.

## Gate and constraints
- P39 implementation/adapter gate CLOSED. Obtain separate explicit authorization naming exact model-only source/test scope before scripts/tests, adapters or CI.
- D-005/D-006 $0. No provider, runtime, database, transport, storage engine or host selected. No deployment, DNS, PR #2/#3/#4 changes or external AI request.
- Preserve LOOP-01..14, CASE-01..16, D-IDs, OD-01..13. CASE-04 stays INCOMPLETE / timed_out.
- Preserve successful Pyodios `summary.json`; do not rerun artifact-producing work. Device acceptance needs exact-device evidence and approved synthetic data.
- On resume, read BOOT, STATE, NEXT_TASK, CHECKPOINT, INBOX_chatgpt, then fetch live branch HEAD and latest five commits. Never open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
