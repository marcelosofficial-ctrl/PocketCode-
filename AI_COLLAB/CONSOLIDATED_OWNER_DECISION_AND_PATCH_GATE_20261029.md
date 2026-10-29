# PocketCode — consolidated owner decision and patch gate

**Date:** 2026-10-29  
**Status:** Review packet only. No owner decisions inferred; no implementation authorized by this document.  
**Research branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Purpose:** Consolidate the decisions and proposed pure-helper fixes so the owner can make a small number of explicit choices instead of revisiting scattered documents.

## Current boundary and source of truth

Canonical acceptance remains on `main`:
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`
- `PRODUCT/EXECUTION_CONTRACT.md`, blob `3861e51ae4f9e45a263b677402f26c41b240959d`

PR #2 (report-contract work) and PR #3 (lifecycle-contract work) are open drafts and remain unmerged. The pure helper pins used by the current static audit are:
- `scripts/lifecycle_contract.py`: `ba8d4d0b217c90513bed020e298029ef4e16f164`
- `scripts/test_lifecycle_contract.py`: `39db87d9f44f5e8474f33cff60136e529364199a`

Re-fetch those exact files immediately before an authorized source change. If their hashes differ, repeat the source review first. The repository has not been run in this pass; all test matrices below are proposed.

## Decision group A — semantic contract choices D-01..D-04

These decisions affect expected behavior and should be resolved before freezing verdict/reducer tests. Read the full context in [OWNER_DECISION_PACKET_D01_D04_20261029.md](OWNER_DECISION_PACKET_D01_D04_20261029.md).

| ID | Proposed default | What owner approval settles | What it does not prove |
|---|---|---|---|
| D-01 limit termination vs truncation | Preserve runtime-enforced limit, collector cap, and display truncation as different facts; retain canonical CASE-04 timeout expectation. | Which confirmed runtime limit causes FAIL versus INCOMPLETE, without contradicting canonical wording. | Actual runtime enforcement. |
| D-02 provider failure without child exit | INCOMPLETE; outcome UNKNOWN; no fabricated exit code; PROVIDER_ERROR only when cause confirmed. | Stable verdict/disposition projection when child terminal evidence is absent. | Provider adapter's actual terminal semantics. |
| D-03 output completeness | Required streams/artifacts gate only when the specific acceptance case requires them; optional diagnostics are not a universal gate. | Per-case output/partial-capture matrix. | Collector's real truncation/availability. |
| D-04 event replay | Coordinator-owned event identity; scoped source identity; exact replay requires immutable observations to match; conflict stays visible. | Semantic replay and contradiction rules; concrete schema remains boundary-dependent. | Authentication, durable replay history or cross-process uniqueness. |

## Decision group B — bounded pure-helper changes G-01..G-03, G-07..G-08

### G-01 — malformed limit flags
**Recommendation:** require exact booleans for `limit_violated` and `output_truncated`; raise `TypeError` for malformed values before deriving a disposition. Do not truthiness-coerce strings/numbers/collections, and do not reinterpret malformed caller input as evidence of LIMIT_EXCEEDED.

**Owner choice:** `APPROVE` strict type rejection / `CHANGE` specify alternative / `OPEN`.

### G-02 — OutputBudget caps
**Recommendation:** reject bool and non-integer cap values with `TypeError`; reject integer values <= 0 with `ValueError`. Validate at construction. Preserve exact-cap, overflow, observed-byte, retained-byte and truncation semantics.

**Owner choice:** `APPROVE` strict positive integers excluding bool / `CHANGE` specify supported numeric types / `OPEN`.

### G-03 — whitespace-only fingerprint fields
**Recommendation:** reject empty or whitespace-only `contract_version`, `tenant_id`, `runtime`, and `entrypoint`. Preserve existing behavior for nonblank values, including existing runtime normalization. Do not silently trim other fields or alter fingerprint version.

**Owner choice:** `APPROVE` reject blank-after-strip only / `CHANGE` specify canonicalization/version policy / `OPEN`.

### G-07 — Windows superscript device aliases
**Recommendation:** explicitly reject `COM¹/²/³` and `LPT¹/²/³`, with extension variants, while preserving current reserved-name and valid-name behavior.

**Owner choice:** `APPROVE` add rejection cases / `CHANGE` specify alternative portable-name policy / `OPEN`.

### G-08 — repeated tombstone additions
**Recommendation:** same tenant/key/same fingerprint is idempotent and cannot shorten expiry; same tenant/key/different fingerprint is a conflict that does not mutate the original record; tenant scope and exact expiry semantics remain explicit.

**Owner choice:** `APPROVE` stable tombstone identity and monotonic expiry / `CHANGE` specify whether and when key reuse during retention is allowed / `OPEN`.

Implementation-level edge cases, validation precedence, and expired-tombstone key reuse are analyzed in [G01_G08_EDGE_CASES_AND_PATCH_REVIEW_NOTES_20261029.md](G01_G08_EDGE_CASES_AND_PATCH_REVIEW_NOTES_20261029.md).

Detailed matrices:
- [G-01..G-03 test specification](G01_G03_PATCH_READY_TEST_SPEC_20261029.md)
- [G-01..G-03 behavior and proof gates](G01_G03_RECOMMENDED_BEHAVIOR_AND_PROOF_GATES_20261029.md)
- [G-07/G-08 test specification](G07_G08_PATCH_READY_TEST_SPEC_20261029.md)

## Suggested patch grouping and dependency order

Do not bundle all five gaps merely to reduce commit count. Their semantics differ.

1. **Patch A — G-02 only** after approval: strict OutputBudget constructor validation. This is the most self-contained change and need not wait for D-01..D-04 if it does not alter verdict semantics.
2. **Patch B — G-01** after approval: malformed flag validation. Valid bool mapping remains unchanged; coordinate with D-01 only if the existing valid limit mapping is itself being changed.
3. **Patch C — G-03** after approval: blank identity validation. Preserve current fingerprint bytes for all previously valid nonblank inputs.
4. **Patch D — G-07** after approval: portable reserved-name coverage.
5. **Patch E — G-08** after approval of key-reuse/retention semantics: tombstone repeat-add and conflict behavior.
6. Separately resolve D-01..D-04 before changing corresponding projection/reducer expectations. These semantic choices must not be smuggled into a validation patch.

This grouping is a proposal; an owner may choose a different grouping, but changes should remain reviewable and each gap should have its own test trace.

## Required proof gates for every authorized patch

- [ ] Explicit owner authorization for the exact gap(s) and branch.
- [ ] Fresh fetch of current PR #3 source/test hashes; re-review if changed.
- [ ] Tests added for valid and malformed boundaries before/alongside minimal source change.
- [ ] Exact local test command, interpreter version, output summary and exit code recorded; if unavailable, mark NOT RUN.
- [ ] Diff reviewed for unrelated changes; `git diff --check` or equivalent if environment available.
- [ ] Canonical LOOP/CASE files and PR #2 remain unchanged.
- [ ] No Actions, provider workload, cloud resources, billing, merge or deployment.
- [ ] Report source-change status, pure-unit-test status, and integration/security proof status separately.

A passing pure unit suite does not prove actual runtime enforcement, authenticated event provenance, policy-at-dispatch barriers, durable idempotency, append-only history, or safe artifact release. D-05 remains blocked until the real dispatch boundary enforces the applied policy revision.

## Copy-ready owner response

Fill only the decisions you want to settle. Leaving a line out means it remains open.

```text
D-01: APPROVE / CHANGE / OPEN — [limit termination mapping]
D-02: APPROVE / CHANGE / OPEN — [provider failure projection]
D-03: APPROVE / CHANGE / OPEN — [required streams / partial capture]
D-04: APPROVE / CHANGE / OPEN — [event replay / conflict]
G-01: APPROVE / CHANGE / OPEN — [strict bool validation]
G-02: APPROVE / CHANGE / OPEN — [positive integer caps excluding bool]
G-03: APPROVE / CHANGE / OPEN — [reject whitespace-only identity fields]
G-07: APPROVE / CHANGE / OPEN — [reject COM¹/²/³ and LPT¹/²/³]
G-08: APPROVE / CHANGE / OPEN — [stable tombstone fingerprint and non-shortening expiry]
Authorized branch: PR #3 only / other: [specify]
Authorized scope: [specific IDs]
Constraints: [optional]
```

Approval of a behavior is not automatically authorization to edit code; the owner should explicitly include the branch and scope. No response or checkbox state is implied by this document.

## State at creation

- Research/documentation branch only.
- No source or test changes; no tests run.
- PR #2 and PR #3 unchanged, open drafts and unmerged.
- Canonical acceptance unchanged.
- No provider, runtime or store selected.
- No Actions, workloads, account creation, billing, merge or deployment.
