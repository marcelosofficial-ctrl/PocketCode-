# STATE: PocketCode   (current state only; under 900 words)
Updated: 2026-11-09 by ChatGPT. Sources: live branch re-fetched 2026-11-09; exact HEAD is recorded in CHECKPOINT.md; pinned source/test evidence 744cb4dc7cd4994647c84ac7476c0d78a21f0540; Claude P39 review reconciliation and receipt/exit audits indexed below.

## Status
- Phase: Discovery and product definition. No runtime, provider, database or hosting selected. Active branch is far ahead of main; commit count is not product progress.
- VERIFIED: GitHub Actions run 42365455316, exact source/test SHA 744cb4dc7cd4994647c84ac7476d0c78a21f0540, Python 3.12 ubuntu-latest, 266/266 tests PASS.
- VERIFIED: current branch HEAD e643d59dd64dbdf52bed084fe55d74a38805a55a has no Actions run. Workflow is path-filtered to scripts/** and itself; workflow_dispatch exists but no manual run was performed. Current changes since 744cb4d are documentation/continuity only. Thus 266/266 remains historical exact-SHA evidence, not a fresh current-HEAD run.
- COMMITTED: intent/proof separation; exact receipt-revision authorization binding; current-grant recovery; concurrency/crash specification; sequential grant model/tests; P39 source audit, Claude reconciliation, receipt audit, canonical crosswalk, exit-provenance proposal/audit, owner decision register, and primary-source implementation-gate research addendum (2026-11-09).
- CLAIMED ONLY / NOT BUILT: durable adapter; real concurrent processes; transactional outbox relay; durable crash recovery; production fencing; transport stream ownership/revocation; trusted policy authority; client receipt.
- Claude's independent P39 review (owner-supplied, not committed as a raw report): P39-S1..S3 confirmed, S4 refined to contract/MVP scope gap; additional clock, pre-commit revocation and restart-ID findings. Claude ran C1-C7 against a byte-verified copy of the pinned sequential model; repository suite was not run by Claude. Receipt subsystem and adapter audit were separately completed by ChatGPT at source/test SHA 744cb4d.
- P39/exit gate: CLOSED. Gemini's independent source-pinned P39 review remains outstanding. No independent Claude exit-provenance report is evidenced in the current ChatGPT inbox; confirm whether that review remains required before re-requesting. Owner decisions OD-01..OD-13 remain OPEN; recommendations are not approvals. No source/test changes authorized.
- Product program (research only): App Store roadmap, website/PoCo page plan and governance audit committed. No name change, website edit, enrollment, spend or deployment authorized.

## Decisions
- D-001 unified PC-and-phone direction with separate development boundaries. D-002 GitHub is source of truth. D-003 no secrets in public repo. D-004 validate before stack commitment. D-005 zero spend.
- OpenHands/Cline are pattern references only; reject wildcard auto-approve. MCP Tasks and ACP are optional adapters and do not replace PocketCode command/attempt identity.
- No durable store selected until atomic persistence contract is defined and tested.
- CASE-04 stays INCOMPLETE / timed_out. No precedence-only patch to report_contract.py.
- Website design must not change. Do not publish PoCo claims beyond built evidence. PocketCode rename to PoCo is only under consideration; nothing renamed.
- No changes to PR #2/#3 or canonical LOOP/CASE/D IDs.

## Open items
- O-1 Owner: read-only Pyodios Console probe (PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md).
- O-2 Gemini independent P39 review; confirm whether Claude exit-provenance review is still required; reconcile any received reports against immutable pins.
- O-3 Obtain explicit owner decisions OD-01..OD-13 in P39_EXIT_OWNER_DECISION_REGISTER_20261108.md.
- O-4 Define atomic persistence contract and adapter evidence only after review/owner gates.
- O-5 Keep P39/P40 implementation gate closed until O-2/O-3 clear. Research addendum P39_IMPLEMENTATION_GATE_RESEARCH_ADDENDUM_20261109.md adds external evidence but makes no owner decisions.
- O-6 Strategy program research: Apple design engineering, context engineering/provider caching, remaining website audit; no implementation/publication without separate authorization.
- O-7 Owner decisions: PoCo name/trademark/domain, possible US$99 Apple Developer Program spend, LinkedIn copy, main pointer banner, optional secret scanner.
- O-8 LinkedIn About/Experience text required from owner; RevDev UI source inaccessible until PC access.

## Known risks
- Chats can freeze while commits continue; always inspect last five commits after checkpoint.
- Large history files are not entry points. Start from BOOT, STATE, NEXT_TASK, CHECKPOINT, INBOX only.
- Keep sequential model evidence distinct from real adapter, concurrent-process, durable-store and device evidence.
