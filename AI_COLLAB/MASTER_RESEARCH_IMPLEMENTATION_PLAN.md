# PocketCode — Master Research and Implementation Plan

**Status:** Scaffold only; Gemini research is not yet complete.  
**Created:** 2026-10-20.  
**Warning:** Do not treat this document as evidence or a completed plan until sections are populated with sourced findings and reviewed.

**Interim companion:** See [AI_COLLAB/MVP_DECISION_BRIEF.md](MVP_DECISION_BRIEF.md) for ChatGPT's current narrow-MVP recommendation and an official-documentation shortlist of execution providers. This companion is not a provider selection, and this master research scaffold remains incomplete. Gemini's pasted specification has not been verified as a canonical repository update.

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
