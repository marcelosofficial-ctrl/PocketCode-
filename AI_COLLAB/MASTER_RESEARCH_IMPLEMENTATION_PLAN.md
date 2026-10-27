# PocketCode — Master Research and Implementation Plan

**Status:** Partial — ChatGPT Pass 0 audit plus Pass 1 provider, competitor, and illustrative cost subpasses drafted; Gemini's required research passes remain incomplete.  
**Created:** 2026-10-20.  
**Warning:** Sections 1–5, 8, 11, 12, and 15–17 contain initial repository-audit or partial provider/competitor-subpass content; other sections remain incomplete. This is not a completed research plan. User demand, all-workstream research, normalized cost, and live provider/security behavior remain unverified.

**Interim companions:** [MVP_DECISION_BRIEF.md](MVP_DECISION_BRIEF.md) contains the narrow-MVP recommendation; [PASS0_REPOSITORY_AUDIT.md](PASS0_REPOSITORY_AUDIT.md) records the repo baseline; [PASS1_PROVIDER_RESEARCH.md](PASS1_PROVIDER_RESEARCH.md), [PASS1_COMPETITOR_RESEARCH.md](PASS1_COMPETITOR_RESEARCH.md), and [PASS1_COST_MODEL.md](PASS1_COST_MODEL.md) contain partial dated evidence; [../PRODUCT/EXECUTION_CONTRACT.md](../PRODUCT/EXECUTION_CONTRACT.md) proposes a provider-neutral lifecycle/contract. These are not final decisions or implementation/test completion. The master plan remains incomplete. Gemini's pasted specification has not been verified as a canonical repository update.

## 1. Executive summary

**Evidence state:** ChatGPT's Pass 0 repository audit is recorded in [PASS0_REPOSITORY_AUDIT.md](PASS0_REPOSITORY_AUDIT.md). This is not Gemini's completed Pass 0, not external-web revalidation, and not customer validation.

**Product hypothesis:** A phone-first workflow lets a user bring code and small input files from any AI assistant, run one supported task in a disposable isolated environment, inspect genuine status/stdout/stderr/files, then paste a bounded report back to the assistant and rerun after a fix.

**What exists:** A static simulated mobile HTML prototype, source-level prototype checks and unit tests, and a pure Python report formatter/classifier. The report helper does not execute code. The repository has product/architecture/security/provider desk-research documents and a controlled-proof runbook.

**What does not exist or is not proven:** No real execution backend, selected provider/framework, authentication, end-to-end execution path, representative user validation, live isolation/egress/cancellation/cleanup proof, or verified operating-cost model. The current prototype's success/error states are fixed examples, not execution.

**Recommendation (not accepted as a final decision):** Keep the first technical proof narrow: a phone-browser/PWA candidate, one small Python task, optional text/CSV input, genuine bounded output and file evidence, and a copyable report. Do not require native mobile, Termux, SSH/Tailscale, local WASM, floating overlays, direct AI integrations, or a broad agentic control plane to prove the core hypothesis. Keep those as future options only if evidence justifies them.

**Confidence:** High on repository state; moderate that the narrow run→evidence→AI handoff loop is the clearest technical test; low on demand, differentiation, and sustainable economics. Public-source research is not representative demand evidence. The current competitor refresh strengthens the counterargument: the one-word PocketCode brand is already used by an Android IDE with local execution/AI, Derle markets a phone-native IDE with local execution/AI, Kodo covers iOS editing/preview/SSH, Codeg supervises host-side agents, and Codespaces provides cloud development from a browser. The product cannot differentiate on “coding from a phone” alone.

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

**Status:** hypotheses only; no representative user validation or task benchmark has been completed. Directional public anecdotes are logged in [RESEARCH/MOBILE_CODING_USER_EVIDENCE.md](../RESEARCH/MOBILE_CODING_USER_EVIDENCE.md); competitor counterevidence and the fixed-task comparison are in [PASS1_COMPETITOR_RESEARCH.md](PASS1_COMPETITOR_RESEARCH.md).

| Segment hypothesis | Job-to-be-done | Current evidence | Strongest counterargument | Cheap falsification step |
|---|---|---|---|---|
| A. Quick-run verifier | “I have an AI-generated script and small input file on my phone; help me check the actual result without setting up a full IDE/server.” | Existing public anecdotes mention phone Python, mobile editing friction, and debugging context loss; official competitors confirm this is technically possible | Free local IDEs (existing PocketCode, Derle) and Codespaces may already solve it; no evidence of enough frequency or willingness to pay | Compare one fixed Python+CSV task across local IDE, Codespaces, Kodo+SSH, Codeg and proposed flow; measure setup steps, time-to-result, report usefulness and failure recovery |
| B. Learner/hobbyist | “Help me learn/debug small scripts and understand errors from my phone.” | Public anecdotal reports of mobile Python use and frustration; no representative sample | Local tools are free and may teach more; support needs and low willingness to pay may undermine hosted economics | Review public learner workflows and existing apps; ask non-leading questions about the last actual failed run |
| C. Professional away from workstation | “Let me supervise a repo-wide agent or long-running task from a phone.” | Codeg and Codespaces already address remote continuation | This is a broader persistent-workspace/agent product with more auth, state, cost and security complexity than the narrow MVP | Defer unless target users explicitly name this as the unmet job |

**Provisional recommendation:** test segment A first because it is the smallest technical hypothesis, not because it is proven to be the largest market.

### Validation protocol (not yet run)

1. Ask about the last real instance of trying to run AI-generated code from a phone, not whether the person likes the idea.
2. Record device/OS, code source, input files, runtime, current workaround, setup steps, time-to-result, error handling, and what they copied back to the AI.
3. Compare the same small Python+CSV task in existing tools using public documentation/screenshots first; hands-on tests require the relevant accounts and approvals.
4. Define thresholds before collecting results. Do not invent a numeric pass threshold until the task and target audience are specified.
5. Pivot/stop if the same task is already easy in a free local IDE/Codespaces, if users need persistent full IDE features, or if safe hosted execution cannot fit the approved budget.

**No interviews, controlled usability study, or task benchmark is claimed complete.**

## 4. Competitors and substitutes

Current official-source refresh: [PASS1_COMPETITOR_RESEARCH.md](PASS1_COMPETITOR_RESEARCH.md), checked 2026-10-26. This is a targeted desk-research subpass, not a hands-on or representative market study.

| Product/alternative | User | Execution location | Mobile UX | Languages / files | AI lock-in | Price/limits | Security evidence | Gap/weakness to test | Source/date/confidence |
|---|---|---|---|---|---|---|---|---|---|
| PocketCode (one word, existing Android IDE) | Android developers wanting a full phone IDE | On-device runtimes; terminal/SSH also available | Android 9+, 64-bit; editor, terminal, Git, API/database tools | Official site lists Python/Node/Ruby/PHP/Java/Kotlin and more; broad local toolchain | BYOK/multiple AI providers | Free tier (one project); Pro advertised at $6.99/month | No independent security test in this pass | Exact-name collision; how much extra value does a hosted disposable runner add over local execution? | Official [site](https://www.pocketcodeapp.com/en), [about](https://www.pocketcodeapp.com/en/about); 2026-10-26; official claims, not hands-on verified |
| Derle | Phone-first users who want local IDE/terminal/AI | On-device Linux/toolchains; site describes Android PRoot and iOS ARM64 emulator | Markets Android and iPhone experiences; public iOS distribution status needs confirmation | Local Python/Node/compilers and project builds claimed; files/Git/previews | Built-in models and BYOK options | Free tier; optional Pro, exact current pricing not assessed | No independent security test in this pass | Local execution is already possible; verify iOS availability and test real constraints | Official [site](https://derle.app/); 2026-10-26; marketing claims |
| Kodo | iPhone/iPad users needing a light editor and remote access | Local HTML/CSS/JS preview; SSH runs other languages on user-owned server | iOS/iPadOS 18+, free/no account according to site | Local web preview; says Python/PHP/Swift are not run locally; SSH/SFTP/FTP/GitHub/SQLite | Optional on-device AI | Free/no subscription according to current site | No independent security test in this pass | A simple Python run without configuring a personal server may be a gap | Official [site](https://www.kodoeditor.com/); 2026-10-26; no app test |
| Codeg | Users supervising coding agents from a phone | User-owned desktop or server hosts projects/agents | Native iOS/Android clients; current mobile releases are described as test releases | Host retains files, CLIs and sessions; mobile streams output/approvals | Multi-agent coding workspace; host-owned | Current price not assessed | Authenticated host/server architecture described; no independent test | Requires a separate host/server; may be too complex for a one-shot run | Official [installation](https://docs.codeg.app/getting-started/installation), [architecture](https://docs.codeg.app/reference/architecture); 2026-10-26 |
| GitHub Codespaces | GitHub users needing a cloud development environment | Hosted cloud VM | Browser access from any internet-connected device; setup uses repo/devcontainer workflow | Full development environment and repository files | Optional GitHub ecosystem integrations | Personal Free quota: 120 compute hours and 15 GB-month storage; over-quota use blocks without payment method or is billed with one | GitHub describes isolated environments/access/cost controls; this is not a PocketCode security test | Full IDE is capable but may be more setup/complexity than a single supported run; mobile usability needs task testing | Official [product page](https://github.com/features/codespaces), [billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces); 2026-10-26 |
| Manual browser + terminal/copy-paste workflow | Users who already have access to a cloud IDE, shell or phone-local runtime | Depends on existing tool | No extra app or account beyond the chosen tools | Flexible but fragmented | None required | Existing quotas/costs vary | Depends on underlying environment | May already solve the user's problem; compare time-to-first-run and evidence quality | INFERENCE; needs task-based comparison |

The main differentiator hypothesis to falsify is not “coding from a phone.” It is a lower-friction, cross-platform, disposable run with trustworthy bounded evidence and a clean AI handoff, without installing a full IDE or configuring a server. The current product still needs to prove that users prefer this narrow flow over the alternatives above.

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

See [PASS1_COST_MODEL.md](PASS1_COST_MODEL.md) for a dated, illustrative 60-second run and 1,000-run calculation. Under the stated assumptions, variable CPU/memory is approximately $0.00111 per 60-second run for the illustrative Daytona and E2B configurations, $0.0015828 active-only for Modal Sandbox+Notebooks (potentially $0.0031656 if a full 60-second idle tail is billed), and within Cloudflare's included resource quotas for one standard-2 run—but Cloudflare still requires the $5/month Workers Paid base plan. These are not comparable performance tests or all-in estimates.

Normalize one request by CPU/vCPU, memory, provisioned disk/storage, startup time, active execution time, post-input idle tail, network egress, request/API charges, logs, concurrency, included credits, monthly base fees, and abuse scenarios. Include best/expected/adverse scenarios with date, currency, source, and sensitivity. Do not treat a free allowance as a guaranteed $0 ceiling. Current pricing pages and terms are snapshots checked 2026-10-26; recheck before a decision. No live workload is authorized under the current $0 budget.

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

**Current status:** no final name or validated positioning. See [PASS1_COMPETITOR_RESEARCH.md](PASS1_COMPETITOR_RESEARCH.md).

- Do not position “code from your phone” as unique: current competitors explicitly claim local code execution, mobile AI assistance, remote-agent supervision, or browser-hosted cloud development.
- The strongest testable positioning hypothesis is “run a small supported task from an AI-generated snippet without setting up an IDE/server; get a truthful, bounded report that can be pasted back into any AI assistant.” This is an INFERENCE, not validated demand.
- **Name risk: high priority.** An existing one-word PocketCode Android IDE directly overlaps the developer-tool category and uses the exact spelling. The Catrobat “Pocket Code” name adds adjacent-category confusion. Keep the name provisional; do not invest in domain, logo, or launch assets before a distinct-name shortlist and formal trademark/domain review.
- Low-cost next experiment: compare one fixed Python+CSV task across existing PocketCode, Derle, Kodo+SSH, Codeg, Codespaces, and a manual workflow using public docs/screenshots first. Record setup steps, time-to-first-run, file handling, error/report quality, mobile friction, cost/limits, and required hardware/server.
- Pass/fail criteria must be set before interpreting results: if a free local IDE or Codespaces completes the same task with similar friction, or target users prefer a full persistent IDE, pivot the product hypothesis rather than adding features.
- Do not claim real execution, sandbox isolation, speed, affordability, security, or user demand until implemented/tested/evidenced. No interview or benchmark claim is supported by this desk pass.

## 12. Business and operations

Current cost gate: do not claim a free hosted runner. See [PASS1_COST_MODEL.md](PASS1_COST_MODEL.md) for explicit illustrative assumptions and exclusions. Modal's Starter page advertises included compute but is pay-as-you-go beyond included usage and its default idle tail can be billable; Daytona advertises free compute but tier requirements affect network policy and higher tiers require top-ups; Cloudflare Containers requires the $5/month Workers Paid plan plus component usage; E2B pricing includes per-second usage and paid plan tiers, and testing requires prior written consent. See [PASS1_PROVIDER_RESEARCH.md](PASS1_PROVIDER_RESEARCH.md).

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
| COMP-PCODE-01 | Existing one-word PocketCode Android IDE with on-device runtimes and AI BYOK | PocketCode official site/about | https://www.pocketcodeapp.com/en | Official product pages | 2026-10-26 | Direct naming collision; claims not independently tested |
| COMP-DERLE-01 | Phone-native IDE with local execution, terminal, Git, previews and AI | Derle official site | https://derle.app/ | Official product page | 2026-10-26 | iOS distribution status and real behavior need confirmation |
| COMP-KODO-01 | iOS/iPadOS editor with local web preview and SSH-based remote execution | Kodo official site | https://www.kodoeditor.com/ | Official product page | 2026-10-26 | Python is not claimed to run locally; no app test |
| COMP-CODEG-01 | Mobile clients supervise agents on a user-owned desktop/server | Codeg installation/architecture docs | https://docs.codeg.app/getting-started/installation | Official technical docs | 2026-10-26 | Current mobile releases described as test releases |
| COMP-CODESPACES-01 | Cloud development from any internet-connected device; included personal quotas and paid overage | GitHub Codespaces product/billing | https://github.com/features/codespaces | Official product/billing docs | 2026-10-26 | Phone UX and exact workflow friction not tested |

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


### 2026-10-26 — Pass 1 competitor/substitute subpass (ChatGPT, workstream B only)

- Added [PASS1_COMPETITOR_RESEARCH.md](PASS1_COMPETITOR_RESEARCH.md) using current official product pages for PocketCode, Derle, Kodo, Codeg, and GitHub Codespaces.
- Strong counterevidence: the exact one-word PocketCode brand is already used by an Android IDE with local runtimes and multi-provider AI; Derle markets local execution and AI on phone; Kodo covers iOS editing/preview/SSH; Codeg supervises host-side agents; Codespaces provides browser-based cloud development. “Code from a phone” is not a differentiator.
- Current differentiation hypothesis to falsify: a no-setup, cross-platform disposable run with trustworthy bounded output/files and a clean report-to-any-AI handoff. No hands-on comparison or customer validation was performed.
- High-priority naming risk; do not invest in final branding before a distinct-name and formal trademark/domain review. No final name recommendation or legal conclusion is made.
- This is ChatGPT's partial subpass, not Gemini completing workstream B or Pass 1. Remaining A–H research remains open.


### 2026-10-26 — Pass 1 illustrative cost-model subpass (ChatGPT)

- Added [PASS1_COST_MODEL.md](PASS1_COST_MODEL.md) with explicit 60-second and 1,000-run arithmetic using current official pricing pages for Modal Sandbox+Notebooks, Daytona, E2B, and Cloudflare Containers.
- The calculations are lower-bound illustrations, not a fair performance comparison or an all-in cost estimate. Modal's idle tail, Daytona's tier-dependent network policy, Cloudflare's $5/month Workers Paid base and additional components, and E2B's testing-consent requirement are material.
- No provider is “safe and free” on the strength of a free allowance. Under the strict $0 constraint, no live provider test is authorized; no accounts/workloads were created.
- This is ChatGPT's partial cost research, not Gemini completing workstream H or Pass 1. A–H research and the normalized best/expected/adverse model remain incomplete.

### 2026-10-27 — Pass 1 public user/problem evidence subpass (ChatGPT)

- Added [PASS1_USER_PROBLEM_EVIDENCE.md](PASS1_USER_PROBLEM_EVIDENCE.md) using public Reddit discussions as directional anecdotes, with source dates, limitations, counterevidence, segment hypotheses, and a zero-cost task-based validation protocol.
- Mixed signal: some people use phones for quick Python/CSV tasks or because they lack a computer; others report touch/screen friction, setup/package limitations, or prefer local tools/remote desktops. These discussions cannot estimate prevalence, retention, willingness to pay, or product-market fit.
- Proposed segment A remains a test-first choice only: people who recently wanted to verify a short AI-generated Python script plus small text/CSV input from a phone. Local IDEs and existing remote workflows are explicit counter-hypotheses.
- Added a fixed-task comparison, behavior-based interview prompts, observable metrics, and exploratory stop/re-scope/continue rules. This is a proposed protocol, not executed research; no interviews, app installs, benchmark, account creation, provider workload, or spend occurred.
- Product implication: do not expand into agent orchestration or native-app complexity until this narrow task is shown to be frequent and underserved. No provider/name/architecture decision was made; budget remains $0.

### 2026-10-27 — Pass 1 execution security/abuse subpass (ChatGPT, workstream D)

- Added [PASS1_SECURITY_ABUSE_RESEARCH.md](PASS1_SECURITY_ABUSE_RESEARCH.md), a provider-neutral threat model and minimum acceptance-test matrix grounded in current Docker and OWASP guidance.
- Critical boundary: containers, unit tests, and vendor security statements alone do not prove hostile-code isolation. The first proof needs fresh per-job isolation, enforceable default-deny egress/metadata protection, hard CPU/memory/process/disk/time/output limits, safe artifact handling, tenant-aware quotas, cancellation, cleanup, and authoritative lifecycle evidence.
- Narrow initial scope excludes arbitrary packages, network, secrets, persistent jobs, public job ports, and repo-wide agents. If a zero-payment provider tier cannot enforce the mandatory controls, it is not eligible for the proof.
- Added adversarial acceptance tests for timeout, resource exhaustion, egress/metadata, cross-job access, traversal, output truncation, false PASS, cancellation/cleanup, queue abuse, unsafe rendering, and secret exposure.
- No provider selected, no live execution or security test, no accounts/workloads, no spend, and no security claim upgraded. $0 gate remains binding.

### 2026-10-27 — Runtime/provider feasibility gate (ChatGPT, workstream D/E)

- Added [PASS1_RUNTIME_PROVIDER_GATE.md](PASS1_RUNTIME_PROVIDER_GATE.md) and clarified [PASS1_PROVIDER_RESEARCH.md](PASS1_PROVIDER_RESEARCH.md) with current plan/version nuances.
- No candidate is approved for live testing under the strict $0 constraint. Cloudflare Containers has the clearest paper fit in current docs (per-sandbox Firecracker microVM, internet disabled by default) but requires Workers Paid at $5/month, so it is not currently eligible. Daytona v2 network restrictions are tier-sensitive and its v2 page is marked alpha; do not conflate it with v0 behavior. Modal credits are not a hard spending cap. E2B testing requires prior written consent per its security documentation.
- Added provider-neutral adapter requirements for job isolation, confirmed network policy, hard limits, lifecycle/cleanup, authoritative outputs, tenant authorization, spend controls, and retention.
- Implementation should expose capability states (supported / unsupported / not_verified / blocked_by_plan) and fail closed rather than silently weakening security. Fake adapters may validate orchestration only, not sandbox isolation.
- No provider selected, no account/workload/live test/spend, no architecture claim upgraded. $0 gate remains binding.

### 2026-10-27 — Draft provider-neutral execution contract

- Added [DRAFT_EXECUTION_CONTRACT.md](DRAFT_EXECUTION_CONTRACT.md): request validation, state machine, provider adapter seam, report trust model, offline test matrix, and unresolved product/security choices.
- This is a proposal only. Initial size/time values are placeholders, not approved production limits or API commitments.
- Core invariant: client-supplied status is never execution evidence; provider-confirmed policy, observed execution, cleanup, and formatter output remain distinct. Missing or contradictory evidence cannot produce PASS.
- Capability states distinguish supported, unsupported, not_verified, and blocked_by_plan. Any mandatory control not verified blocks execution; no silent security downgrade.
- Offline fake-adapter tests may validate orchestration/report behavior only. They cannot prove real isolation, egress blocking, cleanup, tenant isolation, or billing.
- No production implementation/provider SDK, account, workload, test, spend, or provider selection.


### 2026-10-27 — Evidence and decision register (ChatGPT)

- Added [DECISION_REGISTER.md](DECISION_REGISTER.md) to separate evidence-supported facts, hypotheses, unknowns, reversible decisions, approval gates, and research priorities.
- Prioritized offline work first: contract coherence, source/link integrity, threat-to-test traceability, and cross-document state consistency. User interviews and task comparison remain unperformed; provider proof remains blocked by the strict $0 gate and mandatory security requirements.
- Explicit no-go list covers provider accounts/credentials, billing changes/spend, live execution, tests requiring consent, security downgrades, merge/deployment, public claims, and rename without owner approval.
- This is a decision-control document, not product validation or approval to implement. Gemini completion remains unverified/pending.


### 2026-10-27 — Draft contract coherence audit (ChatGPT, static review only)

- Added [CONTRACT_COHERENCE_AUDIT.md](CONTRACT_COHERENCE_AUDIT.md) mapping ten ambiguities to proposed resolutions and offline tests.
- Highest-risk edge cases: execution success with cleanup failure; late completion racing timeout/cancel; missing or contradictory provider-policy evidence; placeholder limits confused with enforceable controls; stale capability declarations; tenant authorization across every operation; and report formatting that could falsely elevate status.
- Proposed invariant: preserve execution outcome separately from overall service disposition; overall PASS requires confirmed mandatory policy, authoritative completion, exit 0, no limit/timeout/cancel/output truncation, valid artifacts, and cleanup success. Exact status vocabulary remains a design decision.
- Static review only. No tests executed, no provider tested, no production API frozen, and no implementation/spend authorized.


### 2026-10-27 — Scoped Gemini independent-review handoff (ChatGPT)

- Added [GEMINI_REVIEW_REQUEST.md](GEMINI_REVIEW_REQUEST.md), a compact, evidence-first review request covering cross-document contradictions, critical security cases, test coverage, provider source/version claims, product falsification, and approval gates.
- It explicitly requires Gemini to distinguish inspected evidence from assumptions, tests actually run from proposed tests, and blockers from offline work. It prohibits provider accounts/workloads/spend/merge/deployment and asks for a copyable review rather than repository changes.
- This is a prepared handoff only. Gemini has not been confirmed to have received or completed it.


### 2026-10-27 — Lifecycle and artifact-policy proposal

- Added [PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md](PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md) to make the next offline design increment concrete: append-only execution evidence and derived disposition; deterministic race/idempotency semantics; conservative artifact quarantine through cleanup; integrity-checked manifests; bounded output/redaction; and separate observed telemetry from estimated/unavailable cost.
- Updated [OFFLINE_ACCEPTANCE_TEST_MATRIX.md](OFFLINE_ACCEPTANCE_TEST_MATRIX.md) with corresponding proposed test IDs and [DECISION_REGISTER.md](DECISION_REGISTER.md) with the remaining owner decisions.
- This is a design proposal, not API freeze or implementation authorization. The key open owner decisions are artifact release after cleanup failure, event reconciliation, idempotency retention/canonical fingerprint, and stream overflow behavior.
- No code/tests executed; no provider selected or tested; strict $0 gate remains. User validation and Gemini's full Pass 0–7 remain incomplete.
- Current PR #3 head should be checked live rather than inferred from older checkpoint SHAs. Keep PR #3 draft/unmerged and PR #2 untouched.


### 2026-10-27 — Race determinism and link audit

- Refined the lifecycle proposal after identifying that compare-and-set alone guarantees a single winner, not a repeatable winner across concurrent timeout/cancel permutations. The proposal now requires a monotonic coordinator-ingress sequence or an explicit precedence rule; tests must distinguish single-winner safety from replay determinism.
- Updated the acceptance matrix with RACE-SEM-04 and corrected literal newline escapes that were rendering as backslash-n text.
- Ran a focused internal Markdown-link audit across 12 current research/contract documents against the live branch tree: 0 missing relative file targets and 0 broken anchors among the inspected documents. This is a focused audit, not a guarantee for every file or external URL.
- Current next step: complete the remaining owner decision packet and static consistency pass. Offline tests remain NOT RUN until expected semantics are approved; no provider-dependent test is authorized.


### 2026-10-27 — Owner decision packet

- Prepared [PASS1_OWNER_DECISION_PACKET_20261027.md](PASS1_OWNER_DECISION_PACKET_20261027.md) with explicit recommendations, trade-offs, and pending approval fields for artifact quarantine, event ordering, idempotency retention, output overflow, canonical request fingerprints, and outcome/disposition separation.
- This packet is a review aid, not authorization or a recorded decision. Do not freeze the schema or implement lifecycle tests until the expected outcomes are agreed.
- Next: owner review, then a single coordinated contract/matrix update and pure offline test implementation. Strict $0 and provider-consent gates remain unchanged.
