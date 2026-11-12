# NEXT TASK: PocketCode

## Goal
Move from design contracts to evidence closure while keeping the P39 implementation/adapter gate CLOSED. Do not implement or select infrastructure from these specifications alone.

## Current evidence
- VERIFIED branch HEAD at start of this work unit: `04d8181bf159f5a90ae6b7ace017c7f58e31611d`. Its latest five commits are 04d8181, 0d7f873, 0545312, 6c67df2 and 5600730; all are documentation-only. GitHub compare from source audit pin `b71315068ec33a0175fed46ef96912e954d87f9f` to this head reports 35 commits, 0 behind, 11 changed paths, all under `AI_COLLAB/`. No app source/scripts/tests/workflows/assets changed in that interval. The branch head has no status checks.
- VERIFIED: P40 model lanes and full scripts suite PASS on exact target SHA 319cffef121e327331aeaff59522ae279b112ecc; Actions run 43126974602; full suite 266/266. Lane 4 BLOCKED / NOT TESTABLE. Model-only.
- VERIFIED: contract and acceptance documents are committed: GRANT_EVENT_ENVELOPE_AND_RELAY_CONTRACT_20261112.md; OPAQUE_ORIGIN_EXECUTION_PROTOCOL_20261112.md; BROWSER_ARTIFACT_STORAGE_RECOVERY_CONTRACT_20261112.md; LIFECYCLE_TERMINATION_RECEIPT_ACCEPTANCE_20261112.md; GRANT_EVENT_MODEL_ACCEPTANCE_PLAN_20261112.md (29 model scenarios); REPORT_PROJECTION_V2_MIGRATION_AND_ACCEPTANCE_20261112.md.
- VERIFIED: OD-01..OD-13 are adopted policy; implementation and durable adapter proof remain outstanding.
- VERIFIED: grant model has event/version parity, first-delivery authenticity/scope and relay-fence gaps. report_contract can misclassify timeout plus nonzero wrapper code; no precedence-only patch.
- VERIFIED: Pages run #17 deployed commit 90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c; current main prototype/workflow blobs match. Portfolio is on the same github.io origin and its BaseLayout uses localStorage. No sensitive persistent data on this host before isolation. UNKNOWN: live HTTP response, headers and device registrations.
- VERIFIED: ZERO_BUDGET_ORIGIN_OPTIONS_20261112.md compares no-spend origin candidates; Cloudflare Pages is research-only, Netlify secondary, Vercel Hobby excluded. No provider selected or account authorized.
- VERIFIED: PHONE_DEVICE_VALIDATION_RUNBOOK_20261112.md now consolidates non-destructive Pyodios diagnosis, device-context inventory, and future synthetic-data isolation/storage/lifecycle acceptance. Owner/device execution NOT RUN. The read-only probe matches the exact steps in PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md; preserve the existing success artifact.
- O-7: Pocket Code by Catrobat and POCO C++ are verified product/search collisions. Xiaomi POCO trademark claims remain UNKNOWN pending official database verification. No rename or PoCo publication.

## Ranked next steps
1. Owner-run the read-only Pyodios Console probe from PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md and PHONE_DEVICE_VALIDATION_RUNBOOK_20261112.md. Return exact output; do not rerun the successful artifact-producing attempt or overwrite summary.json.
2. Owner-reported partial visual check (2026-11-12): user opened the previously requested GitHub link and said it looked okay. The exact target is ambiguous because the prior reply included a GitHub commit URL and referred to the PocketCode Pages URL as an owner action. If the opened URL was https://marcelosofficial-ctrl.github.io/PocketCode-/, treat this as a basic visual smoke-check only; exact URL/content, device/browser/version and live response evidence were not captured. Do not ask the owner to repeat it unless they opened the commit page instead. Live headers, service-worker state and device-context matrix remain UNKNOWN/NOT RUN. Do not store secrets/private code on the shared origin.
3. Use PHONE_DEVICE_VALIDATION_RUNBOOK_20261112.md for separate Safari tab, Home Screen app, WKWebView, Android Chrome/PWA/WebView evidence when those contexts/builds are available. Do not infer between contexts. Browser isolation/storage tests require an explicitly approved synthetic-data test build.
4. Shared-origin comparison is committed in ZERO_BUDGET_ORIGIN_OPTIONS_20261112.md. Keep GitHub Pages preview non-sensitive. Any account authorization, host migration or deployment requires a separate owner decision.
5. VERIFIED plan committed: GRANT_EVENT_MODEL_ACCEPTANCE_PLAN_20261112.md defines 29 deterministic model scenarios. Obtain an explicit owner implementation/test gate before editing source/tests; do not select DB, broker or authentication algorithm.
6. Use REPORT_PROJECTION_V2_MIGRATION_AND_ACCEPTANCE_20261112.md as the report migration packet. Preserve format 1; any format-2 implementation needs a separate gate, authenticated immutable projection input, three distinct projections and its regression matrix. No precedence-only patch. CASE-04 remains INCOMPLETE / timed_out.
7. Prove the five-file fresh-chat resume protocol. Preserve existing names/IDs; do not open CHAT_START_HERE, HOT_RESUME or STATE_LEDGER.
8. Complete O-7 name clearance only if a product naming decision is needed. Verify official trademark records and intended markets before rename/publication.

## Constraints
- D-005/D-006: $0. No paid API keys/provider calls, hosting, Apple Developer Program, TestFlight or App Store.
- No runtime/provider/database/transport/storage/host choice, source/test edits, device tests, deployment/settings/DNS changes, PR #2/#3/#4 changes or RevDev work without applicable authorization.
- Preserve LOOP-01..14, CASE-01..16, all D-IDs and OD-01..OD-13. CASE-04 stays INCOMPLETE / timed_out without authoritative evidence.
- Evidence: VERIFIED / INFERRED / UNKNOWN / NOT RUN. Tests: PASS / FAIL / NOT RUN.
- Commit before summarizing; update CHECKPOINT after each unit; keep INDEX below 1,200 words.


## Live branch baseline (2026-11-12)
- VERIFIED current HEAD: `8298111d2b5d60cab9bbe8d5610fe52861e940c9`.
- VERIFIED latest five commits: `8298111d2b5d60cab9bbe8d5610fe52861e940c9`, `9c05f9158df250efa8cb3d7dcadcab047f5b6087`, `214c39bdd90947efaa660db280182f112c29ba61`, `04d8181bf159f5a90ae6b7ace017c7f58e31611d`, `0d7f8736d0db9855eda5d9d05da07fdf4ff7d0e0`.
- VERIFIED source boundary: compare from `b71315068ec33a0175fed46ef96912e954d87f9f` to HEAD = 38 ahead / 0 behind / 11 paths, all AI_COLLAB. No source/scripts/tests/workflow/assets changed.
- VERIFIED current HEAD has no status checks. Latest CI remains run #59, successful only on historical target `319cffef121e327331aeaff59522ae279b112ecc`; current-head tests NOT RUN.


## Owner usability clarification (2026-11-12)
The owner said the earlier phrase “run the probe” was unclear. The exact simple iPhone steps and copyable read-only code are now in section 2A of PHONE_DEVICE_VALIDATION_RUNBOOK_20261112.md. No Python knowledge is required. Owner action is optional and may be deferred: open Pyodios, tap Console (not Editor), paste the supplied block, run once, and send the output. If Console or its input/run control is unclear or unavailable, stop and report the screen text. Do not rerun main.py, run the wrapper, restart the session, or overwrite summary.json.

## Live branch reconciliation — 2026-11-12 22:43 local

- VERIFIED active branch HEAD at start of this pass: `928bc31dd41b854f6beda0e74d2774b72257b71b`.
- VERIFIED latest five commits, newest first:
- 928bc31dd41b854f6beda0e74d2774b72257b71b — docs(checkpoint): close owner diagnostic usability unit
- ebdaf6dbf4e116f5ab9d887d9b747f3f3e9b2584 — docs(state): record owner-friendly diagnostic guidance
- 599391c0fb57d45b20e3593d99d5013164d21977 — docs(next): clarify owner Pyodios diagnostic steps
- 7cc887837596e2d3099ecfefa738ca716aab84b3 — docs(runbook): make Pyodios probe owner-friendly
- 93f1b7dd40142437270455921303a4704a3e1aa5 — docs(checkpoint): close branch history reconciliation
- VERIFIED compare from source audit pin `b71315068ec33a0175fed46ef96912e954d87f9f` to HEAD: 47 commits ahead, 0 behind, 11 changed paths. Every changed path is under `AI_COLLAB/`; no application source, scripts/tests, workflow or product assets changed in this interval.
- VERIFIED HEAD combined commit status: `pending` with zero status entries (`total_count: 0`). This means no status checks are attached, not that a check passed.
- VERIFIED latest relevant Actions run remains #59 / `43126974602`, SUCCESS, workflow commit `d93cd11e6873090cdb280fd18e45d9eeee9a973f`, checking out historical model target `319cffef121e327331aeaff59522ae279b112ecc`; full scripts suite 266/266. This is model-only evidence on that exact historical target, not current-HEAD CI, adapter proof or CASE acceptance. Lane 4 remains BLOCKED / NOT TESTABLE; CASE-04 remains INCOMPLETE / timed_out.
- Previous baseline entries naming `8298111d2b5d60cab9bbe8d5610fe52861e940c9` or earlier are historical snapshots. This live reconciliation supersedes them for the branch head at this pass.
- The owner-friendly Pyodios instructions remain optional; the Console probe is NOT RUN. No owner action is required for repo-only work. Preserve the existing matching `summary.json`; never rerun the artifact-producing attempt.
- Tests in this documentation reconciliation: NOT RUN. No source/test/device/deployment/provider/DNS/settings/PR/RevDev changes. P39 implementation/adapter gate remains CLOSED; D-005/D-006 remain $0.
