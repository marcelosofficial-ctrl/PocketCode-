# PocketCode — owner decision register

**Status:** Research proposals only; not canonical, not implemented, NOT RUN. Recommendations require owner review.

## D-01 — Confirmed execution limit verdict

Canonical `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` (main blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`) defines FAIL as confirmed program/runtime failure and INCOMPLETE as no confirmed success or failure.

The semantic and transition matrices currently lean toward INCOMPLETE for an enforced limit unless an owner chooses otherwise. That may conflict with the canonical definition when a trusted runtime confirms that the limit caused the run to terminate.

**Proposed interpretation:** limit-triggered termination confirmed by trusted runtime evidence -> FAIL verdict plus `LIMIT_EXCEEDED` disposition; collector-only truncation or ambiguous enforcement -> preserve the actual verdict or INCOMPLETE if terminal evidence is uncertain; renderer-only truncation never implies a runtime limit.

Tests: confirmed limit termination, collector truncation with exit zero, ambiguous limit evidence, display-only truncation. **OPEN; owner confirmation required.**

## D-02 — Provider failure without child exit evidence

Proposed default: user verdict INCOMPLETE; execution outcome UNKNOWN; disposition `PROVIDER_ERROR` only if the infrastructure cause is confirmed. Never invent an exit code. A separately confirmed nonzero child exit remains FAIL when cleanup is unknown. Test before-start failure, partial output then lost exit evidence, and nonzero exit with cleanup failure. **Proposed default.**

## D-03 — Is complete output mandatory for PASS?

Canonical PASS wording requires trusted completion and exit zero but does not explicitly make every output stream complete a universal gate. Proposed default: do not add that hidden requirement unless a chosen contract or acceptance case requires it. Keep COMPLETE, PARTIAL, UNAVAILABLE, EMPTY, RUNTIME_LIMIT, and DISPLAY_TRUNCATED distinct; required artifacts may still gate their specific case or release. **OPEN.**

## D-04 — Event identity scope

Define whether IDs are global, producer-scoped, or tenant/job/attempt-scoped. Proposed default: validate expected identity before reduction; same ID with changed immutable identity, sequence, kind, or canonical payload is a conflict. Test exact replay, changed attempt/job/tenant, changed payload, sequence collision, and nested-payload mutation. **OPEN.**

## D-05..D-08 — Other blocking choices

- **Policy binding:** require an atomic/conditional revision barrier or equivalent immutable attempt policy; read-then-act is insufficient.
- **Ambiguous acknowledgement:** reconcile the original identity; UNKNOWN lookup must not cause blind redispatch; in-memory state does not prove durable uniqueness.
- **Artifact release:** revalidate current authorization, identity, safe path/type/size, quarantine and exact stored-byte integrity immediately before returning bytes.
- **Report history:** issued reports remain immutable; later evidence appends a version using atomic persistence. In-memory history is not durable proof.

These require tests at the actual chosen boundary; fake tests alone cannot establish provider, storage, or device guarantees.

## Order and stop rule

Resolve D-01..D-04 before freezing verdict/event tests; D-05 before execution-boundary safety claims; D-06/D-08 before durable recovery/history claims; D-07 before artifact-release claims. Keep all proposals unapproved until the owner confirms them. Do not change canonical acceptance or implementation merely to make tests pass.

**Evidence:** research note only; no tests or implementation changes. No provider/runtime, account, billing, workload, merge, or deployment action. Canonical acceptance and PR #2/#3 remain unchanged.
