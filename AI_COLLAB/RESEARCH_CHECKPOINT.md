# PocketCode Research Checkpoint — Provider, competitor, and cost subpasses

**Checkpoint ID:** PC-RESEARCH-CP-2026-10-26-003  
**Status:** CHATGPT PASS 0 AUDIT + PASS 1 PROVIDER/COMPETITOR/COST SUBPASSES RECORDED / GEMINI RESEARCH STILL PENDING  
**Date:** 2026-10-26  
**Repository:** https://github.com/marcelosofficial-ctrl/PocketCode-  
**Branch:** `pocketcode-pass0-audit-2026-10-26`  
**Base:** `main` at `555840d8d83342513d9cd353d4d1522d46a5c82d`  
**Branch head before checkpoint:** `6b509711f386f4bd50488e7c405184ae40f31a7c`  
**Draft PR:** https://github.com/marcelosofficial-ctrl/PocketCode-/pull/3

## Canonical artifacts

- [Pass 0 repository audit](PASS0_REPOSITORY_AUDIT.md)
- [Pass 1 provider research](PASS1_PROVIDER_RESEARCH.md)
- [Pass 1 competitor/substitute research](PASS1_COMPETITOR_RESEARCH.md)
- [Pass 1 illustrative cost model](PASS1_COST_MODEL.md)
- [Master research/implementation plan](MASTER_RESEARCH_IMPLEMENTATION_PLAN.md)
- [Gemini progress log](GEMINI_PROGRESS_LOG.md)

## Work completed

1. Audited repository truth, the proposed product loop, prototype/report-helper boundaries, security and zero-budget gates, naming risk, and cross-agent status.
2. Updated master-plan sections 1–5, 8, 11–12, and 15–17 with repository-backed truth, provider/competitor evidence, user-segment hypotheses, cost assumptions, blockers, and source links.
3. Refreshed current official provider docs for Modal, Daytona, Cloudflare Containers/Sandboxes, and E2B.
4. Refreshed current official competitor pages for the existing one-word PocketCode Android IDE, Derle, Kodo, Codeg, and GitHub Codespaces.
5. Added a fixed Python+CSV task comparison and candidate segments: quick-run verifier, learner/hobbyist, professional away from workstation.
6. Added explicit 60-second and 1,000-run variable-cost arithmetic with exclusions; no provider decision or live test.
7. Updated the existing competitor analysis/matrix and progress log while keeping Gemini's required research marked pending.

## Key conclusions

- The project remains discovery-stage; the existing prototype is simulated and no real execution backend exists.
- “Coding from a phone” is not a differentiator. The strongest current hypothesis to falsify is a no-setup, cross-platform disposable run with trustworthy bounded output/files and a clean report-to-any-AI handoff.
- The one-word PocketCode name is a high-priority collision risk because an existing Android IDE uses the same spelling and directly overlaps the category. No rename or legal decision is made.
- No provider is selected. Egress defaults, plan requirements, cost, and testing restrictions differ. A free allowance is not a guaranteed $0 ceiling.
- Under the strict $0 budget, no live provider test is authorized. E2B additionally requires prior written consent before testing.
- The candidate target segment is a quick-run verifier, but this is a hypothesis—not validated demand.

## Evidence / limitations

- Official pages were checked 2026-10-26 and are linked in the provider/competitor research docs.
- No apps were installed; no task benchmark, customer interview, account creation, credentials, provider workload, billing change, or live security test was performed.
- Cost arithmetic excludes major unknowns (startup/idle distributions, storage/logs, requests, abuse, plan-specific charges, orchestration/support); it is not an all-in model.
- Gemini's Pass 0–7 is not complete. ChatGPT's work is a parallel contribution, not a substitute for Gemini's required multi-pass research and cross-review.

## Next task

Continue Pass 1 with a fuller user/problem falsification and task-based comparison, then research remaining workstreams A–H. Keep all decisions provisional and all live tests blocked pending explicit owner approval.

## 2026-10-27 continuation — user/problem evidence

**Latest completed subpass:** [PASS1_USER_PROBLEM_EVIDENCE.md](PASS1_USER_PROBLEM_EVIDENCE.md)

- Public anecdotes are mixed and non-representative: some phone users run small scripts; others prefer local IDEs/Termux or remote environments and cite touch/screen/setup friction.
- Narrow target to test first: users with a recent real need to verify a short AI-generated Python script plus small text/CSV input on a phone. This is a test sequencing choice, not validated market selection.
- Added a proposed no-cost validation protocol: 5–8 behavior-based interviews, same deterministic Python+CSV task across available tools, observable setup/result/report-handoff measures, and pre-registered exploratory decision rules.
- No interviews, hands-on app comparisons, live provider tests, accounts, credentials, workloads, deployments, or spend. Prototype remains simulated. $0 gate unchanged.
- Master plan and Gemini progress log now link this subpass. Gemini completion remains pending; this is ChatGPT's independent work.
- Next: continue remaining Pass 1 workstreams, especially implementation/runtime feasibility and security/abuse requirements; then consolidate a skeptical synthesis without selecting a provider or renaming the project.

## 2026-10-27 continuation — execution security and abuse

**Latest completed subpass:** [PASS1_SECURITY_ABUSE_RESEARCH.md](PASS1_SECURITY_ABUSE_RESEARCH.md)

- Added provider-neutral threat model and mandatory controls for hostile user code, input/output files, multi-tenant isolation, network/metadata, resource exhaustion, artifact access, lifecycle evidence, abuse, and cost ceilings.
- Added adversarial acceptance matrix. It is a proposed test plan only; no live sandbox or provider test occurred.
- Current design rule: if a free tier cannot enforce mandatory controls, do not weaken requirements to fit it. No provider chosen, no live execution, no accounts, no spend; $0 gate unchanged.
- Master plan and Gemini progress log updated. This is ChatGPT research, not Gemini completion.
- Next: compare candidate runtime options against the security/operational requirements and narrow the implementation proof without assuming provider capability.
