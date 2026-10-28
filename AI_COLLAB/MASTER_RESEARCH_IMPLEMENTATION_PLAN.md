# PocketCode — Master Research and Implementation Plan

**Status:** Scaffold only; Gemini research is not yet complete.  
**Created:** 2026-10-20.  
**Warning:** Do not treat this document as evidence or a completed plan until sections are populated with sourced findings and reviewed.

**Interim companions:** See [MVP_DECISION_BRIEF.md](MVP_DECISION_BRIEF.md) for the narrow-MVP recommendation and provider shortlist, and [../PRODUCT/EXECUTION_CONTRACT.md](../PRODUCT/EXECUTION_CONTRACT.md) for a proposed provider-neutral execution lifecycle and testable API contract. Neither document selects a provider or claims implementation/test completion. This master research scaffold remains incomplete. Gemini's pasted specification has not been verified as a canonical repository update.

## 1. Executive summary
Product hypothesis; strongest evidence for/against; recommendation; confidence; go/pivot/stop recommendation; key uncertainties.

## 2. Current truth and repository audit
| Claim/decision | Evidence status | Source | Consequence |
|---|---|---|---|

Use evidence labels: VERIFIED_PRIMARY_SOURCE, SECONDARY_SOURCE, INFERENCE, ASSUMPTION, UNVERIFIED, NEEDS_LIVE_TEST, NEEDS_OWNER_APPROVAL.

## 3. Users and validation
Segment hypotheses; jobs-to-be-done; phone-first failure moments; non-leading interview script; validation protocol; measurable pass/fail thresholds; disconfirming evidence and pivot criteria.

## 4. Competitors and substitutes
| Product/alternative | User | Execution location | Mobile UX | Languages | Files in/out | AI lock-in | Price/limits | Security evidence | Gap/weakness | Source/date/confidence |
|---|---|---|---|---|---|---|---|---|---|---|

Include mobile IDEs, local runtimes, hosted runners, cloud IDEs, remote agents, AI app builders, manual workarounds and naming risk.

## 5. Execution backend comparison
Screen at least three candidates; compare at least two deeply. Include isolation model, egress/network policy, lifecycle/cancel/timeout, resource/output limits, files, logs/streaming, cleanup, region/data handling, retention, quotas, cold starts, API maturity, portability, operator burden and failure behavior.

| Criterion | Weight | Candidate A | Candidate B | Candidate C | Evidence/caveats |
|---|---:|---|---|---|---|

### Cost model
Date/currency; run assumptions; best/expected/adverse scenarios; baseline charges; compute/storage/network; sensitivity; abuse/quota risks; source URLs and unresolved pricing terms.

### Provider-neutral adapter
Request/result schemas; job states; cancellation semantics; files; error mapping; retries/idempotency; limits; provider-specific degraded modes.

## 6. Product requirements and mobile UX
| Requirement ID | Requirement | Priority | Evidence/rationale | Acceptance criteria | Test IDs | Status |
|---|---|---|---|---|---|---|

Include screen behavior, keyboard/viewport, accessibility, uploads/downloads, latency, refresh/reconnection, retries and all terminal states.

## 7. Architecture and contracts
Compare at least two architectures; component responsibilities; trust boundaries; endpoints; schemas; auth/authorization; storage/retention; job scheduling; observability; deployment assumptions; portability/migrations; recommendation and counterargument. Keep proposals separate from accepted decisions.

## 8. Threat model and launch gates
| Threat ID | Threat | Preconditions | Impact | Control | Detection | Test/evidence | Residual risk |
|---|---|---|---|---|---|---|---|

Include malicious code, sandbox escape, SSRF/metadata, tenant crossover, resource exhaustion, secret exposure, malicious archives/path traversal, output injection, supply-chain attacks, network egress, abuse economics and deletion.

## 9. Test plan and traceability
| Test ID | Requirement IDs | Scenario | Expected observable behavior | Automated/manual | Evidence status |
|---|---|---|---|---|---|

Cover success, syntax/runtime errors, timeout, cancellation, output cap, file output, isolation, network restriction, cleanup, lost connection, provider outage and redaction.

## 10. Implementation plan
| Task ID | Status: READY / NEEDS_OWNER_DECISION / BLOCKED | Goal | Paths/modules | Dependencies | Acceptance criteria | Tests | Risks |
|---|---|---|---|---|---|---|---|

Provide a dependency-ordered minimal vertical slice, explicit definition of done, tasks possible without credentials, and owner-only approvals.

## 11. Marketing, naming and distribution
Positioning alternatives; evidence/counterevidence; low-cost ethical experiments; pass/fail thresholds; name validation checklist; distribution hypotheses; claims prohibited until functionality is verified.

## 12. Business and operations
Usage scenarios with assumptions; cost/abuse risks; reliability/support expectations; monetization hypotheses; evidence required before pricing decisions; go/no-go thresholds.

## 13. Risk register
| Risk ID | Description | Likelihood | Impact | Detection | Mitigation | Owner | Residual risk |
|---|---|---|---|---|---|---|---|

## 14. Decision recommendations, not yet accepted
| Decision ID | Question | Recommendation | Evidence | Counterargument | Confidence | Owner approval needed? |
|---|---|---|---|---|---|---|

## 15. Unresolved questions and blockers
Separate owner decisions, live tests, vendor/legal verification, and research gaps.

## 16. Skeptical review and revision log
Product, security, engineering, mobile UX, cost/operations review; issues found and fixed; remaining objections; ChatGPT review status; disposition of each ChatGPT comment.

## 17. Evidence register
| Source ID | Claim | Title | Direct URL | Quality/type | Date checked | Caveats |
|---|---|---|---|---|---|---|

## 18. Completion checklist
- [ ] Pass 0 repository/hypothesis audit
- [ ] Pass 1 all workstreams researched
- [ ] Pass 2 synthesis and falsification
- [ ] Pass 3 implementation-ready specifications
- [ ] Pass 4 cost and operations review
- [ ] Pass 5 skeptical self-review and corrections
- [ ] Pass 6 master artifact consolidated and verified
- [ ] Pass 7 ChatGPT review completed or explicitly pending
- [ ] All material claims sourced and dated
- [ ] No invented tests, interviews, benchmarks, pricing, or repo changes
- [ ] Owner decisions and paid-service gates explicit


## 19. Cross-project AI workflow efficiency and orchestration (2026-10-28)

A research master has been created in the RevDev repository and should be used as the shared reference, without merging repositories: [AI Workflow Efficiency and Cross-App Orchestration Master](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/AI_WORKFLOW_EFFICIENCY_AND_CROSS_APP_ORCHESTRATION_MASTER_2026-10-28.md).

It contains three research passes: (1) Ponytail's actual behavior policy, integration mechanisms and benchmark caveats; (2) comparison with Superpowers, Everything Claude Code, Claude Code, Gemini CLI, Codex/ChatGPT skills/plugins, Cursor rules/hooks, and PC/mobile inter-app boundaries; (3) a proposed provider-adaptive Work Coach, profiles, compact task packet, evaluation criteria and staged plan.

### PocketCode implications

- **Candidate feature:** AI Efficiency Coach & Handoff, helping a user create concise instructions, preserve important state, carry selected code/error/evidence between PocketCode and an arbitrary AI assistant, and prepare a targeted next-step prompt.
- **Universal path:** user-driven copy/share/paste. Do not require paid API access or native provider integration.
- **Optional future path:** host-specific skills/rules/hooks/MCP only where supported and reviewed. Direct UI automation, APIs, account linking and remote-PC control remain separate proposals requiring explicit review.
- **Free-mode promise:** maximize useful verified progress within actual account/feature limits; do not evade quota, imply hidden capabilities, or hardcode volatile provider limits. Use compact context, task-appropriate profiles, local checks, capped retries and checkpoints.
- **Safety boundary:** instructions/AI output cannot authorize execution. Preserve the independent remote runner security requirements and D-001 (separate repositories).

### Evidence status

Ponytail's own Claude Code benchmark is promising but single-host/model, small-run and partially based on size metrics; do not copy its percentages into PocketCode claims. Host integrations documented by a provider do not prove that the corresponding consumer mobile app exposes the same surface. No PocketCode AI integration, backend, app-to-app automation or model/API invocation was implemented or tested by this research.

This section updates the research plan, not an accepted product/architecture decision. The overall PocketCode master research plan remains incomplete until its other workstreams and evidence register are reviewed.
