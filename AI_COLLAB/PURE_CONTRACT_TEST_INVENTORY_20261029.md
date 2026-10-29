# PocketCode — pure contract test inventory

**Date:** 2026-10-29  
**Status:** Test design only; NOT RUN. No implementation or test execution authorized by this document.  
**Branch:** pocketcode-ai-workflow-director-research-2026-10-28  
**Purpose:** Identify small, high-signal tests that can be prepared without waiting for provider/store selection, while explicitly isolating tests whose expected results depend on unresolved owner decisions. This is a test inventory, not an approved schema or acceptance amendment.

## Evidence and source boundaries

Pinned static audit inputs:
- PR #2 report helper `scripts/report_contract.py`, branch `chat-continuity-report-regressions-2026-10-26`, blob `e9d944a722c2fac5279952696528da72a7011af3`.
- PR #2 report tests `scripts/test_report_contract.py`, same branch, blob `39f3a3ef865ed55f333a1edc208096d99197d023`.
- PR #3 lifecycle helper `scripts/lifecycle_contract.py`, branch `pocketcode-pass0-audit-2026-10-26`, blob `ba8d4d0b217c90513bed020e298029ef4e16f164`.
- PR #3 lifecycle tests `scripts/test_lifecycle_contract.py`, same branch, blob `39db87d9f44f5e8474f33cff60136e529364199a`.
- Canonical acceptance remains `main:PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.

The listed hashes identify the audited snapshots, not necessarily the current PR heads. Re-fetch and pin the actual source before implementing tests. No current tests have been run in this pass. Pure tests cannot establish authenticated evidence, provider semantics, persistence atomicity, runtime isolation, enforced egress limits or real HTTP download behavior.

## Test readiness classes

- **A — Semantics stable enough to specify now:** strict input validation, deterministic canonicalization within an approved schema, defensive copying, and non-security-sensitive pure helpers. Expected behavior still must match the exact pinned implementation contract.
- **B — Pure test possible, expected result blocked:** verdict/disposition mapping whose expected value depends on D-01..D-03, or event replay/conflict behavior whose exact identity contract depends on D-04.
- **C — Not a pure-helper proof:** anything that needs the coordinator, authenticated producer, persistent store, provider, artifact store, HTTP boundary or device.
- **D — Separate-branch candidate only:** regression work on PR #2/#3 must not be mixed into the isolated research branch or represented as integrated. This inventory does not modify either PR.

## A. Candidate pure tests that can be specified without deciding D-01..D-04

These are test *specifications*. Before writing code, confirm the exact function signature and existing intended exception/return convention against the pinned source.

| Test ID | Target | Input / perturbation | Required property | Evidence class |
|---|---|---|---|---|
| PURE-01 | Boolean gate validation | Supply true, false, null, 0, 1, empty string, and string "false" for each boolean-only gate | Only the documented boolean values are accepted; malformed values never silently become trusted true/false evidence | UNIT |
| PURE-02 | Positive integer output budgets | Supply True, False, zero, negative, positive float, numeric string and positive integer | Reject invalid configuration deterministically before slicing/processing; no incidental TypeError during output capture | UNIT |
| PURE-03 | Required identity strings | Supply whitespace-only and empty contract version, tenant, runtime and entrypoint independently | Validation boundary rejects blank identity fields; normalization cannot turn accepted required values into empty canonical fields | UNIT |
| PURE-04 | Fingerprint determinism | Same valid semantic request with dictionary insertion order varied | Equal semantic input produces equal fingerprint under the pinned canonicalization rules | UNIT |
| PURE-05 | Fingerprint semantic sensitivity | Change one meaningful request field at a time, including runtime/image or contract/schema version when present | Meaningful execution-affecting changes alter the fingerprint; explicitly excluded transport-only fields do not alter it | UNIT; schema-dependent |
| PURE-06 | Fingerprint type/canonicalization boundary | Include unsupported/non-string keys or ambiguous scalar types where the public request schema would disallow them | Reject before hashing or canonicalize only according to a documented schema; never silently collapse distinct accepted requests | UNIT; schema-dependent |
| PURE-07 | Defensive snapshot | Accept nested dict/list payload, then mutate caller-owned nested values after acceptance | Accepted evidence snapshot remains unchanged | UNIT |
| PURE-08 | File-name normalization | Traversal, absolute paths, separators, NUL, trailing dot/space, reserved Windows names including COM¹/²/³ and LPT¹/²/³ | Reject unsafe names consistently on supported platforms; do not rely on the host OS alone | UNIT |
| PURE-09 | Expiry boundary | Compare just-before, exact-at, and just-after expiry instants with a fixed clock | Boundary behavior is deterministic and documented; repeated refresh cannot unexpectedly shorten a valid retention horizon | UNIT; helper contract-dependent |
| PURE-10 | Output accounting | Zero-byte chunks, exact cap, one byte over cap, repeated chunks, and cap reached across chunk boundaries | Never exceed configured capture cap; preserve distinct collection status; no accidental slicing exceptions | UNIT; truncation labels partly D-03 |
| PURE-11 | Report formatter source labeling | Script-printed PASS/FAIL/SKIP/WARN lines with forged JSON/status-looking text | Formatter preserves source attribution and does not claim to validate program-reported checks as trusted facts | UNIT |
| PURE-12 | Redaction boundary coverage | Tokens at maximum supported length, over-limit suffixes, newline-separated values and near-match strings | Test documents exactly what is redacted and what is not; no claim that regex redaction is primary secret protection | UNIT; source-level test only |

### Important constraints for this group

1. PURE-01 through PURE-12 are not all confirmed bugs; they are test targets motivated by the static audit. Mark each as existing coverage, missing coverage, or source change required only after checking the pinned tests.
2. Do not change a helper's API or silently choose an error policy merely to make a test easy. Where the intended validation result is not documented, record a decision-needed item.
3. Fingerprint equality is only meaningful relative to a frozen semantic request schema. It is not proof that a policy was actually applied at dispatch.
4. Filename unit tests do not prove archive extraction safety, filesystem race resistance, or cross-platform behavior without tests on those platforms.
5. Redaction tests do not make it safe to pass secrets into untrusted code.

## B. Pure tests whose expected result is blocked by owner decisions

| Test ID | Target | Required fixture | Why blocked | Unblocks when |
|---|---|---|---|---|
| SEM-01 | Runtime limit verdict | Trusted limit-caused termination versus unknown terminal evidence | D-01 and CASE-04's explicit timeout expectation must be reconciled | Owner confirms mapping while preserving CASE-04 |
| SEM-02 | Collection cap plus exit 0 | Independent EXIT_ZERO plus each stream collection state | D-01/D-03: case-specific required streams and partial-capture rule | Owner approves case/stream matrix |
| SEM-03 | Display-only truncation | Same terminal evidence with renderer-only output shortening | Expected invariant is clear, but shared projection tests must not accidentally merge it with runtime/collector limits | Test can be specified now; combine with final D-01 vocabulary before schema assertions |
| SEM-04 | Provider failure without exit | Provider error with no child terminal evidence; separately known infrastructure cause | D-02 determines exact disposition projection | Owner confirms proposed default |
| SEM-05 | Missing optional versus required output | EXIT_ZERO with stream states COMPLETE/PARTIAL/UNAVAILABLE/EMPTY | D-03 defines which streams gate each acceptance case | Owner approves per-case output requirements |
| SEM-06 | Event exact replay | Same source ID with same or changed immutable payload | D-04 determines replay namespace and immutable fields | Owner confirms replay identity rule |
| SEM-07 | Cross-attempt/cross-tenant event | Identical source event ID under a different tenant/job/attempt/source namespace | D-04 and auth/source schema determine exact scope tuple | Owner confirms tuple and source-binding rules |
| SEM-08 | Sequence collision | Two distinct event IDs share a coordinator sequence | D-04 must define stream scope and collision diagnostics | Owner confirms sequence namespace and conflict rule |
| SEM-09 | Late contradictory terminal event | EXIT_ZERO followed by timeout, and reverse order | Need final terminal evidence/replay semantics; expected conservative INCOMPLETE is consistent with current research but must be tested against the approved reducer contract | D-04 approved; retain contradiction fail-closed rule |
| SEM-10 | Immutable event snapshot | Nested payload mutation after acceptance | Unit immutability property can be tested now; integration-level persistence/reference behavior depends on D-04/D-08 | Unit-level part can proceed; durable history part waits on D-08 |

No row in this section authorizes a unilateral owner decision. Tests may be drafted with parametrized expected values, but do not label the suite conformant while a required expected value remains unset.

## C. Coordinator/fake-adapter tests — not pure helper tests

Use the companion `COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md`. The minimum suite must assert ordered calls and dispatch count, not only final return values.

| Test family | Must establish | Cannot establish |
|---|---|---|
| Attempt/tenant binding | Coordinator rejects evidence not bound to active tenant/job/attempt before reduction | Real producer authentication or durable binding unless integrated |
| Policy-at-dispatch | Stale revision prevents dispatch at the actual coordinator boundary | Real provider enforcement unless the selected boundary is tested |
| Ambiguous start acknowledgement | Same reservation/job/attempt is reconciled; UNKNOWN does not trigger a second start | Provider's authoritative "not created" semantics |
| Concurrent idempotency requests | Fake store sees expected reservation conflict/identity behavior | Cross-process atomicity or database durability |
| Report append retry | Lost acknowledgement can be retried with the same append identity | Persistent atomic commit/restart behavior |
| Artifact release denial | Coordinator denies stale/unknown/quarantined/mismatched manifest state | HTTP byte stream, auth revocation during transfer, exact bytes served |
| Contradictory/late evidence | Earlier evidence is preserved; no silent overwrite or PASS from a conflicting terminal result | Real provider event ordering/delivery guarantees |

## D. Evidence ladder and exit conditions

1. **Source preparation:** re-fetch exact branch heads and source/test blobs; label each test existing/missing/new.
2. **Pure unit layer:** implement only the approved validation/canonicalization properties. Record command, environment, exact output and fixture IDs.
3. **Pure projection layer:** do not finalize expected verdicts for SEM-01/02/04/05 until D-01..D-03 are approved. D-04 gates replay/conflict expectations.
4. **Coordinator/fake layer:** use ordered event logs, scripted failures and exact dispatch-count assertions; label as FAKE/COORDINATOR TESTED, never provider-verified.
5. **Persistence/provider/artifact/API layers:** remain blocked on selected, owner-approved boundaries and zero-cost approval; use their own evidence labels.
6. **Canonical acceptance:** map results to unchanged LOOP-01..14 and CASE-01..16. No helper test closes a canonical case by itself unless the case's full evidence requirement is actually met.

## E. Required test result record

For every executed test batch preserve:
- exact branch and commit SHA;
- source/test blob SHA;
- interpreter/runtime and OS;
- exact command;
- test IDs and expected versus actual result;
- stdout/stderr and exit code;
- skipped/blocked cases and reason;
- evidence class (UNIT, FAKE/COORDINATOR, PERSISTENCE, PROVIDER, ARTIFACT/API/HTTP, DEVICE);
- what the result does **not** prove.

Until this record exists, status is NOT RUN. Historical counts and a test file's existence are not current execution evidence.

## Next bounded task

Reconcile PURE-01..PURE-12 against the actual pinned tests, then produce a gap-only list: already covered, missing test, or requires a source change/owner decision. Do not modify PR #2/#3 from this research branch. Do not run Actions or remote workloads, enable billing, or select a provider/store/runtime as part of this task.

## Provenance

Static review and planning only. No tests or workloads run; no implementation, provider/store/runtime selection, account, billing, merge, or deployment performed. Canonical acceptance and PR #2/#3 remain untouched.
