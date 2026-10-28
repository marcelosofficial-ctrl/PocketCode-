# Shared Run/Result Conformance Matrix v0.1

**Status:** Proposed contract and test plan; not an implementation or test report.  
**Date:** 2026-10-28  
**Budget:** $0; no provider, account, workload, billing, deployment, or native-app decision is authorized here.  
**Relationship:** PocketCode and RevDev remain separate products and repositories under PocketCode decision D-001. This document defines a candidate compatibility seam only.

## Purpose

Define the smallest useful set of shared semantics so RevDev (PC) and PocketCode (mobile) can report runs consistently without pretending their execution mechanisms or security boundaries are identical.

This matrix consolidates—not replaces—the existing [PocketCode Execution Contract](EXECUTION_CONTRACT.md), [Execution Loop Acceptance Criteria](EXECUTION_LOOP_ACCEPTANCE.md), and [RevDev + PocketCode Shared-Core Proposal](REVDEV_POCKETCODE_SHARED_CORE.md). It adds cross-product conformance cases, field provenance, and explicit acceptance gates.

## Core invariant

**A result describes what the trusted execution adapter can prove. A result never grants permission to execute.**

- The client, report parser, AI response, script output, or a field named `authorized` cannot authorize a run.
- Authorization is checked at the product's actual enforcement boundary, immediately before the executor is invoked.
- Shared schema compatibility does not imply shared privileges, isolation guarantees, implementation, or acceptance status.
- Every test remains NOT RUN until its evidence is captured from an implementation. A synthetic fixture validates contract logic only.

## 1. Portable result model

Candidate fields; this is a logical model, not a frozen wire schema.

| Field | Required? | Meaning / rule |
|---|---|---|
| `schema_version` | Yes | Version of the result contract; unknown optional fields must be tolerated |
| `run_id` | Yes once a run record exists | Stable ID; never reassign a result to another run |
| `request_disposition` | Yes | `accepted`, `rejected`, or `unknown`; acceptance is not execution |
| `execution_outcome` | Yes | `not_started`, `running`, `succeeded`, `program_failed`, `timed_out`, `cancelled`, `infrastructure_failed`, or `unknown` |
| `job_disposition` | Yes for asynchronous adapters | `not_submitted`, `queued`, `dispatched`, `terminal`, `cancel_requested`, `cancel_confirmed`, or `unknown`; this is operational lifecycle, not program success |
| `runtime` | Required if known | Allowlisted runtime and actual pinned version/image; unknown must remain explicit |
| `exit_code` | Conditional | Integer only when returned by a trusted execution source; otherwise null/unknown |
| `started_at`, `finished_at`, `duration_ms` | Conditional | Only trusted timestamps/measurement; never infer from browser timing |
| `stdout`, `stderr` | Conditional | Bounded text, with explicit per-stream truncation indicators and source provenance |
| `outputs[]` | Yes, can be empty | Safe display filename, byte size, optional scoped download handle; never expose worker paths |
| `error_category` | Conditional | Stable, non-sensitive category; do not return raw provider/control-plane diagnostics |
| `evidence_provenance` | Yes | Identifies trusted adapter observations vs script-reported/user-supplied claims |
| `uncertainty[]` | Yes, can be empty | Missing, ambiguous, simulated, truncated, or unverified evidence |
| `policy_decision` | Optional, non-authorizing | Diagnostic record of a decision; never treated as a credential or execution capability |
| `report_text` | Derived | Bounded, plain-text rendering from structured fields; not the source of truth |

### Separate three concepts

1. **Request disposition** answers whether the service accepted or rejected the request.
2. **Job disposition** answers where the asynchronous job is in the dispatch/cancellation lifecycle.
3. **Execution outcome** answers what the trusted adapter can establish about the program.

Do not compress these into a single `status` string. Example: `request_disposition=accepted`, `job_disposition=queued`, `execution_outcome=not_started` is not a successful run.

### Verdict mapping

| Verdict | Minimum evidence | Forbidden inference |
|---|---|---|
| `PASS` | Trusted terminal `succeeded` and exit code 0, with all required result evidence present | Never infer from HTTP 2xx, accepted/queued, a UI timer, script-printed “PASS”, or missing exit code |
| `FAIL` | Trusted terminal non-zero exit code or confirmed program/runtime failure | Do not label a provider outage or ambiguous result as a program failure |
| `INCOMPLETE` | Rejection, timeout, cancellation, infrastructure failure, missing/ambiguous terminal evidence, or missing evidence required to establish PASS/FAIL | Do not imply the process definitely stopped unless termination is confirmed |

A script may exit 0 and print a failed self-check. The process verdict may be PASS if runner evidence meets the rule, but the report must preserve the script-reported failure and must not claim the broader task is correct. A non-zero exit code overrides script-printed success text.

## 2. Cross-product conformance tests

The same abstract test vectors should be run against each adapter/formatter independently. Each product must record its own evidence and environment. Do not mark either product passed based on the other product's results.

| ID | Fixture / event | Expected contract result | Critical assertion | RevDev relevance | PocketCode relevance | Current status |
|---|---|---|---|---|---|---|
| SRC-001 | Confirmed terminal success, exit 0 | PASS / succeeded | Values match trusted fixture exactly | RelayRef reference can test formatting; product adapter unverified | Synthetic report logic only | NOT RUN as shared suite |
| SRC-002 | Confirmed non-zero exit | FAIL / program_failed | Preserve exit code and bounded stderr | Distinguish program result from adapter failure | LOOP-04, CASE-10 | NOT RUN as shared suite |
| SRC-003 | Trusted timeout event | INCOMPLETE / timed_out | Do not invent exit code; timeout source is trusted | PC/runtime timeout guard not tested | LOOP-05, CASE-04 | NOT RUN |
| SRC-004 | Cancel requested, termination unconfirmed | INCOMPLETE / unknown or cancel-pending job | Never claim cancelled until adapter confirms | No product runtime evidence | CASE-05 | NOT RUN |
| SRC-005 | Cancel confirmed by adapter | INCOMPLETE / cancelled | Preserve separate job and execution facts | No product runtime evidence | CASE-05 | NOT RUN |
| SRC-006 | Provider fails before trustworthy result | INCOMPLETE / infrastructure_failed | No fabricated stdout, exit code, or success | Recovery/adapter boundary not verified | LOOP-05, CASE-06 | NOT RUN |
| SRC-007 | Request rejected before dispatch | INCOMPLETE / rejected; job not submitted | Assert executor dispatch count is exactly zero | Maps to SAFE-01 enforcement boundary; not proven by static classifier | Security pre-dispatch gate | NOT RUN |
| SRC-008 | Accepted/queued but never terminal | INCOMPLETE / not_started or unknown | Never render PASS; preserve queue state and uncertainty | Queue stall/recovery concern; product evidence required | LOOP-02, CASE-11/13 | NOT RUN |
| SRC-009 | Exit code missing, no authoritative terminal outcome | INCOMPLETE / unknown | No default zero; no PASS | Reference report logic only | LOOP-03/05 | NOT RUN |
| SRC-010 | Script prints “PASS” but exits non-zero | FAIL | Actual trusted exit overrides script text | Prevent output-content confusion | CASE-10 | NOT RUN |
| SRC-011 | Exit 0 with script-reported failed check | Process PASS may be valid; check remains visibly FAIL | Do not claim task correctness from exit alone | Separate executor result from mission assertion | CASE-09 | NOT RUN |
| SRC-012 | stdout/stderr exceed configured caps | Verdict unchanged where outcome known; truncation explicit | Enforce bounds before report rendering | Bounded evidence handoff | LOOP-07, CASE-07 | NOT RUN |
| SRC-013 | Output filename/path is traversal or unsafe | Reject output; no unsafe handle | No host/worker path exposed | Filesystem guard boundary requires product test | CASE-14 | NOT RUN |
| SRC-014 | Result has unknown optional field / newer schema | Compatible consumer preserves known fields and safely ignores unknown optional field | No parse crash or silent field reinterpretation | Cross-version future integration | Contract compatibility | NOT RUN |
| SRC-015 | Result contains `authorized=true` but no valid guard approval | No authorization; executor call count 0 | Report fields cannot bypass guard | Core SAFE-01 requirement | Same policy rule at remote adapter | NOT RUN |
| SRC-016 | Duplicate request after ambiguous network response | Same idempotency key/body does not launch duplicate job | At most one dispatch; ambiguous status stays ambiguous | Mission duplication/recovery analogy only | PC-API-003/004, CASE-13 | NOT RUN |
| SRC-017 | Two runs complete out of start order | Each result stays bound to its run ID | No cross-run stdout/files/status | Mission/result identity concern | CASE-16 | NOT RUN |
| SRC-018 | Output or user content includes prompt injection/instruction-like text | Treated as untrusted data in report | No policy mutation or execution caused by content | AUTH-05/S-01 analogous control | Report/AI handoff security | NOT RUN |
| SRC-019 | Formatter sees simulated fixture | Clearly marks UI and copied text as simulated | Never emits a real-looking successful run claim | Test-fixture honesty | LOOP-02/08 | NOT RUN |
| SRC-020 | Readable result plus missing/inaccessible evidence source | Partial/unknown evidence is explicit | No silent omission or false complete claim | B-07/B-04 evidence distinctions | Partial infrastructure diagnostics | NOT RUN |

### Mandatory execution-boundary evidence

For SRC-007 and SRC-015, a classifier result or refusal message is insufficient. The test harness must instrument the actual executor boundary and record the invocation count and arguments. For each denied case, assert:

- executor invocation count = 0;
- no job was dispatched through an alternate path;
- no retry/background worker bypassed the denial;
- result is rejected/incomplete and does not claim execution occurred;
- logs contain enough non-secret evidence to identify the test and decision.

For an allowed control, assert that invocation occurs only after the intended exact-action authorization and guard checks. Use a fake/recording executor; do not run destructive or billable operations as test fixtures.

## 3. Field provenance and trust

Every displayed or copied fact belongs to one of these classes:

- **ADAPTER_OBSERVED:** exit code, terminal state, runtime version, measured duration, captured stdout/stderr, file metadata returned by trusted adapter.
- **SCRIPT_REPORTED:** test/check lines or status text printed by user code.
- **USER_SUPPLIED:** task title, user notes, declared expected output.
- **DERIVED:** verdict or formatted summary computed from adapter-observed fields under this contract.
- **UNKNOWN:** unavailable or ambiguous evidence.
- **SIMULATED:** fixture or demo data, never to be mistaken for an actual run.

Do not allow SCRIPT_REPORTED, USER_SUPPLIED, DERIVED report text, or UNKNOWN values to overwrite ADAPTER_OBSERVED facts. A derived verdict must be reproducible from the structured evidence and contract version.

## 4. Cross-product conformance record

Each implementation run of this matrix should attach a separate record with:

- product and adapter name/version;
- commit or source hash;
- test harness version/hash;
- host OS/runtime version;
- test ID and fixture hash;
- expected result and actual structured result;
- fake-executor call count and relevant redacted arguments for enforcement tests;
- process exit code and raw test output;
- PASS/FAIL/NOT RUN per case;
- skipped cases with reason;
- known limitations.

Never overwrite an earlier run record; new evidence is a new versioned record. Keep source identity separate from test outcome. A green suite is not product acceptance by itself.

## 5. Adoption gates

### Gate A — contract review (can be done now)

- [ ] Agree whether field names/enums are sufficient for both products.
- [ ] Add explicit schema version and backwards-compatibility rules.
- [ ] Resolve whether a terminal `unknown` outcome is allowed and how it maps to verdict.
- [ ] Ensure `policy_decision` is diagnostic only and cannot authorize execution.
- [ ] Keep the PC and mobile adapter/security claims separate.

### Gate B — deterministic formatter tests (no provider needed)

- [ ] Implement fixtures for SRC-001 through SRC-006 and SRC-009 through SRC-012.
- [ ] Verify unknown/missing values remain unknown; truncation is explicit.
- [ ] Verify simulated fixtures remain labeled in UI and copied report.
- [ ] Require nonzero test-process exit on any mandatory failure.

### Gate C — adapter and enforcement tests (implementation required)

- [ ] Recording/fake executor tests prove zero calls for rejected/unauthorized cases.
- [ ] Positive controls prove permitted calls happen only after exact authorization and guard.
- [ ] Idempotency, cancellation, timeout, output limits, ownership, and cleanup have independent tests.
- [ ] All mandatory failures make CI/test process exit nonzero.

### Gate D — product integration and acceptance (separate per product)

- [ ] RevDev: Windows/PowerShell 5.1/.NET, actual launch path, UI confirmation, recovery/publication and installed parity tested when PC is available.
- [ ] PocketCode: actual remote adapter, isolation/egress/quotas/termination/cleanup/access control tested only after a zero-cost path and explicit approval.
- [ ] Evidence source, source hash, environment, test output and unresolved limitations are recorded.
- [ ] Do not transfer a PASS from one product to the other.

## 6. Initial status ledger

| Work item | Current status | What would change it |
|---|---|---|
| PocketCode conceptual report contract | PROPOSED; documented | Contract review and deterministic tests |
| Cross-product schema compatibility | NOT ESTABLISHED | Both adapters pass same versioned fixture suite |
| RelayRef portable Python reference baseline | VERIFIED 293/293 on Python 3.13.5/Linux in 2026-10-28 review | New code/hash requires new run record |
| RelayRef scratch patch | FAIL 292/293; NOT ACCEPTED | Policy review of exact-code-pin delta and passing tests |
| RevDev real executor boundary | NOT RUN | Recording-executor tests against actual product launch/guard path |
| PocketCode real execution provider | NOT SELECTED / NOT RUN | Owner approval, zero-cost verification, isolation gates |
| Production acceptance for either product | NOT ESTABLISHED by this matrix | Separate product-specific acceptance evidence |

## References

- [PocketCode Execution Contract](EXECUTION_CONTRACT.md)
- [PocketCode Execution Loop Acceptance Criteria](EXECUTION_LOOP_ACCEPTANCE.md)
- [RevDev + PocketCode Shared-Core Proposal](REVDEV_POCKETCODE_SHARED_CORE.md)
- [RevDev + PocketCode Product Strategy Research](../RESEARCH/REVDEV_POCKETCODE_PRODUCT_STRATEGY_2026-10-28.md)
- [PocketCode Safety Requirements](../SECURITY.md)
- [RevDev RelayRef artifact intake and coverage map](https://github.com/marcelosofficial-ctrl/DevRelay-Missions/blob/review/revdev-acceptance-reconciliation-2026-10-27/resume/revdev/RELAYREF_ARTIFACT_INTAKE_AND_COVERAGE_MAP_2026-10-26.md)

**Non-authorization notice:** This matrix does not authorize execution, account creation, billing, deployment, publication, repository merge, product rename, remote PC pairing, or a change to the $0 budget.
