# PocketCode — Open-Source Reuse Audit

**Review date:** 2026-10-29  
**Status:** Public-source and repository-document review; no competitor code copied, no build/tests run, no PocketCode runtime selected.  
**Scope:** Find prior work that can reduce PocketCode's custom engineering across phone-first coding, execution lifecycle, truthful evidence, recovery, provider neutrality, and cross-AI continuation.

## Executive decision

**Reuse patterns and conformance ideas now; do not vendor an agent framework or execution runtime yet.** The strongest sources show that many proposed PocketCode features already exist elsewhere. The product hypothesis cannot rely on generic tool logs, mobile AI coding, error handoff, session recovery, or a structured run record as unique by themselves.

The current PocketCode proposal already has valuable foundations: a provider-neutral execution contract, separate user verdict vs exact lifecycle status, unknown evidence kept explicit, bounded stdout/stderr, file metadata, explicit timeout/cancellation semantics, and no PASS without trusted terminal evidence. Keep the existing contract as the one candidate schema; do not fork it into a new “receipt schema.” The best additions from prior art are mostly stronger conformance fixtures and recovery semantics, not more fields or a bigger framework.

## Findings and recommended adoption

### 1. RunSeal — execution protocol, policy and conformance (highest value for contract review)

**Sources:** [RunSeal implementation](https://github.com/runseal-labs/runseal), [RFC-0006 stable execution protocol](https://github.com/runseal-labs/rfcs/blob/main/rfcs/0006-stable-execution-protocol.md), [RFC-0021 real-time protocol v2](https://github.com/runseal-labs/rfcs/blob/main/rfcs/0021-realtime-execution-protocol-v2.md), [RFC-0016 adversarial conformance](https://github.com/runseal-labs/rfcs/blob/main/rfcs/0016-adversarial-conformance-harness-and-case-format.md). Repository license: Apache-2.0. Maintainer status: technical preview; Windows reference backend, other platform backends experimental. This is not an independent security audit.

**Useful patterns to map onto PocketCode:**
- One lifecycle owner is responsible for start, streaming output, cancellation/timeout, cleanup and terminal publication; avoid contradictory “CLI says cancelled / worker still running” states.
- Separate the execution's own result from wrapper/coordinator errors. RunSeal's CLI wrapper status and child process exit status are distinct.
- Explicit capability discovery and fail-closed behavior when a requested capability is unsupported; a skipped test is not a pass.
- Ordered structured events / JSONL audit, stable execution IDs, versioned protocol, immutable policy identity for the duration of a run, and adversarial black-box conformance tests.
- Treat timeout/cancellation as proven only when the execution boundary confirms it; do not infer process death from a client timer.

**PocketCode application:** use these as cross-checks for the existing proposed lifecycle contract and the PR #3 reconciliation. Add missing expectations to the fixed-task/conformance matrix only when they clarify a real gap. Do not copy RunSeal's OS-specific sandbox code: it is Rust/desktop OS infrastructure and is not an iOS/Android/browser sandbox drop-in. Do not import RunSeal's state machine wholesale; PocketCode's accepted lifecycle vocabulary and PR #3 status still require reconciliation.

### 2. AndroidHarness — phone-native task receipts, recovery and diagnostics (highest value for phone UX patterns)

**Sources:** [AndroidHarness](https://github.com/Sanuu7/AndroidHarness), [README and implementation overview](https://github.com/Sanuu7/AndroidHarness/blob/main/README.md). Root license: MIT. Android/Kotlin-specific; maintainer-described features, not independently verified by this review.

**Useful patterns:**
- Persist completed tool results before advancing to the next model action; after interruption, resume from a durable checkpoint instead of replaying completed writes.
- If an operation's completion is uncertain, show a recovery/inspect step instead of blindly repeating it.
- Build diagnostics from a fixed whitelist of safe fields and state missing logs/collection failures explicitly.
- Name the actual execution backend in the receipt; use a digest to reject stale edits.
- Use a doctor-style capability self-test to report what works on the current device, instead of a blanket “supported” label.

**PocketCode application:** map these patterns to the future AI Workflow Director continuation capsule, report privacy requirements, and mobile preflight. Keep the first Director evaluation local/manual and supporting. A general phone-agent implementation is not the target, and AndroidHarness is not an iOS implementation. Do not copy Kotlin UI/runtime code into the current platform-neutral product.

### 3. PhoneCode — crash-safe sessions and strict runtime claims

**Sources:** [PhoneCode](https://github.com/dttdrv/phonecode), [mobile backend boundary](https://github.com/dttdrv/phonecode/blob/main/MOBILE_BACKEND.md), [third-party inventory](https://github.com/dttdrv/phonecode/blob/main/THIRD_PARTY.md). Original project code: Apache-2.0. Its inventory identifies additional third-party components with separate licenses, including PRoot (GPL-2.0 family) and talloc (LGPL-3.0 family). Android-specific, and its production runtime design is in active migration per its documentation.

**Useful patterns:**
- Crash-safe sessions, atomic state writes, explicit tool checkpoints, bounded retries and explicit recovery when the OS interrupts a task.
- Keep provider credentials and app state outside the untrusted execution guest; expose only explicit files/channels.
- Make unsupported runtime boundaries explicit. A path translator such as PRoot is not automatically a security sandbox.
- Use a release gate that blocks distribution until runtime isolation, licensing/provenance and device lifecycle evidence pass.

**PocketCode application:** add these as future implementation/release checks, not as claims about our current static prototype. Do not vendor PhoneCode's whole runtime or any bundled dependency before component-level license/provenance review. Its Android-specific VM work does not resolve iOS execution or browser sandbox decisions.

### 4. OpenHand — provider-neutral modularity and failure taxonomy

**Sources:** [OpenHand repository](https://github.com/ricardo-foundry/openhand), [error-handling strategy](https://github.com/ricardo-foundry/openhand/blob/main/docs/ERROR_HANDLING.md). License: MIT. TypeScript monorepo, relatively small by agent-framework standards, but it is a general agent runtime rather than a tiny execution receipt library. Its own docs warn that its allowlist sandbox runs under the host UID and is not OS-level isolation unless placed in a stronger boundary.

**Useful patterns:**
- A narrow provider interface so provider changes do not leak throughout product logic.
- Separate user/input errors, provider errors, sandbox/execution errors and internal errors; retry only known transient classes with bounded attempts and delay.
- Do not show raw provider responses, stack traces or headers to users; retain safe structured diagnostics with correlation IDs.
- Test protocol adapters and streaming failure paths with fake providers and deterministic fixtures.

**PocketCode application:** retain the existing provider-neutral boundary. Use the error taxonomy as a review checklist when the contract/error categories are reconciled. Do not adopt its runtime wholesale or mistake command allowlists for an OS sandbox. Exact TypeScript modules are a future candidate only if PocketCode chooses a compatible TypeScript runtime and the module saves more work than its dependencies add.

### 5. Pairlet — remote-host continuity and capability matrix

**Sources:** [Pairlet](https://github.com/heypandax/pairlet), [contributor architecture and test guidance](https://github.com/heypandax/pairlet/blob/main/CONTRIBUTING.md), [observability documentation](https://github.com/heypandax/pairlet/tree/main/docs/observability). Root project license: MIT (verify all transitive components before code reuse). Pairlet's primary execution model requires a separate computer/daemon; it is not a no-PC execution substitute.

**Useful patterns for a later host-available scenario:**
- Reconnect with missed event backfill; explicit approval prompts; safe deny on approval timeout.
- A capability matrix per backend rather than pretending every agent supports the same operations.
- Distinguish client-side observation from end-to-end correlation and from server-confirmed completion.
- Keep diagnostics opt-in, structured and privacy-filtered; record partial/incomplete log reads explicitly.

**PocketCode application:** use the backend capability matrix if a remote-PC option remains in the study. Do not make Pairlet or a remote daemon the default while execution location remains undecided and PC access is unavailable.

### 6. OpenHands — event history and sandbox/runtime separation

**Sources:** [OpenHands](https://github.com/OpenHands/OpenHands), [OpenHands sandbox server](https://github.com/OpenHands/sandbox-server). Core repositories are MIT-licensed, with an enterprise-directory carve-out in the main repository. Large and fast-moving; check the exact subrepository and directory license before reuse.

**Useful patterns:** separate UI/client, agent SDK, server/control plane and execution workspace; keep a reviewable event history; use isolated workspaces; expose stable client abstractions rather than coupling UI directly to one runtime.

**PocketCode application:** architecture inspiration only. The full framework is too broad for our narrow, $0 first workflow. If we ever use a component, choose the smallest standalone, MIT-covered module and verify the exact pinned revision, dependency graph, mobile/browser compatibility and license notices first.

## Cross-project adoption matrix

| PocketCode concern | Best prior-art pattern | Where to apply it | Decision |
|---|---|---|---|
| Truthful run lifecycle | One owner, child exit separate from wrapper failure, explicit timeout/cancel confirmation | Existing execution contract + PR #3 crosswalk | Adopt as review criteria; reconcile states before edits |
| Audit/report provenance | Ordered events, source labels, bounded logs, explicit unknown/missing evidence | Existing report contract + fixed-task worksheet | Adopt test criteria; do not create a second schema |
| Recovery after interruption | Persist completed step before next action; never replay uncertain writes blindly | Director capsule proposal and future session design | Adopt as future design requirement |
| Device/backend support | Capability discovery, safe fixed whitelist, per-backend capability matrix | Mobile preflight and competitor matrix | Adopt in the test protocol |
| Provider portability | Thin provider interface and deterministic adapter tests | Existing provider-neutral architecture | Keep; reuse implementation only after stack choice |
| Security boundary | Fail closed; explicit runtime isolation; separate secrets and untrusted code | SECURITY.md, acceptance gates, PC-return checklist | Adopt as mandatory gate; no security claims from docs alone |
| Error handling | Stable error categories, bounded retry only for transient errors, sanitized user messages | Execution contract/error mapping review | Adopt as review checklist |
| Remote PC | Reconnect/backfill, explicit approval, backend-specific support matrix | Optional remote-PC comparator only | Defer; not the no-PC core |
| Whole agent framework | Large integrated runtime / mobile app | None for current discovery stage | Do not import wholesale |

## Reuse rules before any code is copied

1. Record exact upstream repository, immutable commit/tag, file paths, root and file-level licenses, required notices, modifications, and dependency closure.
2. Prefer small libraries or a thin adapter over a wholesale framework. If a feature can be adopted as a documented invariant/test first, do that before introducing code.
3. Do not infer license compatibility from a repository badge alone. Check subdirectories, vendored binaries, transitive packages and generated assets; preserve attribution and notices.
4. Compare current upstream source with PocketCode's exact branch contract before porting. Never import an upstream state machine as if it were already compatible with PR #2/#3.
5. Add a deterministic regression test for each adopted behavior. A README claim or upstream green badge is not evidence that PocketCode satisfies it.
6. Do not introduce paid services, hosted dependencies, account setup, network calls, native build requirements, CI/Actions, or provider workload under this research pass.
7. No competitor source code has been copied in this audit. “Adopt” here means recording specific, traceable design/test patterns into PocketCode's existing work queue; implementation remains a separately approved step.

## Recommended next actions (ordered)

1. **Now:** use this audit to refine the existing cross-branch discrepancy list and fixed-task test protocol; do not edit PR #2/#3.
2. **Before contract freeze:** add test cases for timeout-with-process-still-running, wrapper failure vs child exit, unsupported capability, interrupted write/uncertain completion, partial diagnostic evidence, and reconnect/backfill if the remote path is retained.
3. **When execution location is chosen:** select only one candidate adapter/runtime, inspect its exact source/license/dependency graph, and run the canonical success/failure task in a fresh isolated workspace.
4. **At PC return:** verify the exact PR #2/#3 blobs and execute only the approved offline tests before considering any runtime integration.
5. **Decision gate:** if native evidence from a local app is already adequate and a portable report does not improve the next correction, narrow the product to the smallest useful evidence/continuity utility or stop the separate execution-product direction.

## Evidence boundary

This is a desk review of public repositories and their own documentation as retrieved on 2026-10-29. Feature statements are maintainer claims, not independent tests. No competitor was built or executed, no code was transplanted, and no PocketCode implementation/security/market claim is validated by this document.


## Cross-branch adversarial coverage map — 2026-10-29

**Method:** Static comparison of the proposed main contract/acceptance criteria, PR #2's pure report formatter/tests, and PR #3's pure lifecycle helper/tests and traceability document. This is source coverage, not test execution or proof of a working runtime. PR #2 and PR #3 were read-only in this pass.

### Revision anchors

- `main`: base commit `555840d8d83342513d9cd353d4d1522d46a5c82d`; `PRODUCT/EXECUTION_CONTRACT.md` blob `3861e51ae4f9e45a263b677402f26c41b240959d`; `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.
- PR #2: `chat-continuity-report-regressions-2026-10-26`, head `eb8b7ea83cb0e8fe1880351276c485b761431791`; `scripts/report_contract.py` blob `e9d944a722c2fac5279952696528da72a7011af3`; `scripts/test_report_contract.py` blob `39f3a3ef865ed55f333a1edc208096d99197d023`.
- PR #3: `pocketcode-pass0-audit-2026-10-26`, head `0ddcc0bc97bac5d446aefedf3d71f99411bd841d`; `scripts/lifecycle_contract.py` blob `ba8d4d0b217c90513bed020e298029ef4e16f164`; `scripts/test_lifecycle_contract.py` blob `39db87d9f44f5e8474f33cff60136e529364199a`; `AI_COLLAB/CONTRACT_CODE_TEST_TRACEABILITY_20261027.md` blob `a580ab54c20a9524f6822b81712a87eb62221212`.
- PR #2 and PR #3 remain open, draft, and unmerged at the heads above. The two contract documents have the same blob SHAs on main, PR #2, PR #3, and the research branch; they were not changed here.

### Seven-case matrix

| Prior-art case | Main contract / acceptance evidence | PR #2 report helper/tests | PR #3 lifecycle helper/tests | Static coverage judgement |
|---|---|---|---|---|
| 1. Client timeout while execution continues | Contract lines 21, 29–34, 72–78: client timeout/disconnect is not termination proof; timeout/cancel require trusted control evidence. Acceptance CASE-04/05/11 and LOOP-05. | `classify_verdict` returns INCOMPLETE for timeout/cancel/nonterminal states; tests `test_nonzero_exit_does_not_override_uncertain_lifecycle` and `test_timeout_cancel_rejection_and_infrastructure_failure_are_incomplete`. Formatter does not control or observe a running process. | `derive_disposition` requires confirmed termination for TIMED_OUT/CANCELLED; tests `test_timeout_unknown_termination_and_output_violation_never_pass` and event-order/contradiction cases. | **Covered as a rule/model; runtime enforcement missing.** No implementation test proves the process is actually stopped after timeout or that a client timer cannot mask continued execution. |
| 2. Wrapper/coordinator failure versus child-program exit | Contract distinguishes `program_failed` from `infrastructure_failed` (lifecycle list and PC-API-006), but does not explicitly define separate wrapper exit and child exit fields. | Formatter accepts caller-supplied status/exit evidence; no process/wrapper boundary. | Helper separates `execution_outcome` from derived `job_disposition`, but reviewed event vocabulary has exit/timeout/cancel/provider_error, not an explicit pair of wrapper status and child exit status. No matching test found in the reviewed test module. | **Missing explicit contract/test.** Define evidence ownership and mapping before an adapter exists; never infer the child exit from a wrapper failure. |
| 3. Requested capability unsupported | Contract PC-API-001 requires unsupported runtime rejection before provider dispatch; the request is allowlisted. It does not define per-backend capability discovery or unsupported-vs-unknown capability states. | No capability model; this is a formatter only. | Fingerprint/input validation and lifecycle gates do not constitute backend capability discovery; reviewed traceability says request validation/orchestration is not implemented in the helper. | **Partial / adapter gap.** The pre-dispatch rejection principle exists, but a capability matrix and fail-closed test for unsupported versus unknown are not evidenced. |
| 4. Interruption after side effect, before receipt | Contract idempotency/retry section (lines 65–70) prohibits duplicate runs for a key and changed-body reuse; acceptance CASE-13 addresses ambiguous network retry. It does not say to inspect side-effect state before retrying a partially completed operation. | No side-effect/recovery logic; formatter only. | Idempotency fingerprint/reservation, report history and tombstone models exist; tests cover same-key replay/conflict and report-version append. Traceability explicitly says storage/history models are in-memory and production needs atomic persistence. No test found for interruption after an external side effect but before its receipt. | **Partial; recovery gap remains.** Idempotency is useful but is not proof of exactly-once side effects or safe recovery after a lost receipt. Inspect/reconcile current state before retrying uncertain operations. |
| 5. Partial/missing diagnostic evidence | Contract lines 58–63, 106–108, 166–181 require bounded output, truncation and explicit unknown/missing fields; acceptance LOOP-07 and CASE-03/06/12. | Tests distinguish empty from unavailable stdout/stderr, missing exit/duration, truncation, malformed entries and report-size truncation. See `test_missing_values_and_empty_output_are_distinct`, `test_actual_output_truncation_is_reported_without_source_flag`, `test_malformed_entries_are_disclosed`, `test_report_cap_preserves_header_and_uncertainty_footer`. | OutputBudget accounts/limits retained bytes and redactor tests cover configured patterns; traceability says this is an accounting model, not real pipe-drain/collection. No explicit evidence found that a failed diagnostic collector is represented separately from an empty stream. | **Report formatting covered; collection provenance partial.** Preserve the distinction between empty, unavailable, truncated and collection-failed. Tests on supplied values do not prove the runtime collected all available diagnostics. |
| 6. Reconnect/backfill after event gap (remote path only) | Contract line 34 and PC-API-013 require authoritative state recovery after reconnect; acceptance CASE-11 says recover server state after disconnect. Neither specifies replay/backfill of missed events or how an unrecoverable event gap is disclosed. | No reconnect/event transport implementation. | `reduce_terminal_events` deterministically reduces supplied events and flags conflicting terminal evidence; tests cover duplicate/conflicting/out-of-order events. It is not a reconnect transport or durable event store; traceability explicitly notes no durable append-only event store. | **Partial and remote-only.** State recovery is a requirement; event backfill/gap disclosure is not specified or implemented. Keep this case conditional if no remote/event-stream path is selected. |
| 7. Stale edit/file revision | Contract binds idempotency keys to request bodies (lines 67–70), but does not require compare-and-swap or stale-file rejection for an edit based on an older file version. | No file-write or revision guard. | `canonical_request_fingerprint` binds canonical source, inputs and effective policy; `test_fingerprint_binds_source_policy_and_canonical_inputs` checks changed source/policy produce a different fingerprint. This protects idempotency-key reuse, not overwriting a file that changed after the read. | **Partial adjacent protection; stale-write test missing.** Add revision/digest precondition at the future write boundary if edits are supported; do not treat request fingerprinting as a stale-edit guard. |

### Consequence / smallest next action

1. Keep the current canonical contract as the only report-schema candidate. Do not add a parallel receipt schema.
2. Prioritize three genuinely missing cross-boundary expectations for the next spec/test-design pass: (a) wrapper versus child exit provenance, (b) interruption after side effect with inspect-before-retry recovery, and (c) stale-revision rejection at a write boundary. Capability discovery/fail-closed behavior and diagnostic-collector failure disclosure are also adapter/integration gaps.
3. Treat timeout termination, event replay, idempotency and diagnostic handling as **modeled or specified**, not verified runtime behavior. If remote execution is not selected, keep reconnect/backfill conditional rather than adding remote infrastructure by assumption.
4. Before proposing contract edits, map these cases to the existing cross-branch audit and PR #3 traceability table, resolve the two-axis execution-outcome/job-disposition projection, and keep any new tests synthetic/offline until an implementation is explicitly authorized.
5. No tests were run in this pass; no code or canonical contract was changed; no provider, app, workflow, or runtime was executed. The seven-case coverage labels above are static-review conclusions only.


## Minimal non-duplicative test proposals — 2026-10-29

These are **design proposals only**. Do not edit PR #2/#3 or the canonical contract as part of this pass. Before implementing tests, re-fetch the source refs and check whether a later commit already covers the case.

| Proposed case ID | Existing related coverage | Smallest missing assertion | Best home if separately authorized |
|---|---|---|---|
| REUSE-WRAP-01 — wrapper versus child result | Main contract already distinguishes `program_failed` and `infrastructure_failed`; PR #2 formats trusted supplied status; PR #3 has one execution outcome plus derived disposition. | Given child exit 0 plus wrapper/collector failure, preserve both observations and prohibit a false complete-success verdict. Given wrapper exit 0 plus child exit nonzero, verdict must reflect the child failure. Missing child exit must remain unknown, not be inferred from wrapper exit. | First add a case to the existing offline acceptance matrix / lifecycle contract crosswalk; only add helper tests if the selected model can represent both sources without inventing a schema. |
| REUSE-RECOVERY-01 — side effect completed, receipt lost | Existing IDEM-01/02, idempotency reservation tests, report history and LC-06 cover key reuse or cleanup/report recovery, not a lost receipt after an external side effect. | Simulate: action's side effect is committed; response/receipt is dropped; coordinator restarts. Recovery must inspect authoritative operation state and return/reconcile the existing outcome; it must not repeat the side effect solely because the receipt is absent. If state cannot be inspected, remain UNKNOWN/INCOMPLETE and request reconciliation. | Offline acceptance matrix and future adapter contract; fake adapter only. Do not claim exactly-once external effects from in-memory idempotency helpers. |
| REUSE-STALE-01 — stale write precondition | PR #3 fingerprint tests prove changed source/policy changes a request fingerprint. No reviewed case proves compare-and-swap on a file/workspace edit. | Read revision R1; another actor commits R2; write based on R1 must be rejected with a stale-revision conflict and must leave R2 unchanged. Matching revision permits the write. Test content/digest and no-mutation on conflict. | File/workspace write contract and future write-adapter tests, only if PocketCode chooses to support edit/write operations. Do not put this into the execution-report schema. |
| REUSE-CAP-01 — unsupported versus unknown capability | Existing CAP-01/CAP-02 already say unsupported/unverified capabilities stop before execution and configuration mismatch requires recheck/reject. | Reuse these IDs; clarify expected outcomes for capability known unsupported, capability unknown/unavailable, and evidence bound to stale plan/config. In every case assert zero adapter start calls. | Extend existing CAP-01/CAP-02 fixtures rather than create duplicate IDs. |
| REUSE-DIAG-01 — collector failure provenance | PR #2 formatter tests distinguish empty and unavailable supplied fields; PR #3 OutputBudget tests retention limits, not actual collection. | Distinguish (a) successfully collected empty stream, (b) stream unavailable from adapter, (c) collection failed partway, and (d) stream truncated by policy. Preserve collected prefix and explicit reason without inventing bytes/exit status. | Extend existing PR #2 formatter tests only after mapping its current field vocabulary; keep collection failure source in the future adapter evidence, not as a fabricated formatter inference. |

### Merge discipline and decision

- Reuse existing `CAP-01/CAP-02`, `IDEM-01/02`, `LC-01..LC-15`, `REPORT-01/02`, `STREAM-01`, and `ARTIFACT-02` IDs where semantics match; avoid a second parallel test catalogue.
- `REUSE-WRAP-01`, `REUSE-RECOVERY-01`, and `REUSE-STALE-01` are the three clearest genuinely new cross-boundary expectations. `REUSE-DIAG-01` is a refinement of existing diagnostic/report cases. Capability handling is primarily a coverage clarification of existing CAP cases.
- Keep every case synthetic/offline until the relevant implementation and exact test environment are authorized. A fake adapter proves only the modeled decision/call ordering, not provider behavior, process termination, durable atomicity, or security isolation.
- Do not change the canonical report schema merely to store these tests. Any need for separate wrapper/child observations should be reconciled against the existing three-layer model (execution outcome, cleanup/evidence gates, derived disposition) before proposing field names.


## Correction after checking the existing offline matrix — 2026-10-29

A deeper reread of the exact PR #3 matrix shows that the previous section's shorthand "missing coverage" needs more precise labels. Several neighboring requirements already exist as proposed synthetic cases. Do not duplicate them or describe a design case as implemented/verified.

| Topic | Existing exact coverage in PR #3 matrix / contract | Corrected gap statement |
|---|---|---|
| Unsupported capabilities | `AI_COLLAB/OFFLINE_ACCEPTANCE_TEST_MATRIX.md` cases `CAP-01` and `CAP-02`; `AI_COLLAB/DRAFT_EXECUTION_CONTRACT.md` adapter contract explicitly distinguishes supported, unsupported, not_verified and blocked_by_plan. | **Specified already.** The gap is execution of the exact checked-in tests (NOT RUN) and eventual adapter evidence that enforces zero start calls; do not add duplicate CAP IDs. |
| Cleanup recovery/report history | Matrix `LIFE-04`, `LC-06`, `LIFE-SEM-02`; lifecycle helper test `test_cleanup_reconciliation_appends_new_report_version_without_rewriting_history`. | **Cleanup recovery specified/modelled.** This does not cover a distinct external side effect that committed before its operation receipt was lost. Only the latter is a candidate new case. |
| Idempotency and interrupted request replay | Matrix `IDEM-01/02`, `IDEM-SEM-01..04`; helper tests cover same-key replay/conflict and a serial-order batch model. | **Request deduplication specified/modelled.** Not proof of durable atomicity, and not proof that retrying an uncertain external side effect is safe. The receipt-loss scenario should explicitly test inspect/reconcile-before-retry, not duplicate basic idempotency tests. |
| Artifact interruption/digest mismatch | Matrix `ARTIFACT-02` and `ART-SEM-01`; artifact release gate tests. | **Artifact write integrity specified/modelled.** It is not the same as stale-source revision protection for a future workspace edit. |
| Output/diagnostic limits | Matrix `OUT-01/02`, `STREAM-01`, `STREAM-SEM-01..03`, `REDACT-01/02`; PR #2 tests distinguish empty/unavailable fields and report truncation. | **Output budget/report presentation substantially specified/modelled.** A separate adapter-level collection-failure provenance case remains a refinement; don't call generic diagnostics wholly missing. |
| Timeout/cancel and process tree | Matrix `LIFE-01/03`, `LC-03`, `RACE-SEM-01/03/04`, `PROC-TREE-01`. | **Synthetic lifecycle rules specified.** They do not prove real OS/provider termination. |
| Wrapper exit versus child exit | Main contract names program vs infrastructure failure; PR #2 formatter accepts a single lifecycle status and optional exit code; PR #3 outcome model records an execution outcome. No reviewed test explicitly models both child exit and wrapper/collector exit as separate evidence. | **Candidate new contract/test gap**, if a concrete adapter actually has both process layers. Preserve separate provenance; do not invent child status from wrapper status. |
| Stale file revision | Request fingerprints bind source/policy/input identity; no reviewed case models read revision R1, concurrent update to R2, then attempted write based on R1. | **Conditional future write-boundary gap.** The current first proof excludes a persistent project workspace, so this is not a reason to expand the current MVP or canonical execution report. Add only if workspace/file editing is selected. |

### Revised smallest-next-step recommendation

1. Do not add another capability, generic idempotency, cleanup-recovery, artifact-integrity, or output-cap test: the matrix already contains those semantics.
2. If one new synthetic case is approved, prioritize **receipt lost after an external side effect** because it tests a failure mode not equivalent to same-key request replay: side effect commits, receipt disappears, recovery queries authoritative state, and only repeats when safely proven not committed. If state cannot be queried, remain UNKNOWN/INCOMPLETE.
3. Add **wrapper-versus-child provenance** only once the intended adapter boundary is concrete enough to say which wrapper exists and which exit codes it owns.
4. Defer **stale-revision compare-and-swap** unless file/workspace writes enter the chosen MVP; it is adjacent to, not part of, the current stateless execution contract.
5. For diagnostic collection failure, extend an existing report/output case only after defining the adapter evidence shape. No schema field is approved by this note.
6. The exact PR #3 helper/test files and PR #2 formatter/test files remain **NOT RUN** in this environment. No test or runtime claim is upgraded by this static reread.


## Scope correction — receipt-loss recovery is not a current MVP test gap

Cross-checking the canonical [execution contract](../PRODUCT/EXECUTION_CONTRACT.md) and [acceptance plan](../PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md) changes the immediate recommendation:

- The first proof explicitly excludes a persistent project workspace, arbitrary networking, and broad agent orchestration. A generic external side effect with an independently lost operation receipt is therefore **outside the currently selected proof boundary**, unless the concrete execution adapter introduces such an operation.
- Existing acceptance case `CASE-13` already addresses retry after an ambiguous network response: idempotency must prevent accidental duplicate execution where supported, and unknown execution state stays unknown. That is the right current run-level recovery baseline; do not add a parallel generic “lost receipt” case without specifying a distinct operation boundary.
- The proposed `REUSE-RECOVERY-01` should be treated as a **conditional future case**, not one of the immediate MVP gaps. Activate it only if a selected design includes multi-step orchestration or external side effects whose commit can be separated from recording/receiving their operation receipt. Then name the exact side effect, authoritative inspection API, idempotency key/operation identity, and recovery behavior.
- For the current stateless execution proof, the next safe work is a traceability clarification: link `CASE-13` to the existing idempotency contract and verify its assertions cover “same key after response loss returns the same run reference / queries authoritative state; never launches a second run; if state cannot be established, stays INCOMPLETE.” This is a **proposed assertion-strengthening recommendation**, not a claim that the checked-in implementation/test already satisfies it. Any change to canonical contract/tests still needs explicit implementation authorization.

Thus the immediate decision is **REUSE existing CASE-13 and DEFER external side-effect receipt-loss testing**. Wrapper-versus-child provenance also remains conditional on a concrete adapter with separate process layers; stale-revision CAS remains out of scope unless workspace writes are selected.


## CASE-13 traceability result — reuse existing acceptance ID; expose a mapping gap

Static review of the exact checked-in sources confirms that CASE-13 already states the right high-level invariant, but the lower-level mapping is incomplete:

- Canonical acceptance source: `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`, CASE-13 at line 64: retry after ambiguous network response; prevent duplicate execution where supported; unknown execution state stays unknown.
- Canonical execution contract: `PRODUCT/EXECUTION_CONTRACT.md`, blob `3861e51ae4f9e45a263b677402f26c41b240959d`, idempotency/retries section requires same user/key not to create multiple billable runs, changed body to conflict, unknown provider result not to become success, and explicit retry policy.
- PR #3 offline matrix: blob `3a9b214a9ccde9f3abad8dba2d7f14d6c97632ad`, contains IDEM-01/02 and IDEM-SEM-01..04 for key/fingerprint/tenant replay, but no explicit CASE-13 cross-reference or dedicated ambiguous-response assertion was found in the reviewed matrix.
- PR #3 helper/test pair: `scripts/lifecycle_contract.py` blob `ba8d4d0b217c90513bed020e298029ef4e16f164`; `scripts/test_lifecycle_contract.py` blob `39db87d9f44f5e8474f33cff60136e529364199a`. `reserve_idempotency` stores `(tenant, key) -> (fingerprint, job_id)` and returns the existing job ID for matching replay; the tests verify replay/conflict/tenant scope and a deterministic serial-order batch model. This is not a durable job-state lookup, receipt recovery protocol, or real concurrency primitive.
- PR #2 report formatter/test pair only formats supplied result metadata; it does not implement run lookup or idempotent dispatch.

**Result:** no reason to add a new acceptance ID. There is a real **traceability/semantic precision gap** between the high-level CASE-13 and the helper's key reservation tests: same-key replay returning an old job ID is necessary but does not by itself prove that the UI/API can recover authoritative current state after the original response is lost.

**Minimal recommended disposition:** retain CASE-13 and IDEM IDs. In the existing traceability/checklist when implementation work is authorized, map CASE-13 to (a) tenant-scoped same-key/same-fingerprint replay, (b) authoritative lookup of the existing run, (c) no second dispatch, and (d) INCOMPLETE when current terminal state cannot be established. A synthetic fake-adapter test can assert call order and zero additional dispatches; durable storage, atomicity, and real provider recovery remain separate implementation-level evidence. This note does not edit the protected PR #2/#3 branches and does not claim the exact tests were run.


## CASE-13 matrix-to-traceability crosswalk verification — 2026-10-29

A second static pass checked the acceptance matrix and the existing contract-to-code-to-test traceability document together, rather than relying only on the earlier audit summary.

- **Canonical acceptance:** `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` remains the only existing acceptance ID needed: CASE-13 covers retry after an ambiguous network response.
- **Matrix:** `AI_COLLAB/OFFLINE_ACCEPTANCE_TEST_MATRIX.md` has IDEM-01/02 and IDEM-SEM-01..04. These specify tenant/key/fingerprint replay, conflict, tenant separation, and an atomic reservation requirement. The matrix does not explicitly map those rows to CASE-13 or separately state response-loss recovery / authoritative current-run lookup.
- **Traceability:** `AI_COLLAB/CONTRACT_CODE_TEST_TRACEABILITY_20261027.md` maps generic same-tenant/key/fingerprint replay to `reserve_idempotency` and the existing replay/conflict/tenant-scope and serial-order batch tests. It does not contain a CASE-13-specific row. Its own caveat correctly says the batch model is not concurrency and production requires an atomic transaction/unique constraint.
- **Helper and tests:** exact checked-in helper/test blobs remain `ba8d4d0b217c90513bed020e298029ef4e16f164` and `39db87d9f44f5e8474f33cff60136e529364199a`. The helper returns the prior job ID for matching key/fingerprint; it does not query an authoritative current run state or model a lost response at an API/adapter boundary.
- **PR #2 report layer:** `report_contract.py` / `test_report_contract.py` classify and format caller-supplied metadata, including INCOMPLETE for missing/nonterminal evidence. They do not provide durable run lookup, dispatch deduplication, or retry recovery.

**Disposition:** the previous finding is confirmed and sharpened: the gap is not absence of generic idempotency tests; it is the missing explicit traceability bridge from CASE-13 to the existing idempotency rows plus the unmodeled response-loss/recovery boundary. When implementation work is authorized, reuse CASE-13 and existing IDEM IDs, and strengthen the mapping with four assertions: (1) same tenant/key/fingerprint resolves to the original run reference, (2) retry/reconnect obtains authoritative current state for that run, (3) no second dispatch occurs, and (4) if state cannot be established, the report remains INCOMPLETE/unknown. A fake adapter can test call ordering and zero extra dispatches; durable persistence, atomicity, and provider recovery need separate evidence.

**No implementation or test run occurred.** This is repository-source traceability only. No code, matrix, traceability file, PR #2, or PR #3 was changed by this addendum; no provider, Actions, deployment, merge, or spend.


## MVP-scope-aware priority reconciliation — 2026-10-29

The seven-case map identifies gaps, but “missing” alone is not a reason to add MVP scope. Re-ranking against the current provider-neutral first-proof boundary gives this order:

| Priority for the next design pass | Case / concern | Why it belongs here | Safe next step |
|---|---|---|---|
| **P1 — cross-path correctness** | Wrapper/coordinator failure vs child-program exit (REUSE-WRAP-01) | Any adapter may have a wrapper or collector distinct from user code. Confusing their exit facts can create a false run result. The current helper's one execution_outcome does not represent both facts. | Define evidence ownership and a minimal synthetic truth table before choosing fields. Keep separate observations; missing child exit remains unknown. |
| **P1 — core report truthfulness** | Diagnostic collection failure (REUSE-DIAG-01) | The core promise depends on truthful stdout/stderr and errors. Empty, unavailable, partially collected, and policy-truncated are different facts. Current formatter tests cover some supplied-value distinctions, but do not prove actual collection provenance. | Extend existing report semantics only after confirming the current field vocabulary can express the distinctions; do not fabricate bytes or exit status. |
| **P2 — path-dependent** | Capability known unsupported vs capability unknown (CAP-01/CAP-02) | The fail-closed principle is already specified. The concrete discovery/verification mechanism depends on whether the chosen path is local phone, browser/WASM, remote PC, or hosted. | Reuse CAP-01/CAP-02; require zero start calls for unsupported, unknown/unavailable, or stale-plan evidence when a concrete adapter is selected. |
| **P2 — remote-only** | Exact policy revision applied before task start (NET-BARRIER-01/NET-SEM-01) and reconnect/event-gap recovery | These require a coordinator/provider policy barrier or remote event transport. They are critical if that path is selected, but must not be projected onto local/browser paths without a matching control boundary. | Keep as explicit selection gates for remote/hosted candidates; do not claim the pure boolean helper proves policy identity or chronology. |
| **Deferred unless scope changes** | Lost external side-effect receipt (REUSE-RECOVERY-01) | Current first proof excludes broad orchestration and arbitrary network access; CASE-13 already covers run-level ambiguous-response retry. A separate case needs a concrete external side-effect boundary. | Do not add it to the immediate MVP matrix unless an operation can commit separately from its receipt. |
| **Deferred unless scope changes** | Stale workspace/file revision (REUSE-STALE-01) | Current first proof is a stateless run/inspect/report loop, not collaborative file editing or workspace writes. Request fingerprinting is not compare-and-swap. | Add a write-precondition contract only if editing/writing a persistent workspace enters scope. |

**Important adjacent invariant:** regardless of the FAILED-versus-INCOMPLETE projection for a nonzero exit, artifact release is a separate gate and must remain denied unless cleanup, integrity, job association, and authorization are all confirmed. The reviewed PR #3 pure helper has an explicit artifact_release_allowed function with those checks; that is model coverage, not proof of a real artifact store or quarantine boundary.

**Disposition:** next spec-only work should clarify wrapper/child provenance and diagnostic-collection provenance, while preserving the unresolved two-axis decision (execution observation vs job disposition). Do not change the canonical contract, test matrix, PR #2, or PR #3 without explicit implementation authorization. This ranking is a proposal based on the current product scope, not an owner-approved decision; no tests were run.
