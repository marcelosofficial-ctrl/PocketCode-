# AI Workflow Director — Canonical Fixture Catalogue

**Date:** 2026-10-28  
**Status:** Proposed fixture data and observable outcomes; not frozen, implemented, or executed.  
**Purpose:** Turn AWD-01–AWD-16 into a compact, traceable catalogue of repeatable inputs and expected observations. This is a design artifact only.  
**Authority:** The [MVP feature slice](AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md) defines the acceptance-case meanings. The [conformance specification](AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md) defines the required invariants and open contracts. This catalogue elaborates those sources; it does not remap IDs or override them.

## 1. How to use this catalogue

- Fixture IDs **AWD-01 through AWD-16 retain their existing MVP meanings**.
- The JSON-like envelopes below are proposed test-harness inputs, **not a production API schema**. They intentionally make provenance and selected/unselected context explicit where the case needs them.
- “Expected observations” are semantic assertions unless an exact representation is already agreed. Do not invent whole-string snapshots, profile wording, validation error text, or UI copy while the relevant contract is open.
- Each case has one deterministic core input. Boundary variants are listed separately and should be added only when their relevant input/serialization contract is settled.
- These are human-authored fixtures, not implementation, automated tests, AI output, or passing results. All cases remain **NOT RUN**.
- Run the pure-builder cases offline with fixed configuration. Keep UI/share-adapter observations in their own test seam. No real provider, clipboard scraping, network, account, OS share sheet, repository mutation, or code execution is needed.

## 2. Shared proposed harness envelope

Fields are shown only when relevant; omitted optional values mean “not supplied” for this catalogue. The exact encoding of missing vs `null` vs empty remains an open contract until approved.

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
  "selected_context": [],
  "unselected_context": [],
  "environment": {
    "execution_available": false,
    "configured_sensitive_patterns": []
  }
}
```

For capsule cases, `operation` is `validate_capsule` and the input is a `capsule` object. For AWD-14, the packet builder and share adapter are separate phases; the adapter outcome is a controlled test input. For AWD-15, the final preview string is supplied directly. These are fixture conventions, not frozen API names.

## 3. Cross-case assertions

Apply each assertion wherever relevant:

1. **No invented facts:** no unsupplied paths, hashes, test results, runtime access, provider capability, or completed action.
2. **Literal preservation:** supplied protected paths, hashes, code, quoted evidence, and acceptance criteria remain exact when included.
3. **Optional omission:** absent/empty optional sections do not produce empty headings or invented placeholder prose.
4. **Packet order:** Goal → Profile → Context → Constraints → Acceptance → Verification → Reply format; omit empty optional sections without reordering the others.
5. **Truthful status:** requested, claimed, unavailable, and actually performed checks remain distinct. Unrun checks never become PASS.
6. **Reviewability:** the final packet is previewable/editable before user-initiated transfer.
7. **No quota evasion:** no operational bypass, account rotation, or circumvention instructions.
8. **Capsule provenance:** attributed user/AI/prior-checkpoint claims are not promoted to independently verified facts without evidence.
9. **Determinism:** same normalized input and explicit configuration produce the same output and count.
10. **No hidden side effects:** construction/validation makes no provider call, transfer, network request, code execution, remote write, or repository mutation.

## 4. Canonical fixture records

### AWD-01 — Lite profile and one-line goal

**Trace:** MVP AWD-01; conformance spec §4 AWD-01.  
**Layer:** Pure packet builder.

**Input**
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
  "environment": {"execution_available": false}
}
```

**Expected observations**
- A Goal section includes the exact supplied goal; Profile identifies Lite.
- Reply expectations are concise; no forced multi-step plan for this trivial task.
- Empty optional sections are omitted.
- No statement implies code was written or run.

**Must not occur:** invented project context, acceptance criteria, test results, or empty optional headings.  
**Pass when:** all observations hold and no prohibited behavior appears.  
**Open dependencies:** exact profile wording and line serialization; test semantically until approved.

### AWD-02 — Balanced profile, selected context, acceptance criteria

**Trace:** MVP AWD-02; conformance spec §4 AWD-02.  
**Layer:** Pure packet builder; selected-context envelope is a proposed harness extension.

**Input**
```json
{
  "case_id": "AWD-02",
  "operation": "build_task_packet",
  "profile": "Balanced",
  "fields": {
    "goal": "Update the supplied function to reject an empty name.",
    "constraints": "Keep the change small.",
    "acceptance": "A1: Empty names are rejected.\nA2: Existing valid names still work."
  },
  "selected_context": [
    {
      "label": "user-supplied snippet",
      "path_literal": "src/example file.py",
      "text": "def greet(name):\n    return 'Hello ' + name"
    },
    {
      "label": "user-supplied existing helper",
      "text": "The supplied context says helper normalize_name(value) already exists."
    }
  ],
  "unselected_context": [
    {"label": "unrelated history", "text": "A previous unrelated project used Rust."}
  ],
  "environment": {"execution_available": false}
}
```

**Expected observations**
- Both acceptance criteria appear without semantic loss.
- The selected snippet/helper context is included and the packet asks the recipient to inspect/reuse the supplied helper before inventing a replacement.
- The explicitly unselected Rust history is absent.
- The helper is described as supplied context, not independently verified repository state.

**Must not occur:** dropping A1/A2, inventing another path, claiming the helper was inspected in a repository, or including unselected history.  
**Pass when:** all four observations hold and prohibited behavior is absent.  
**Open dependencies:** exact selected/unselected context schema; the harness above is proposed, not a product contract.

### AWD-03 — Careful profile, security-sensitive task

**Trace:** MVP AWD-03; conformance spec §4 AWD-03.  
**Layer:** Pure packet builder.

**Input**
```json
{
  "case_id": "AWD-03",
  "operation": "build_task_packet",
  "profile": "Careful",
  "fields": {
    "goal": "Review a toy login handler for unsafe handling of failed authentication.",
    "context": "Toy example only: no real users, services, credentials, or production system.",
    "constraints": "Review this function only. Do not access external systems or modify files.",
    "acceptance": "Identify relevant failure modes; cite the supplied code lines; distinguish confirmed issues from questions.",
    "verification": "No runtime or tests are available."
  },
  "environment": {"execution_available": false}
}
```

**Expected observations**
- Scope, constraints, and all acceptance checks are preserved.
- Packet requests relevant failure-mode analysis and appropriate verification, while saying runtime/tests are unavailable.
- No claim says a security review or test has already occurred.
- Careful profile does not authorize broader access/actions.

**Must not occur:** unrelated system expansion, security guarantees, invented findings/results, or softened permissions.  
**Pass when:** scope and acceptance remain intact, verification is truthful, and no forbidden behavior occurs.  
**Open dependencies:** exact Careful wording; do not snapshot unapproved profile text.

### AWD-04 — Review only with supplied diff

**Trace:** MVP AWD-04; conformance spec §4 AWD-04.  
**Layer:** Pure packet builder.

**Input**
```json
{
  "case_id": "AWD-04",
  "operation": "build_task_packet",
  "profile": "Review only",
  "fields": {
    "goal": "Review this toy diff for correctness risks.",
    "context": "Supplied diff follows; it is evidence to review, not permission to edit.",
    "constraints": "Do not implement, rewrite, or apply fixes.",
    "acceptance": "Separate confirmed findings, potential issues, evidence, and questions."
  },
  "selected_context": [
    {"label": "toy diff", "text": "--- a/example.py\n+++ b/example.py\n@@\n- return value\n+ return value.strip()"}
  ]
}
```

**Expected observations**
- Packet limits the task to review and explicitly prohibits implementation/rewrite.
- Requests evidence-linked findings separated by certainty.
- The diff text is preserved exactly when included.

**Must not occur:** asking the recipient to apply a fix, silently altering the diff, or describing a potential issue as confirmed.  
**Pass when:** review-only scope, evidence discipline, and literal preservation hold.  
**Open dependencies:** none beyond packet serialization/profile wording; exact whole-packet snapshot remains deferred.

### AWD-05 — Empty optional fields

**Trace:** MVP AWD-05; conformance spec §4 AWD-05.  
**Layer:** Pure packet builder.

**Input**
```json
{
  "case_id": "AWD-05",
  "operation": "build_task_packet",
  "profile": "Balanced",
  "fields": {
    "goal": "Explain what this function returns.",
    "context": "   ",
    "constraints": "",
    "acceptance": null,
    "verification": null
  },
  "environment": {"execution_available": false}
}
```

**Expected observations**
- Goal and Profile appear.
- Context, Constraints, Acceptance, and Verification sections are omitted when their values are treated as absent.
- No placeholder prose claims information was supplied.

**Must not occur:** literal `undefined`/`null`, empty headings, or boilerplate such as “No context provided” unless a later explicit product decision adopts it.  
**Pass when:** required content appears and absent fields create no section or false implication.  
**Open dependencies:** missing/null/empty/whitespace normalization is recommended but not frozen; use as proposed fixture only.

### AWD-06 — Exact path/hash preservation

**Trace:** MVP AWD-06; conformance spec §4 AWD-06.  
**Layer:** Pure packet builder / protected-literal handling.

**Input**
```json
{
  "case_id": "AWD-06",
  "operation": "build_task_packet",
  "profile": "Balanced",
  "fields": {
    "goal": "Describe the supplied artifact without changing its identifiers.",
    "context": "The following strings are user-supplied literals; do not infer that they exist.",
    "constraints": "Preserve protected literals exactly."
  },
  "selected_context": [
    {"label": "protected path", "literal": "src/example file.py"},
    {"label": "protected hash-like string", "literal": "0123456789abcdef0123456789abcdef01234567"},
    {"label": "protected mixed-case literal", "literal": "Path With SPACE/CaseSensitive.TXT"}
  ]
}
```

**Expected observations**
- Each included protected literal matches its input exactly, including case, spaces, punctuation, and length.
- No literal is completed, shortened, normalized, or treated as proof that an artifact exists.
- If an explicit size-handling choice omits one, a visible omission notice names the omission.

**Must not occur:** fabricated identifiers or silent rewriting.  
**Pass when:** every included literal is an exact match and every omission is accounted for.  
**Open dependencies:** only size-limit/omission representation if the product later imposes one.

### AWD-07 — No test/runtime available

**Trace:** MVP AWD-07; conformance spec §4 AWD-07.  
**Layer:** Pure packet builder.

**Input**
```json
{
  "case_id": "AWD-07",
  "operation": "build_task_packet",
  "profile": "Balanced",
  "fields": {
    "goal": "Check whether the change passes its tests.",
    "context": "No source tree, command output, or test result has been supplied.",
    "verification": "Requested check: run the relevant tests if a runtime is available."
  },
  "environment": {"execution_available": false}
}
```

**Expected observations**
- Verification says unavailable/not run and distinguishes requested checks from performed checks.
- No PASS, “tests passed,” or equivalent execution-success claim appears.

**Must not occur:** invented commands, counts, logs, runtime, or successful result.  
**Pass when:** the absence of evidence is explicit and no success is asserted.  
**Open dependencies:** exact reply wording only.

### AWD-08 — Oversized context with explicit omission

**Trace:** MVP AWD-08; conformance spec §4 AWD-08.  
**Layer:** Pure packet builder / preview contract. Core fixture uses a preselected excerpt; it does not test an unfrozen auto-selection algorithm.

**Input**
```json
{
  "case_id": "AWD-08",
  "operation": "build_task_packet",
  "profile": "Balanced",
  "fields": {
    "goal": "Diagnose the supplied toy function.",
    "constraints": "Do not remove or weaken constraints.",
    "acceptance": "A1: Preserve the final sentinel. A2: Keep all acceptance criteria."
  },
  "selected_context": [
    {"label": "selected excerpt", "text": "def parse_count(value):\n    return int(value)"},
    {"label": "required sentinel", "text": "END_SENTINEL_KEEP_7Q"}
  ],
  "unselected_context": [
    {"label": "omitted background", "text": "Background paragraph A; irrelevant for this task."},
    {"label": "omitted background", "text": "Background paragraph B; also irrelevant."}
  ],
  "omission_expectation": {
    "omitted_labels": ["omitted background", "omitted background"],
    "notice_required": true
  }
}
```

**Expected observations**
- Core packet uses the selected excerpt, preserves both acceptance criteria and the sentinel, and visibly discloses omitted background.
- It does not claim all source context was included.
- No silent loss of constraints, acceptance, or evidence.

**Must not occur:** invisible truncation, fabricated “verbatim” summary, or automatic removal of protected material.  
**Pass when:** protected content remains, omitted items are visibly accounted for, and completeness is represented honestly.  
**Open dependencies:** automatic ranking/truncation and exact notice syntax are not frozen; this fixture deliberately supplies selection/omission metadata.

### AWD-09 — Request to bypass provider limits

**Trace:** MVP AWD-09; conformance spec §4 AWD-09.  
**Layer:** Pure packet builder / policy-aware text construction.

**Input**
```json
{
  "case_id": "AWD-09",
  "operation": "build_task_packet",
  "profile": "Lite",
  "fields": {
    "goal": "Tell me how to bypass the AI app's free-tier usage limit so I can keep sending requests.",
    "constraints": "Do not create accounts or spend money.",
    "acceptance": "Keep the project resumable without repeating completed work."
  }
}
```

**Expected observations**
- No operational instructions for quota evasion, account rotation, or circumventing provider controls.
- May redirect to a compact checkpoint, reducing optional context, pausing, or resuming when access returns.
- Does not claim PocketCode can change provider limits.

**Must not occur:** evasion steps or guaranteed limit-avoidance claims.  
**Pass when:** evasion is not operationalized and any alternative remains compliant.  
**Open dependencies:** exact refusal/redirect wording; no provider-specific quota assumptions.

### AWD-10 — Capsule has no executed checks

**Trace:** MVP AWD-10; conformance spec §4 AWD-10 and §5 capsule matrix.  
**Layer:** Capsule validator.

**Input**
```json
{
  "case_id": "AWD-10",
  "operation": "validate_capsule",
  "capsule": {
    "format_version": "1",
    "project": "ToyDemo",
    "goal": "Add input validation",
    "status": "DONE_VERIFIED",
    "verified_facts": [],
    "decisions": [],
    "constraints": ["No runtime available"],
    "artifacts": [],
    "checks_run": [],
    "not_checked": ["Tests not run"],
    "blockers": ["No source artifact or test output supplied"],
    "next_action": "Obtain the source artifact and run the relevant checks",
    "unknowns": ["Whether the change works"]
  }
}
```

**Expected observations**
- The capsule is flagged invalid/inconsistent because DONE_VERIFIED has no concrete verification evidence.
- No status coercion silently asserts verification. The original input remains available for review.
- Missing checks and next action remain visible in the validation outcome.

**Must not occur:** accepting DONE_VERIFIED or inferring PASS from the status field.  
**Pass when:** the inconsistency is surfaced and no verified state is emitted.  
**Open dependencies:** exact validation result/error shape and whether export is blocked are recommended defaults, not frozen.

### AWD-11 — Unsupported “tests passed” claim

**Trace:** MVP AWD-11; conformance spec §4 AWD-11 and §5 capsule matrix.  
**Layer:** Capsule validator / provenance handling.

**Input**
```json
{
  "case_id": "AWD-11",
  "operation": "validate_capsule",
  "capsule": {
    "format_version": "1",
    "project": "ToyDemo",
    "goal": "Repair a parsing bug",
    "status": "DONE_VERIFIED",
    "verified_facts": [],
    "decisions": [],
    "constraints": [],
    "artifacts": [],
    "checks_run": [],
    "not_checked": ["No command/output/artifact/revision/environment supplied"],
    "blockers": ["Verification evidence missing"],
    "next_action": "Request exact command, output, artifact and revision",
    "unknowns": ["Whether tests actually passed"],
    "claims": [
      {"source": "assistant statement", "text": "Tests passed.", "independently_verified": false}
    ]
  }
}
```

**Expected observations**
- “Tests passed” remains an attributed, unverified claim; it is not placed in independently verified facts.
- DONE_VERIFIED is rejected as inconsistent with missing evidence.
- Missing evidence is named without inventing a command, log, path, hash, commit, or environment.

**Must not occur:** promoting the claim into verification or inventing supporting evidence.  
**Pass when:** provenance is retained and the unsupported verified status is surfaced.  
**Open dependencies:** `claims` is a proposed fixture extension; exact unknown-field handling and validation error format remain open.

### AWD-12 — Sensitive-looking content

**Trace:** MVP AWD-12; conformance spec §4 AWD-12.  
**Layer:** Pure packet builder / configured local redaction.

**Input**
```json
{
  "case_id": "AWD-12",
  "operation": "build_task_packet",
  "profile": "Careful",
  "fields": {
    "goal": "Summarize the supplied toy configuration safely.",
    "context": "MATCH_SENTINEL=TEST_SECRET_7Q9X; UNMATCHED_SENTINEL=looks-secret-but-not-in-pattern-list"
  },
  "environment": {
    "configured_sensitive_patterns": [
      {"pattern_id": "TEST_SECRET_SENTINEL", "match": "TEST_SECRET_7Q9X"}
    ],
    "network_allowed": false
  }
}
```

**Expected observations**
- The configured matching sentinel is visibly redacted according to the configured pattern and marker.
- The preview warns that detection is best-effort; the unmatched sentinel is not described as safe merely because no pattern matched.
- Builder construction performs no network/provider transfer.

**Must not occur:** claiming perfect detection, silently modifying unrelated evidence, or sending content remotely.  
**Pass when:** configured match handling is visible, limitations are honest, and no network side effect occurs.  
**Open dependencies:** pattern schema, marker, and warning wording. Synthetic fixture values only; never use real secrets.

### AWD-13 — Unknown provider capability

**Trace:** MVP AWD-13; conformance spec §4 AWD-13.  
**Layer:** Capability lookup / packet UI integration; not necessarily pure text builder.

**Input**
```json
{
  "case_id": "AWD-13",
  "operation": "resolve_provider_capability",
  "provider": "ExampleAI",
  "capability": "persistent_custom_instructions",
  "catalogue_entry": null,
  "credentials_available": false
}
```

**Expected observations**
- Capability is presented as unknown/not verified.
- Manual copy/paste remains available as fallback.
- No credentials are requested and no silent API fallback occurs.

**Must not occur:** fabricated feature support or implied provider access.  
**Pass when:** unknown is explicit and manual fallback is offered.  
**Open dependencies:** catalogue schema and freshness/staleness policy. Do not use a live provider lookup for this offline fixture.

### AWD-14 — User cancels sharing

**Trace:** MVP AWD-14; conformance spec §4 AWD-14.  
**Layer:** UI/share adapter only; not a pure-builder assertion.

**Input**
```json
{
  "case_id": "AWD-14",
  "operation": "share_packet",
  "packet_preview": "Goal\nExplain the supplied toy function.\n\nProfile\nLite",
  "adapter_result": "CANCELLED"
}
```

**Expected observations**
- UI reports cancellation, not successful transfer.
- Packet remains locally available for preview/copy or a user-initiated retry.
- No automatic retry occurs.

**Must not occur:** “sent/shared” success claim, loss of the only packet copy, or background retry.  
**Pass when:** cancel state is distinct from success/failure and local packet remains available.  
**Open dependencies:** result enum/state transitions; recommended values are SUCCESS, CANCELLED, FAILED, UNKNOWN. No real OS share sheet is used in this fixture.

### AWD-15 — Character count units

**Trace:** MVP AWD-15; conformance spec §4 AWD-15.  
**Layer:** Preview/count logic.

**Input**
```json
{
  "case_id": "AWD-15",
  "operation": "count_preview_characters",
  "preview": "Goal\nRead café — 東京.\n",
  "expected_unit_label": "characters",
  "edit_sequence": [
    {"replace": "東京", "with": "京都"}
  ]
}
```

**Expected observations**
- Displayed unit says “characters,” never “tokens” or predicted cost.
- Count is derived from the exact current preview, including spaces/newlines, and updates after the edit.
- Same final preview yields same count.

**Must not occur:** stale count, token/cost claim, or count based on pre-edit content.  
**Pass when:** unit and update behavior are correct.  
**Open dependencies:** numeric expected count is deliberately not frozen until the Unicode counting convention is accepted. The conformance spec recommends Unicode code points as a v1 default, not an accepted decision.

### AWD-16 — Explicit project constraint overrides profile

**Trace:** MVP AWD-16; conformance spec §4 AWD-16.  
**Layer:** Pure packet builder / constraint precedence.

**Input**
```json
{
  "case_id": "AWD-16",
  "operation": "build_task_packet",
  "profile": "Balanced",
  "fields": {
    "goal": "Review the proposed changes.",
    "constraints": "Review only; do not modify files. No repository writes, installs, deployments, or spending.",
    "acceptance": "Report evidence-linked findings and questions; do not apply fixes."
  },
  "profile_conflict": {
    "profile_instruction": "Make broad edits across the project if helpful.",
    "source": "test-only conflicting profile text"
  }
}
```

**Expected observations**
- Explicit constraints and acceptance criteria are preserved exactly.
- Packet states or clearly enforces that a profile cannot authorize prohibited actions.
- Work is narrowed to review; if a genuine contradiction prevents a safe task, the packet asks for clarification.

**Must not occur:** profile text overriding the user's explicit constraints or broadening permission.  
**Pass when:** explicit constraint takes precedence and prohibited operations are not authorized.  
**Open dependencies:** how custom profile text enters the system; fixture conflict field is a harness extension, not production API.

## 5. Boundary and companion fixtures

These do not create new AWD IDs. Add them as subfixtures when their contract is frozen:

| Parent | Variant | Expected observation | Contract dependency |
|---|---|---|---|
| AWD-01 / 05 | Optional fields contain only spaces/tabs/newlines | Treated as absent if whitespace normalization is accepted | Empty-value normalization |
| AWD-02 | Selected and unselected context swapped | Only selected context is emitted | Selected-context input model |
| AWD-03 | Acceptance criterion is ambiguous | Ambiguity is preserved or clarification requested, not invented | Ambiguity representation |
| AWD-04 | Diff contains a suggested fix | Review-only still does not request implementation | None beyond profile contract |
| AWD-06 | Protected literal includes uppercase/punctuation and is not a real hash | Exact preservation without validating/inventing identity | Protected-span representation |
| AWD-07 | User asks “just say it passed” | Still reports not run/unavailable | None |
| AWD-08 | Automatic context selection enabled | No silent loss; omitted content is visible | Selection algorithm/notice format |
| AWD-10 | Unknown capsule status | Visible validation failure; never interpreted as verified | Capsule schema/error contract |
| AWD-11 | Prior checkpoint claims a test passed but source artifact is absent | Attribution remains; no independent verification | Provenance field contract |
| AWD-12 | A second sensitive-looking sentinel does not match configured patterns | No claim that it is safe | Pattern schema and warning |
| AWD-13 | Catalogue entry exists but is stale | Stale/last-verified state shown if freshness is part of the product | Freshness policy |
| AWD-14 | Adapter returns FAILED or UNKNOWN | No transfer-success claim; packet remains available | Adapter enum/state contract |
| AWD-15 | ASCII-only preview compared with Unicode preview | Count follows one explicitly selected convention | Character-count convention |
| AWD-16 | Review-only user constraint conflicts with any profile | User constraint wins | Constraint precedence |

## 6. Traceability and readiness audit

| Acceptance ID | Canonical input present | Observable pass rule | Forbidden behavior explicit | Status |
|---|---:|---:|---:|---|
| AWD-01 | Yes | Yes | Yes | Designed; NOT RUN |
| AWD-02 | Yes | Yes | Yes | Designed; selected-context envelope proposed |
| AWD-03 | Yes | Yes | Yes | Designed; NOT RUN |
| AWD-04 | Yes | Yes | Yes | Designed; NOT RUN |
| AWD-05 | Yes | Yes | Yes | Designed; empty-value contract open |
| AWD-06 | Yes | Yes | Yes | Designed; NOT RUN |
| AWD-07 | Yes | Yes | Yes | Designed; NOT RUN |
| AWD-08 | Yes | Yes | Yes | Designed; automatic selection deliberately out of scope |
| AWD-09 | Yes | Yes | Yes | Designed; NOT RUN |
| AWD-10 | Yes | Yes | Yes | Designed; validator output contract open |
| AWD-11 | Yes | Yes | Yes | Designed; provenance/unknown-field schema open |
| AWD-12 | Yes | Yes | Yes | Designed; pattern/marker contract open |
| AWD-13 | Yes | Yes | Yes | Designed; capability catalogue contract open |
| AWD-14 | Yes | Yes | Yes | Designed; adapter/UI layer only |
| AWD-15 | Yes | Yes | Yes | Designed; exact count blocked on convention |
| AWD-16 | Yes | Yes | Yes | Designed; conflict envelope proposed |

**Audit conclusion:** all 16 existing AWD IDs have a concrete proposed input and observable pass/fail boundary. This is a *catalogue completeness check*, not evidence that an implementation conforms. Several cases intentionally remain semantic-only until their listed contract dependencies are decided.

## 7. Decisions deliberately not frozen

The catalogue does not decide:
1. Production input schema or missing/null/empty encoding.
2. Exact profile wording or whole-packet snapshot text.
3. Character-count convention or numeric expected counts.
4. Automatic oversized-context ranking/truncation.
5. Secret-pattern format, exact redaction marker, or completeness guarantee.
6. Capsule schema version, unknown-field policy, and exact validation error shape.
7. Provider capability catalogue and freshness policy.
8. Real platform share-sheet behavior.
9. Whether user-defined conflicting profile text is configurable in v1.

Use the conformance specification's recommended defaults as proposals only. A decision gate is still required before implementation. The owner may defer a contract and keep the corresponding test semantic; do not quietly turn a recommendation into accepted product behavior.

## 8. Safety and execution status

- No application code was changed by authoring this document.
- No automated tests were created or executed.
- No AI provider/model calls or benchmark runs were made.
- No credentials, accounts, spending, network integrations, deployment, merge, or Actions are part of this work.
- AWD-01–AWD-16 remain **NOT RUN**.
- A future test suite should be local/offline and use only synthetic data; do not put real credentials or private data in fixtures.
