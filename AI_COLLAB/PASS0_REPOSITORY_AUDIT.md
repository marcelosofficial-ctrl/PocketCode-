# PocketCode Pass 0 — Repository and Product-Hypothesis Audit

**Audit ID:** PC-PASS0-2026-10-26-CHATGPT-01  
**Date:** 2026-10-26  
**Repository:** https://github.com/marcelosofficial-ctrl/PocketCode-  
**Inspected ref:** `main` (PR #2 base SHA: `555840d8d83342513d9cd353d4d1522d46a5c82d`)  
**Purpose:** Establish the repository's actual baseline, identify contradictions/gaps, and plan evidence gathering.  
**Scope:** Repository desk audit only. This is ChatGPT's parallel audit, **not** Gemini completing its required Pass 0, and not a current external-web/vendor revalidation.

## 1. Executive finding

PocketCode is still at discovery/product-definition stage. The core hypothesis is a phone-first loop: bring code and small input files from any AI assistant, run one supported task in a disposable isolated environment, inspect genuine status/output/errors/files, then paste a bounded report back into the AI assistant and rerun after a fix.

The repository has a static simulated mobile HTML prototype, a dependency-free prototype source checker with unit tests, and a pure Python report formatter/classifier with unit tests. It does **not** contain a real execution backend, selected provider, approved framework, authentication system, or demonstrated end-to-end execution path. No customer interviews or live provider/security proof are recorded as completed.

**Recommendation (not an accepted decision):** keep the first proof narrow and mobile-browser-first, with one small Python run and optional text/CSV input. Treat PWA as a candidate, not a decision. Keep the expanded “agentic orchestration control plane” concept, native app, Termux, SSH/Tailscale, and local WASM as future options rather than MVP prerequisites. Do not select a provider or run live workloads until current primary-source research, the isolation/egress/cancellation proof plan, and explicit owner approval are complete.

**Confidence:** high on repository state; moderate on the smallest technical proof being the clearest test; low on user demand, differentiation, and sustainable unit economics because there is no representative user validation or live cost/latency evidence.

## 2. Evidence register — repository baseline

Evidence labels: `VERIFIED_PRIMARY_SOURCE` means the repository artifact itself directly establishes what is currently recorded; it does not imply external claims in that artifact are independently verified. `INFERENCE` and `UNVERIFIED` are explicitly not facts.

| Claim | Evidence label | Repository source / inspected blob | Consequence |
|---|---|---|---|
| Project phase is discovery/product definition | VERIFIED_PRIMARY_SOURCE | [PROJECT_STATUS.md](../PROJECT_STATUS.md), `68b603302130796f7d22cddde9c16e803ccf8a93` | Avoid implying a production product exists |
| First-use workflow is a proposed phone-browser Python run with optional text/CSV input, real output/error/file evidence, and AI handoff | VERIFIED_PRIMARY_SOURCE | [PRODUCT/FIRST_RUN_WORKFLOW.md](../PRODUCT/FIRST_RUN_WORKFLOW.md), `213fc452c1af824c130c46fc5ef397287eca7253` | Use as testable hypothesis, not validated demand |
| Product spec remains draft; target users and scope decisions remain open | VERIFIED_PRIMARY_SOURCE | [PRODUCT_SPEC.md](../PRODUCT_SPEC.md), `f1e4149c15df55e338829170ed6bcb6cb70d7d28` | Do not treat acceptance criteria as proven |
| Architecture is conceptual; no stack/provider selected | VERIFIED_PRIMARY_SOURCE | [ARCHITECTURE.md](../ARCHITECTURE.md), `e66365db6433e62281fd6580018ba47cbf83197e` | No implementation or vendor commitment is justified yet |
| Security requirements call for disposable isolation, server-side limits, default-deny egress, secret separation, cleanup, and explicit retention/deletion | VERIFIED_PRIMARY_SOURCE | [SECURITY.md](../SECURITY.md), `e4009c48bd474b1106e253ea25f1f2fb769f3d7a`; [PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md](../PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md), `68e7615d0ae36f1d3adce4feb0c3ba302e126a2f` | Security controls need proof, not just provider claims |
| Existing mobile prototype is simulated; it does not execute submitted code | VERIFIED_PRIMARY_SOURCE | [prototype source](../prototypes/mobile-runner/index.html), blob `e2c4ece041be95ce9a73bc60ff354702b21c33c2`; [source checker](../scripts/check_mobile_prototype.py), `c745668f4abcc9c164c6d846ecb661a625e8d4d5` | Keep all marketing/UI copy explicit that results are samples |
| Report formatter/classifier is not a runner or trusted source of execution evidence | VERIFIED_PRIMARY_SOURCE | [scripts/report_contract.py](../scripts/report_contract.py), current PR branch work; helper's module contract is explicit | Future runner must provide authoritative lifecycle evidence |
| Zero-dollar budget and owner approval gates are explicit | VERIFIED_PRIMARY_SOURCE | [PRODUCT/ZERO_BUDGET_WORK_PLAN.md](../PRODUCT/ZERO_BUDGET_WORK_PLAN.md), `248568bed9b6aa0b5810b16d456f09f56d0086dc`; [DECISIONS.md](../DECISIONS.md), `53734417085475efefc15d92854eaee8d5b7e91e` | Continue with public desk research and local/static tests; no provider workload |
| Provider research lists E2B, Modal, Daytona, Cloudflare, Judge0 CE, and Piston, but labels itself desk research and selects no vendor | VERIFIED_PRIMARY_SOURCE | [RESEARCH/EXECUTION_PROVIDER_RESEARCH.md](../RESEARCH/EXECUTION_PROVIDER_RESEARCH.md), `d55f051c0a8265c86bb6a35bd47ad029d0be6a50` | Refresh official facts and compare actual control semantics before a decision |
| MVP brief calls Modal a leading proof candidate, not an approved selection; Cloudflare is an alternative | VERIFIED_PRIMARY_SOURCE | [AI_COLLAB/MVP_DECISION_BRIEF.md](MVP_DECISION_BRIEF.md), `1ef5e781a067b7053fd72bdc7b18b68e552d71e6` | Preserve shortlist only; do not treat candidate status as approval |
| Competitive analysis and user-evidence notes are initial public-source research, not representative user validation | VERIFIED_PRIMARY_SOURCE | [RESEARCH/COMPETITIVE_ANALYSIS.md](../RESEARCH/COMPETITIVE_ANALYSIS.md), `840ece569e66368a57c5f25eafeb8246b70642d3`; [RESEARCH/MOBILE_CODING_USER_EVIDENCE.md](../RESEARCH/MOBILE_CODING_USER_EVIDENCE.md), `d772225fd297785d5690cfc9e352de82aa8bed9a` | Validate recency and avoid broad market claims |
| A prior review of a pasted “agentic orchestration” architecture recommended keeping it out of MVP scope; pasted spec was not verified as a repo change | VERIFIED_PRIMARY_SOURCE about review status; underlying design claims UNVERIFIED | [AI_COLLAB/CHATGPT_REVIEW_OF_GEMINI_PLAN.md](CHATGPT_REVIEW_OF_GEMINI_PLAN.md), `c461fb03014886d369a23d6ef7ec3a38d7becdb3` | Keep remote-agent control plane, SSH/Tailscale, Termux, native app, and WASM as optional future hypotheses |
| Gemini's research passes are recorded as not yet executed | VERIFIED_PRIMARY_SOURCE | [AI_COLLAB/GEMINI_PROGRESS_LOG.md](GEMINI_PROGRESS_LOG.md), `3554ae5c77a0beba57d469ecb579dda69a08cbf6` | Do not imply the cross-agent research/review loop is complete |
| Master plan is still a scaffold, with empty research matrices and completion checklist | VERIFIED_PRIMARY_SOURCE | [AI_COLLAB/MASTER_RESEARCH_IMPLEMENTATION_PLAN.md](MASTER_RESEARCH_IMPLEMENTATION_PLAN.md), `a1058d7a5cc4407289407953e82804bd7b2410a3` | Fill it incrementally with sourced findings, not invented conclusions |

## 3. Contradictions, stale points, and scope hazards

1. **Recommendation versus decision:** `PROJECT_STATUS.md` says Modal is the leading candidate for evaluation; the provider research, MVP brief, and controlled runbook all say no provider is selected and live proof is not approved. These can coexist if the wording consistently says “candidate for a future controlled proof,” never “chosen provider.”
2. **Prototype versus promise:** the product concept depends on genuine execution evidence, but the current HTML only switches between fixed success/error examples. No copy, screenshot, or marketing claim may present those examples as actual execution.
3. **Architecture expansion risk:** the pasted agentic-control-plane proposal adds native-app, remote-host, SSH/Tailscale, local runtime, overlay/keyboard, and orchestration complexity before the basic hosted run loop is proven. Existing independent review recommends deferring those as optional future directions.
4. **Evidence freshness:** most competitor/provider documents are dated 2026-10-20. Pricing, plans, quotas, security controls, availability, and terms must be rechecked against current official sources before any provider decision. No prices are revalidated in this Pass 0.
5. **Demand/differentiation:** public posts and competitor pages support plausibility, not prevalence or willingness to pay. No user interviews or task-based competitive test are recorded as completed. The differentiator may be the low-friction evidence→AI handoff loop, but this is an INFERENCE to falsify.
6. **Naming:** the repository itself flags an existing similarly named Android coding product; name/trademark/domain clearance remains unverified.
7. **Budget and proof:** real execution, egress denial, termination, cleanup, and cost are impossible to prove from the simulated prototype or report formatter. The runbook requires owner approval before accounts, credentials, or provider workloads.
8. **Documentation quality:** `PRODUCT_SPEC.md` contains a duplicated “10. RevDev compatibility and shared-core direction” heading. Low priority; fix when editing that document, not as a reason to expand the current report-contract PR.
9. **Separate PR scope:** PR #2 is report-contract hardening and continuity documentation. Do not add product-research changes to that branch; use a separate branch for this audit/master-plan work.

## 4. Open questions grouped by evidence type

### Owner decisions (not requested in this audit)
- Is the initial target a beginner/hobbyist who needs a one-off run, or a developer who wants remote control of an existing environment?
- Should the first proof remain a disposable hosted Python run, or is a user-owned remote host an essential target?
- What, if anything, is the future spend ceiling? Until explicitly changed, it remains $0.
- Is a native app required for the long-term vision, or is a mobile web/PWA sufficient to validate the core loop?

### Research gaps
- Which exact phone-first failure moments are common enough to justify a separate product?
- What do current alternatives actually let users do on iOS/Android, with which files, dependencies, and network restrictions?
- Does the report→AI→fix→rerun loop materially outperform existing mobile IDEs, cloud IDEs, remote agents, or simply using a browser and copy/paste?
- What name/brand options are sufficiently distinct to investigate further?

### Live-test gates
- Real Python success, syntax error, runtime error, timeout, cancellation, output cap, file round-trip, isolation, network denial, cleanup, disconnect/retry, and cost/latency.
- Current provider billing, free allowance, account limits, data region/retention, and exact sandbox product/configuration.
- Browser behavior on iOS Safari and Android browsers.

### Legal/operational checks
- Name and trademark/domain review before investing in final identity.
- Data processing, retention/deletion, abuse response, and support burden before any public service.

## 5. Dependency-ordered workstream plan

| Order | Workstream | Next deliverable | Evidence gate |
|---:|---|---|---|
| 0 | Repository/hypothesis audit | This audit plus master-plan baseline update | ChatGPT audit completed; Gemini's required Pass 0 still pending |
| 1 | Current external evidence | Refresh official competitor/provider docs and pricing with date/source register | No vendor ranking based on stale memory |
| 2 | Falsification | Compare alternatives on the same user task; list strongest counterarguments and pivot criteria | Identify what would disprove the product hypothesis |
| 3 | User/problem validation | Non-leading questions and low-cost public-evidence protocol; interviews optional | No fabricated interview/demand claims |
| 4 | Technical proof specification | Provider-neutral run/result/error/file contract plus threat/acceptance matrix | Security and billing gates explicit |
| 5 | Cost/operations | Best/expected/adverse scenarios, quotas, abuse, cleanup, outage handling | No live spend without approval |
| 6 | Consolidation/review | Populate master plan, record ChatGPT comments and disposition | Gemini review/revision loop actually occurs |

## 6. Pass 0 disposition

- Repository facts are separated from product hypotheses and vendor claims.
- No provider/framework/name/business decision is accepted by this audit.
- No external web research, customer interview, benchmark, live execution, or security test was performed in Pass 0.
- The master plan may now record this audit as a ChatGPT contribution, but `AI_COLLAB/GEMINI_PROGRESS_LOG.md` must continue to say Gemini's own required passes have not yet happened.
- **Next:** update master-plan sections 1, 2, 15, and 16 from these findings; append this contribution to the progress log; then begin Pass 1 external research as a separate, evidence-cited stage.
