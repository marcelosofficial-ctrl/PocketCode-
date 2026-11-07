# NEXT TASK: P39 independent adversarial review

## Goal
Obtain and reconcile two independent, source-pinned reviews of the release-grant recovery/concurrency design before any durable adapter or storage selection.

## Reviewer assignments
- Claude: architecture, transaction linearization, receipt-head races, stable-intent/auth separation, outbox atomicity/order, fencing and stream effects.
- Gemini: caller/producer trust boundary, tenant isolation, replay/revocation, event identity/digest/order, fence authority, source/license claims and adversarial tests.

## Exact brief
Use `AI_COLLAB/P39_INDEPENDENT_REVIEW_PROMPT_20261107.md`. It contains exact branch/code pins, required output format and no-edit/no-commit instructions. Review the exact pinned source/test SHA and current documentation branch as specified. If any file is inaccessible, report NOT REVIEWED.

## Owner-mediated handoff
The owner forwards the prompt to Claude and Gemini and returns both complete Markdown reports. No direct AI-to-AI channel is assumed.

## ChatGPT completion steps
1. Verify both reports' file/line references against the live branch.
2. Deduplicate and rank findings by severity and exploitability.
3. Separate model-level gaps from adapter-only requirements and unsupported assumptions.
4. Reconcile disagreements without erasing either reviewer's rationale.
5. Recommend ACCEPT / ACCEPT WITH CHANGES / REJECT and define one next bounded task.

## Constraints
No code edits, PR changes, merges, deployment, provider calls, paid services, runtime/database selection or changes to canonical LOOP/CASE/D IDs. Do not treat the 266/266 suite as proof of real concurrency or durability.

## Done when
A review reconciliation note exists with both reviewer reports linked or quoted by exact source, findings verified against source, risk-ranked disposition and one next task. Until the owner returns both reports, status is BLOCKED / WAITING FOR OWNER INPUT.
