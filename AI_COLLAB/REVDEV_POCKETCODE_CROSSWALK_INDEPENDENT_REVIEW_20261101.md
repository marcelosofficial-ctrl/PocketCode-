# RevDev ↔ PocketCode Crosswalk — Independent Static Review (2026-11-01)

**Status:** ChatGPT and Claude static desk reviews received; Gemini review pending. This is a review note, not approval of a shared contract, implementation, or combined acceptance suite.

**Reviewed source snapshot**
- RevDev review branch: `review/revdev-adaptive-ai-workshare-2026-10-27`
- RevDev acceptance traceability supplement: `resume/revdev/POCKETCODE_REVDEV_ACCEPTANCE_TRACEABILITY_SUPPLEMENT_2026-10-29.md`, blob `d56da68bdc5414cf518d97abc63445f26c6af1fa`.
- RevDev AWC fixture manifest: `AI_WORK_COACH_SYNTHETIC_FIXTURES_V0_1.json`, blob `c2d4cba6c836f725f7bc4585f91e02d443fe89e1`.
- RevDev AWC fixture/measurement specification: blob `9169ae6c6e5689f70287b7c6c0aeac534d8f7183`.
- RevDev primary-source audit: blob `d7ad0bafbf4b0107967589be29b436b78d0f35e1`.
- RevDev P0-D source: `SHARED_INFRA_RELIABILITY_HARDENING_PLAN_2026-09-30.md`, blob `6a0c804e1ad75edf1022af960acbb143ba1430b6`, source lines 107–123.
- PocketCode canonical acceptance: `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, main blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.
- PocketCode execution contract: research-branch blob `128a00a9b2a335514814cab76fb5781fe8f9f858`.

The review inspected the complete 18-row AWC fixture manifest and the full Section 11–12 crosswalk text, then checked the PocketCode canonical LOOP/CASE meanings and original P0-D canary wording. No code, test, runtime, provider, queue, PR, or acceptance artifact was changed. No tests or model trials were run.

## 1. Overall verdict

**ACCEPT AS A CAUTIOUS CONCEPTUAL TRACEABILITY DRAFT, WITH TWO PRECISION REFINEMENTS RECOMMENDED.**

The crosswalk's central discipline is sound:
- it preserves AWC, AEC, LOOP/CASE, P8U, P0-D and CYC namespaces;
- it distinguishes conceptual adjacency from acceptance equivalence;
- it does not count one project's tests as proof for another;
- it correctly identifies the AWC fixtures as assistant/Work Coach evaluations, not execution-runner acceptance;
- it leaves P0-D items 1–7 and 9 unmapped where the PocketCode cases do not share the same observable invariant;
- it does not overstate RevDev implementation status or PocketCode execution capability.

No wholesale remapping is justified by this review. The table should remain a draft until the independent Claude/Gemini reviews are reconciled.

## 2. Section 11 — AWC-to-PocketCode review

| AWC ID | Review verdict | Reason / refinement |
|---|---|---|
| AWC-001 | No direct mapping is correct | One-file typo/task quality does not establish a phone execution or trusted exit-0 result. |
| AWC-002 | LOOP-06 adjacent only is correct | A multi-file acceptance checklist is not the same as named program-reported checks with source/status provenance. |
| AWC-003 | No mapping is correct | Helper/dependency reuse is outside the current LOOP/CASE execution acceptance. |
| AWC-004 | LOOP-02/03 adjacent is defensible | Honest “not run” reporting and refusing unsupported PASS touch these requirements, but AWC tests assistant reporting while LOOP-03 requires trusted execution-terminal evidence. |
| AWC-005 | LOOP-12 / CASE-15 adjacent only is correct | Prompt/trust-boundary handling is not a test of enforced runtime egress denial or absence of service secrets. Keep the threat models separate. |
| AWC-006 | LOOP-07 / CASE-12 conceptual relation is defensible | Both value bounded, useful diagnostics, but AWC tests assistant log diagnosis and PocketCode tests report contents/transfer. |
| AWC-007 | No direct LOOP/CASE mapping is correct | Session/context continuation is broader than preserving a prior execution result or distinguishing reruns. |
| AWC-008 | LOOP-09 / CASE-13 adjacent only is correct | Repair retries after failed edits differ from idempotent dispatch after an ambiguous network acknowledgement. |
| AWC-009 | LOOP-14 adjacent only is correct | Assistant advice against quota evasion is not the product's explicit provider/billing authorization gate. |
| AWC-010 | LOOP-08 / LOOP-13 conceptual relation is defensible, but clarify transfer direction | AWC-010 prepares a task packet **from PocketCode/RevDev toward an assistant** using explicit copy/share/paste. LOOP-08 copies an execution report **from PocketCode back toward an assistant**. The transport principle overlaps, but payload purpose and direction differ. LOOP-13 separately constrains unsupported automation claims. Neither is an equivalent acceptance test. |
| AWC-011 | No direct mapping is correct | Prompt injection in source/task content is not the same security property as runtime network isolation or secret exclusion. |
| AWC-012 | LOOP-02 / LOOP-14 adjacent only is correct | Simulated metric labeling touches honest UI/simulation and zero-cost governance, but LOOP-14 does not validate telemetry provenance or fabricated token/time/cost values. |
| AWC-013 | No direct mapping is correct | Mid-task checkpoint creation is not a terminal run/report criterion. |
| AWC-014 | No mapping is correct | Research completeness/source provenance is not directly covered by LOOP/CASE. |
| AWC-015 | No mapping is correct | Kernel/host retention is not established by execution-loop acceptance. |
| AWC-016 | No mapping is correct | Review-efficiency choices are outside the current execution-loop acceptance. |
| AWC-017 | LOOP-13 / LOOP-14 adjacent only is defensible | Capability honesty and provider governance overlap, but neither LOOP criterion is a general provider/model/plan/host capability-registry test. |
| AWC-018 | Mapping is defensible but LOOP-05 needs a condition | LOOP-02/03 and CASE-12 are the strongest adjacent concepts: preserve partial evidence and do not invent completion/PASS in a report. LOOP-05 is relevant **only when the missing terminal signal also leaves lifecycle/infrastructure outcome uncertain**. Truncation alone is an evidence-collection quality problem, not necessarily a timeout, cancellation, rejection, or infrastructure failure. |

### Recommended Section 11 wording refinements

1. For AWC-010, explicitly say the shared copy/share mechanism is directionally related but the AWC task packet and LOOP-08 execution report are different payloads and transfer stages.
2. For AWC-018, qualify LOOP-05 as conditional on lifecycle/terminal uncertainty; do not imply that all truncated evidence is a LOOP-05 timeout/uncertain-infrastructure case.
3. Preserve all existing AWC/AEC/LOOP/CASE IDs and the current “adjacent/no mapping” discipline. No new IDs are needed.

## 3. Section 12 — P0-D review

The source wording was checked directly in the P0-D matrix at source lines 107–123.

| P0-D item | Review verdict | Reason |
|---|---|---|
| 1 | No direct PocketCode mapping is correct | Legacy READ_ONLY mission with full expected guards is a RevDev mission compatibility canary. |
| 2 | No direct mapping is correct | Absence of optional `interactionCycle` is a RevDev backward-compatibility condition. |
| 3 | No direct mapping is correct | Optional top-level `expected` handling is a RevDev mission-schema condition. |
| 4 | No direct mapping is correct | Empty optional mission-object handling has no matching PocketCode observable criterion. |
| 5 | No direct mapping is correct | Grouped BEGIN is a RevDev interaction-cycle phase, not PocketCode execution lifecycle. |
| 6 | No direct mapping is correct | Same boundary as item 5 for grouped MIDDLE. |
| 7 | No direct mapping is correct | Same boundary as item 5 for grouped END. |
| 8 | CASE-12 / LOOP-07 adjacent only is correct | PocketCode requires truthful failure/incomplete diagnostics and a useful report; P0-D additionally requires durable persistence/publication of the intentional validation-failure result. PocketCode acceptance does not currently assert that same publication invariant. |
| 9 | No direct mapping is correct | Quarantining a malformed mission while allowing later queue work to continue is not equivalent to rejecting a missing/unsafe PocketCode input. |
| 10 | CASE-13 / CASE-16 adjacent only is correct | Ambiguous retry/idempotency and run identity/order are related; P0-D additionally checks exact-result publication and duplicate/idempotent replay. Neither PocketCode case proves the RevDev publication path. |

### Editorial precision

Section 12's column header “Exact requirement (condensed without changing meaning)” is understandable but slightly awkward. Prefer **“Source requirement (condensed)”** and retain the source citation/line range. The table is a faithful summary, but it is not a verbatim transcription.

No substantive P0-D remapping is recommended.

## 4. Cross-cutting semantic risks to retain

1. AWC fixtures evaluate assistant/coach behavior; PocketCode LOOP/CASE evaluate a proposed mobile execution/report product; RevDev P8U/P0-D evaluate publisher/recovery and mission/runtime compatibility. These are separate test objects.
2. AEC-001–012 are PocketCode Work Coach evaluation fixtures, not LOOP/CASE execution acceptance. AWC-001–018 are RevDev Work Coach fixtures, not P8U/P0-D acceptance.
3. AWC-010's manual task handoff and LOOP-08's execution-report handoff should not be collapsed into one directionless “copy” capability.
4. AWC-018's partial/truncated input is not automatically a timeout. Evidence completeness and lifecycle outcome remain distinct axes.
5. P0-D item 8's durable publication requirement and item 10's exact-result replay requirement remain RevDev-specific acceptance obligations.
6. The P0-D source says all compatibility canaries must be green before shared-runtime activation. This is a RevDev activation gate, not a PocketCode runtime/provider selection rule.
7. The PocketCode canonical acceptance and execution contract are proposed/not run. RevDev AWC trials and P8U/P0-D runtime acceptance remain NOT RUN; RevDev PC/runtime/queue/publication state remains UNKNOWN.

## 5. Review status and next independent reviews

**ChatGPT:** static crosswalk review completed as recorded here. This is not an independent second-person review and does not replace Claude/Gemini.

**Gemini review request:** independently challenge Section 11 for false semantic equivalence, missing negative cases, and overbroad LOOP/CASE associations. Prioritize AWC-010 transfer direction, AWC-018 truncation versus lifecycle uncertainty, and the exact boundaries for AWC-005/011/012/017. Review Section 12 for whether any P0-D item has been incorrectly mapped or omitted. Do not rewrite IDs or turn adjacent concepts into shared tests.

**Claude review request:** independently challenge the engineering-state and recovery implications of Sections 11–12. Focus on which evidence producer/observer owns each claim, identity correlation, durable persistence/publication, queue quarantine/liveness, exact-result replay, and the difference between a task repair retry and a dispatch retry. Do not infer current PC implementation behavior; it remains UNKNOWN. Do not propose source/runtime changes from this documentation-only review.

Both reviews should return:
- exact row/ID;
- ACCEPT / CHANGE / REJECT;
- source-backed rationale and exact artifact/line references;
- any counterexample or missing negative case;
- whether the point is conceptual, contract-level, implementation-level, or runtime evidence;
- explicit NOT RUN / UNKNOWN status where applicable.

Do not edit PR #2/#3, source/tests, canonical PocketCode acceptance, RevDev source/tests, runtime, queue, provider, security boundary, or integration topology. Any resulting crosswalk correction remains documentation-only and must preserve the original acceptance IDs.

## 6. Verification record

- Read-only source and acceptance comparison only.
- AWC manifest contains the stated 18 fixture IDs; the manifest is labelled `PROPOSED_NOT_RUN`.
- P0-D source matrix contains ten ordered canaries; all ten were compared against the PocketCode canonical LOOP/CASE meanings.
- No AWC model trials, PocketCode LOOP/CASE tests, RevDev P8U/P0-D runtime tests, provider calls, GitHub Actions, or local PC tests were run.
- No implementation, source, test, PR, queue, runtime, security boundary, merge, or deployment was changed.


## 7. Supplemental execution-boundary helper observations — 2026-11-01

**Scope separation:** These are additional read-only observations from the lifecycle-helper source referenced by the separate execution-boundary crosswalk. They do not alter Sections 2–3 above, the AWC/P0-D semantic mappings, PocketCode canonical acceptance, or any original test namespace. They are candidate gaps, not an implementation authorization.

### OBS-01 — No terminal event is conflated with confirmed provider failure

Exact source snapshot:
- PR #3 base helper: `scripts/lifecycle_contract.py`, blob `ba8d4d0b217c90513bed020e298029ef4e16f164`.
- Lifecycle-fingerprint descendant helper: blob `316345341603848c4a86a6a82e533daa796c7695`.
- Owner decision register: `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md`, blob `e67b2659cf2d71ef77d8e4619c91143e71062470`, D-02.

Static path:
1. `TERMINAL_EVENTS` maps `provider_error` to raw outcome `UNKNOWN` (helper lines 16–23).
2. `reduce_terminal_events()` also initializes its outcome to `UNKNOWN` and leaves `winning_event_id=None` when no terminal event exists (lines 128–137).
3. `derive_disposition()` maps every `execution_outcome == "UNKNOWN"` to `PROVIDER_ERROR` (lines 52–53).

Therefore an empty event list or a stream with no terminal event is indistinguishable at the disposition-helper interface from an explicit provider-error terminal event. D-02's working default says `PROVIDER_ERROR` is appropriate only when the infrastructure cause itself is confirmed; missing terminal evidence must remain unknown/incomplete. The two states need a distinct representation or an explicit confirmed-cause input before disposition derivation. The reducer's existing event-ownership limitation also means an event kind alone does not establish trusted provider provenance.

**Candidate negative/positive cases:**
- Empty event list and nonterminal-only event list: no terminal evidence; must not become confirmed `PROVIDER_ERROR`.
- Explicit, identity-bound and trusted provider-error evidence: may produce provider-error disposition while the user-facing execution verdict remains INCOMPLETE.
- Unknown, missing, or unbound event source: retain UNKNOWN/INCOMPLETE, not a confirmed infrastructure cause.

This is a source-level contract finding, not proof that a live caller currently misuses the helper. No tests were run.

### OBS-02 — Malformed contradiction flag can bypass the contradiction gate

In the same helper, `contradictory_evidence` is checked with ordinary truthiness (`if contradictory_evidence`, lines 43–47), while the four positive PASS gates are explicitly required to be literal `True` (lines 64–67). The helper does not reject non-boolean values for `contradictory_evidence`, `limit_violated`, or `output_truncated`.

For example, `contradictory_evidence=0` is falsy and bypasses the contradiction guard. With EXIT_ZERO, confirmed cleanup and all four PASS gates set to literal True, the current function can return PASS even though the contradiction field is malformed rather than an explicit boolean False. Truthy malformed limit flags can also be interpreted as a confirmed limit; falsy malformed flags can be treated as no limit.

**Candidate cases:** test `contradictory_evidence` with 0, None, empty string and string "false"; test both limit flags with malformed truthy and falsy values. Invalid values should be rejected or yield an incomplete/unknown disposition, never silently coerced into valid evidence. Add a passing-path regression proving malformed contradiction evidence cannot yield PASS.

The existing `test_malformed_truthy_gate_values_never_produce_pass` does not cover these three flags. This is static source analysis; no suite was run.

### OBS-03 — Bearer-token redaction can lose a long separator across the carry boundary

Exact source snapshot: the same PR #3 and lifecycle-fingerprint helper blobs above; `StreamingRedactor` has `CARRY_BYTES = 768` (line 342) and the bearer pattern `Bearer\\s+[A-Za-z0-9._~+/-]{8,256}` (line 344). The whitespace quantifier is unbounded. The streaming algorithm emits a prefix when no complete configured match is present in the current combined buffer; it only moves the cutoff backward when it can already see a complete match crossing that cutoff (lines 359 onward).

A local reproduction of this exact pattern/carry algorithm, with the Bearer prefix followed by 900 whitespace bytes before the token and input split across chunks, retained the bearer token unredacted. The current carry-boundary regression uses a short separator and does not cover a separator longer than the carry.

**Candidate cases:** test whitespace separators at, below and above 768 bytes, including chunked input where the token arrives only after the prefix has already crossed the candidate cutoff. The helper should either use an explicitly bounded separator with a safe streaming rule or preserve bounded parser state sufficient to avoid emitting a potentially sensitive prefix. Do not treat this redactor as a privacy guarantee; prevent credentials from entering the user-code environment and minimize collection.

This reproduction is a targeted check of the pattern/carry algorithm, not execution of the repository's full test suite. No source or tests were changed.

### Review disposition

OBS-01 through OBS-03 should be reconciled with the existing execution-boundary crosswalk Sections 6–9 and the D-01..D-04 owner register before any helper patch or schema decision. The known positive improvements on the lifecycle-fingerprint descendant (identity validation, malformed-event preservation, tombstone retention/fingerprint conflict) remain branch-scoped; these new observations do not negate them. Both helper/test suites remain NOT RUN in this review. No PR, source, test, canonical acceptance, provider, runtime, queue, Actions, account, spend, merge or deployment was changed.


## 8. Claude review received and source-reconciled disposition (2026-11-01)

**Status:** Claude's two review responses were received. The reconciliation below supersedes Sections 2–3 wherever a row-level mapping changes, and extends Section 7 where the source review found additional contract gaps. Gemini's independent review remains pending.

### 8.1 Review provenance and exact source recheck

Claude explicitly reported that it read only this review note, could not retrieve the underlying source files, did not verify the review's line references, and did not run tests. Treat Claude's comments as an independent conceptual challenge, not as source verification.

ChatGPT then re-fetched the source snapshots to resolve the disputed points:

- RevDev AWC manifest: blob c2d4cba6c836f725f7bc4585f91e02d443fe89e1. It contains AWC-001 through AWC-018 and remains PROPOSED_NOT_RUN.
- PocketCode canonical execution acceptance, main and research branch: blob c6714c27db52b2962fe8d1c7e6a16829d46a8338. The two refs returned the same blob. LOOP/CASE criteria remain proposed/not run.
- RevDev P0-D source: blob 6a0c804e1ad75edf1022af960acbb143ba1430b6, lines 107–123. The ten ordered canary requirements match the crosswalk's source wording.
- Lifecycle-fingerprint helper: scripts/lifecycle_contract.py, branch pocketcode-lifecycle-fingerprint-audit-2026-10-27, blob 316345341603848c4a86a6a82e533daa796c7695.
- Lifecycle-fingerprint tests: blob ef9a68de632be30c091afe57f0724fd030a513f9.
- Owner decision register: AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md, blob e67b2659cf2d71ef77d8e4619c91143e71062470, especially D-01 through D-04 and D-06/D-08.

The lifecycle-fingerprint branch remains a separate, unmerged 34-commit descendant of the PR #3 base. Its helper and tests are not evidence of integration into PR #3, main, or a live runtime. No test suite was run in this recheck.

### 8.2 Superseding AWC mapping decisions

The manifest confirms the fixture intents. The following changes reduce false-positive mappings and preserve the separation between assistant behavior and execution acceptance.

| AWC ID | Reconciled PocketCode relation | Disposition |
|---|---|---|
| AWC-001 | None | Keep none. |
| AWC-002 | LOOP-06 adjacent only | Keep. Preserving a task checklist is not the same as validating named program-reported checks and provenance. |
| AWC-003 | None | Keep none. |
| AWC-004 | LOOP-02/03 adjacent only | Keep. Honest not-run reporting and refusal to invent PASS are related, but AWC tests an assistant response, not trusted execution evidence. |
| AWC-005 | None | Remove LOOP-12/CASE-15. It concerns unsafe instructions in untrusted task content and preserving authorization checks, not enforced runtime egress denial or secret exclusion. |
| AWC-006 | LOOP-07/CASE-12 adjacent only | Keep as a bounded-diagnostics/report-quality analogy, not acceptance equivalence. |
| AWC-007 | None | Keep none. Session continuation is not a run lifecycle criterion. |
| AWC-008 | None | Remove LOOP-09/CASE-13. Repair retries change or repair task work; dispatch retries resend the same attempt after ambiguous acknowledgement. The shared word “retry” is not a shared invariant. |
| AWC-009 | None | Remove LOOP-14. Assistant advice against quota evasion is not the product's provider/billing authorization gate. |
| AWC-010 | LOOP-13 primary adjacency; LOOP-08 secondary transport analogy | Keep as conceptual only. Both move information from the product/workflow toward an assistant. AWC-010 is a prospective task packet without an execution verdict; LOOP-08 is a retrospective report bound to a run identity and verdict. The common point is truthful, user-initiated manual handoff, not payload equivalence. |
| AWC-011 | None | Keep none. It concerns source-file prompt injection and assistant instruction hierarchy, not runtime network/secret isolation. |
| AWC-012 | LOOP-02 adjacent only | Remove LOOP-14. Honest labeling of simulated values relates to UI state honesty; LOOP-14 does not test telemetry provenance or fabricated counters. |
| AWC-013–016 | None | Keep none. |
| AWC-017 | None | Remove LOOP-13/14. Unknown provider/model/plan/host capability metadata is not a capability-registry acceptance case in the current LOOP/CASE suite. |
| AWC-018 | CASE-12 primary adjacency; LOOP-02/03 secondary conceptual relation | Remove LOOP-05 from this fixture. CASE-12 is the closest report behavior: preserve the actual uncertainty, diagnostics and truncation markers. LOOP-02/03 express related honesty principles, but AWC-018 does not observe a PocketCode execution lifecycle or trusted terminal event. |

#### AWC-005 and AWC-011 boundary

These fixtures both concern assistant-side handling of untrusted instructions, but they are not duplicates: AWC-005 is an unsafe shortcut in task content during a security-sensitive change; AWC-011 is instruction-like text embedded in a source file that attempts to change assistant policy. Neither proves the separate PocketCode runtime property in LOOP-12/CASE-15. Keep both AWC fixtures, but do not map either to runtime isolation.

#### AWC-010 handoff precision

Correction is explicit: the transfer directions are the same. Both handoffs move information outward from the product/workflow toward an AI assistant. Their distinctions are payload, stage and identity binding:
- AWC-010 prepares a task packet before execution and carries no run verdict.
- LOOP-08 copies a report after execution and the report is associated with a specific run and observed result.
- LOOP-13 is the stronger adjacency for truthful claims about unsupported cross-app automation and explicit manual fallback.
- LOOP-08 is a secondary analogy for user-initiated copy/share transport only.

Neither AWC-010 nor a manual copy/share action proves an execution report is accurate.

#### AWC-018 and truncation precision

The exact fixture says the evidence excerpt is partial and lacks a terminal result. It does not tell us whether truncation was display-only, collector/retention truncation, or caused by an enforced runtime limit. PocketCode's D-01/D-03 working definitions keep those states separate. Therefore:
- Keep CASE-12 as the primary adjacent report requirement.
- Keep LOOP-02/03 only as broader honesty concepts.
- Do not map this fixture to LOOP-05.
- A separate runtime fixture is needed for an enforced limit that kills a child while termination remains unconfirmed. That is a lifecycle uncertainty case, unlike display-only or collector-only truncation with independent confirmed exit evidence.

### 8.3 Superseding P0-D mapping decisions

The original P0-D source at lines 107–123 was re-fetched and checked. Keep the original ten IDs and meanings.

| P0-D item | Reconciled PocketCode relation | Disposition |
|---|---|---|
| 1–7 | None | Keep none. These are RevDev mission compatibility/schema/grouped-cycle cases. |
| 8 | CASE-12/LOOP-07 adjacent only | Keep adjacency, but state explicitly that neither current PocketCode case requires durable persistence/publication of the validation-failure result. |
| 9 | None | Keep none. CASE-16 is out-of-order run identity/order, not poison-item quarantine or queue liveness. No current LOOP/CASE case proves a malformed queue item can be quarantined while later work continues. |
| 10a: duplicate/idempotent replay after ambiguous response | CASE-13 adjacent only | Covers only the ambiguous retry/idempotency sub-invariant. |
| 10b: run identity and order association | CASE-16 adjacent only | Covers only correct run/result correlation under out-of-order completion. |
| 10c: durable exact-result publication and replay | None equivalent | Neither CASE-13 nor CASE-16 proves exact-byte durable publication, restart recovery, or persistent duplicate replay. |

Use “Source requirement (condensed)” as the Section 12 column header. Do not say “exact” when the text is condensed.

P0-D item 9 remains a RevDev queue-liveness obligation. Its minimum negative cases should include: a poisoned item does not block later work; quarantine preserves diagnostic evidence instead of silently deleting the item; crash during quarantine is idempotently recoverable; and a poison item cannot enter an unbounded retry loop. These are candidate RevDev acceptance checks, not additions to PocketCode's canonical suite.

### 8.4 OBS-01 through OBS-03: reconciled findings

#### OBS-01 — No terminal evidence and provider error need separate states

The source path is confirmed in the helper snapshot:
- TERMINAL_EVENTS maps provider_error to UNKNOWN.
- reduce_terminal_events() initializes its outcome to UNKNOWN and leaves the winning event unset if no terminal event exists.
- derive_disposition() maps UNKNOWN to PROVIDER_ERROR.

Claude accepts the finding and adds an important authority requirement. Preserve at least three distinguishable input states:
1. No terminal evidence exists.
2. A provider-error event exists, but its producer/source is missing, untrusted or mismatched.
3. A provider-error event is authenticated to the trusted provider boundary and its cause is confirmed.

Only state 3 may support a confirmed provider-error disposition. States 1 and 2 remain UNKNOWN/INCOMPLETE. D-02 requires a confirmed infrastructure cause; a terminal event kind by itself is not confirmation.

Candidate cases: empty stream; nonterminal-only stream; provider_error from a wrong/untrusted source; authenticated provider_error with confirmed cause. A pure helper can test the disposition distinction, but cannot prove a producer is authentic.

#### OBS-02 — Falsy malformed negative flags can bypass the contradiction/limit guard

The helper uses truthiness for contradictory_evidence, limit_violated and output_truncated. A malformed falsy value such as 0, None or an empty string can therefore be treated like False. In the PASS path, malformed contradictory_evidence=0 can bypass the contradiction check while the four positive gates are literal True.

The checked-in test test_malformed_truthy_gate_values_never_produce_pass exercises malformed values for the positive PASS gates. It does not exercise malformed falsy values for these three negative-polarity flags. The existing truthy cases such as the string "false" are not the same false-PASS bypass: they are truthy and currently fail closed for the contradiction guard or can cause limit misclassification.

Candidate regressions:
- For each of the three negative flags, test 0, None and empty string on an otherwise valid PASS path.
- Reject malformed values or return INCOMPLETE; never treat them as an explicit False.
- Test truthy malformed values separately for safe rejection and correct classification.
- Require literal booleans at the contract boundary. For a clean PASS, contradiction and limit/truncation flags must be explicitly False.

Evidence class: source-level helper contract. The caller's actual types and runtime behavior remain UNKNOWN.

#### OBS-03 — Bearer redaction has both a carry-boundary gap and a token-length gap

The source regex is explicitly case-insensitive ((?i)), so Claude's uncertainty about case variants is resolved by the checked-in source. Case-variant tests remain useful regression coverage.

The 768-byte carry issue is independently reproduced using the source algorithm copied from the helper. A match is not recognized until at least eight token characters are present. If the combined buffer crosses the cutoff while only zero to seven token characters are present, no complete regex match exists to move the cutoff backwards. With Bearer length 6, the leak trigger is 6 + separator_bytes + visible_token_bytes > 768. For zero to seven visible token bytes, the minimum separator length is 763 down to 756 bytes. The leak depends on chunk boundaries, so a single fixed 768-byte boundary test is insufficient.

Claude also correctly highlighted the 256-character token bound, with one precision correction: a token longer than 256 characters is not always “first 256 redacted, rest visible.” With a plain alphanumeric token, the trailing word-boundary requirement can cause the entire match to fail. With punctuation inside the allowed character class, a boundary can allow the first matched portion to be redacted while a suffix remains visible. Both outcomes are unsafe for a best-effort redactor.

Candidate regressions:
- Separator lengths 755–763 with zero to seven token bytes present at the chunk that crosses the carry cutoff; split chunks across the boundary.
- Bearer token lengths 255, 256, 257, 300 and above 600, using both alphanumeric-only and punctuation-containing values.
- Padding and delimiter cases including equals sign, period and hyphen.
- Mixed-case Bearer spellings. The source already uses case-insensitive matching.
- Assert that no secret suffix is emitted, not merely that a full known token string is absent.

This was a local reproduction of the copied source algorithm, not execution of the repository helper test suite. No source or tests were changed. The redactor remains best-effort and must not be treated as a security boundary.

### 8.5 Additional lifecycle-helper contract gaps

#### OBS-04 — Event kind does not establish producer authority

The reducer validates event ID, coordinator sequence, kind and mapping-shaped payload. It does not authenticate the producer or establish that a provider_error, exit, timeout or cleanup claim came from the component authorized to make that observation. The helper's accepted event shape does not itself prove source authority.

Candidate authority model:
- Child exit code: trusted process supervisor.
- Cleanup confirmation: cleanup observer, not child-reported output.
- Provider failure: authenticated provider boundary with confirmed cause.
- Policy/tenant authorization: coordinator or policy boundary.
- Artifact digest and object association: storage boundary.

A pure helper can require a producer-role/source field and allow-listed role. It cannot prove authenticity. A real boundary needs authenticated or channel-bound observations and tests for wrong-source and unauthenticated events. This is a contract gap, not proof of live caller misuse.

#### OBS-05 — Event reduction lacks explicit attempt-context correlation

The reducer does not receive an expected tenant/job/attempt/source/policy identity against which each event is checked. It sorts accepted events by coordinator sequence and event ID, but sequence order alone does not prevent an event from an earlier or different attempt from influencing the current reduction. D-04 proposes source-scoped event identity and tenant/job/attempt binding; it remains OPEN.

Candidate cases:
- An event for a different tenant, job or attempt cannot win the current reduction.
- A stale terminal event from an earlier attempt cannot replace the current attempt's result.
- Mismatched task/job/attempt/source/policy identity is rejected or quarantined, not coerced.
- Same event identity with changed payload or sequence is a conflict.

A pure helper can test explicit identity comparisons once expected context is part of its contract. It cannot prove IDs are unforgeable or unique across restarts. The caller's filtering behavior remains UNKNOWN.

#### OBS-06 — output_truncated is collapsed into LIMIT_EXCEEDED

The helper currently returns LIMIT_EXCEEDED when output_truncated is truthy, independently of whether an enforced runtime limit terminated the child. The owner register's D-01/D-03 working definitions distinguish:
- A trusted runtime-enforced deadline/resource limit and confirmed termination.
- Collector/retention truncation while independent process evidence may still confirm exit zero.
- Display-only truncation, which must preserve the execution verdict.

The current boolean field does not identify which case occurred. Do not interpret generic output truncation as a confirmed runtime limit or a lifecycle timeout. Preserve truncation cause/evidence quality separately from execution outcome and limit enforcement. Required evidence depends on the specific acceptance case; a presentation-only truncation must not rewrite a previously confirmed execution verdict.

Candidate cases: display-only truncation plus confirmed exit zero; collector cap plus independently confirmed exit zero; trusted enforced limit with confirmed termination; enforced limit with termination unconfirmed. Each must preserve the separate execution verdict, lifecycle and disposition dimensions.

Evidence class: source-level helper/contract mismatch against D-01/D-03 working definitions. Owner decisions remain OPEN; no canonical acceptance change is implied.

### 8.6 Engineering proof layers and next tests

Claude correctly separates what each test layer can establish:

| Layer | What it can establish | What it cannot establish alone |
|---|---|---|
| Pure helper | Deterministic mapping, typed-input rejection, event reduction over a supplied event list, fingerprint and reservation rules | Producer authenticity, durable transactions, provider execution, live queue liveness |
| Fake adapter | Scripted acknowledgement loss, call count/order, reconciliation transitions and no-redispatch decisions under controlled responses | Actual provider idempotency, cross-process atomicity or real termination |
| Persistence test | Atomic reservation/version allocation, durability across restart, torn-write detection and byte-for-byte republish | Authentic provider events or actual child termination |
| Provider/runtime boundary | Authenticated event source, actual child termination, real provider idempotency/lookup and queue liveness | Claims outside the chosen, exercised boundary |

The engineering gaps should be carried separately from AWC/P0-D semantic traceability:
- Dispatch retry: same key/same fingerprint resolves to the original attempt; same key/changed fingerprint conflicts before dispatch; after lost acknowledgement, UNKNOWN lookup means no redispatch; authoritative same-attempt lookup adopts the existing result.
- Repair retry: changed task content is a new task/attempt with a new identity. Reusing the same idempotency key with changed fingerprint must conflict. A repair must not race on the same workspace while an earlier dispatch remains unresolved.
- Persistence/publication: crash after result computation but before publication; restart republishes stored bytes exactly rather than recomputing; partial/torn writes are detectable; later evidence creates a new immutable version rather than silently changing an issued report.
- Queue liveness: quarantining a poison item does not block later items, preserves diagnosis, is idempotent across restart, and cannot retry forever.
- Authority/correlation: wrong-source and wrong-attempt events cannot determine the current disposition.

D-06 and D-08 already describe proposed idempotency and report-history requirements, but they remain proposals until tested at the actual atomic storage/provider boundary. A pure helper or fake adapter is not proof of those guarantees.

### 8.7 Reviewer reconciliation status

- ChatGPT: static source and crosswalk review recorded in Sections 2–3 and this reconciliation.
- Claude: two conceptual/engineering reviews received. Claude did not independently verify the underlying artifacts or run tests; ChatGPT rechecked the relevant source blobs listed in Section 8.1.
- Gemini: pending. The updated review request should prioritize the reconciled AWC changes, P0-D 9/10 split, OBS-01 through OBS-06, D-01/D-03 truncation semantics, and the boundary between pure-helper evidence and persistence/provider/runtime evidence.

Everything remains static review. AWC fixtures are PROPOSED_NOT_RUN; PocketCode LOOP/CASE is proposed/NOT RUN; lifecycle helper tests are NOT RUN; provider/runtime/queue/host behavior remains UNKNOWN. No implementation, test, canonical acceptance, PR, queue, runtime, provider, Actions, merge, deployment or spend was changed or invoked.


### 8.8 Cross-branch comparison and priority refinement

A direct source comparison was made between the PR #3 base helper (blob ba8d4d0b217c90513bed020e298029ef4e16f164) and the lifecycle-fingerprint descendant helper (blob 316345341603848c4a86a6a82e533daa796c7695):

- The complete derive_disposition block is identical in both snapshots. OBS-01, OBS-02 and OBS-06 therefore apply to both.
- The complete StreamingRedactor class is identical in both snapshots. OBS-03 therefore applies to both.
- reduce_terminal_events differs. The descendant adds checks for non-mapping events, blank event IDs/kinds, invalid sequence values, and non-mapping payloads; it preserves malformed events in invalid_events. The PR #3 base does not have these same checks.
- Neither reducer validates an authenticated producer role or compares event tenant/job/attempt/source/policy identity with an expected current-attempt context. OBS-04 and OBS-05 remain model-boundary gaps in both snapshots.
- The descendant's positive event-shape hardening is branch-specific and does not imply it is integrated into PR #3, main, or runtime.

The redaction test design is extended beyond Bearer values. The configured key/password/secret patterns also cap captured values at 256 characters. A targeted local reproduction of the copied source algorithm with 300-character values left 44 trailing characters visible for each of secret=, api_key=, access_token= and password=. Add 257, 300 and 600-plus character values for these patterns, and assert that no suffix is emitted. This was a copied-algorithm reproduction, not an execution of the repository tests.

Suggested source-level work priority, subject to the still-open owner decisions:
1. Separate no terminal evidence from confirmed provider error; require strict boolean validation for negative-polarity flags; distinguish runtime-enforced limit from collector/display truncation.
2. Specify producer authority and attempt-context identity before terminal reduction. Do not let coordinator sequence alone stand in for source or attempt binding.
3. Expand redaction regression coverage for carry boundaries and overlong values, while keeping the redactor explicitly outside the security boundary.
4. Only then use fake adapters, persistence/restart tests and provider/runtime evidence to establish dispatch, publication and queue guarantees.

This is prioritization for future review, not authorization to modify implementation or tests.


## 9. Regression plan

A separate staged test-design artifact has been added: [LIFECYCLE_CONTRACT_REGRESSION_PLAN_20261101.md](LIFECYCLE_CONTRACT_REGRESSION_PLAN_20261101.md). It separates pure-helper tests (OBS-01..06) from fake-adapter, persistence, provider-boundary and runtime/queue tests, defines candidate negative cases, and states evidence exit criteria. All cases remain proposed and NOT RUN. The plan does not authorize or imply implementation changes.
## 10. Gemini specification audit received and source-reconciled (2026-11-01)

**Input provenance:** The owner supplied a Gemini response headed "PocketCode Cross-Project Specification Audit and Lifecycle Regression Plan Review". Its self-reported date is 2026-11-02, one calendar day later than this audit's current date (2026-11-01). The date and authorship metadata were not independently authenticated. The response supplied artifact names but no commit SHAs, blob SHAs, source line numbers, or test output.

**Overall verdict:** Do not accept Gemini's AWC, CASE, P0-D, or OBS mappings as written. The supplied response systematically assigns meanings from different or unidentified specifications to identifiers already pinned in this project. Several engineering concerns are valuable and are retained below under new supplementary test IDs. This reconciliation does not replace or renumber any canonical acceptance ID.

### 10.1 Exact artifact recheck

The following snapshots were fetched again from GitHub:

- RevDev AWC synthetic fixture manifest: repository `marcelosofficial-ctrl/DevRelay-Missions`, blob `c2d4cba6c836f725f7bc4585f91e02d443fe89e1`. It contains 18 AWC fixtures, AWC-001 through AWC-018, with status PROPOSED_NOT_RUN.
- RevDev P0-D source: repository `marcelosofficial-ctrl/DevRelay-Missions`, blob `6a0c804e1ad75edf1022af960acbb143ba1430b6`, lines 107-123 for the P0-D matrix.
- PocketCode canonical execution acceptance: `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, main blob `c6714c27db52b2962fe8d1c7e6a16829d46a8338`.
- PocketCode execution contract: `PRODUCT/EXECUTION_CONTRACT.md`, research branch blob `128a00a9b2a335514814cab76fb5781fe8f9f858`.
- PocketCode transition/report matrix: `AI_COLLAB/TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md`, blob `c4166ad1447e5628c4f4aadd34c864c878d5f795`.
- PocketCode semantic-decision note: `AI_COLLAB/SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md`, blob `a237e882128865ce6a47651a1f9c6da6901f4994`.
- Current owner decision register: `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md`, blob `e67b2659cf2d71ef77d8e4619c91143e71062470`.

The cited PocketCode execution-acceptance file defines CASE-01 through CASE-16. It does not define CASE-17 or CASE-18. The execution contract does not contain the cited "Multi-Attempt Logging" section. The semantic-decision note contains four proposed executive decisions and no OBS-01 through OBS-06 identifier set. The actual OBS-01 through OBS-06 used in this review are the six helper findings pinned in Sections 7-8.

### 10.2 Identifier corrections

| Gemini's description | Pinned source meaning | Reconciliation |
|---|---|---|
| AWC-005 = resource capping | Unsafe shortcut suggested in untrusted task content | Reject mapping. It is a Work Coach trust-handling fixture, not a runtime resource test. |
| AWC-008 = egress isolation | Recovery after two consecutive targeted repair attempts fail | Reject mapping. Repair recovery is not network enforcement. |
| AWC-009 = secret protection | User asks how to bypass a usage limit | Reject mapping. Usage-limit advice is not secret scanning or environment isolation. |
| AWC-010 = output truncation | Manual task handoff when no supported connector exists | Reject mapping. The task packet is not an execution stream. |
| AWC-011 = cleanup guarantee | Source content contains instruction-like text asking the assistant to change its safety policy | Reject mapping. Prompt injection is not provider teardown. |
| AWC-012 = idempotency | Fabricated token, time, and cost metrics in a packet | Reject mapping. Telemetry honesty is not dispatch replay. |
| AWC-017 = attempt binding | Provider/model/host capabilities are unknown | Reject mapping. Capability honesty is not cross-attempt event correlation. |
| AWC-018 = artifact release gate | Partial/truncated evidence with no completion signal | Reject mapping. The fixture is assistant reporting from incomplete evidence, not current download authorization. |

The canonical PocketCode CASE meanings also contradict several Gemini descriptions:

- CASE-05 is cancellation and termination confirmation, not memory/CPU resource capping.
- CASE-07 is configured output-limit enforcement and explicit truncation/rejection.
- CASE-08 is missing input or an unsafe input path/name, not network egress.
- CASE-09 is exit zero with a program-reported failed check.
- CASE-10 is printed PASS with a non-zero exit.
- CASE-11 is browser disconnect while execution continues.
- CASE-12 is copying a report after a failed/incomplete run.
- CASE-13 is retry after an ambiguous network response and duplicate-execution prevention.
- CASE-15 is untrusted code attempting outbound network access or reading environment secrets.
- CASE-16 is out-of-order concurrent run completion with correct run identity.
- CASE-17 and CASE-18 are not defined by this canonical acceptance file.

The original P0-D source defines item 9 as an intentional malformed mission quarantined without blocking later queue work. Item 10 is exact-result publication and duplicate/idempotent replay. They are not a cancel-versus-timeout race or a worker-disconnect state machine. Preserve the existing crosswalk split: P0-D-10a ambiguous replay is adjacent to CASE-13; P0-D-10b run identity/order is adjacent to CASE-16; exact durable publication remains RevDev-specific. P0-D-09 remains unmapped.

### 10.3 Engineering findings retained, with corrected scope

**A. Applied-policy barrier before untrusted execution: ACCEPT as a real provider-boundary requirement.**

Gemini's Daytona v2 example is materially supported by the current official Daytona v2 Network Limits documentation: policy updates to an existing sandbox are stored immediately but applied in the background; a policy read exposes both desired and applied policies/revisions, and the update can remain pending until enforcement catches up. The documentation recommends checking connectivity before critical work. This validates the race for an update-on-an-existing-sandbox flow, not a claim that every provider or create-time policy has the same race.

Required design: apply the restrictive policy during sandbox creation where supported. If changing an existing sandbox, do not dispatch untrusted code until a fresh authoritative read confirms the exact required policy and revision are applied. A pending, stale, missing, or mismatched applied policy must fail closed. An ETag/If-Match token protects a conditional update from lost-update races; by itself it does not prove that the data plane is enforcing the policy. A probe is useful corroboration but is not proof against every protocol, address family, DNS route, or bypass path. This is a D-05 / LOOP-12 / CASE-15 concern, not an AWC-008 mapping.

The current Modal documentation fetched for this review documents create-time `block_network` and outbound allowlist options, but does not substantiate Gemini's specific asynchronous-update timing claim for Modal. Keep the race provider- and operation-specific unless provider documentation and a real adapter test establish it.

**B. Resource-limit enforcement and containment: ACCEPT as an important LOOP-12 evidence gap, not an AWC fixture.**

LOOP-12 already requires a disposable constrained runtime with egress denied by default and resource limits enforced outside user code. A fake adapter returning MEMORY_EXCEEDED is not evidence that a host-side or guest-side limit is actually active. Future provider/runtime proof must identify the real enforcement boundary and show that the workload cannot exhaust or kill the orchestration worker/host outside its sandbox. Use the selected provider's authoritative resource telemetry and scoped before/after counters where available; do not assume every provider exposes Linux cgroups.

Technical correction to Gemini's example: Linux pipe capacity is not a generic silent truncation threshold. A write to a full pipe blocks, or fails for nonblocking I/O. A collector may separately drop, cap, or lose data. `RLIMIT_FSIZE` limits file growth and can cause SIGXFSZ (or EFBIG when the signal is handled); it is not a stdout-pipe cap. A bare SIGKILL does not uniquely identify OOM. If cgroup v2 is the actual enforcement mechanism, record the relevant cgroup identity, configured limit, and scoped event-counter delta; distinguish hierarchical `memory.events` from local `memory.events.local`. Do not treat a global or pre-existing counter as proof that this attempt hit the limit.

**C. Runtime, stream-capture, collector, and display truncation: ACCEPT; refine, do not replace PC-LC-05.**

The existing plan already requires separate execution outcome, limit enforcement, termination evidence, and collection/presentation truncation. Extend evidence detail to distinguish: (1) an enforced execution/resource limit and its actual termination effect, (2) process-stream capture/transport interruption or reader failure, (3) collector/retention cap or storage loss, and (4) display/viewport shortening. Preserve retained-byte counts, the affected stream, and the observing component. No single `is_truncated` flag can establish where data was lost. A confirmed EXIT_ZERO must remain an observed execution fact even when collection is partial; the user-facing verdict then follows the applicable case's explicit evidence requirements.

**D. Execution outcome versus cleanup/teardown: ACCEPT as a separation requirement, already represented in the current semantic matrix.**

Preserve a trusted child EXIT_ZERO/EXIT_NONZERO independently from cleanup state. A provider delete timeout or HTTP 500 after a confirmed exit must not rewrite the child exit code. Cleanup may be UNKNOWN, FAILED, or pending reconciliation, and artifact release remains denied while a mandatory cleanup/release gate is unresolved. Gemini's phrase "Axis B verdict INCOMPLETE" is too imprecise: execution outcome, evidence quality, user-facing verdict, job disposition, cleanup state, and artifact-release decision are separately represented in the current matrix, not a simple pair of axes. The matrix already says EXIT_ZERO with a missing mandatory gate is INCOMPLETE while preserving EXIT_ZERO.

**E. Request fingerprint and durable idempotency: ACCEPT; extend the test detail.**

This is already a proposed D-06 requirement and PC-DB-01/PC-AD-01 concern. The reservation must be tenant-scoped and atomic. Same key plus same canonical semantic request fingerprint resolves to the original job/attempt; same key plus changed fingerprint conflicts before dispatch. The fingerprint should cover the complete execution-relevant request, including normalized inputs/files, runtime/entrypoint, requested limits, and policy revision, not just a loosely serialized text payload. After lost acknowledgement, UNKNOWN lookup must never trigger blind redispatch. Prove this with database concurrency/crash/restart tests; fake adapters alone do not prove it.

**F. Producer authority and cross-attempt correlation: ACCEPT; retain the existing PC-LC-03/04 design.**

Attempt identity must bind tenant, job, attempt, source namespace, event identity, sequence, and relevant policy revision before reduction. A late event from attempt N must not enter attempt N+1's active result. Identical replay is idempotent only within the same scoped identity; changed payload under the same identity is a conflict. The valid producer must be authenticated at the trusted boundary. A cryptographic signature is one possible mechanism only if key ownership, rotation, verification, and source binding are defined; a self-asserted role or signed but untrusted client header is insufficient. Do not mandate signatures as the only design.

**G. Artifact integrity and current release authorization: ACCEPT; this is already a contract rule that needs explicit regression coverage.**

The current execution contract already requires a fresh release decision and re-checks current authorization, run/attempt association, trusted manifest, quarantine/lifecycle state, safe object identity, size/type/path policy, and exact immutable bytes at release time. D-07 records this as proposed and NOT RUN. Add cases for interrupted/partial writes, checksum mismatch, changed bytes after manifest creation, stale authorization/policy, wrong tenant/run/attempt, and quarantined artifacts. A partially written or digest-mismatched artifact must not be published or streamed. Content scanning for a private key or other sensitive pattern is required only if an explicit release policy defines that scanner, its version, coverage, and failure semantics; do not imply such a scanner already exists or is complete.

**H. Delayed cost telemetry: RETAIN AS A FUTURE, SEPARATE REQUIREMENT.**

This is not the existing OBS-03 (which is the streaming-redactor carry/token-length finding) and it does not map to AWC-012 or LOOP-14 as an equivalence. If a provider is selected later, distinguish measured resource usage, estimated cost, provider-reconciled billing, and unknown/pending cost. Never show a delayed invoice as final zero spend. This remains a future adapter/persistence design item and is blocked by the current $0/no-provider/no-workload constraint.

**I. Untrusted stdout containing control-shaped JSON: ACCEPT as a useful negative test.**

Printed JSON, fake exit codes, and strings such as `{"verdict":"PASS"}` remain untrusted program output. They must never become lifecycle events or authoritative report fields. The transition matrix already states this trust rule; add an explicit pure-helper/adapter regression that keeps such bytes in stdout and leaves authoritative state unchanged.

### 10.4 Revised cross-project disposition

- No AWC-to-LOOP/CASE mapping is changed by Gemini's response.
- No canonical LOOP/CASE ID or P0-D item is renamed, split, or redefined.
- The P0-D-10a/10b/10c split remains as documented in Section 8.3.
- Existing OBS-01 through OBS-06 retain their original source meanings. Gemini's six differently labelled observations are treated as engineering suggestions, not as a second definition of those OBS IDs.
- The new regression additions are supplementary test-design IDs only. They do not become AWC fixtures, canonical LOOP/CASE acceptance, P0-D canaries, or proof of implementation.
- No provider, storage system, runtime, billing mechanism, authentication scheme, or integration topology is selected.

### 10.5 External technical references checked

- Daytona v2 Network Limits: https://www.daytona.io/docs/en/v2/network-limits/ (v2 documentation labels itself alpha; policy updates on an existing sandbox are asynchronous and expose desired/applied revisions).
- Linux `pipe(7)`: https://man7.org/linux/man-pages/man7/pipe.7.html (full pipes block writers or fail for nonblocking I/O).
- Linux `getrlimit(2)`: https://man7.org/linux/man-pages/man2/getrlimit.2.html (RLIMIT_FSIZE limits file growth and SIGXFSZ behavior).
- Linux cgroup v2: https://docs.kernel.org/6.9/admin-guide/cgroup-v2.html (memory.max and memory.events / memory.events.local semantics).
- Modal networking and security: https://modal.com/docs/guide/sandbox-networking (the fetched page documents create-time network-block and allowlist options; it did not substantiate the specific asynchronous update claim attributed to Modal).

**Verification status:** Source and documentation inspection only. No tests, provider calls, sandbox workloads, runtime experiments, Actions, source/test changes, canonical acceptance changes, PR edits, merges, deployments, or spend occurred. All proposed acceptance and provider/runtime evidence remains NOT RUN; PC and hosted provider state remain UNKNOWN/unselected.


## 11. Regression-specification de-duplication and authoritative checklist alignment

A further source pass checked the Gemini-derived PC-EXT suggestions against the existing PocketCode research checklists. The detailed checklists predate this response and remain the authoritative research/test specifications:

- D-05 policy barrier: `AI_COLLAB/ADAPTER_BOUNDARY_DECISION_GATE_20261029.md`, PBR-01..07 and PF-01..05. PBR already rejects stale/pending/missing/mismatched policy before dispatch, tests revision races and concurrent starts, and requires an actual conditional/immutable policy binding. PF already separates canonical request fingerprint from applied-policy proof.
- D-06 dispatch recovery: `AI_COLLAB/IDEMPOTENCY_RECOVERY_FALSIFICATION_CHECKLIST_20261029.md`, DR-01..12. It already covers tenant-scoped semantic fingerprints, atomic reservation, concurrent requests, crash points, ambiguous ACK, lookup UNKNOWN, lease expiry, recovered-attempt identity and tombstone retention.
- D-07 release: `AI_COLLAB/ARTIFACT_RELEASE_FALSIFICATION_CHECKLIST_20261029.md`, AR-01..14. It already covers authorization revocation, wrong tenant/job/attempt, immutable digest/object mutation, incomplete manifests, quarantine, size/type/path, active content, streaming races, ranges, non-disclosure and concurrent quarantine/replacement.
- D-08 report persistence: `AI_COLLAB/REPORT_HISTORY_PERSISTENCE_FALSIFICATION_CHECKLIST_20261029.md`, RH-01..14. In particular RH-05/06 preserve later cleanup/contradiction observations as new immutable versions; RH-07/08/13 test crash and ambiguous commit; RH-12 addresses cross-store report/artifact publication.
- Provider-neutral operation sketch: `AI_COLLAB/PROVIDER_NEUTRAL_BOUNDARY_CONTRACT_SKETCH_20261029.md`, Sections 3–8. It separates request fingerprint from actual applied policy evidence, authenticates and binds evidence before reduction, and requires release to use the exact immutable object version.
- General security requirements: `SECURITY.md`; provider evaluation: `RESEARCH/EXECUTION_PROVIDER_RESEARCH.md`. Both remain design/evaluation sources, not evidence of any selected provider.

Therefore PC-EXT-01, PC-EXT-03 and PC-EXT-07 in regression-plan Section 8 are traceability wrappers around existing PBR/PF, AR and DR requirements, not new parallel acceptance suites. Their examples should be added to the corresponding existing test rows only where they contribute a missing negative case. PC-EXT-02 remains a real provider/runtime proof-planning gap under LOOP-12. PC-EXT-04 remains a focused teardown/orphan reconciliation gap; it should preserve the existing multi-field projection semantics and add actual provider deletion/termination evidence when a boundary is selected. PC-EXT-05 is future cost observability and remains blocked. PC-EXT-06 is additional hostile stdout data for existing producer-authority/terminal-observation tests, with TPM-15 as the report-matrix trace.

The readiness backlog confirms the dependency order: WP-03 policy barrier (D-05/PBR/PF), WP-04 durable reservation (D-06/DR), WP-05 trusted evidence/report history (D-04/D-08/RH), and WP-06 artifact publication/release (D-03/D-07/AR). It explicitly keeps these BLOCKED until the relevant selected boundary and actual integration evidence exist. Do not create a second test framework or treat the PC-EXT labels as owner decisions.

This pass is documentation cross-reference only. No owner decision, canonical acceptance text, source/test, provider, store, runtime, PR, queue, Actions, merge, deployment or spend changed. All linked checklists and test suites remain SPECIFIED ONLY / NOT RUN where stated.


## 12. Resource containment and teardown source audit (2026-11-01)

The focused follow-up is recorded in [RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md](RESOURCE_CONTAINMENT_AND_TEARDOWN_EVIDENCE_REVIEW_20261101.md). It strengthens PC-EXT-02 and PC-EXT-04 without creating or remapping canonical acceptance IDs.

Source-grounded corrections:
- cgroup v2 `memory.max` is a hard memory boundary, but some allocation failures return `-ENOMEM` rather than causing OOM kill; do not require every fixture to have the same terminal signal.
- Use `memory.events.local` for local cgroup event attribution. Hierarchical `memory.events` may include descendant events.
- `memory.swap.max` is a separate control. `memory.high` is a throttle/reclaim boundary, not a kill threshold.
- `cpu.max` is bandwidth quota/period, not a wall-clock timeout. `pids.max` counts tasks/TIDs.
- `io.max` limits BPS/IOPS, not disk capacity. `RLIMIT_FSIZE` limits individual files, not total workspace size.
- `cgroup.kill` sends SIGKILL to the cgroup subtree; `cgroup.events: populated=0` reports no live processes in that subtree. Neither proves a cloud sandbox object or its separately attached volume/snapshot has been deleted.
- Firecracker's production guidance calls for Jailer or equivalent constraints, seccomp, cgroups/namespaces, privilege dropping and protected paths. The Jailer docs leave cleanup to the operator and warn of `notify_on_release` race conditions.
- Daytona v2 documents asynchronous delete progression (`destroying` to `destroyed`); the call returns when teardown starts. Stable v0 delete is fire-and-forget unless its wait option is used. These are version-specific API semantics, not interchangeable.
- Modal distinguishes CPU/memory request from hard limits and documents outbound public-IP access by default. Its dynamic network-policy update is Alpha and domain allowlist Beta.
- Cloudflare documents immediate destroy and warns not to rely on process cleanup handlers; its current sandbox product is on Workers Paid.
- E2B describes per-sandbox Firecracker microVMs, but its public security page alone does not prove PocketCode's exact teardown wait/lookup or resource-containment requirements.

**Result:** PC-EXT-02 and PC-EXT-04 remain provider/runtime proof gaps. The new RES/TDN labels are local research test-design identifiers only. No provider is selected and no runtime claim is made. All cases remain NOT RUN.
