# Gemini review request — PocketCode research branch

**Purpose:** independent skeptical review of the current research/specification set. This is a request, not evidence that Gemini has reviewed anything.  
**Budget/safety:** strict $0. Do not create accounts, use credentials, run provider workloads, change billing, deploy, merge, or weaken security requirements. Do not claim live tests or market validation.

## Read these first

1. [DECISION_REGISTER.md](DECISION_REGISTER.md) — current evidence ledger and decision gates.
2. [CONTRACT_COHERENCE_AUDIT.md](CONTRACT_COHERENCE_AUDIT.md) — ten contract ambiguities and proposed tests.
3. [DRAFT_EXECUTION_CONTRACT.md](DRAFT_EXECUTION_CONTRACT.md) — provider-neutral draft, not production API.
4. [PASS1_CONTRACT_COHERENCE_RESOLUTION.md](PASS1_CONTRACT_COHERENCE_RESOLUTION.md) — proposed separation of execution outcome and overall disposition; not adopted.
5. [OFFLINE_ACCEPTANCE_TEST_MATRIX.md](OFFLINE_ACCEPTANCE_TEST_MATRIX.md) — proposed deterministic test inventory, including LC-01–LC-12; tests are NOT RUN.
6. [PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md](PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md) — newest lifecycle, race, idempotency, artifact, streaming, and cost proposal; not frozen.
7. [PASS1_OWNER_DECISION_PACKET_20261027.md](PASS1_OWNER_DECISION_PACKET_20261027.md) — proposed defaults and trade-offs for remaining owner decisions; all approvals pending.
8. [PASS1_SECURITY_ABUSE_RESEARCH.md](PASS1_SECURITY_ABUSE_RESEARCH.md) — threat model and mandatory gates.
9. [PASS1_RUNTIME_PROVIDER_GATE.md](PASS1_RUNTIME_PROVIDER_GATE.md) — provider feasibility and plan/version constraints.
10. [PASS1_PROVIDER_RESEARCH.md](PASS1_PROVIDER_RESEARCH.md) — provider comparison; check its v0/v2 version distinctions.
11. [PASS1_SOURCE_INTEGRITY_UPDATE.md](PASS1_SOURCE_INTEGRITY_UPDATE.md) — recent official-source refresh.
12. [PASS1_SOURCE_VERSION_COHERENCE_AUDIT.md](PASS1_SOURCE_VERSION_COHERENCE_AUDIT.md) — cross-document source/version conflicts to verify independently.
13. [PASS1_USER_PROBLEM_EVIDENCE.md](PASS1_USER_PROBLEM_EVIDENCE.md) — mixed public anecdotes and proposed user-validation protocol.
14. [MASTER_RESEARCH_IMPLEMENTATION_PLAN.md](MASTER_RESEARCH_IMPLEMENTATION_PLAN.md) and [RESEARCH_CHECKPOINT.md](RESEARCH_CHECKPOINT.md) — project continuity.

Review the current branch content rather than relying on summaries or old snapshots. If you cannot access the branch links, state that limitation and review only what is provided.

## Requested review — in this order

### A. Critical contradictions
Find contradictions or unsafe gaps between contract, threat model, provider gate, report contract, source/version audit, and decision register. Prioritize issues that could permit false PASS, cross-tenant access, network/metadata access, unbounded resource use, or cleanup uncertainty. Pay special attention to whether the proposed two-axis lifecycle semantics actually resolve the contradiction without creating a new one.

### B. Test coverage
For each critical issue, provide:
- ID and severity (Critical / High / Medium / Low)
- exact file and heading (line numbers only if actually inspected)
- concrete failure scenario
- minimum fix or explicit decision required
- deterministic offline test that would detect it
- whether proof requires a real provider and why

Do not say a test passed unless you actually ran it and can state the exact command/environment/result. Do not treat a proposed test as executed.

### C. Provider evidence
Check only primary vendor sources for claims that can change by plan, API version, or date. Specifically reconcile Daytona v0 tier-based network restrictions versus Daytona v2 alpha policy behavior; verify source links and distinguish documented claims from verified configuration or tested behavior. Identify missing/contradictory source links. Do not select a provider merely because its marketing documentation sounds strong.

### D. Product falsification
Challenge the narrow Python+CSV verifier hypothesis. Identify strongest competing explanations and what observation would change the recommendation. Do not infer market size or demand from anecdotes.

### E. Decision summary
Return only:
1. **Blockers** — issues that must be resolved before implementation.
2. **Offline work** — next deterministic tasks possible at $0.
3. **Approval-gated work** — any task requiring owner approval, account, spend, consent, deployment, or live execution.
4. **Contradictions with ChatGPT’s review** — with evidence.
5. **Unverified items** — things you could not check.

## Constraints

- No broad rewrite, new architecture, provider SDK, or speculative implementation.
- Prefer standard/open-source tools over custom utilities where appropriate, but justify the choice and licensing/maintenance burden.
- Preserve provider-neutrality and fail-closed behavior.
- Strict $0 means no payment, no card entry, no paid plan, and no assumption that credits are a hard spending cap.
- Do not modify the repository unless explicitly asked. Return the review as a compact, copyable response so the owner can relay it.
