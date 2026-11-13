# PocketCode Master Workflow — Efficiency and Evidence Rules

**Status:** Operating-method guidance; it does not replace the product or technical master.
**Authority:** Follow repository instructions and established project decisions first. This document governs how work is performed, not what PocketCode must become.
**Owner constraints:** The owner is working mainly from a phone and may lack PC access for months. Keep spend at $0. Do not deploy, merge, enable paid infrastructure, create provider workloads, change repository visibility, push publicly, rewrite history, or perform consequential external actions without explicit authorization. PR #2 is out of scope and must remain untouched unless explicitly authorized.

## 1. Source of truth and evidence

Before significant work, inspect the current repository, branch, relevant history, instructions, source files, status/checkpoints, product/architecture/security/roadmap documents, decisions, tests, issues, and PRs. Follow the repository's own authority order. In general: verified repository state; current status/checkpoints; product and technical specifications; decisions; research/issues/PR/test evidence; chat memory last.

A chat message is not proof of a commit or passing test. Never invent files, commits, test results, research findings, deployment success, or runtime guarantees. Separate verified facts, assumptions, proposals, decisions, unresolved questions, and blockers. If tools cannot verify a claim, say so and do only work that remains reliable.

## 2. Substantial, coherent passes

Prefer fewer, productive passes over fragmented exchanges. A pass should produce a meaningful implementation with tests, a researched decision, a coherent feature slice, a verified bug fix, a focused security review, or a continuity blocker removed. Batch related code/tests/docs when safe; split unrelated or risky changes when this improves review, rollback, or security.

For each substantial pass: establish state; choose the highest-value achievable task; define outcome and acceptance criteria; inspect/reuse existing work; implement/research; verify; inspect the diff; record evidence, risks, and next action. Do not add planning documents unless they change a decision, reduce uncertainty, or unblock work.

## 3. Scale planning to risk

Small/clear/low-risk tasks need focused inspection, change, test, and diff review. Complex, cross-cutting, ambiguous, or security-sensitive work needs investigation, dependencies and alternatives, interfaces, a concise plan, acceptance criteria, failure cases, approval boundaries, implementation, and verification. Avoid elaborate ceremony for trivial work and avoid skipping planning when a wrong assumption is expensive or unsafe. Define interfaces before parallel component work.

## 4. Outcome-oriented task definitions

Specify goal, context, constraints, observable acceptance criteria, verification, and prohibited actions. Prefer concrete bug/behavior requests over vague “improve the system” prompts. Preserve exact diagnostics, errors, paths, and excerpts when available. Extend existing examples and patterns rather than building a parallel solution without reason.

## 5. Reuse before reinventing

Search the repository and its dependencies before creating utilities, parsers, algorithms, frameworks, or infrastructure. Evaluate established libraries by maintenance, licensing, security, compatibility, portability, and operating cost. Add dependencies only when justified. Prefer the simplest solution that satisfies real requirements without omitting necessary safeguards.

## 6. Three-AI division of labor

Default roles, subject to actual access and current instructions:
- **Claude:** primary implementation lead when it has required repository access/tools.
- **ChatGPT:** research, requirements, architecture comparisons, continuity, integration planning, and evidence-based acceptance review.
- **Gemini:** independent architecture/specification review, adversarial analysis, test planning, and focused co-development when useful.

Assign one primary implementer. Give reviewers bounded questions, a deliverable, relevant context, and intended use. Avoid all three independently implementing the same feature or repeating research. Define ownership boundaries, consolidate results before integration, and resolve disagreement through evidence, assumptions, security, compatibility, and cost. Record consequential resolutions. Model count is not a quality metric.

## 7. Efficient, decision-relevant research

State the decision/uncertainty and criteria first. Search existing project material and prior research before repeating work. Prefer primary sources, official docs, specifications, and original research; use practitioner reports to find failure modes, then verify consequential claims independently. Compare alternatives against the same criteria. Report recommendation, trade-offs, uncertainty, sources, and what would change the decision. Stop when evidence is sufficient or returns diminish. Popularity is not proof. Maintain existing research indexes; do not create duplicate summaries.

## 8. Discovery-first product discipline

Existing product/architecture/roadmap documents remain authoritative. Product hypothesis: phone-first work with AI-generated or user-written code, an appropriate runtime/environment, truthful execution evidence, and a useful report the user can return to their preferred AI. Do not treat this hypothesis as validated demand.

Separate validated needs from personas/assumptions, user evidence from AI-generated claims, requirements from proposals, options from decisions, demos from reliable end-to-end behavior, and feasibility from sustainable operations. Prioritize research that can change direction, narrow MVP, resolve expensive uncertainty, or prevent unsafe implementation. Seek evidence of real tasks, workarounds, repeat use, and willingness to pay where relevant. Do not expand platforms, languages, integrations, or infrastructure just because they sound attractive.

## 9. Protect the core workflow and truthful status

The intended loop is: create/open workspace; add/edit code and inputs; select supported runtime; submit to an appropriate isolated environment; inspect status/stdout/stderr/timing/exit information/files; distinguish program outcome from infrastructure failure; share a bounded, appropriately redacted report with the preferred AI; iterate, save, or export.

Keep the direction provider-neutral unless an explicit decision changes it. Do not imply a provider/runtime/pricing model has been selected when records leave it open. API acceptance is not execution success; a running process is not completion; missing output must never be fabricated as success.

## 10. Security from the beginning

Follow current SECURITY/specification/release gates. Evaluate disposable isolation, unprivileged execution, host mounts/access, CPU/memory/process/disk/upload/output/concurrency/user limits, authentication and authorization on every project/run/result/file operation, tenant isolation, outbound-network and metadata protection, safe archives/path handling/downloads, separation of credentials from untrusted workers, dependency/package-registry controls, cleanup/retention/deletion/logging, abuse prevention, and incident response as applicable.

Use relevant OWASP API Security and NIST SSDF guidance. A sample program running is not permission to expose public arbitrary-code execution. Public execution requires explicit review/testing of isolation, access controls, limits, network restrictions, cleanup, monitoring, abuse controls, and recovery. Unit tests cannot prove multi-tenant security. Claims must match actual evidence.

## 11. Verification means executed evidence

Choose verification according to risk: unit/regression; API/integration; static/type/format/dependency checks; authorization and cross-user tests; failure paths; cancellation/timeouts/cleanup/limits; browser/responsive; real iOS/Android; end-to-end tests with a real isolated environment where required.

Add regression tests for defects. Where practical, demonstrate a test fails before the fix. Do not weaken tests just to pass; explain legitimate behavior changes. After implementation run relevant tests, broader checks as warranted, inspect full diff/callers/interfaces/dependencies, and check edge cases, security, compatibility, secrets, unsafe defaults, generated artifacts, and unrelated changes.

Report exact status: implemented/not tested; targeted tests passed; integration verified; real-device behavior verified; scoped security review completed; or blocked/partial. A written test that was not executed has not passed. Mocks do not prove real provider integration. Browser preview does not prove real-device behavior.

## 12. Focused changes and owner control

Follow repo branch/commit/PR practices. Keep changes useful but reviewable. Explain what/why, inspect actual diff, check docs/tests against implementation, and cite exact refs. Never expose secrets. No force-push, history rewrite, deletion of owner content, visibility changes, releases, paid infrastructure, deployment, merge, public execution, or other consequential external effects without explicit owner approval. A proposed change is not permission for every related action.

## 13. Free-plan and phone-first efficiency

Assume AI quotas, uploads, context, and tools vary. Keep the workflow useful without paid AI, unlimited uploads, PC access, or proprietary features. Inspect relevant files only; consolidate related questions/research; batch coherent changes; keep durable context in GitHub; avoid duplicate uploads; preserve exact decisions, paths, evidence, and open questions; use bounded independent review; reuse completed research until new evidence warrants updating; leave a checkpoint when interrupted. Do not bypass usage limits. When a tool is unavailable, adapt and state the limitation. Do not ask the owner to run commands or inspect files routinely if connected tools can do it. Ask for the smallest specific owner input only when genuinely blocking.

## 14. Durable continuity and active-work source of truth

Repository files are durable truth; chat memory is supplementary. Update existing status, checkpoint, decision, research, and test documents when meaningful state changes. Avoid redundant or contradictory records. A handoff should preserve branch and exact commit, relevant files and changes, adopted decisions and rationale, tests actually run, research/source links, limitations/risks/blockers, and next task with acceptance criteria.

Use existing task/status mechanisms. Active work should have an outcome, priority/reason, dependencies/decisions, acceptance criteria, primary owner, verifiable status, and result. Capture ideas without automatically interrupting priority; reprioritize only when evidence, risk, or dependencies justify it. Do not let multiple AIs maintain conflicting roadmaps/checkpoints.

## 15. Completion report

For every substantial pass report:
- **Outcome:** what changed.
- **Evidence:** exact files/commit/PR and checks/results.
- **Decisions:** adopted versus proposed.
- **Limitations:** what could not be verified and why.
- **Risks/blockers:** unresolved items or approvals.
- **Next action:** highest-value continuation and acceptance criteria.

A task is complete only when its criteria are met, or it is explicitly partial/blocked with remaining limits documented. Avoid vague “done” claims.

## 16. Improve based on observed failure

Treat this as a practical standard, not ceremony. Investigate root causes of repeated context loss, implementation mistakes, duplicated research, conflicting edits, excessive abstractions, false success claims, security omissions, and wasted free-tier usage. Improve checkpoints, acceptance criteria/tests, research indexes, ownership boundaries, evidence requirements, threat cases/release gates, and batching as appropriate. Keep rules only when they demonstrably improve reliability, security, continuity, or progress.

## 17. Research references (revisit when consequential/current)

- Anthropic Claude Code best practices: https://www.anthropic.com/research/claude-code-best-practices
- OpenAI Codex best practices: https://learn.chatgpt.com/docs/learn/best-practices
- OpenAI team Codex practices: https://openai.com/business/guides-and-resources/how-openai-uses-codex/
- Practitioner reports: https://www.reddit.com/r/ClaudeAI/comments/1l1uea1/after_6_months_of_daily_ai_pair_programming_heres/ and https://www.reddit.com/r/ChatGPTCoding/comments/1hinwsr
- ChatGPT Projects: https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- File uploads/limits: https://help.openai.com/en/articles/8555545-uploading-files-and-audio-to-chatgpt
- GitHub PR review guidance: https://docs.github.com/en/pull-requests/concepts/helping-others-review-your-changes
- OWASP API Security Top 10: https://owasp.org/www-project-api-security/
- NIST SSDF: https://csrc.nist.gov/pubs/sp/800/218/final

These sources inform working methods; they do not prove every technique universally effective. Revalidate changing product limits and consequential technical claims.

## Final principle

Optimize for verified progress, not generated-code volume, messages, agents, or long plans. Inspect before inventing; reuse before rebuilding; research the decision that matters; plan in proportion to risk; implement coherent changes; verify actual results; review independently where useful; preserve security and owner control; keep discovery honest; record durable evidence. Every substantial pass should leave a verified improvement, a better-supported decision, a meaningful uncertainty reduction, or a clear next action.

**Authority reminder:** This workflow supplements PocketCode's existing project documents. It does not replace PRODUCT_SPEC, ARCHITECTURE, SECURITY, ROADMAP, DECISIONS, repository instructions, or current verified implementation state.
