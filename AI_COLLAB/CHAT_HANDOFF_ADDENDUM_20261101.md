# PocketCode Continuation Addendum — 2026-11-01

**Purpose:** Fresh continuation pointer after the 2026-10-29 handoff. Read this addendum after `CHAT_HANDOFF_20261029_POCKETCODE.md`; it records the newest completed review and exact next task.

## 1. Latest PocketCode research-branch update

Repository: `marcelosofficial-ctrl/PocketCode-`  
Branch: `pocketcode-ai-workflow-director-research-2026-10-28`

- New commit: `5a41947753348dea5f45db578ca945cc4854d3fe`
- New review file: [REVDEV_POCKETCODE_CROSSWALK_INDEPENDENT_REVIEW_20261101.md](REVDEV_POCKETCODE_CROSSWALK_INDEPENDENT_REVIEW_20261101.md)
- Review file blob after read-back: `daa3317d44506562f153ea9191a2a5104787ae18`

This is a documentation-only update on the existing research branch. It did not modify PR #2/#3, canonical PocketCode acceptance, source/tests, RevDev source/tests, runtime, queue, providers, or security boundaries.

## 2. Work completed in this pass

ChatGPT read the full 2026-10-29 PocketCode handoff, including §§33–35, then inspected:
- the RevDev cross-project alignment note and draft semantic crosswalk;
- the complete RevDev acceptance traceability supplement, especially Sections 11–12;
- the complete 18-entry AWC synthetic fixture manifest and fixture/measurement specification;
- the RevDev primary-source audit for AWC/AEC namespace meanings;
- the original P0-D source matrix (source lines 107–123);
- PocketCode canonical `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` on main and the proposed execution contract on the research branch;
- live PR #2 and #3 metadata/diffs.

### Independent review verdict

**Accept the crosswalk as a cautious conceptual traceability draft, with two precision refinements recommended.** No wholesale remapping is justified.

1. **AWC-010:** clarify that its task packet travels from PocketCode/RevDev toward an assistant, while LOOP-08's execution report travels from PocketCode back toward an assistant. Copy/share is a shared transport principle, not an equivalent payload or acceptance test. LOOP-13 separately constrains unsupported automation claims.
2. **AWC-018:** LOOP-02/03 and CASE-12 are the strongest adjacent concepts. LOOP-05 should apply only if the missing terminal signal also leaves lifecycle/infrastructure outcome uncertain. Truncation alone is an evidence-collection problem, not automatically a timeout/cancellation/rejection/infrastructure failure.

Section 12 is substantively sound:
- P0-D items 1–7 and 9 have no direct PocketCode LOOP/CASE mapping.
- Item 8 is adjacent to LOOP-07/CASE-12 only; P0-D additionally requires durable persistence/publication of an intentional validation failure.
- Item 10 is adjacent to CASE-13/CASE-16 only; P0-D additionally requires exact-result publication and duplicate/idempotent replay.
- Suggested editorial change: rename the table column “Exact requirement (condensed without changing meaning)” to “Source requirement (condensed)”; the table is a summary, not a verbatim quotation.

The review preserves all namespaces and IDs: PocketCode LOOP-01–14 / CASE-01–16 and AEC-001–012; RevDev AWC-001–018, P8U-01–12, P0-D 1–10, and CYC-01–10. These are different test objects. No suite proves another project's implementation.

## 3. Current evidence boundaries

- AWC manifest: 18 unique proposed fixtures, status `PROPOSED_NOT_RUN`. No model trials were run.
- PocketCode canonical LOOP/CASE acceptance: proposed/not run.
- RevDev P8U and P0-D runtime acceptance: NOT RUN; P8U remains specification-only.
- RevDev PC source/runtime/installed binary/watcher/queue/publication/audio: UNKNOWN until PC access returns.
- PocketCode execution location/provider remains unselected; no live execution capability is established by this review.
- PR #2 remains open, draft, unmerged. Its timeout-precedence candidate is not merged or newly tested.
- PR #3 remains open, draft, unmerged.
- Exit-code provenance remains an open PocketCode contract question: the contract does not clearly distinguish authoritative child-program exit code from wrapper/termination code. Preserve the canonical CASE-04 timeout expectation. Do not invent a schema or modify PR #2.

## 4. Next task

Obtain two bounded independent reviews of the crosswalk review file:

**Gemini:** challenge semantic overreach, false equivalence and missing negative cases. Prioritize AWC-010 transfer direction; AWC-018 truncation versus lifecycle uncertainty; AWC-005/011/012/017 boundaries; and all ten P0-D mappings. Preserve IDs and distinguish conceptual adjacency from test equivalence.

**Claude:** challenge engineering-state and recovery implications. Focus on evidence producer/observer authority, identity correlation, durable persistence/publication, queue quarantine/liveness, exact-result replay, and task repair retry versus dispatch retry. Do not infer PC implementation behavior.

Require each reviewer to return exact row/ID, ACCEPT/CHANGE/REJECT, source-backed rationale and artifact/line references, counterexample or missing negative case, evidence layer (conceptual/contract/implementation/runtime), and NOT RUN/UNKNOWN status.

ChatGPT should then reconcile both reviews against the exact source blobs. Only make documentation corrections supported by source evidence. Keep the crosswalk a draft until the independent reviews are reconciled.

## 5. Standing restrictions

No provider selection/account/workload/spend, GitHub Actions, merge, deployment, PR #2/#3 changes, source/test edits, canonical acceptance edits, runtime/queue/host mutation, installation, restart, security-boundary change, or integration-topology decision without explicit owner authorization. Research-only documentation updates on the PocketCode research branch remain authorized for continuity. $0 budget remains the default.


## 6. Continuation update — supplemental helper review and live branch reconciliation (2026-11-01)

A further read-only source pass extended `REVDEV_POCKETCODE_CROSSWALK_INDEPENDENT_REVIEW_20261101.md` with Section 7 (OBS-01..OBS-03). The new observations are deliberately separate from the AWC-to-LOOP/CASE and P0-D mappings:

- OBS-01: the lifecycle helper overloads `UNKNOWN`: the reducer uses it when no terminal event exists and also maps `provider_error` to it, while disposition derivation turns every UNKNOWN into `PROVIDER_ERROR`. D-02 says a provider-error disposition requires the infrastructure cause itself to be confirmed.
- OBS-02: `contradictory_evidence`, `limit_violated`, and `output_truncated` are not strictly validated as booleans. A malformed falsy contradiction value such as 0 can bypass the contradiction guard and permit PASS when other gates are true.
- OBS-03: the streaming bearer-token pattern has unbounded whitespace before the token but only a 768-byte carry. A targeted local reproduction of that pattern/carry algorithm with 900 whitespace bytes retained the token unredacted. The checked-in suite was not run.

These are static helper-contract observations, not claims of a live caller vulnerability or product/runtime behavior. The helper/test blobs inspected were PR #3 base `ba8d4d0b217c90513bed020e298029ef4e16f164` and lifecycle-fingerprint descendant `316345341603848c4a86a6a82e533daa796c7695`; the latter contains prior input/tombstone/event-shape improvements but remains a separate 34-commit descendant, not merged into PR #3. Both exact test suites remain NOT RUN.

### Crosswalk wording precision

Correction to avoid ambiguity: AWC-010's task-packet handoff and LOOP-08's execution-report handoff both move information outward from the product/workflow toward an AI assistant. They share a copy/share transport principle, but the payloads, purpose and stage differ. They are not equivalent acceptance tests.

AWC-018 remains adjacent primarily to LOOP-02/03 and CASE-12. LOOP-05 applies only if the missing terminal signal also leaves the lifecycle/infrastructure outcome uncertain; truncation by itself is not a timeout or cancellation.

### Live branch state and separation

- PocketCode main remains `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- PocketCode research branch before this continuity commit: `c28884dab868a0707b6af0ee22feeaa3ac74aedc`.
- The separate execution-boundary branch `pocketcode-execution-boundary-crosswalk-2026-11-01` was at `35a195e3fb0d3e0cdb3ab6692760533869639264`. Its compare against the research branch showed 10 commits ahead and 2 behind from common base `97db362e3f57c4d605d5d84a28d5cbb264c23c24`; do not merge or silently reconcile it.
- PR #2 remains open/draft/unmerged at `eb8b7ea83cb0e8fe1880351276c485b761431791`.
- PR #3 remains open/draft/unmerged at `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`.
- Lifecycle-fingerprint branch remains at `26de6bb29020d6781d342c691e430616a4321083`, a direct 34-commit descendant of PR #3, not merged. No PR for that descendant was found in the repository PR search.

### Next bounded work

The next step remains the two independent reviews requested in Sections 4–5 of the review file:
- Gemini: challenge Section 11–12 semantic equivalence, false-positive mappings and missing negative cases, with emphasis on AWC-010/018 and P0-D 1–10.
- Claude: challenge evidence authority, identity correlation, persistence/publication, quarantine/liveness, exact-result replay, and repair retry versus dispatch retry, without inferring PC implementation behavior.

ChatGPT's static review is complete for now; it does not substitute for Claude/Gemini. After their responses, reconcile exact source/line references and make only supported documentation corrections. No runtime tests, model trials, provider use, source/test edits, PR changes, canonical acceptance edits, Actions, queue/host mutation, merge, deployment or spend occurred. The $0 and phone-only constraints remain unchanged.


### Final read-back identifiers for this continuation update

- Research branch HEAD after the review/checkpoint commit: `d5344329d8578e105f9be5bee38e1bb9dde3a2bc`.
- Updated independent review blob: `c1d1a6a7f31706035198a0b0522e35bca1f33a0a`.
- Updated addendum blob before this identifier-only pointer commit: `450f2cd25ba9db68ea7196be2e1e10abd409c7ae`.
- Commit message: `docs: extend crosswalk and lifecycle evidence review`.
- Both edited files were fetched again after the commit; the exact blob hashes matched the new objects and the OBS-01..OBS-03 section was present.


## 7. Continuation update after Claude's reviews — 2026-11-01

Claude returned both requested reviews. The reconciled source-backed disposition is now appended as Section 8 of REVDEV_POCKETCODE_CROSSWALK_INDEPENDENT_REVIEW_20261101.md.

### Review status

- Claude's conceptual and engineering critiques were received. Claude disclosed that it had read only the review note and had not inspected the underlying source files or run tests.
- ChatGPT re-fetched the exact AWC manifest, PocketCode canonical LOOP/CASE acceptance, RevDev P0-D source, lifecycle-fingerprint helper and test blobs, and D-01..D-04 owner register before reconciling the findings.
- Gemini's independent review remains pending.

### Material crosswalk decisions

- AWC-005 and AWC-011 remain separate assistant-side untrusted-instruction fixtures, but neither maps to LOOP-12/CASE-15 runtime isolation.
- AWC-008 has no LOOP-09/CASE-13 mapping: task repair retries are not dispatch retries.
- AWC-009 has no LOOP-14 mapping: quota-evasion advice is not a provider/billing authorization gate.
- AWC-010's transfer direction is the same for both cases, from product/workflow toward an assistant. LOOP-13 is the primary adjacent concept; LOOP-08 is only a secondary copy/share transport analogy because a prospective task packet is not a retrospective run-bound report.
- AWC-012 maps only adjacently to LOOP-02; remove LOOP-14.
- AWC-017 has no current LOOP/CASE mapping.
- AWC-018 is primarily adjacent to CASE-12, with LOOP-02/03 only as broader honesty concepts. Remove LOOP-05 unless a separate fixture establishes lifecycle uncertainty from a missing terminal signal.
- P0-D 9 remains unmapped. CASE-16 is not a queue-quarantine/liveness test.
- Split P0-D 10 into CASE-13 idempotency adjacency and CASE-16 run-identity/order adjacency. Neither proves durable exact-result publication/replay.
- Section 12 header should be “Source requirement (condensed)”.

### New helper review items

Section 8 also records OBS-04 producer authority, OBS-05 attempt-context correlation and OBS-06 truncation-cause conflation, in addition to the reconciled OBS-01 through OBS-03.

Important redaction refinements: the source regex already has case-insensitive matching; the carry leak trigger depends on chunk boundaries and can occur with 756–763 separator bytes; and overlong bearer-like values can be wholly missed or partially redacted depending on punctuation at the 256-character boundary. A local copied-algorithm reproduction was performed, but repository tests remain NOT RUN.

The source review also confirms that generic output_truncated currently maps to LIMIT_EXCEEDED, while D-01/D-03 distinguish runtime-enforced limits, collector truncation and display truncation. Keep that as a source-level contract gap, not a runtime vulnerability claim.

### Exact source pins used for this reconciliation

- AWC manifest: c2d4cba6c836f725f7bc4585f91e02d443fe89e1, PROPOSED_NOT_RUN.
- PocketCode canonical LOOP/CASE acceptance: c6714c27db52b2962fe8d1c7e6a16829d46a8338, proposed/NOT RUN.
- RevDev P0-D source: 6a0c804e1ad75edf1022af960acbb143ba1430b6, lines 107–123.
- Lifecycle-fingerprint helper: 316345341603848c4a86a6a82e533daa796c7695.
- Lifecycle-fingerprint tests: ef9a68de632be30c091afe57f0724fd030a513f9, NOT RUN.
- Owner decision register: e67b2659cf2d71ef77d8e4619c91143e71062470; D-01..D-04 and D-06/D-08 remain proposed/open.
- The lifecycle-fingerprint branch remains separate from PR #3 and main. No code, tests, canonical acceptance, PR, runtime, queue, provider, Actions, merge, deployment or spend was changed.

### Next review

Ask Gemini to independently challenge the reconciled Section 8, especially AWC-005/011/008/009/010/012/017/018, the P0-D 9/10 split, OBS-01 through OBS-06, and the exact distinction between runtime-enforced limits, collector caps and display truncation. Require exact source/artifact references and evidence-layer labels. Do not ask Gemini to infer runtime behavior or approve implementation.


### Second source pass: branch comparison and redaction coverage

A direct diff-level comparison confirms:
- PR #3 base and lifecycle-fingerprint descendant have identical disposition logic and identical StreamingRedactor code.
- The descendant has stricter malformed-event shape validation and preserves invalid events; the PR #3 base does not contain those same protections.
- Neither branch's reducer authenticates producer authority or compares an event to an expected tenant/job/attempt/source/policy context.
- Additional copied-algorithm checks show 300-character values after secret=, api_key=, access_token= and password= leave a 44-character suffix visible. The bearer rule has separate word-boundary behavior and carry-boundary risk.
- Repository helper and test suites remain NOT RUN. The reproduction was local and limited to code copied from the pinned source. No patch was made.

This comparison and the future-work priority are recorded in Section 8.8 of the independent review file. It supersedes any implication that every malformed-event finding is identical across the two branch versions.


## 8. Regression plan added — 2026-11-01

A staged, evidence-layered test design is now available at [LIFECYCLE_CONTRACT_REGRESSION_PLAN_20261101.md](LIFECYCLE_CONTRACT_REGRESSION_PLAN_20261101.md).

It separates:
- Pure-helper regressions for OBS-01 through OBS-06.
- Fake-adapter dispatch/reconciliation tests.
- Persistence and exact-byte replay tests.
- Provider/process-observer authority tests.
- Queue quarantine and runtime liveness tests.

Priority begins with false-PASS prevention (OBS-02) and terminal-evidence state separation (OBS-01), then attempt identity, producer authority and truncation taxonomy. Redaction is explicitly defense-in-depth. Every test remains proposed/NOT RUN; no source or test was changed.

Current research branch includes the regression plan commit `fc987878c23d0a6e69189b3a9b706bbb3d2eacfb`. Its file blob is `70b457623c392a99475e5682ceb01903c2b9cf9a`.
## 9. Gemini review received and source-reconciled - 2026-11-01

Gemini's supplied review was read and rechecked against exact source snapshots. Its AWC/CASE/P0-D/OBS mappings are not accepted because the identifiers are materially misassigned:

- AWC-005 is unsafe untrusted suggestion handling, AWC-008 is failed-repair recovery, AWC-009 is usage-limit bypass advice, AWC-010 is manual task handoff, AWC-011 is prompt injection in source content, AWC-012 is fabricated usage telemetry, AWC-017 is unknown provider/model/host capabilities, and AWC-018 is partial evidence with no completion signal.
- PocketCode CASE-05 is cancellation, CASE-07 output limits, CASE-08 unsafe input path, CASE-13 ambiguous-request idempotency, CASE-15 egress/secrets, and CASE-16 out-of-order run identity. CASE-17/18 do not exist in the pinned canonical acceptance.
- RevDev P0-D-09 is malformed mission quarantine without blocking later queue work. P0-D-10 is exact-result publication and duplicate/idempotent replay.
- The actual OBS-01..06 meanings remain the ones in the independent review and regression plan; Gemini's six alternative labels are not substituted.

Useful engineering findings retained in the audit and new regression-plan Section 8:
1. D-05 must be an actual applied-policy barrier before untrusted process launch. Daytona v2 documentation confirms existing-sandbox policy updates can remain pending while desired and applied revisions differ. ETag is a concurrency token, not applied-enforcement proof.
2. LOOP-12 requires provider/runtime proof of resource boundaries and host containment; mock adapter errors are insufficient.
3. PC-LC-05 is extended to distinguish execution enforcement, stream capture, collector/retention, and display loss. Linux pipes block/fail when full; they do not inherently truncate at a universal 1 MB threshold.
4. D-06 semantic fingerprints must be tenant-scoped and include all execution-relevant normalized request inputs.
5. D-07's current release-boundary revalidation is already specified; tests now cover partial writes, digest mismatch, exact immutable bytes, current authorization and quarantine.
6. Provider teardown failure needs explicit orphan reconciliation while preserving the confirmed child exit separately from cleanup.
7. Forged JSON in stdout must remain untrusted text. Delayed cost reconciliation is a separate future requirement and remains blocked by the $0/no-provider/no-workload constraint.

New supplementary test IDs PC-EXT-01 through PC-EXT-07 are proposed only. They do not become canonical CASE/AWC/P0-D IDs and all remain NOT RUN.

**Date caveat:** Gemini's supplied response says 2026-11-02, one day ahead of the current date in this audit. The content is treated as supplied review text; its date/authorship metadata is not independently verified.

**Current research branch state before these documentation additions:** `a3db9294d4e6d4692a2a990b56d925d34a12ef5c`. After the additions, verify the new branch HEAD and read back all three updated documents. Main and PR #2/#3 are to remain untouched. No implementation, canonical acceptance, tests, provider, runtime, queue, Actions, merge, deployment or spend is authorized.


## 10. Final GitHub checkpoint after Gemini reconciliation

The three documentation updates were committed sequentially to the existing research branch:

| File | Commit | Resulting blob |
|---|---|---|
| `AI_COLLAB/REVDEV_POCKETCODE_CROSSWALK_INDEPENDENT_REVIEW_20261101.md` | `9e99020bea45239c9b3295d57a3663d7f8f64a7d` | `1bd83b8b30988bc8313bd30e0dceefe73eb3ded2` |
| `AI_COLLAB/LIFECYCLE_CONTRACT_REGRESSION_PLAN_20261101.md` | `e925fbd49ab518d565d56374d4bf4ca7593ef9c8` | `565eba82399b44d32d049f16084f1fda1a30d494` |
| `AI_COLLAB/CHAT_HANDOFF_ADDENDUM_20261101.md` (Gemini reconciliation update) | `01cd7d4e69ecba411dcf1c9d07a77a94d1b42696` | `e1412fa1aaeb5fbff0eddd27c1f0427fc658fd79` |

Read-back checks confirmed the Gemini reconciliation section and its source pins in the independent review, all seven PC-EXT cases in the regression plan, and the continuation summary in this addendum. The three files were fetched from the research branch after commit. The independent review and regression plan both explicitly retain NOT RUN / UNKNOWN boundaries.

A live GitHub ref/PR check immediately after those commits returned:

- Research branch `pocketcode-ai-workflow-director-research-2026-10-28`: `01cd7d4e69ecba411dcf1c9d07a77a94d1b42696` before this final handoff checkpoint update.
- Main: unchanged at `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- PR #2: OPEN, DRAFT, UNMERGED; head `eb8b7ea83cb0e8fe1880351276c485b761431791`; base main.
- PR #3: OPEN, DRAFT, UNMERGED; head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`; base main.

No PR, main, source, tests, canonical acceptance, runtime, queue, provider, workflow/Actions, merge, deployment, or billing state was changed. The only writes in this pass were the three documentation files on the research branch. The commit created by this final handoff update must be read as the new research-branch HEAD; the next chat should verify the live ref before writing again.


## 11. Follow-up source pass: align supplemental tests to existing detailed checklists

A final specification pass found that the new Gemini-derived PC-EXT labels overlapped existing detailed research checklists. The regression plan now explicitly says those checklists are authoritative and PC-EXT is only a traceability index:

- D-05: PBR-01..07 and PF-01..05 in `AI_COLLAB/ADAPTER_BOUNDARY_DECISION_GATE_20261029.md`.
- D-06: DR-01..12 in `AI_COLLAB/IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md`.
- D-07: AR-01..14 in `AI_COLLAB/ARTIFACT_RELEASE_FALSIFICATION_CHECKLIST_20261029.md`.
- D-08: RH-01..14 in `AI_COLLAB/REPORT_HISTORY_PERSISTENCE_FALSIFICATION_CHECKLIST_20261029.md`.
- Boundary contract: `AI_COLLAB/PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md`, Sections 3–8.
- Readiness dependencies: `AI_COLLAB/IMPLEMENTATION_READINESS_BACKLOG_20261029.md`, WP-03 through WP-06.

Resulting gap assessment:
- PC-EXT-01, PC-EXT-03 and PC-EXT-07 are pointers/illustrations against existing PBR/PF, AR and DR coverage, not parallel specifications.
- PC-EXT-02 remains a provider/runtime resource-containment evidence gap under LOOP-12 and SECURITY.md.
- PC-EXT-04 remains a focused provider teardown/orphan reconciliation gap. Keep execution, cleanup, disposition and release separate; prove actual deletion/termination only after a provider is selected.
- PC-EXT-05 is future cost reconciliation, separate from OBS-03 and blocked by $0/no-provider/no-workload.
- PC-EXT-06 adds hostile stdout fixtures to PC-LC-04/PC-RT-02 and TPM-15; it does not create a new trust mechanism.
- The stream correction remains: a full Linux pipe blocks or fails depending on mode; it does not inherently truncate at a generic 1 MB threshold.

Main remains `555840d8d83342513d9cd353d4d1522d46a5c82d`. PR #2 and PR #3 remain OPEN, DRAFT, UNMERGED at their previously recorded heads. The only additional writes were documentation updates on the research branch. Exact commits/blobs and the latest HEAD are recorded in the next final checkpoint section.


## 12. Final verified research-branch snapshot — after Gemini checklist alignment

The last documentation-only commits in this work pass are:

| File | Commit | Read-back blob |
|---|---|---|
| Independent crosswalk review, Sections 10–11 | `4eed9c15b74a69cd5d5438f890b07918c55608f5` | `75f97c91e8c7bfdd7a4673ae8410c9035e87cc0e` |
| Lifecycle regression plan, Sections 8–9 | `40ca0ba5e8142e85090cb0f3b8890f5a90edf7c3` | `8d9725bca53bacb772cfd0a54f8758ee6da83cb4` |
| This continuation addendum, Sections 11–12 | `ea41c51bc1ec181a26b42dd12dd08b0c89bd0692` | `3f87de325ee88d51dd2f07127eef6f83863477d3` |

The live research branch ref was read after the above updates and returned `ea41c51bc1ec181a26b42dd12dd08b0c89bd0692`. The final addendum update that records this snapshot is the next commit and becomes the new branch HEAD.

Final read-back checks confirmed:
- Review document: Gemini source reconciliation, exact identifier corrections, Daytona/policy discussion, and existing-checklist alignment.
- Regression plan: PC-EXT-01..07, the PBR/PF/DR/AR/RH traceability table, and NOT RUN status.
- Handoff: this audit's corrected meanings, source alignment, and branch/PR protection rules.

Verified branch separation immediately before this final addendum write:
- Main: `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- PR #2: OPEN, DRAFT, UNMERGED; head `eb8b7ea83cb0e8fe1880351276c485b761431791`, base main.
- PR #3: OPEN, DRAFT, UNMERGED; head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`, base main.

Only the three named AI_COLLAB documents on the existing research branch were written in this pass. No source, tests, canonical acceptance, main, PR head, provider, store, runtime, queue, GitHub Actions, merge, deployment, account, billing, or workload was changed or invoked. All implementation and integration tests remain NOT RUN; local PC and hosted execution state remain UNKNOWN.


## 13. Resource-containment and teardown evidence pass

A new source-grounded research artifact was created:

- `AI_COLLAB/RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md`
- Initial create commit: `d63ebc339ab6764d647ffdac721c82449a0e19bb`
- Final blob after source clarifications: `477674c773aeadae979c64c06a07770974e316a7`
- It defines local test-design IDs RES-01..09 and TDN-01..08. These are not canonical LOOP/CASE IDs.

Additional documentation updates:
- `AI_COLLAB/LIFECYCLE_CONTRACT_REGRESSION_PLAN_20261101.md`: detailed resource/teardown review pointer and semantic corrections. Commit `066e49e68770debbc31b5a51855bcdeae7e233b5`; blob `8b2f23833d5d2aec59df70a56db9c52f8af73975`.
- `AI_COLLAB/REVDEV_POCKETCODE_CROSSWALK_INDEPENDENT_REVIEW_20261101.md`: source-specific findings and corrected evidence boundaries. Commit `e8945bc364d82269c37ab65ccf1e0bcbc772b887`; blob `d7d34194d72c9d0795f856e377dc2ff5dcb3e9fa`.
- `RESEARCH/EXECUTION_PROVIDER_RESEARCH.md`: provider lifecycle/resource documentation recheck supplement. Latest commit `33aea5f99687d70266ef8356acffeefb7e58bf31`; blob `231f9cfda80ab52726e265e5160d1f97486458a6`.
- `AI_COLLAB/IMPLEMENTATION_READINESS_BACKLOG_20261029.md`: added WP-08, explicitly BLOCKED on owner decisions, selected/approved provider/runtime, budget, durable evidence and integration. Commit `fa5f8af5181e8b805ff1be56bb43eef9b0e34bd9`; blob `75a73621b78f77e87ed0abc84691f45453268e5d`.

Key source-grounded corrections:
1. cgroup v2 `memory.max` is a hard memory boundary but does not imply every allocation failure produces OOM kill. `memory.events.local` is preferred for local attribution; `memory.swap.max` is separate.
2. `cpu.max` is CPU bandwidth, not wall-clock termination. `pids.max` counts kernel tasks/TIDs.
3. `io.max` is I/O throughput, not disk capacity. `RLIMIT_FSIZE` is per-file, not total workspace size.
4. `cgroup.kill` sends SIGKILL to a cgroup subtree; `cgroup.events: populated=0` confirms no live process in that subtree, not remote resource deletion.
5. A delete API can be asynchronous. Daytona v2 progresses from deleting/destroying to deleted/destroyed; its call returns when teardown starts. Stable v0 offers a wait option because default delete is fire-and-forget. Modal documents `terminate(wait=True)` as waiting for sandbox finish and returning exit code. These signals must not be generalized to separately attached storage or billing release.
6. Firecracker Jailer leaves cleanup to its operator and warns of cleanup-registration races. It is a building block, not a turnkey hosted service.
7. Modal resource request and hard limit are distinct; default outbound public-IP access is allowed. Cloudflare destroy is immediate and does not allow relying on process cleanup handlers. E2B's microVM claim is vendor architecture information, not independent proof.

Decision: PC-EXT-02 and PC-EXT-04 remain genuine provider/runtime evidence gaps. No provider selected. RES/TDN are test-design labels only. No account, API key, workload, provider call, paid usage, implementation or test run occurred. WP-08 is BLOCKED under the $0 constraint.


## 14. OOM evidence attribution refinement

The resource review received a final kernel-semantics correction (commit `609b252f669d91bd22b2dd23142744c16b3eaa00`, blob `dbb1bac56097d85e8fd20e1ccaa4583ce20d6844`): `memory.events.local:oom_kill` counts processes in the cgroup killed by any OOM killer. It cannot alone prove the target cgroup's own `memory.max` caused the kill. Conversely, some memory-limit failures return `-ENOMEM` without OOM kill. Tests must correlate effective memory/swap limits, local `max`/`oom`/`oom_kill` deltas, exact cgroup/PID membership, trusted termination evidence and supervisor/sibling health. No single counter is proof of causation.

This refinement is reflected in the lifecycle regression plan and independent review. It does not alter canonical acceptance or authorize execution.


## 15. Final verified checkpoint for resource/teardown pass

Read-back verified final blobs:
- Resource review: `dbb1bac56097d85e8fd20e1ccaa4583ce20d6844` (commit `609b252f669d91bd22b2dd23142744c16b3eaa00`).
- Lifecycle regression plan: `05c4ff9eca8f7816831348a077fcd356b33e4c53` (latest OOM clarification commit `2ac1c4d9105295821bc7089c4e535ccd7e97092b`).
- Independent review: `da7dc4e8644a948f410c2d1cee502db333f1b07e` (latest OOM clarification commit `6d07c8bf61c20eef012007dab8a2f0db43c75a57`).
- Implementation readiness backlog: `75a73621b78f77e87ed0abc84691f45453268e5d` (WP-08 commit `fa5f8af5181e8b805ff1be56bb43eef9b0e34bd9`).
- Provider research: `231f9cfda80ab52726e265e5160d1f97486458a6` (latest provider refresh commit `33aea5f99687d70266ef8356acffeefb7e58bf31`).

The current research branch ref was `287eb770fff8ac6ea6f5b0b9ca71a3e3790140c0` before this final handoff update. This update becomes the new branch HEAD.

Branch separation was checked again:
- Main: `555840d8d83342513d9cd353d4d1522d46a5c82d`.
- PR #2: OPEN, DRAFT, UNMERGED; head `eb8b7ea83cb0e8fe1880351276c485b761431791`, base main.
- PR #3: OPEN, DRAFT, UNMERGED; head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`, base main.

Only documentation files on the existing research branch were written. No canonical acceptance, source, implementation tests, PR head, main, provider, account, runtime, queue, Actions, billing or deployment was touched. All RES/TDN cases and implementation/integration tests remain NOT RUN. No provider is selected; WP-08 remains BLOCKED.


## 16. Claude resource/teardown challenge reconciliation — 2026-11-01

### Review limitation and disposition

Claude explicitly stated that it could not read the three new research-branch AI_COLLAB documents and therefore could not verdict RES/TDN. Do not describe its reply as a review of those files. ChatGPT independently reconciled its claims against the pinned canonical acceptance, SECURITY.md, the main-branch provider research, and the exact research-branch documents. The useful challenges were accepted and recorded as a source-reconciled addendum.

### New/changed records

1. Resource and teardown evidence review, blob `e86cacdd2960b86bc4030c971f7a6306f605e832`, commit `ea64aba8d16a7dca50c305d6d46bb58fcfa38490`:
   - strengthened RES-02, RES-08 and RES-09;
   - tightened TDN-02/03/04/05/07/08;
   - added TDN-09 lost create acknowledgement and TDN-10 warm/reused sandbox contamination;
   - recorded no canonical cleanup-confirmed ID and no resource-limit lifecycle status;
   - added hierarchical/local cgroup event semantics, mount-option checks, OOM/timeout race attribution, observer survival and pre-removal snapshots;
   - clarified Firecracker is a VMM/microVM building block, not a managed sandbox service.
   - URL: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md
2. Lifecycle regression plan, blob `0135df7d894fbaa7017bed58bde7f86a89eb59a6`, commit `b23231e9549658a9922a90f3be29c49ffcc4e055`:
   - added Claude-review reconciliation and canonical-boundary notes;
   - corrected cgroup evidence guidance to include actual hierarchy, mount options, local and hierarchical counters, OOM/timeout race and pre-removal evidence;
   - retained all PC-LC/AD/DB/RT and RES/TDN tests as NOT RUN.
   - URL: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/LIFECYCLE_CONTRACT_REGRESSION_PLAN_20261101.md
3. Implementation readiness backlog, blob `449047335f97fd59bf8a0ae0ebcd92aee9c27c4a`, commit `e9d9c523e117ca03850db8758c82c3b239ed753c`:
   - strengthened WP-08 worker isolation, cgroup evidence, create/delete intent, ambiguous 404, warm reuse and cross-attempt checks;
   - added a separate Claude challenge reconciliation note;
   - WP-08 remains BLOCKED.
   - URL: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/IMPLEMENTATION_READINESS_BACKLOG_20261029.md

### Technical corrections now in the records

- The canonical lifecycle enum has no resource_limit_exceeded state. OOM, ENOSPC, per-file size, PID and I/O events must retain typed cause, enforcement layer, observer and child-terminal evidence. Classification as program/runtime failure versus infrastructure failure remains open where owner decisions D-01/D-02 do not settle it.
- CASE-07 is stdout/stderr output cap; CASE-14 is output-file path/size safety. Neither proves total workspace disk capacity or I/O throughput.
- There is no standalone canonical cleanup-confirmed case. TDN stays supplementary.
- Kernel cgroup v2 docs: memory.events is hierarchical by default, memory.events.local is local-only, and memory_localevents can change memory.events to local-only. pids.events has a similar hierarchical/local distinction and pids_localevents option. Capture actual mount options and topology; a local read on a job parent may miss descendants, while a broad hierarchical parent can mix attempts.
- oom and oom_kill are different observations. oom_kill counts processes in the cgroup killed by any OOM killer; it does not prove the cgroup's own memory.max caused the kill. Exit 137/SIGKILL does not resolve an OOM/timeout race.
- Capture counters before cgroup removal. The observer/supervisor must survive outside the workload kill domain.
- A lost create acknowledgement requires durable pre-call intent and scoped/paginated orphan reconciliation. Fake/pure tests alone cannot prove that persistence property.
- LOOP-14 gates any provider account, billing enablement or potentially billable workload. A fake cannot prove that charges stopped.

### Current proof status and next action

- Read-back verified all three updated blobs on the existing research branch. Latest research-branch commit at this checkpoint: `e9d9c523e117ca03850db8758c82c3b239ed753c` before this handoff file update.
- No source/test/PR/main/canonical acceptance/provider/runtime/queue/Actions/account/billing/host state changed. No tests, provider calls or workloads run.
- All RES/TDN and PC-LC/AD/DB/RT cases remain SPECIFIED ONLY / NOT RUN. WP-08 remains BLOCKED, provider selection NONE, budget $0.
- Next reviewer step: provide Claude these exact three blob URLs and request a source-backed verdict on the updated content, not the inaccessible path names. Separately resolve the outstanding Gemini OBS/fixture namespace collision before merging any reviewer observation IDs into the existing register; do not reuse ChatGPT OBS-01..06 labels for Gemini's differently described observations.


## 17. Gemini AWC namespace collision — source-verified (2026-11-01)

A direct fetch of the authoritative RevDev AWC files resolved the pending identifier concern. The AWC fixture source is in `marcelosofficial-ctrl/DevRelay-Missions`, not the PocketCode repository root:
- Manifest: `resume/revdev/AI_WORK_COACH_SYNTHETIC_FIXTURES_V0_1.json`, blob `c2d4cba6c836f725f7bc4585f91e02d443fe89e1`, 18 fixtures AWC-001..018, status PROPOSED_NOT_RUN.
- Specification: `resume/revdev/AI_WORK_COACH_FIXTURE_AND_MEASUREMENT_SPEC_V0_1.md`, blob `9169ae6c6e5689f70287b7c6c0aeac534d8f7183`.
- Semantic matrix: `resume/revdev/AI_WORK_COACH_RUN_RECORD_SEMANTIC_CONFORMANCE_MATRIX_V0_1.md`, blob `6618d878747e4d09dd82f0b5228f5f9f3c175927`.
- Static audit: `resume/revdev/AI_WORK_COACH_SYNTHETIC_FIXTURE_MANIFEST_STATIC_AUDIT_2026-10-29.md`, blob `333f6732499bd8f32ceb78f9e95c6001d9b6ed5e`.

Gemini's supplied response used the labels AWC-005/008/009/010/011/012/017/018 for subjects that do not match those fixtures. The pinned manifest says, respectively: security-sensitive untrusted shortcut; failed targeted repair recovery; request to bypass a limit; task handoff to an assistant without a connector; untrusted source-file policy text; fabricated token/time/cost telemetry; unknown provider/model/plan/host capabilities; truncated evidence without a completion signal. Therefore those Gemini labels are not accepted as references to this AWC fixture set without an alternative artifact path/ref/blob SHA.

Gemini's actual engineering suggestions are retained under the proper concerns: cgroup/worker containment -> RES-02/08; applied network-policy barrier -> D-05/PBR/PF; artifact/encoded-secret leakage -> release boundary/AR-01..14; truncation taxonomy -> execution/report evidence model; outcome/cleanup separation -> report projection; atomic semantic idempotency -> DR-01..12/PC-AD/DB; cross-attempt event/log binding -> PC-LC-03; release-time revalidation -> AR; cost lag -> separate cost observability/LOOP-14. No suggestions are discarded, but they do not get mismatched AWC labels.

The helper OBS-01..06 meanings remain exactly as source-pinned in the crosswalk. Gemini's six differently described observations remain an independent unnumbered reviewer set until exact source references are provided. No OBS renumbering or overwrite is allowed.

Crosswalk source reconciliation update:
- `AI_COLLAB/REVDEV_POCKETCODE_CROSSWALK_INDEPENDENT_REVIEW_20261101.md`, blob `e052a3c989acfb15a939b26fb99ba3cc7fcfe773`, commit `06200ee9bf596871cfa62c236b80c89dec973567`.
- URL: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/REVDEV_POCKETCODE_CROSSWALK_INDEPENDENT_REVIEW_20261101.md

Next step: request from Gemini the alternative artifact path, repository, branch/ref, blob SHA, and exact line references for the AWC IDs it used. If no alternative AWC artifact exists, it must correct the labels while preserving its useful engineering findings. The AWC fixture set itself remains PROPOSED_NOT_RUN.

This was documentation and source verification only. No AWC trial, model run, PocketCode test, provider call, workload, source/test/PR/canonical acceptance change, Actions, spend, merge or deployment occurred. The research branch immediately before this handoff update was `06200ee9bf596871cfa62c236b80c89dec973567`.


## 18. Final verified continuation snapshot — Claude + Gemini reconciliation (2026-11-01)

This section supersedes the earlier preliminary blob/commit references in Sections 16–17 where a later date-correction commit replaced the file blob. The human-readable links remain stable, but use these final blob identities for exact source pinning:

| Document | Final blob SHA | Current link |
|---|---|---|
| Resource containment and teardown review | `178498a9e2e44babc87f405fc1e81d29c19df555` | https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md |
| Lifecycle contract regression plan | `34bc74f82df5e6714bd872c63f3d86b7e4c93bf4` | https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/LIFECYCLE_CONTRACT_REGRESSION_PLAN_20261101.md |
| Implementation readiness backlog | `7645b908f5079cf7cd23061319fc775086cfb7e3` | https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/IMPLEMENTATION_READINESS_BACKLOG_20261029.md |
| RevDev ↔ PocketCode crosswalk review | `2e577636535bff05916ae21e4e9b63db040deb37` | https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/REVDEV_POCKETCODE_CROSSWALK_INDEPENDENT_REVIEW_20261101.md |
| This handoff addendum (before this final snapshot append) | `b327f2c854968559acf21b9662b65223af3bad15` | https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/CHAT_HANDOFF_ADDENDUM_20261101.md |

Latest research-branch commit before this final handoff append: `4d5d9c2bfedfe4f92ed5f53df9c9cacebf63658a`.

### Source verification

- All four substantive documents and the handoff were fetched again from the research branch. Their current blob SHAs matched the final values above.
- Resource review read-back confirmed RES/TDN additions, OOM/timeout race text, and cgroup mount-option clarification.
- Lifecycle plan read-back confirmed canonical cleanup/resource-status boundary, LOOP-14 gate, and cgroup hierarchy guidance.
- Backlog read-back confirmed WP-08 remains BLOCKED and records write-ahead create/delete and resource observer requirements.
- Crosswalk read-back confirmed the exact AWC-005/008/009/010/011/012/017/018 fixture definitions, and its OBS namespace rule is in Section 13.3. Preserve helper OBS-01..06; Gemini's six differently described observations remain unnumbered until Gemini supplies exact source references.
- All dates in the newly added review sections are 2026-11-01. Gemini's supplied review self-reports 2026-11-02; that is retained solely as unverified input provenance and is not the date of this work.

### Additional kernel documentation precision

The Linux kernel cgroup v2 documentation states that `memory.events` includes descendant events by default, with `memory_localevents` restoring local-only behavior; `memory.events.local` remains local to the cgroup. Its `oom` counter is about the cgroup's limit-reaching allocation event, while `oom_kill` counts processes belonging to that cgroup killed by any OOM killer. These are different attribution dimensions and should not be treated as a matched one-to-one causal pair. `pids.events` is hierarchical by default, `pids.events.local` is local, and `pids_localevents` restores local-only behavior. See https://www.kernel.org/doc/html/v6.14/admin-guide/cgroup-v2.html. Record both limit-owner cgroup and victim process membership, plus the mount options and exact hierarchy. This is kernel semantics only, not evidence that PocketCode currently uses cgroups.

### Final state

- Documentation-only changes on the existing research branch.
- No source, implementation tests, PR, main, canonical acceptance, Actions, provider, account, billing, workload, runtime, queue, local host or security boundary changed.
- No tests, provider calls or workloads run. All RES/TDN and PC-LC/AD/DB/RT remain SPECIFIED ONLY / NOT RUN.
- Provider selection NONE; budget $0; WP-08 BLOCKED; D-01..D-08 remain open as previously recorded.
- Claude did not review the new files because its fetch failed. Gemini's AWC source IDs are mismatched against the pinned manifest; request exact alternate source pins before reconciling its labels.


## 19. Provider API-generation and host-output research pass — 2026-11-01

### What changed

A second official-documentation pass identified a material Cloudflare API-generation distinction, a Modal create/detach/terminate distinction, and a host-side Firecracker output-exhaustion path. These were added as documentation-only updates on this research branch:

1. Resource containment and teardown review, final blob `2fd1ddee9674c59719fbd3f93c95004d754c927`, commit `d6c29b8b9ed6d6a96f261394a34ad6cd2acb591a`:
   - Cloudflare section now distinguishes current `@cloudflare/sandbox` 1.0 Durable Object + Container lifecycle from legacy SDK 0.x `destroy()` semantics.
   - TDN-05 now includes Durable Object/control-plane storage, snapshots, mounted buckets, preview/tunnel resources and other separately managed resources.
   - RES-08 includes host-side VMM/log collector memory/disk bounds; RES-09 requires the workload cannot migrate processes out of the observed cgroup subtree; added RES-10 for guest-controlled Firecracker serial/VMM log pressure.
   - URL: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md
2. Provider research, final blob `900476c031c031f4a88f2a0eb42e0526f3e8e07f`, commit `9a01b95266cd0c4931cc602c36f25c1d06083691`:
   - Provider matrix and distinctions updated for Cloudflare API generations, Modal async create/detach/terminate and Firecracker host log handling.
   - URL: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/RESEARCH/EXECUTION_PROVIDER_RESEARCH.md
3. Lifecycle regression plan, final blob `90fd54a10f7e638631da10749fcdac9ac6c1e610`, commit `eeae952ce7e32f7dcc25eb8c863444bd6c80cab4`:
   - added PC-EXT-08 provider API-generation/resource-scope reconciliation and PC-EXT-09 host-side VMM/log-sink containment.
   - strengthened PC-EXT-02 and PC-EXT-04 with process membership and provider resource scope requirements.
   - URL: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/LIFECYCLE_CONTRACT_REGRESSION_PLAN_20261101.md
4. Implementation readiness backlog, final blob `de61496d85c3ffd2d945b6fc40bdedbbbc3d825d`, commit `fa9302b60d34d3967c6f12b8cd3a1d4c571ece52`:
   - WP-08 now explicitly includes PC-EXT-08/09, API generation pinning, and host VMM/log containment.
   - WP-08 remains BLOCKED.
   - URL: https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/IMPLEMENTATION_READINESS_BACKLOG_20261029.md

### Research findings that affect architecture

**Cloudflare:** Current Sandboxes lifetime docs describe a Durable Object identity/storage layer separate from the container instance. The DO's storage survives instance stop until application code deletes it; snapshots and mounted R2 buckets have their own persistence. Instance-local processes/files end when the container stops. Explicit destroy stops the instance without a graceful cleanup window. The legacy Sandbox SDK 0.x docs separately describe deleting that SDK's sandbox files/processes/sessions. Do not apply the 0.x guarantee to current 1.0 Durable Object storage, snapshots or mounted buckets. Cloudflare Sandboxes are Workers Paid; active instance resource billing is documented. Sources: https://developers.cloudflare.com/sandbox/concepts/lifetime/ ; https://developers.cloudflare.com/sandbox/sdk/api/lifecycle/ ; https://developers.cloudflare.com/containers/platform/pricing/ ; https://developers.cloudflare.com/sandbox/files/save-and-restore-a-workspace/.

**Modal:** Python SDK docs state that `Sandbox.create` provisions the corresponding container asynchronously; `detach()` disconnects the client and cleans connection resources; `terminate(wait=True)` waits for execution termination and returns an exit code. `from_id`, `from_name(include_terminated=True)` and `list` provide identity-based lookup surfaces. These are distinct operations and do not establish attached volume release. Source: https://modal.com/docs/sdk/py/latest/Sandbox.

**Firecracker:** Production host setup explicitly warns that guest-controlled serial output and guest-influenced log generation can cause unbounded host memory/storage use unless sinks are rate-limited, bounded or discarded safely. A PocketCode report cap alone does not protect host VMM logging. Source: https://github.com/firecracker-microvm/firecracker/blob/main/docs/prod-host-setup.md.

**cgroup membership:** `cgroup.events: populated=0` means no live processes in that cgroup and descendants at the observation time. It does not prove a process was never moved outside the observed subtree. Prevent workload-controlled cgroup migration and keep the supervisor's membership boundary authoritative. Source: https://www.kernel.org/doc/html/v6.14/admin-guide/cgroup-v2.html.

### Final status and proof boundaries

- RES-10 and PC-EXT-08/09 are supplementary test-design IDs only. No canonical LOOP/CASE IDs or lifecycle statuses were added or remapped.
- The Cloudflare distinction corrects an overbroad reading of `destroy()`; resource classes and API generations are now explicit.
- No provider selected. No provider APIs, accounts, workloads, billing, local host tests or runtime operations used.
- All RES/TDN and PC-LC/AD/DB/RT/EXT tests remain SPECIFIED ONLY / NOT RUN. WP-08 remains BLOCKED; budget $0.
- No source code, implementation tests, main branch, PRs, Actions, queues or deployments changed.


## 20. Firecracker serial limiter default verified — 2026-11-01

A further exact-source check of Firecracker's current API schema found that serial-console rate limiting is **optional**, not enabled by default. When configured, guest serial writes above the token-bucket rate are dropped and counted in `uart.rate_limiter_dropped_bytes`; when absent, serial output is not rate-limited. This refines RES-10/PC-EXT-09: test the effective serial configuration and dropped-byte metric, and independently bound VMM stdout and guest-influenced log sinks. Do not infer that Firecracker automatically rate-limits serial output.

Pinned source: `firecracker-microvm/firecracker`, branch `main`, `src/firecracker/swagger/firecracker.yaml`, blob `245c8e4473a43befbd1d5a28ecece098a994a815`. Production host guidance: `docs/prod-host-setup.md`, blob `8939b56a965963d8df1c44c583dcd38361197347`.

Updated PocketCode docs:
- Resource review blob `df6eda10467069738eb72818fc4b36ddd69b7889`, commit `71be16af411aa1bf573ad3f1cff36d773ece8d58`.
- Provider research blob `e754aee41858e45e0fb907a7f46df442a757f317`, commit `4a0aee6f8485b8cbf70bddb8067f2536130ff53f`.
- Lifecycle plan blob `f33d2deeabb97a36c5916eb86de1f88d2b375acd`, commit `95ae1df46abe9a730b409eba44426327121b10b8`.
- WP-08 backlog blob `a13788cc48c23cb3d2c98c4f6118c03e79479bdb`, commit `01144816ae99eb77a6ee2d962951e3d3901b40e4`.

All additions remain design-only. No implementation, tests, provider, workload, account, host operation or spending occurred.


## 21. Final continuation pins after Firecracker schema pass — 2026-11-01

Final current blob identities for this checkpoint:

| File | Blob SHA |
|---|---|
| `AI_COLLAB/RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md` | `df6eda10467069738eb72818fc4b36ddd69b7889` |
| `RESEARCH/EXECUTION_PROVIDER_RESEARCH.md` | `e754aee41858e45e0fb907a7f46df442a757f317` |
| `AI_COLLAB/LIFECYCLE_CONTRACT_REGRESSION_PLAN_20261101.md` | `f33d2deeabb97a36c5916eb86de1f88d2b375acd` |
| `AI_COLLAB/IMPLEMENTATION_READINESS_BACKLOG_20261029.md` | `a13788cc48c23cb3d2c98c4f6118c03e79479bdb` |
| `AI_COLLAB/POCKETCODE_CURRENT_CHECKPOINT_20261028.md` | `897db38b4f7ae32bb7c7c3849c49a583938bebf6` |
| `PROJECT_STATUS.md` | `9d8e5bd049fa90584546a598f843b95d6abd8ec6` |
| `AI_COLLAB/CHAT_HANDOFF_ADDENDUM_20261101.md` (before this section is appended) | `0d0b4b736a6521711672aadde1d66c1a0cc6365f` |

The RevDev/PocketCode crosswalk review remains blob `2e577636535bff05916ae21e4e9b63db040deb37` unless separately updated; it contains the source-verified AWC namespace correction.

The PocketCode research branch HEAD before this handoff append was `41ec4aba3d0d48d2d8d96a7e5ba69f0adfa0b198`. The checkpoint and Project Status were read back after their updates. The latest queue now requests Claude's source-backed review of the exact resource/lifecycle/backlog URLs, Gemini's exact alternate AWC source pins, and then same-task product validation. No implementation/provider gates have changed.

### Final boundaries

- RES-10, PC-EXT-08/09 and TDN-09/10 are supplementary design IDs only.
- Canonical LOOP-01..14 / CASE-01..16 remain unchanged; no lifecycle status or owner decision was added.
- All tests remain SPECIFIED ONLY / NOT RUN; no provider selected; WP-08 BLOCKED; budget $0.
- No source/test, PR #2/#3, main, Actions, account, API, billing, workload, host, queue, merge or deployment changed.
- Local PC/source/binary/runtime/queue state remains UNKNOWN until the owner regains PC access.


## 22. Product-path comparison desk review — 2026-11-01

Added [PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md](PRODUCT_PATH_COMPARISON_DESK_REVIEW_20261101.md), blob `2592cafe479faed5059357074b5e7cbd80fc22ae`, after reviewing the existing fixed-task worksheet and product hypothesis, current official/maintainer documentation, and relevant platform documentation.

### Main findings

- Pyodios is the strongest direct iOS local-Python comparator for the fixed standard-library CSV task. Its own FAQ reports a 300 MB Python memory budget, 5–15 second initialization, fresh sessions after app launch, and a 120-second UI timeout that does not stop the running code; recovery requires a Python session restart.
- Browser-local Pyodide remains plausible on iOS, but the distinction between Safari OPFS and a user's visible Files directory matters. Pyodide's experimental direct native-directory mount is documented as Chromium-only; a Safari route should use explicit import/export or a tested origin-private workspace.
- AndroidHarness and PhoneCode make generic local mobile-agent positioning substantially less distinctive. PhoneCode explicitly separates its PRoot debug prototype from its gated QEMU Google Play architecture; do not treat the latter as a released, fully proven runtime.
- Atlan is an Android power-user alternative; its own security docs say proot Bash is not OS-sandboxed and its reported confinement tier is device-specific.
- Codeg and Pairlet are remote-host clients, not phone-only execution. Codespaces has included personal-account compute/storage quotas, not unlimited free usage.
- The report/receipt concept is not yet a proven differentiator. Competitors already expose tool activity, logs, session continuity and handoff features.

### Next experiment

The desk review specifies a paired raw-evidence versus portable-receipt experiment. Both conditions must receive exactly the same source, input and observed run facts; the receipt may reorganize but not add facts or diagnoses. Measure correction accuracy, provenance preservation, verification honesty, user steps and turns. The malformed CSV case may be ceiling-limited; if so, define a separate failure fixture before collecting results. A synthetic receipt can test information design only, not end-to-end execution value.

### Status and boundaries

- Product-path claims are source review only; no app installed, no code executed, no interview conducted.
- Fixed CSV comparison and raw-vs-receipt experiment remain NOT RUN.
- No product hypothesis, architecture, provider, MVP or owner decision has been accepted or changed.
- No source/implementation tests, PRs, main, Actions, accounts, provider APIs, workloads, billing, host operations, merge or deployment changed.
- Budget remains $0; PC/runtime/queue state remains UNKNOWN until PC access returns.

Primary sources and verification date are listed in Section 8 of the desk review.


## 23. Report contract traceability follow-up

The product-path desk review now includes Section 9. The proposed portable receipt must reuse the existing proposed report contract and LOOP-07/08 rather than invent a parallel schema. The paired experiment compares raw evidence against the exact same facts rendered through the proposed report, with no added diagnosis or omitted material evidence. This is design-only; no new acceptance ID or schema change.


## 24. Final product-path research pins — 2026-11-01

- Product path comparison desk review: `035f8db30f1512ad1c9d3e4fa19edf13dbf0ca86`.
- Current checkpoint with Claude/Gemini review prompts: `bab4e70c9b8ebec4fbba2e5d2abe633d790b1e9c`.
- Project status: `15929f3d0d2387b68641f517fbf1fddf73b69275`.
- Handoff before this final pin section: `187f06627c78b98d08b47f5889deb49c7c0ff715`.

The product-path desk review is source-backed desk research only. The next action is adversarial review by Claude and Gemini using the prompts in the current checkpoint, followed by a decision whether a hands-on fixed-task test is worth undertaking. The proposed report remains the existing LOOP-07/08 report projection; no new receipt schema or acceptance ID. No app installation or direct test was performed.
