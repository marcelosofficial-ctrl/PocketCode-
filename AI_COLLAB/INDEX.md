# INDEX (map of PocketCode docs; target under 1,200 words)

Size: S <8 KB, M 8–25 KB, L 25–50 KB, XL >50 KB (never load XL whole). “History” means named/date only; verify before relying on it.

## Entry set
| Path | Purpose / status |
|---|---|
| BOOT.md, STATE.md, NEXT_TASK.md, CHECKPOINT.md | Start, current state, next task, last unit (live) |
| MAILBOX.md, INBOX_<name>.md, MOVES.tsv | AI coordination, messages, move log (live) |
| kit/docs/WORK_PROTOCOL.md | Work rules v2 (live) |
| kit/docs/PLUGIN_LESSONS.md, REUSE_BACKLOG.md | Plugin learnings and reuse candidates (live) |
| kit/docs/AI_LANES_AND_DISPATCH.md | Task packets and AI routing (proposed; indexed once) |

## Product program (research/proposals)
| Path | Purpose / status |
|---|---|
| STRATEGY_PROGRAM_20261108.md | Strategy tracker (live) |
| APPLE_DESIGN_ENGINEERING_SPEC_20261108.md | PoCo web design proposal; corrected 2026-11-10; not implemented |
| PROVIDER_CACHING_AND_CONTEXT_ENGINEERING_20261110.md; CLAUDE_PROVIDER_AND_LANES_INDEPENDENT_AUDIT_20261111.md | Provider cache/context proposal and independent audit; no provider selected |
| RED_TEAM_CORRECTIONS_CLAUDE_20261110.md | Corrections to earlier Claude documents |
| NAME_COLLISION_RESEARCH_20261111.md | PocketCode/PoCo naming collisions; no rename; clearance pending |
| IPHONE_ONLY_APP_STORE_ROADMAP_20261108.md | Phone-only build/signing/submission; paid steps deferred by D-006 |
| WEBSITE_AUDIT_AND_POCO_PAGE_PLAN_20261108.md | Portfolio audit/page plan; proposed |
| GOVERNANCE_AUDIT_20261108.md | Governance review; proposed |

## Repo root (outside AI_COLLAB)
../AGENTS.md decision rights; ../ARCHITECTURE.md architecture; ../DECISIONS.md D-IDs; ../ROADMAP.md; ../PRODUCT_SPEC.md; ../SECURITY.md; ../PROJECT_STATUS.md (XL history); ../CLAUDE.md; ../GEMINI.md.

## Contracts and recovery
| Path | Purpose / status |
|---|---|
| EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md | Lifecycle/recovery/evidence (L) |
| EVENT_JOURNAL_MODEL_20261106.md; FAKE_OUTBOX_MODEL_20261106.md | In-memory journal and effect-dispatch models |
| DURABLE_ADAPTER_CONTRACT_20261106.md | Adapter-neutral transaction obligations |
| RELEASE_GRANT_ADAPTER_RESEARCH_AND_REDTAM_20261107.md; RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md | Grant adapter/concurrency research |
| P39 review set: P39_CHATGPT_STATIC_AUDIT_ADDENDUM_20261107.md; P39_RESEARCH_REVIEW_DISPOSITIONS_20261108.md; P39_SOURCE_PINNED_AUDIT_CROSSWALK_20261108.md; P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md; GEMINI_P39_REVIEW_RECONCILIATION_20261109.md; P39_GATE_CLOSURE_PLAN_20261109.md; P39_REVIEW_CONSENSUS_MATRIX_20261109.md; P39_RECEIPT_SUBSYSTEM_AUDIT_20261108.md; P39_EP_CANONICAL_ACCEPTANCE_CROSSWALK_20261108.md | Closed/reconciled review and acceptance evidence; implementation gate remains closed |
| P39_OWNER_DELEGATED_DECISIONS_20261111.md | OD-01..OD-13 adopted; implementation gate remains closed |
| P39_EXIT_OWNER_DECISION_REGISTER_20261108.md; EXIT_PROVENANCE_RESOLUTION_20261108.md; EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md | Exit provenance and historical decision register |
| P39 implementation research set: P39_IMPLEMENTATION_GATE_RESEARCH_ADDENDUM_20261109.md; P39_EVENT_RELAY_AND_EXIT_BOUNDARY_RESEARCH_20261109.md | Earlier gate research; do not treat as implementation evidence |
| EXECUTION_BOUNDARY_DURABILITY_AND_EVIDENCE_RESEARCH_20261109.md; PWA_LOCAL_STORAGE_AND_RECOVERY_CONTRACT_20261109.md | Mobile/WASM, storage and recovery |
| GITHUB_PAGES_ORIGIN_ISOLATION_AND_LOCAL_DATA_SECURITY_20261109.md; PHONE_FIRST_EXECUTION_AND_RECOVERY_REDTEAM_20261109.md | Origin and phone-first security |
| PYODIDE_WORKER_CONTROL_CHANNEL_REDTEAM_20261110.md | Worker-channel threats; actual topology UNKNOWN |
| FULL_POWER_GAP_RESEARCH_20261112.md | Ranked execution, grant, storage and evidence research |
| PAGES_READ_ONLY_SOURCE_AUDIT_20261112.md | Exact Pages source/deploy artifact comparison; live response remains unknown |
| ZERO_BUDGET_ORIGIN_OPTIONS_20261112.md | Supplemental $0 hosting-origin comparison; Cloudflare/Netlify research only, no provider selected |
| OPAQUE_ORIGIN_EXECUTION_PROTOCOL_20261112.md | Opaque-origin frame, MessageChannel, CSP, bounded I/O and teardown contract |
| BROWSER_ARTIFACT_STORAGE_RECOVERY_CONTRACT_20261112.md | Origin trust, staged artifact durability signals, eviction recovery and export contract |
| LIFECYCLE_TERMINATION_RECEIPT_ACCEPTANCE_20261112.md | Typed lifecycle, child/wrapper distinction, same-attempt termination and receipt acceptance contract |
| REPORT_PROJECTION_V2_MIGRATION_AND_ACCEPTANCE_20261112.md | Pinned report formatter defect, typed projection boundary and versioned migration/regression packet |
| GRANT_EVENT_ENVELOPE_AND_RELAY_CONTRACT_20261112.md | Versioned event envelope, atomic parity, relay fence and inbox acceptance contract |
| GRANT_EVENT_MODEL_ACCEPTANCE_PLAN_20261112.md | 32 deterministic model scenarios for parity, integrity, relay fencing and inbox/restore |
| P40 source/run set: P40_MODEL_ONLY_EXECUTION_PROTOCOL_20261110.md; P40_BOUNDED_MODEL_RUN_AUTHORIZATION_20261111.md; P40_EXECUTION_ATTEMPT_20261111.md; P40_SOURCE_PINNED_COVERAGE_AND_PAGES_ORIGIN_AUDIT_20261111.md | Exact-SHA model-only plan, approval, run record and coverage/origin audit |
| PR4_CONTINUITY_REFINEMENT_RECONCILIATION_20261109.md | PR #4 seven-file review; no owner action |
| VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md; PROVIDER_NEUTRAL_RECIPE_AND_DURABLE_TASK_MANIFEST_PROPOSAL_20261105.md | Exit matrix and manifest proposal |
| CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md; OWNER_DECISION_REGISTER_20261029.md | LOOP/CASE traceability and earlier decision register |

## Device evidence
PYODIOS_DEVICE_BASELINE_AND_HANDS_ON_PROTOCOL_20261106.md; PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md (O-1); PHONE_DEVICE_VALIDATION_RUNBOOK_20261112.md (read-only, owner/device evidence pending); PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md (XL); IOS_PYTHON_RUNNER_COMPETITIVE_BASELINE_20261103.md.

## Research and review (read by section)
COMPETITOR_FEATURE_AND_OPEN_SOURCE_REUSE_DEEP_DIVE_20261105.md; OPEN_SOURCE_REUSE_AUDIT_20261029.md; OPEN_SOURCE_CANDIDATE_DEEP_DIVE_20261101.md; GEMINI_OPEN_SOURCE_RESEARCH_REVIEW_20261101.md; REVDEV_POCKETCODE_CROSSWALK_INDEPENDENT_REVIEW_20261101.md (XL); POCKETCODE_TASK_EVIDENCE_RECOVERY_RESEARCH_20261106.md; PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md (XL); RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md (XL); PYODIDE/MOBILE audits from 2026-11-03.

## Process and history
RECONCILIATION_2026-11-07.md; CHATGPT_IOS_CONVERSATION_DETAIL_ERROR_RUNBOOK_20261106.md; CHAT_CONTINUITY_AND_MULTI_CHAT_OPERATING_PROTOCOL_20261106.md (superseded start-up); kit/ (templates/work kit). History files (never load whole): CHAT_START_HERE, STATE_LEDGER_20261106, CHAT_WORK_LOG, old handoffs/checkpoints, four-month phone-only plan, old audits, Gemini logs and cross-project continuity files.

Rule: add every new doc here in the same commit that creates it.
