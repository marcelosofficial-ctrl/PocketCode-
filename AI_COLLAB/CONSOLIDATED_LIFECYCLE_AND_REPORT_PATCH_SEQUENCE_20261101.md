# PocketCode — Consolidated lifecycle and report-boundary patch sequence

**Date:** 2026-11-01  
**Status:** Technical review plan only. NOT OWNER-APPROVED; NOT IMPLEMENTED; NOT RUN.  
**Documentation branch:** `pocketcode-execution-boundary-crosswalk-2026-11-01`  
**Purpose:** Turn the verified lifecycle-descendant, event-reducer, and report-confidentiality findings into one dependency-ordered engineering plan without duplicating canonical acceptance or silently deciding owner-open semantics.

## 1. Executive decision

Do not merge or combine PR #2, PR #3, and the research branch. Keep their source histories isolated until a reviewed integration plan exists. The lifecycle-fingerprint branch is a direct 34-commit descendant of PR #3's pinned head, but it is still a separate branch and has not been accepted or tested here.

The next engineering work should be split into three independently reviewable layers:

1. **Pure lifecycle helper hardening** on the lifecycle descendant: strict input validation and any still-open helper edge cases, with no verdict-policy changes.
2. **Trusted event acceptance and coordinator reduction**: scope binding, immutable event snapshots, exact replay/conflict semantics, and explicit sequence-collision diagnostics. This is blocked on D-04 owner semantics and a trusted ingress design.
3. **Report/output integration**: one trusted collection/redaction boundary and a typed report projection. The PR #2 formatter must not be assumed protected by PR #3's separate redactor.

This ordering prevents a helper-only patch from being mistaken for coordinator, persistence, provider, confidentiality, or device proof.

## 2. Source pins and branch topology

| Item | Exact reference | Meaning |
|---|---|---|
| PR #2 branch | `chat-continuity-report-regressions-2026-10-26` at `eb8b7ea83cb0e8fe1880351276c485b761431791` | Report formatter source under review; open draft, not merged |
| PR #2 formatter | `scripts/report_contract.py`, blob `e9d944a722c2fac5279952696528da72a7011af3` | Escaping/truncation, but no redaction call |
| PR #3 base | `pocketcode-pass0-audit-2026-10-26` at `0ddcc0bc97bac5d446aefedf3d71f99411bd841d` | Original lifecycle audit branch; open draft, not merged |
| Lifecycle descendant | `lifecycle-fingerprint` at `26de6bb29020d6781d342c691e430616a4321083` | 34 commits ahead, 0 behind PR #3 base; source candidate only |
| Descendant lifecycle helper | `scripts/lifecycle_contract.py`, blob `316345341603848c4a86a6a82e533daa796c7695` | Current source reviewed for Sections 17–19 |
| Research branch | `pocketcode-ai-workflow-director-research-2026-10-28` at `97db362e3f57c4d605d5d84a28d5cbb264c23c24` | Separate divergent design/test branch; not cumulative with PR #2/#3 |
| Current documentation branch | `pocketcode-execution-boundary-crosswalk-2026-11-01` | Documentation-only continuity branch |

**Mandatory refresh rule:** before any source patch, fetch the live branch HEAD and exact source/test blobs again. If a pin changed, stop and re-review the changed function and its tests. The old G-01..G-03 patch packet pins the PR #3 base, not the lifecycle descendant, so it is a test-design reference, not a patch-ready authorization against the descendant.

## 3. Workstream A: pure lifecycle helper hardening

Target only the lifecycle descendant after source refresh and explicit authorization. Do not put these changes into PR #2 or the research branch.

| Finding | Descendant status | Required action | Existing design reference |
|---|---|---|---|
| G-01 malformed `limit_violated` / `output_truncated` values | Still accepts truthy malformed values | Choose validation policy, then test both flags independently before any disposition branch | `G01_G03_PATCH_READY_TEST_SPEC_20261029.md`; `G01_G03_RECOMMENDED_BEHAVIOR_AND_PROOF_GATES_20261029.md` |
| G-02 `OutputBudget` cap types | Still only checks `cap <= 0`; bool/float not explicitly rejected | Require exact documented positive-integer behavior at construction; test both caps independently | Same G-01..G-03 references |
| G-03 required fingerprint fields | Descendant has already added blank-after-strip rejection and runtime normalization validation | Do not reapply. Verify its tests and preserve fingerprint version/normalization | Section 17 of `POCKETCODE_EXECUTION_BOUNDARY_TRUST_CROSSWALK_20261101.md` |
| Reservation identity inputs | Descendant has already added nonblank string validation | Do not duplicate. Preserve tenant/key/fingerprint/job identity checks | Section 17.2a |
| Tombstone validation/retry | Descendant has already added identity/epoch validation, live conflicting-fingerprint rejection, and no-shortening retry behavior | Do not duplicate. Expired-key reuse semantics still need an authoritative time rule before any extension | Section 17.2 |
| G-07 Windows superscript device-name aliases | Prior base-branch audit identified COM¹/²/³ and LPT¹/²/³ gaps; descendant status has not been established by the current exact source review | Recheck `_canonical_input_name()` and current tests before deciding whether this remains open; do not assume base finding still applies | `G01_G08_EDGE_CASES_AND_PATCH_REVIEW_NOTES_20261029.md` |
| G-08 tombstone expiry/key reuse | Descendant improves repeated same-fingerprint retention and rejects live conflicting reuse; API time semantics remain a separate question | Do not expand behavior until the contract defines trusted current time vs event time and expired-key replacement | Same G-01..G-08 note |

### A1. Decisions required before tests encode behavior

- **G-01:** The recommendation is exact booleans with `TypeError` before deriving a disposition. This remains a recommendation, not an owner decision. Alternative fail-closed typed validation is possible but must preserve the distinction between malformed API input and an actual incomplete run.
- **G-02:** Recommended: reject bool/non-integer with `TypeError`, integer values <= 0 with `ValueError`. Confirm compatibility with project conventions before implementation.
- **G-08:** Define whether a repeated same-fingerprint add is a no-op or extends retention to the maximum deadline, and define how `add()` knows a prior tombstone is expired. A supplied `deleted_at` is not automatically trusted current acceptance time.
- **D-01:** Do not alter valid limit semantics in the G-01/G-02 patch. Runtime-enforced limit termination, collection-only output caps, and report-display truncation are distinct facts. The user-facing mapping for confirmed limit-caused termination remains owner-open.

### A2. Bounded patch and proof

1. Refresh lifecycle branch HEAD, helper blob and test blob.
2. Resolve A1 choices that affect assertions.
3. Add tests first, then the smallest helper changes.
4. Keep G-01, G-02, G-07 and any G-08 change independently reviewable.
5. Run only an explicitly authorized local pure unit suite when an environment is available. Record interpreter, command, revision, count, failures and exit code.
6. Do not infer process termination, policy enforcement, durable idempotency, or runtime safety from these helper tests.

## 4. Workstream B: event identity, reducer integrity and coordinator

**Status:** blocked on D-04 semantics and a trusted ingress boundary. The lifecycle descendant's event-shape validation is useful but insufficient.

### B1. Required order

1. **Owner resolves D-04:** define authenticated source namespace, tenant/job/attempt binding, policy-revision relationship, immutable event fields, exact replay identity, changed-content conflict behavior, and sequence-collision semantics.
2. **Trusted ingress binds scope:** authenticate the producer and compare every event to the expected tenant, logical job, attempt, source namespace and relevant policy revision before reduction. Never trust a user-supplied `trusted=true` flag.
3. **Canonical immutable snapshot:** validate the complete schema and create a canonical immutable representation before it enters accepted evidence or duplicate-comparison state. A shallow dict copy is insufficient; a deep copy alone is not a schema/canonicalization policy.
4. **Reducer diagnostics:** preserve exact replay as idempotent; represent changed content under the same scoped source event ID as a conflict; expose every same-sequence collision with references to both records. A deterministic sort tie-break must never imply one event is authoritative.
5. **Coordinator fake tests:** assert event log, identity scope, accepted evidence, conflict/collision diagnostics, and no duplicate dispatch. Then test durable persistence separately.

### B2. Existing acceptance IDs to reuse

- **COORD-11:** exact replay, scoped source-ID conflicts and sequence collisions. The current source finding maps directly to its sequence-collision and scoped-replay setups.
- **COORD-12:** mutation of nested payload after acceptance. The reducer's shallow-copy behavior is the concrete falsification target.
- **FLA-04/06/07:** retain existing traceability mappings from the research-branch function-level audit. Do not create duplicate finding IDs.
- **D-04:** remains OPEN. Do not freeze event schema or claim tenant-safe replay until the owner decision and ingress binding are specified.

Add focused assertions to these existing cases rather than renumbering them. At minimum:
- mutate nested dict and list members after reduction; accepted evidence and derived outcome must remain unchanged;
- mutate invalid-event diagnostic inputs after reduction if diagnostics are retained as evidence; returned diagnostics must remain stable;
- submit two distinct IDs with the same sequence for nonterminal/nonterminal and terminal/nonterminal combinations; both colliding records must be visible in deterministic diagnostics;
- submit exact replay within one scope and changed content under the same scoped source ID; distinguish replay from conflict;
- submit an otherwise identical event under another tenant/job/attempt/source scope; no cross-scope acceptance or disclosure.

### B3. Proof boundary

Fake-coordinator tests prove coordinator branching only. They do not prove authenticated provider identity, durable append uniqueness, cross-process race safety, atomic persistence, or restart recovery. Those require the G3/G4 persistence and provider gates in the implementation-readiness backlog.

## 5. Workstream C: output collection, redaction and report projection

**Status:** integration gap. PR #2 and PR #3 remain separate. No complete coordinator-to-formatter path has been verified.

### C1. Architecture decision

Establish one trusted collection boundary that owns:
- byte limits and observed/retained accounting;
- per-stream collection state and provenance;
- streaming redaction policy and its explicitly bounded coverage;
- separation of runtime-enforced termination from collector-only caps;
- separation of execution collection from report/UI display truncation.

The report formatter should consume a typed, already-classified collection/report projection from the trusted coordinator. It must not be treated as an authenticator or accept arbitrary provider dictionaries as authoritative evidence.

Redaction is defense in depth, not a guarantee against unknown secret formats. The primary control is to prevent credentials from entering untrusted execution environments and minimize what is collected.

### C2. Required semantic distinctions

Preserve independently:
- raw execution outcome and trusted child exit evidence;
- job disposition and user-facing verdict;
- termination and cleanup state;
- each stream's collection state, including complete-empty vs unavailable vs partial failure vs runtime/policy truncation;
- report/UI display truncation;
- artifact release decision.

A collection cap must not be reported as proof the process was terminated. A renderer's display truncation must never become a runtime limit event. A required stream's missing/partial state may block PASS only according to the acceptance case's explicit output requirements. Do not impose a universal stdout/stderr completeness rule.

### C3. Focused report-projection tests

These are **proposed new test labels**, not existing canonical LOOP/CASE or coordinator IDs. Reuse them only if no conflicting IDs exist when implementation begins:

| Proposed label | Fixture | Required assertion |
|---|---|---|
| REPORT-SEC-01 | Secret-like marker appears in stdout and stderr across chunk boundaries | Configured redactor behavior is tested at and around its supported maximum/carry window; uncovered patterns are explicitly not claimed protected |
| REPORT-SEC-02 | Secret-like marker appears in task summary, check name/provenance/detail, filename, note and evidence metadata | No raw sensitive value is reintroduced by report projection; each field has a documented classification/handling rule |
| REPORT-SEC-03 | Formatter receives arbitrary raw/unclassified provider mapping | Reject or require a typed trusted projection; formatter must not imply authentication |
| REPORT-STATE-01 | COMPLETE empty stream vs UNAVAILABLE vs PARTIAL_FAILURE vs policy/runtime cap | Distinct state and reason survive formatting |
| REPORT-STATE-02 | Collector cap reached while trusted child EXIT_ZERO is independently confirmed | Preserve EXIT_ZERO; do not infer process termination; disposition follows case-specific required-output policy |
| REPORT-STATE-03 | Renderer shortens report after successful execution | Preserve execution verdict and mark display truncation only |
| REPORT-STATE-04 | Confirmed runtime-enforced output limit terminates execution | Preserve authoritative limit event, termination evidence and D-01-dependent verdict mapping separately |

These tests supplement, not replace, the existing PR #2 formatter tests, PR #3 redactor/output-budget tests, COORD tests, and canonical LOOP/CASE acceptance.

### C4. Integration order

1. Define the typed output/report envelope without claiming it is a frozen public API.
2. Define per-field trust/classification and collection provenance.
3. Wire the selected collector through one trusted coordinator projection to the formatter.
4. Test that all rendered fields use the intended projection and cannot bypass redaction/classification.
5. Test chunk/carry boundaries, maximum token lengths and over-limit cases; document unknown-pattern limitations.
6. Only then consider source integration across the PR #2/#3 histories, with a reviewed minimal merge/cherry-pick plan. Do not cherry-pick the redactor helper alone and claim formatter protection.

## 6. Cross-workstream dependency graph

| Order | Work | May proceed now? | Blocking condition | Evidence label on completion |
|---|---|---|---|---|
| 0 | Refresh exact branch/source/test pins | Yes | None | VERIFIED IN SOURCE |
| 1 | Pure helper G-01/G-02 decisions and tests | Design yes; patch only with authorization | Owner/error-policy choice | UNIT TESTED |
| 2 | Recheck G-07 and G-08 on descendant | Static review yes | G-08 time semantics before behavior change | VERIFIED IN SOURCE / UNIT TESTED |
| 3 | Resolve D-01 and D-04 | Decision preparation yes | Explicit owner decision | OWNER-DECIDED |
| 4 | Trusted ingress + immutable event snapshot + collision diagnostics | Design only until D-04 | Authenticated scope and schema | UNIT TESTED, then FAKE-ADAPTER TESTED |
| 5 | Typed output/report projection and redaction data flow | Design only | Envelope/classification decisions; integration ownership | UNIT TESTED, then FAKE-ADAPTER TESTED |
| 6 | Durable event/report/idempotency persistence | Blocked | Selected store, identity and transaction contract | PERSISTENCE INTEGRATION TESTED |
| 7 | Provider policy barrier and dispatch reconciliation | Blocked | Selected provider/boundary and $0 approval | PROVIDER INTEGRATION TESTED |
| 8 | Artifact release and device workflow | Blocked | Actual store/API/HTTP and device availability | STORE/API/HTTP INTEGRATION TESTED; DEVICE ACCEPTED |
| 9 | Canonical LOOP/CASE run | Not ready | Integrated path and exact build/runtime | CASE/LOOP evidence per case |

The sequence intentionally separates independent pure-helper work from D-01/D-04-dependent semantic behavior. Do not let an easy unit patch create the impression that blocked integration gates have advanced.

## 7. Review assignments

- **Claude, lead developer:** review the exact descendant source and propose the smallest implementation diff per workstream, with touched functions, test names, dependency and migration risks. Do not modify PR #2/#3 until branch topology and owner decisions are reconciled.
- **Gemini, independent security/spec auditor:** adversarially challenge event scope binding, mutable evidence, sequence collisions, report-field redaction bypass, output-limit semantics, and any claim that fake tests prove provider or persistence behavior.
- **ChatGPT, continuity and acceptance coordinator:** reconcile both reviews against pinned source, retain disagreement, map findings to existing IDs, and verify evidence labels. Do not claim tests ran without an actual execution record.
- **Project owner:** decide D-01/D-04 and any G-01/G-08 policy choices. No implied approval from silence.

## 8. Explicit non-goals and stop rules

This packet does not:
- change canonical `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` or `PRODUCT/EXECUTION_CONTRACT.md`;
- authorize code changes, merge, PR creation, Actions, deployments, provider selection, hosted workloads, accounts, billing or spending;
- prove provider isolation, network/egress enforcement, durable uniqueness, transactional history, artifact safety, HTTP release behavior or device acceptance;
- declare the lifecycle descendant accepted merely because it is ahead of PR #3;
- resolve D-01..D-04 on behalf of the owner.

If exact source pins change, re-review. If a test depends on unresolved owner semantics, keep it specified but do not encode one alternative as accepted behavior. If an integration boundary cannot be evidenced, record BLOCKED/NOT RUN.

## 9. Current evidence status

- Lifecycle descendant: static source review only; 30 test methods counted in source versus 24 at PR #3 base; neither count means executed tests.
- PR #2 formatter: static source review only; escaping/truncation present, no formatter redaction call.
- PR #3 redactor/output budget: static source review only; configured-pattern, bounded best-effort redaction; no verified end-to-end path into PR #2 formatter.
- Event reducer: static source review only; shallow nested references and incomplete sequence-collision diagnostics identified.
- Coordinator, persistence, provider, artifact release, HTTP and device integration: NOT RUN / UNKNOWN.
- Canonical acceptance: unchanged.
- No implementation source or test file changed in this work. No test command, workflow, provider call, workload, deployment or merge was performed.

## 10. References

- `AI_COLLAB/POCKETCODE_EXECUTION_BOUNDARY_TRUST_CROSSWALK_20261101.md` Sections 16–19.
- `AI_COLLAB/G01_G08_EDGE_CASES_AND_PATCH_REVIEW_NOTES_20261029.md`.
- `AI_COLLAB/G01_G03_PATCH_READY_TEST_SPEC_20261029.md`.
- `AI_COLLAB/G01_G03_RECOMMENDED_BEHAVIOR_AND_PROOF_GATES_20261029.md`.
- `AI_COLLAB/COORDINATOR_FAKE_ADAPTER_TEST_PLAN_20261029.md`.
- `AI_COLLAB/IMPLEMENTATION_READINESS_BACKLOG_20261029.md`.
- `AI_COLLAB/ADAPTER_RESULT_ENVELOPE_AND_FAKE_PROTOCOL_20261029.md`.
- `AI_COLLAB/OUTPUT_STATE_AND_VERDICT_RELEASE_CROSSWALK_20261029.md`.
- `AI_COLLAB/SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md`.
- `AI_COLLAB/CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md`.
