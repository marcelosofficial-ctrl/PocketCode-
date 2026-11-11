# INDEX (map of PocketCode docs; target under 1,200 words)

Size: S <8 KB, M 8–25 KB, L 25–50 KB, XL >50 KB (never load XL whole). “History” means named/date only; verify before relying on it.

## Entry set
| Path | Purpose / status |
|---|---|
| BOOT.md, STATE.md, NEXT_TASK.md, CHECKPOINT.md | Start, current state, next task, last unit (live) |
| MAILBOX.md, INBOX_<name>.md, MOVES.tsv | AI coordination, messages, move log (live) |
| kit/docs/WORK_PROTOCOL.md | Work rules v2 (live) |
| kit/docs/PLUGIN_LESSONS.md, REUSE_BACKLOG.md | Plugin learnings and reuse candidates (live) |
| kit/docs/AI_LANES_AND_DISPATCH.md | Task packets and AI routing (proposed; see independent audit) |

## Product program (research/proposals)
| Path | Purpose / status |
|---|---|
| STRATEGY_PROGRAM_20261108.md | Strategy tracker (live) |
| APPLE_DESIGN_ENGINEERING_SPEC_20261108.md | PoCo web design proposal; corrected 2026-11-10; not implemented |
| PROVIDER_CACHING_AND_CONTEXT_ENGINEERING_20261110.md | Provider cache/context proposal (proposed; independently audited) |
| CLAUDE_PROVIDER_AND_LANES_INDEPENDENT_AUDIT_20261111.md | Current provider-cache facts, AI-role corrections, measurement contract (audit) |
| RED_TEAM_CORRECTIONS_CLAUDE_20261110.md | Claude's corrections to earlier docs |
| IPHONE_ONLY_APP_STORE_ROADMAP_20261108.md | Phone-only build/signing/submission; paid steps deferred by D-006 |
| WEBSITE_AUDIT_AND_POCO_PAGE_PLAN_20261108.md | Portfolio audit/page plan (proposed) |
| GOVERNANCE_AUDIT_20261108.md | Governance review (proposed) |
| CLAUDE_REVIEW_RELEASE_GRANT_RESEARCH_20261108.md | Superseded partial F-01..F-09 review |

## Repo root (outside AI_COLLAB)
`../AGENTS.md` decision rights; `../ARCHITECTURE.md` architecture; `../DECISIONS.md` D-IDs; `../ROADMAP.md`; `../PRODUCT_SPEC.md`; `../SECURITY.md`; `../PROJECT_STATUS.md` (XL history); `../CLAUDE.md` (Claude only); `../GEMINI.md` (Gemini only).

## Contracts and recovery
| Path | Purpose / status |
|---|---|
| EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md | Lifecycle/recovery/evidence (L) |
| EVENT_JOURNAL_MODEL_20261106.md; FAKE_OUTBOX_MODEL_20261106.md | In-memory models |
| DURABLE_ADAPTER_CONTRACT_20261106.md | Adapter obligations |
| RELEASE_GRANT_ADAPTER_RESEARCH_AND_REDTAM_20261107.md; RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md | Grant adapter/concurrency research (under review) |
| P39_CHATGPT_STATIC_AUDIT_ADDENDUM_20261107.md; P39_INDEPENDENT_REVIEW_PROMPT_20261107.md | Static audit and review brief |
| P39_RESEARCH_REVIEW_DISPOSITIONS_20261108.md; P39_SOURCE_PINNED_AUDIT_CROSSWALK_20261108.md | Finding dispositions and source crosswalk |
| P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md; GEMINI_P39_REVIEW_RECONCILIATION_20261109.md | Independent review reconciliations |
| P39_GATE_CLOSURE_PLAN_20261109.md; P39_REVIEW_CONSENSUS_MATRIX_20261109.md | Review and owner gate (open) |
| P39_RECEIPT_SUBSYSTEM_AUDIT_20261108.md; P39_EP_CANONICAL_ACCEPTANCE_CROSSWALK_20261108.md | Receipt audit and EP-to-LOOP/CASE map |
| P39_EXIT_OWNER_DECISION_REGISTER_20261108.md | OD-01..13 (all open) |
| P39_OWNER_DELEGATED_DECISIONS_20261111.md | OD-01..13 adopted under explicit owner delegation; implementation gate remains closed |
| EXIT_PROVENANCE_RESOLUTION_20261108.md; EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md | Child/wrapper/termination and formatter gaps |
| P39_IMPLEMENTATION_GATE_RESEARCH_ADDENDUM_20261109.md; P39_EVENT_RELAY_AND_EXIT_BOUNDARY_RESEARCH_20261109.md | Outbox, revocation, exit evidence (gate closed) |
| EXECUTION_BOUNDARY_DURABILITY_AND_EVIDENCE_RESEARCH_20261109.md; PWA_LOCAL_STORAGE_AND_RECOVERY_CONTRACT_20261109.md | Mobile/WASM, storage and recovery |
| GITHUB_PAGES_ORIGIN_ISOLATION_AND_LOCAL_DATA_SECURITY_20261109.md; PHONE_FIRST_EXECUTION_AND_RECOVERY_REDTEAM_20261109.md | Origin and phone-first security |
| PAGES_AND_EXIT_PROVENANCE_VERIFICATION_20261110.md | Superseded for Pages facts by 11/11 audit |
| PYODIDE_WORKER_CONTROL_CHANNEL_REDTEAM_20261110.md | Worker-channel threats; topology unknown |
| FULL_POWER_GAP_RESEARCH_20261110.md | Gap research (not implemented/run) |
| P40_MODEL_ONLY_EXECUTION_PROTOCOL_20261110.md | Six-lane model-only plan (not authorized/run) |
| P40_BOUNDED_MODEL_RUN_AUTHORIZATION_20261111.md | Exact source-pinned read-only run request; owner approved, execution blocked |
| P40_EXECUTION_ATTEMPT_20261111.md | Approved run attempt; target pins verified; runner unavailable, tests NOT RUN |\n| P40_SOURCE_PINNED_COVERAGE_AND_PAGES_ORIGIN_AUDIT_20261111.md | Source/test mapping and Pages/shared-origin audit |
| PR4_CONTINUITY_REFINEMENT_RECONCILIATION_20261109.md | PR #4 seven-file review; no merge recommendation |
| VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md; PROVIDER_NEUTRAL_RECIPE_AND_DURABLE_TASK_MANIFEST_PROPOSAL_20261105.md | Exit matrix and manifest proposal |
| CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md; OWNER_DECISION_REGISTER_20261029.md | LOOP/CASE traceability and earlier owner register |

## Device evidence
`PYODIOS_DEVICE_BASELINE_AND_HANDS_ON_PROTOCOL_20261106.md`; `PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md` (O-1); `PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md` (XL canonical); `IOS_PYTHON_RUNNER_COMPETITIVE_BASELINE_20261103.md`.

## Research and review (read by section)
`COMPETITOR_FEATURE_AND_OPEN_SOURCE_REUSE_DEEP_DIVE_20261105.md`; `OPEN_SOURCE_REUSE_AUDIT_20261029.md`; `OPEN_SOURCE_CANDIDATE_DEEP_DIVE_20261101.md`; `GEMINI_OPEN_SOURCE_RESEARCH_REVIEW_20261101.md`; `REVDEV_POCKETCODE_CROSSWALK_INDEPENDENT_REVIEW_20261101.md` (XL); `POCKETCODE_TASK_EVIDENCE_RECOVERY_RESEARCH_20261106.md`; `PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md` (XL); `RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md` (XL); relevant PYODIDE/MOBILE audits from 2026-11-03.

## Process and history
`RECONCILIATION_2026-11-07.md`; `CHATGPT_IOS_CONVERSATION_DETAIL_ERROR_RUNBOOK_20261106.md`; `CHAT_CONTINUITY_AND_MULTI_CHAT_OPERATING_PROTOCOL_20261106.md` (superseded for start-up by BOOT/WORK_PROTOCOL); `kit/` (templates/work kit). History files (never load whole): CHAT_START_HERE, STATE_LEDGER_20261106, CHAT_WORK_LOG, handoffs/bootstrap/checkpoints, four-month phone-only plan, old 2026-10-28/29 audits, Gemini logs, CROSS_PROJECT and REVDEV continuity files.

Rule: add every new doc here in the same commit that creates it.