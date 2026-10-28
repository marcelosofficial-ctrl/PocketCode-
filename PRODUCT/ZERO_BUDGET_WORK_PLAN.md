# PocketCode Zero-Budget Work Plan

**Status:** Active working constraint, 2026-10-20  
**Budget assumption:** $0 available for this project unless the owner explicitly changes this constraint.  
**Purpose:** Keep making progress without subscriptions, surprise charges, or avoidable CI usage.

## Hard rules

- Do not create a paid account, start a trial that may convert to paid, attach a payment method, enable billing, purchase a domain, or run billable workloads.
- Do not assume promotional credits, free tiers, or open-source software guarantee zero cost. Recheck current limits and billing terms before relying on any hosted service.
- Do not create provider accounts, add credentials, or run live sandbox workloads as part of routine progress. The existing proof runbook stays unexecuted until the owner explicitly approves a genuinely zero-cost test path.
- Do not add an AI API integration that requires paid tokens. Keep copy/paste handoff as the default.
- Preserve the current static prototype and label its execution results as simulated.
- Conserve GitHub Actions minutes. Make documentation-only changes without triggering deployment; run source checks locally where a suitable environment is available. Deploy only when the prototype itself materially changes or the owner asks.
- Never move untrusted code onto the app server or developer workstation just to avoid a cloud bill.

## What we can do for $0

1. **Review public user evidence:** use `RESEARCH/MOBILE_CODING_USER_EVIDENCE.md` as the starting point; prefer firsthand discussions and include evidence against the idea. Interviews are optional, not a blocker.
2. **Improve the prototype:** make small, understandable UX changes based on observed confusion; keep it static and simulated.
3. **Test source-level behavior locally:** run the dependency-free Python checker and unit tests when a Python environment is available. These checks do not prove browser behavior, accessibility, or sandbox security.
4. **Strengthen the contract and threat model:** review state transitions, quotas, file handling, cancellation, data retention, abuse controls, and truthful reporting before implementation.
5. **Compare existing options on paper:** use official docs to identify hard blockers and free-tier conditions; do not sign up or run workloads just to gather pricing evidence.
6. **Prepare a portable local development path:** keep source files and scripts simple enough to edit from a phone when necessary; avoid choosing a framework until the product need is validated.

## What we should not do yet

- Build a public arbitrary-code execution endpoint.
- Select Modal, Cloudflare, Daytona, or another provider based only on promotional credits.
- Build accounts, payments, an AI API integration, multi-language support, or a large project workspace.
- Spend Actions minutes on documentation-only commits.
- Claim demand, accessibility, execution reliability, or security has been validated without evidence.

## Decision gates

### Gate A — Evidence of need
Start with public firsthand discussions, reviews, and community feature requests. Document recurring pain points, existing workarounds, positive experiences, and counter-evidence. This is qualitative desk research, not a representative sample. User interviews are optional; lack of access to interview participants must not block progress. Before backend work, the evidence should at least identify a specific unmet job that existing tools do not already solve adequately.

### Gate B — Zero-cost implementation path
Before any hosted execution experiment, document:
- why local-only/mock testing is insufficient for the next question;
- a verified route to test without a payment method or billable usage;
- current service limits and any account/trial expiry behavior;
- how to stop execution, enforce egress restrictions, and clean up;
- an explicit owner go-ahead.

If any cost or billing condition is uncertain, do not run the workload. Continue with mock interfaces, static analysis, and design review.

### Gate C — Revisit the budget only by choice
If real execution eventually cannot be demonstrated at $0, stop at that boundary and explain the trade-off. Do not silently spend money or pressure the owner to pay. The owner decides whether to wait, find a different free path, or change the budget.

## AI Efficiency Coach research path (2026-10-28)

The [AI Efficiency Coach & Handoff proposal](AI_EFFICIENCY_COACH_HANDOFF_PROPOSAL_2026-10-28.md) adds a candidate no-provider feature. The shared research master is [AI Workflow Efficiency and Cross-App Orchestration](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/AI_WORKFLOW_EFFICIENCY_AND_CROSS_APP_ORCHESTRATION_MASTER_2026-10-28.md).

Zero-cost next steps allowed:
- Refine the proposal and profile/task-packet wording.
- Create deterministic synthetic fixtures for prompt generation and checkpointing.
- Test that unsupported integration falls back to copy/share and that examples stay labelled SIMULATED.
- Compare the feature with documented OS/provider surfaces through public documentation only.
- Record user-visible behavior and open questions in GitHub.

Do not add model API calls, accounts, paid tools, backend code execution, silent message submission or real cross-app automation as part of this work. “Free-mode optimization” means more verified useful progress within legitimate current limits, never bypassing limits or skipping necessary validation.

## Current next action

Use `RESEARCH/MOBILE_CODING_USER_EVIDENCE.md` to guide desk research and narrow the proposed user job. Improve only the static prototype and its source-level checks; do not start provider implementation. The interview script is optional if relevant participants become available later.
