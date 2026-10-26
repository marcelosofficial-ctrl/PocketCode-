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

**Initial official-source refresh:** [PASS1_PROVIDER_RESEARCH.md](PASS1_PROVIDER_RESEARCH.md), checked 2026-10-26. This is a partial provider workstream, not a final ranking. Four candidates have been screened from current official pricing/security/network pages; exact API semantics, plan eligibility, retention, and real behavior remain unverified.

| Candidate | Current documented strengths | Cost / $0 risk | Main unresolved gate | Status |
|---|---|---|---|---|
| Modal Sandboxes | Python SDK documents `block_network=True`; CIDR allowlists and a beta domain allowlist; gVisor default and VM runtime option described | Starter advertises $30/month included compute but is pay-as-you-go; Sandbox+Notebooks rates differ from standard compute; default 60-second post-input idle tail is billable unless configured | Verify hard spend cap/plan, exact timeout/cancel/termination semantics, region/retention, and observed network denial | Candidate only |
| Daytona Sandboxes | Docs describe Firecracker microVMs and configurable network limits | $200 free compute advertised, but network controls and organization policy depend on tier; Tier 2 requires card plus $25 top-up; Tier 3/4 require larger top-ups | Confirm the no-payment tier can enforce required default-deny policy and verify the exact product version/plan | Candidate only |
| Cloudflare Containers / Sandboxes | Container internet is documented disabled by default; Worker-mediated outbound controls available; distinct Container vs Dynamic Worker modes | Containers require the $5/month Workers Paid plan and may add CPU, memory, disk, egress, Workers, Durable Objects, and logs costs | Define execution mode; verify current 1.0 API, lifecycle/termination, full cost, and per-job sandbox boundary | Candidate only |
| E2B Sandboxes | Docs describe one Firecracker microVM per sandbox | Per-second CPU/memory rates and plan/concurrency differences; Pro base and Enterprise minimum appear in current estimator; not a normalized estimate | Default egress, lifecycle, full cost, plan/retention, and written testing consent | Candidate only; no test without prior written consent |

The vendor pages describe their products; they do not prove PocketCode's security properties. No provider is selected. See [PASS1_PROVIDER_RESEARCH.md](PASS1_PROVIDER_RESEARCH.md) for current source links, values, caveats, and next checks.

### Cost model

Do not compare headline per-second prices directly. Normalize one request by CPU/vCPU, memory, provisioned disk/storage, startup time, active execution time, post-input idle tail, network egress, request/API charges, logs, concurrency, included credits, monthly base fees, and abuse scenarios. Include best/expected/adverse scenarios with date, currency, source, and sensitivity. Do not treat a free allowance as a guaranteed $0 ceiling. Current pricing pages and terms are snapshots checked 2026-10-26; recheck before a decision.

### Provider-neutral adapter

Request/result schemas; job states; cancellation semantics; files; error mapping; retries/idempotency; limits; provider-specific degraded modes. The adapter must keep lifecycle evidence authoritative, represent unknown outcomes as INCOMPLETE, avoid duplicate billable runs after uncertain retries, and expose network/timeout/resource policy as server-owned configuration rather than client-supplied arbitrary controls.

## 6. Product requirements and mobile UX
| Requirement ID | Requirement | Priority | Evidence/rationale | Acceptance criteria | Test IDs | Status |
|---|---|---|---|---|---|---|

Include screen behavior, keyboard/viewport, accessibility, uploads/downloads, latency, refresh/reconnection, retries and all terminal states.

## 7. Architecture and contracts
Compare at least two architectures; component responsibilities; trust boundaries; endpoints; schemas; auth/authorization; storage/retention; job scheduling; observability; deployment assumptions; portability/migrations; recommendation and counterargument. Keep proposals separate from accepted decisions.

## 8. Threat model and launch gates
| Threat ID | Threat | Preconditions | Impact | Control | Detection | Test/evidence | Residual risk |
|---|---|---|---|---|---|---|---|
| SEC-NET-001 | Untrusted code exfiltrates user data or probes internal/metadata addresses | Sandbox can reach public/internal network | Data loss, SSRF, credential exposure | Server-side default-deny egress; allowlist only when needed; no secrets in job environment | Provider audit/network logs and alerts | NEEDS_LIVE_TEST: outbound public, private, link-local/metadata, DNS, IPv4/IPv6 cases | Unknown until provider+plan+configuration are tested |
| SEC-TENANT-001 | Two jobs/users share a sandbox trust domain | Reused named sandbox, shared container, or snapshot | Cross-user file/process/credential access | One disposable sandbox per job or user; derive IDs server-side; never trust client sandbox names | Ownership and lifecycle logs | NEEDS_LIVE_TEST: attempt cross-job file/process/snapshot access | Vendor isolation docs are not PocketCode proof |
| SEC-OUTPUT-001 | Malicious output or generated files attack the app/browser or operator | Untrusted program emits HTML/URLs/archives/oversized files | XSS, path traversal, resource exhaustion, misleading reports | Render output as text; bounded output/file count/size; safe archive extraction; no execution of returned artifacts | Validation errors and bounded logs | Automated malformed-output, archive traversal, output-cap and browser-render tests | Requires implementation and browser tests |
| SEC-BILLING-001 | Runaway jobs or retries create unexpected cost | Weak deadlines, uncertain retries, free allowance overrun | Budget breach or abuse | Server-enforced wall-time/resource caps, idempotency, concurrency quotas, hard stop/approval gates | Usage and cost reconciliation | NEEDS_LIVE_TEST: timeout/cancel/retry/cleanup and cost observations | No provider test approved; budget remains $0 |

Initial official docs show different egress defaults: Modal outbound is open unless blocked/configured; Daytona policy depends on organization tier; Cloudflare Container internet is disabled by default but Dynamic Worker network access differs; E2B egress still needs further verification. These facts are in [PASS1_PROVIDER_RESEARCH.md](PASS1_PROVIDER_RESEARCH.md). Do not treat provider documentation as a verified control until the exact plan/configuration is tested.

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

Current cost gate: do not claim a free hosted runner. Modal's Starter page advertises included compute but is pay-as-you-go beyond included usage and its default idle tail can be billable; Daytona advertises free compute but tier requirements affect network policy and higher tiers require top-ups; Cloudflare Containers requires the $5/month Workers Paid plan plus component usage; E2B pricing includes per-second usage and paid plan tiers, and testing requires prior written consent. See [PASS1_PROVIDER_RESEARCH.md](PASS1_PROVIDER_RESEARCH.md).

Before pricing or a live proof, model one short run, repeat-use monthly patterns, and adverse/abuse scenarios using consistent runtime, CPU, memory, disk, startup/idle, egress, logs, concurrency, and plan assumptions. Include quotas, support, abuse response, retention/deletion, and provider outage behavior. The owner has not approved any spend; current budget is $0.

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
| PROV-MODAL-PRICE-01 | Sandbox-specific pricing and Starter credits/idle billing | Modal pricing | https://modal.com/pricing | Official pricing page | 2026-10-26 | Sandbox+Notebooks rate card differs from standard compute; pay-as-you-go can exceed included credits |
| PROV-MODAL-NET-01 | Outbound default and network-block/allowlist API | Modal Sandbox networking | https://modal.com/docs/guide/sandbox-networking | Official technical docs | 2026-10-26 | Outbound is open by default; domain allowlist is Beta; live behavior untested |
| PROV-DAYTONA-PRICE-01 | Resource rates, free compute, tier/top-up gates | Daytona pricing | https://www.daytona.io/pricing | Official pricing page | 2026-10-26 | Free allowance is not a $0 guarantee; normalize resource/time assumptions |
| PROV-DAYTONA-NET-01 | Tier-based egress restrictions and sandbox network controls | Daytona Network Limits | https://www.daytona.io/docs/en/network-limits/ | Official technical docs | 2026-10-26 | Policy depends on organization tier; exact zero-payment-tier behavior needs confirmation |
| PROV-CF-SEC-01 | Container vs Dynamic Worker network behavior and sandbox trust boundary | Cloudflare Sandbox security | https://developers.cloudflare.com/sandbox/concepts/security/ | Official technical docs | 2026-10-26 | Verify current SDK/mode; all processes in one Container share a trust domain |
| PROV-CF-PRICE-01 | Containers base plan, resource, egress and component charges | Cloudflare Containers pricing | https://developers.cloudflare.com/containers/platform/pricing/ | Official pricing page | 2026-10-26 | Requires Workers Paid plan; Workers, Durable Objects and logs add costs |
| PROV-E2B-SEC-01 | Per-sandbox microVM claims and testing-consent restriction | E2B security | https://e2b.dev/security | Official security page | 2026-10-26 | Written consent required before testing; vendor claims need review |
| PROV-E2B-PRICE-01 | Per-second resource pricing and plan/concurrency differences | E2B pricing | https://e2b.dev/pricing | Official pricing page | 2026-10-26 | Current estimator is not a normalized cost model; exact plan assumptions required |

## 18. Completion checklist
- [ ] Pass 0 repository/hypothesis audit (ChatGPT audit draft exists; Gemini's required Pass 0 still pending)
- [ ] Pass 1 all workstreams researched (ChatGPT has completed only a current-source provider subpass; A–H research remains incomplete)
- [ ] Pass 2 synthesis and falsification
- [ ] Pass 3 implementation-ready specifications
- [ ] Pass 4 cost and operations review
- [ ] Pass 5 skeptical self-review and corrections
- [ ] Pass 6 master artifact consolidated and verified
- [ ] Pass 7 ChatGPT review completed or explicitly pending
- [ ] All material claims sourced and dated
- [ ] No invented tests, interviews, benchmarks, pricing, or repo changes
- [ ] Owner decisions and paid-service gates explicit


### 2026-10-26 — Pass 1 provider-source subpass (ChatGPT, workstream C only)

- Added [PASS1_PROVIDER_RESEARCH.md](PASS1_PROVIDER_RESEARCH.md) using current official pricing/security/network docs for Modal, Daytona, Cloudflare Containers/Sandboxes, and E2B.
- Key finding: no provider can be called “safe and free” from marketing pages alone. Modal's outbound default is open but `block_network=True` is documented; Daytona's egress policy depends on organization tier; Cloudflare Container internet is disabled by default but its Workers Paid base plan is $5/month and Dynamic Worker behavior differs; E2B documents a per-sandbox microVM and requires prior written consent before testing.
- No provider selected, no account/workload created, no live security claim made, and no budget changed. Official pages were checked 2026-10-26; pricing is time-sensitive.
- This is ChatGPT's partial research, not Gemini completion. Pass 1 across workstreams A–H remains open.
