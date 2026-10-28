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
- [Deterministic AWD conformance test specification](AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md) — assertion-level design for AWD-01–16, forbidden behaviors, cross-case invariants, and unresolved contracts; not implemented or run.
- [Offline evaluation kit](AI_WORKFLOW_DIRECTOR_EVALUATION_KIT_20261028.md) — canonical task profiles, cases EVAL-01 through EVAL-08, scoring rubric, and limitations.
- [Manual paired-run sheet](AI_WORKFLOW_DIRECTOR_MANUAL_RUN_SHEET_20261028.md) — exact phone-friendly baseline/Director prototype prompts and copyable fixtures.
- [Reference output fixtures](AI_WORKFLOW_DIRECTOR_REFERENCE_FIXTURES_20261028.md) — human-authored examples; do not show them to an assistant during measured runs.
- [Shared-core proposal](../PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md) — keep repositories separate and compare report/lifecycle contracts only against actual authoritative RevDev artifacts.

## Work completed in this pass

- Authored a deterministic conformance-test specification for all 16 proposed AWD acceptance cases, including required assertions, forbidden behaviors, boundary variants, capsule validation cases, and explicit unresolved contracts. The document is design-only; no test code was created or executed.

1. Audited the manual run sheet against the canonical evaluation kit.
2. Fixed the profile assignment mismatch: the old sheet had forced Balanced for every test. The current run sheet maps EVAL-01 to Lite, EVAL-02 to Balanced, EVAL-04 to Review only, EVAL-06 to Balanced, and EVAL-08 to Careful.
3. Aligned the run sheet's test prompts and toy context with the canonical EVAL-01, EVAL-02, EVAL-04, EVAL-06, and EVAL-08 cases.
4. Prioritized EVAL-06 (compact-checkpoint continuation) as the first pair to try when usage is scarce.
5. Added the human-authored EVAL-06 reference response; aligned EVAL-02/EVAL-04/EVAL-08 reference semantics with the canonical fixture definitions.
6. Clarified the Director prompt is a hand-authored prototype proxy, not output from a product implementation; it proves neither a working feature nor efficiency savings.
7. Added input prompt character count to the measurement form, alongside output characters and turns.
8. Added capsule provenance rules and proposed definitions for all six status values. Clarified that `READY_TO_VERIFY` is not a generic substitute for an unknown state.
9. Added a continuation-capsule integrity checklist covering status/evidence honesty, field preservation, provenance, and bounded next actions.
10. Reclassified the unsupported “tests passed” EVAL-08 reference as `BLOCKED` because the source revision, command, environment, and output needed to proceed are not available.
11. Added this durable checkpoint and linked it from the project README, master research, and evaluation kit.
12. No AI assistant runs, product tests, code execution, benchmark, deployment, merge, or paid action occurred in this pass.

## Next work sequence

### Pass A — Static protocol QA (completed for the current document set)
- [x] Verify the run sheet uses canonical task fixtures and profile assignments.
- [x] Make EVAL-06 the first suggested pair when usage is scarce.
- [x] Audit relative Markdown links in the touched project documents against the branch tree.
- [x] Check Markdown fence balance in the touched documents.
- [x] Recheck branch comparison and PR #2/#3 states; they remain separate and untouched.

### Pass B — Continuation capsule contract (design pass completed)
- [x] Define when each of the six proposed status values is appropriate.
- [x] Define provenance behavior for facts inherited from prior checkpoints.
- [x] Add explicit EVAL-06/EVAL-08 scoring guidance for missing evidence, unknowns, and `DONE_VERIFIED`.
- [ ] If scope is expanded later, turn these rules into static input/output fixtures for a deterministic local packet/capsule builder.

### Pass C — Owner/user evaluation when feasible
1. If only one pair can be afforded, run EVAL-06 baseline and Director prototype in the same AI app/model in fresh chats.
2. Save both full outputs and fill one record row per condition; mark any incomplete pair.
3. Apply the existing evaluation rubric only after both outputs are saved.
4. Do not claim product benefit from one sample. Repeat only if usage allows.

### Pass D — Later implementation review, only after owner review
1. Review the profile wordings and task/capsule fields in the MVP slice.
2. Build a deterministic local packet/capsule builder and static tests only after the owner wants implementation to begin.
3. Treat official provider-specific setup guides and any paid APIs as a separate later decision.
4. Map PocketCode/RevDev lifecycle/report concepts only after the actual authoritative RevDev artifacts are available for comparison. Do not infer field mappings from memory.

## Evidence boundaries

- Branch contents and GitHub status are the source for actual repository state.
- This checkpoint is a handoff, not a declaration that any future step has been completed.
- The research branch can contain proposed work that is not in `main`; never state otherwise.
- Before continuing, reread the current versions of the linked documents and verify branch/PR state rather than trusting the counts in this checkpoint.
