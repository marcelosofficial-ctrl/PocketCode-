# INDEX   (map of PocketCode docs; under 1,200 words)
Size classes: S under 8 KB, M 8-25 KB, L 25-50 KB, XL over 50 KB (never load whole). Status "history" is by name and date, not by reading; check before relying on it.

## Entry set (read these)
| path | what it answers | size | status |
|---|---|---|---|
| BOOT.md | identity, constraints, read order | S | live |
| STATE.md | current status, decisions, open items | S | live |
| NEXT_TASK.md | the single next task | S | live |
| CHECKPOINT.md | last unit of work, resume line | S | live |
| MAILBOX.md | how AIs message each other | S | live |
| MOVES.tsv | log of every moved or archived file | S | live |
| kit/docs/WORK_PROTOCOL.md | working rules v2 | M | live |
| kit/docs/PLUGIN_LESSONS.md | what we adopted from plugins | S | live |
| kit/docs/REUSE_BACKLOG.md | open-source reuse candidates | S | live |

## Product program (2026-11-08, research only)
| path | what it answers | size | status |
|---|---|---|---|
| STRATEGY_PROGRAM_20261108.md | design/product strategy tracker | S | live |
| APPLE_DESIGN_ENGINEERING_SPEC_20261108.md | Claude's proposed PoCo web design; not implemented | S | proposed |
| IPHONE_ONLY_APP_STORE_ROADMAP_20261108.md | phone-only build, signing, TestFlight and submission | M | proposed |
| WEBSITE_AUDIT_AND_POCO_PAGE_PLAN_20261108.md | portfolio audit and PoCo page plan | M | proposed |
| GOVERNANCE_AUDIT_20261108.md | rule audit and recommendations | M | proposed |
| CLAUDE_REVIEW_RELEASE_GRANT_RESEARCH_20261108.md | partial F-01..F-09 review; superseded | S | superseded |

## Repo root (outside AI_COLLAB; read from repo root)
| path | what it answers | size | status |
|---|---|---|---|
| ../AGENTS.md | shared rules and decision rights | S | live |
| ../ARCHITECTURE.md | architecture sketch | S | reference |
| ../DECISIONS.md | decision log (D IDs) | S | live |
| ../ROADMAP.md | roadmap | S | reference |
| ../PRODUCT_SPEC.md | product spec | M | reference |
| ../SECURITY.md | security notes | S | reference |
| ../PROJECT_STATUS.md | long status history | XL | history |
| ../CLAUDE.md | Claude-specific notes (18 KB); Claude only | M | provider |
| ../GEMINI.md | Gemini-specific notes | S | provider |

## Contracts and models (current recovery and release work)
| path | what it answers | size | status |
|---|---|---|---|
| EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md | lifecycle, recovery, evidence semantics | L | live |
| EVENT_JOURNAL_MODEL_20261106.md | event journal prototype, limits | S | live |
| FAKE_OUTBOX_MODEL_20261106.md | fake outbox model | S | live |
| DURABLE_ADAPTER_CONTRACT_20261106.md | what a durable adapter must satisfy | M | live |
| RELEASE_GRANT_ADAPTER_RESEARCH_AND_REDTAM_20261107.md | adapter research and red team | M | under review |
| RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md | concurrency and crash spec | M | under review |
| P39_CHATGPT_STATIC_AUDIT_ADDENDUM_20261107.md | static audit | M | under review |
| P39_INDEPENDENT_REVIEW_PROMPT_20261107.md | review brief | S | live |
| P39_RESEARCH_REVIEW_DISPOSITIONS_20261108.md | Claude research finding dispositions | M | interim; gate open |
| P39_SOURCE_PINNED_AUDIT_CROSSWALK_20261108.md | source-pinned S1..S8 and P37 crosswalk | M | audit complete; gate open |
| P39_CLAUDE_REVIEW_RECONCILIATION_20261108.md | Claude P39 findings, tests and gate | L | owner gate open |
| GEMINI_P39_REVIEW_RECONCILIATION_20261109.md | Gemini findings and corrected adapter boundaries | M | owner gate open |
| P39_GATE_CLOSURE_PLAN_20261109.md | review, owner-decision and implementation-gate sequence | M | no implementation |
| P39_REVIEW_CONSENSUS_MATRIX_20261109.md | Claude/Gemini reconciliation and owner dependencies | L | owner gate open |
| P39_RECEIPT_SUBSYSTEM_AUDIT_20261108.md | receipt model/test audit; RCP-01..05 | L | adapter unverified |
| P39_EP_CANONICAL_ACCEPTANCE_CROSSWALK_20261108.md | P39/RG/RCP and EP-01..25 to LOOP/CASE | L | gates open |
| P39_EXIT_OWNER_DECISION_REGISTER_20261108.md | OD-01..13 streaming, revocation, identity, receipts and exit | M | all OPEN |
| EXIT_PROVENANCE_RESOLUTION_20261108.md | child/wrapper exit, termination and verdict rules | M | proposed |
| EXIT_PROVENANCE_STATIC_CONSISTENCY_AUDIT_20261108.md | EP-01..25 consistency and formatter gaps | M | static audit |
| P39_IMPLEMENTATION_GATE_RESEARCH_ADDENDUM_20261109.md | outbox, revocation and exit-provenance research | M | gate closed |
| EXECUTION_BOUNDARY_DURABILITY_AND_EVIDENCE_RESEARCH_20261109.md | mobile/WASM boundary, crash durability and evidence | M | no stack selected |
| P39_EVENT_RELAY_AND_EXIT_BOUNDARY_RESEARCH_20261109.md | outbox, retries, fencing and mobile exit evidence | L | gate closed |
| PWA_LOCAL_STORAGE_AND_RECOVERY_CONTRACT_20261109.md | IndexedDB/OPFS recovery, Web Locks and PWA tests | L | no storage engine selected |
| GITHUB_PAGES_ORIGIN_ISOLATION_AND_LOCAL_DATA_SECURITY_20261109.md | shared-origin storage threat and ORIGIN tests | M | URL unknown |
| PHONE_FIRST_EXECUTION_AND_RECOVERY_REDTEAM_20261109.md | origin, Pyodide, storage crash and evidence red-team | L | no implementation |
| PAGES_AND_EXIT_PROVENANCE_VERIFICATION_20261110.md | Pages facts, URL unknowns, Worker/native exit and EP tests | M | no implementation |
| PYODIDE_WORKER_CONTROL_CHANNEL_REDTEAM_20261110.md | Pyodide FFI and Worker channel spoofing tests | M | actual topology UNKNOWN |
| FULL_POWER_GAP_RESEARCH_20261110.md | outbox, fencing, PWA recovery, execution evidence and red-team corrections | M | NOT IMPLEMENTED / NOT RUN |
| PR4_CONTINUITY_REFINEMENT_RECONCILIATION_20261109.md | seven-file PR #4 review, KEEP/MERGE-INTO-BOOT/DROP classifications and no-merge recommendation | M | review complete; PR remains owner-controlled |

| VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md | exit provenance matrix | M | live (O-5) |
| PROVIDER_NEUTRAL_RECIPE_AND_DURABLE_TASK_MANIFEST_PROPOSAL_20261105.md | recipe and manifest proposal | M | proposal |
| CANONICAL_ACCEPTANCE_TRACEABILITY_20261029.md | LOOP and CASE traceability | S | live |
| OWNER_DECISION_REGISTER_20261029.md | owner decisions | M | live |

## Device evidence (Pyodios)
| path | what it answers | size | status |
|---|---|---|---|
| PYODIOS_DEVICE_BASELINE_AND_HANDS_ON_PROTOCOL_20261106.md | device test protocol | M | live |
| PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md | Console probe steps (O-1) | M | live |
| PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md | canonical fixed task (sections 2A and 8) | XL | canonical |
| IOS_PYTHON_RUNNER_COMPETITIVE_BASELINE_20261103.md | iOS runner comparison | M | reference |

## Research and review (reference; read by section)
COMPETITOR_FEATURE_AND_OPEN_SOURCE_REUSE_DEEP_DIVE_20261105.md (L), OPEN_SOURCE_REUSE_AUDIT_20261029.md (L), OPEN_SOURCE_CANDIDATE_DEEP_DIVE_20261101.md (M), GEMINI_OPEN_SOURCE_RESEARCH_REVIEW_20261101.md (M), REVDEV_POCKETCODE_CROSSWALK_INDEPENDENT_REVIEW_20261101.md (XL), POCKETCODE_TASK_EVIDENCE_RECOVERY_RESEARCH_20261106.md (L), PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md (XL), RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md (XL), PYODIDE_* and MOBILE_* audits of 20261103 (M-L).

## Process and continuity
| path | what it answers | size | status |
|---|---|---|---|
| RECONCILIATION_2026-11-07.md | what was committed vs claimed, CI by commit | S | live |
| CHATGPT_IOS_CONVERSATION_DETAIL_ERROR_RUNBOOK_20261106.md | ChatGPT iOS error runbook | S | reference |
| CHAT_CONTINUITY_AND_MULTI_CHAT_OPERATING_PROTOCOL_20261106.md | older multi-chat protocol | M | superseded by BOOT and kit/docs/WORK_PROTOCOL.md for starting chats |
| kit/ | work kit: docs, templates, prompts | S-M | live |

## History (do not load whole; read a named section only)
CHAT_START_HERE.md (XL), STATE_LEDGER_20261106.md (XL), CHAT_WORK_LOG.md (XL), CHAT_HANDOFF_20261029_POCKETCODE.md (XL), CHAT_HANDOFF_ADDENDUM_20261101.md (XL), NEW_CHAT_BOOTSTRAP_20261101.md (L), NEW_CHAT_HANDOFF_20261028.md, _20261103.md, _20261105.md, _20261106.md, POCKETCODE_CURRENT_CHECKPOINT_20261028.md (XL), FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md (L), all 20261028 and 20261029 audit, matrix, checklist and G01-G08 files, GEMINI_HANDOFF.md, GEMINI_PROGRESS_LOG.md, CROSS_PROJECT_* and REVDEV_* continuity updates.

Rule: every new doc gets a row (or a group entry) here in the same commit that creates it.
