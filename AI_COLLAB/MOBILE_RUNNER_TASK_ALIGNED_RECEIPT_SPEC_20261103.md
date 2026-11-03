# Mobile Runner Next Pass — Canonical Task and Evidence Receipt Specification

**Date:** 2026-11-03  
**Status:** Design-only continuity artifact. No source edit, browser interaction, execution, installation, provider selection, or test is authorized or claimed.  
**Branch:** \`pocketcode-ai-workflow-director-research-2026-10-28\`  
**Inputs reviewed:** mobile runner prototype blob \`e2c4ece041be95ce9a73bc60ff354702b21c33c2\`; static UX audit \`4e5679dccd041bdae55a05b22e51a0d5bd668f58\`; fixed-task worksheet; proposed execution contract; canonical LOOP-01..14 / CASE-01..16.

## 1. Decision

The next mobile-runner prototype pass should be a **task-aligned, truthful evidence-receipt design**, not a backend or runner implementation.

The current prototype is a simulated UX sketch. It uses a sales CSV and writes a sample \`summary.txt\`; the frozen comparison task is a standard-library CSV-to-JSON program that reads \`items.csv\` and creates \`summary.json\`. Those are different tasks and must not be conflated.

For this next design pass:

1. Use the exact frozen task and source unchanged wherever the page is intended to illustrate the fixed-task workflow.
2. Keep the visible simulated-execution banner and explicit no-execution wording.
3. Make both success and malformed-header examples show the same complete report structure.
4. Preserve execution outcome, job disposition, cleanup, artifact state/release, and report evidence as separate concepts.
5. Do not add a fake file picker, fake Run button, pretend cancellation, or fabricated runtime metrics.
6. Keep the UI design independent of the still-unselected execution location.

This spec does not select Pyodide, a native local runtime, a remote PC, Linux execution, or a hosted provider.

## 2. Canonical task that the prototype must represent

Use the frozen worksheet's exact source file \`main.py\` and exact input names/bytes. Do not rewrite the script or regenerate it with an AI between conditions.

### Success scenario

Input \`items.csv\`:

\`\`\`csv
item,quantity,unit_price
notebook,2,3.50
pen,3,1.25
\`\`\`

Expected program behavior:
- Read the CSV using the standard library.
- Use decimal-safe arithmetic.
- Group totals by item.
- Create a real file named \`summary.json\`.
- Print \`Wrote summary.json\`.
- Exit 0 when run as a normal Python process.

Expected parsed \`summary.json\` values:
- \`grand_total\`: string \`10.75\`
- \`line_items\`: integer \`2\`
- \`totals_by_item.notebook\`: string \`7.00\`
- \`totals_by_item.pen\`: string \`3.75\`

### Malformed-header scenario

Input \`items.csv\`:

\`\`\`csv
item,quantity
notebook,2
pen,3
\`\`\`

Expected fixture behavior:
- Report the missing \`unit_price\` header clearly.
- Return exit 2 when run as a normal Python process.
- Write the error to stderr.
- Do not create a misleading \`summary.json\` in a fresh workspace.

The isolated harness sanity check of this fixture passed, but the mobile product-path comparison remains NOT RUN. These expected values may be displayed as a **simulated illustration**, never as a real PocketCode run.

## 3. Screen structure and content

### A. Workspace identity and inputs

Show:
- Workspace name, explicitly marked sample/demo while simulated.
- \`main.py\` and \`items.csv\` as two distinct workspace files.
- A clear label that the input is the canonical sample fixture.
- The scenario selector: success or malformed-header example.

Do not present the fixed text preview as a user-imported file. Do not add an enabled upload/import affordance until file selection, byte handling, workspace association, and error states actually work on the target platform. A future actual import flow must show filename, byte size, import status, and which run used that input.

The editor may display the canonical source. If editable, clearly distinguish the displayed source from the frozen fixture used in the comparison protocol. Do not silently alter the comparison source when a user edits the editor.

### B. Scenario/result panel

For both sample scenarios, show the same field groups in the same order:

1. **Example label:** \`SIMULATED EXAMPLE — NOT AN EXECUTION\`.
2. **Execution status:** show the illustrative expected status separately from actual observation. In a simulation, label it \`example outcome\`, not an observed execution status.
3. **Job disposition:** \`NOT_APPLICABLE — NO JOB WAS DISPATCHED\` for the static prototype. Do not imply accepted/queued/running.
4. **Exit code:** show \`fixture expectation: 0\` or \`fixture expectation: 2\`; explicitly state it was not observed in this prototype.
5. **Duration:** \`NOT MEASURED\`. Remove the current fabricated 0.18s / 0.04s sample timings.
6. **Runtime:** \`NOT SELECTED / NOT RUN\`. A conceptual Python runtime label is not evidence of a selected runtime/version.
7. **stdout and stderr:** separate panels. Each has an independent capture-state label: \`SAMPLE CONTENT\`, \`CAPTURED EMPTY\`, \`UNAVAILABLE\`, or \`NOT OBSERVED\`. Never render an empty panel without saying whether it was captured empty or unavailable.
8. **Output artifacts:** explicit artifact state, name and content when applicable. For success, show the expected \`summary.json\` content as an illustrative expected artifact, not a real generated file. For malformed input, show \`NOT_CREATED (fresh-workspace fixture expectation)\`, not a generic missing card.
9. **Cleanup:** \`NOT OBSERVED\`. Do not infer cleanup from hiding a file card or resetting the page.
10. **Artifact release:** \`NOT IMPLEMENTED / NOT AUTHORIZED\`. An expected sample file is not a downloadable run artifact.
11. **Evidence/provenance:** state which fields are fixture-defined expectations and which are actually observed. In this static demo, no process, runtime, or service facts are observed.

A visual success badge must say \`SAMPLE SUCCESS\` or \`EXPECTED SUCCESS EXAMPLE\`, not plain \`SUCCESS\`. A failure badge must say \`SAMPLE FAILURE\` or \`EXPECTED FAILURE EXAMPLE\`.

### C. Handoff actions

Use one clear primary action: **Copy example report**. Keep **Copy debugging prompt** secondary.

Both copied strings must begin with the simulation label. The prompt must state that the sample report is not execution evidence and ask the receiving AI to reason from the exact displayed source/input, not claim a run happened.

Provide a visible selectable-text fallback. Clipboard success/failure must be described only after the browser reports it. Clipboard API availability remains browser-dependent and untested.

## 4. Copyable report examples

The examples below define content semantics for the simulated prototype. They are not a frozen API schema and not a claim of actual execution.

### Success illustration

\`\`\`text
POCKETCODE EXAMPLE REPORT
Evidence class: SIMULATED EXAMPLE — NOT AN EXECUTION
Task fixture: canonical-csv-to-json
Scenario: SUCCESS
Run ID: NONE — no run was created
Execution status: NOT_OBSERVED
Example fixture outcome: succeeded (expected, not observed here)
Job disposition: NOT_APPLICABLE — no job was dispatched
Runtime/version: NOT_SELECTED
Exit code: NOT_OBSERVED (fixture expectation: 0)
Duration: NOT_MEASURED

stdout state: SAMPLE CONTENT
stdout:
Wrote summary.json

stderr state: SAMPLE CAPTURED EMPTY
stderr:
(empty in this fixture's expected behavior; not collected by this prototype)

Artifact state: EXPECTED_TO_BE_CREATED (fixture expectation only)
Artifact name: summary.json
Artifact content (expected):
{"grand_total":"10.75","line_items":2,"totals_by_item":{"notebook":"7.00","pen":"3.75"}}
Artifact integrity/read-back: NOT_OBSERVED
Artifact release: NOT_IMPLEMENTED
Cleanup: NOT_OBSERVED

Evidence notes:
- The expected result comes from the frozen task specification and isolated fixture sanity check.
- This prototype did not execute code, create a workspace, collect process output, or create a file.
- Do not treat the expected JSON as a downloaded/generated artifact.
\`\`\`

### Malformed-header illustration

\`\`\`text
POCKETCODE EXAMPLE REPORT
Evidence class: SIMULATED EXAMPLE — NOT AN EXECUTION
Task fixture: canonical-csv-to-json
Scenario: MALFORMED_HEADER
Run ID: NONE — no run was created
Execution status: NOT_OBSERVED
Example fixture outcome: program_failed (expected, not observed here)
Job disposition: NOT_APPLICABLE — no job was dispatched
Runtime/version: NOT_SELECTED
Exit code: NOT_OBSERVED (fixture expectation: 2)
Duration: NOT_MEASURED

stdout state: SAMPLE CAPTURED EMPTY
stdout:
(empty in this fixture's expected behavior; not collected by this prototype)

stderr state: SAMPLE CONTENT
stderr:
ERROR: missing required CSV column(s): unit_price

Artifact state: NOT_CREATED (fresh-workspace fixture expectation only)
Artifact name: summary.json
Artifact content: NOT_APPLICABLE
Artifact inventory/read-back: NOT_OBSERVED
Artifact release: NOT_IMPLEMENTED
Cleanup: NOT_OBSERVED

Evidence notes:
- The missing-header behavior is defined by the frozen fixture and was sanity-checked in an isolated interpreter.
- This prototype did not execute code or inspect a workspace.
- NOT_CREATED is the expected result in a fresh fixture workspace, not a live filesystem observation by this page.
\`\`\`

Important distinction: a *real* runner report must use authoritative execution status, actual exit code when available, measured duration when available, separately collected stdout/stderr, real output inventory, and explicit cleanup/release evidence. It must not copy the illustrative values above.

## 5. Interaction and accessibility requirements

- Tabs must have complete tab/panel relationships (\`aria-controls\`, \`aria-labelledby\`) and expected keyboard navigation (arrow keys, Home, End) if tab semantics are retained.
- Focus remains visible; status changes are announced without forcing a screen reader through the entire output.
- Scenario selection is not a Run action.
- No countdown, spinner, or cancel control should imply live execution.
- If an actual Run control is introduced in a later implementation, it must be wired only to an approved execution boundary and show accepted/queued/running plus authoritative terminal states. A client timer cannot establish timeout or termination.
- If a real cancellation action is introduced, distinguish request sent, cancellation confirmed, already terminal, and termination unconfirmed.

The existing static checker is a source heuristic, not a browser, keyboard, screen-reader, or clipboard test.

## 6. Mapping to existing acceptance only

This spec maps to existing requirements; it creates no new LOOP/CASE IDs and does not change their meanings.

| Existing requirement | What this prototype design can illustrate | What it cannot prove |
|---|---|---|
| LOOP-01 | Code and two named sample inputs visible together | Real phone file import/association |
| LOOP-02 | Simulation banner and distinct sample outcomes | Real lifecycle state |
| LOOP-03 / CASE-01 | Expected success receipt | Trusted successful execution |
| LOOP-04 / CASE-02 / CASE-03 | Expected program-error receipt | Actual runtime error/exit evidence |
| LOOP-05 / CASE-04 / CASE-05 / CASE-06 | Reserved space for incomplete outcomes | Deadline enforcement, cancellation, infrastructure truth |
| LOOP-07 | Separate stdout/stderr, provenance, truncation/artifact fields | Actual collection quality |
| LOOP-08 | Copyable complete example report | Clipboard reliability on iOS/Android |
| LOOP-09 | Conceptual before/after correction loop | Preserved run history or actual rerun |
| LOOP-10 | Expected artifact presentation | Real file creation/download |
| LOOP-11 | Report excludes source/secrets by default | Real data-flow/privacy behavior |
| LOOP-12 | No sandbox claim | Any isolation, egress, resource, termination or cleanup property |
| LOOP-13 | Explicit manual handoff | Any cross-app automation |
| LOOP-14 | No service/account/cost implication | Any provider cost or billing guarantee |

## 7. Next evidence sequence

1. Keep this iteration design-only until a source-edit request is explicitly authorized.
2. If a UI-only source edit is later authorized, align the simulated task and receipt with this spec; preserve the simulation banner and do not add fake execution controls.
3. Read back the exact source diff and run only the existing static checks if separately authorized; label them static checks.
4. Browser, accessibility, clipboard, file-import, and device checks remain separate and NOT RUN until actually performed on target browsers/devices.
5. Product-path comparison remains a separate experiment. A simulated PocketCode screen cannot receive execution/correctness points.
6. The paired AI correction experiment must use identical observed evidence in both conditions. Synthetic receipt examples can validate format comprehension only, not report advantage.

## 8. Non-actions and current decision

No source/test files were modified. No browser/device tests, app installation, file import, clipboard test, runtime execution, provider workload, account, spend, GitHub Actions, merge, deployment, or host/queue operation occurred.

**Decision:** adopt this as the next design reference, not as implementation approval. The mobile runner remains simulated; the execution location remains unselected; fixed-task product-path comparison remains NOT RUN; paired AI correction experiment remains NOT RUN; the report differentiator remains UNVALIDATED.
