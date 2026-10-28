# AI Workflow Director — Pre-implementation Readiness Audit

**Date:** 2026-10-28  
**Status:** Static documentation review only. Not owner-approved, implemented, or tested.

## Conclusion

**Readiness: suitable for bounded implementation planning, not yet authorized for implementation.** The product semantics are mostly clear. A small number of exact contracts must be chosen before code can make deterministic claims. Other items can remain explicitly deferred.

The current MVP remains the authority for acceptance-case meanings. The conformance spec and fixture catalogue are elaborations, not permission to redefine the product.

## Focused audit: high-risk fixtures

### AWD-08 — Oversized context and omissions

**Finding:** The fixture explicitly supplies selected context, unselected context, and omission expectations. It therefore tests truthful disclosure and preservation, not automatic ranking or truncation.

**Keep:** Preserve constraints, acceptance criteria, and protected sentinels; identify omitted material; never claim the full source was included.

**Defer:** Automatic relevance ranking, summarization, and exact omission-notice wording.

**Risk if mishandled:** Implementing an unapproved summarizer would expand scope and could silently erase requirements.

### AWD-11 — Unsupported “tests passed” claim

**Finding:** The fixture includes the unsupported statement as an explicitly unverified entry in the proposed `unknowns` field and supplies no command, output, artifact, revision, or environment.

**Keep:** Do not promote the statement to `verified_facts`; reject or flag `DONE_VERIFIED` when concrete evidence is absent; preserve what is unknown.

**Open:** The final capsule schema may represent attributed claims differently. The current fixture representation is proposed and should not be mistaken for a production API.

**Risk if mishandled:** Treating a text claim as evidence would undermine the central evidence-integrity requirement.

### AWD-12 — Sensitive-looking content

**Finding:** The input contains a configured synthetic match and an unmatched synthetic sentinel. This can check configured redaction and honest limitations without using real secrets.

**Keep:** A configured match must be visibly handled; the warning must describe detection as best-effort; unmatched content must not be declared safe; packet construction must not transmit data.

**Open:** Pattern syntax, marker format, warning wording, and whether the initial MVP includes redaction at all require explicit scope/contract review.

**Risk if mishandled:** A simplistic detector can create false confidence. Do not advertise comprehensive secret detection.

### AWD-14 — User cancels sharing

**Finding:** The fixture supplies a fake `CANCELLED` result and is correctly scoped to the UI/share-adapter boundary, not the pure builder.

**Keep:** Cancellation is not success; retain the local packet; no automatic retry.

**Defer:** Real OS share-sheet behavior and device-level integration.

**Risk if mishandled:** Reporting “sent” after cancellation or losing the only local copy.

## Prioritized decision classes

| Priority | Item | Classification | Required before first local builder? |
|---|---|---|---|
| P0 | Evidence/status honesty for capsules | Existing MVP semantic requirement | Yes, as a semantic invariant |
| P0 | Protected evidence and explicit constraints remain intact | Existing MVP semantic requirement | Yes |
| P0 | No network/provider/execution/repository side effects in the builder | Existing scope boundary | Yes |
| P1 | Required goal/profile validation and optional-field normalization | Exact behavior partly open | Choose minimal behavior before implementation |
| P1 | Stable section order and empty-section omission | Existing MVP semantic requirement | Yes; exact copy/byte serialization can wait |
| P1 | Character-count convention | Exact numeric rule open | Only if numeric count ships in the first slice |
| P1 | Oversize-input behavior | Safety invariant exists; mechanics open | Confirm no silent/destructive truncation |
| P1 | Capsule invalid-status/error and unknown-field policy | Partly open | Needed only for the capsule import/export behavior included in v1 |
| P2 | Redaction pattern syntax and marker | Open implementation contract | Can defer if redaction is explicitly excluded from the first slice |
| P2 | Share adapter enum and platform integration | Open integration contract | No; defer real share integration |
| P3 | Automatic context ranking, provider capability freshness, paid APIs | Explicitly deferred | No |

## Minimal implementation scope proposal

If implementation is later authorized, the smallest useful offline slice is:

1. Accept a goal, selected text/context, constraints, acceptance criteria, and a profile.
2. Normalize ordinary input edges without modifying protected literals.
3. Produce a stable, previewable packet with MVP section order and omitted empty sections.
4. Build/validate a continuation capsule with provenance and evidence/status invariants.
5. Show a character count only after choosing its counting convention.
6. Keep preview/edit/copy separate from any share integration.
7. Have no provider calls, network access, code execution, repository writes, telemetry, or paid services.

Redaction and real sharing should be independently scoped; do not quietly fold them into the initial builder.

## Readiness checklist

- [x] AWD-01–AWD-16 are present in the canonical catalogue.
- [x] The decision register maps all 16 cases and eight proposed contract areas.
- [x] AWD-08, AWD-11, AWD-12, and AWD-14 have explicit boundaries and open dependencies.
- [x] Recommendations are labelled as proposals, not accepted decisions.
- [x] The current research process preserves the no-spend/no-provider-call boundary.
- [ ] Owner authorizes implementation.
- [ ] Minimum input, serialization, capsule, and count contracts are approved or deliberately deferred.
- [ ] Executable tests are authored only after implementation scope and authorization are explicit.

## Evidence status and next action

This report is a static reading of the current MVP, fixture catalogue, conformance spec, and decision register. It does not establish that the proposed behavior exists in application code. No code or executable tests were created or run; no AI evaluation occurred.

**Next action:** record this audit in the checkpoint, ensure the register is linked from the fixture catalogue, and recheck repository/PR status. After that, the next meaningful gate is explicit implementation authorization or a decision to continue research; no further documentation should be added merely to make the project appear more complete.
