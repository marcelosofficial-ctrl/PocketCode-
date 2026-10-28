# PocketCode Roadmap

This roadmap is provisional. Work should advance through evidence and tested milestones rather than assumed dates.

## Phase 0: Discovery and validation

- [ ] Define the initial target user and top use cases.
- [ ] Build a sourced competitor/alternative matrix.
- [ ] Identify the unmet workflow, if any, that users care enough about.
- [ ] Interview or test with a small number of target users.
- [ ] Define a narrow MVP and explicit non-goals.
- [ ] Compare execution providers, isolation guarantees, regional availability, pricing, and data retention.
- [ ] Review naming and brand conflicts before investing in public identity.
- [ ] Evaluate the AI Efficiency Coach/Handoff feature: compact task packets, checkpointing, and provider-neutral copy/share flow. Use the cross-project AI workflow master; do not assume direct app control.

**Exit gate:** a specific user problem and first workflow are supported by evidence, not just an attractive concept.

## Phase 1: Technical proof

- [ ] Demonstrate one real Python execution in a disposable isolated worker.
- [ ] Verify success, stderr, exit status, timeout, cancellation, and cleanup.
- [ ] Test resource limits and blocked or controlled networking.
- [ ] Measure cold-start and repeat-run latency.
- [ ] Estimate unit cost under realistic use.
- [ ] Verify that outputs and files can be returned safely.

**Exit gate:** security and operational constraints are understood, with a credible cost model.

## Phase 2: Private mobile prototype

- [ ] Mobile-first workspace UI.
- [ ] Code/file input and runtime selection for the single supported runtime.
- [ ] Execution status, output, errors, and generated files.
- [ ] Useful history and copyable execution report.
- [ ] Authentication and user isolation if persisted user data is enabled.
- [ ] Automated tests and basic observability.
- [ ] Test on iOS Safari and Android browsers.
- [ ] Prototype task-profile selection and a compact “prepare prompt / copy or share” handoff using synthetic examples only.

**Exit gate:** a target user can complete the core loop on a phone without a PC.

## Phase 3: Closed MVP

- [ ] Invite-only user testing.
- [ ] Usage limits, abuse prevention, retention/deletion controls, and support process.
- [ ] Improve onboarding and error messages from observed failures.
- [ ] Validate repeat use and willingness to pay before adding expensive features.

## Phase 4: Expand only with evidence

Candidate features, not commitments:
- JavaScript/Node.js runtime.
- More project files and dependency/environment controls.
- Git integration.
- Reviewable diffs and rollback.
- Optional AI provider integrations.
- PowerShell 7 in a Linux environment, if validated demand justifies it.
- Windows-specific execution as a separate infrastructure decision.
- Native apps if browser limitations demonstrably block key workflows.

## Release discipline

- Every milestone has explicit acceptance criteria.
- No feature is called complete without evidence and tests.
- Keep production credentials and deployment secrets out of Git.
- Do not make public release, billing, or infrastructure commitments without owner approval.


## Cross-cutting candidate: AI Efficiency Coach & Handoff (2026-10-28)

This feature is a discovery-stage product hypothesis and does not change the execution-provider decision or the $0 budget. The cross-project [AI Workflow Efficiency and Cross-App Orchestration Master](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/AI_WORKFLOW_EFFICIENCY_AND_CROSS_APP_ORCHESTRATION_MASTER_2026-10-28.md) records three research passes and defines provider-neutral profiles/task packets.

Initial no-cost test: a user selects Lean/Balanced/Deep Verify/Research/Repair/Checkpoint (or accepts an automatic suggestion), receives a concise prompt with scope and acceptance checks, copies/shares it into any AI assistant, then returns its code/error/output to PocketCode. Keep examples simulated. A native skill/plugin/MCP integration may be investigated where officially supported, but not required for the first test.

**Non-goals at this stage:** no background clipboard monitoring, hidden conversation scraping, universal app automation, API credentials, direct model calls, account creation, billing, provider selection, or remote-PC control. No promise of bypassing free-tier usage limits. OS-supported share/copy flows and truthful fallback behavior are the baseline.
