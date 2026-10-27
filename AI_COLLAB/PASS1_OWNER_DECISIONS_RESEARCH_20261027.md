# PocketCode — Research and Rationale for Delegated Decisions

**Date:** 2026-10-27  
**Authority:** The owner explicitly delegated selection to ChatGPT after reviewing the decision packet.  
**Status:** Selected provider-neutral baseline. Numeric limits are provisional offline-test defaults, not production guarantees.  
**Safety boundary:** Strict $0; no provider, account, workload, spend, live execution, merge, or deployment.

## Decision summary

Adopt the six packet recommendations, with the clarifications below. PocketCode's goal is a trustworthy small-task verifier, not a generic cloud IDE. Prefer fail-closed behavior, minimal result exposure, replayable evidence, safe retries, and simple controls.

### 1. Artifacts and cleanup — SELECTED

Keep artifacts quarantined until cleanup is confirmed, integrity checks pass, and authenticated tenant/job authorization succeeds on every access. While cleanup is uncertain, expose status/evidence metadata only: no artifact bytes, live provider URLs, or raw stdout/stderr. Release output only after cleanup and the configured size/redaction gates. Recovery creates a new immutable report version; never rewrite a report already issued.

Why: an environment may still be running and artifacts may contain sensitive content. OWASP recommends app-generated storage names, size/type validation, authorization, and controlled retrieval. A digest verifies bytes against a recorded digest; it does not establish safety or prove execution.

### 2. Timeout/cancel ordering — SELECTED

Use a coordinator-owned append-only event sequence. Assign a monotonically increasing sequence when an event is accepted; atomically commit at most one terminal execution decision per attempt. Record the winning sequence. Later/conflicting events remain evidence and cannot silently replace the decision or cause duplicate cleanup. Provider timestamps are descriptive, not authoritative ordering. If sequence/evidence is ambiguous, disposition is INCOMPLETE or PROVIDER_ERROR, never PASS. No universal timeout-over-cancel priority: the first eligible event serialized by the coordinator wins. Cleanup itself must be idempotent.

Why: timestamps can be skewed, absent, or reflect provider-side event time rather than coordinator observation. The sequence makes decisions replayable based on what the service accepted, without claiming that arrival order equals physical occurrence order.

### 3. Idempotency and retention — SELECTED

Scope keys to the authenticated tenant. Same key + same server-computed fingerprint returns the existing job/report; same key + different fingerprint conflicts before allocation. Explicit rerun requires a new key. Retain the full record while the job/report is addressable. After deletion, retain a tenant-scoped one-way tombstone for a 30-day late-retry window; reject reuse during that window. Clients must never intentionally reuse keys; reruns always use new keys. After tombstone expiry, server-side detection of old-key reuse is no longer guaranteed.

Why: AWS guidance relates retention to resource lifetime plus a late-arrival interval and recommends rejecting parameter mismatch. Stripe replays the first result and rejects parameter mismatch, while allowing pruning after a documented interval. The 30-day tombstone is PocketCode's provisional MVP choice, not a vendor requirement; revisit it if privacy/deletion or retry evidence requires a different window.

### 4. Output caps and overflow — SELECTED

For offline tests only, use the existing illustrative profile: stdout 32 KiB, stderr 32 KiB, 64 KiB aggregate retained output, 64 KiB source, 256 KiB total inputs, 10-second wall time, 10 artifacts, 256 KiB per artifact, 1 MiB total artifacts. Count bytes, not characters. On any per-stream or aggregate output cap breach, stop retaining output, request termination, then drain/discard only to prevent pipe deadlock for at most 1 second. Mark LIMIT_EXCEEDED; never PASS. If termination/stream closure remains uncertain, preserve that uncertainty. The effective server policy sets limits; clients cannot raise them.

**Qualification:** these values are test defaults, not validated capacity or production promises. Review memory accounting, artifact needs, and end-to-end cleanup budget before live execution. Python's subprocess documentation warns that waiting without draining piped stdout/stderr can deadlock when pipe buffers fill, so bounded concurrent draining is required.

### 5. Canonical request fingerprint — SELECTED

Compute server-side over a versioned, unambiguous encoding of contract/schema version; authenticated tenant namespace; normalized allowlisted runtime and fixed entrypoint; exact decoded source bytes; canonical input names, normalized media types, and exact decoded input bytes; and effective server policy identity/version plus execution-affecting values. Normalize names to Unicode NFC, restrict initial input names to safe basenames, reject duplicates after normalization, and preserve input order unless the contract explicitly defines it as semantically irrelevant. Use length-prefixing or equivalent canonical encoding before SHA-256. Exclude timestamps, transport headers, retry counters, and client-supplied fingerprints. Keep the fingerprint internal by default.

Why: a retry token identifies an intent, not the payload alone. Source, input, runtime, schema, or effective security-policy changes must not accidentally reuse an old result.

### 6. Execution facts vs disposition — SELECTED

Keep separate:
- `execution_outcome`: NOT_STARTED, EXIT_ZERO, EXIT_NONZERO, TIMED_OUT, CANCELLED, LIMIT_EXCEEDED, UNKNOWN, plus source/evidence references.
- `cleanup_state`: PENDING, CONFIRMED, FAILED, UNKNOWN, with attempt history.
- `job_disposition`: REJECTED, PASS, FAILED, TIMED_OUT, CANCELLED, LIMIT_EXCEEDED, INCOMPLETE, PROVIDER_ERROR, derived by a versioned policy.

PASS requires authoritative zero exit, required policy revision confirmed before start, termination evidence, no prohibited timeout/cancel/limit/truncation, validated artifact manifest and hashes, correct tenant/job association, and confirmed cleanup. Missing/contradictory evidence or unknown termination/cleanup is never PASS. New evidence can produce a new report version and revised disposition, but cannot erase prior reports or silently rewrite the committed execution decision.

Why: a flat status cannot truthfully express “exit zero, cleanup failed.” Immutable observations plus a versioned derived conclusion are auditable and stop the formatter from inventing success.

## Additional constraints from research

- OWASP Logging guidance recommends excluding or masking tokens, passwords, keys, connection strings, source code, and sensitive personal data. Redaction is defense-in-depth, not a guarantee. Never inject service credentials into task environments.
- OWASP File Upload guidance supports allowlists, validation beyond client MIME declarations, generated storage names, limits, authorization, and controlled retrieval.
- Current Modal docs say outbound traffic is allowed by default; `block_network=True` is documented for a full outbound block. Documentation is not runtime proof and does not authorize a provider choice.
- E2B's current security page asks users to contact them before testing and says its terms require prior written consent. No E2B test is authorized here.

## Official sources reviewed 2026-10-27

1. AWS Builders' Library — https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/
2. Stripe idempotent requests — https://docs.stripe.com/api/idempotent_requests
3. Python subprocess — https://docs.python.org/3/library/subprocess.html
4. OWASP File Upload Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
5. OWASP Logging Cheat Sheet — https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
6. Modal networking and security — https://modal.com/docs/guide/sandbox-networking
7. E2B security and compliance — https://e2b.dev/security

## Not authorized by these decisions

Provider selection, accounts/credentials, billing changes, spend, live user-code execution, adversarial provider tests, production implementation, deployment, merge, public security/performance claims, or project rename. Fake-adapter tests can validate only provider-neutral orchestration logic under synthetic inputs.
