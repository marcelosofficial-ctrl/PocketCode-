# Offline acceptance-test traceability matrix

**Date:** 2026-10-27  
**Owner:** ChatGPT independent contribution  
**Status:** Proposed test specification only. No tests were implemented or executed in this pass; no provider was tested.  
**Related:** [Draft execution contract](DRAFT_EXECUTION_CONTRACT.md), [Security research](PASS1_SECURITY_ABUSE_RESEARCH.md), [Contract audit](CONTRACT_COHERENCE_AUDIT.md), [Lifecycle resolution proposal](PASS1_CONTRACT_COHERENCE_RESOLUTION.md), [Decision register](DECISION_REGISTER.md).

## Contract blocker

The draft lifecycle places SUCCEEDED before CLEANUP_PENDING and CLEANED/CLEANUP_FAILED, but also says SUCCEEDED requires cleanup success. These statements conflict unless execution outcome and overall job disposition are separate concepts. Do not implement the state machine verbatim.

**Proposed resolution for review, not yet adopted:** keep execution outcome separate from service disposition. Preserve a successful process exit as an observation, but set overall status to non-PASS if cleanup or required evidence is missing. Choose final field names and statuses before freezing the schema.

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

Resolve the lifecycle contradiction and the open questions in the contract audit before implementation. The two-axis outcome/disposition model is a proposal only and requires review before schema freeze. Provider integration remains blocked by the strict $0 gate.
