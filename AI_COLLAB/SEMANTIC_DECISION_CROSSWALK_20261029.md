# PocketCode semantic decision crosswalk

Research-only index; no canonical changes, implementation, or tests.

| Decision | Current status | Source documents | Next action |
|---|---|---|---|
| PASS requires trusted completion and exit zero | Canonical | PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md; semantic decisions; transition matrix | Preserve mandatory evidence and contradictions |
| Nonzero exit remains FAIL if cleanup unknown | Proposed, consistent with canonical FAIL definition | Semantic decisions; transition matrix; COORD-02 | Keep cleanup separate and artifacts blocked |
| Provider failure with no child exit | Open, D-02 | Owner decision register; COORD-03 | Keep verdict INCOMPLETE and never invent exit code |
| Confirmed enforced limit verdict | Open, D-01 | Owner decision register; semantic decisions; transition matrix; COORD-10 | Canonical says confirmed runtime failure is FAIL; settle whether limit-triggered termination qualifies before freezing tests |
| Collector truncation vs display truncation | Proposed distinction | Semantic decisions; coordinator plan; FLA-05/12 | Test as separate evidence states |
| Complete output as universal PASS gate | Open, D-03 | Owner decision register; coordinator plan | Define required streams per acceptance case |
| Event ID scope / duplicate identity | Open, D-04; integration gap | FLA-04/06/07/08; COORD-05/11 | Define immutable fields and validate attempt binding |
| Policy revision at dispatch | Specified only; integration gap | Adapter decision gate; COORD-06 | Prove an enforceable revision barrier |
| Ambiguous acknowledgement recovery | Proposed; integration gap | COORD-07/08; cross-branch gap audit G4 | Verify durable uniqueness and no blind retry |
| Artifact release checks | Proposed; integration gap | COORD-09; transition matrix | Verify authorization and exact-byte integrity at release |
| Report history | Proposed; integration gap | Semantic decisions; transition matrix; FLA-10 | Define durable atomic versioning |
| Runtime/device test evidence | NOT RUN | Function-level audit; staged acceptance gates | Do not promote specs or helper tests into integration claims |

## Two immediate consistency tasks

1. Resolve D-01 and align semantic decisions, transition matrix and COORD expectations together. Do not change canonical acceptance without separate approval.
2. Resolve D-03 so output completeness is not accidentally imposed as a universal PASS gate. Distinguish required evidence from optional diagnostics.

Evidence: static review only. No tests, implementation, provider/runtime selection, workload, account, billing, merge or deployment.
