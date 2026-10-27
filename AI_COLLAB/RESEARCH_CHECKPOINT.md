# PocketCode Research Checkpoint — Provider, competitor, and cost subpasses

**Checkpoint ID:** PC-RESEARCH-CP-2026-10-26-003  
**Status:** CHATGPT PASS 0 AUDIT + PASS 1 SUBPASSES RECORDED / GEMINI INDEPENDENT PASS 1 REVIEW RECEIVED; FULL GEMINI PASS 0–7 STILL PENDING  
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

## 2026-10-27 continuation — runtime/provider feasibility gate

**Latest completed subpass:** [PASS1_RUNTIME_PROVIDER_GATE.md](PASS1_RUNTIME_PROVIDER_GATE.md)

- No candidate approved for a live proof at $0. Cloudflare has the clearest paper fit but Containers require a $5/month Workers Paid plan. Daytona network controls are tier/API-version dependent; Modal credits are not a hard billing cap; E2B testing requires prior written consent.
- Added a provider-neutral adapter contract and fail-closed capability states; fake adapters can prove report/orchestration logic only.
- Updated provider research, master plan, and cross-agent log. No account, workload, live test, provider selection, or spend.
- Next: convert the combined user/problem, security, and provider gates into a small implementation-neutral contract and test plan, then audit remaining research gaps and link integrity. Keep PR draft and do not merge.

## 2026-10-27 continuation — draft execution contract

**Latest artifact:** [DRAFT_EXECUTION_CONTRACT.md](DRAFT_EXECUTION_CONTRACT.md)

- Translates the combined research into a provider-neutral request/lifecycle/report contract and offline test plan.
- Explicitly labels request limits and semantics as proposals, not production commitments.
- Distinguishes requested policy, provider-confirmed policy, observed execution, and formatter output. Missing evidence cannot produce PASS.
- No real adapter, provider SDK, execution backend, account, workload, test, or spend. No provider selected.
- Master plan and progress log updated. Continue with research-gap/link audit and consolidate the PR scope; do not merge.


## 2026-10-27 continuation — evidence and decision register

**Latest artifact:** [DECISION_REGISTER.md](DECISION_REGISTER.md)

- Consolidates supported evidence vs hypotheses vs unknowns; reversible decisions vs approval-required actions; prioritized offline/user-dependent/blocked gaps; exploratory stop/continue/pivot criteria; and a strict no-go list.
- Next highest-value offline pass: contract coherence audit plus threat-to-test traceability and external-link/version integrity. Avoid starting a real provider integration while $0/security gates remain unresolved.
- User interviews/task comparison have not happened. No provider/account/workload/credentials/live tests/spend, no rename, no merge/deployment. PR #3 remains research-only and should remain draft/unmerged.


## 2026-10-27 continuation — contract coherence audit

**Latest artifact:** [CONTRACT_COHERENCE_AUDIT.md](CONTRACT_COHERENCE_AUDIT.md)

- Static cross-review of the draft contract, security/abuse requirements, and provider gate found ten areas to settle before implementation: cleanup-failure semantics, terminal-state races, field-level evidence rules, honest cleanup claims, limit enforcement, capability freshness, artifact safety, tenant authorization, exact egress model, and report/evidence integrity.
- Added minimum proposed state/evidence rules and mapped offline tests separately from provider tests that remain blocked.
- No code or tests executed. No provider, account, live workload, spend, API freeze, merge, or deployment. Strict $0 gate unchanged.
- Next: verify source/link/version integrity and ensure the decision register, checkpoint, master plan, and PR description remain aligned.


## 2026-10-27 continuation — Gemini review handoff prepared

**Artifact:** [GEMINI_REVIEW_REQUEST.md](GEMINI_REVIEW_REQUEST.md)

- Prepared a narrow independent review request so the second AI can inspect current artifacts without duplicating broad research or making unverified completion claims.
- Requested outputs: critical contradictions, deterministic offline tests, primary-source/provider version issues, product falsification, and approval-gated work.
- The request has not itself been delivered to or completed by Gemini. No repo changes by Gemini are claimed. Strict $0 gate and draft/unmerged PR status remain.


## 2026-10-27 continuation — offline acceptance-test traceability

**Latest artifact:** [OFFLINE_ACCEPTANCE_TEST_MATRIX.md](OFFLINE_ACCEPTANCE_TEST_MATRIX.md)

- Added a proposed test inventory covering request validation, policy authority, tenant checks, lifecycle races, evidence integrity, output limits, artifacts, report status, cleanup, and cost unknowns.
- Found a contract consistency issue during static review: the lifecycle puts SUCCEEDED before cleanup, while the prose requires cleanup success for SUCCEEDED. The contract needs separate execution-outcome and overall-disposition semantics before implementation.
- This is a test specification and static review only; no tests were run and no provider was tested.
- Next: reconcile the proposed lifecycle semantics, then check source links and plan/version statements. Keep PR #3 draft/unmerged and the $0 gate binding.

## 2026-10-27 continuation — Gemini independent Pass 1 review received

**Latest artifact:** [GEMINI_PASS1_REVIEW_INTEGRATION_20261027.md](GEMINI_PASS1_REVIEW_INTEGRATION_20261027.md)

- The user supplied Gemini's independent review. ChatGPT integrated it as review evidence; this is not evidence that Gemini completed the full Pass 0–7 protocol.
- Accepted as high-priority issues: separate process outcome from overall disposition; add a fail-closed network-policy applied-state barrier before user code starts; expand deterministic tests for cancellation/timeout races, process trees, streaming/output bounds, artifact integrity, idempotency conflicts, and cost telemetry.
- Not adopted automatically: Modal as default provider, blanket rejection of local Android execution, fixed 24-hour idempotency TTL, fixed 1 MiB inline output cap, universal CSV schema checks, or project rename.
- Official E2B pricing checked 2026-10-27 lists free Hobby with a one-time $100 usage credit and Pro at $150/month plus usage. Credits do not satisfy a hard $0 ceiling. E2B test consent remains required.
- Draft contract now states that asynchronous mandatory network policy must be confirmed applied to the exact required revision before execution. Proposed tests remain NOT RUN; no provider accessed and no spending.
- At the time of this earlier note, DNS wording was unresolved. The later 2026-10-27 source clarification below records that the current indexed official guide says DNS is unrestricted except when all outbound traffic is blocked; runtime behavior remains unverified.
- Next: resolve remaining lifecycle/idempotency/report semantics, finish link/source integrity, and keep PR #3 draft/unmerged with PR #2 untouched.


## 2026-10-27 continuation — lifecycle/idempotency/artifact semantics proposal

**Latest artifact:** [PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md](PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md)

- Consolidated deterministic proposals for append-only execution evidence vs derived disposition, timeout/cancel event races, cleanup failure and result quarantine, same-key/different-payload idempotency conflicts, concurrent key reservation, artifact write/hash integrity, bounded streaming/redaction, and observed telemetry vs estimated/unavailable cost.
- Default proposed result-exposure rule is conservative: artifacts stay quarantined until cleanup is confirmed and artifact/tenant gates pass. This is a proposal for owner review, not a frozen product/API decision.
- Idempotency key TTL remains undecided; no fixed 24-hour TTL adopted. No fixed 1 MiB inline output cap adopted. Canonical fingerprint fields and stream overflow behavior remain open.
- Added corresponding test IDs to [OFFLINE_ACCEPTANCE_TEST_MATRIX.md](OFFLINE_ACCEPTANCE_TEST_MATRIX.md). All are proposed and NOT RUN.
- No code/tests executed, no provider/account/workload, no spend, no security claim, no merge/deploy. Strict $0 gate remains binding; PR #3 remains draft/unmerged; PR #2 untouched.
- **Next:** continue static cross-document/link integrity audit, correct any stale next-step text, and ensure all research status and decision boundaries are consistent. Owner review is needed before schema freeze or implementation.


## 2026-10-27 continuation — Modal networking source clarification

- Rechecked the current official search-indexed [Modal networking guide](https://modal.com/docs/guide/sandbox-networking) after direct page retrieval returned 502. The indexed guide explicitly states DNS traffic is unrestricted except when all outbound traffic is blocked; block_network=True drops all outbound traffic. Domain allowlisting remains Beta/TLS 443, and dynamic policy updates remain Alpha.
- Updated [PASS1_PROVIDER_RESEARCH.md](PASS1_PROVIDER_RESEARCH.md), [PASS1_RUNTIME_PROVIDER_GATE.md](PASS1_RUNTIME_PROVIDER_GATE.md), [PASS1_SOURCE_INTEGRITY_UPDATE.md](PASS1_SOURCE_INTEGRITY_UPDATE.md), and [PASS1_SOURCE_VERSION_COHERENCE_AUDIT.md](PASS1_SOURCE_VERSION_COHERENCE_AUDIT.md) to replace the prior DNS-wording uncertainty.
- This closes a documentation wording gap only. It is not runtime proof; metadata/private-address paths, exact configuration, plan eligibility, and billing controls remain unverified. No provider is selected; strict $0 remains.


## 2026-10-27 continuation — race determinism refinement

A static review found one subtle ambiguity in the lifecycle proposal: atomic compare-and-set guarantees one committed winner, but does not by itself guarantee the same winner across repeated concurrent timeout/cancel races. The lifecycle proposal now distinguishes single-winner safety from replay determinism and recommends a monotonic coordinator-ingress sequence or an explicitly chosen precedence rule. The acceptance matrix now requires replayable ordering evidence and does not assume identical winners across race permutations unless a precedence rule is approved.

This is documentation/specification work only. No tests were run. Before schema freeze, decide the authoritative event-ordering rule; keep provider timestamps alone from silently overriding the committed decision. Strict $0 remains; PR #3 stays draft/unmerged and PR #2 untouched.
