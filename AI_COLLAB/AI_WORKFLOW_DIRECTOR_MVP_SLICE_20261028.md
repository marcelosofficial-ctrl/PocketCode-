# AI Workflow Director — First Testable Feature Slice
**Date:** 2026-10-28  
**Status:** Proposed specification for validation; not implemented, frozen, or tested.  
**Parent research:** [Master AI Workflow Director research](MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md)  
**Evaluation kit:** [Offline Evaluation Kit](AI_WORKFLOW_DIRECTOR_EVALUATION_KIT_20261028.md) (eight fixtures; not yet run).  
**Reference fixtures:** [Expected-output examples](AI_WORKFLOW_DIRECTOR_REFERENCE_FIXTURES_20261028.md) for five priority cases (not AI-generated benchmark data).
**Manual run sheet:** [Paired baseline/Director prompts and record form](AI_WORKFLOW_DIRECTOR_MANUAL_RUN_SHEET_20261028.md); protocol only, no runs recorded.  
**Conformance test design:** [Deterministic AWD-01–16 test specification](AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md); proposed assertions only, not implemented or run.  
**Canonical fixture catalogue:** [AWD-01–AWD-16 repeatable inputs and observable outcomes](AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES_20261028.md); proposed harness data only, not production API, tests, or passing results.  
**Contract reconciliation:** [Decision register](AI_WORKFLOW_DIRECTOR_CONTRACT_DECISION_REGISTER_20261028.md) compares the proposed defaults with existing MVP requirements; recommendations remain unapproved.  
**Purpose:** Convert the research into the smallest useful, provider-neutral feature slice that can be designed and evaluated without API calls, paid services, or privileged access to other apps.

## 1. Scope and non-goals

### In scope
1. Four small task profiles: **Lite**, **Balanced**, **Careful**, and **Review only**.
2. A deterministic task-packet builder that combines the chosen profile with user-provided task/context/constraints/acceptance checks.
3. A portable continuation capsule for saving verified state and resuming in any AI app.
4. Preview, edit, copy, and share-ready text output. The initial slice can be specified and fixture-tested without integrating an AI provider.
5. A small evaluation set comparing ordinary prompts with generated packets.

### Out of scope
- Calling any model/API, spending money, collecting provider credentials, or requiring account connections.
- Background clipboard polling, reading another app's private chat, system-wide overlays, or silent cross-app control.
- Claiming to prevent all free-tier limits, bypass quotas, or guarantee model compliance.
- Running code, changing repositories, merging PRs, deploying, or authorizing consequential actions.
- Implementing all provider adapters or locking the execution backend.
- Treating prompt character count as exact token count.

## 2. User journey

1. User chooses **New AI task** or **Save continuation**.
2. For a task, user chooses a profile and enters the goal; optional fields include relevant context, constraints, acceptance checks, and verification evidence available.
3. PocketCode previews the exact packet and its character count. The user can edit it, remove sensitive content, copy it, or invoke a supported user-initiated share target.
4. User pastes/submits the packet in the AI app themselves.
5. User returns the response, code, or run report to PocketCode through explicit paste/import.
6. PocketCode can produce a continuation capsule with verified facts separated from claims, assumptions, and unknowns.

A packet must still be useful if the target app has no persistent custom instructions, no share integration, and no API. The fallback is ordinary text copy/paste.

## 3. Profile requirements

### Lite
Use for a small, low-risk, well-defined task. Ask for the smallest complete solution, relevant context only, and concise result/verification notes. Do not force a formal plan for trivial edits.

### Balanced (default)
Inspect relevant context and existing solutions; state assumptions only when needed; make the smallest complete change; check the most relevant behavior; report changed, verified, not checked, risks, and next step.

### Careful
Use for high-impact, multi-file, security-sensitive, data-handling, or ambiguous changes. Require explicit scope and acceptance checks, consider relevant failure modes, and report limitations. It must not imply that a review or test happened when it did not.

### Review only
Analyze the supplied proposal/diff/report; do not implement or rewrite unless the user explicitly changes the task. Separate confirmed issues, potential issues, evidence, and questions.

Profile selection is a workflow hint, not a safety bypass or authorization grant. The selected profile must not override project rules, user permissions, provider policies, or safety requirements.

## 4. Task packet contract

The builder should emit sections in this order, omitting optional empty sections rather than filling them with generic text:

1. **Goal** — one concrete outcome.
2. **Profile** — selected profile and short behavior instruction.
3. **Context** — only relevant user-supplied or verified project facts; cite paths/commit IDs when actually known.
4. **Constraints** — scope, platform, budget, permissions, and prohibited actions.
5. **Acceptance** — observable conditions for success.
6. **Verification** — exact checks/evidence expected and whether execution is available.
7. **Reply format** — Changed / Verified / Not checked / Risks / Next step, shortened for Lite if appropriate.

### Input rules
- Trim leading/trailing whitespace in ordinary text fields; do not silently rewrite code, logs, paths, hashes, or quoted evidence.
- Empty optional fields are omitted.
- Never invent file paths, repository state, tests, tool access, runtime status, provider features, or completed work.
- Do not copy a full conversation or the research master by default. Prefer a small selected excerpt and a stable artifact reference.
- The user can preview and edit all generated text before transfer.
- Display a character count as a rough size indicator; do not label it as tokens or predicted cost.
- If content is truncated, say what was omitted. Never truncate a constraint, acceptance criterion, or evidence label silently.

## 5. Continuation capsule contract

The portable capsule should contain:

- format_version
- project
- task_id (optional when not known)
- goal
- status (proposed enum: NOT_STARTED, IN_PROGRESS, BLOCKED, READY_TO_VERIFY, DONE_UNVERIFIED, DONE_VERIFIED)
- verified_facts
- decisions
- constraints
- artifacts (path/URL/hash only when known and relevant)
- checks_run (exact command/check and actual result, or explicitly none)
- not_checked
- blockers
- next_action
- unknowns

The capsule should be short by default and expandable if needed. Do not include secrets, credentials, full logs, or large source files. Redact only when a known pattern is detected; tell the user that automatic redaction is best-effort. Keep source claims and AI/user assertions distinct from independently verified facts. If a prior checkpoint says a fact was verified but the supporting artifact is not included, preserve its attribution (for example, “prior checkpoint reports…”) and do not imply that the current operator independently rechecked it. An unsupported claim must not be promoted into `verified_facts` merely because it was repeated.

### Proposed status semantics

| Status | Use when |
|---|---|
| `NOT_STARTED` | No implementation/work has been reported as started. |
| `IN_PROGRESS` | Work is underway and the goal is not complete. |
| `BLOCKED` | A missing input, permission, artifact, or decision prevents the next meaningful step. |
| `READY_TO_VERIFY` | The relevant implementation/artifact is available and the next step is verification; do not use this to imply that unseen code exists. |
| `DONE_UNVERIFIED` | Work is reported complete, but the required acceptance evidence is absent or incomplete. |
| `DONE_VERIFIED` | Required acceptance checks have concrete, reviewable evidence tied to the relevant artifact/revision. |

`DONE_VERIFIED` is allowed only when the capsule includes concrete verification evidence. If a check was not run or cannot be independently confirmed, choose the status that matches the actual work state; do not use `READY_TO_VERIFY` as a generic synonym for “unknown.” A model's statement that it ran tests is a claim until evidence supports it.

## 6. Proposed portable profile kernel

This is a candidate, not frozen copy:

> Inspect relevant context and reuse existing code, libraries, and platform features before inventing new ones. Do only the requested scope and make the smallest complete change. For complex or risky work, define acceptance checks before editing. Verify the important behavior when tools are available. Never claim a file was inspected or a check was run if it was not. Report what changed, what was verified, what was not checked, risks, and the next step. Preserve a short checkpoint when context is running low.

Do not attach the entire feature research to every task. If persistent instructions are configured, the per-task packet should contain only the task-specific details and any short profile selector needed. If no persistent instructions exist, include the smallest complete profile instruction in the packet.

## 7. Offline/static acceptance tests

These are required test cases for a future implementation; **none have been run yet**.

| ID | Fixture/input | Expected behavior |
|---|---|---|
| AWD-01 | Lite profile + one-line goal | Emits concise packet with Goal, Profile, and Reply format; no forced long plan |
| AWD-02 | Balanced profile + selected file snippet + acceptance criteria | Includes supplied relevant context and criteria; does not append unrelated project history |
| AWD-03 | Careful profile + security-sensitive task | Includes explicit scope and failure-mode/verification expectations without claiming execution |
| AWD-04 | Review only + diff | Explicitly prohibits implementation in this task; requests evidence-linked findings |
| AWD-05 | Empty optional fields | Omits empty sections rather than outputting placeholder prose |
| AWD-06 | User includes a file path/hash | Preserves exact supplied value; does not synthesize new identifiers |
| AWD-07 | No test tool/runtime available | Says verification unavailable/not run; never reports PASS |
| AWD-08 | Very large context | Requests/selects bounded excerpts; any truncation is visible and never silently removes constraints/acceptance |
| AWD-09 | User asks to bypass provider limits | Refuses quota evasion and offers checkpoint/resume or a compliant alternative |
| AWD-10 | Capsule with no executed checks | Cannot claim DONE_VERIFIED |
| AWD-11 | Capsule includes an AI claim that tests passed but no evidence | Keeps it as an unverified claim; DONE_VERIFIED is not allowed |
| AWD-12 | Sensitive-looking content included | Shows preview and warns/redacts only detectable configured patterns; never claims perfect secret detection |
| AWD-13 | Unknown provider capability | Displays unknown/not verified and falls back to copy/paste |
| AWD-14 | User cancels sharing | No transfer is claimed; generated packet remains available locally |
| AWD-15 | Character count displayed | Labeled characters, not tokens or cost |
| AWD-16 | Existing project instructions conflict with a profile | Project/user constraints take precedence; profile cannot authorize a prohibited action |

### Evaluation protocol
For each representative task, compare:
- **Baseline:** user sends a normal prompt with the same source context.
- **Director:** user sends the generated packet with the same source context.

Keep model, plan, task, and evidence constant where possible. Score completion/correctness, unrequested changes, turns, repeated context, prompt/output characters, verification truthfulness, interruptions, and user effort. Record native token/cost metrics only if actually exposed. A small sample is exploratory; do not publish savings claims without adequate repeated trials and transparent limitations.

## 8. Implementation sequence after owner review

1. Implement a pure deterministic packet/capsule builder using local data only.
2. Add unit tests for AWD-01 through AWD-16 and fixtures for malformed/missing fields.
3. Add UI preview/edit/copy. Add share-sheet integration only after platform-specific behavior is verified on real devices.
4. Run baseline-vs-director tasks with free consumer AI modes where available; record missing samples and do not compare unlike models as if only the prompt changed.
5. Add provider-specific setup guides from official documentation, each with a last-verified date and manual fallback.
6. Consider APIs only after a separate cost/privacy/security decision and explicit authorization.

## 9. Exit gate for this slice

The slice is ready for implementation review only when:
- The profile wording is accepted and remains compact.
- Task and capsule fields are agreed, including the status vocabulary.
- Static tests cover omission, exact evidence preservation, non-verified states, and limit-respecting behavior.
- The user can review and edit exactly what will be transferred.
- The plan remains $0 and local-only until explicitly changed.
- No acceptance claim depends on direct control of another app.

Implementation is complete only after the code and tests exist and their exact execution results are recorded. This document alone is a proposal, not proof of implementation or success.

## 10. Relationship to RevDev

The capsule and task packet should be candidates for later mapping to RevDev's mission/continuation and result-report formats. Do not copy or rename RevDev fields by guesswork. Record each mapping as exact match, transform, not represented, or unknown after comparing the actual authoritative artifacts. Keep repositories separate until compatibility is demonstrated and a separate architecture decision is approved.
