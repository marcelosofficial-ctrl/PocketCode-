# Offline acceptance-test traceability matrix

**Date:** 2026-10-27  
**Owner:** ChatGPT independent contribution  
**Status:** Selected test specification plus initial pure helper/test files. The repository test suite is NOT RUN; no provider was tested.  
**Related:** [Draft execution contract](DRAFT_EXECUTION_CONTRACT.md), [Security research](PASS1_SECURITY_ABUSE_RESEARCH.md), [Contract audit](CONTRACT_COHERENCE_AUDIT.md), [Lifecycle resolution proposal](PASS1_CONTRACT_COHERENCE_RESOLUTION.md), [Decision register](DECISION_REGISTER.md), [Lifecycle/idempotency/artifact proposal](PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md), [Owner decision packet](PASS1_OWNER_DECISION_PACKET_20261027.md).

## Contract blocker

The draft lifecycle places SUCCEEDED before CLEANUP_PENDING and CLEANED/CLEANUP_FAILED, but also says SUCCEEDED requires cleanup success. These statements conflict unless execution outcome and overall job disposition are separate concepts. Do not implement the state machine verbatim.

**Proposed resolution for review, not yet adopted:** keep execution outcome separate from service disposition. Preserve a successful process exit as an observation, but set overall status to non-PASS if cleanup or required evidence is missing. Choose final field names and statuses before freezing the schema. The six open decision areas and recommended defaults are consolidated in [PASS1_OWNER_DECISION_PACKET_20261027.md](PASS1_OWNER_DECISION_PACKET_20261027.md); every approval remains pending.

## Proposed offline tests

All tests below use synthetic inputs and a fake adapter. They do not run submitted code. Assert both returned status and adapter side effects/call order.

| ID | Setup | Required result |
|---|---|---|
| REQ-01 | Unsupported schema version | Reject before adapter allocation |
| REQ-02 | Input at byte limit and one byte over; multibyte text | Enforce decoded byte count, not character count |
| REQ-03 | Traversal, absolute path, duplicate normalized names, NUL | Reject ambiguous or unsafe paths |
| REQ-04 | Archive or unsupported media type | Reject under initial allowlist |
| POL-01 | Client requests more permissions or larger limits than server policy | Never grant extra permissions |
| AUTH-01 | Missing tenant or client-supplied tenant spoof | Reject or ignore spoof; bind owner from authenticated context |
| AUTH-02 | Another tenant requests status, cancellation, report, or artifact | Deny access without leaking protected content |
| IDEM-01 | Repeated request ID from same and different tenants | Deterministic idempotency; no cross-tenant collision |
| CAP-01 | Mandatory capability unsupported, unverified, or blocked by plan | Stop before execution |
| CAP-02 | Capability evidence belongs to a different plan/configuration | Recheck or reject |
| LIFE-01 | Invalid transition or late success after timeout | Reject transition; committed outcome stays immutable |
| LIFE-02 | Provider preparation fails | No execution claim |
| LIFE-03 | Cancellation requested but termination unconfirmed | Remain pending; do not claim cancellation complete |
| LIFE-04 | Cleanup retried more than once | Idempotent behavior; preserve event history |
| EVID-01 | Exit code zero but policy/termination evidence missing | Overall status is not PASS |
| EVID-02 | Client claim conflicts with provider evidence | Ignore client execution claims; preserve contradiction |
| OUT-01 | Output and artifacts at cap and cap+1 | Enforce byte/count limits and disclose truncation |
| ART-01 | Unsafe artifact name, unknown ID, or cross-tenant ID | Deny access; never derive storage path from display name |
| UI-01 | HTML/script-like strings in output or filenames | Display inertly and escape untrusted content |
| REDACT-01 | Synthetic secret-like text in source/output | Do not inject service secrets; verify report redaction |
| COST-01 | Provider usage data unavailable | Cost remains unknown, never zero |
| REPORT-01 | Formatter attempts PASS while evidence indicates timeout or cleanup failure | Reject inconsistent status |
| REPORT-02 | Documented capability compared with configured and tested behavior | Keep evidence categories distinct |
| CLEAN-01 | Successful exit followed by failed or unknown cleanup | Preserve execution observation; overall status is not PASS |
| LIMIT-01 | Limit configured but enforcement not observed | Do not claim the limit was enforced |
| NET-BARRIER-01 | Fake provider reports required network policy as pending, wrong revision, failed, missing, or applied only after a deterministic scheduler event | No task-start call until exact required policy/revision is confirmed applied; timeout/mismatch fails closed |
| RACE-01 | Deterministic scheduler delivers cancel and timeout signals in both possible orders, including same logical tick | One authoritative execution outcome is committed; duplicate terminal events do not cause duplicate cleanup; chronology remains recorded |
| PROC-TREE-01 | Local test harness creates a parent and descendant process under the test OS | Harness records whether descendants terminate before cleanup is considered confirmed; label OS-specific behavior and do not infer provider process-tree guarantees |
| STREAM-01 | Synthetic stdout/stderr arrives in chunks much larger than the inline cap | Memory use remains bounded by implementation design; inline report is capped with explicit truncation and total observed-byte metadata |
| REDACT-02 | Synthetic token-shaped strings appear across chunk boundaries in stdout/stderr | Configured detector catches the fixture across chunks, emits redaction marker and redaction metadata; test must not imply universal secret detection |
| ARTIFACT-02 | Artifact write is interrupted or computed digest differs from final stored bytes | Artifact marked invalid/incomplete; no PASS and no valid manifest entry for corrupted bytes |
| TELEMETRY-01 | Provider invoice/cost endpoint is delayed while local CPU/RAM observations exist | Report separates observed resource telemetry from estimated cost; cost status is ESTIMATED or UNAVAILABLE per defined rule, never falsely final or $0 |
| IDEM-02 | Same tenant submits same idempotency key with a different canonical payload | Return a deterministic conflict; do not launch a second job or return the first job's result as if it matched |
| CSV-01* | If CSV is confirmed as the first workflow: unsupported encoding, malformed header, or size above configured limit | Reject before sandbox allocation according to the documented CSV policy; this is workflow-specific, not a universal execution-contract rule |

## Lifecycle-resolution cases (proposed; not run)

These additional cases trace [PASS1_CONTRACT_COHERENCE_RESOLUTION.md](PASS1_CONTRACT_COHERENCE_RESOLUTION.md). They refine the generic cases above and should be implemented together when offline tests are authorized. They are **not executed tests**.

| ID | Synthetic scenario | Required assertion |
|---|---|---|
| LC-01 | Exit code 0, cleanup pending | No PASS while cleanup is pending |
| LC-02 | Exit code 0, cleanup fails | Preserve exit-zero execution fact; disposition is non-PASS and exposes cleanup failure |
| LC-03 | Timeout requested, termination unknown | Do not claim process stopped; no PASS |
| LC-04 | Cancel requested, late success event arrives | No silent PASS; reconcile chronology or mark incomplete |
| LC-05 | Duplicate/out-of-order provider events | Idempotent processing; no unsafe regression to PASS |
| LC-06 | Cleanup retry eventually succeeds | Append recovery evidence; preserve initial failure event; apply explicit disposition rule |
| LC-07 | Exit code 0 but policy confirmation missing/stale | No PASS |
| LC-08 | Exit code 0 but artifact manifest missing/contradictory | No PASS |
| LC-09 | Client supplies PASS or fabricated exit code | Client fields cannot influence authoritative outcome |
| LC-10 | Provider cost observation absent | Report cost as unknown, not zero |
| LC-11 | Same idempotency key from two tenants | No cross-tenant collision or disclosure |
| LC-12 | Cleanup success event belongs to another job | Reject evidence association; no PASS |



*CSV-01 is conditional on owner confirmation that CSV is the initial supported workflow. The proposed 1 MiB inline cap is not adopted; choose it only after payload and memory budgets are reviewed. Secret redaction is best-effort defense-in-depth and cannot guarantee that all secrets are detected. Tests using fake adapters verify orchestration logic only.

## Provider-dependent tests — not authorized

These need explicit owner approval, an eligible exact plan, required permissions, and a proven spending ceiling. E2B also requires prior written consent according to the reviewed documentation.

- **LIVE-01 Isolation:** separate jobs cannot access each other's data or processes.
- **LIVE-02 Network:** provider-level controls block unintended internet, internal address, and metadata access.
- **LIVE-03 Resource limits:** time, CPU, memory, process, disk, and output caps are actually enforced.
- **LIVE-04 Cancellation:** the complete process tree stops after timeout/cancel.
- **LIVE-05 Cleanup:** provider cleanup behavior is observed and reported honestly.
- **LIVE-06 Cost:** usage and account-level spending controls fail closed.
- **LIVE-07 Tenant boundary:** deployed API denies cross-tenant access.

Mocks and unit tests cannot substitute for these checks.

## Recording standard

For tests actually run, record test ID, source commit, exact command, runtime version, environment, synthetic fixture, exit code, result, and limitations. Otherwise label the test NOT RUN. Do not infer real-world security from a fake adapter.

## Next safe step

The lifecycle contradiction now has two linked resolution proposals: [PASS1_CONTRACT_COHERENCE_RESOLUTION.md](PASS1_CONTRACT_COHERENCE_RESOLUTION.md) and [PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md](PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md). They narrow the semantics but do not settle owner decisions or freeze the schema. Next is owner review of artifact quarantine/release, event reconciliation, idempotency retention/fingerprint, and stream-overflow behavior; implement pure offline tests only after those expected outcomes are agreed. Provider integration remains blocked by the strict $0 gate.


## 2026-10-27 lifecycle/idempotency/artifact expansion

Detailed proposed semantics and test IDs are in [PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md](PASS1_LIFECYCLE_IDEMPOTENCY_ARTIFACT_POLICY_20261027.md). These cases are specifications only and remain **NOT RUN**.

| ID | Synthetic scenario | Required assertion |
|---|---|---|
| LIFE-SEM-01 | Exit-zero evidence followed by cleanup failure | Preserve execution fact; disposition is not PASS; artifact remains quarantined |
| LIFE-SEM-02 | Cleanup retry succeeds after initial failure | Append retry evidence; preserve first failure; version report; release only after all gates pass |
| RACE-SEM-01 | Timeout/cancel signals arrive concurrently or in either order | Exactly one decision commits using documented coordinator ordering/precedence; both events retained; no duplicate cleanup. Same winner across permutations is required only if an explicit precedence rule is adopted |
| RACE-SEM-02 | Duplicate event ID with same vs conflicting payload | Same payload is idempotent; conflicting payload marks evidence contradictory |
| RACE-SEM-03 | Late success after timeout decision | No silent PASS; reconciliation requires an explicit authoritative ordering rule |
| RACE-SEM-04 | Replay accepted events with coordinator sequence numbers | Decision is reproducible from the recorded sequence; provider timestamps alone cannot silently reorder the committed result |
| IDEM-SEM-01 | Same tenant/key and same canonical request | One job/attempt; retry returns existing reference |
| IDEM-SEM-02 | Same tenant/key but changed source, input, or effective policy | Deterministic conflict before allocation; no second job or first-result substitution |
| IDEM-SEM-03 | Concurrent submissions with same tenant/key | Exactly one atomic reservation wins; loser applies same-key rules |
| IDEM-SEM-04 | Same key in different tenant namespaces | Independent jobs; no cross-tenant disclosure |
| ART-SEM-01 | Interrupted artifact write or final digest mismatch | No valid manifest publication; artifact quarantined; no PASS |
| ART-SEM-02 | Traversal/Unicode-lookalike display name | Storage identity remains server-generated; unsafe metadata rejected or normalized |
| ART-SEM-03 | Artifact requested by wrong job/tenant | Deny access and avoid metadata leakage |
| STREAM-SEM-01 | Chunked output exceeds cap | Bounded retention; observed byte count and truncation are explicit |
| STREAM-SEM-02 | Synthetic secret-shaped pattern crosses chunk boundary | Configured detector catches fixture; no claim of universal detection |
| COST-SEM-01 | Resource metrics exist but invoice data is delayed/missing | Keep observed telemetry distinct; cost is ESTIMATED or UNAVAILABLE, never falsely FINAL/$0 |
| NET-SEM-01 | Required policy revision changes between prepare and execute | Revalidate at the execution barrier; mismatch prevents task start |

**Decision status:** the six lifecycle choices are selected under owner delegation. The 30-day post-deletion tombstone and 1-second drain window are provisional policy defaults for offline tests, not production commitments. See [PASS1_OWNER_DECISIONS_RESEARCH_20261027.md](PASS1_OWNER_DECISIONS_RESEARCH_20261027.md) for rationale and source links.

## Current next safe step

The lifecycle decisions are selected and initial helper/test files are added. Next: run the offline test module in a local interpreter if available, review failures and source, then record exact results. Provider-dependent tests remain blocked by strict $0 and consent requirements. Do not claim fake-adapter tests prove provider isolation, egress, cleanup, or billing.


## Delegated decision update — 2026-10-27

The owner delegated selection of the six lifecycle decisions to ChatGPT. The selected defaults and research rationale are recorded in [PASS1_OWNER_DECISION_PACKET_20261027.md](PASS1_OWNER_DECISION_PACKET_20261027.md) and [PASS1_OWNER_DECISIONS_RESEARCH_20261027.md](PASS1_OWNER_DECISIONS_RESEARCH_20261027.md). These decisions resolve the design-level ambiguity: execution observations, cleanup state, and derived disposition are separate; artifacts remain quarantined until cleanup and integrity/authorization gates pass; event ordering uses coordinator-ingress sequence plus atomic terminalization; idempotency is tenant-scoped and fingerprinted; output caps terminate the attempt with bounded drain/discard; each report version is immutable.

Additional selected-decision tests are required for cleanup quarantine/release, report versioning, coordinator sequence replay, same-key/different-fingerprint conflicts, 30-day deletion tombstones, aggregate output cap plus 1-second drain deadline, and canonicalized input-name collisions. All are **NOT RUN**. Numeric limits are provisional offline-test defaults only. Provider tests, spend, deployment, and merge remain unauthorized.
