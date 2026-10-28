# AI Workflow Director — Bounded Implementation Plan

**Date:** 2026-10-28  
**Status:** Planning proposal only. No implementation authorization is inferred.  
**Parent:** [Master research](MASTER_AI_WORKFLOW_DIRECTOR_RESEARCH_20261028.md)  
**Acceptance authority:** [MVP feature slice](AI_WORKFLOW_DIRECTOR_MVP_SLICE_20261028.md)  
**Conformance:** [Test specification](AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md) · [Canonical fixtures](AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES_20261028.md)  
**Readiness:** [Pre-implementation audit](AI_WORKFLOW_DIRECTOR_READINESS_AUDIT_20261028.md) · [Contract decision register](AI_WORKFLOW_DIRECTOR_CONTRACT_DECISION_REGISTER_20261028.md)

## 1. Goal and boundaries

Prepare the smallest useful, provider-neutral AI Workflow Director slice for a phone-first workflow. It builds task packets and continuation capsules from explicitly supplied input, lets the user review/edit/copy the result, and never pretends a prompt claim is verified execution evidence.

This is not a PocketCode app implementation specification for every future execution backend. It is a staged plan for the local/offline Director feature only.

**Hard boundaries:** $0; no provider APIs, model calls, credentials, network access, background clipboard reading, hidden cross-app access, code execution, repository mutation, PR operations, deployments, or telemetry. No implementation starts until the owner explicitly authorizes it. Manual copy/paste remains the baseline.

## 2. Work packages and acceptance mapping

| Stage | Work package | Cases / evidence | Exit condition |
|---|---|---|---|
| G0 | Confirm scope and the few contracts needed by the selected v1 slice | MVP §9; D-01–D-08 | Explicit scope/contract approval; deferred features written down |
| G1 | Define typed input and pure normalization | AWD-01, AWD-02, AWD-05, AWD-06, AWD-16 | Required goal/profile validation; ordinary edge trimming; optional empties omitted; protected literals unchanged |
| G2 | Implement deterministic packet builder | AWD-01–AWD-09, AWD-13, AWD-15, AWD-16 | MVP section order; selected context only; constraints/acceptance/evidence preserved; omissions disclosed; no fabricated facts; count uses an approved convention |
| G3 | Implement capsule validator/builder and provenance rules | AWD-10, AWD-11, plus capsule matrix | Six statuses handled; DONE_VERIFIED requires concrete evidence; claims/unknowns are not promoted to verified facts; malformed inputs produce an explicit, non-destructive validation result |
| G4 | Add offline automated tests | AWD-01–16, determinism and protected-literal suites | All required assertions have runnable tests; test command/environment/output are recorded; no network or real external side effects |
| G5 | Add reviewable preview/edit/copy UI | MVP user journey; AWD-04, AWD-08, AWD-15 | User can inspect and edit exact output before copying; no automatic transfer; size label says characters, not tokens/cost |
| G6 | Optional local redaction | AWD-12 | Only if explicitly included in scope: synthetic tests, configured patterns, visible redaction, best-effort warning, no false safety guarantee |
| G7 | Optional user-initiated sharing | AWD-14 | Only after separate approval and device verification; cancellation distinct from success; local copy retained; no automatic retry |
| G8 | Manual AI comparison | EVAL-01–EVAL-08; prioritize EVAL-06 | Separate baseline and prototype outputs saved; same app/model/conditions where possible; incomplete pairs marked; no benchmark claims from unsaved recollection |

G0–G5 are the proposed core. G6–G8 are separately gated and must not be smuggled into the initial implementation.

### Explicit acceptance traceability

| Acceptance ID | Planned work package | Required proof focus |
|---|---|---|
| AWD-01 | G1, G2, G4 | Lite packet is concise and preserves the concrete goal |
| AWD-02 | G1, G2, G4 | Selected context and acceptance criteria preserved; unselected context excluded |
| AWD-03 | G2, G4 | Careful profile states scope and verification honestly |
| AWD-04 | G2, G5, G4 | Review only does not authorize edits |
| AWD-05 | G1, G2, G4 | Empty optional sections omitted |
| AWD-06 | G1, G2, G4 | Protected literals remain exact |
| AWD-07 | G2, G4 | No runtime means no claimed PASS |
| AWD-08 | G2, G4, G5 | Omission is visible; no silent destructive truncation |
| AWD-09 | G2, G4 | Refuse quota evasion; offer compliant pause/resume |
| AWD-10 | G3, G4 | Capsule with no executed checks cannot be DONE_VERIFIED |
| AWD-11 | G3, G4 | Unsupported “tests passed” claim remains unverified |
| AWD-12 | G6 only, if approved | Configured synthetic match redacted; best-effort limits disclosed |
| AWD-13 | G2, G4 | Unknown provider capability stays unknown; copy/paste fallback remains |
| AWD-14 | G7 only, if approved | Cancellation is not success; local packet remains |
| AWD-15 | G2, G4, G5 | Size label says characters; count updates with the exact preview |
| AWD-16 | G1, G2, G4 | Explicit constraints take precedence over profile hint |

This mapping preserves the existing MVP IDs and meanings. A case assigned to an optional stage is **not** permission to include that stage in v1; it means the case remains deferred until the relevant scope gate is approved.

## 3. Proposed dependency order

1. **G0 — Scope gate:** Decide whether v1 includes capsule construction/validation alongside packet generation, and explicitly defer redaction/sharing unless approved.
2. **G1 — Input contract:** Define required fields, allowed profile values, optional field normalization, and a clear validation-error shape. Do not mutate protected spans.
3. **G2 — Packet core:** Implement as a pure local function with fixed configuration. Keep UI and adapters outside it. No dynamic provider lookups or auto-selection algorithm.
4. **G3 — Capsule core:** Preserve provenance and status semantics. Reject/flag unsupported verified status without inventing evidence. Avoid destructive normalization of unknown data.
5. **G4 — Tests:** Convert the canonical fixtures into executable tests only after the input/output contracts used by those tests are approved. Keep fake adapters and offline tests isolated from platform behavior.
6. **G5 — UI:** Wire preview/edit/copy only after pure-builder tests pass. The visible preview must be the same content the copy action uses.
7. **G6/G7 — Optional capabilities:** Add redaction and real sharing only after independent scope approval and focused security/platform review.
8. **G8 — Evaluation:** Run only when usage is available; stop at free-tier limits. A hand-authored prototype prompt is not product output and cannot prove product effectiveness.

## 4. Contract choices that can genuinely block the first slice

These are the smallest unresolved choices that affect externally observable behavior. Recommendations below are not approved defaults.

| Choice | Why it blocks code/tests | Recommended low-risk direction | May be deferred if… |
|---|---|---|---|
| Required input and invalid-input result | UI and builder need a deterministic response to missing/blank goal or invalid profile | Trim ordinary edge whitespace; reject a blank goal/unknown profile with a visible validation result; do not rewrite protected text | It cannot be deferred for a callable builder |
| Exact v1 feature boundary | Determines whether capsule and count behavior are acceptance requirements | Keep packet builder + capsule validator in the core only if both remain part of the agreed MVP; exclude redaction/share adapters from the first slice | Redaction, share UI, and provider guides are excluded |
| Profile copy and packet serialization | Needed for reproducible output; semantic rules exist but exact wording/encoding is not frozen | Freeze short versioned profile strings and section separators before exact snapshot assertions; retain semantic assertions for other behavior | Whole-string snapshot tests can wait, but production output still needs deterministic text |
| Character-count convention | “Character” count must be reproducible across platforms | Choose and document one convention; a Unicode code-point count is a simple candidate but may differ from user-perceived grapheme clusters | Numeric count is omitted from an explicitly narrower first increment |
| Capsule invalid/unknown fields | A validator must define how malformed status/evidence combinations are surfaced and whether export is blocked | Non-destructive validation error; never export a capsule as valid when required status/evidence invariants fail; preserve source for correction | Capsule import/export is removed from v1, which would change the proposed scope |
| Oversize input | Must avoid silently dropping protected content | Do not auto-summarize or truncate constraints, acceptance, or evidence; require user selection/edit and disclose omissions | Automatic ranking and exact warning copy can be deferred |

**Not blockers for the pure local core:** actual OS share sheet, provider-specific setup, live provider capability lists, paid APIs, automatic context ranking, and device-level integrations.

## 5. Test and evidence requirements

For each work package, completion evidence must include:

- exact source revision/commit;
- exact test command and environment;
- full pass/fail/skip counts and relevant output;
- explicit not-run items and limitations;
- fixture-to-test mapping for each AWD ID;
- confirmation that no prohibited network/provider/side effect occurred.

A code review or model assertion is not a test result. DONE_VERIFIED must never be inferred from a plan, an unexecuted test file, or an unsupported assistant statement.

## 6. Stop conditions

Stop before proceeding if:
- implementation authorization is absent or unclear;
- a contract choice would be guessed rather than approved;
- a test could contact a real provider/network or mutate a repository;
- a feature needs credentials, payment, device access, or an account connection;
- the available environment cannot produce reliable evidence.

When blocked, update the checkpoint with the exact missing decision/evidence; do not fabricate a result or broaden scope.

## 7. Current state

- This plan is a documentation artifact on the isolated research branch.
- The readiness audit and fixture catalogue are design/review documents only.
- AWD-01–AWD-16 remain **NOT RUN**; no implementation or executable tests are claimed.
- PR #2 and PR #3 remain separate and must not be changed by this work.
- The next real gate is explicit owner authorization plus the minimal G0 contract decisions—not another round of speculative feature design.
