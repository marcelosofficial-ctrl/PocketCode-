# Report projection v2 migration and acceptance packet

Date: 2026-11-12
Status: read-only source audit and proposed migration packet; no implementation authorization.
Scope: report_contract.py, execution_projection.py and their model tests.
Authority: preserve LOOP-01..14, CASE-01..16, D-IDs and OD-01..OD-13. This packet does not amend canonical contracts.

## 1. Finding

VERIFIED source pins on branch `pocketcode-ai-workflow-director-research-2026-10-28`:
- `scripts/report_contract.py` blob `2459137b6f8d4b6bfadd6218e5a9bd92e75b0817`.
- `scripts/test_report_contract.py` blob `85109f056009d65a274e9306deb39b68e1fefbd2`.
- `scripts/execution_projection.py` blob `f32237c8c5ee5d62b0416b3dd867515ce567c21b`.
- `scripts/test_execution_projection.py` blob `cbd756cce1bc42a6aab0d5c48d8fac6f56cce7c1`.

The legacy `classify_verdict(execution_status, exit_code)` treats any integer nonzero exit as FAIL before it considers lifecycle. It therefore returns FAIL for a nonzero code paired with `timed_out`, `cancelled`, `rejected`, `infrastructure_failed`, `accepted`, `queued`, `running`, or an unknown status. `format_report()` normalizes an unrecognized status to `unknown`, but still passes a valid integer exit code to this classifier. A wrapper exit, signal convention, embedded interpreter request, or caller-invented integer is indistinguishable from a trusted direct-child natural exit.

The existing test suite covers nonzero exit with `succeeded`, and timeout/cancel/rejection/infrastructure states with no exit code. It does not cover their cross-product. This is a model-test coverage gap, not evidence that an external runner currently supplies such values.

## 2. Existing typed projection is the correct design input, not an authority

`execution_projection.project_verdict()` already distinguishes coordinator lifecycle, direct-child natural wait, wrapper exit, signal termination and embedded interpreter observations. Its current tests include timeout plus wrapper 137 and keep the result INCOMPLETE with no child exit code.

Important boundary: this module is explicitly a pure helper. It validates typed shapes, producer classes and attempt IDs, but it does not authenticate producers, authorize attempts, deduplicate persisted events, validate current policy or establish coordinator authority. Typed strings supplied by an untrusted caller are not proof. The authenticated adapter/coordinator boundary must precede this helper.

The lifecycle acceptance contract remains controlling for three independent outputs:
1. Execution verdict/evidence.
2. Overall job/evidence disposition, including policy barriers, collection and cleanup.
3. Artifact disposition and release eligibility.

A report formatter may render these resolved projections. It must not collapse them into one verdict or independently infer authority from raw fields.

## 3. Proposed versioned report boundary

Keep report format 1 and the two-argument legacy classifier unchanged until a separately reviewed implementation gate is granted. Introduce a versioned format 2 input rather than silently changing old report meaning.

Proposed input sections (field names illustrative, not canonical IDs):
- `format_version: 2`.
- `identity`: CommandId, EffectId, DispatchAttemptId, ExecutionId when known, ResultReceiptId and immutable receipt revision.
- `execution_projection`: contract version, coordinator-resolved lifecycle, verdict, reason, and child natural exit code only when established by an accepted direct-child wait.
- `job_disposition`: complete/incomplete state and explicit policy-barrier, collection and cleanup outcomes.
- `artifact_disposition`: immutable artifact/object version, byte length, digest, integrity/quarantine and release state.
- `raw_evidence_refs`: immutable references/digests and accepted ObservationSequence high-water, preserving source class and provenance without allowing the renderer to reinterpret them.
- `uncertainties`: explicit missing, contradictory or unauthenticated evidence.

Validation before rendering:
- Require the exact supported format and projection contract versions.
- Require authenticated coordinator/adapter provenance and exact attempt binding before accepting the projection.
- Reject a caller-supplied verdict that is not bound to the accepted immutable projection.
- Preserve raw observations and contradiction details; never rewrite history to make the projection look consistent.
- Reject malformed types, booleans masquerading as integers, missing identity, invalid sequence/high-water and unknown critical fields.
- Bound all strings, lists and total rendered output using the existing report limits.
- A simulated report remains explicitly simulated and can never become PASS.
- Missing projection or any required uncertainty yields INCOMPLETE, not a guessed FAIL or PASS.
- The renderer is pure: it formats an already resolved projection and does not authenticate, repair, retry, execute or authorize artifact release.

## 4. Minimum regression matrix for a future gated model change

| Input evidence | Required execution result | Required report behaviour |
|---|---|---|
| `timed_out` + wrapper exit 137 | INCOMPLETE | Never show program FAIL from wrapper code |
| `timed_out` + direct-child natural exit 137 | INCOMPLETE | Preserve raw child observation; timeout lifecycle remains unresolved |
| `cancelled` / `rejected` / `infrastructure_failed` + any wrapper nonzero | INCOMPLETE | Preserve lifecycle and wrapper fact separately |
| `running` / `queued` + child nonzero | INCOMPLETE or contradiction per coordinator reconciliation | No precedence-only FAIL |
| `succeeded` + wrapper exit 0, no child wait | INCOMPLETE | No PASS |
| `succeeded` + direct-child natural exit 0, trusted projection | PASS candidate | Overall job may still be INCOMPLETE |
| `succeeded` + direct-child natural nonzero | INCOMPLETE contradiction | Preserve both facts |
| `program_failed` + trusted coordinator disposition | FAIL candidate | Collection/cleanup can still make overall job INCOMPLETE |
| Unknown/malformed status + nonzero caller code | INCOMPLETE | No caller-controlled FAIL |
| Boolean exit code, missing projection or wrong attempt | INCOMPLETE | Reject/mark untrusted; no PASS |
| Correct execution projection + missing policy barrier | Execution facts retained | Overall INCOMPLETE; artifact blocked |
| Correct bytes + missing receipt/current authorization | Execution facts retained | Artifact not releasable |
| Legacy format 1 input | Existing bounded legacy behaviour | No silent reinterpretation during migration |
| Simulated format 2 input | INCOMPLETE | Simulation banner remains explicit |

Tests should assert the three projections independently, exact attempt/receipt binding, deterministic rendering, format-1 compatibility, output bounds and absence of authority from caller-supplied fields. Keep tests deterministic and standard-library-only if a future owner gate authorizes model work.

## 5. Safe implementation sequence after a separate gate

1. Review the v2 schema and compatibility policy; do not change format 1 semantics in place.
2. Add typed format-2 input validation that consumes an already authenticated, immutable coordinator projection.
3. Add pure rendering from the accepted projection; preserve raw evidence references and explicit uncertainty.
4. Add the regression matrix above and run the full scripts discovery suite on an exact pinned source SHA.
5. Review the diff for accidental adapter, provider, runtime, storage, network or canonical-ID changes.
6. Keep model PASS distinct from durable adapter, device, production and CASE acceptance. CASE-04 remains INCOMPLETE / timed_out until authoritative same-attempt evidence exists.

## 6. Red-team limits and current gate

- The typed projection is not cryptographic producer authentication.
- A report schema does not prove the coordinator persisted observations atomically.
- A model test does not prove a real child wait, browser worker termination, cleanup, policy barrier or artifact receipt.
- A renderer must not be used as a security boundary.
- No precedence-only patch is acceptable.
- No source/test implementation, provider/runtime/adapter choice, device test, deployment or spending is authorized by this packet.

Evidence: source structure and stated test cases VERIFIED from the pinned blobs above. Cross-product tests NOT RUN. Production report caller provenance UNKNOWN. P39 implementation/adapter gate CLOSED. CASE-04 remains INCOMPLETE / timed_out.
