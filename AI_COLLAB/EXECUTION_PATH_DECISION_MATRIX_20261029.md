# PocketCode — execution-path decision matrix and first-proof checklist
**Date:** 2026-10-29  
**Status:** Research/design aid only. NOT RUN. No architecture/provider selected. No code, tests, provider workloads, installs, or canonical-contract/PR changes.

## Decision to make (two separate questions)

Do not collapse these into one architecture decision:

1. **Near-term practical proof:** Can an existing iPhone workflow run the fixed CSV task, preserve a real output file, and expose enough trustworthy evidence to teach us what the PocketCode user loop needs?
2. **Product architecture:** Does PocketCode eventually need its own execution service to provide reliable lifecycle evidence, isolation, limits, recovery, and authenticated artifacts that an on-device comparator cannot provide?

A successful comparator experiment can validate the user workflow without proving it is suitable as PocketCode's production execution backend. A failed comparator experiment does not by itself prove that a hosted service is necessary.

## Evidence-based path matrix

| Criterion | Existing iPhone Python app (Pyodios comparator) | Browser-local Pyodide | PocketCode-owned/provider-backed service |
|---|---|---|---|
| $0/no account or workload | Likely lowest-friction to inspect; no new provider workload required for a manual comparator | No provider required, but actual browser workflow remains unverified | Cannot assume $0 until a provider's current limits, billing, and failure behavior are checked; no workload authorized |
| iPhone-first workflow | Public-source review documents local editing/run/files/import-export; hands-on status unknown | Possible in principle; iOS file import/export and output handling unverified | Better potential for consistent server-side controls, but mobile UX/API is not proof of a secure runner |
| Real output artifact | Documentation says real files and export; exact CSV task not tested | Must demonstrate file creation and export, not just console JSON | Contract requires artifact association/access controls; no adapter/storage tested |
| Authoritative run evidence | Unknown: process exit, timeout/termination, bounded streams, collector failure | Unknown: runtime status and whether execution can be reliably interrupted | Desired contract exists, but adapter must map provider facts honestly; none selected/tested |
| Isolation and resource limits | Local app/runtime behavior and limits not established by this review | Browser sandbox is not equivalent to an application-level resource/security guarantee | Must verify provider isolation, limits, network policy, cleanup, and timeout behavior empirically |
| Recovery/idempotency | Useful for user-loop learning, not proof of remote job recovery | No durable remote-job boundary implied | Must resolve ambiguous submit/response by authoritative lookup; never blindly redispatch |
| What a positive result proves | The basic phone-based coding and artifact loop is feasible in this app | A browser-local loop is feasible under tested iOS constraints | Only the tested provider/adapter configuration and cases—not general security or production readiness |
| What it cannot prove | PocketCode production isolation, backend lifecycle contract, durable recovery | Server isolation, durable recovery, provider controls | Anything not exercised by explicit tests/evidence |

## Minimal first-proof cases

Use the exact same two inputs for any path actually selected for a hands-on comparison. Do not run anything until a path and test action are explicitly authorized and available.

**Valid input**
```csv
item,quantity,unit_price
notebook,2,3.50
pen,3,1.25
```

Expected computed values: `grand_total: "10.75"`, `line_items: 2`, `totals_by_item.notebook: "7.00"`, `totals_by_item.pen: "3.75"`.

**Malformed input**
```csv
item,quantity
notebook,2
pen,3
```

Expected: a clear missing-`unit_price` failure, no valid summary, and a non-success status where the environment exposes one.

For each case, capture:
- exact input and task/script revision;
- execution location/runtime and any visible version;
- user-visible status and raw exit/terminal status if exposed;
- stdout and stderr separately, distinguishing empty from unavailable;
- whether output collection completed, failed, or was partial (if the environment exposes this);
- actual output file existence, contents, and export/openability—not merely printed JSON;
- timeout/cancellation behavior only if deliberately tested;
- screenshots or copied raw evidence with sensitive information removed;
- limitations and unknowns; never infer missing values.

Do not invent unavailable exit codes, termination confirmation, collector status, or policy evidence. Mark them UNKNOWN/UNAVAILABLE.

## Decision gates after evidence collection

**Comparator is useful for product-loop learning if** both cases can be attempted on iPhone, the valid case yields the expected real artifact, the malformed case fails clearly without a false valid summary, and the evidence gaps are recorded. It may still be unsuitable as the production runner.

**Investigate PocketCode-owned execution further if** a concrete product requirement cannot be met locally—for example, controlled server-side execution, independently verified resource limits, authenticated artifact retrieval, or recovery after a lost response—and the need is backed by the failed criterion rather than assumption. Then compare provider options against a fixed acceptance matrix and current $0 constraints before choosing one.

**Do not choose a provider or add report fields yet.** First identify the actual execution boundary and authoritative source for child/runtime outcome, wrapper/infrastructure failure, timeout/termination, stream capture, and artifact validity. Add separate wrapper/child fields only if that boundary exists; model collection failure separately only if the adapter can observe it. Preserve the existing canonical execution contract as the candidate source of truth.

## Known unresolved issues

- Pyodios and browser-local paths have not been hands-on tested; all app behavior above is prior public-source documentation, not independent verification.
- No provider/adapter has been selected or run.
- No tests have been run in this pass.
- `FAILED` versus `INCOMPLETE` projection remains an owner decision; observed execution outcome and job disposition must remain conceptually distinct.
- Artifact release remains a separate fail-closed gate.
- Idempotency helper/model tests do not prove durable lookup, atomic reservation, provider recovery, or concurrency.
- Provider/network policy revision or ETag confirmation is relevant only if a remote/hosted path is pursued; a boolean alone is not proof of the exact revision or chronology.

## Guardrails

- $0 budget; phone-only through 2027-02-28.
- No account creation, provider workload, billing change, GitHub Actions, install, deployment, merge, or secrets.
- Do not modify PR #2, PR #3, or canonical main contract without explicit approval.
- This file is research guidance, not an implementation request or acceptance claim.

## Recommended next step

When practical, run the fixed two-case comparison on the existing iPhone app first because it can test the user loop without prematurely committing to backend architecture. Record all unavailable evidence explicitly. If the app cannot be accessed or tested, do not substitute assumptions; use the checklist as a specification for the next available test window.
