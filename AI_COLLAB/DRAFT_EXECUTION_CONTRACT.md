# Draft execution contract — provider-neutral and offline-testable

**Status:** Proposal for review; not an implementation or security proof.
**Prepared:** 2026-10-27
**Budget:** $0; no provider adapter or real execution backend is included.

## Purpose

Turn research constraints into a small contract that can be unit-tested without a provider, account, networked sandbox, or billable workload. It defines the seam between future orchestration, an execution adapter, and the report formatter. It does not select a provider or authorize execution.

## Design invariants

1. Parsing, policy validation, user authorization, execution, and reporting are separate stages.
2. Client input cannot assert that a job ran, passed, timed out, or produced a file. Only adapter evidence can establish execution facts.
3. Every job has a unique opaque ID and tenant owner. A user-controlled sandbox name is never an authorization token.
4. Requested controls and confirmed controls are separate. An unverified or plan-blocked mandatory control prevents execution.
5. Provider error, missing evidence, malformed result, timeout, cancellation, output cap, or cleanup uncertainty must never be promoted to PASS.
6. The default first-proof policy is no outbound network, no secrets, no arbitrary package installation, no persistence, and small allowlisted text/CSV inputs.
7. All sizes and durations are bounded server-side. Truncation is explicit and cannot be hidden by a formatter.
8. The fake adapter is a test double only. Passing its tests does not establish real isolation, network blocking, cleanup, or billing behavior.

## Proposed request shape

Illustrative JSON shape; exact schema/version remains to be reviewed:

    {
      "contract_version": "pc-run/0.1",
      "client_request_id": "opaque-id",
      "task": {
        "runtime": "python",
        "entrypoint": "main.py",
        "source": "...",
        "inputs": [
          {
            "name": "input.csv",
            "media_type": "text/csv",
            "content_base64": "..."
          }
        ]
      },
      "policy": {
        "network": "deny",
        "max_wall_seconds": 10,
        "max_source_bytes": 65536,
        "max_input_bytes": 262144,
        "max_stdout_bytes": 32768,
        "max_stderr_bytes": 32768,
        "max_artifact_count": 10,
        "max_artifact_bytes_each": 262144,
        "max_artifact_bytes_total": 1048576,
        "allow_packages": false,
        "persist_after_job": false
      }
    }

The example is not a public API commitment. Limit values are discussion defaults only and require capacity/security review before real execution.

### Request validation
- Reject unknown contract versions and unknown runtime/entrypoint policies.
- Reject absolute paths, traversal, duplicate names after normalization, NUL bytes, dangerous archive formats, oversized payloads, unsupported media types, and malformed encodings.
- Do not accept arbitrary shell command strings as entrypoint. Use a fixed launcher and validated arguments.
- Do not accept policy downgrades from client input; server policy defines maximum permissions and minimum security.
- Bind requests to an authenticated tenant server-side. Client request IDs are idempotency hints, not identity.
- Validate decoded byte counts after decoding; encoded length alone is insufficient.

## Proposed lifecycle

    RECEIVED
      -> REJECTED
      -> QUEUED
      -> STARTING
      -> RUNNING
      -> SUCCEEDED | FAILED | TIMED_OUT | CANCELLED | LIMIT_EXCEEDED | PROVIDER_ERROR
      -> CLEANUP_PENDING
      -> CLEANED | CLEANUP_FAILED

Rules:
- REJECTED has no execution evidence and no sandbox allocation.
- SUCCEEDED requires authoritative runner termination evidence, exit code zero, complete policy confirmation, no output-limit violation, and cleanup success. If future policy allows returning results before cleanup is confirmed, cleanup must remain a separate warning/state.
- FAILED requires execution evidence with nonzero exit or a defined runtime failure.
- TIMED_OUT requires observed timeout enforcement and termination; client-side timeout alone is insufficient.
- CANCELLED requires provider-confirmed termination; until then the job remains cancellation-pending.
- LIMIT_EXCEEDED identifies the limit and whether termination is confirmed.
- PROVIDER_ERROR must not imply the user code itself failed.
- CLEANUP_FAILED is an operations/security signal, not a successful completion.
- Terminal states are immutable. Corrections append an event rather than silently rewriting history.

## Proposed provider adapter contract

The orchestration layer should depend on a narrow interface equivalent to:

- capabilities(plan_context): each mandatory feature is supported, unsupported, not_verified, or blocked_by_plan, with evidence/source timestamp.
- prepare(job_id, tenant_id, validated_task, enforced_policy): creates a fresh boundary and returns confirmed configuration; no code runs before validation.
- execute(job_id, fixed_entrypoint): starts only validated task content and emits lifecycle events.
- collect(job_id): returns exit code, termination reason, bounded stdout/stderr and byte counts, artifact manifest, and provider-side resource observations.
- cancel(job_id): requests cancellation and reports whether process-tree termination is confirmed.
- cleanup(job_id): idempotently destroys the boundary and reports confirmed result.
- cost_observation(job_id): returns provider usage evidence where available; unknown cost is unknown, never zero.

This is conceptual, not a demand to build a generic framework before choosing a provider. Implement only what a concrete, approved proof requires.

## Report trust model

Keep these categories separate:
- **Request:** what the client asked for.
- **Policy decision:** what the server allowed and why.
- **Provider confirmation:** what the provider says it configured.
- **Observed execution:** start/end times, exit code, termination reason, byte counts, artifacts, cleanup status.
- **Formatter output:** concise human/AI-readable presentation derived from the above.

The formatter may summarize or redact but may not invent missing facts or upgrade status. PASS requires complete authoritative evidence and every required gate passing. Missing or contradictory evidence yields INCOMPLETE or PROVIDER_ERROR, never success.

Include contract version, job ID, status, exit code when known, termination reason, elapsed time with source, output truncation indicators, artifact manifest, policy confirmation, cleanup state, and unavailable evidence. Avoid including source or raw input by default.

## Offline test plan

These tests may use a deterministic fake adapter and synthetic data only. They require no execution provider.

### Request and policy
- Valid minimal Python/CSV request is accepted.
- Wrong version, unknown runtime, oversized input, invalid encoding, duplicate normalized names, traversal, absolute path, and archive input are rejected.
- Client attempts to enable network, packages, persistence, or exceed server limits are rejected or explicitly clamped; no silent privilege escalation.
- Missing tenant binding is rejected.
- Repeated client request IDs follow defined idempotency behavior without cross-tenant collision.

### Capability and state machine
- unsupported, not_verified, or blocked_by_plan for any mandatory control prevents preparation and execution.
- Provider preparation failure yields PROVIDER_ERROR and no execution claim.
- Invalid state transitions are rejected.
- Terminal state cannot be rewritten to SUCCEEDED.
- Client disconnect does not imply cancellation or success.
- Cancellation remains pending until termination evidence exists.
- Cleanup retries are idempotent; cleanup failure remains visible.

### Evidence and report
- Exit code zero without confirmed policy, termination, or cleanup cannot produce PASS.
- Nonzero exit, timeout, output cap, malformed provider response, missing exit code, contradictory timestamps, or missing artifact manifest cannot produce PASS.
- Stdout/stderr and artifacts are byte-bounded and truncation is explicit.
- Client-supplied fake status, elapsed time, provider ID, artifact URL, or exit code is ignored.
- Artifact names are normalized; traversal and cross-tenant fetches are rejected.
- HTML/JavaScript-like output is represented inertly and never rendered as trusted markup.
- Secret-shaped strings are redacted in reports; tests confirm no service secret is passed to the fake job environment.
- Unknown provider cost is shown as unknown, never $0.

### Limits of offline tests
They cannot prove kernel/microVM isolation, egress enforcement, metadata denial, CPU/memory/process quotas, real process-tree termination, billing behavior, provider cleanup, or deployed tenant isolation. These remain blocked until a provider, plan, budget, permissions where required, and adversarial test environment are approved.

## Open questions before implementation

1. Is the initial input limited to one source file plus CSV/text, or should a tiny multi-file bundle be allowed?
2. Which output artifact types are necessary for the first validated user task?
3. Should cleanup failure after a completed run expose results with a prominent warning, or withhold them until cleanup is confirmed?
4. What is the minimum retention policy and how is deletion confirmed?
5. Is authentication required before the first closed beta? Recommended: yes, unless a carefully reviewed abuse model justifies otherwise.
6. What owner-approved spend ceiling, if any, can replace the current $0 gate? Until explicitly changed, none.

## Decision

Keep this contract as a design proposal. The next safe implementation increment, if approved internally, is pure schema/state-machine/report-contract code plus fake-adapter unit tests. Do not add a provider SDK or execute user code yet.
