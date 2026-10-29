# G-01..G-03 — recommended behavior and proof gates

**Status:** ChatGPT technical recommendation, not an owner decision or implementation authorization.  
**Date:** 2026-10-29  
**Scope:** PR #3 pure lifecycle helper only; no runtime/provider claim.

Companion: [G01_G03_PATCH_READY_TEST_SPEC_20261029.md](G01_G03_PATCH_READY_TEST_SPEC_20261029.md).

## Recommendation at a glance

| Gap | Recommended behavior | Why | Must not change |
|---|---|---|---|
| G-01 malformed `limit_violated` / `output_truncated` | Reject non-exact booleans with `TypeError` before deriving disposition | Invalid caller input is a contract violation, not evidence of a run outcome. Returning `INCOMPLETE` would blur malformed API usage with a real incomplete execution. | Valid bool behavior; contradiction precedence for valid inputs; timeout and exit mapping |
| G-02 output caps | Reject non-integers (including bool) with `TypeError`; reject integers <= 0 with `ValueError` | Separates type from range and catches errors at the constructor boundary. Python `bool` is a subclass of `int`, so it needs an explicit exclusion. | Byte caps, exact-cap behavior, overflow accounting, redaction and retention |
| G-03 required fingerprint fields | Reject any required field whose `strip()` is empty; preserve the original nonblank value and existing per-field normalization | Fixes blank identity fields without broadening canonicalization or changing meaningful existing fingerprint semantics. | Fingerprint version, nonblank raw contract/tenant/entrypoint values, existing runtime lower/strip behavior |

This is the recommended minimal scope, not a claim that the owner has accepted it. If project conventions require a single exception class, use the repo's established convention consistently and document it; do not silently coerce malformed values.

## Why not map malformed G-01 values to LIMIT_EXCEEDED or INCOMPLETE?

- `LIMIT_EXCEEDED` is a domain claim: the job exceeded a configured limit. A string like `"false"` is not such evidence.
- `INCOMPLETE` is a domain disposition for uncertainty/insufficient evidence. A caller passing the wrong type is a programming/schema validation error and should remain diagnosable as such.
- The pure helper's contract is explicitly typed with booleans. Rejecting malformed types keeps the helper deterministic and prevents truthiness coercion.
- If a future network boundary accepts arbitrary JSON, that boundary must validate and classify malformed payloads before calling the helper. That boundary behavior needs its own tests and is not proven by a pure-helper unit test.

## Minimal proposed code shape (illustrative, not applied)

```python
# derive_disposition: validate before any outcome branch
if type(limit_violated) is not bool or type(output_truncated) is not bool:
    raise TypeError("limit flags must be booleans")

# OutputBudget: validate each cap before storing it
for name, cap in (("per_stream_cap", per_stream_cap),
                  ("aggregate_cap", aggregate_cap)):
    if isinstance(cap, bool) or not isinstance(cap, int):
        raise TypeError(f"{name} must be an integer")
    if cap <= 0:
        raise ValueError(f"{name} must be positive")

# canonical_request_fingerprint: required strings must contain non-whitespace
required = (contract_version, tenant_id, runtime, entrypoint)
if not all(isinstance(value, str) and value.strip() for value in required):
    raise ValueError("contract, tenant, runtime, and entrypoint must be non-blank")
```

The snippet is an illustrative review aid, not a patch and not a full diff. Preserve the existing runtime normalization line `runtime.strip().lower()` and do not trim the other fields as part of this change.

## Regression tests to add

### G-01
For each flag independently, with all other PASS gates valid and `execution_outcome="EXIT_ZERO"`:
- `False` preserves PASS.
- `True` produces LIMIT_EXCEEDED.
- `None`, `0`, `1`, `""`, `"false"`, `[]`, `{}` raise TypeError.
- Add a valid-input contradiction-precedence regression if the existing suite does not already assert it in this exact helper configuration.

### G-02
For each cap independently:
- `1` and a normal positive integer construct successfully.
- `True`, `False`, `1.5`, `"10"`, `None` raise TypeError at construction.
- `0` and `-1` raise ValueError at construction.
- Keep existing exact-cap and one-byte-overflow tests unchanged; verify observed byte counts and retained bytes still match existing contract.

### G-03
For each of `contract_version`, `tenant_id`, `runtime`, `entrypoint` independently:
- empty string, ASCII spaces, tabs/newlines and mixed whitespace-only strings raise ValueError;
- a valid nonblank value continues to fingerprint;
- surrounding whitespace around a nonblank value is not newly rejected or normalized by this patch. Existing per-field behavior remains in place.

## Suggested bounded verification sequence (only if authorized and an environment is available)

1. Re-fetch the PR #3 source and test blobs; compare with the audit pins. If they changed, re-review first.
2. Add tests and implementation together on PR #3's branch only; keep PR #2 and the research branch free of source changes.
3. Run `python -m unittest discover -s scripts -p 'test_*.py' -v` from the repository root if Python and dependencies are available. Record exact command, interpreter version, exit code, and full summary. This command is suggested, not executed.
4. Run `git diff --check` and inspect the diff for unrelated changes. If the repo test layout makes the command inappropriate, determine the project's documented invocation instead of claiming a run.
5. Do not run GitHub Actions, provider workloads, external execution, or cloud resources as part of this pure-helper patch.
6. Record outcomes separately: source changed, unit tests passed/failed/not run, and integration proof not run. A green pure suite does not prove durable idempotency, trusted evidence, dispatch policy, cleanup, or artifact-release security.

## Provenance and state

- Exact source pins from the prior audit: `scripts/lifecycle_contract.py` blob `ba8d4d0b217c90513bed020e298029ef4e16f164`; `scripts/test_lifecycle_contract.py` blob `39db87d9f44f5e8474f33cff60136e529364199a`.
- Canonical acceptance on main remains pinned at `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338` and `PRODUCT/EXECUTION_CONTRACT.md` blob `3861e51ae4f9e45a263b677402f26c41b240959d`.
- No source/test file changed; no tests executed; no Actions/workloads launched. PR #2/#3 remain open drafts and unmerged. No provider/store/runtime selected.
