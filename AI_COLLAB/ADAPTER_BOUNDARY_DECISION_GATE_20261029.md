# PocketCode adapter-boundary decision gate — 2026-10-29

**Status:** Research aid only. No adapter selected, no provider run, no code/tests, and no canonical contract or PR changes.

## Why this gate exists

The report-provenance question cannot be settled in the abstract. Different execution locations expose different process boundaries. Do not assume that an on-device Python app, browser-local Pyodide, and a future server-side provider have the same wrapper/child process model.

## Candidate paths from existing research

| Path | Evidence already documented | Critical unknowns before it can support the PocketCode proof |
|---|---|---|
| Existing iPhone Python app (Pyodios comparator) | Prior public-source review says its documentation describes local CPython/Pyodide, project folders, CSV/JSON preview, real files, and iOS Files/share-sheet import/export. | Whether it provides authoritative per-run lifecycle/exit evidence, structured bounded stdout/stderr, collector-failure provenance, and a machine-readable timeout/termination state. No hands-on test was run. |
| Browser-local Pyodide | Existing research treats it as conditional on practical iPhone Safari file import/export. | Actual iOS file flow, runtime termination/control limits, output-file creation/export, and authoritative evidence. Not demonstrated. |
| Provider-neutral server execution contract | The proposed contract defines lifecycle, bounded output, explicit unknown states, fixed limits, authenticated output access, and provider-neutral adapter goals. | Provider and adapter are deliberately unselected; no live provider, security boundary, timeout termination, report mapping, or recovery behavior has been verified. |

These are not equivalent implementation options. The first is a comparator for whether an existing local app already meets the user need; the third is a future product architecture. Do not blend their assumptions or treat documentation as execution evidence.

## Decision sequence

1. **Clarify the product proof:** is the immediate target to validate whether an existing iPhone app already solves the fixed CSV task, or to design a PocketCode-owned execution service? Keep the first comparator cheap and separate from the hosted API proposal.
2. **Inspect the real boundary:** identify which component launches user code, which component observes its exit, and whether any wrapper/collector can fail independently.
3. **Prove the evidence source:** identify who authoritatively reports terminal status, child exit, timeout/termination, stdout/stderr completeness, and output files. Unknown remains unknown.
4. **Only then map fields:** if wrapper and child are the same process boundary, do not add separate wrapper/child fields. If separate, preserve independent observations. If partial diagnostic collection is possible, model that explicitly rather than inferring it from empty/unavailable strings.
5. **Run the fixed success and malformed-input cases only after a path is explicitly authorized and actually available.** Fresh workspace per case; verify exported file bytes and report evidence, not merely printed JSON.

## Existing constraints retained

- Budget remains $0. No accounts, billing, provider workload, Actions, deployment, or installs under this research-only step.
- Do not modify PR #2, PR #3, or the canonical contract without explicit authorization.
- Do not claim a test or runtime comparison was executed. Current status remains NOT RUN.
- The FAILED-versus-INCOMPLETE disposition question stays unresolved; artifact release remains an independent fail-closed gate.

## Sources within this repository

- `PRODUCT/EXECUTION_CONTRACT.md` on `main`: provider-neutral proposal; provider-specific adapter remains an open decision.
- `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md` on `main`: truthful PASS/FAIL/INCOMPLETE and diagnostic requirements.
- `AI_COLLAB/POCKETCODE_CURRENT_CHECKPOINT_20261028.md` on the research branch: Pyodios and browser-local Pyodide comparator status.
- `AI_COLLAB/OPEN_SOURCE_REUSE_AUDIT_20261029.md` on the research branch: wrapper/child and diagnostic provenance truth table.
