# PocketCode Execution Contract — Cross-Branch Consistency Audit

**Checked:** 2026-10-28  
**Status:** Static source/document review only. No code was changed in PR #2 or PR #3. No tests were run by this audit.  
**Purpose:** Preserve a coherent product/report vocabulary across main, the report formatter in PR #2, and the lifecycle model in PR #3 before anyone proposes implementation or an API freeze.

## 1. Exact sources inspected

| Source | Branch/ref | Exact file/blob SHA |
|---|---|---|
| Product acceptance and verdict semantics | main — PRODUCT_SPEC.md | f1e4149c15df55e338829170ed6bcb6cb70d7d28 |
| Security launch requirements | main — SECURITY.md | e4009c48bd474b1106e253ea25f1f2fb769f3d7a |
| Existing proposed execution contract | main — PRODUCT/EXECUTION_CONTRACT.md | 3861e51ae4f9e45a263b677402f26c41b240959d |
| PR #2 report formatter | chat-continuity-report-regressions-2026-10-26 — scripts/report_contract.py | e9d944a722c2fac5279952696528da72a7011af3 |
| PR #2 formatter tests | same branch — scripts/test_report_contract.py | 39f3a3ef865ed55f333a1edc208096d99197d023 |
| PR #3 draft lifecycle contract | pocketcode-pass0-audit-2026-10-26 — AI_COLLAB/DRAFT_EXECUTION_CONTRACT.md | 02ad9934cc40c84f7e8cd7f6c982d5d8ed7d1b70 |
| PR #3 pure lifecycle helper | same branch — scripts/lifecycle_contract.py | ba8d4d0b217c90513bed020e298029ef4e16f164 |
| PR #3 lifecycle test source | same branch — scripts/test_lifecycle_contract.py | 39db87d9f44f5e8474f33cff60136e529364199a |
| PR #3 contract-to-code-to-test crosswalk | same branch — AI_COLLAB/CONTRACT_CODE_TEST_TRACEABILITY_20261027.md | a580ab54c20a9524f6822b81712a87eb62221212 |
| PR #3 offline acceptance matrix | same branch — AI_COLLAB/OFFLINE_ACCEPTANCE_TEST_MATRIX.md | 3a9b214a9ccde9f3abad8dba2d7f14d6c97632ad |
| PR #3 selected lifecycle decisions | same branch — AI_COLLAB/PASS1_OWNER_DECISION_PACKET_20261027.md | d0d59465a4eed1b394aabeacf33b9f5988e4544f |

The SHA values make this audit reproducible. Re-fetch each exact ref/blob before relying on it in a later session.

## 2. Findings

### F1 — The main product direction and safety principles are aligned

The main product specification and security requirements call for real execution evidence, server-enforced limits, isolation, access control, cleanup, and honest reporting. PR #2's formatter and PR #3's draft lifecycle model both reject unsupported success claims and distinguish an observed program result from unconfirmed execution or infrastructure behavior.

**Disposition:** No product-direction contradiction found in the inspected rules.

### F2 — Three status layers must not collapse into one field

The current sources expose different levels of status:

| Layer | Main / PR #2 vocabulary | PR #3 draft vocabulary | Meaning |
|---|---|---|---|
| Execution lifecycle/observation | accepted, queued, running, succeeded, program_failed, timed_out, cancelled, rejected, infrastructure_failed; formatter accepts trusted status and optional exit evidence | execution_outcome: NOT_STARTED, EXIT_ZERO, EXIT_NONZERO, TIMED_OUT, CANCELLED, LIMIT_EXCEEDED, UNKNOWN | What can be established about request execution |
| Cleanup and evidence gates | Main contract requires cleanup, bounded output, and truthful missing evidence, but has no separate cleanup-state field frozen | cleanup_state: PENDING, CONFIRMED, FAILED, UNKNOWN; explicit policy, termination, artifact, and tenant/job gates | Whether the result/artifacts are safe and sufficiently evidenced |
| Derived job disposition / user-facing verdict | PR #2 formats PASS, FAIL, or INCOMPLETE | job_disposition: REJECTED, PASS, FAILED, TIMED_OUT, CANCELLED, LIMIT_EXCEEDED, INCOMPLETE, PROVIDER_ERROR | Whether the overall request can be described as a pass/failure/incomplete result |

This is primarily a **contract projection gap**, not proof that the approaches are inherently inconsistent. The newer model intentionally preserves a valid process exit as an observation even when cleanup or required evidence blocks overall PASS. That is more informative than flattening everything to one terminal state.

**Recommended next contract action (not an approved schema):** define one versioned projection from PR #3's detailed outcome/cleanup/disposition record to the simpler user-facing verdict. A conservative candidate is:

| Detailed job disposition (PR #3 draft) | Candidate user-facing verdict | Required explanation / preserved detail |
|---|---|---|
| PASS | PASS | Only after every mandatory policy, termination, artifact, tenant/job, output-limit, and cleanup gate is confirmed; show the exact execution evidence. |
| FAILED | FAIL | Use only for a confirmed program/process failure represented by the detailed contract; preserve exit code and relevant error evidence when available. |
| REJECTED | INCOMPLETE | Say the task did not start/was rejected; do not imply a program failure or success. |
| TIMED_OUT | INCOMPLETE | Show timeout and whether termination was confirmed; do not claim the process stopped if evidence is missing. |
| CANCELLED | INCOMPLETE | Show cancellation and termination evidence separately; never render it as successful execution. |
| LIMIT_EXCEEDED | OPEN under D-01: candidate FAIL for trusted limit-caused runtime failure; INCOMPLETE for unknown/contradictory terminal outcome. Collection-only caps derive from trusted terminal facts and case-specific output requirements. | Preserve exact limit and truncation/discard evidence; never represent partial output as complete. |
| PROVIDER_ERROR | INCOMPLETE | State that execution/service outcome is unconfirmed; do not invent an exit code or program result. |
| INCOMPLETE | INCOMPLETE | Preserve missing/contradictory evidence, cleanup state, and the next required reconciliation step. |

Example: `execution_outcome=EXIT_ZERO` plus `cleanup_state=UNKNOWN` must preserve the observed zero exit as a fact but render the overall verdict as **INCOMPLETE**, not PASS. The summary must not hide the cleanup blocker. A confirmed nonzero program exit may render FAIL while retaining the exact exit/error evidence. The final field names, reason codes, and display text remain open and need owner/reviewer approval before a schema is frozen.

### F3 — PR #3 adds mandatory policy-revision evidence that main does not yet spell out

Main says outbound networking is disabled by default and must be enforceable outside the untrusted process. PR #3 requires confirmation that the exact mandatory policy revision has actually been applied to the intended execution boundary **before code starts**; pending, missing, failed, stale, or mismatched evidence must fail closed. An acknowledgement or ETag alone is explicitly insufficient.

**Disposition:** Treat this as a safety refinement that must be reconciled into the authoritative contract before a provider implementation. Do not claim this runtime guarantee is implemented or verified. No live policy enforcement was tested.

### F4 — Output/artifact behavior is more specific in PR #3, but the numeric values are test-only defaults

Main requires bounded inputs/outputs and says truncation must be explicit. PR #3 models per-stream and aggregate byte budgets, termination/drain behavior, artifact-manifest integrity, tenant/job authorization, quarantine while cleanup is uncertain, and append-only report versions after later reconciliation.

The current PR #3 helper has provisional offline-test values of 32 KiB retained stdout, 32 KiB retained stderr, 64 KiB aggregate retained output, and a separate 1-second drain/discard budget. These values are not validated production settings, cost guarantees, or a selected execution-provider configuration. Main's exact limits remain open.

**Disposition:** Preserve the semantic safety gates; keep numeric limits, storage policy, and exact output/API schema open pending an explicit, evidence-backed design decision.

### F5 — Idempotency and report history need a boundary between test defaults and production policy

Main already says same-key/same-request should not create duplicate runs and same-key/different-request must conflict. PR #3 refines this with a tenant-scoped, server-computed canonical fingerprint, append-only lifecycle evidence, immutable report versions, and a 30-day post-deletion tombstone in the pure helper.

The 30-day tombstone is described in the PR #3 research as a provisional offline-test policy. Main's actual retention/deletion policy remains unresolved.

**Disposition:** Keep the selected semantics scoped to the PR #3 provider-neutral offline baseline. Do not promote 30 days, exact schema names, or storage behavior to production policy without further approval and review.

### F6 — Current test evidence is branch-specific and must remain separate

- **PR #2:** its PR description records 25 Python tests passing on 2026-10-26 in a temporary reconstruction from the exact checked-in branch blobs using Python 3.13.5/Linux. Scope was the pure report helper and prototype source checker. This does not establish execution-backend, mobile-browser, isolation, cleanup, provider, or billing behavior.
- **PR #3:** the test source currently contains 24 synthetic test methods, but the PR description explicitly states that the exact checked-in helper/test pair and full repository suite were **NOT RUN**. Method count is not a test result.
- **Main:** no evidence inspected here establishes a production execution backend or a real user-code run.
- **AI Workflow Director:** its separate AWD-01–AWD-16 fixtures are design-only and NOT RUN.

**Disposition:** Never transfer test results between branches or infer that a helper was integrated because another branch has related code. Before later test execution, verify the exact fetched file blob SHAs and record the actual command, interpreter, exit code, counts, output, and limitations.

## 3. Combined contract rules safe to preserve

These principles are consistent across the inspected sources and should remain invariants during future implementation review:

1. Client-provided statuses and text printed by user code are not execution evidence.
2. A successful process exit is an observation, not sufficient evidence that the complete job succeeded.
3. Overall PASS requires all required evidence/policy/termination/artifact/tenant/cleanup gates to be confirmed.
4. Contradictory, missing, malformed, or stale mandatory evidence cannot produce PASS.
5. Timeout, cancellation, output-limit breach, and infrastructure uncertainty are distinguishable; cleanup uncertainty is preserved separately.
6. Mandatory execution policy must be confirmed on the exact intended boundary before user code starts.
7. Output is bounded; truncation/limit breach is explicit; raw data and artifacts remain unavailable when the applicable release gates are not met.
8. Provider-confirmed behavior, configured behavior, documentation claims, and actual test observations are different evidence classes.
9. Offline fake-adapter tests can validate pure decision logic; they cannot prove provider isolation, egress, cleanup, tenant separation, or cost.
10. No provider is selected and no live workload is authorized under the strict $0 gate.

## 4. Unresolved contract items (do not guess)

- Exact public/versioned request and response schema; which fields are source observations vs derived projection.
- Mapping from detailed disposition to user-facing PASS/FAIL/INCOMPLETE without losing reason or cleanup state.
- Exact runtime/request/input-file scope and supported artifact types.
- Production output/time/CPU/memory/process/storage caps and how they are enforced.
- Authentication, tenant and job authorization in a real deployment.
- What provider-side evidence proves applied policy, termination, cleanup, and artifact integrity for the intended job.
- Actual retention/deletion behavior for reports, artifacts, and idempotency data.
- Any provider plan, account, price, or sustainable $0 ceiling.

## 5. Safe next action

1. Use this audit as a review companion; do not edit PR #2/#3 or declare their work integrated.
2. In the next pass, update the existing evidence/competitor research with the current mobile coding landscape and then prepare a compact product hypothesis card.
3. Before any integration, conduct a scoped contract review with the relevant owner/AI reviewers and reconcile proposed changes into the authoritative docs through an explicitly authorized branch/PR workflow.
4. Keep provider tests blocked until the owner authorizes the exact test, cost path, source data, safety plan, and prerequisites.

**Audit limits:** read-only static document/source inspection; no executable test was run, no live provider or browser workload was performed, and no security guarantee was verified.

## Follow-up proposal: trusted verdict projection (2026-10-28)

**Status:** Review proposal only. This section does not approve a schema, change main/PR #2/PR #3, or establish that any gate is implemented.

The integration question is not whether the pure report formatter can map a status and exit code to a verdict. It can. The question is which trusted component has already established all mandatory job-level gates before that formatter is allowed to display PASS.

| Gate / fact | Required evidence before overall PASS | Trusted owner boundary (proposed) | If missing, false, stale, or contradictory |
|---|---|---|---|
| Request accepted and authorized | Server-side authenticated principal, validated request and policy decision tied to this job/attempt | API/coordinator, not client fields | Reject before execution or INCOMPLETE if discovered after allocation |
| Exact mandatory execution policy applied before start | Authoritative provider/boundary evidence identifies the required policy revision and confirms it was applied before process start; request acknowledgement/ETag alone is insufficient | Coordinator verifies provider/boundary evidence before releasing start | Do not start if not confirmed; otherwise INCOMPLETE/provider error, never PASS |
| Execution outcome and exit | Attempt-bound terminal event from authoritative runner/provider, with exit code and event association | Execution adapter/coordinator | INCOMPLETE if absent or ambiguous; confirmed nonzero program exit can be FAIL |
| Termination | Authoritative terminal/termination evidence appropriate to the outcome | Adapter/coordinator | Timeout/cancel cannot be described as stopped if termination is unconfirmed; overall result remains incomplete |
| Output limits and truncation | Trusted byte counts, limit outcome, and explicit truncation/discard metadata | Adapter/coordinator; formatter only renders supplied evidence | Limit breach is not PASS; disclose discarded/truncated evidence |
| Artifact manifest and integrity | Manifest bound to the job/attempt, validated names, sizes and hashes, with no path escape | Artifact gate/service | Do not release artifacts; overall PASS blocked |
| Tenant/job authorization | Server-side ownership check on each artifact/report reference | API/artifact service | Deny access; never trust a client-supplied tenant/job claim |
| Cleanup | Authoritative cleanup confirmation for the relevant boundary and attempt | Cleanup controller/coordinator | INCOMPLETE; preserve zero exit as an observation but do not elevate overall verdict |
| Derived disposition | Versioned, deterministic projection from the above immutable observations and policy decisions | Coordinator/domain layer; formatter must not recompute missing security facts | INCOMPLETE or PROVIDER_ERROR where evidence is absent or contradictory |
| Human/AI report | Bounded, redacted report containing the derived disposition plus provenance, uncertainty and visible blockers | Pure formatter, given an already-derived trusted report model | Never upgrade status; never imply a simulated example is real |

### Conservative display mapping to validate

| Trusted detailed disposition | Candidate simple verdict | Required retained detail |
|---|---|---|
| PASS | PASS | All mandatory gates confirmed; show provenance and applicable policy/termination/artifact/cleanup evidence |
| Confirmed program failure (FAILED, or main's confirmed program_failed) | FAIL | Exact exit/error evidence; do not claim infrastructure or policy failure without evidence |
| REJECTED | INCOMPLETE | State that execution did not start and provide the rejection reason where safe |
| TIMED_OUT / CANCELLED | INCOMPLETE | Preserve outcome and whether termination was confirmed |
| LIMIT_EXCEEDED | OPEN under D-01: candidate FAIL for trusted limit-caused runtime failure; INCOMPLETE for unknown/contradictory terminal outcome. Collection-only caps follow terminal facts and case-specific collection rules. | Name the limit and expose truncation/discard status without inventing execution failure. |
| PROVIDER_ERROR / UNKNOWN / INCOMPLETE | INCOMPLETE | State what is unknown, what evidence conflicts or is missing, and the next reconciliation step |

This projection is intentionally conservative and needs owner/reviewer review. In particular, the final mapping for a confirmed nonzero exit when cleanup later fails must be specified carefully: the report may preserve the observed process failure while still withholding artifacts and separately showing that cleanup/security completion is unconfirmed. Do not flatten those facts into an invented single cause.

### Acceptance checks for a future implementation (not run)

1. EXIT_ZERO + confirmed policy + confirmed termination + valid artifact/authorization gates + cleanup_state=CONFIRMED may derive PASS.
2. EXIT_ZERO + cleanup_state=UNKNOWN derives INCOMPLETE, not PASS.
3. EXIT_ZERO + missing/stale/mismatched mandatory policy revision never starts user code; if discovered retrospectively, no PASS is issued.
4. A client-supplied PASS, exit code, artifact manifest or policy acknowledgement cannot satisfy a trusted gate.
5. EXIT_NONZERO preserves the process failure observation and cannot become PASS, even if program output prints “success”.
6. Timeout/cancellation with unconfirmed termination does not claim the process stopped.
7. Limit overflow, missing manifest, wrong tenant/job association, hash mismatch or cleanup failure blocks artifact release and overall PASS.
8. Later reconciliation appends a new report version rather than silently rewriting an already issued report.
9. The formatter receives a derived report model and remains incapable of upgrading an incomplete disposition based only on execution_status and exit_code.

**Decision needed before provider implementation:** approve a versioned canonical disposition model and its gate ownership, then define a versioned projection to the simpler UI/report verdict. Until then, keep PR #2's formatter as a pure presentation helper and PR #3's lifecycle model as a separate draft contract.

## Follow-up evidence: acceptance tests clarify the integration seam (2026-10-28)

**Status:** Static source inspection of exact branch files and test definitions. The tests below were not executed in this pass; file contents are not proof that tests pass in a runtime.

### Exact reviewed sources

- `main` `PRODUCT/EXECUTION_CONTRACT.md`, blob `3861e51ae4f9e45a263b677402f26c41b240959d`; lines 171–180 describe proposed formatter checks, including confirmed zero exit plus confirmed terminal success for PASS and INCOMPLETE for timeout/cancel/rejection/missing terminal evidence/infrastructure uncertainty. Lines 203 onward explicitly state the listed tests are proposed and none is marked passed until implemented and executed in a controlled environment.
- PR #2 branch `chat-continuity-report-regressions-2026-10-26`, `scripts/report_contract.py`, blob `e9d944a722c2fac5279952696528da72a7011af3`; `classify_verdict` uses the supplied `execution_status` and `exit_code`. Its module/docstring says it formats supplied metadata and does not execute submitted code. Companion `scripts/test_report_contract.py`, blob `39f3a3ef865ed55f333a1edc208096d99197d023`, has 146 lines and includes lifecycle-state, missing-exit, boolean-exit, simulated-report and bounded-report cases.
- PR #3 branch `pocketcode-pass0-audit-2026-10-26`, `AI_COLLAB/DRAFT_EXECUTION_CONTRACT.md`, blob `02ad9934cc40c84f7e8cd7f6c982d5d8ed7d1b70`; lines 73–91 define separate `execution_outcome`, `cleanup_state`, derived `job_disposition`, report versions, PASS gates, and artifact quarantine. `scripts/lifecycle_contract.py`, blob `ba8d4d0b217c90513bed020e298029ef4e16f164`, derives disposition using cleanup, policy, termination, artifact and tenant/job authorization gates. Companion `scripts/test_lifecycle_contract.py`, blob `39db87d9f44f5e8474f33cff60136e529364199a`, includes cases requiring those gates and checking cleanup reconciliation/history; PR #3's `scripts/test_report_contract.py` is blob `85109f056009d65a274e9306deb39b68e1fefbd2`.

### Refined conclusion

The isolated formatter is not, by itself, evidence of an implementation defect: it is a presentation helper that accepts supplied metadata. The integration risk is at the call boundary. If a caller maps a raw execution status plus exit code directly into the user-facing verdict, without first deriving the trusted PR #3-style disposition, it can bypass mandatory policy, termination, cleanup, artifact-integrity and tenant/job-authorization gates. Therefore the canonical flow must be explicit: **authoritative observations → versioned disposition derivation → report formatting**. The formatter must render, not upgrade, the disposition.

The two-axis model is important: `execution_outcome` records what execution did (or whether it started/ended); `job_disposition` records what the system is permitted to conclude after applying all evidence and safety gates. These fields are related but not interchangeable. Keep a nonzero process outcome visible even if cleanup is later uncertain; cleanup uncertainty must separately block artifact release and a clean final disposition rather than erase the process observation.

### Required follow-up before integration approval

1. Define a versioned, explicit projection from PR #3 lifecycle observations/disposition to the main/PR #2 report vocabulary; do not assume a one-to-one enum rename.
2. Require report generation to consume the derived disposition and evidence references, not re-derive PASS from client-controlled or partial fields.
3. Add an integration-level regression case: zero exit + success-like raw status but missing/stale policy confirmation, termination evidence, cleanup confirmation, artifact integrity, or tenant/job authorization must not produce PASS or release artifacts.
4. Add a history/reconciliation case proving later cleanup evidence creates a new immutable report version without rewriting the earlier report.
5. Reconcile terminology for `program_failed`/`FAILED`, `infrastructure_failed`/`PROVIDER_ERROR`, and terminal status versus disposition before freezing the external schema.

These are proposed acceptance requirements only. No source code changed on PR #2 or PR #3, no test was run, and no integration is claimed.

## Follow-up proposal: two-axis vocabulary and conservative display projection (2026-10-28)

**Proposal only:** This table is a discussion aid to make the integration seam reviewable. It is not an approved schema, implementation, or assertion that all states currently exist on every branch.

### Axis A — execution observation (what happened)

| Candidate `execution_outcome` | Meaning | Minimum evidence expectation |
|---|---|---|
| `NOT_STARTED` | No user program started | Authoritative validation/policy rejection or provider-preparation evidence; distinguish from missing start evidence |
| `EXIT_ZERO` | Process reported a zero exit | Attempt-bound authoritative exit/terminal evidence; does not by itself mean the job passed |
| `EXIT_NONZERO` | Process reported a nonzero exit | Attempt-bound authoritative exit evidence; retain exit code and relevant bounded error output |
| `TIMED_OUT` | Deadline outcome was reported | Trusted deadline/limit event; separately record whether process-tree termination is confirmed |
| `CANCELLED` | Cancellation outcome was reported | Cancellation request and separate termination confirmation; request alone is not proof of stopped process |
| `LIMIT_EXCEEDED` | An enforced execution/output limit was hit | Trusted limit event, byte counts where applicable, and truncation/discard evidence |
| `UNKNOWN` | Execution outcome cannot be established reliably | Missing, malformed, contradictory, stale, or incorrectly associated provider evidence |

### Axis B — derived job disposition (what may safely be concluded)

| Candidate `job_disposition` | Required derivation | Candidate simple report verdict | Important retained facts |
|---|---|---|---|
| `REJECTED` | Authoritative pre-start validation/policy rejection; no contradictory execution evidence | `INCOMPLETE` | Explicitly say not started; safe rejection reason |
| `PASS` | Zero exit plus all mandatory policy, termination, artifact-integrity, tenant/job authorization and cleanup gates confirmed | `PASS` | Gate provenance and report version |
| `FAILED` | Confirmed program failure/nonzero exit, with no evidence that contradicts the failure observation | `FAIL` | Preserve exit/error evidence even if a separate cleanup issue remains |
| `TIMED_OUT` | Timeout outcome and termination confirmed | `INCOMPLETE` | Deadline evidence and termination status |
| `CANCELLED` | Cancellation outcome and termination confirmed | `INCOMPLETE` | Cancellation and termination status separately |
| `LIMIT_EXCEEDED` | Trusted limit event; classify limit-caused termination separately from collection-only cap | Verdict OPEN under D-01: candidate FAIL for confirmed runtime failure, INCOMPLETE if terminal outcome is unknown/contradictory | Exact limit, terminal evidence, bounded/truncated output, and required evidence missing |
| `PROVIDER_ERROR` | Provider/execution evidence is unavailable, malformed, contradictory, or untrustworthy | `INCOMPLETE` | Unknowns, conflicting evidence and reconciliation path |
| `INCOMPLETE` | A required gate/evidence item is missing, stale, or unconfirmed; or outcome cannot safely support a stronger conclusion | `INCOMPLETE` | Gate(s) not met and any known execution observations |

### Projection invariants

1. `execution_outcome` and `job_disposition` must be separate fields; neither is an alias for the other.
2. The simple verdict is a lossy display summary, not the source of truth. Preserve the detailed disposition, outcome, reason codes, evidence references, policy revision, cleanup state, artifact gate state, and report version in the canonical model.
3. A zero exit never implies `PASS` by itself. A formatter must consume an already-derived disposition and may not infer security gates from client-supplied status strings.
4. A confirmed nonzero exit remains an observed program failure even if cleanup is later uncertain. Artifact release remains independently blocked until cleanup/integrity/authorization gates pass; do not erase one fact to represent another.
5. Timeout/cancellation without confirmed termination cannot claim that execution stopped. It remains `INCOMPLETE` or an equivalent explicitly uncertain disposition until reconciled.
6. Unknown or contradictory evidence never becomes `PASS` through retries, formatting, or report-version replacement. Later authoritative evidence appends a new report version and retains prior history.
7. Names and mappings (`FAILED` vs `program_failed`; `PROVIDER_ERROR` vs `infrastructure_failed`; UI `FAIL` vs `INCOMPLETE`) require owner/reviewer approval before the external schema is frozen.

**Recommended next review:** have Claude and Gemini independently challenge this mapping against the exact PR #2 and PR #3 branches. Only after review should an authorized integration task change authoritative contracts or tests. No code or tests were changed/run by adding this proposal.

## Static reviewer challenge: disposition ordering and gate semantics (2026-10-28)

**Exact PR #3 helper reviewed:** scripts/lifecycle_contract.py, blob ba8d4d0b217c90513bed020e298029ef4e16f164, function derive_disposition. **PR #2 formatter reviewed:** scripts/report_contract.py, blob e9d944a722c2fac5279952696528da72a7011af3, function classify_verdict. This is static source inspection only; neither helper nor tests were executed in this pass.

### Confirmed ordering behavior

The PR #3 helper checks contradictory evidence first, then NOT_STARTED, limit conditions, UNKNOWN, timeout/cancellation termination, and then EXIT_NONZERO. The EXIT_NONZERO branch returns FAILED **before** checking cleanup_state, policy_confirmed, termination_confirmed, artifacts_valid, or tenant_job_authorized. Those four booleans plus confirmed cleanup are checked only on the EXIT_ZERO path.

This is not automatically a defect: preserving a confirmed nonzero process observation is important, and artifact release can remain separately blocked. But it leaves a material contract question because the function calls its output a **job disposition**, while a nonzero exit alone does not establish that the job was authorized, that the required policy was applied, or that lifecycle evidence is complete.

### Required clarification before calling the projection settled

Keep the two axes explicit:

- execution_outcome=EXIT_NONZERO can preserve the observed process failure even when another gate is uncertain.
- The canonical job-level conclusion must state whether FAILED is intentionally allowed when policy/authorization/cleanup gates are missing, or whether those cases require INCOMPLETE (with the observed nonzero exit retained separately).
- Artifact release/visibility must be a separate fail-closed decision; FAILED must never implicitly authorize artifacts.
- A NOT_STARTED value must be backed by authoritative pre-start evidence, not merely a caller-supplied enum. The pure helper's signature cannot itself establish that provenance; this is a caller/contract precondition unless the API is redesigned.
- A boolean such as policy_confirmed=True is not enough for a real provider boundary unless it is bound to the exact required policy revision and confirmed before start. The PR #3 applied-policy/ETag barrier remains an integration evidence requirement, not something this pure helper proves.

### Minimal reviewer matrix to add before integration

| Synthetic observation | Preserve execution outcome | Candidate job disposition question | Artifact release |
|---|---|---|---|
| EXIT_NONZERO, all mandatory gates confirmed | EXIT_NONZERO | FAILED / FAIL is appropriate if failure is attributable to the program | Only if artifact policy independently allows release |
| EXIT_NONZERO, cleanup unknown | EXIT_NONZERO | Decide whether overall disposition is FAILED plus cleanup warning, or INCOMPLETE with failure observation retained | Deny until cleanup/integrity/authorization requirements pass |
| EXIT_NONZERO, required policy not confirmed or tenant/job authorization false | EXIT_NONZERO if trustworthy evidence exists | Do not silently treat a process exit as proof the job was validly authorized; explicit disposition rule required | Deny |
| EXIT_ZERO, any required gate missing/stale/false | EXIT_ZERO | INCOMPLETE, not PASS | Deny |
| Any outcome with contradictory evidence | Preserve individual observations and conflict | INCOMPLETE (or a separately approved conflict disposition), never PASS | Deny |
| NOT_STARTED without authoritative pre-start evidence | UNKNOWN / unresolved, not a trusted rejection | INCOMPLETE or provider error until reconciled | Deny |

**Reviewer conclusion:** the current advisory projection is directionally conservative, but it is not yet precise enough to freeze the FAILED vs INCOMPLETE rule when nonzero exit coexists with a failed or unconfirmed security/lifecycle gate. Do not modify PR #2 or PR #3 as part of this documentation pass. Ask Claude and Gemini for independent opinions on this exact question before integration approval; no owner decision is inferred.

## Follow-up: artifact-release boundary is explicitly separate; policy revision is not encoded in the pure gate (2026-10-28)

A targeted read of PR #3's exact DRAFT_EXECUTION_CONTRACT.md (blob 02ad9934cc40c84f7e8cd7f6c982d5d8ed7d1b70), lifecycle helper (blob ba8d4d0b217c90513bed020e298029ef4e16f164), and test helper (blob 39db87d9f44f5e8474f33cff60136e529364199a) narrows the previous concern:

- **Artifact release is explicitly separate.** The draft contract says artifacts remain quarantined until cleanup is confirmed and integrity plus per-request tenant/job authorization pass. The pure artifact_release_allowed helper checks cleanup_state == CONFIRMED, digest_valid is exactly True, job_association_valid is exactly True, and tenant_authorized is exactly True. Tests cover unknown cleanup and each independent release gate. This is a strong contract/test-design point, not proof of a real provider's isolation or cleanup.
- **PASS gates exist in both contract and helper.** The draft requires authoritative zero exit, exact mandatory policy revision confirmation before execution, termination evidence, no prohibited timeout/cancel/limit/truncation, validated manifest/hashes, tenant/job association, and confirmed cleanup. The pure derive_disposition helper checks the policy/termination/artifact/tenant booleans and cleanup on the EXIT_ZERO path; its interface does not carry the policy revision identifier or prove when the policy was applied.
- **The remaining disposition ambiguity is narrow but real.** Current tests require EXIT_ZERO to meet every gate, but there is no visible test in the reviewed test file asserting how EXIT_NONZERO should be classified when cleanup is unknown or policy/tenant authorization is false. The helper returns FAILED before those checks. The contract preserves the nonzero execution observation, but its versioned job-disposition policy still needs to define this combination explicitly.
- **Offline-only boundary remains clear.** The contract and helper describe synthetic/fake-adapter logic. Their presence does not prove real termination, egress, cleanup, policy application, tenant isolation, artifact safety, or billing behavior.

### Recommended smallest follow-up

Before integration or schema freeze, add reviewer-approved semantic cases (not necessarily new enum values) for:
1. EXIT_NONZERO + cleanup UNKNOWN;
2. EXIT_NONZERO + policy revision missing/mismatched or not confirmed before start;
3. EXIT_NONZERO + tenant/job authorization false;
4. artifact_release_allowed false for each corresponding gate even when disposition is FAILED;
5. EXIT_ZERO + policy revision absent or confirmed only after start.

Expected invariant: retain trustworthy execution observations; never let a process verdict bypass security gates or release artifacts; represent job disposition and release eligibility separately. The exact FAILED-versus-INCOMPLETE display for cases 1–3 remains an explicit contract decision, not a conclusion inferred from this static review.

## Follow-up: source-to-test traceability map (2026-10-28)

**Status:** Read-only source/test design review. Exact checked-in PR #3 tests have NOT RUN in this pass. “Source-covered” means the named pure helper/test source contains a relevant assertion; it does not mean the test passed or that an adapter/provider enforces the behavior.

| Invariant | Exact source evidence in PR #3 draft | Existing test evidence | Current classification / missing proof |
|---|---|---|---|
| Exact mandatory policy revision applied to the intended boundary before task start | `AI_COLLAB/DRAFT_EXECUTION_CONTRACT.md` policy barrier; `AI_COLLAB/OFFLINE_ACCEPTANCE_TEST_MATRIX.md` NET-BARRIER-01 and NET-SEM-01; `scripts/lifecycle_contract.py` accepts only boolean `policy_confirmed` in `derive_disposition` | The matrix specifies a fake-provider start-call barrier, but `scripts/test_lifecycle_contract.py` has no coordinator/adapter start-call test in the reviewed source | **Missing from reviewed implementation source; NOT RUN.** Need an adapter/coordinator seam that checks policy identity/revision and records confirmation before invoking execute. A boolean disposition gate is not proof of identity or chronology. |
| EXIT_ZERO must not become PASS with cleanup/policy/termination/artifact/tenant evidence missing | `scripts/lifecycle_contract.py` `derive_disposition`; draft contract PASS/release gate sections | `test_exit_zero_needs_cleanup_policy_termination_artifact_and_tenant_gates`; `test_malformed_truthy_gate_values_never_produce_pass`; `test_timeout_unknown_termination_and_output_violation_never_pass` | **Pure logic source-covered; NOT RUN.** Does not prove upstream evidence is authoritative, fresh or job-bound. |
| EXIT_NONZERO observation with cleanup/policy/authorization failure | `derive_disposition` returns `FAILED` for EXIT_NONZERO before checking cleanup or the other gates | No focused test found for EXIT_NONZERO combined with cleanup UNKNOWN/FAILED, policy false, or tenant/job authorization false | **Open disposition semantic / test gap; NOT RUN.** Preserve the process observation; explicitly define overall disposition; independently block artifacts. Do not call it a proven vulnerability from the pure helper alone. |
| Artifact release requires cleanup, digest, job association and tenant authorization | `artifact_release_allowed` requires cleanup `CONFIRMED` and each other flag exactly `True` | `test_artifact_release_requires_each_gate_independently`; `test_artifact_release_rejects_truthy_non_boolean_evidence` | **Pure helper source-covered; NOT RUN.** No provider storage/quarantine or real per-request authorization is established. |
| Cleanup reconciliation preserves earlier report and appends a new version | `ReportHistory.append` models versioned report history | `test_cleanup_reconciliation_appends_new_report_version_without_rewriting_history`; `test_report_history_versions_are_per_job_and_require_evidence_reference` | **Pure model source-covered; NOT RUN.** Does not prove durable transactional persistence or concurrent production behavior. |
| Terminal event ordering is deterministic and contradictory terminal events do not silently pass | `reduce_terminal_events` uses coordinator sequence and flags duplicate/conflicting terminal evidence | `test_coordinator_sequence_wins_over_provider_timestamp`; `test_duplicate_event_is_idempotent_but_conflict_is_marked`; `test_duplicate_event_id_with_changed_sequence_is_conflict`; `test_duplicate_coordinator_sequence_has_deterministic_replay_order` | **Pure replay source-covered; NOT RUN.** Does not prove an actual coordinator assigns unique sequences atomically or commits terminal state transactionally. |
| Output remains bounded and overflow is explicit | `OutputBudget` tracks per-stream and aggregate observed/retained bytes | `test_artifact_and_output_gates`; `test_aggregate_cap_triggers_when_each_stream_is_below_its_own_cap`; `test_output_budget_counts_observed_bytes_and_stops_retaining_on_overflow` | **Pure byte-accounting source-covered; NOT RUN.** Does not prove OS pipe draining, process termination or provider-side memory limits. |
| AI report does not claim execution or verification without evidence | PR #2 formatter and prototype have explicit simulation labels; PR #3 report matrix includes REPORT-01/REPORT-02 | PR #2 formatter tests are separately recorded in this audit; the PR #3 helper suite is synthetic | **Presentation/contract requirement; NOT RUN as a cross-branch integration.** Need a caller-level regression proving formatter cannot derive PASS directly from raw fields while mandatory gate evidence is missing. |

### Dependency order for the first PC session

1. Re-fetch live refs and blob SHAs; build separate clean worktrees for PR #2 and PR #3.
2. Run only the documented offline Python tests/checker; record exact command, environment, exit code and test totals. Stop on unavailable dependencies rather than installing broadly.
3. Add or finalize the policy barrier and nonzero-plus-gate semantic cases only after reviewer/owner agreement; do not patch either PR in this pass.
4. Review the caller/integration seam before considering any report-vocabulary mapping.
5. Keep real-provider tests blocked until the explicit $0/cost, security, synthetic-input and owner-approval gates in the PC-return checklist are met.

This table is a traceability aid, not a claim that source-covered cases pass, that any coordinator exists, or that offline tests establish live security properties.


## Follow-up semantic clarification — 2026-10-29

The earlier conservative LIMIT_EXCEEDED → INCOMPLETE rows in this cross-branch audit are superseded by the more precise, still owner-open D-01 decision. Do not treat `LIMIT_EXCEEDED` alone as sufficient to infer one user verdict. Distinguish trusted limit-caused termination/failure (candidate FAIL under canonical wording), a collection-only cap alongside independently confirmed EXIT_ZERO (verdict depends on case-specific required-output rules), and presentation-only truncation (does not change execution verdict). Unknown or contradictory terminal evidence remains INCOMPLETE. See `OWNER_DECISION_REGISTER_20261029.md`, `SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md`, and `SEMANTIC_DECISION_CROSSWALK_20261029.md`.
