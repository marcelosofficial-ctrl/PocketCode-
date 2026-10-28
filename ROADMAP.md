# PocketCode Roadmap

This roadmap is provisional. Work should advance through evidence and tested milestones rather than assumed dates.

For the current phone-only work sequence through February 2027, see the [four-month coordination plan](AI_COLLAB/FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md) and its [continuity hub](AI_COLLAB/POCKETCODE_CONTINUITY_HUB_20261028.md). This overlay coordinates discovery and PC-return preparation; it does not change the roadmap phase gates or approve live execution.

## Phase 0: Discovery and validation

- [ ] Define the initial target user and top use cases.
- [ ] Build a sourced competitor/alternative matrix.
- [ ] Identify the unmet workflow, if any, that users care enough about.
- [ ] Interview or test with a small number of target users.
- [ ] Define a narrow MVP and explicit non-goals.
- [ ] Compare execution providers, isolation guarantees, regional availability, pricing, and data retention.
- [ ] Review naming and brand conflicts before investing in public identity.
- [ ] Evaluate the AI Workflow Director feature hypothesis: compact task profiles, universal copy/paste, provider-specific setup guidance, and continuation capsules; use the research master as the source and validate before implementation.

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
- [ ] If research/user tests justify it, add a user-reviewed AI handoff flow with share-sheet support where available, a universal copy/paste fallback, and a portable continuation capsule.
- [ ] Authentication and user isolation if persisted user data is enabled.
- [ ] Automated tests and basic observability.
- [ ] Test on iOS Safari and Android browsers.

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
