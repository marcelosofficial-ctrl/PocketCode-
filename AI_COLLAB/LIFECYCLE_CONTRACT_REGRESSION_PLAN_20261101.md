# Lifecycle Contract Regression Plan

**Date:** 2026-11-01  
**Purpose:** Turn the static review findings OBS-01 through OBS-06 and Claude's engineering review into a staged, evidence-layered regression plan.  
**Status:** Proposed test design only. No source or tests changed; all tests NOT RUN.

## 1. Scope and evidence pins

This plan targets the pure helper snapshot on branch `pocketcode-lifecycle-fingerprint-audit-2026-10-27`:

- `scripts/lifecycle_contract.py`, blob `316345341603848c4a86a6a82e533daa796c7695`.
- Existing test snapshot, blob `ef9a68de632be30c091afe57f0724fd030a513f9`.
- Owner decision register `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md`, blob `e67b2659cf2d71ef77d8e4619c91143e71062470`.

The helper snapshot is a pure provider-neutral model. Its module docstring expressly says it does not launch processes, contact providers, or claim runtime security. The lifecycle-fingerprint branch is separate and unmerged. This plan does not imply that its helper is integrated into main, PR #3, or a live host.

## 2. Priority and required proof layers

| Priority | Finding | First appropriate layer | Why |
|---|---|---|---|
| P0 | OBS-02 malformed negative flags can permit false PASS | Pure helper | PASS is the release-enabling disposition; strict input typing is locally testable. |
| P0 | OBS-01 missing terminal evidence conflated with provider error | Pure helper, then authenticated boundary | Deterministic state mapping is testable locally; source authenticity is not. |
| P1 | OBS-05 cross-attempt event contamination | Pure helper with expected attempt context, then coordinator integration | The reducer needs an explicit expected identity to compare against. |
| P1 | OBS-04 event producer authority | Pure helper schema tests, then authenticated adapter/boundary | Role labels can be validated locally; authenticity requires a trusted channel or signature. |
| P1 | OBS-06 truncation cause conflated with runtime limit | Pure helper | Distinct evidence causes and outcomes must not be collapsed. |
| P2 | OBS-03 streaming redaction carry and token-length gaps | Pure helper plus adversarial chunk tests | Deterministic byte-stream behavior is locally testable; redaction remains defense-in-depth only. |
| P1 at integration stage | Ambiguous dispatch and retry identity | Fake adapter, persistence/concurrency, provider | Pure decisions are insufficient to prove atomic reservation or provider idempotency. |
| P1 at integration stage | Exact-result persistence and queue liveness | Persistence and runtime/fake-queue tests | Restart durability and liveness are external to a pure helper. |

Priority is risk-oriented, not a claim that the corresponding test currently exists or fails in a running product.

## 3. Pure-helper regression matrix

### PC-LC-01: strict negative-polarity booleans (OBS-02)

For each field `contradictory_evidence`, `limit_violated`, and `output_truncated`, exercise values `0`, `None`, and `""` against an otherwise valid EXIT_ZERO/PASS candidate.

Expected: reject malformed input or return INCOMPLETE. It must never return PASS by interpreting a falsy non-boolean as False.

Also test `True`, `False`, `1`, and `"false"` explicitly. Literal booleans must have documented semantics; malformed truthy values must not become a PASS or be silently treated as valid evidence. Keep the existing positive-gate malformed-input tests, but do not mistake them for coverage of negative-polarity flags.

### PC-LC-02: terminal evidence state separation (OBS-01)

Inputs:
1. Empty event stream.
2. Nonterminal-only stream.
3. `provider_error` event with no source identity.
4. `provider_error` event with an untrusted or mismatched source.
5. Provider-boundary event with an authenticated producer identity and confirmed cause.

Expected: cases 1–4 do not become confirmed PROVIDER_ERROR. Only case 5 may support that disposition. The pure helper can test the state mapping when given a trusted/untrusted classification; a separate authenticated boundary test must establish how that classification is produced.

### PC-LC-03: event identity and attempt correlation (OBS-05)

Supply an expected context containing tenant, job, attempt, source and policy identity. Include:
- Correctly bound terminal event.
- Event from another tenant.
- Event from another job.
- Stale event from an earlier attempt.
- Mismatched source or policy identity.
- Reused event ID with changed payload or sequence.
- Duplicate identical event ID and payload.

Expected: mismatched events are rejected or quarantined and cannot win reduction. Identical duplicates are idempotent only within the same expected context. Conflicting identity reuse produces an explicit conflict/incomplete state. A pure helper cannot prove IDs are globally unique or unforgeable across restarts.

### PC-LC-04: producer-role contract (OBS-04)

For each event kind, test missing, unknown, wrong-role and allowed producer roles. Define the allowed observation owner for exit code, cleanup confirmation, provider failure, policy authorization and artifact digest.

Expected: a syntactically valid event kind from the wrong producer role cannot establish the corresponding fact. This checks role policy, not cryptographic or channel authenticity.

### PC-LC-05: truncation taxonomy (OBS-06)

Keep execution outcome, limit enforcement, termination evidence and presentation/collection truncation as separate inputs. Test:
- Display-only truncation plus independently confirmed EXIT_ZERO.
- Collector/retention cap plus independently confirmed EXIT_ZERO.
- Trusted runtime-enforced limit with confirmed termination.
- Runtime limit requested but termination unconfirmed.
- Truncation with no reliable terminal evidence.

Expected: display/collector truncation alone does not rewrite a confirmed EXIT_ZERO to LIMIT_EXCEEDED. LIMIT_EXCEEDED requires trusted evidence of an enforced limit under the contract. Unconfirmed termination remains INCOMPLETE/UNKNOWN rather than being inferred from truncation. A new model must not simply rename the existing boolean without defining the evidence producer and cause.

### PC-LC-06: redactor adversarial stream tests (OBS-03)

Test chunked inputs around:
- Separator lengths 755–763 after `Bearer`, with zero to seven token bytes present when the carry cutoff is crossed.
- Bearer-like token lengths 255, 256, 257, 300 and over 600.
- Alphanumeric-only and punctuation-containing tokens.
- Padding/delimiter cases, including equals, period and hyphen.
- Mixed-case scheme text.

Expected: no portion of the secret is emitted, including a suffix. Assert across every emitted chunk and final flush, not only against a full-token substring. Test chunk partitions that place each relevant boundary on either side of a feed call.

The source pattern is case-insensitive and caps the bearer token at 256 characters. The carry algorithm retains 768 bytes and only backs up the cutoff when a complete regex match crosses it. The separator threshold is chunk-dependent. This test is defense-in-depth, not a security guarantee; secret minimization and prevention remain primary.

## 4. Adapter, persistence and runtime matrix

### PC-AD-01: ambiguous dispatch with fake adapter

Script provider outcomes:
- Dispatch acknowledged.
- Dispatch accepted but acknowledgement lost.
- Lookup returns authoritative same-attempt result.
- Lookup returns UNKNOWN.
- Lookup returns a result for a different attempt.
- Same idempotency key with changed request fingerprint.

Expected: UNKNOWN lookup never causes a second dispatch while the first attempt remains unresolved. Authoritative same-attempt result is adopted. Changed fingerprint under the same key conflicts before dispatch. Different-attempt results cannot be adopted.

### PC-AD-02: repair retry identity and workspace exclusion

A repair retry changes task content and therefore creates a new task/attempt identity. Test both:
- New attempt with new idempotency key.
- New attempt reusing the old key with changed fingerprint.

Expected: the latter conflicts. A repair must not execute concurrently in a workspace whose previous dispatch remains unresolved. The workspace exclusion guarantee requires coordinator/integration tests, not only a pure helper.

### PC-DB-01: durable reservation and exact-result replay

Inject process crashes:
1. Before reservation.
2. After reservation but before dispatch.
3. After result computation but before publication.
4. During result write.
5. After durable publication but before acknowledgement.

Expected: reservation is atomic; torn/partial writes are detectable; restart resolves the same attempt; published result bytes are replayed exactly rather than recomputed; duplicate requests do not create a second execution. A later evidence update creates an explicit immutable version and does not silently rewrite an already-issued result.

### PC-RT-01: queue quarantine and liveness

With a fake queue first, then a real isolated runtime:
- Poison item ahead of valid work.
- Crash during quarantine.
- Repeated poison item.
- Later valid item after quarantine.
- Diagnostic record and source identity preserved.

Expected: poison item is quarantined without deletion of its evidence; later work proceeds; recovery is idempotent; poison item cannot retry forever. A pure classifier cannot prove queue liveness.

### PC-RT-02: termination and trusted observation

At the actual process/provider boundary, test:
- Exit code observed by supervisor.
- Cleanup observed independently of child output.
- Timeout/limit signal with confirmed termination.
- Timeout/limit signal with unconfirmed termination.
- Forged or wrong-channel terminal event.

Expected: terminal facts are attributed to the trusted observer; missing or unauthenticated evidence stays UNKNOWN/INCOMPLETE. No synthetic helper test is a substitute for this boundary evidence.

## 5. Crosswalk boundaries

These tests belong to the lifecycle helper/RevDev engineering workstream. They do not automatically become PocketCode LOOP/CASE tests, AWC fixtures, or P0-D canaries.

- AWC tests assistant behavior and remains PROPOSED_NOT_RUN.
- LOOP/CASE tests PocketCode execution acceptance and remains proposed/NOT RUN.
- P0-D tests RevDev publisher/mission obligations.
- The helper's unit tests establish only pure-model behavior.
- Fake adapter, persistence and runtime tests are separate evidence classes.

Do not merge the suites or claim cross-project coverage because two tests use similar words such as retry, handoff, truncation or report.

## 6. Exit criteria for claiming progress

A finding can be marked **pure-helper verified** only when:
1. The exact source and test commit are pinned.
2. The test is present in the committed suite.
3. The suite is actually executed in a named environment.
4. The complete result and skipped count are recorded.
5. The result is explicitly scoped to the helper.

A finding can be marked **adapter/persistence/runtime verified** only with the corresponding executed test and exact implementation/evidence producer pinned. Never promote a pure-helper PASS into a provider, durability, security, host or queue-liveness claim.

## 7. Current status

All rows in this plan are proposed. No source code, tests, canonical acceptance, provider adapter, persistence layer, runtime, queue, PR or main branch was changed. No test was run. PC state remains UNKNOWN. This document is a sequencing and acceptance-design artifact only.
