# PocketCode — Current Work Checkpoint

**Checkpoint date:** 2026-10-28  
**Status:** Documentation/research branch only. No feature implementation or AI evaluation runs have occurred in this work pass.  
**Purpose:** Give a new chat or another AI enough verified state to continue without relying on old conversation context.

## Repository and branch state

- Repository: [marcelosofficial-ctrl/PocketCode-](https://github.com/marcelosofficial-ctrl/PocketCode-)
- Active isolated research branch: [pocketcode-ai-workflow-director-research-2026-10-28](https://github.com/marcelosofficial-ctrl/PocketCode-/tree/pocketcode-ai-workflow-director-research-2026-10-28)
- This branch is a research/documentation branch and is not `main`.
- PR #2 and PR #3 are separate ongoing draft work and must not be changed as part of this feature research. Rechecked after this pass: both remain open, draft, and unmerged. PR #2 head is `eb8b7ea83cb0e8fe1880351276c485b761431791` on `chat-continuity-report-regressions-2026-10-26`; PR #3 head is `0ddcc0bc97bac5d446aefedf3d71f99411bd841d` on `pocketcode-pass0-audit-2026-10-26`. Their branches were not modified by this work.
- The latest comparison during this pass showed the research branch ahead of `main` and not behind it; the compare endpoint listed the canonical fixture catalogue as a new path. Exact commit counts change with documentation commits, so re-run the comparison before reporting counts in a later session.

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

- [PocketCode Continuity Hub](POCKETCODE_CONTINUITY_HUB_20261028.md) — read-first project map, source-of-truth order, branch separation, AI roles, and evidence boundaries.
- [Four-month phone-only master plan](FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md) — dated workstreams, monthly exits, zero-budget constraints, future feature tiers, and PC-return readiness.
- [PC-return checklist draft](PC_RETURN_CHECKLIST_DRAFT_20261028.md) — exact-ref verification, isolated offline test sequence, evidence template, and a separately gated provider path.
- [Execution-contract cross-branch audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md) — current/main vs PR #2 and PR #3 status semantics; static-only, no tests run.
- [Phone-only competitor scan addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md) — additional current project claims, source caveats, and task-comparison questions.
- [Product hypothesis card](PRODUCT_HYPOTHESIS_CARD_20261028.md) — provisional target user/job, alternatives, evidence gaps, and falsification criteria.
- [Fixed-task comparison worksheet](PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md) — synthetic CSV-to-JSON success/failure protocol and evidence record; not executed.
- [Complete new-chat handoff](NEW_CHAT_HANDOFF_20261028.md) — consolidated mission, constraints, three-AI roles, exact refs/PR state, evidence boundaries, four-month plan, and next task.
- [Master AI Workflow Director research](MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md) — research synthesis and product proposal.
- [First testable feature slice](AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md) — proposed profiles, task packet, continuation capsule, static acceptance tests, and implementation sequence.
- [Deterministic AWD conformance test specification](AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md) — assertion-level design for AWD-01–16, forbidden behaviors, cross-case invariants, and eight recommended v1 contract defaults; not implemented or run.  
- [Canonical AWD fixture catalogue](AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES_20261028.md) — proposed concrete input envelopes and observable pass/fail boundaries for all 16 IDs, with forbidden behaviors, layer boundaries, traceability, and unresolved contract dependencies; design-only, NOT RUN.
- [Contract reconciliation and decision register](AI_WORKFLOW_DIRECTOR_CONTRACT_DECISION_REGISTER_20261028.md) — compares all eight proposed defaults with the MVP, separates established semantics from open exact contracts, and recommends a minimal implementation gate; not owner-approved.
- [Pre-implementation readiness audit](AI_WORKFLOW_DIRECTOR_READINESS_AUDIT_20261028.md) — focused review of AWD-08/11/12/14, prioritized decision classes, and a minimal offline-builder scope proposal; static review only.
- [Bounded implementation plan](AI_WORKFLOW_DIRECTOR_BOUNDED_IMPLEMENTATION_PLAN_20261028.md) — dependency-ordered work packages, AWD mappings, evidence requirements, and the minimal contract gate; proposal only, no implementation authorization.
- [Offline evaluation kit](AI_WORKFLOW_DIRECTOR_EVALUATION_KIT_20261028.md) — canonical task profiles, cases EVAL-01 through EVAL-08, scoring rubric, and limitations.
- [Manual paired-run sheet](AI_WORKFLOW_DIRECTOR_MANUAL_RUN_SHEET_20261028.md) — exact phone-friendly baseline/Director prototype prompts and copyable fixtures.
- [Reference output fixtures](AI_WORKFLOW_DIRECTOR_REFERENCE_FIXTURES_20261028.md) — human-authored examples; do not show them to an assistant during measured runs.
- [Shared-core proposal](../PRODUCT/REVDEV_POCKETCODE_SHARED_CORE.md) — keep repositories separate and compare report/lifecycle contracts only against actual authoritative RevDev artifacts.

## Work completed in this pass

- Authored a deterministic conformance-test specification for all 16 proposed AWD acceptance cases, including required assertions, forbidden behaviors, boundary variants, capsule validation cases, and explicit unresolved contracts. The document is design-only; no test code was created or executed.
- Added eight recommended v1 defaults for unresolved contracts (input normalization, packet serialization, character counting, oversized-context behavior, configured redaction, capsule validation, share-adapter results, and component boundaries). These are recommendations, not frozen decisions.
- Authored the canonical fixture catalogue with proposed repeatable input envelopes, observable pass/fail rules, forbidden behaviors, traceability, layer boundaries, and unresolved dependencies for AWD-01–AWD-16. This is design-only; no test code was created or executed.
- Reconciled the eight proposed conformance defaults against the MVP and all 16 fixture meanings in a decision register. Marked existing semantic requirements separately from exact open contracts; no recommendations were treated as accepted decisions.
- Audited the register against the MVP and fixture catalogue: all eight proposed contracts are represented; AWD-01–AWD-16 each have a traceability row; current MVP-supported semantics are separated from exact open choices. The register remains advisory, and no owner decision or implementation authorization was inferred.
- Completed a focused readiness audit for AWD-08 (omissions), AWD-11 (unsupported verification claims), AWD-12 (configured redaction), and AWD-14 (cancelled sharing). Separated must-have semantic invariants from open implementation details and explicitly deferred integrations.
- Added a bounded implementation plan with G0–G8 work packages and acceptance mappings. G0–G5 describe the proposed core sequence; redaction, real sharing, and manual AI comparison are separately gated. The plan does not authorize implementation. Added an explicit AWD-01–AWD-16 traceability table so every existing acceptance ID maps to a work package without redefining its meaning.
- Linked the readiness audit from the README, master research, canonical fixture catalogue, and checkpoint. Static review of the new feature documents confirms the 16 fixture IDs and 16 register rows align; code fences are balanced. A broad README link scan was inconclusive for older unrelated links because their target files were outside the fetched audit set, so no repository-wide broken-link claim is made.
- Audited the overall project hierarchy, current product goals, zero-budget rules, main-vs-PR branch boundaries, and existing three-AI method. Added a read-first continuity hub and a four-month phone-only plan ending 2027-02-28. Kept the core execution/evidence loop primary and the AI Workflow Director supporting; neither PR #2 nor PR #3 was edited.
- Completed a static cross-branch execution-contract audit using exact refs/blob SHAs for main, PR #2, and PR #3. Key gap: PR #3's richer execution_outcome/cleanup_state/job_disposition needs a versioned projection into the user-facing PASS/FAIL/INCOMPLETE verdict. Its exact policy-revision barrier is a safety refinement; numeric output/tombstone values remain test-only defaults. No code was changed and no tests were run by the audit.
- Added [phone-only competitor scan addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md) for current Android local coding agents and phone steering clients, and [product hypothesis card](PRODUCT_HYPOTHESIS_CARD_20261028.md) with alternative explanations and falsification criteria. These are source-led research inputs, not hands-on testing or market validation.



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

### Pass A — Static protocol QA (completed)
- [x] Align the manual run sheet with canonical EVAL cases and profile assignments.
- [x] Prioritize EVAL-06 when usage is scarce.
- [x] Audit local links and Markdown fence balance across the current document set.
- [x] Recheck branch comparison and PR #2/#3 states; both remain separate and untouched.

### Pass B — Continuation capsule contract (design complete; not implemented)
- [x] Define the six proposed status meanings and evidence/provenance rules.
- [x] Add capsule-integrity scoring guidance for EVAL-06/EVAL-08.
- [x] Add human-authored reference fixtures without claiming AI performance.

### Pass C — Deterministic AWD conformance design (documented; NOT RUN)
- [x] Define required assertions and forbidden behavior for AWD-01 through AWD-16.
- [x] Add cross-case invariants, capsule-validation cases, deterministic test-suite boundaries, and eight open contracts.
- [x] Propose minimal v1 defaults without treating them as accepted/frozen.
- [x] Link the specification from the MVP slice, master research, evaluation kit, README, and this checkpoint.
- [x] Reconciled proposed defaults and completed a focused readiness audit. Do not freeze contracts by implication; minimum decisions still require explicit owner authorization before implementation.
- [x] Established an overall continuity/source-of-truth map and a four-month phone-only coordination plan; this plan is an overlay, not a replacement for the product roadmap or branch-specific contracts.
- [x] Create a canonical catalogue with proposed fixture inputs and observable pass/fail boundaries for AWD-01–AWD-16; audit coverage and label unresolved dependencies.
- [x] Reconcile the eight proposed defaults against the MVP and fixture catalogue; record existing semantics, exact open contracts, deferred scope, and the minimum implementation gate. This is analysis, not owner approval.
- [x] Audit the decision register for unsupported assumptions and traceability: eight contract rows D-01–D-08, all 16 AWD IDs mapped, no recommendation marked owner-approved, and Markdown fences balanced. The register is linked from the MVP, conformance spec, master research, checkpoint, and README.
- [ ] Create executable tests only after implementation is authorized.

### Current phone-only overlay — active next steps
- [x] Audit main product/security/execution contracts against PR #3 source on exact refs; findings are in the cross-branch audit document.
- [x] Add a dated delta for newly surfaced local-phone/remote-agent competitors without copying PR #3's broader research.
- [x] Create a product hypothesis card with alternatives and falsification criteria; no market validation claimed.
- [x] Reconcile dated competitor deltas into the existing matrix and competitive analysis on this isolated branch; add source caveats and links. The PR #3 branch remains untouched.
- [x] Draft the compact PC-return checklist; exact branch/blob verification, offline tests first, test output capture, and a separately gated provider test are documented. Provider/spend/merge/deployment/Actions gates remain closed.
- [x] Define the fixed synthetic CSV-to-JSON success/failure task and scoring/evidence fields. No apps were installed; the comparison remains NOT RUN.
- [x] Complete the scoped static audit: all 18 relative links in the new handoff resolve on this branch; reviewed Markdown fences are balanced; README start order and handoff navigation are correct. Current branch comparison was 133 ahead/0 behind at the pre-refresh snapshot; recheck because these documentation updates advance HEAD. PR #2/#3 remain open, draft, unmerged with known heads unchanged.
- [ ] Review the advisory PASS/FAIL/INCOMPLETE projection against the detailed outcome/cleanup/disposition contract, and record only genuine contradictions or open owner decisions. Do not create more master docs unless they remove a material blocker.


### Pass D — Manual AI evaluation when feasible
1. If only one pair can be afforded, run EVAL-06 baseline and Director prototype in the same AI app/model in fresh chats.
2. Save both full outputs and fill one record row per condition; mark any incomplete pair.
3. Score only after both outputs are saved. Keep the result exploratory.
4. Stop at any free-tier limit; do not evade quotas or pay to finish.

### Pass E — Implementation review, only after explicit owner approval
1. Review/freeze the four profile wordings, packet serialization, capsule validation, and local redaction defaults.
2. Implement a pure deterministic local packet/capsule builder and tests for AWD-01–16.
3. Add preview/edit/copy UI; test the share adapter separately on real devices later.
4. Treat provider-specific guides and paid APIs as separate future decisions.
5. Map PocketCode/RevDev lifecycle/report concepts only after the actual authoritative RevDev artifacts are available. Do not infer field mappings from memory.

## Evidence boundaries

- Branch contents and GitHub status are the source for actual repository state.
- This checkpoint is a handoff, not a declaration that any future step has been completed.
- The research branch can contain proposed work that is not in `main`; never state otherwise.
- Before continuing, reread the current versions of the linked documents and verify branch/PR state rather than trusting the counts in this checkpoint.

## Follow-up pass — static link and contract projection findings (2026-10-28)

**Status:** Static GitHub-source review only. No code was executed, no tests were run, and no PR #2/#3 or main-branch files were changed.

### Continuity-link check

- Re-fetched the handoff, Continuity Hub, Four-Month Plan, Current Checkpoint, Execution-Contract Audit, Product Hypothesis Card, Fixed-Task Worksheet, PC-Return Checklist, and Competitor Scan Addendum from this branch.
- Compared relative Markdown file links in those nine documents against the branch's recursive Git tree. All checked relative file targets exist (0 missing file targets across the checked documents).
- This check did not validate URL availability, fragment/heading anchors, links in every other Director specification, or rendering. Do not describe it as a full repository link audit.

### Material contract-projection finding

Exact source blobs rechecked:

- main `PRODUCT/EXECUTION_CONTRACT.md`: `3861e51ae4f9e45a263b677402f26c41b240959d`
- PR #2 `scripts/report_contract.py`: `e9d944a722c2fac5279952696528da72a7011af3`
- PR #3 `AI_COLLAB/DRAFT_EXECUTION_CONTRACT.md`: `02ad9934cc40c84f7e8cd7f6c982d5d8ed7d1b70`
- PR #3 `scripts/lifecycle_contract.py`: `ba8d4d0b217c90513bed020e298029ef4e16f164`

PR #2's pure formatter classifies `execution_status == "succeeded"` plus a valid exit code of zero as `PASS`. It does not itself receive or evaluate the PR #3 draft's separate mandatory policy-revision confirmation, termination evidence, artifact-manifest/integrity checks, tenant/job association, or cleanup state. The formatter docstring correctly says it does not verify the trustworthiness of its input, so this is not proof of a bug in the isolated formatter; it is an integration/projection gap if a caller treats its status and exit-code inputs as sufficient for the overall job verdict.

PR #3 explicitly requires those additional gates before overall `PASS`; for example, zero exit with `cleanup_state != CONFIRMED` derives `INCOMPLETE`. Main's current contract describes a simpler lifecycle/reporting model and does not yet define a complete versioned projection from the PR #3 multi-axis record into the PR #2 verdict. Preserve the earlier audit recommendation: define the trusted caller boundary and versioned projection before any provider integration or schema freeze. Never infer that PR #3 helper behavior has been integrated into main or PR #2.

### Evidence boundaries

- Fixed-task worksheet remains design-only: no app install, mobile execution, benchmark, or user study.
- PR #2's prior reported pure-helper test evidence is branch-specific and does not establish live runner/security behavior.
- PR #3 helper/test pair remains recorded as NOT RUN in its draft evidence; a test-method count is not a pass result.
- AWD-01–AWD-16 remain design-only and NOT RUN.

### Next highest-value work

1. Complete relative-link and anchor validation for the remaining Director specifications and source-of-truth documents on the exact research branch.
2. Draft a compact projection table that explicitly identifies which trusted component owns each gate, the evidence required, the displayed verdict, and what details must remain visible. Treat it as a proposal, not an approved schema.
3. Keep product-alternative comparison separate from the execution-contract audit; no architecture/provider choice follows from this static finding alone.

## Follow-up pass: Director and product comparison review (2026-10-28)

**Status:** Static source review only. No implementation, test execution, AI evaluation, app install, or mobile benchmark was performed.

### AI Workflow Director

Reviewed the MVP slice, AWD-01–16 conformance specification and canonical fixture catalogue, reference outputs, decision register, readiness audit, bounded implementation plan, offline evaluation kit, manual run sheet, and master research document. The documents consistently identify themselves as proposals and keep the AWD IDs/meanings under the MVP's authority. No reason was found to remap fixture IDs or claim implementation/test success.

The remaining bottleneck is a small owner decision gate, not more fixtures: choose the first-slice boundary; define deterministic goal/profile and optional-input handling; settle serialization only to the degree required for tests; preserve protected literals; keep oversize handling non-destructive; and either define capsule invalid/unknown-field behavior or defer capsule import/export. Character count can be deferred. Redaction and real sharing should remain separately scoped. These are recommendations, not approved decisions or implementation authorization.

### Fixed-task comparison worksheet

Re-read the existing worksheet. It already has a useful fair-comparison protocol: one deterministic CSV success case and one malformed-input failure case; separate documented claims from direct observation; record real setup actions and timing; mark unknowns as U rather than zero/free/PASS; let safety/correctness disqualifiers override convenience; and avoid a total score if a critical dimension is unobserved. No additional worksheet or duplicate scorecard is warranted now.

### Next work

1. Finish a branch-specific relative-link and heading-anchor audit for the core continuity and Director documents.
2. Keep product alternative evidence and execution-contract review separate.
3. Continue non-blocking phone-only research; do not request implementation decisions until a concrete decision changes the next work, and do not imply that any manual comparison has run.

## Follow-up pass: expanded relative-link integrity check (2026-10-28)

**Result:** PASS for relative Markdown file-target existence across the 14 documents listed below. This is a static path check against the research branch's recursive Git tree; it does not verify external URLs, every heading anchor, rendered Markdown, or semantic correctness.

- Core continuity: `NEW_CHAT_HANDOFF`, `POCKETCODE_CONTINUITY_HUB`, `FOUR_MONTH_PHONE_ONLY_MASTER_PLAN`, `POCKETCODE_CURRENT_CHECKPOINT`.
- Director contract/test design: `AI_WORKFLOW_DIRECTOR_MVP_SLICE`, `AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC`, `AI_WORKFLOW_DIRECTOR_CONTRACT_DECISION_REGISTER`, `AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES`, `AI_WORKFLOW_DIRECTOR_REFERENCE_FIXTURES`, `AI_WORKFLOW_DIRECTOR_EVALUATION_KIT`, `AI_WORKFLOW_DIRECTOR_MANUAL_RUN_SHEET`.
- Product and readiness: `PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET`, `PC_RETURN_CHECKLIST_DRAFT`, `PRODUCT_HYPOTHESIS_CARD`.

The review covered 141 relative Markdown links; zero pointed to a file path absent from the branch tree. Fetches and file-tree comparison are not application tests. Some heading anchors and all external destinations remain outside this pass.

**Next work:** review exact acceptance/provenance semantics across the report lifecycle and Director boundary; do not expand the document set merely to inflate coverage. Then check PR state and update this checkpoint with the next material finding. No PR was edited, no tests were run, and no implementation is authorized by this result.

## Follow-up pass: report/lifecycle integration seam and PR boundary recheck (2026-10-28)

- Expanded the execution-contract audit with exact source and test blob IDs from `main`, PR #2, and PR #3. See [Execution Contract Cross-Branch Audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md), section “Follow-up evidence: acceptance tests clarify the integration seam.”
- Refined finding: PR #2's formatter is a presentation helper, so its narrow status/exit-code classification is not by itself proof of a defect. The risk is a caller bypassing the PR #3-style trusted disposition derivation. The intended sequence is authoritative observations → versioned disposition derivation → report formatting. Execution outcome and job disposition are separate axes.
- PR #3's lifecycle tests include assertions for cleanup, policy, termination, artifact validity and tenant/job authorization gates; PR #2's report tests cover lifecycle states, missing/invalid exit codes, simulated reports and bounded output. These are source-level test definitions only; no tests were executed in this pass.
- Rechecked GitHub PR metadata through the API: PR #2 remains open/draft, head `chat-continuity-report-regressions-2026-10-26`, head SHA `eb8b7ea83cb0e8fe1880351276c485b761431791`; PR #3 remains open/draft, head `pocketcode-pass0-audit-2026-10-26`, head SHA `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`. Neither PR was changed.
- The last verified comparison before this checkpoint update was 145 commits ahead of `main`, zero behind. This checkpoint update adds another commit, so future chats must recheck the current count instead of treating 145 as current.

**Next pass:** define a minimal versioned vocabulary/projection table as a proposal inside the existing audit, then audit the product fixed-task protocol and the external-source evidence boundary. Do not merge, change either PR, run provider workloads, or imply any code/test execution.

## Follow-up pass: explicit two-axis projection and fixed-task sanity check (2026-10-28)

- Added a proposed two-axis vocabulary/projection table to the existing [Execution Contract Cross-Branch Audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md). It distinguishes execution observations (`NOT_STARTED`, `EXIT_ZERO`, `EXIT_NONZERO`, `TIMED_OUT`, `CANCELLED`, `LIMIT_EXCEEDED`, `UNKNOWN`) from derived job dispositions (`REJECTED`, `PASS`, `FAILED`, `TIMED_OUT`, `CANCELLED`, `LIMIT_EXCEEDED`, `PROVIDER_ERROR`, `INCOMPLETE`) and maps the latter conservatively to a simple user-facing verdict.
- This proposal remains unapproved. It explicitly preserves nonzero-exit observations when cleanup is uncertain, separates artifact release from process outcome, and requires the formatter to render an already-derived disposition rather than infer security gates.
- Sanity-checked the existing fixed task: notebook subtotal `2 × 3.50 = 7.00`, pen subtotal `3 × 1.25 = 3.75`, grand total `10.75`, two line items. The malformed-input case requires a clear error and no misleading valid summary. The arithmetic and success/failure distinction are internally consistent; no worksheet change was needed.
- No tests were run, no mobile runner or provider was exercised, and no product alternative has been hands-on compared. PR #2 and PR #3 remain untouched.

**Next pass:** do a focused external-source refresh on the few alternatives most likely to falsify the current product hypothesis (local iOS Python/WASM, Android-local coding workspaces, and remote-PC control), then record only material changes to the existing competitor matrix/addendum. Keep documented claims separate from observed results; no install or execution claim without a real attempt.

## Follow-up pass: current mobile alternative refresh (2026-10-28)

- Updated the existing [Phone-Only Competitor Scan Addendum](PHONE_ONLY_COMPETITOR_SCAN_ADDENDUM_20261028.md) with current primary-source claims for Pyodios, AndroidHarness, PhoneCode and Pairlet, and added Mobile Harness from F-Droid as a newly surfaced Android-local alternative.
- Material update: Pairlet's current repository advertises v1.9.4 and six agent backends, but remains host-dependent; its published security page says the custom encrypted channel has not received an independent audit. Encryption does not establish sandboxing.
- Pyodios remains a strong iOS-local comparator for the fixed standard-library task; its own FAQ documents startup initialization, a roughly 300 MB Python memory budget, and session reset between launches. These are source claims, not independent measurements.
- AndroidHarness, PhoneCode and Mobile Harness make a generic “AI coding on a phone without a PC” promise less differentiated. The hypothesis must instead show task-specific value in setup friction, truthful execution evidence, portable reports, continuity, or safety.
- No app was installed, no fixed-task run was performed, no timing/correctness scores were recorded, and no market/user validation occurred. All such fields remain NOT RUN.

**Next pass:** re-verify the exact research branch and PR boundaries, then prepare a compact decision-ready summary of what is settled, what remains unknown, and which next tasks can be done without owner action. Do not create another master document or ask for broad approvals prematurely.

## Final verification for this work session (2026-10-28)

- Latest pre-checkpoint-update GitHub comparison: research branch was 145 commits ahead of `main`, zero behind. Recompute after this commit before quoting a current count.
- PR #2 remains open/draft on `chat-continuity-report-regressions-2026-10-26` at head `eb8b7ea83cb0e8fe1880351276c485b761431791`; PR #3 remains open/draft on `pocketcode-pass0-audit-2026-10-26` at head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`. Neither was modified.
- Current research work is confined to the isolated research branch. No merge, deployment, GitHub Actions run, app install, provider workload, implementation test, or user research occurred.
- Next batch is ready: complete the remaining scoped anchor/external-link checks; challenge the proposed two-axis disposition projection against reviewer feedback if available; then turn the product alternatives into a one-at-a-time, evidence-preserving fixed-task protocol. The hands-on comparison remains NOT RUN and needs an explicit owner action only when the exact phone/app test is selected.

## Follow-up pass — fixed-task protocol and lifecycle gate-ordering review (2026-10-28)

### Fixed-task worksheet tightened

Updated [Fixed-Task Comparison Worksheet](PRODUCT_FIXED_TASK_COMPARISON_WORKSHEET_20261028.md) with a reproducible attempt protocol. It now specifies UTF-8/LF inputs, separate fresh workspaces for success and malformed-header scenarios, expected JSON value types, no stale success artifact after failure, ordered evidence capture, actual-file verification, setup/run timing, explicit UNKNOWN/UNAVAILABLE values, disqualifiers, and a copyable per-attempt record.

This is still **DESIGN ONLY / NOT RUN**. No mobile app was installed, no script was executed in a mobile environment, no account/provider was used, and no benchmark result is claimed. The key anti-false-positive is a fresh workspace for the malformed input, so an old summary.json cannot be mistaken for a valid result.

### Lifecycle/disposition review sharpened

Updated [Cross-Branch Execution-Contract Audit](EXECUTION_CONTRACT_CROSS_BRANCH_AUDIT_20261028.md) after inspecting the exact PR #2 and PR #3 helper sources. Static review confirms that PR #3 derive_disposition returns FAILED for EXIT_NONZERO before checking cleanup, policy confirmation, termination confirmation, artifact validity, or tenant/job authorization. Contradictory evidence is checked earlier.

This ordering may intentionally preserve a confirmed process failure, but the helper's output is called a job disposition. The external contract must explicitly decide whether nonzero exit plus an unconfirmed/failed mandatory gate means FAILED with a separate gate warning, or INCOMPLETE with EXIT_NONZERO preserved as a separate observation. Artifact release must remain independently fail-closed either way. The PR #3 pure helper cannot itself prove the provenance of NOT_STARTED or that a policy confirmation is bound to the exact required revision and applied before start.

**Reviewer decision remains open.** Ask Claude and Gemini to independently review this narrow FAILED-vs-INCOMPLETE/gate-ordering question before integration approval. Do not edit PR #2 or PR #3; no tests were run.

### Scoped static documentation link check

On the research branch tree at commit 5bfe97068168d5e1cbbea9fa22fcee0d89c07a16, checked 8 high-priority documents (handoff, continuity hub, four-month plan, this checkpoint, Director MVP slice, Director conformance spec, fixed-task worksheet, and cross-branch contract audit).

- 109 relative Markdown link targets were resolved against the branch tree: **0 missing paths** in this scoped set.
- 32 external URL references were identified but not fetched/validated as live links.
- The scoped files contain no fragment-only Markdown anchors; no heading-anchor validation was needed for this set.
- This is not a repository-wide link audit and does not validate rendered Markdown, every external URL, or uninspected files.

### Repository/PR state rechecked before this checkpoint refresh

- Research branch was 148 commits ahead and 0 behind main; compare base SHA was 555840d8d83342513d9cd353d4d1522d46a5c82d. The branch head at the comparison was 5bfe97068168d5e1cbbea9fa22fcee0d89c07a16. Counts/head will advance with this checkpoint update.
- PR #2 remains open, draft, unmerged at eb8b7ea83cb0e8fe1880351276c485b761431791.
- PR #3 remains open, draft, unmerged at 0ddcc0bc97bac5d446aefedf3d71f99411bd841d.
- Neither PR branch was modified.

### Next bounded pass

1. Ask for independent Claude/Gemini challenge of the exact disposition-ordering issue above, if their review can be obtained without PC access or paid usage.
2. In parallel, audit the remaining relevant contract definitions and tests for contradictory expectations, focusing on whether artifact release is explicitly independent from verdict and whether policy-revision evidence is bound to the attempt.
3. Keep product comparison as a design protocol until an owner-chosen hands-on phone session is possible. Do not turn desk research into performance claims.
4. Recheck branch/PR state after material updates. No owner action is required for the static work completed here.

