# AI Workflow Director — Deterministic Conformance Test Specification

**Date:** 2026-10-28  
**Status:** Proposed test design only; not implemented, executed, or accepted as frozen.  
**Scope:** Convert AWD-01 through AWD-16 in the MVP slice into deterministic fixture and assertion requirements for a future local-only packet/capsule builder.  
**Budget and safety:** $0; no provider/API calls, credentials, account connections, repository execution, merge, deployment, or privileged access.  
**Source of truth:** [MVP feature slice](AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md). If this document and the MVP slice conflict, record the conflict; do not silently treat either as implemented behavior.

## 1. What this specification does — and does not do

This document defines observable conformance assertions for a future implementation. It is a test design artifact, not test code, not a frozen public API, and not evidence that any case passes.

The MVP currently defines packet section order and six capsule statuses, but does not freeze exact profile wording, a serialization format for builder inputs, truncation-selection algorithm, sensitive-pattern configuration schema, or share-adapter interface. Tests should assert semantic invariants until those decisions are explicitly frozen. Do not use brittle whole-string snapshots to invent those missing decisions.

### Evidence labels

- **Required assertion:** must hold for the fixture to pass.
- **Forbidden behavior:** a failing condition if observed.
- **Open contract:** a decision the owner must freeze before a test can assert one exact representation.
- **Adapter-level:** belongs to a UI/share boundary, not the pure text builder.

## 2. Proposed minimal fixture envelope

This is a test-harness shape for discussion, not a production API contract:

```json
{
  "case_id": "AWD-01",
  "operation": "build_task_packet",
  "profile": "Lite",
  "fields": {
    "goal": "Return whether an integer is even.",
    "context": "",
    "constraints": "",
    "acceptance": "",
    "verification": ""
  },
  "environment": {
    "execution_available": false,
    "configured_sensitive_patterns": []
  }
}
```

The harness should pass structured values to a pure builder and capture its output without invoking an AI provider. Empty strings represent absent optional fields only in this proposed harness. The eventual input API may use null/missing values instead; that representation remains an open contract.

### Determinism baseline

For the same normalized input and configuration, the builder must produce the same output bytes/characters and the same reported character count. The builder must not read wall-clock time, random values, network state, provider state, or ambient clipboard contents to construct a packet. If any output contains an identifier, it must come from explicit input or a separately specified deterministic rule.

Character count must be calculated from the exact final preview string, using one documented counting convention. The convention (Unicode code points, UTF-16 code units, or another explicit definition) is an **open contract**; it must be selected before exact count assertions are frozen. In every case, the displayed unit must be “characters,” never “tokens” or predicted cost.

## 3. Cross-case invariants

Apply these checks to every relevant fixture:

1. **No invented facts:** no unsupplied paths, hashes, repository state, test results, runtime access, provider capability, or completed action.
2. **Exact evidence preservation:** paths, hashes, code, quoted evidence, and other protected spans are not silently rewritten.
3. **Optional-field omission:** absent/empty optional sections are omitted, not filled with placeholder prose.
4. **Stable order:** emitted packet sections follow the MVP order: Goal, Profile, Context, Constraints, Acceptance, Verification, Reply format. Empty optional sections may be omitted.
5. **Reviewability:** the exact final packet is available for preview/edit before the user transfers it.
6. **Truthful verification:** unavailable or unrun checks are described as unavailable/not run; they never become PASS.
7. **No quota evasion:** a request to evade provider limits is not operationalized; compliant checkpoint/resume alternatives may be offered.
8. **Capsule provenance:** a claim from an assistant/user/prior checkpoint is not promoted to an independently verified fact without supporting evidence.
9. **Deterministic behavior:** equivalent normalized input and same config yield the same result.
10. **No hidden side effects:** building a packet/capsule does not call a model, transfer data, execute code, change a repository, or write to a remote service.

## 4. Case-by-case conformance matrix

### AWD-01 — Lite profile and one-line goal

**Fixture input:** profile `Lite`; goal `Return whether an integer is even.`; all optional fields empty; execution unavailable.

**Required assertions**
- Output contains a Goal section with the supplied goal.
- Output identifies the Lite profile and includes a concise reply expectation.
- The packet does not force a multi-step planning template for this trivial task.
- The packet does not claim code was written or run.

**Forbidden behavior**
- Adding unrelated project context, fabricated acceptance criteria, or invented test results.
- Emitting empty Context, Constraints, Acceptance, or Verification sections solely to fill space.

**Useful boundary variant:** whitespace-only optional fields normalize to empty and are omitted.

### AWD-02 — Balanced profile with relevant context and acceptance criteria

**Fixture input:** profile `Balanced`; goal to update a supplied function; context contains one selected file snippet and an existing helper; acceptance contains two user-supplied criteria; unrelated history is present in a separate, explicitly unselected field.

**Required assertions**
- Includes the selected relevant snippet and both acceptance criteria without semantic loss.
- Instructs the recipient to inspect/reuse the supplied helper before inventing a replacement.
- Excludes explicitly unselected unrelated history.
- Preserves the distinction between supplied context and verified repository facts.

**Forbidden behavior**
- Dropping a criterion, inventing a file path, or claiming the helper exists outside the supplied context.

**Open contract:** the input envelope must distinguish selected from unselected context before this fixture is frozen.

### AWD-03 — Careful profile for a security-sensitive task

**Fixture input:** profile `Careful`; a clearly labelled toy security-sensitive goal; bounded scope and explicit acceptance checks.

**Required assertions**
- Includes the supplied scope and acceptance checks.
- Requests relevant failure-mode analysis and verification appropriate to the task.
- Does not imply that a security review, execution, or test has already happened.
- Preserves the user's permission constraints.

**Forbidden behavior**
- Expanding into unrelated files/systems, claiming a security guarantee, or treating the profile as authorization to perform actions.

**Useful boundary variant:** ambiguous acceptance input remains visibly ambiguous or is flagged for clarification; it is not silently invented.

### AWD-04 — Review only with a diff

**Fixture input:** profile `Review only`; a supplied toy diff.

**Required assertions**
- The packet clearly limits the task to analysis/review and prohibits implementation or rewriting for this task.
- Requests evidence-linked findings and distinguishes confirmed findings from potential issues and questions.
- Preserves the diff as supplied.

**Forbidden behavior**
- Asking the recipient to apply fixes, silently rewriting the diff, or presenting speculation as confirmed.

**Useful boundary variant:** even if the diff includes a suggested fix, Review only remains analysis-only unless the user changes the task.

### AWD-05 — Empty optional fields

**Fixture input:** valid profile and goal; every optional field absent, null, empty, or whitespace-only (once the representation is frozen).

**Required assertions**
- Required Goal and Profile information appears.
- Empty optional sections are omitted.
- No placeholders such as “No context provided” appear unless a future product decision explicitly requests them.

**Forbidden behavior**
- Literal `undefined`, `null`, empty headings, or boilerplate that falsely suggests user-supplied information.

**Open contract:** decide which input representations count as empty before locking serialization-level tests.

### AWD-06 — Exact path/hash preservation

**Fixture input:** include distinctive path and hash strings, for example `src/example file.py` and `0123456789abcdef0123456789abcdef01234567`, explicitly marked as user-supplied literals.

**Required assertions**
- Each protected literal appears exactly as supplied in the output wherever it is included.
- No path/hash is completed, normalized, case-changed, shortened, or synthesized.
- Any omitted protected literal is accounted for by an explicit user-visible omission notice if size handling applies.

**Forbidden behavior**
- Replacing the supplied values with plausible invented repository identifiers.

**Useful boundary variant:** include punctuation, spaces, uppercase characters, and a hash-like string that is deliberately not a real hash.

### AWD-07 — No test/runtime available

**Fixture input:** execution unavailable; task requests a check; no test results supplied.

**Required assertions**
- Verification is labelled unavailable/not run.
- No PASS, “tests passed,” “verified by execution,” or equivalent success claim is emitted.
- The reply format separates requested checks from checks actually performed.

**Forbidden behavior**
- Inventing a command result, test count, log, or runtime environment.

**Useful boundary variant:** user asks for “just say it passed”; truthful evidence constraints still win.

### AWD-08 — Oversized context and visible truncation

**Fixture input:** long context with labelled sections: relevant excerpt, irrelevant background, constraints, acceptance criteria, and a sentinel string near the end. Supply a fixed, preselected bounded excerpt for the deterministic core fixture.

**Required assertions**
- The output uses only the bounded selected excerpt for the core fixture.
- If any source material is omitted, the preview/packet identifies the omission in a visible, inspectable way.
- No constraint, acceptance criterion, or evidence label is silently removed.
- The output does not claim to contain the complete context when it does not.

**Forbidden behavior**
- Silent truncation, hidden removal of protected sections, or fabricated summaries presented as verbatim evidence.

**Open contract:** the automatic selection/truncation algorithm and exact notice syntax are not defined yet. Keep the first fixture deterministic by supplying the selected excerpt and expected omitted-item list explicitly; test automatic selection separately after its policy is frozen.

### AWD-09 — Request to bypass provider limits

**Fixture input:** goal asks the Director to bypass or evade a free-tier quota.

**Required assertions**
- Does not provide steps to evade quotas, rotate accounts, or circumvent provider controls.
- May offer a compliant alternative: save a compact checkpoint, reduce optional context, pause, or resume when access returns.
- Does not claim that the Director changes provider limits.

**Forbidden behavior**
- Operational quota-evasion instructions or claims of guaranteed limit avoidance.

### AWD-10 — Capsule with no executed checks

**Fixture input:** capsule reports work in progress or complete, but `checks_run` is empty/none and no concrete verification evidence exists.

**Required assertions**
- `DONE_VERIFIED` is rejected as an invalid status for the supplied evidence.
- The selected status reflects the actual work state: e.g. `IN_PROGRESS`, `BLOCKED`, or `DONE_UNVERIFIED`, as appropriate to the fixture.
- Missing checks and the next useful action remain visible.

**Forbidden behavior**
- Promoting completion assertion alone into verification evidence.

**Open contract:** exact validation response (error vs corrected capsule vs warning) must be chosen before asserting one exact serialized output.

### AWD-11 — Unsupported “tests passed” claim

**Fixture input:** a supplied assistant statement says tests passed but provides no command, output, artifact, revision, or environment details.

**Required assertions**
- Preserves the statement as an attributed, unverified claim.
- Does not put the claim in `verified_facts` as independently verified.
- Does not choose `DONE_VERIFIED`.
- Requests the missing evidence or uses `BLOCKED` if the required artifact/evidence is unavailable to proceed.

**Forbidden behavior**
- Inventing test commands, logs, paths, hashes, commit IDs, or environment details.

### AWD-12 — Sensitive-looking content

**Fixture input:** text contains a synthetic secret-like sentinel that matches a test-only configured detection pattern; include a second sensitive-looking value that does not match any configured pattern.

**Required assertions**
- Preview clearly indicates detected/redacted content according to the configured test pattern.
- Any redaction is visible to the user and the output accurately describes it as best-effort.
- The nonmatching sentinel demonstrates that detection is not claimed to be comprehensive.
- The system does not transmit content to a model/service during local packet construction.

**Forbidden behavior**
- Claiming perfect secret detection, silently changing protected evidence, or sending the content remotely.

**Open contract:** pattern configuration, redaction marker, and behavior for unmatched sensitive-looking strings must be frozen. Use synthetic values only; never put real credentials in fixtures.

### AWD-13 — Unknown provider capability

**Fixture input:** target provider capability is absent from the local verified capability catalogue or marked unknown/stale.

**Required assertions**
- Capability is labelled unknown/not verified.
- Falls back to ordinary user-driven copy/paste.
- Does not assert the provider supports a feature based on guesswork.

**Forbidden behavior**
- Fabricated support, silent API fallback, or a requirement for credentials.

**Useful boundary variant:** a known-but-old entry should show its last-verified date and stale status if that freshness behavior is adopted by the product contract.

### AWD-14 — User cancels sharing

**Fixture input:** a valid packet is previewed, then a test share adapter returns an explicit cancel result.

**Required assertions** (adapter-level)
- No successful transfer is claimed.
- The generated packet remains available locally for preview/copy/retry.
- The UI distinguishes cancellation from success and failure.

**Forbidden behavior**
- Reporting “shared/sent” on cancellation, discarding the only packet copy, or retrying in the background.

**Open contract:** the share adapter result enum and UI state transitions are not defined in the pure builder spec. Test them separately from deterministic packet text.

### AWD-15 — Character count units

**Fixture input:** a known final packet string, including a Unicode test string such as `café — 東京`.

**Required assertions**
- The displayed unit is characters.
- The count is derived from the exact final preview string, after edits and any explicit truncation.
- No label claims tokens, token savings, or predicted cost.

**Open contract:** define the counting convention before freezing exact numeric assertions. Include ASCII and non-ASCII cases so code-point vs UTF-16 behavior cannot differ silently.

**Forbidden behavior**
- Displaying the count as tokens, implying it predicts cost, or retaining a stale count after the preview changes.

### AWD-16 — Project constraints override profile

**Fixture input:** a profile requests a behavior that conflicts with an explicit project/user constraint; for example, a profile asks for broad edits while the constraint says “review only; do not modify files.”

**Required assertions**
- The packet preserves the explicit constraint and states that the profile cannot authorize the prohibited action.
- The output does not soften, omit, or override the constraint.
- If the conflict makes the task impossible, it asks for clarification or narrows to the permitted work.

**Forbidden behavior**
- Treating a profile as an authorization grant or prioritizing generic profile wording over explicit user/project rules.

## 5. Capsule validation matrix

These are cross-cutting deterministic cases, not additional AWD IDs. Use them to expand AWD-10 and AWD-11 into malformed-input tests.

| Capsule input condition | Required invariant | Forbidden result |
|---|---|---|
| Missing required field | Clear validation failure or explicitly defined safe default | Invented value silently inserted |
| Unknown status enum | Reject or surface validation error | Treat as `DONE_VERIFIED` |
| `DONE_VERIFIED` with no concrete evidence | Reject as inconsistent | Accepted as verified |
| Prior checkpoint claim without source evidence | Keep attribution/provenance | Promoted to independently verified fact |
| `READY_TO_VERIFY` but relevant artifact unavailable | Prefer `BLOCKED` where missing artifact prevents checking | Implied artifact exists |
| `checks_run` says “none” | No verification claim | Inferred PASS |
| Unknown fields | Preserve only if schema policy explicitly allows; otherwise surface them without silently treating as trusted | Quietly drop safety-relevant content |
| Secrets/full logs included | Warn and avoid unnecessary inclusion; best-effort detection only | Claim complete redaction |

**Open contract:** decide strict vs permissive handling of unknown fields and whether invalid capsules are rejected, warned, or normalized. Do not encode one policy into tests until agreed.

## 6. Suggested test-suite organization

A future implementation can keep this compact and local:

- `PacketBuilderTests`: AWD-01–09, AWD-13, AWD-15, AWD-16.
- `CapsuleValidatorTests`: AWD-10–11 plus the capsule validation matrix.
- `SensitiveContentTests`: AWD-12 with synthetic configured patterns.
- `ShareAdapterTests`: AWD-14, using a fake adapter that returns success/cancel/failure without launching a real share sheet.
- `DeterminismTests`: same normalized input/config twice; compare exact output and count.
- `ProtectedLiteralTests`: exact preservation for paths, hashes, code, and evidence spans.

Tests must be local and offline. No network mock may accidentally perform a real request. No test should depend on current time, real provider availability, a live account, or the actual operating-system share UI.

## 7. Exit criteria before implementation

Do not start implementation until these open contracts are explicitly decided or deliberately deferred with tests limited to semantic assertions:

1. Input envelope and representation of absent/empty values.
2. Exact profile wording and packet serialization/newline convention.
3. Character-count convention.
4. Oversized-context selection/truncation policy and omission notice.
5. Sensitive-pattern configuration and visible redaction behavior.
6. Capsule validation policy for unknown/missing fields and invalid status/evidence combinations.
7. Share adapter result contract and cancel-state behavior.
8. Which behaviors are guaranteed by the pure builder versus UI/adapter layers.

## 8. Recommended defaults to unblock a deterministic first slice

These are **recommendations for review, not accepted or frozen decisions**. They minimize hidden behavior, keep the first slice local/offline, and make tests stable.

| Open contract | Recommended v1 default | Why / test consequence |
|---|---|---|
| Input envelope and empty values | Typed object; require a non-empty goal and one of the four profile enum values. Treat missing, null, empty, and whitespace-only optional text as absent. Trim ordinary text fields at the edges only. Protected literals/evidence spans are copied byte-for-byte when included. Reject invalid required fields with a visible validation result. | Small input surface; avoids placeholder sections and invented values. Freeze a schema version before serialization tests. |
| Profile wording and packet serialization | Store the four profile instructions as versioned constants. Emit headings in the MVP-defined order, one blank line between non-empty sections, UTF-8/LF line endings, and no trailing whitespace. Do not snapshot entire profile text until the owner approves the wording. | Enables deterministic output while keeping profile copy reviewable. Semantic tests can precede exact snapshots. |
| Character count | Count Unicode code points in the exact final preview string, including spaces and line breaks; recompute after any user edit. Label only “characters.” | Consistent cross-platform semantics; avoids JavaScript UTF-16 surprises and token/cost claims. Document the chosen method in implementation tests. |
| Oversized context | Do not automatically summarize or silently truncate in v1. Preserve required constraints/acceptance/evidence. If a configured size limit is exceeded, show a warning and let the user edit/select excerpts; show an explicit omission notice for any user-approved removal. | Safest deterministic behavior without inventing a relevance-ranking algorithm. Automatic context selection can be a later feature with its own tests. |
| Sensitive patterns and redaction | Use a small, versioned local pattern list; redact only confirmed matches using a visible marker such as `[REDACTED:pattern-id]`. Show a best-effort warning on the preview. Never claim unmatched content is safe; never transmit from the builder. | Makes fixture results reproducible and avoids implying perfect detection. Pattern list and marker must be versioned test inputs. |
| Capsule invalid/unknown fields | Validate against a versioned schema. Missing required fields, unknown status enums, and impossible status/evidence combinations produce a visible validation error; do not silently coerce to `DONE_VERIFIED`. Preserve the original input locally for user review. Unknown extra fields trigger a warning and must not be silently discarded; v1 should reject export until the user resolves them. | Strict and auditable. If future forward-compatible preservation is needed, define an explicit extension field and test it separately. |
| Share adapter results | Keep sharing outside the pure builder. Adapter returns exactly one of `SUCCESS`, `CANCELLED`, `FAILED`, or `UNKNOWN`; report transfer only for explicit `SUCCESS`. Cancellation/failure/unknown keeps the packet available locally and never triggers background retry. | Prevents false “sent” claims and keeps UI behavior testable with a fake adapter. Confirm real OS behavior later on device. |
| Pure builder vs UI/adapter | Pure builder handles normalized inputs, packet/capsule text, validation, protected-literal preservation, redaction configured by explicit input, and deterministic character count. UI handles preview/edit/copy. Share adapter handles transfer and cancellation. No model call, code execution, repository mutation, or network access in the first slice. | Clear test seams; the 16 cases can be divided into pure-builder and adapter/UI suites. |

### Decision gate

Before implementation, either accept these defaults or explicitly replace individual rows. Until then, tests should enforce only the already stated semantic invariants and must not claim that the recommendations are frozen product behavior.

## 9. Current evidence status

- This specification was authored by reviewing the proposed MVP acceptance table and related project constraints.
- No implementation code was changed.
- No test code was created or executed.
- AWD-01 through AWD-16 remain **NOT RUN**.
- This document is not evidence that the requirements are complete, that the product is implemented, or that the tests pass.

**Next step:** review the eight open contracts in Section 7 against the existing MVP slice. Resolve only the decisions needed for a deterministic first implementation; keep the rest explicitly deferred rather than expanding scope.
