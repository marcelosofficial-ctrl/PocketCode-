# AI Efficiency Coach & Handoff — PocketCode Proposal

**Status:** Product/UX proposal; not accepted as an implementation or architecture decision.  
**Date:** 2026-10-28  
**Budget:** $0.  
**Related master:** [AI Workflow Efficiency and Cross-App Orchestration Master](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/AI_WORKFLOW_EFFICIENCY_AND_CROSS_APP_ORCHESTRATION_MASTER_2026-10-28.md).  
**Product boundary:** PocketCode remains a separate project from RevDev under accepted D-001.

## 1. Problem hypothesis

A person on a phone may use ChatGPT, Claude, Gemini or another assistant to generate technical work, then get stuck when the assistant assumes they have a computer, loses important task state, produces too much code/context, asks repeatedly for already supplied information, or hits a usage/tool limitation. A compact workflow coach could help the user direct the assistant toward useful complete progress while preserving a reliable handoff into PocketCode.

This is an unvalidated hypothesis, not evidence that these problems occur at a particular rate or that existing tools fail to solve them.

## 2. Product outcome

Help the user **get more verified progress out of the AI capability they already have access to**, including free tiers, without falsely claiming to unlock hidden tools, extra quotas, larger context or provider-only features.

The coach is a candidate feature distinct from PocketCode's execution/reporting loop. It does not require an AI API or account link.

## 3. First no-cost user flow

1. **Choose a work profile:** Lean, Balanced, Deep Verify, Research/3-pass, Repair/Recovery, Continue/Checkpoint. The app may suggest one based on a short task description; let the user change it.
2. **Describe the task:** goal, acceptance checks, constraints and optional relevant paths/notes.
3. **Prepare instructions:** show a compact provider-neutral packet with what the chosen mode expects and what information is missing.
4. **Copy/share:** use a visible Copy button or the platform-supported iOS/Android share interface. User chooses the destination and submits; PocketCode does not silently send.
5. **Bring the result back:** user shares/pastes the assistant's proposed code, error, answer or relevant excerpt into PocketCode.
6. **Make a next step:** the app can help construct a bounded execution request or focused AI correction prompt. In the current prototype all output is simulated and must be labelled as such.
7. **Checkpoint:** save a short task summary and durable artifact pointers for long tasks so the next session need not reconstruct the entire chat.

## 4. Profiles

| Profile | Intent | Typical output |
|---|---|---|
| Lean | Small, bounded task | Short instruction, minimal complete solution, one relevant check |
| Balanced | Default engineering/task work | Relevant inspection, plan only when useful, implementation, real evidence, compact report |
| Deep Verify | High-risk or subtle change | Failure paths, security concerns, test/verification evidence and unresolved risks |
| Research/3-pass | Broad or uncertain research | Primary sources, comparison/falsification, synthesis and source register |
| Repair/Recovery | Failed/ambiguous attempt | Exact state first, evidence preservation, targeted fix, capped retries |
| Continue/Checkpoint | Long task or context boundary | Verified facts, decisions, unknowns, artifact pointers, tests and next action |

These are behavior templates, not modes all AI apps necessarily support natively. The generic prompt is the cross-provider fallback. Native integrations are optional capability adapters.

## 5. Packet contents

Candidate text packet:
- version and task ID;
- chosen profile and target assistant (optional);
- goal and acceptance criteria;
- constraints and forbidden actions;
- short verified context and evidence pointers;
- explicit unknowns and missing inputs;
- retry/stop condition;
- requested result format: outcome, checks actually run, gaps/risks, next action.

Keep it concise. Include only task-relevant excerpts. Do not include full conversation histories, large log dumps, secret environment values, credentials or unrelated files. Exact provider token counts should only be displayed if surfaced through a supported authoritative interface; otherwise say estimated or unknown.

## 6. Platform and integration ladder

- **Baseline:** user-driven copy/paste and Share Sheet/Android Sharesheet. Should work wherever an assistant accepts text.
- **Later, optional:** user-reviewed rule/skill files or documented CLI/IDE integrations for a specific agent.
- **Not baseline:** direct app-to-app control, hidden history ingestion, continuous clipboard polling, automatic message submission, or autonomous cross-app execution. Those require platform/vendor feasibility checks, separate permission/security design and explicit approval.

Provider profile options must not imply more quota or tool capability. If a host does not support a requested automation, show that as unsupported and fall back to manual sharing.

## 7. “Free-mode optimization” requirements

- Build a clear task packet up front to avoid unnecessary clarifying turns.
- Keep permanent prompt text small; load task-specific procedures only when selected.
- Point to relevant evidence; avoid repeatedly pasting the same long material.
- Batch related work when doing so avoids round trips, but don't create an unmanageably broad task.
- Encourage local deterministic checks when the user has them and the task is safe.
- Use bounded repair attempts and a checkpoint after repeated failure.
- Respect actual provider limits and terms. Do not evade quotas, rotate accounts, fake usage state or assume consumer subscriptions include API calls.
- Do not cut requested scope, security checks or necessary verification merely to save tokens.
- Do not market token savings until representative fixed-scope tests verify them.

## 8. Acceptance tests for the synthetic prototype

All are **NOT RUN** until implemented in a named harness with recorded evidence.

| ID | Fixture | Expected |
|---|---|---|
| AEC-001 | One-sentence small task | Suggest Lean, packet remains short and complete |
| AEC-002 | Multi-file engineering change with acceptance criteria | Suggest Balanced or Deep Verify; include criteria and boundaries |
| AEC-003 | User supplies long logs but only one error matters | Packet contains a bounded excerpt/pointer and preserves the exact failure |
| AEC-004 | Long task enters new session | Checkpoint includes verified facts, unknowns, current artifact pointers and next action |
| AEC-005 | Task fails repeatedly | Coach does not encourage endless retry; asks for targeted diagnosis/next decision |
| AEC-006 | User selects an assistant with no supported connector | Make copy/share fallback available and do not claim a send occurred |
| AEC-007 | User asks to bypass provider's free-tier usage cap | Decline evasion; suggest legitimate workflow efficiency or wait for reset |
| AEC-008 | Prompt packet contains user notes with instruction-like malicious text | Treat notes as task data; don't allow them to override policy |
| AEC-009 | Example includes fake token/time/cost counters | Label simulated/estimated; never imply measured provider telemetry |
| AEC-010 | Assistant response contains execution instructions | Do not treat those instructions as execution authorization |
| AEC-011 | Share/paste unavailable | Keep packet selectable and explain manual alternative |
| AEC-012 | User changes chosen profile | Rebuild packet for selected profile and keep the intent clear |

## 8A. Compact prompt and evaluation protocol

To prevent the coach itself from wasting context, use the shorter [AI Work Coach compact prompt and zero-cost evaluation protocol](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/AI_WORK_COACH_ABLATION_AND_COMPACT_PROMPT_V0_1.md). It defines an A/B/C comparison (no coach vs compact kernel vs kernel plus selected profile), 18 synthetic acceptance cases, and an evidence-led metric set. It explicitly marks all tests NOT RUN until a real harness records results. RevDev also now has a [machine-readable AWC fixture manifest](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/AI_WORK_COACH_SYNTHETIC_FIXTURES_V0_1.json), [schema](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/AI_WORK_COACH_SYNTHETIC_FIXTURES_SCHEMA_V0_1.json), and [format contract](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/AI_WORK_COACH_SYNTHETIC_FIXTURE_FORMAT_V0_1.md). These are RevDev-only fixture definitions for structural reference; PocketCode's AEC-001–AEC-012 remain its own tests, and the manifest is not an implemented harness or test evidence.

Use progressive disclosure: do not resend a large permanent prompt every turn if the host retains instructions; append only the selected profile and task-specific evidence. Do not claim a token saving until comparable runs at equal task scope show it.

## 9. Measures of success

Compare the coach with a baseline on fixed tasks. Record: task requirements completed; real checks and outcomes; scope completeness; retry/rework count; model turns/tool calls where visible; exact tokens/cost only if authoritative; estimated values separately; elapsed time; user interventions; safety misses; and whether a fresh session can resume from the checkpoint. A shorter output that misses requirements is a regression.

## 10. Out of scope now

No provider/API selection, API keys, authentication, backend, live model calls, automatic message submission, PC pairing, native release commitment, paid service, usage-limit evasion, production runner, or new permissions. No existing PocketCode PR #2 is touched by this document.

## 11. Required research / owner decisions still open

- Which assistant surfaces and phone OS flows are the first real target for testing?
- Does the task-profile selector help users, or is a single “prepare instructions” action clearer?
- Which features should be generic versus assistant-specific profiles?
- What current platform restrictions and app-store review considerations apply to any future native integration?
- Does measured task completeness improve at equal or lower context/tool use?

These are open questions. No feature implementation is claimed.
