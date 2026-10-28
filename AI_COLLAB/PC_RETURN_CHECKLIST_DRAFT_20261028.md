# PocketCode — PC-Return Checklist (Draft, 2026-10-28)

**Status:** Prepared checklist only. Not a command to merge, deploy, run provider workloads, or change billing. Review the current refs and explicit approvals again when a PC is available.  
**Parent plan:** [Four-month phone-only master plan](FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md).  
**Orientation:** [PocketCode Continuity Hub](POCKETCODE_CONTINUITY_HUB_20261028.md).

## 0. Hard stop rules

- Do not merge PR #2 or PR #3 or edit their branches without separate explicit authorization.
- Do not run GitHub Actions: the existing Pages workflow includes deployment.
- Do not create provider accounts, credentials, payment methods, paid trials, live sandboxes, or run submitted/untrusted code until a separate written test plan and owner approval explicitly permit it.
- The first PC session is for **repository verification and offline deterministic tests only**.
- No test result is assumed in advance. Capture actual interpreter version, exact commit, exact command, exit code, pass/fail/skip counts, output, and limitations.
- If a tool/package is unavailable, stop and record it; do not turn the first session into an installation/dependency hunt.

## 1. Re-establish the repository truth

Use a clean clone or dedicated Git worktrees. Keep the owner's existing working folder untouched unless they specifically choose otherwise.

1. Check Git and Python versions and the current working directory.
2. Fetch current main, PR #2's head, PR #3's head, and the AI Workflow Director research branch.
3. Record exact commit SHAs from live GitHub metadata; the October 2026 SHAs below are historical references only:
   - PR #2 previously observed:  eb8b7ea83cb0e8fe1880351276c485b761431791
   - PR #3 previously observed:  0ddcc0bc97bac5d446aefedf3d71f99411bd841d
4. Confirm PR #2/#3 remain open/draft/unmerged unless the owner has explicitly changed their state.
5. Save the outputs of git status --short --branch, git rev-parse HEAD, and the current branch refs to the evidence record.
6. Never test by combining files from different PR branches. Build a separate clean worktree for each exact ref.

Suggested inspection commands (adapt only if the actual environment requires it):

~~~sh
git --version
python --version
git status --short --branch
git fetch origin
git branch -avv
~~~

Use GitHub to verify current PR heads before using any pinned SHA. Do not assume this document's historical refs remain current.

## 2. Verify the exact checked-in files

For each branch being tested:

1. Check out a separate worktree at the exact verified commit SHA.
2. Capture git rev-parse HEAD.
3. Confirm critical file blob IDs with git rev-parse HEAD:path/to/file; compare them with the GitHub blob SHAs recorded for that exact branch/ref.
4. Record any mismatch before running a test; do not silently replace a local file with a version from another branch.
5. Save the original output outside the repository worktree if possible, or capture it in the continuity evidence record. Do not commit raw logs if they include private data.

## 3. Offline test order

### A. PR #2 — report and static-prototype utilities

In a dedicated worktree for the exact PR #2 head:

~~~sh
python -m unittest discover -s scripts -p 'test_*.py' -v
python scripts/check_mobile_prototype.py
~~~

Record exact file blob SHAs for:
- scripts/report_contract.py
- scripts/test_report_contract.py
- scripts/check_mobile_prototype.py
- scripts/test_check_mobile_prototype.py
- prototypes/mobile-runner/index.html

The PR description previously reported 25 tests passing in a temporary reconstruction on Python 3.13.5/Linux. Re-run the exact current source rather than assuming that historical result reproduces. The static prototype check inspects source patterns; it does not test browser interactions or real execution.

### B. PR #3 — pure lifecycle helper and synthetic tests

In a separate worktree for the exact PR #3 head:

~~~sh
python -m unittest discover -s scripts -p 'test_lifecycle_contract.py' -v
~~~

Optionally run the full Python unit discovery in that same dedicated worktree after confirming all discovered tests are local/offline and safe:

~~~sh
python -m unittest discover -s scripts -p 'test_*.py' -v
~~~

Record exact blob SHAs for:
- scripts/lifecycle_contract.py
- scripts/test_lifecycle_contract.py
- AI_COLLAB/DRAFT_EXECUTION_CONTRACT.md
- AI_COLLAB/OFFLINE_ACCEPTANCE_TEST_MATRIX.md
- AI_COLLAB/CONTRACT_CODE_TEST_TRACEABILITY_20261027.md

The PR #3 description reports 24 lifecycle test methods but explicitly states that the exact checked-in helper/test pair and full suite have NOT RUN. Method count is not a pass result. The helper uses synthetic caller-supplied evidence; strict local validation does not prove that provider evidence is authoritative, fresh, signed, transactionally stored, or bound to a real job/tenant.

### C. Main and AI Workflow Director research

Do not infer PR test results from main or the Director branch. Run only checks justified by files actually present at their exact refs.

- Inspect whether any new code was added before choosing a test.
- AWD-01–AWD-16 remain design-only until an implementation is explicitly authorized and actual tests are authored/run.
- Do not treat the Director's fixtures, profile prompts, decision register, or hand-authored reference outputs as automated tests or AI evaluation results.

## 4. Evidence record template

For every command, record one row with:

| Field | Required record |
|---|---|
| Workstream | main / PR #2 / PR #3 / Director branch |
| Exact revision | Branch name and commit SHA |
| Source identity | Relevant file paths and blob SHAs |
| Environment | OS, architecture if known, Python version, Git version |
| Command | Copy exact command line |
| Exit/result | Exit code and PASS/FAIL/SKIP/NOT RUN counts as actually printed |
| Output location | Where complete stdout/stderr is preserved |
| What this proves | Narrow scope of the test |
| What it does not prove | Browser, provider, isolation, network, cleanup, billing, or production gaps |
| Next action | Fix, inspect, rerun, or mark BLOCKED |

Use NOT RUN when not executed. Use BLOCKED when a prerequisite or approval is missing. Use INCONCLUSIVE when output/evidence cannot establish the expectation. Do not convert unavailable evidence to zero, success, or a guessed value.

## 5. Review findings before any integration

After offline tests:

1. Compare PR #2 report formatter verdict mapping to PR #3 detailed lifecycle fields, using [the cross-branch audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md).
2. Keep program execution outcome separate from cleanup, mandatory policy confirmation, artifact-release gates, and derived job disposition.
3. Review every failure, skipped test, and divergence from recorded expectations. Do not accept a green suite as proof of security properties that the tests do not exercise.
4. Produce a small review summary with exact paths/lines, a severity, and a recommended action. Do not write to PR branches in this step.
5. Ask for owner authorization only when a specific review/integration/implementation action is ready and all relevant prerequisites are explicit.

### 5A. Exact contract blockers to resolve before integration

Use the [source-to-test traceability map](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md) as the detailed index. These are review/design gates, not authorization to edit PR #2 or PR #3.

1. **Policy barrier before start:** prove that the coordinator/adapter confirms the exact mandatory policy revision on the intended execution boundary before the task-start call. A boolean `policy_confirmed`, acknowledgement, or ETag by itself is insufficient. The test must assert that the execute/start callback was never called for missing, pending, failed, late, stale, or mismatched policy evidence.
2. **Nonzero exit plus failed gates:** add a focused semantic case for `EXIT_NONZERO` with cleanup UNKNOWN/FAILED, policy evidence false/missing, and tenant/job authorization false. Preserve the observed process failure; define whether overall disposition is FAILED or INCOMPLETE; block artifact release independently in every unsafe case.
3. **Artifact release:** test cleanup, digest/integrity, job association and tenant authorization independently, including malformed truthy values. Existing pure-helper cases are useful but do not prove storage quarantine or real authorization.
4. **Cleanup recovery/history:** prove that later cleanup evidence creates a new report version and does not rewrite the earlier record. Offline model coverage does not prove durable/concurrent persistence.
5. **Terminal ordering and limits:** retain coordinator sequence, duplicate/conflicting terminal-event cases, and output cap + 1 behavior. Separate pure replay/byte-accounting results from actual process-tree termination, pipe draining and provider enforcement.

For each case, record exact source/test blob SHAs and whether the evidence is SOURCE-REVIEWED, TEST-RUN, NOT RUN, BLOCKED or PROVIDER-ONLY. No cross-branch file mixing; no integration change until the contract and owner/reviewer decisions are explicit.

## 6. Separate future gate: controlled real execution

This is **not part of the first PC-return session**. Before a provider test, revisit [the controlled Python proof runbook](../PRODUCT/CONTROLLED_PYTHON_PROOF_RUNBOOK.md), [security requirements](../SECURITY.md), and current provider research.

No live test may start until the owner explicitly approves the exact scope and:
- current official provider terms/tier and total-cost ceiling have been verified;
- no paid trial/payment method/billing activation is needed unless separately approved;
- mandatory egress policy is actually enforced on the exact job boundary before execution;
- resource/output limits, timeout, cancellation/termination, cleanup, artifact quarantine, and tenant authorization are testable;
- inputs are synthetic and contain no personal data or secrets;
- a controlled test matrix, stop criteria, and evidence-capture plan are reviewed.

If any gate cannot be established within the approved $0 boundary, do not run the workload.

## 7. Definition of a successful first PC session

The first session is successful when:
- exact current refs and file identities are recorded;
- safe offline tests have actual recorded outputs, or explicit blockers are documented;
- PR #2 and #3 were not changed;
- no Actions, deployment, provider, account, or cost action occurred;
- the next code review task is small, concrete, and supported by the evidence.

It is **not** successful merely because dependencies install, test methods exist, a provider is selected, or a simulated UI displays plausible output.
