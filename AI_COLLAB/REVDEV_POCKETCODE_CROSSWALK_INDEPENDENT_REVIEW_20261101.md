# RevDev ↔ PocketCode Crosswalk — Independent Static Review (2026-11-01)

**Status:** ChatGPT independent desk review completed; Claude/Gemini reviews still outstanding. This is a review note, not approval of a shared contract, implementation, or combined acceptance suite.

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
