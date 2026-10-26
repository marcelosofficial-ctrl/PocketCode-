# PocketCode — Master Research and Implementation Plan

**Status:** Partial — ChatGPT Pass 0 repository audit drafted; Gemini's required research passes remain incomplete.  
**Created:** 2026-10-20.  
**Warning:** Only sections 1, 2, 15, and 16 have initial repository-audit content. This is not a completed research plan; external claims, current pricing, user demand, and provider/security behavior remain unverified until sourced and reviewed.

**Interim companions:** See [MVP_DECISION_BRIEF.md](MVP_DECISION_BRIEF.md) for the narrow-MVP recommendation and provider shortlist, and [../PRODUCT/EXECUTION_CONTRACT.md](../PRODUCT/EXECUTION_CONTRACT.md) for a proposed provider-neutral execution lifecycle and testable API contract. Neither document selects a provider or claims implementation/test completion. This master research scaffold remains incomplete. Gemini's pasted specification has not been verified as a canonical repository update.

## 1. Executive summary

**Evidence state:** ChatGPT's Pass 0 repository audit is recorded in [PASS0_REPOSITORY_AUDIT.md](PASS0_REPOSITORY_AUDIT.md). This is not Gemini's completed Pass 0, not external-web revalidation, and not customer validation.

**Product hypothesis:** A phone-first workflow lets a user bring code and small input files from any AI assistant, run one supported task in a disposable isolated environment, inspect genuine status/stdout/stderr/files, then paste a bounded report back to the assistant and rerun after a fix.

**What exists:** A static simulated mobile HTML prototype, source-level prototype checks and unit tests, and a pure Python report formatter/classifier. The report helper does not execute code. The repository has product/architecture/security/provider desk-research documents and a controlled-proof runbook.

**What does not exist or is not proven:** No real execution backend, selected provider/framework, authentication, end-to-end execution path, representative user validation, live isolation/egress/cancellation/cleanup proof, or verified operating-cost model. The current prototype's success/error states are fixed examples, not execution.

**Recommendation (not accepted as a final decision):** Keep the first technical proof narrow: a phone-browser/PWA candidate, one small Python task, optional text/CSV input, genuine bounded output and file evidence, and a copyable report. Do not require native mobile, Termux, SSH/Tailscale, local WASM, floating overlays, direct AI integrations, or a broad agentic control plane to prove the core hypothesis. Keep those as future options only if evidence justifies them.

**Confidence:** High on repository state; moderate that the narrow run→evidence→AI handoff loop is the clearest technical test; low on demand, differentiation, and sustainable economics. Public-source research is not representative demand evidence.

**Gate:** Continue $0 desk research and static work. No provider selection, account, credentials, live workload, billing, public runner, or deployment without explicit owner approval after current official-source and safety review.

## 2. Current truth and repository audit

The detailed baseline table, blob SHAs, contradictions, and next-workstream order are recorded in [PASS0_REPOSITORY_AUDIT.md](PASS0_REPOSITORY_AUDIT.md). This section is a concise index, not an independent vendor/source verification.

| Claim/decision | Evidence status | Source | Consequence |
|---|---|---|---|
| Project is in discovery/product definition; no production runner is present | VERIFIED_PRIMARY_SOURCE | [PROJECT_STATUS.md](../PROJECT_STATUS.md), [ARCHITECTURE.md](../ARCHITECTURE.md) | Do not describe a production app or real execution as existing |
| Core proposed loop is phone browser → small Python run → genuine output/errors/files → report to chosen AI → fix/rerun | VERIFIED_PRIMARY_SOURCE as documented proposal; demand UNVERIFIED | [PRODUCT_SPEC.md](../PRODUCT_SPEC.md), [PRODUCT/FIRST_RUN_WORKFLOW.md](../PRODUCT/FIRST_RUN_WORKFLOW.md) | Treat as hypothesis and acceptance-test candidate, not validated demand |
| Existing mobile prototype is simulated and never runs user code | VERIFIED_PRIMARY_SOURCE | [prototypes/mobile-runner/index.html](../prototypes/mobile-runner/index.html) | Preserve visible simulation disclaimers; no live-execution marketing claims |
| Report formatter/classifier is not a runner or trusted evidence source | VERIFIED_PRIMARY_SOURCE | [scripts/report_contract.py](../scripts/report_contract.py) | Future runner must supply authoritative lifecycle metadata |
| No framework/provider has been selected; Modal is only a candidate for a future controlled proof | VERIFIED_PRIMARY_SOURCE about current documented decision state | [ARCHITECTURE.md](../ARCHITECTURE.md), [AI_COLLAB/MVP_DECISION_BRIEF.md](MVP_DECISION_BRIEF.md), [PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md](../PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md) | Refresh primary sources and prove controls before a provider decision |
| Current research notes include competitor and provider desk research, mostly dated 2026-10-20 | VERIFIED_PRIMARY_SOURCE; underlying facts need freshness review | [RESEARCH/COMPETITIVE_ANALYSIS.md](../RESEARCH/COMPETITIVE_ANALYSIS.md), [RESEARCH/EXECUTION_PROVIDER_RESEARCH.md](../RESEARCH/EXECUTION_PROVIDER_RESEARCH.md) | Recheck current official availability, terms, security, pricing, quotas, and product behavior |
| No representative user interviews or live provider/security proof are recorded as completed | VERIFIED_PRIMARY_SOURCE about project records | [PROJECT_STATUS.md](../PROJECT_STATUS.md), [PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md](../PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md) | Keep demand and runtime claims unverified |
| $0 budget and owner approval gates remain binding | VERIFIED_PRIMARY_SOURCE | [PRODUCT/ZERO_BUDGET_WORK_PLAN.md](../PRODUCT/ZERO_BUDGET_WORK_PLAN.md), [DECISIONS.md](../DECISIONS.md) | Continue public desk research/static tests; no paid workload |
| An expanded agentic-control-plane proposal was reviewed from pasted text, not verified as a repository update; prior review recommends it remain outside MVP baseline | VERIFIED_PRIMARY_SOURCE about review status; underlying claims UNVERIFIED | [AI_COLLAB/CHATGPT_REVIEW_OF_GEMINI_PLAN.md](CHATGPT_REVIEW_OF_GEMINI_PLAN.md) | Treat native app, Termux, SSH/Tailscale, local WASM and overlay ideas as future options, not requirements |
| Gemini's research passes are not yet recorded as completed | VERIFIED_PRIMARY_SOURCE | [AI_COLLAB/GEMINI_PROGRESS_LOG.md](GEMINI_PROGRESS_LOG.md) | ChatGPT's audit must not be misreported as Gemini's research completion |

Use evidence labels: VERIFIED_PRIMARY_SOURCE, SECONDARY_SOURCE, INFERENCE, ASSUMPTION, UNVERIFIED, NEEDS_LIVE_TEST, NEEDS_OWNER_APPROVAL. “VERIFIED_PRIMARY_SOURCE” for repository facts only means the repo directly states the fact; it does not validate external claims repeated by that document.

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

See the detailed grouped register in [PASS0_REPOSITORY_AUDIT.md](PASS0_REPOSITORY_AUDIT.md). Highest priority:

- **Demand/differentiation — UNVERIFIED:** which phone-first failure moments occur often enough, and does report→AI→fix→rerun beat existing mobile IDEs, cloud IDEs, remote agents, or copy/paste workarounds?
- **Target user — NEEDS_RESEARCH:** beginner/hobbyist one-off execution versus experienced developer remote control are materially different jobs.
- **Provider/security — NEEDS_LIVE_TEST + NEEDS_OWNER_APPROVAL:** prove exact isolation mode, egress default-deny, server-side deadline, cancellation/termination, file boundaries, cleanup, retry/idempotency, and cost for one specific product/plan.
- **Current provider facts — NEEDS_CURRENT_PRIMARY_SOURCES:** refresh pricing, free allowances, quotas, availability, data region/retention, API semantics, and security docs before ranking vendors.
- **Budget — OWNER GATE:** remains $0. No account, credentials, billing, or live provider workload without explicit approval.
- **Naming/legal — UNVERIFIED:** the name has a same/adjacent-category collision risk; no trademark/domain clearance is implied.
- **Architecture scope — INFERENCE:** keep the agentic-control-plane/native/SSH/Tailscale/Termux/WASM direction outside the MVP until the narrow loop is proven.
- **Cross-agent completion — BLOCKED/PENDING:** ChatGPT Pass 0 audit is drafted; Gemini's required Pass 0–7 research/review loop remains incomplete.
- **Documentation hygiene:** `PRODUCT_SPEC.md` has a duplicate section 10 heading; low priority and separate from current report-contract PR.

## 16. Skeptical review and revision log

### 2026-10-26 — ChatGPT Pass 0 repository audit (initial)

- **Scope:** repository state, existing product/architecture/security/provider documents, zero-budget rules, prior review of the pasted agentic architecture proposal, and Gemini handoff/progress status.
- **Artifact:** [PASS0_REPOSITORY_AUDIT.md](PASS0_REPOSITORY_AUDIT.md).
- **Found/fixed in this plan:** replaced placeholder-only executive summary/repository audit and populated high-priority blockers with repository-backed evidence labels. No product/provider decision is accepted.
- **Main objection:** the core value proposition is plausible but unvalidated; a polished UI or provider comparison cannot establish demand. The current prototype is simulated, and the hardest product claim (safe, reliable, affordable real execution from a phone) has not been proven.
- **Architecture objection:** the expanded agentic-control-plane proposal risks adding native/remote-host/overlay/local-runtime complexity before the simplest workflow is validated. Existing independent review recommends a narrow browser-based proof first.
- **Security objection:** provider descriptions are not evidence of PocketCode's actual isolation/egress/cancellation/cleanup behavior; these require current docs and eventually controlled tests.
- **Cost objection:** provider pricing and free allowances are time-sensitive; no reliable unit-cost conclusion can be made from old desk research or illustrative arithmetic.
- **Status boundary:** this is a ChatGPT repository audit, not Gemini's required Pass 0 and not the full skeptical review of a completed master plan. Gemini's pasted specification is not treated as a canonical repo update. No external web refresh, interviews, benchmarks, live workload, or browser test was performed.
- **Next review:** after Pass 1 sources and a complete master plan exist, ChatGPT should review the actual artifact and record disposition for every comment.

## 17. Evidence register
| Source ID | Claim | Title | Direct URL | Quality/type | Date checked | Caveats |
|---|---|---|---|---|---|---|

## 18. Completion checklist
- [ ] Pass 0 repository/hypothesis audit (ChatGPT audit draft exists; Gemini's required Pass 0 still pending)
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
