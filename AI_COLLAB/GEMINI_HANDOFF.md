# Gemini Co-Developer Handoff — PocketCode

Created 2026-10-20. This is an operating contract and research assignment, not a claim that research has already been done.

## Assignment

You are a co-developer on PocketCode. Do substantial, multi-pass research and turn useful ideas into implementation-ready specifications, decisions, tests, and dependency-ordered tasks. Do not stop after a quick brainstorm or one generic pass. The goal is to leave ChatGPT with research and implementation planning mature enough that the remaining work is execution, implementation, and verification.

If you cannot actually access or edit GitHub from Gemini, do not pretend otherwise. Return complete Markdown artifacts for the owner to carry back. Do not fabricate commits, tests, interviews, benchmarks, pricing, or sources.

## Project context

Repository: https://github.com/marcelosofficial-ctrl/PocketCode-

PocketCode is an early-stage project separate from RevDev. No app code exists yet; no framework, execution provider, pricing model, or final brand has been selected.

Current hypothesis: a mobile-first workspace for people using AI to generate code who need to run, inspect, and improve it when they do not have a computer nearby:
1. Paste/import code and supporting files from any AI assistant.
2. Execute in a real, appropriately isolated environment.
3. Inspect actual stdout/stderr, exit status, duration, and generated files.
4. Copy a structured, redacted execution report into their preferred AI assistant.
5. Apply a fix and rerun to verify it.

Potential positioning: “Vibe code. Run it. Fix it. From your phone.” This is unvalidated. “Vibe coding” is the marketing hook, phone-first access is the promise, and actual execution evidence is the proposed product proof. Competitors may already cover parts of this loop.

First candidate workflow: from a phone browser, paste a small Python script and add a text/CSV input file; run it in a disposable sandbox; inspect genuine success/errors; download a generated output file; copy a report to an AI assistant; modify and rerun.

Guardrails:
- PocketCode is provisional and has a same-name/adjacent-category conflict risk.
- PWA and remote Python are candidates, not decisions.
- No app implementation or real execution has been proven.
- Repository is public: never include secrets, credentials, private user data, or real user code.
- No paid service, paid infrastructure, vendor commitment, public execution endpoint, release, public launch, or irreversible change without explicit owner approval.
- Treat submitted code as hostile. Require disposable isolation, no host secrets, strict server-side resource limits, restricted networking by default, tenant isolation, cleanup, abuse controls, and clear retention/deletion rules.
- Never claim a test passed unless it was run and evidence recorded.
- Optimize for an owner who may have only an iPhone; plans and handoffs must be actionable without local developer tools.
- Keep execution-provider and AI-provider choices open until evidence supports a decision.

## Read these repository docs first

Read current versions, not only this handoff:
- AGENTS.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/AGENTS.md
- GEMINI.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/GEMINI.md
- PROJECT_STATUS.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/PROJECT_STATUS.md
- PRODUCT_SPEC.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/PRODUCT_SPEC.md
- PRODUCT/FIRST_RUN_WORKFLOW.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/PRODUCT/FIRST_RUN_WORKFLOW.md
- ARCHITECTURE.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/ARCHITECTURE.md
- SECURITY.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/SECURITY.md
- ROADMAP.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/ROADMAP.md
- DECISIONS.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/DECISIONS.md
- RESEARCH/COMPETITIVE_ANALYSIS.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/RESEARCH/COMPETITIVE_ANALYSIS.md
- RESEARCH/EXECUTION_PROVIDER_RESEARCH.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/RESEARCH/EXECUTION_PROVIDER_RESEARCH.md
- MARKETING/POSITIONING_HYPOTHESIS.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/MARKETING/POSITIONING_HYPOTHESIS.md
- AI_COLLAB/CHATGPT_INITIAL_PROVIDER_REVIEW.md: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/main/AI_COLLAB/CHATGPT_INITIAL_PROVIDER_REVIEW.md — preliminary independent provider evidence; verify it rather than copying it.

Do not merely restate these docs. Find stale claims, gaps, contradictions, and questions requiring evidence.

## Division of labor

This is the default division of responsibility, consistent with AGENTS.md. Gemini and ChatGPT do not have direct inter-model messaging; the owner carries artifacts between them. GitHub is the durable source of truth. A role assignment in a specific owner request can override these defaults.

### Claude — lead implementer
Own focused implementation tasks and substantial code changes when assigned. Inspect the current repository state and acceptance criteria first; make reviewable changes; report exact branch, commit, paths, test commands/results, and remaining risks. Do not claim tests passed without running them.

### Gemini — co-developer and independent design/spec auditor
Own multi-pass research, architecture alternatives, provider and security comparisons, product/API contracts, acceptance criteria, test matrices, and skeptical review of Claude's proposed changes. Identify contradictions, unsupported claims, edge cases, and missing evidence. Avoid independently implementing the same task unless explicitly assigned. Keep the master plan marked incomplete until its required research and review actually exist.

### ChatGPT — continuity and integration coordinator
Own compact recovery context, synthesis of research and decisions, independent acceptance/diff cross-checks, task sequencing, status/decision-log upkeep, and deployment/portfolio preparation when relevant and explicitly authorized. ChatGPT should not claim local execution or direct access it does not have.

### Required handoff payload
Every handoff must state: (1) exact repository, branch, and commit; (2) exact changed/proposed paths; (3) task and acceptance criteria; (4) results and evidence actually collected; (5) verification status, including commands actually run or explicitly not run; (6) limitations, risks, and open questions; and (7) one clear requested next action. Use statuses **proposed**, **in progress**, **completed-unverified**, **verified**, **blocked**, or **superseded**. The owner remains the approval authority for paid services, live workloads, releases, deployments, and irreversible actions.

### Review loop
1. Gemini researches and delivers a sourced specification, keeping AI_COLLAB/GEMINI_PROGRESS_LOG.md current and consolidating mature findings in the master plan.
2. For substantial research/design work, complete at least two substantive research/review passes. ChatGPT or Claude should challenge omissions, unsafe shortcuts, unsupported claims, cost surprises, contradictions, and implementability; Gemini should mark each material finding resolved, disputed with rationale, or blocked. If a second pass is not useful for a narrowly scoped task, explain why rather than pretending it happened.
3. Claude implements only tasks that are sufficiently specified and explicitly assigned, or identifies blockers.
4. ChatGPT reconciles artifacts, cross-checks claims against available evidence, and prepares the next task/handoff.
5. Gemini reviews material implementation changes for requirements, architecture, security, edge cases, and test adequacy.
6. The owner carries artifacts between agents and approves owner-gated actions. Do not claim this loop occurred until each named step actually happened.

## Workstreams — all required

A. Users and validation: distinguish beginners, hobbyists, students, professionals, and AI app builders; identify phone-first failure moments; compare jobs; create non-leading interviews; define pass/fail thresholds and disconfirming evidence. Never invent interviews or demand data.

B. Competitors and substitutes: mobile IDEs/local runtimes, hosted runners, cloud IDEs, remote coding agents, AI app builders, manual workarounds. Verify capabilities using current primary sources; compare onboarding, language support, execution location, files, AI lock-in, mobile UX, pricing/limits, privacy/security and limitations. Investigate the PocketCode name conflict without giving legal clearance.

C. Execution backend: screen at least three candidates and compare the strongest two in depth. Verify actual isolation model, networking/egress, lifecycle, cancellation, timeouts, CPU/memory/process/disk/output limits, file transfer, streaming, cleanup, region/data handling, retention, quotas, cold starts, API maturity, portability and operator burden. Create a provider-neutral adapter contract. Model cost using current official pricing, explicit assumptions, best/expected/adverse scenarios and source dates. No paid workloads.

D. Security and abuse: threat model malicious code, sandbox escape, SSRF/metadata, tenant crossover, data exfiltration, resource exhaustion, malicious archives/path traversal, output injection, supply chain, secrets, public service abuse, retention/deletion and incident response. Distinguish vendor claims from verified guarantees and tests that need a live run.

E. Product and mobile UX: detailed screen/state/error specifications, iOS Safari and Android browser constraints, touch/keyboard/viewport, file picker/download, refresh/lost connection, retries, accessibility, minimal project/file model, job lifecycle, report format. Keep MVP narrow.

F. Architecture and implementation: compare at least two plausible architectures; define trust boundaries, APIs/schemas, job lifecycle, storage/retention, auth, secrets, observability, deployment assumptions, and tasks with paths/modules, dependencies, acceptance criteria, tests, risks and definition of done. Mark tasks READY, NEEDS_OWNER_DECISION, or BLOCKED. Identify work possible without credentials.

G. Marketing/naming/distribution: compare “vibe code from your phone” with utility-led messages; create ethical low-cost validation experiments and measurable thresholds; define name-validation process, not legal advice; do not market unbuilt features.

H. Business/operations: cost and abuse economics, quotas, provider outages, privacy risk, reliability, retention, support and monetization hypotheses. No invented market size or conversion rates.

## Mandatory multi-pass protocol

Pass 0 — Audit repository and hypothesis. Inventory current docs, claims, decisions, contradictions and gaps. Create an audit/checklist and workstream plan. Classify claims as verified primary source, secondary source, inference, assumption, unverified, needs live test, or needs owner approval.

Pass 1 — Broad evidence gathering across A–H. Prefer official docs, pricing pages, API references, security docs, terms/data policies, app stores and source repositories. Record source title, direct URL, date checked, claim supported, quality and caveats. Use multiple sources for high-impact claims. No provider decision yet.

Pass 2 — Synthesis and falsification. Compare alternatives; actively search for evidence against the current hypothesis and each leading provider. Separate unique, useful, table-stakes and unproven features. Define the smallest test that could disconfirm key assumptions.

Pass 3 — Implementation-ready specs. Define UX, architecture, API/data contracts, provider adapter, security controls, errors/state model, acceptance tests and tasks. Use stable IDs such as REQ-EXEC-001, SEC-004, TEST-RUN-007 and TASK-BE-003. Trace tasks to requirements/tests. No vague tasks like “build backend.”

Pass 4 — Cost and operational review. Recalculate current cost; test best/expected/adverse scenarios; cover quota exhaustion, outage, malicious jobs, timeout, cleanup failure, output leakage and deletion. Stop before paid use or credentials.

Pass 5 — Skeptical self-review. Review as a senior engineer, security reviewer, product researcher and mobile UX reviewer. Find missing work, unsupported claims, hidden prerequisites, contradictions, false precision, and tasks impossible for an iPhone-only owner. Fix issues, not just list them. Add likelihood/impact/detection/mitigation/owner/residual risk.

Pass 6 — Consolidate. Update AI_COLLAB/MASTER_RESEARCH_IMPLEMENTATION_PLAN.md as a self-contained canonical master. Include executive summary, current truth, evidence register, competitive/provider matrices, threat model, UX/technical specs, cost model, recommended decisions, requirement-to-test traceability, sequenced implementation tasks, risk register, blockers, change log and completion checklist. Supporting notes are fine, but key findings must be in the master file.

Pass 7 — ChatGPT review and revision. Deliver master file plus concise questions for ChatGPT. After ChatGPT provides review comments, revise the master, record disposition for every comment, and leave unresolved disagreements visible. Do not claim ChatGPT reviewed it before that happens.

## Evidence and quality rules

- Cite direct URLs and dates for material claims.
- Classify evidence: VERIFIED_PRIMARY_SOURCE, SECONDARY_SOURCE, INFERENCE, ASSUMPTION, UNVERIFIED, NEEDS_LIVE_TEST, NEEDS_OWNER_APPROVAL.
- For major recommendations give supporting evidence, strongest counterargument, confidence, and what would change the recommendation.
- Pricing must include currency, unit, assumptions, date and source.
- No invented benchmarks, user research, tests, prices or repo changes.
- Time-sensitive facts must be rechecked before implementation.
- Cover all A–H workstreams.
- Screen at least 3 backend options; compare at least 2 deeply.
- Include concrete security mitigations and tests, not just general warnings.
- Include testable API, state, file and error contracts.
- Include go/no-go/pivot criteria.
- Finish with the master artifact, a self-review and explicit unresolved items.
- A quick summary or empty template is not completion.

## Required outputs

1. AI_COLLAB/GEMINI_PROGRESS_LOG.md with pass-by-pass dated evidence and blockers.
2. AI_COLLAB/MASTER_RESEARCH_IMPLEMENTATION_PLAN.md as the canonical digest.
3. Supporting research notes only where they materially improve traceability.
4. A concise owner handoff stating passes completed, top recommendations/confidence, approvals needed, gaps, and what ChatGPT should do next.

Begin with Pass 0 now and continue through all passes. Do not stop after a preliminary plan.
