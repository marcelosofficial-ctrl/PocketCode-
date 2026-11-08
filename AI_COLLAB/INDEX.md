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
| CLAUDE_REVIEW_RELEASE_GRANT_RESEARCH_20261108.md | Claude review of research packet only; not source/model review | S | partial review |
| P39_RESEARCH_REVIEW_DISPOSITIONS_20261108.md | interim decisions F-01..F-09 plus source cross-check | M | interim; P39 open |
| VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md | exit provenance matrix | M | live (O-5) |
| EXIT_PROVENANCE_RESOLUTION_20261108.md | child vs wrapper exit, termination and verdict projection rules plus adversarial tests | M | proposed; review pending |
| PROVIDER_NEUTRAL_RECIPE_AND_DURABLE_TASK_MANIFEST_PROPOSAL_20261105.md | recipe and manifest proposal | M | proposal |

## Canonical acceptance and decisions
| path | what it answers | size | status |
|---|---|---|---|
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
