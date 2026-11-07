# NEXT TASK: P39 independent adversarial review reconciliation

## Goal
Obtain and reconcile two independent, source-pinned reviews of the release-grant recovery/concurrency design before correcting the reference model or selecting/planning a durable adapter.

## Reviewer assignments
- Claude: architecture, transaction linearization, receipt-head races, stable-intent/auth separation, outbox atomicity/order, fencing and stream effects.
- Gemini: caller/producer trust boundary, tenant isolation, replay/revocation, event identity/digest/order, fence authority, source/license claims and adversarial tests.

## Exact review inputs
Forward both documents:
1. P39 brief: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/4c9d17b818fd823eff5e183e6728655262446336/AI_COLLAB/P39_INDEPENDENT_REVIEW_PROMPT_20261107.md
2. ChatGPT source-pinned static audit addendum: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/fd013786ef6daa4c13f2dce14f9782f13e43655d/AI_COLLAB/P39_CHATGPT_STATIC_AUDIT_ADDENDUM_20261107.md

The immutable pins are:
- P39 documentation snapshot: `04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0`
- Source and tests: `744cb4dc7cd4994647c84ac7476d0c78a21f0540`
- P39 review brief: `4c9d17b818fd823eff5e183e6728655262446336`
- Supplemental audit addendum: `fd013786ef6daa4c13f2dce14f9782f13e43655d`

Use immutable links in the addendum, not branch-floating paths. If any file is inaccessible, report NOT REVIEWED. Reviewers must not edit the repository, create commits, change PRs or claim tests they did not run.

## Findings that must be challenged
- P39-S1: `record_progress()` increments aggregate version without creating matching event/outbox record.
- P39-S2: `consume_event()` trusts caller-supplied digest and does not bind digest to grant/version/state metadata.
- P39-S3: grant-event outbox has no relay claim/lease/fence; distinguish it from the separate fake effect-dispatch outbox.
- P39-S4: state fencing does not stop bytes already being sent on an established stream.
- Also challenge the journal adapter trust boundary, event-to-tenant binding, first-head bootstrap races, authorization replay/revocation, tombstone/fence durability, and all research/license/maintenance claims.

## Owner-mediated handoff
The owner forwards the exact brief and addendum to Claude and Gemini, then returns both complete Markdown reports. No direct AI-to-AI channel is assumed.

## ChatGPT completion steps
1. Verify each report's file/line references against the exact pinned source and docs.
2. Deduplicate and rank findings by severity and exploitability.
3. Separate model-level defects from adapter-only obligations and unsupported assumptions.
4. Reconcile disagreements without erasing either reviewer's rationale.
5. Produce a review reconciliation note with ACCEPT / ACCEPT WITH CHANGES / REJECT disposition and one bounded next task.

## Constraints
No source-code edits before the reviews are reconciled. No PR #2/#3 changes, merges, deployment, provider calls, paid services, runtime/database selection or changes to canonical LOOP/CASE/D IDs. Do not treat the 266/266 CI result as proof of real concurrency or durability. Keep $0 default and all PocketCode/RevDev separation boundaries.

## Done when
Both complete reports are available; all material findings are verified and risk-ranked; disagreements have explicit dispositions; and the next bounded task is recorded. Until both reports are returned, status is BLOCKED / WAITING FOR OWNER INPUT.
