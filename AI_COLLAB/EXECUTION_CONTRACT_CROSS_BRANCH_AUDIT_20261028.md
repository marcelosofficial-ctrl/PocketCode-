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

**Recommended next contract action (not an approved schema):** define one versioned projection from PR #3's detailed outcome/cleanup/disposition record to the simpler user-facing verdict. A conservative candidate is: PASS only for job_disposition PASS; FAIL only for a confirmed program failure/FAILED disposition; INCOMPLETE for rejection, timeout, cancellation, limit exceeded, provider error, unknown, contradictory, or missing evidence. Keep detailed state fields available separately; do not lose cleanup or reason codes in the summary.

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
