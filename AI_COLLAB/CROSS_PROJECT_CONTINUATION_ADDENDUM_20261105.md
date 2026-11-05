# Cross-project continuation addendum — 2026-11-05

**Status:** Read-only source/contract reconciliation and documentation-only continuity update. No product source, tests, runtime, host, queue, provider, account, PR or deployment was changed.
**Repositories:** `marcelosofficial-ctrl/PocketCode-` and `marcelosofficial-ctrl/DevRelay-Missions`.
**Authority:** Existing canonical acceptance and owner decision registers remain authoritative. This addendum adds no acceptance IDs and approves no implementation.

## 1. Fresh GitHub snapshot

| Repository / owner-designated branch | Head | Ahead of main | Behind | Merge base |
|---|---|---:|---:|---|
| PocketCode `pocketcode-ai-workflow-director-research-2026-10-28` | `4325e477b5c08a29dbe7d81ae7321d562ecdb851` | 598 | 0 | `555840d8d83342513d9cd353d4d1522d46a5c82d` |
| RevDev `review/revdev-adaptive-ai-workshare-2026-10-27` | `aa342fa02ee92d2dfe78d477eb8f40c310d8fa97` | 508 | 0 | `058f9025319d12e76195659c715ccb4afce133b8` |

These are divergence counts, not merge-readiness evidence.

Protected PRs freshly read from GitHub API:
- PocketCode #2: OPEN / DRAFT / UNMERGED; head `eb8b7ea83cb0e8fe1880351276c485b761431791`.
- PocketCode #3: OPEN / DRAFT / UNMERGED; head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`.
- RevDev #1: OPEN / DRAFT / UNMERGED; head `59f88dc0bd884872cf379c8aeb6272c9a70c71ce`.

All three PRs remain untouched. The two PocketCode research branches remain separate; the owner-designated AI Workflow Director branch remains the continuity branch. Do not infer PR readiness from branch divergence or GitHub's mergeable metadata.

## 2. PocketCode — verdict projection/provenance reconciliation

### Exact source pins re-fetched on the owner-designated branch

- `scripts/report_contract.py`: blob `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817`.
- `scripts/test_report_contract.py`: blob `85109f056009d65a274e9306deb39b68e1fefbd2`.
- Existing source audit: `AI_COLLAB/REPORT_VERDICT_PROVENANCE_PROJECTION_AUDIT_20261104.md`, blob `f35dd2b9b310b2587d13d3fd0fb4e729864b4acb`.

### Confirmed behavior and limits

The helper is explicitly a pure formatter/projection and says it does not authenticate caller-supplied evidence. That separation is appropriate. Keep authentication, producer authorization, tenant/job/run/attempt binding and event acceptance at a trusted coordinator ingress boundary. A typed object or a field named `trusted` is not authentication.

The current `classify_verdict()` checks any integer nonzero `exit_code` before considering lifecycle status. It therefore returns FAIL for combinations such as `accepted + 1`, `queued + 1`, `running + 1`, `rejected + 1`, `timed_out + 137`, `cancelled + 143`, `infrastructure_failed + 1`, and `unknown + 1`. It also returns FAIL for `succeeded + nonzero`, although that combination is contradictory under the documented meaning of succeeded.

The existing tests do not cover these combinations. The timeout/cancel/infrastructure tests pass no exit code; nonterminal tests pass zero. The test called `test_nonzero_exit_overrides_script_printed_pass` does not supply stdout and tests only `succeeded + 2`.

This is a **source-level projection/contract gap**, not evidence of a currently exploitable product path: no production ingress/caller is implemented or proven on this branch, and the helper is not itself a runner.

### Decision

1. Keep `format_report()` a bounded, pure projection. Do not bolt authentication onto it.
2. Do not patch `classify_verdict()` blindly or infer a child exit from a generic integer.
3. Preserve separate evidence for natural child exit, wrapper/supervisor exit, forced termination, lifecycle terminal state, and termination confirmation. The existing adapter envelope already sketches `child_exit_code`, optional `wrapper_exit_code`, `termination_state`, and evidence provenance.
4. Keep the current canonical CASE-04 rule: trusted timeout is INCOMPLETE / timed_out. Do not turn wrapper code 137/143 into program FAIL.
5. Treat `succeeded + nonzero`, `rejected + child-exit`, and other impossible combinations as contradictory evidence pending the owner-approved rule, not as a silent precedence win.
6. D-01..D-08 remain owner-open/proposed as recorded in `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md`. Do not change LOOP-01..14 or CASE-01..16.

### Targeted review/test matrix to prepare before implementation

A more precise 20-case review matrix is now recorded in [Verdict Evidence and Exit Provenance Matrix, November 5](VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md). It adds the previously untested `program_failed + natural child exit 0` contradiction and separates natural child exit, wrapper exit, forced termination, and coordinator lifecycle. This is design-only; the helper and tests remain unchanged.

The pure projection review should cross lifecycle states (`accepted`, `queued`, `running`, `succeeded`, `program_failed`, `timed_out`, `cancelled`, `rejected`, `infrastructure_failed`, `unknown`) with distinct evidence classes:
- no child exit observed;
- natural child exit zero;
- natural child exit nonzero;
- wrapper/supervisor nonzero;
- forced-termination code after timeout/cancel;
- malformed values (including bool, string, missing and stale/mismatched values).

Expected conservative anchors:
- `succeeded + trusted natural child exit 0` can be PASS only after all case-required gates are satisfied.
- `program_failed + independently trusted natural child nonzero` is FAIL.
- `timed_out` / `cancelled` with wrapper termination code remains INCOMPLETE under current canonical CASE-04/LOOP-05; preserve the code as a separate fact.
- accepted/queued/running with a code but no terminal child-exit evidence remains INCOMPLETE.
- `succeeded + nonzero` is contradictory/INCOMPLETE candidate, not a silent FAIL.
- `rejected + independently observed child execution` is a dispatch-boundary contradiction.
- unknown/provider-loss without a trusted child result remains INCOMPLETE / UNKNOWN.
- cleanup uncertainty remains independent; it blocks applicable artifact release and must not erase a known natural child failure.

These are review candidates, not approved new expectations. D-01..D-04 and canonical wording control. Pure tests can test projection only; they cannot prove ingress authenticity, persistence, provider behavior or device behavior.

## 3. PocketCode — product proof remains an empirical question

The iOS competitive baseline and mobile comparator refresh invalidate generic local Python execution as a unique proposition. Existing apps already advertise offline Python, editors, notebooks, files, terminals, stop controls and debugging. These are public claims, not hands-on verification.

The strongest remaining product hypothesis is a portable task/evidence/recovery/AI-correction layer:
- exact source/input identity and attempt lineage;
- honest provenance for observed versus user-reported facts;
- real output file verification and hashes;
- separate execution, cleanup, artifact release and report states;
- recovery without rerunning a completed task;
- compact report handoff to any assistant, explicit patch review/approval, and a new linked attempt.

The fixed CSV-to-JSON task is a workflow benchmark, not proof of runtime advantage or hostile-code security. The exact product-path comparison and paired AI correction experiment remain NOT RUN. No competitor app was installed or tested. Do not assign runner-grade trust to output manually pasted from an external app: a user-supplied transcript is user-attested evidence, while a verified file hash proves the bytes inspected, not that a particular process created them. The eventual receipt must label these evidence sources accurately.

No runtime/provider/framework is selected. Stock Pyodide 314.0.7 remains rejected as a hostile-code sandbox; trusted-bootstrap attenuation is not proven and is not an MVP priority. Linux isolation remains a research direction, not an adopted runtime. Remote PC remains unavailable/UNKNOWN. Manual copy/paste remains the transparent workflow control.

## 4. RevDev — P8U-04/P8U-05 exact-content oracle refinement

Exact maintained source:
- `maintenance/devrelay/r5/queue-publish-r5.ps1`, blob `9c10caadd73e871eff6d4f12f7fe472c4da7f3e5`.
- Collision audit: `resume/revdev/P8U04_P8U05_MAINTENANCE_PUBLISHER_COLLISION_SOURCE_AUDIT_20261103.md`, blob `a1b80f1e5f828a6d2de3469c0a5af3c81d81eb13`.

The source-level gap remains:
- same project/mission/runId is labelled idempotent without exact content/hash comparison;
- different runId at the same mission path is labelled successful duplicate suppression rather than an integrity conflict;
- the early return preserves the existing remote immutable object, but does not meet P8U-04/05 by itself.

The November 4 addendum correctly identifies that the publisher parses the local terminal JSON, enriches it with publisher metadata, and serializes the outbound result. Comparing remote bytes directly with the raw local terminal file would therefore be the wrong oracle.

### Required three-part identity model for the future test design

1. **Source terminal identity:** exact raw local terminal-result bytes plus SHA-256 before parsing/enrichment. Retain this to prove which original product result was used and that it was not altered.
2. **Product-result semantic projection:** a versioned, explicitly allowlisted projection of material product-result fields, compared with the parsed source terminal result. This detects meaningful field changes even if publisher metadata is unchanged. The canonicalization/projection algorithm is not yet approved.
3. **Publication envelope identity:** exact UTF-8 bytes and SHA-256 of the prepared outbound immutable by-mission JSON after publisher enrichment and serialization, captured before network publication. This is the object to compare against exact remote read-back.

For one stable publication operation, prepare and durably retain the envelope bytes/hash once, then reuse those exact bytes on retry. Do not silently rebuild the old operation with changed source bytes, serializer version, metadata, or property ordering.

Future collision dispositions:
- same operation/source identity, same semantic projection and exact envelope bytes: idempotently complete only after exact remote read-back equality;
- same runId but different source bytes or changed semantic product fields: integrity conflict;
- same semantic product result but changed envelope serialization/metadata: distinguish envelope-version/operation drift; do not call it exact-byte idempotency;
- different runId at the same single-use mission path: immutable identity conflict;
- unreadable, malformed, inaccessible or ambiguous remote target: UNKNOWN/integrity/access failure, never absence;
- changed local source bytes for an already-prepared operation: stop and preserve evidence; do not reconstruct a new payload under the old operation identity.

Keep mutable latest pointers, timestamped history, evidence index and handoff separate from the immutable by-mission result. Their recovery/ordering assertions require their own evidence. Do not let a successful by-mission read-back imply that all side effects, no-rerun/audio behavior, or unrelated-project preservation passed.

No source fix is approved. Current PC/live publisher/source parity remains UNKNOWN; historical P8V live and maintenance hashes differed. Do not rerun the recovered P8U mission. P8U/P0-D remain NOT RUN; P0 remains OPEN/release-blocking; OD-04 remains OPEN.

### RevDev follow-up: consolidated publisher source findings

The latest static pass also reconciled the separate P8U-03/P8U-06 audit and the conditional P8U-08 source-risk review. See [R5 Maintenance Publisher Consolidated Source Findings, November 5](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/R5_MAINTENANCE_PUBLISHER_CONSOLIDATED_SOURCE_FINDINGS_20261105.md). It preserves the distinction between four maintenance-source gaps and a conditional cross-writer race hypothesis. OD-04 remains OPEN; no installed/live defect is inferred.

## 5. Next work order

1. Prepare a narrowly scoped Claude/Gemini review of the PocketCode verdict matrix and the existing report-projection audit. Ask only whether the proposed separation of child exit, wrapper exit, forced termination and lifecycle precedence is consistent with canonical LOOP/CASE and D-01..D-04. Do not treat a review response as owner approval.
2. Define the RevDev semantic projection and publication-envelope identity at the design level before proposing any code. Preserve P8U expected strings and the existing acceptance file.
3. Keep PocketCode's fixed-task experiment ready, but do not install apps or start workloads. When the owner explicitly chooses an already-installed runner or authorizes a specific install/test, compare the same frozen source and inputs across success and malformed-input cases, then run the paired AI correction comparison with identical observed facts.
4. Keep PC-return work read-only first: inventory current source checkout, installed publisher, runtime, queue and branch state; verify exact source parity before any local test or implementation.
5. Re-fetch both branch heads and protected PR metadata before any later consequential GitHub action.

## 6. Verification and non-actions

- GitHub branch refs, main comparisons and protected PR metadata were read.
- PocketCode helper/test source and RevDev maintenance publisher/audit were fetched and inspected statically.
- No tests, builds, app/browser/device runs, provider workloads or AI-to-AI contacts occurred.
- No source/tests, runtime, queue, host, accounts, secrets, Actions, PRs, deployments or merges were changed.
- Canonical acceptance IDs/expected strings and owner-open decisions remain unchanged.



## 8. November 5 later ref comparison and snapshot qualification

A later read-only comparison against each repository's `main` returned:

| Repository / owner-designated branch | Merge base | Ahead of main | Behind |
|---|---|---:|---:|
| PocketCode `pocketcode-ai-workflow-director-research-2026-10-28` | `555840d8d83342513d9cd353d4d1522d46a5c82d` | 619 | 0 |
| RevDev `review/revdev-adaptive-ai-workshare-2026-10-27` | `058f9025319d12e76195659c715ccb4afce133b8` | 510 | 0 |

The comparison response exposed the branch names, merge bases and ahead/behind counts, but did not expose either current tip SHA. Therefore the tip SHAs in Sections 1 and 7 are historical snapshots, not verified current heads. Do not use them as current branch pins. The previous counts (598/508) are superseded by this later comparison (619/510). This addendum correction itself creates one additional PocketCode commit, so the 619 count is the pre-correction snapshot; refresh both refs and comparisons before the next consequential action.

The protected PR search was repeated for both repositories. PocketCode #2 and #3 and RevDev #1 remain discoverable as open PRs. No PR was edited, converted, reviewed, merged, or closed in this pass. The earlier verified draft/unmerged status remains the last full PR-metadata snapshot; the latest search response did not independently return every PR field.

This section is a continuity correction only. It does not change canonical acceptance, owner decisions, source, tests, runtime, queue, provider, installation, Actions, or deployment state.

## 7. November 5 continuation update

- PocketCode owner-designated branch now points to `4325e477b5c08a29dbe7d81ae7321d562ecdb851` (598 ahead / 0 behind main). New matrix blob: `f146bd45cdbc3e7f6f1301ad3c0e172ffa4443d7`.
- RevDev owner-designated branch now points to `aa342fa02ee92d2dfe78d477eb8f40c310d8fa97` (508 ahead / 0 behind main). New consolidated publisher audit blob: `c6f3c5cd2380f68bd83a84467b992ded0909d89f`.
- Protected PRs were re-read after the documentation commits: PocketCode #2/#3 and RevDev #1 remain OPEN / DRAFT / UNMERGED and untouched.
- No source/tests, runtime, local host, queue, provider, account, Actions, installation, restart, deployment, merge or mission replay occurred.


## 9. November 5 RevDev publication operation plan

A companion RevDev design artifact now translates the canonical P8U-01..12 scenarios into an ordered publication-operation state model and synthetic fault-injection cut points F0-F14:

- [P8U Publication Operation State Machine and Fault-Injection Plan](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/P8U_PUBLICATION_OPERATION_STATE_MACHINE_AND_FAULT_INJECTION_PLAN_2026-11-05.md)
- [R5 Maintenance Publisher Consolidated Source Findings](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/R5_MAINTENANCE_PUBLISHER_CONSOLIDATED_SOURCE_FINDINGS_20261105.md)

This is planning for a future isolated synthetic transport harness, not implementation or live evidence. It preserves execution/publication separation, exact immutable content identity, ambiguity-safe recovery, independent mutable-view verification, and no duplicate execution/terminal/audio effects. Canonical P8U JSON and owner decisions remain unchanged; OD-01..OD-08 remain OPEN.

The latest pre-this-addendum-write comparison reported PocketCode 627 ahead / 0 behind main and RevDev 519 ahead / 0 behind main. The PocketCode addendum update itself adds one commit, so refresh the branch comparison before using an ahead count as current. Comparison responses do not expose current tip SHAs. Protected PR searches still find PocketCode #2/#3 and RevDev #1 open; the latest search did not independently return all draft/merge metadata.


## 2026-11-05 source-level follow-up

- PocketCode code-level competitor/source review: [Code-Level Open-Source Reuse Review](../RESEARCH/CODE_LEVEL_OPEN_SOURCE_REUSE_REVIEW_20261105.md).
- PocketCode evidence authority map: [Mobile Runner Evidence Sourceability Matrix](../RESEARCH/MOBILE_RUNNER_EVIDENCE_SOURCEABILITY_MATRIX_20261105.md).
- RevDev companion design review: [P8U Upstream Recovery and Outbox Pattern Review](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/P8U_UPSTREAM_RECOVERY_AND_OUTBOX_PATTERN_REVIEW_2026-11-05.md).

These are research/design references only. They do not change separate-repository boundaries, canonical acceptance suites, PR states or owner decisions.


## Happy Agent daemon follow-up

- [Happy Agent Daemon Source Audit](../RESEARCH/HAPPY_AGENT_DAEMON_SOURCE_AUDIT_20261105.md) adds a code-level review of PC-host orchestration, durable work, process sessions, sandboxing and event replay.

This is architectural research only; no host backend, process runtime, provider, sandbox or dependency has been selected.


## Provider-neutral recipe and durable work packet proposals

Two companion design artifacts now turn the competitor research into concrete, reviewable contracts while preserving separate product/runtime boundaries:

- PocketCode: [Provider-Neutral Recipe and Durable Task Manifest Proposal](PROVIDER_NEUTRAL_RECIPE_AND_DURABLE_TASK_MANIFEST_PROPOSAL_20261105.md). Defines separate recipe, run, attempt, step-attempt, approval, evidence and derived-report identities; bounded DAGs; permission scopes; strict checkpoint deserialization; approval binding; and lifecycle/evidence separation. It maps at suite level to LOOP-01..14 and CASE-01..16 without inventing individual case meanings.
- RevDev: [Bounded Operation Recipe and Durable Work Packet Proposal](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-adaptive-ai-workshare-2026-10-27/resume/revdev/BOUNDED_OPERATION_RECIPE_AND_DURABLE_WORK_PACKET_PROPOSAL_2026-11-05.md). Applies the same conceptual vocabulary to RevDev's one-action bounded batch, dependency-aware stepper, repair continuation and separately identified publication operation. It preserves AEC/AWC/P8U/P0-D suites and OD-01..OD-08.

New source-level references inspected include LangGraph's checkpoint/pending-write contract, Hatchet's explicit task/attempt/idempotency projection, and Temporal's workflow/run/attempt metadata. These are design references, not selected dependencies. LangGraph's broad default checkpoint deserialization is specifically rejected for untrusted task state; use a strict data-only schema and explicit type allowlist.

No framework or runtime is selected, no additional code was copied in this pass, and no implementation/test claim is made. The existing isolated reference copies and RevDev JCS research copy retain their previous non-production status. Both proposals require Claude architecture review and Gemini security/spec review before any schema is frozen.


## Scope reconciliation for the new manifest proposals

A cross-check against the pre-existing contracts found important overlap that must be preserved rather than duplicated:

- PocketCode already has the provider-neutral boundary sketch, adapter result envelope/fake protocol, and a bounded offline AI Workflow Director plan with its own AWD acceptance IDs. The new task manifest is a later planning/execution layer. It does **not** expand the initial offline Director slice into code execution, select a provider/runtime, or replace the existing job/attempt/evidence contract. Existing contracts remain authoritative for their covered fields and gates.
- RevDev already has REVDEV_OPERATION_ENVELOPE_AND_DURABLE_ORCHESTRATION_DESIGN_2026-11-05.md for P0-first publication operation identity, prepared bytes, transport attempts, target obligations and concurrency. The new work-packet proposal is the parent product-batch/recipe layer. It does not replace the detailed publication design or the separate AI Work Coach evaluation trial schema.

Both proposals now state these boundaries explicitly. This avoids two competing run IDs, duplicate lifecycle state machines, and scope creep. The proposals remain unfrozen and require independent Claude/Gemini review.


## Workspace recovery feature research

- [Cline Workspace Checkpoint and Restore Audit](../RESEARCH/CLINE_WORKSPACE_CHECKPOINT_AND_RESTORE_AUDIT_20261105.md) evaluates snapshot, diff, transactional rollback and branch-safety patterns for PocketCode's correction loop.

Recommendation: keep workspace checkpoints a P1 feature, but require a reversible checkpoint or explicit approval before future unattended multi-file repair. Workspace snapshots must not replace immutable task/attempt evidence. No implementation or canonical acceptance changes were made.
