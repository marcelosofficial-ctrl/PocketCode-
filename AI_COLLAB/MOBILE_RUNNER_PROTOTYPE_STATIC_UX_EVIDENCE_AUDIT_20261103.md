# Mobile Runner Prototype — Static Product and Evidence UX Audit

**Date:** 2026-11-03  
**Status:** Read-only source review. No browser/device interaction, source checker, tests, execution engine, deployment or Actions were run.  
**Branch:** \`pocketcode-ai-workflow-director-research-2026-10-28\`  
**Reviewed source:** \`prototypes/mobile-runner/index.html\`, blob \`e2c4ece041be95ce9a73bc60ff354702b21c33c2\`.  
**Supporting files:** \`prototypes/mobile-runner/README.md\`, \`scripts/check_mobile_prototype.py\`, \`scripts/test_check_mobile_prototype.py\`.

## Executive decision

The current page is an honest, useful *simulated UX sketch*. Its fixed success/error examples, persistent simulation banner, copyable report/prompt and explicit statement that no code executes are good safeguards against false claims.

It is not yet a convincing demonstration of PocketCode's primary product hypothesis. In particular, it does not yet demonstrate the frozen CSV-to-JSON task, real input-file intake, a complete evidence receipt, or timeout/cancellation controls. The next prototype pass should improve those product seams, not add visual polish or imply a runtime exists.

No source edits are made or authorized by this audit.

## Findings

### P1 — Demo task differs from the frozen comparison task

The prototype embeds a sales CSV with \`date,category,amount\`, calculates a total, and presents a generated \`summary.txt\`. The project's frozen comparison task is CSV-to-JSON.

**Why it matters:** a prototype demonstration and the fixed-task comparison would be showing different inputs, output contracts and failure modes. A successful UX demo could therefore be mistaken for evidence about the comparison task.

**Recommendation:** either align the simulated example with the exact frozen CSV-to-JSON fixture, or label the sales-summary flow as a separate illustrative UX example. Do not modify the canonical fixture to fit the prototype.

### P1 — Copied report is too small to demonstrate the portable-evidence differentiator

The current \`report()\` contains simulated status, generic runtime label, exit status, sample duration and one combined output string. It omits:
- distinct stdout and stderr streams and their capture states;
- explicit artifact state (created, not created, unavailable, or not required);
- source/input identity or hashes and a stable run/attempt identity;
- result provenance and whether the exit/terminal observation came from a trusted execution boundary;
- timeout/cancellation disposition and cleanup state;
- output-limit versus display-truncation distinctions.

The error example hides the file card, but the copied report does not explicitly state that no artifact was produced. Hiding a UI card is not a portable evidence statement.

**Recommendation:** before calling this a representative execution receipt, project the existing execution-contract semantics into a compact copyable report. Keep execution outcome, job disposition, cleanup and artifact release separate. For the fixed sample error, a truthful sample could state \`artifactState=NOT_CREATED\`; do not generalize that value to every failed run. If a collector or artifact inventory cannot be queried, state UNKNOWN/UNAVAILABLE rather than infer absence.

This is a design alignment recommendation, not a request to add every internal lifecycle field to the first screen. The compact report can show a small summary with detailed evidence available behind it.

### P1 — The page previews an input file but does not accept one

The CSV panel is a hard-coded \`div\`, and the copy prompt reads \`csv.textContent\`. There is no file picker, pasted-file buffer, filename/size identity, input manifest or actual import state.

**Why it matters:** the core phone workflow begins with user-supplied code and supporting files. The current demo only displays a sample input; it does not exercise intake, association with the script, or the user's actual task.

**Recommendation:** for a future UI-only iteration, make the input-file area visibly distinguish sample data from a user-selected/pasted file. Show filename, size and input association. Do not claim that a real file has been imported until browser interaction and file handling are actually implemented and tested.

### P1 — Timeout and cancellation are absent from the task flow

The action controls are deliberately named “Show success example” and “Show error example”, not Run. This is honest. However, there is no timeout configuration, cancellation request, stop acknowledgement, or termination state.

**Recommendation:** keep these out of the current simulated behavior. In the next design iteration, reserve a clear place for configured time limit and cancellation state, with distinct labels for request, acknowledgement and confirmed termination. A timer reaching zero or a browser message is not proof that code stopped.

### P2 — Tab semantics are only partially represented

The code/CSV controls have \`role=tab\` and \`aria-selected\`, and the CSV preview has \`role=tabpanel\`. The inspected source does not associate each tab with its panel using \`aria-controls\` / \`aria-labelledby\`, and no arrow-key/Home/End tab navigation is present.

The static checker verifies roles and selected-state attributes, but it does not prove the complete WAI-ARIA tab interaction pattern or screen-reader behavior.

**Recommendation:** add explicit tab/panel relationships and keyboard navigation in a future source-authorized pass, then perform real browser/screen-reader checks. Do not describe the current source heuristics as an accessibility audit.

### P2 — Clipboard behavior remains unverified

The code attempts \`navigator.clipboard.writeText\` and falls back to a temporary textarea plus \`document.execCommand('copy')\`. The README correctly warns that clipboard behavior depends on browser permission and secure-context support.

**Recommendation:** keep clipboard capability explicitly conditional until tested on supported iOS Safari and Android browsers. Always retain a manual select/copy fallback if the browser denies clipboard access.

## What is already good and should be preserved

- The top-level simulation banner is visible before the user interacts.
- Buttons are explicitly examples, not a real Run action.
- Copied report and debugging prompt both state that code was not executed.
- The debugging prompt includes the current editor contents, sample CSV and simulated report.
- The UI hides the sample output file on the sample failure path rather than showing a success artifact.
- The README warns against placing private data, credentials or real user code in the public demo.
- No external JavaScript library or backend is implied.

## Prioritized next design pass

1. Freeze which task this demo represents. Prefer the canonical CSV-to-JSON fixture if this page is meant to support the fixed-task comparison; otherwise label it explicitly as a separate example.
2. Redesign the copyable receipt summary so that a user/AI can distinguish execution outcome, job disposition, stdout, stderr, artifact state and evidence availability without inferring from hidden UI.
3. Show the difference between sample input and a real imported/pasted input file. Do not simulate successful import as real evidence.
4. Reserve explicit timeout and cancellation states in the UI without pretending the simulated page can stop code.
5. Complete tab keyboard/ARIA relationships and verify clipboard/accessibility on actual devices only when authorized and available.

## Verification and non-actions

- Static source inspection only; source blob: \`e2c4ece041be95ce9a73bc60ff354702b21c33c2\`.
- The source checker and its tests were read, not run. They explicitly describe themselves as static source heuristics and do not execute browser JavaScript.
- No browser/device test, app installation, code execution, file import, clipboard test, accessibility audit, test run, source/test modification, workflow dispatch, Actions, deployment, provider call or spend occurred.
- This audit does not change the canonical CSV-to-JSON fixture, LOOP/CASE acceptance, owner decisions, runtime choice or product security boundary.
- The current prototype remains simulated; product execution and report differentiator remain unvalidated.
