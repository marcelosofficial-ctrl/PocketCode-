# PocketCode — Current Work Checkpoint

**Checkpoint date:** 2026-10-28  
**Status:** Documentation/research branch only. No feature implementation or AI evaluation runs have occurred in this work pass.  
**Purpose:** Give a new chat or another AI enough verified state to continue without relying on old conversation context.

## Repository and branch state

- Repository: [marcelosofficial-ctrl/PocketCode-](https://github.com/marcelosofficial-ctrl/PocketCode-)
- Active isolated research branch: [pocketcode-ai-workflow-director-research-2026-10-28](https://github.com/marcelosofficial-ctrl/PocketCode-/tree/pocketcode-ai-workflow-director-research-2026-10-28)
- This branch is a research/documentation branch and is not `main`.
- PR #2 and PR #3 are separate ongoing draft work and must not be changed as part of this feature research. Before this checkpoint was authored, GitHub confirmed both were open, draft, and unmerged; re-check their live state before making any future statement about them.
- The latest known branch comparison before this checkpoint showed the branch ahead of `main` and not behind it. Re-run the compare after new changes before reporting exact counts.

## Product and working constraints

PocketCode remains a provisional, phone-first AI coding/workflow project. The central product hypothesis is to help a user create or receive code, run it in an appropriate isolated environment, inspect actual evidence, and bring a trustworthy report back to an AI assistant. The **AI Workflow Director** is a distinct proposed feature for compact task packets, portable continuity capsules, user-initiated handoff, and improved work discipline across AI assistants.

These are proposals, not a frozen product or proof of market demand. No runtime provider, live execution environment, paid API, account connection, or billing plan has been approved. Budget remains $0 unless the owner explicitly approves otherwise. Do not merge the PocketCode and RevDev repositories. Align any future shared concepts through verified contracts first.

Owner constraints for all future work:
- Phone-first, no PC access expected for months.
- Use GitHub docs as durable continuity.
- Prefer substantial, evidence-backed progress and multiple useful actions per pass.
- No secrets in the public repo.
- Do not merge/deploy, run Actions, install software, change account state, or spend money without explicit approval.
- Never claim code was run, a test passed, an artifact was integrated, or an AI evaluation occurred without evidence.
- A free-tier limit is a stopping condition, not something to evade.

## Relevant documents

- [Master AI Workflow Director research](MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md) — research synthesis and product proposal.
- [First testable feature slice](AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md) — proposed profiles, task packet, continuation capsule, static acceptance tests, and implementation sequence.
- [Offline evaluation kit](AI_WORKFLOW_DIRECTOR_EVALUATION_KIT_20261028.md) — canonical task profiles, cases EVAL-01 through EVAL-08, scoring rubric, and limitations.
- [Manual paired-run sheet](AI_WORKFLOW_DIRECTOR_MANUAL_RUN_SHEET_20261028.md) — exact phone-friendly baseline/Director prototype prompts and copyable fixtures.
- [Reference output fixtures](AI_WORKFLOW_DIRECTOR_REFERENCE_FIXTURES_20261028.md) — human-authored examples; do not show them to an assistant during measured runs.
- [Shared-core proposal](../PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md) — keep repositories separate and compare report/lifecycle contracts only against actual authoritative RevDev artifacts.

## Work completed in this pass

1. Audited the manual run sheet against the canonical evaluation kit.
2. Found and corrected a substantive mismatch: the old run sheet forced the Balanced profile for every test even though the canonical kit assigns Lite, Balanced, Review only, and Careful by case.
3. Aligned the manual fixtures with the canonical EVAL-01, EVAL-02, EVAL-04, EVAL-06, and EVAL-08 tasks and profiles.
4. Prioritized EVAL-06, the compact-checkpoint continuation case, as the first test if usage allows only one pair.
5. Added a human-authored EVAL-06 reference response and aligned the reference examples with the canonical task fixtures.
6. Clarified that the Director prompt is a hand-authored prototype proxy. It does not test an implemented packet builder and does not prove savings.
7. Added input prompt character count to the run record in addition to output characters, and kept token/cost claims explicitly out of scope.
8. No AI assistant runs, product tests, code execution, benchmark, deploy, merge, or paid action was performed.

## Key evaluation design rules

- Use the same AI app/model, plan, context, task, and tool availability for both conditions.
- Start with fresh chats and never show the assistant the reference fixture or scoring checklist.
- Record interruptions and confounders; do not reconstruct missing outputs.
- EVAL-06 is the best first case for chat-continuity value. A single pair is exploratory only.
- A future packet builder must be tested independently with deterministic static/unit tests; these manual AI runs do not replace those tests.
- Character counts are not tokens. Shorter is not better if correctness or evidence honesty declines.
- Do not treat assistant claims as execution evidence.

## Next work sequence

### Pass A — finish static protocol QA
1. Verify the updated run sheet and reference fixture for exact profile/task alignment with the canonical evaluation kit.
2. Check all relative Markdown links in the touched documents and scan for contradictory language such as “Balanced for every case,” “tested,” “implemented,” or unsupported savings claims.
3. Verify the branch comparison and confirm PR #2/#3 remain untouched.

### Pass B — strengthen the test plan without spending AI usage
1. Add a compact continuity-capsule schema checklist to the evaluation notes: required fields, unknown preservation, no secret/log dumping, and status evidence rule.
2. Decide whether EVAL-07 (limit-reached safe recovery) should be part of a later second batch; don't run it simply to fill a matrix.
3. Keep future implementation tasks independent from the broader hosted-code-execution provider decision.

### Pass C — owner/user evaluation when feasible
1. If only one pair can be afforded, run EVAL-06 baseline and Director prototype in the same AI app/model in fresh chats.
2. Save both full outputs and fill one record row per condition; mark any incomplete pair.
3. Apply the existing evaluation rubric only after both outputs are saved.
4. Do not claim product benefit from one sample. Repeat only if usage allows.

### Pass D — later implementation review, only after owner review
1. Review the profile wordings and task/capsule fields in the MVP slice.
2. Build a deterministic local packet/capsule builder and static tests only after the owner wants implementation to begin.
3. Treat official provider-specific setup guides and any paid APIs as a separate later decision.
4. Map PocketCode/RevDev lifecycle/report concepts only after the actual authoritative RevDev artifacts are available for comparison. Do not infer field mappings from memory.

## Evidence boundaries

- Branch contents and GitHub status are the source for actual repository state.
- This checkpoint is a handoff, not a declaration that any future step has been completed.
- The research branch can contain proposed work that is not in `main`; never state otherwise.
- Before continuing, reread the current versions of the linked documents and verify branch/PR state rather than trusting the counts in this checkpoint.
