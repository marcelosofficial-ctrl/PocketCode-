# PocketCode semantic decision crosswalk

Research-only index; no canonical changes, implementation, or tests.

| Decision | Current status | Source documents | Next action |
|---|---|---|---|
| PASS requires trusted completion and exit zero | Canonical | PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md; semantic decisions; transition matrix | Preserve mandatory evidence and contradictions |
| Nonzero exit remains FAIL if cleanup unknown | Proposed, consistent with canonical FAIL definition | Semantic decisions; transition matrix; COORD-02 | Keep cleanup separate and artifacts blocked |
| Provider failure with no child exit | Open, D-02 | Owner decision register; COORD-03 | Keep verdict INCOMPLETE and never invent exit code |
| Limit-caused termination vs capture-only cap | Open, D-01 | Owner register; semantic decisions; transition matrix; COORD-10; adapter envelope | Confirmed limit-caused runtime failure is a candidate FAIL under canonical wording, with `LIMIT_EXCEEDED` disposition; exact mapping remains owner-review. A capture cap with independent EXIT_ZERO follows case-specific collection rules; display-only truncation does not change verdict. |
| Collector truncation vs display truncation | Proposed distinction | Semantic decisions; coordinator plan; FLA-05/12 | Test as separate evidence states |
| Required output collection | Open, D-03 | Owner register; coordinator plan; adapter envelope | Define required streams and accepted partial capture per acceptance case/runtime. Required evidence can block PASS; optional diagnostics must not become an accidental universal gate. |
| Event ID scope / duplicate identity | Open, D-04; integration gap | FLA-04/06/07/08; COORD-05/11 | Define immutable fields and validate attempt binding |
| Policy revision at dispatch | Specified only; integration gap | Adapter decision gate; COORD-06 | Prove an enforceable revision barrier |
| Ambiguous acknowledgement recovery | Proposed; integration gap | COORD-07/08; cross-branch gap audit G4 | Verify durable uniqueness and no blind retry |
| Artifact release checks | Proposed; integration gap | COORD-09; transition matrix | Verify authorization and exact-byte integrity at release |
| Report history | Proposed; integration gap | Semantic decisions; transition matrix; FLA-10 | Define durable atomic versioning |
| Runtime/device test evidence | NOT RUN | Function-level audit; staged acceptance gates | Do not promote specs or helper tests into integration claims |

## Two immediate consistency tasks

1. Review the three limit cases now represented in the semantic note, transition matrix, adapter envelope, and COORD-10: limit-caused termination; collection-only cap with trusted EXIT_ZERO; display-only truncation. D-01 remains owner-open. Do not change canonical acceptance without separate approval.
2. Confirm D-03's per-case default: only streams/artifacts explicitly required by that acceptance case gate PASS/release; optional diagnostics can be incomplete without automatically making every run INCOMPLETE. Keep raw process outcome and collection state separate.

Evidence: static review only. No tests, implementation, provider/runtime selection, workload, account, billing, merge or deployment.
