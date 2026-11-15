# PocketCode research addendum: version pins and replay ordering — 2026-11-15

## Why this addendum exists

This addendum sharpens the previous `EVIDENCE_BOUNDARY_REPLAY_DESIGN_2026-11-15.md` with a version-pinned standards correction and two explicit test requirements. It does not change product decisions, acceptance IDs, runtime choices, dependencies or authorization boundaries.

## Standards and source status

### CloudEvents

**VERIFIED:** the official CloudEvents repository release page lists `ce@v1.0.2` as the latest released Core specification; the project README distinguishes that release from the current working draft. The current `main` spec page is therefore not the correct normative citation for a released compatibility claim.

- Released spec: https://github.com/cloudevents/spec/releases/tag/ce%40v1.0.2
- Release index: https://github.com/cloudevents/spec/releases
- Project specification status: https://github.com/cloudevents/spec

**VERIFIED:** the opened working draft describes the `source + id` uniqueness rule and reuse of the same pair for redelivery. For PocketCode, cite the released v1.0.2 document directly before claiming conformance; the draft page is useful only as a research lead until checked against that tag.

**INFERRED:** stable source-scoped event identity is useful for duplicate detection. It is not a signature, producer authentication mechanism, authorization proof, payload-integrity proof or durable deduplication store.

### GitHub Actions

**VERIFIED:** GitHub's workflow documentation states that for a `push` event, `GITHUB_SHA` is the tip commit pushed to the ref. A workflow that checks out a fixed SHA is intentionally testing that fixed SHA, regardless of the event's triggering commit.

- Push event semantics: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows
- Workflow trigger lifecycle: https://docs.github.com/en/actions/concepts/workflows-and-actions/workflows

**VERIFIED:** the official `actions/checkout` release page surfaced v7.0.1 as latest in this research window; its repository states MIT licensing. This is metadata only. PocketCode's workflow remains untouched and no action upgrade is recommended or authorized by this addendum.

**INFERRED:** an eventual authorized exact-head lane should print and assert the checked-out SHA equals the event SHA before running tests. The historical pinned lane must report its own target SHA independently. This catches both an incorrect checkout ref and misleading green status association.

### Temporal retry guidance

**VERIFIED:** Temporal's official Activity documentation states that an Activity may execute multiple times under retry, and describes idempotency keys enforced by the external service. This matters because the worker cannot guarantee a remote side effect was not applied merely because its completion acknowledgement was lost.

- https://docs.temporal.io/activity-definition

**INFERRED:** PocketCode should model the same ambiguity without adopting Temporal: stable logical effect/outbox identity, repeatable send attempts, and receiver-side durable deduplication in any future adapter. Model-only tests do not establish durable exactly-once effects.

## Additions to the regression packet

Add these explicit cases to the previously committed packet:

1. **Released-spec identity test:** a duplicate event with the same source and ID and identical canonical bytes returns the original disposition; the same source and ID with changed canonical bytes is a conflict. Do not claim cryptographic producer authentication from this behavior.
2. **Out-of-order delivery test:** apply event N, then receive N+2 before N+1. The consumer must not advance its accepted sequence/version past the gap. It must either reject or buffer according to a declared contract; it must not silently apply N+2.
3. **Lost acknowledgement test:** publisher sends stable event E, receiver commits E, acknowledgement is lost, publisher retries E. Receiver applies E once and returns the original disposition.
4. **CI checkout assertion (proposal only):** exact-head job asserts `git rev-parse HEAD == GITHUB_SHA`, prints both values and fails before tests on mismatch. The historical lane asserts and prints its explicit pinned target SHA. No workflow change in this pass.

## Red-team corrections

- Do not cite CloudEvents `main` as the released v1.0.2 standard; use the tagged release.
- Do not conflate event deduplication with producer authentication or payload integrity.
- Do not equate idempotent consumption with ordered consumption. Sequence-gap handling needs its own explicit behavior.
- Do not equate a push-triggered workflow with testing the push commit if the workflow explicitly checks out a different SHA.

## Scope and evidence

No source/test/workflow/adapter/provider/device/PR/runtime/infrastructure changes were made. No tests were run. $0, provider neutrality, all existing IDs, P39 gate CLOSED, CASE-04 INCOMPLETE / `timed_out`, and report format 1 remain unchanged.

Research was opened 2026-11-15 from official CloudEvents, GitHub Actions, actions/checkout and Temporal sources. No source code was copied. The addendum is design guidance, not a product conformance claim.
