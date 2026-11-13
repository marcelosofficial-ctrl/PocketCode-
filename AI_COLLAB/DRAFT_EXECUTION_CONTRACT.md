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
9. If a mandatory control (including network egress policy) is applied asynchronously, no user code may start until authoritative provider evidence confirms the exact required policy and revision are applied. Pending, failed, missing, stale, or mismatched policy evidence fails closed; a request acknowledgement or ETag alone is not proof of enforcement.

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
        "max_output_total_bytes": 65536,
        "max_output_drain_seconds": 1,
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

## Selected lifecycle and evidence model

The owner delegated the six decisions in [PASS1_OWNER_DECISION_PACKET_20261027.md](PASS1_OWNER_DECISION_PACKET_20261027.md) to ChatGPT; the selected baseline and rationale are recorded in [PASS1_OWNER_DECISIONS_RESEARCH_20261027.md](PASS1_OWNER_DECISIONS_RESEARCH_20261027.md). This is a provider-neutral contract direction, not an API freeze or permission to run user code.

Do not model execution and cleanup as one flat linear state. Keep these separate:

- `execution_outcome`: `NOT_STARTED | EXIT_ZERO | EXIT_NONZERO | TIMED_OUT | CANCELLED | LIMIT_EXCEEDED | UNKNOWN`, with evidence source and event references.
- `cleanup_state`: `PENDING | CONFIRMED | FAILED | UNKNOWN`, retaining every cleanup attempt.
- `job_disposition`: `REJECTED | PASS | FAILED | TIMED_OUT | CANCELLED | LIMIT_EXCEEDED | INCOMPLETE | PROVIDER_ERROR`, derived from immutable observations by a versioned policy.
- `report_version`: monotonically increasing; each issued report is immutable. Reconciliation or later cleanup evidence creates a new version and preserves the earlier one.

### Terminalization and event order

- Assign a monotonically increasing sequence when the coordinator accepts each event for a job attempt. Record the event and its sequence append-only.
- Atomically commit at most one terminal execution decision per attempt. The first eligible decision serialized by the coordinator wins; later evidence cannot silently replace it.
- Provider timestamps alone never reorder or overturn a committed decision. If authoritative order or evidence association is ambiguous, disposition is `INCOMPLETE` or `PROVIDER_ERROR`, never `PASS`.
- Deduplicate cleanup actions by attempt/action identity and make cleanup idempotent; an atomic status update alone does not guarantee exactly-once side effects.

### PASS and result-release gates

`PASS` requires authoritative zero exit, confirmation of the exact mandatory policy revision before execution, termination evidence, no prohibited timeout/cancel/limit/truncation, validated artifact manifest and hashes, correct tenant/job association, and confirmed cleanup. Missing or contradictory evidence never becomes PASS.

Artifacts remain quarantined until cleanup is confirmed and integrity plus per-request tenant/job authorization checks pass. While cleanup is uncertain, expose status/evidence metadata only—no artifact bytes, live provider URLs, or raw stdout/stderr. A later successful cleanup may produce a new report version; never overwrite a report already issued.

### Idempotency and request fingerprint

- Scope idempotency keys to the authenticated tenant.
- Same key and same server-computed canonical fingerprint returns the existing job/report reference; same key with a different fingerprint conflicts before allocation.
- Explicit reruns require a new key and create a distinct attempt.
- Retain idempotency records while the job/report is addressable. After deletion, retain a tenant-scoped one-way tombstone for 30 days and reject reuse during that window. Clients must never intentionally reuse a key; after tombstone expiry, server detection is not guaranteed.
- Compute a versioned server-side fingerprint over schema version, authenticated tenant namespace, normalized allowlisted runtime/fixed entrypoint, exact decoded source bytes, canonical input names and normalized media types plus exact decoded input bytes, and effective server policy identity/version and execution-affecting values. Exclude transport metadata, retry timestamps, and client-supplied fingerprints. Use unambiguous canonical encoding before hashing.

### Output limits

For offline tests only, use the provisional profile in the request example: 32 KiB retained stdout, 32 KiB retained stderr, 64 KiB aggregate retained output, and a separate 1-second drain/discard window after an output cap triggers termination. Count bytes, not characters. On either per-stream or aggregate cap breach, stop retaining output, request termination, and drain/discard only to avoid pipe deadlock within the separate bounded window. Mark `LIMIT_EXCEEDED`; never PASS. If termination or stream closure remains unconfirmed, preserve that uncertainty. These are not validated production limits; the server sets effective limits and clients cannot raise them.

## Proposed provider adapter contract

The orchestration layer should depend on a narrow interface equivalent to:

- capabilities(plan_context): each mandatory feature is supported, unsupported, not_verified, or blocked_by_plan, with evidence/source timestamp.
- prepare(job_id, tenant_id, validated_task, enforced_policy): creates a fresh boundary and returns provider-confirmed configuration and policy evidence. The orchestrator must verify that mandatory controls are actually applied to the intended revision before execute() is called; pending/failed/missing/mismatched evidence blocks execution.
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

## Remaining questions before any implementation or schema freeze

The six delegated lifecycle decisions are selected as a provider-neutral baseline; they are not live-execution authorization or a frozen public API. The following remain unresolved:

1. Is the first supported request one source file plus CSV/text, or a small multi-file bundle?
2. Which output artifact types are necessary for the first validated user task?
3. What retention/deletion behavior applies to full reports and artifacts, and what evidence confirms deletion? The selected 30-day idempotency tombstone is only a provisional offline-test default.
4. What exact provider evidence proves the required network policy revision is applied to the intended boundary immediately before execution?
5. What authentication/abuse controls are required before any closed beta?
6. What report fields distinguish observed CPU/RAM/process telemetry from provider-invoice cost, and how are ESTIMATED, FINAL, and UNAVAILABLE defined?
7. Which exact API field names and schema version should represent the selected execution outcome, cleanup state, evidence quality, and derived disposition?
8. What validated resource limits and cleanup budget are appropriate for a real provider? Current numeric limits are provisional offline-test defaults only.

The selected rules for artifact quarantine, coordinator-sequenced terminalization, tenant-scoped idempotency/fingerprinting, and bounded output overflow are recorded in the owner decision packet and research rationale. No provider, account, spend, live execution, production implementation, merge, or deployment is authorized.

## Decision

Keep this contract as a design proposal. The next safe implementation increment, if approved internally, is pure schema/state-machine/report-contract code plus fake-adapter unit tests. Do not add a provider SDK or execute user code yet.
