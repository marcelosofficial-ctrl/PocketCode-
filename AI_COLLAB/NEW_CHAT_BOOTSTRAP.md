# PocketCode New-Chat Bootstrap

Use this file when starting a new ChatGPT, Claude, or Gemini conversation about PocketCode. GitHub is the durable source of truth; chat memory and copied summaries are not authoritative implementation evidence.

## Start here

1. Read [AGENTS.md](../AGENTS.md) and follow its rules.
2. Read [CURRENT_CHECKPOINT.md](CURRENT_CHECKPOINT.md).
3. Open the historical record linked from the current checkpoint. The latest review record is [PC-CP-2026-10-26-012](checkpoints/PC-CP-2026-10-26-012.md); earlier records 001 through 010 are historical snapshots.
4. Verify the repository's latest commit and branch state on GitHub. Compare the current checkpoint's recorded SHA with the actual current branch head. Do not assume this file's original branch or SHA remains current.
5. Read the relevant source, tests, and contract documents named by the active task. Prefer a targeted read over re-reading the entire repository.
6. Report any mismatch between the checkpoint and repository before making further changes. Source code, commit history, and actual test evidence outrank stale chat text.

## Compact project context

- Repository: https://github.com/marcelosofficial-ctrl/PocketCode-
- Product hypothesis: a phone-first workflow for running a small supported script, inspecting genuine output/errors/files, and copying a bounded report into any AI assistant.
- Current prototype is static and simulated; it does not execute submitted code.
- No production runtime, provider, backend, pricing model, or final brand is approved.
- Budget remains $0. Do not create provider accounts, enable billing, start potentially billable workloads, or use paid services without explicit owner approval.
- PocketCode and RevDev are separate repositories/projects. Do not merge them or assume shared implementation.
- The owner may have only an iPhone and no local PC/developer tools. Keep next steps practical in that constraint.

## Rules for every resumed task

- One primary implementation task at a time; do substantial, bounded work per pass.
- State the task goal and acceptance criteria before changing code.
- Inspect the existing files and current branch before replacing or editing anything.
- Use a separate branch and reviewable pull request for meaningful changes when practical. Do not merge without explicit approval.
- Never claim tests, builds, deployments, browser behavior, security properties, or real execution passed without actual evidence.
- Record the exact test command, exit/result, environment limitations, and source of evidence. A historical test result is not a fresh test run.
- Separate VERIFIED, PROPOSED, UNVERIFIED, NEEDS_LIVE_TEST, BLOCKED, and NEEDS_OWNER_APPROVAL claims.
- Never commit secrets, tokens, credentials, private user data, or production configuration to this public repository.
- Do not enable paid infrastructure, publish a release, deploy a runner, or make irreversible changes without the owner's explicit approval.
- Do not rerun a potentially billable/side-effecting operation to “recover” an uncertain result; inspect evidence first.
- Update `AI_COLLAB/CURRENT_CHECKPOINT.md` after meaningful progress and add a new record under `AI_COLLAB/checkpoints/`. Keep previous checkpoint records historical and do not rewrite them to match later state.
- Update `PROJECT_STATUS.md` and `DECISIONS.md` only when the actual project status or a decision meaningfully changes; don't duplicate all checkpoint details into them.

## Checkpoint minimum fields

Every checkpoint must include:
- unique checkpoint ID, stage, status, date, repository, branch and exact base/head commit SHA;
- exact files inspected/changed and relevant blob/commit links;
- completed work and what is still only proposed;
- test commands and observed results, or a clear statement that tests were not run and why;
- unresolved risks, dependencies, decisions, and required owner approvals;
- one next task with acceptance criteria.

## Baseline at bootstrap creation (historical)

The initial checkpoint is `PC-CP-2026-10-26-001`, anchored to baseline commit `555840d8d83342513d9cd353d4d1522d46a5c82d`. The latest checkpoint record is `PC-CP-2026-10-26-012`; it records 25 passing unit tests and a passing standalone checker run against GitHub-blob-hash-verified Python and prototype HTML files. Draft PR #2 remains unmerged. The next product task should use a separate branch and begin by reading the master research plan and Gemini handoff. Always verify the latest branch head and checkpoint before acting.

## Copy/paste opening prompt

```text
Continue my PocketCode project from GitHub. First read AGENTS.md, AI_COLLAB/CURRENT_CHECKPOINT.md, and the checkpoint record it references. Verify the current repository commit/branch and inspect the relevant source/tests before acting. Treat GitHub evidence as authoritative, not chat memory. Continue the first unfinished task in the current checkpoint, doing substantial work per pass. Do not claim tests or runtime behavior passed unless actually verified. Preserve the $0 budget, do not create accounts/start workloads/enable billing/deploy/merge without explicit owner approval, and do not expose secrets. At the end, report exact changed paths, commit/PR refs, test commands/results, unresolved risks, and update the checkpoint plus a new historical record.
```

## Open-source-first development rule

Before writing custom utility/algorithm/framework code, check the standard library, existing repository code, and reputable maintained ecosystem packages. Prefer reuse where it reduces risk and complexity, but do not add dependencies automatically. For a third-party package, verify the official source, current maintenance, license, compatibility, security/advisory status, dependency footprint, and concrete benefit; document the decision. Check existing manifests before adding anything. Review reference code's provenance/license/security assumptions before adapting it. Keep product-specific logic narrow and tested. Security guarantees such as isolation, network egress restrictions, idempotency, cancellation, and reliable run recovery must be explicitly proven; a library name alone is not proof. For the current Python report-contract helper, standard-library modules are sufficient unless evidence demonstrates a concrete gap.
