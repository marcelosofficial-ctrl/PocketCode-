# PocketCode Shared AI and Contributor Instructions

These rules apply to ChatGPT, Claude, Gemini, human contributors, and automation. This file is the common entry point; provider-specific instruction files should link here rather than contradict it.

## Source of truth

1. Current repository contents and commit history are authoritative for implementation state.
2. PROJECT_STATUS.md records current phase and verified progress.
3. PRODUCT_SPEC.md, ARCHITECTURE.md, SECURITY.md, and ROADMAP.md record current proposals and constraints.
4. DECISIONS.md records decisions and their rationale.
5. Chat messages are discussion, not proof that repository changes or tests happened.

Inspect relevant files and the current branch before claiming knowledge of project state.

## Working style

- Prefer a small number of substantial, verifiable tasks over many tiny speculative changes.
- Never claim tests, builds, deployments, or runtime behavior passed without evidence.
- Separate verified facts, assumptions, proposals, and open questions.
- Check existing files, issues, branches, and recent commits to avoid duplicate work.
- Do not introduce a large framework or paid service without explaining why it is needed.
- Do not mix PocketCode work with RevDev or other repositories.
- Keep the product provider-neutral unless a documented decision changes that direction.
- Optimize for an owner who may have only an iPhone and no PC access for an extended period.

## Git and public repository rules

- This repository is public. Never commit credentials, API keys, tokens, private user data, or secret configuration.
- Do not rewrite history, force-push, delete owner content, change repository visibility, publish a release, or enable paid infrastructure without explicit owner approval.
- Prefer focused commits and reviewable changes.
- Read existing files before replacing them and preserve owner-authored material unless asked to replace it.
- Do not add invented test results or placeholder success claims.

## Task protocol

1. Inspect relevant files and repository state.
2. State the goal and acceptance criteria.
3. Make the smallest coherent change.
4. Run available tests or clearly state why tests could not be run.
5. Inspect the diff/result.
6. Update project status and decision documents when state meaningfully changes.
7. Report exact changed paths, commit/PR references, test evidence, and remaining risks.

## Cross-agent collaboration

- Assign one primary implementer per task.
- Other agents review requirements, edge cases, tests, and diffs rather than independently implementing the same task.
- Use branches and pull requests for meaningful code changes when possible.
- Share findings with evidence and file/line references.
- Resolve conflicts through documented decisions, not by having multiple agents overwrite the same file.
- Keep CLAUDE.md and GEMINI.md aligned with this file.

## Product discipline

- Treat product direction as a hypothesis until validated.
- Do not implement a public code runner without reviewed isolation and abuse controls.
- Do not promise broad runtime support before a tested execution contract exists.
- Favor exportability, honest limitations, mobile usability, and verifiable execution evidence.

## Chat continuity and checkpoints

- For a new or resumed AI chat, read [AI_COLLAB/NEW_CHAT_BOOTSTRAP.md](AI_COLLAB/NEW_CHAT_BOOTSTRAP.md) and [AI_COLLAB/CURRENT_CHECKPOINT.md](AI_COLLAB/CURRENT_CHECKPOINT.md) before project work.
- Verify the repository's actual current branch head and compare it with the checkpoint SHA. The checkpoint is a resume index, not a substitute for source files or test evidence.
- Update `AI_COLLAB/CURRENT_CHECKPOINT.md` after meaningful progress. Add a dated, uniquely identified snapshot under `AI_COLLAB/checkpoints/`; preserve earlier snapshots as historical records rather than rewriting them to match later progress.
- Every checkpoint records exact commit/branch, work performed, changed paths, tests actually run and results (or why not run), remaining risks, approvals needed, and the next bounded task with acceptance criteria.
- Distinguish VERIFIED, PROPOSED, UNVERIFIED, NEEDS_LIVE_TEST, BLOCKED, and NEEDS_OWNER_APPROVAL. Chat claims and historical test notes are not fresh verification.
- Never merge a working branch, deploy, start paid or potentially billable workloads, enable billing, or create provider accounts without the required explicit owner approval.

## Open-source-first implementation policy

Before implementing a utility, algorithm, parser, protocol, security control, or framework feature, inspect whether the language standard library, an existing project component, or a reputable open-source package already solves the need. Prefer the smallest suitable, maintained, ecosystem-standard option; do not add a dependency merely to avoid a few clear lines of safe code.

For any proposed third-party dependency, record the package and version range, official source, license, maintenance/release health, compatibility with the project stack, known security/advisory status, transitive/deployment footprint, and the concrete benefit over the standard library or existing code. Verify current facts rather than relying on popularity or memory. Check repository manifests and existing dependencies before proposing a new one. Do not add a dependency until its fit and trade-offs are reviewed.

Reuse a reference implementation only after checking its provenance, license, maintenance, security assumptions, and compatibility with PocketCode's contract. Adapt only the relevant pattern; do not copy code blindly or silently change the product contract.

Custom code is appropriate when the behavior is genuinely product-specific, no suitable maintained solution fits, or a dependency would add disproportionate risk or complexity. Keep such code narrow and test edge cases. Security-critical behavior (including execution isolation, egress enforcement, authorization, idempotency, and trustworthy lifecycle/recovery decisions) must be backed by explicit guarantees and tests; a package's existence is not proof that these guarantees hold.

For the current report-contract helpers, the Python standard library is sufficient; do not add third-party packages unless a specific gap is demonstrated.
