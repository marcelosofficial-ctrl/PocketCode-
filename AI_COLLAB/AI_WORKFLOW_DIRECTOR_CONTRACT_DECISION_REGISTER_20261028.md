# AI Workflow Director — Contract Reconciliation & Decision Register

**Date:** 2026-10-28  
**Status:** Analysis proposal; not owner-approved, frozen, implemented, or tested.  
**Purpose:** Compare the eight proposed conformance defaults with the existing MVP, identify already-defined behavior, and prevent recommendations from silently becoming requirements.  
**Authority:** The [MVP feature slice](AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md) retains authority for product intent and acceptance IDs. The [conformance specification](AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md) and [canonical fixture catalogue](AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES_20261028.md) elaborate test design; they do not override the MVP or authorize implementation.

## 1. Executive conclusion

The eight defaults are mostly compatible with the MVP, but they do not all have the same status.

The MVP already establishes semantic behavior: trim ordinary text at the edges; omit empty optional sections; preserve protected evidence; keep packet sections in a fixed order; disclose omissions; report verification honestly; preserve capsule provenance; require evidence for DONE_VERIFIED; make the packet previewable/editable before transfer; label size as characters rather than tokens/cost; and retain manual copy/paste as fallback.

Exact implementation choices remain open: missing/null/empty input representation, exact profile copy and newline serialization, Unicode counting convention, oversized-input mechanics, sensitive-pattern schema and marker, invalid/unknown capsule-field policy, share-adapter result interface, and precise component boundaries.

**Recommendation:** keep existing semantic requirements testable now. Before implementation, approve only the minimum local deterministic contract. Defer automatic context ranking, provider capability freshness, real share-sheet integration, and provider APIs unless they become essential.

## 2. Reconciliation matrix

| ID | Contract | MVP already says | Proposed default | Disposition |
|---|---|---|---|---|
| D-01 | Input and empty values | Trim ordinary text edges; omit empty optional fields; do not rewrite code, logs, paths, hashes, or quoted evidence. | Typed input; non-empty goal; one of four profiles; missing/null/empty/whitespace-only optional text is absent; protected spans remain exact. | Mostly aligned. Exact schema and invalid-input result remain open. |
| D-02 | Profile wording and serialization | Four profiles and their intent are described; section order is explicit; empty optional sections are omitted; preview/edit is required. | Versioned profile copy; MVP order; stable separators; LF line endings; no trailing whitespace. | Order and omission are already specified. Exact copy, encoding, and newline contract remain open. |
| D-03 | Character count | Show a rough size indicator labelled characters, not tokens or predicted cost. | Count Unicode code points in the exact preview, including whitespace/newlines; recompute after edits. | Label and preview basis align. Counting convention remains open until approved. |
| D-04 | Oversized context | Prefer small selected excerpts; disclose omissions; never silently truncate constraints, acceptance, or evidence labels. | No automatic destructive summarization/truncation in v1; user selects/edits; disclose approved omissions. | Safety invariant already specified. Automatic ranking and exact notice format are not. |
| D-05 | Sensitive patterns | Redact only known patterns; warn that detection is best-effort; never imply perfect detection. | Versioned local pattern list; visible marker such as [REDACTED:pattern-id]; no transmission by the builder. | Principle aligns. Pattern schema and marker remain open. |
| D-06 | Capsule validation | Proposed fields and six statuses exist; DONE_VERIFIED requires concrete evidence; unsupported claims cannot become verified facts. | Versioned schema; visible validation error for invalid status/evidence; preserve original; warn/reject export for unknown extra fields. | Evidence rules align. Unknown-field policy, exact error shape, and export behavior remain open. |
| D-07 | Sharing | User-initiated supported share target; cancellation is not success; local preview/copy fallback remains. | Adapter results SUCCESS, CANCELLED, FAILED, UNKNOWN; only SUCCESS permits a transfer-success claim; no automatic retries. | Semantic safety aligns. Exact interface and platform state transitions remain open. |
| D-08 | Builder/UI/adapter boundary | MVP separates packet building from preview/edit/copy/share journey; provider/API integration is out of scope. | Pure builder handles deterministic text/validation; UI previews/edits/copies; adapter transfers. | Direction aligns. Exact modules, class names, and APIs remain implementation choices. |

## 3. What can be asserted semantically now

These behaviors are supported by the current MVP and do not need exact whole-string snapshots:

1. Emit packet sections in MVP order and omit empty optional sections.
2. Preserve supplied acceptance criteria, constraints, paths, hashes, code, logs, and quoted evidence without silent rewriting.
3. Exclude explicitly unselected context.
4. Never invent repository state, runtime availability, provider capability, test output, or completed actions.
5. Distinguish requested, proposed, unavailable, unrun, claimed, and verified checks.
6. Never promote an unsupported “tests passed” claim into verified facts or DONE_VERIFIED.
7. Treat profiles as workflow hints, not permission grants; explicit user/project constraints take precedence.
8. Make the final packet reviewable/editable before user-initiated transfer.
9. Label size as characters, not tokens or predicted cost.
10. Do not operationalize quota evasion; offer compliant checkpoint/pause/resume alternatives.
11. Keep packet/capsule construction free of provider calls, network transfer, code execution, and repository mutation.
12. Keep cancellation distinct from transfer success and retain the packet locally.

These are test-design assertions only. No executable tests exist or have passed.

## 4. Fixture-by-fixture contract audit

| Fixture | Primary acceptance rule | Exact contract needed now? | Recommended treatment |
|---|---|---|---|
| AWD-01 | Lite goal, concise packet | No exact profile string | Semantic assertions |
| AWD-02 | Selected context and criteria preserved | Selected/unselected context must be explicit in test input | Proposed harness extension; semantic assertions |
| AWD-03 | Careful scope and honest verification | No exact profile string | Semantic assertions |
| AWD-04 | Review only does not authorize edits | No whole-packet snapshot | Semantic assertions |
| AWD-05 | Empty optionals omitted | Normalization rule needed before code | MVP supports omission; encoding remains open |
| AWD-06 | Protected literals remain exact | No, if fixture explicitly identifies protected spans | Exact equality assertions |
| AWD-07 | No runtime means no PASS | No | Semantic assertions |
| AWD-08 | Omission visible; no silent destructive truncation | Automatic selector not required | Use supplied selection/omission metadata; defer ranking |
| AWD-09 | No quota evasion | No provider-specific lookup | Semantic assertions |
| AWD-10 | No checks cannot mean DONE_VERIFIED | Status/evidence rule already defined | Semantic validator assertion; error wording open |
| AWD-11 | Unsupported test-success claim remains unverified | Provenance must be retained | Semantic assertion; capsule representation may evolve |
| AWD-12 | Best-effort configured redaction | Exact marker/config only for exact redaction assertion | Synthetic input; pattern schema open |
| AWD-13 | Unknown capability remains unknown; copy/paste fallback | No live provider catalogue | Offline semantic assertion |
| AWD-14 | Cancel is not success | Adapter/UI seam must be separate | Fake-adapter semantics; real platform behavior deferred |
| AWD-15 | Character label and live count | Numeric count requires a chosen convention | Test label/update first; exact numeric assertion blocked |
| AWD-16 | Explicit constraints beat profile hint | No assumed implementation interface | Semantic precedence assertion |

## 5. Minimum decisions before implementation

| Decision | Minimum proposed rule | Can detail be deferred? |
|---|---|---|
| Required input | Goal must contain non-whitespace text; profile must be one of Lite, Balanced, Careful, Review only; invalid input gets a visible validation result. | Exact error wording and production schema version can wait for implementation review. |
| Optional text | Missing/null/empty/whitespace-only ordinary text is absent; trim ordinary text edges only; never normalize protected spans. | Wire encoding can wait, but normalization must be consistent. |
| Packet serialization | MVP order, omit empty optional sections, stable separators, no trailing whitespace. | Exact profile wording and byte-level newline contract can wait for owner approval. |
| Character count | Count the exact visible preview and recompute after edits; label “characters.” | Choose the numeric convention before exact count assertions or implementation. |
| Oversized content | No automatic destructive summary/truncation in v1; user selects/edits; disclose omissions; never silently remove constraints, acceptance, or evidence. | Automatic relevance ranking is deferred. |
| Redaction | Only explicit configured local patterns; visibly mark matches; state best-effort limits; never claim unmatched content is safe. | Exact pattern syntax and marker can be selected when implementing redaction. |
| Capsule validation | DONE_VERIFIED requires concrete evidence; preserve unsupported claims; never silently coerce status. | Unknown-field policy and exact error/export behavior can be deferred only if no strict import/export API depends on them. |
| Sharing | User action only; distinguish cancellation/failure/unknown from success; retain local packet; no automatic retry. | Exact adapter enum and real OS integration can wait until sharing is scheduled. |
| Component boundary | Deterministic builder has no provider/network/execution/repository side effects. | Class names, file layout, and language are not product-contract decisions. |

**Minimum v1 recommendation:** defer automatic context selection, provider capability catalogue/freshness, real share-sheet integration, whole-packet snapshots before profile copy is approved, and provider APIs. They are not prerequisites for an offline builder/capsule prototype.

## 6. Explicitly deferred contracts

- Automatic relevance scoring, summarization, or context ranking.
- Provider capability discovery, account connections, persistent-instruction setup, or freshness guarantees.
- Real OS share-sheet behavior and provider-specific adapters.
- Paid APIs, model calls, billing, telemetry, or network execution.
- Exact whole-packet snapshots before profile copy is approved.
- PocketCode/RevDev field mapping before authoritative artifacts are compared.
- Unknown capsule-field forward compatibility beyond a documented v1 choice.

A deferred contract remains unknown; it is not silently decided by code or fixture text.

## 7. Implementation gate

Implementation remains blocked until explicitly authorized and the minimum decisions are recorded:

- [ ] Approve or replace D-01 input/normalization behavior.
- [ ] Approve or defer exact profile wording/serialization in D-02; semantic section-order checks can come first.
- [ ] Choose character-count convention before numeric assertions.
- [ ] Confirm no automatic destructive truncation in v1.
- [ ] Approve redaction pattern/marker contract before implementing redaction.
- [ ] Decide invalid-capsule and unknown-field behavior if strict import/export is included.
- [ ] Keep share behavior separate; defer real platform integration until explicitly scheduled.
- [ ] Confirm local-only, no provider/API calls, no repository mutation, and $0 remain the boundaries.

The owner may deliberately defer a decision and keep its tests semantic-only. Recommendations in this register are not accepted decisions.

## 8. Evidence status and next step

- This is a static reconciliation of the current MVP, conformance specification, and canonical fixtures.
- Original AWD IDs and meanings are unchanged.
- No implementation code or executable tests were created; no tests or AI evaluations were run.
- All AWD cases remain NOT RUN.

**Next pass:** audit this register for unsupported assumptions, validate its links and consistency against all 16 fixture records, then update the checkpoint. Do not ask for decisions until a real blocker is reached.
