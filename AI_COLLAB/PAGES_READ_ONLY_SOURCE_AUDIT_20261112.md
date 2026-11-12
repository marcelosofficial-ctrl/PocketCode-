# Read-only GitHub Pages source and deployment audit

Date: 2026-11-12
Status: repository/deployment evidence VERIFIED; live serving and headers UNKNOWN.
Scope: read-only. No Pages settings, workflow, branch, domain or deployment changes.

## Findings

**VERIFIED:** Latest successful preview deployment is GitHub Actions run #17, ID 39433670146, on 2026-10-20. It deployed commit 90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c. The deploy job and its seven substantive steps completed successfully, including source checker, Pages configuration, artifact upload and deploy-pages. The workflow log recorded https://marcelosofficial-ctrl.github.io/PocketCode-/.

**VERIFIED:** Current main is 03e65ef35d8b22cb4337ac7097b2a31247c3721e, 34 commits ahead and zero behind the deployment commit. The deployed and current-main prototype inputs are identical:
- prototypes/mobile-runner/index.html blob: e2c4ece041be95ce9a73bc60ff354702b21c33c2.
- .github/workflows/preview-prototype.yml blob: 58b1bb968aa8e6a2ae824079046e5968a140ab16.
- At deployment commit 90cc378..., the prototypes/mobile-runner subtree had only README.md (45ea89bfb9fd47e8c5d8441f835d84523730d8a4) and index.html (e2c4ece041be95ce9a73bc60ff354702b21c33c2).

The workflow uploads prototypes/mobile-runner as the Pages root. Therefore, the repository-defined output for run #17 is a two-file static prototype, not the full repository or active development branch.

## What the deployed source does

**VERIFIED from the exact HTML blob:**
- The banner states simulated execution only; submitted code is not run.
- Success/error controls switch fixed sample output. They do not execute textarea code.
- Python version and duration are illustrative; download is fixed sample text.
- Clipboard writing occurs only after explicit copy-button interaction, with a legacy user-initiated fallback. No clipboard polling.
- HTML uses inline CSS/JS. No Pyodide/runtime, Worker, provider, remote API, external JS library, service-worker registration/script, web manifest, browser database, local artifact store, login or backend is present in that published subtree.
- The deployment also publishes README.md with public setup/review instructions.
- The workflow runs Python unit tests and scripts/check_mobile_prototype.py. That checker describes itself as static source validation and does not run browser JS or submitted code.

**INFERRED:** Repository-controlled deployment bytes match current main because both relevant source blob hashes are identical. This does not prove GitHub Pages has not been changed outside this workflow.

## Trigger and freshness

**VERIFIED:** preview-prototype.yml deploys on main pushes when the prototype HTML or workflow changes, plus manual workflow_dispatch. Run #17 is the latest returned preview run; Actions lists 17 preview runs total. Older runs include failures/cancellations, so only the latest run is called successful.

**INFERRED:** Unrelated main changes and documentation-only changes do not republish the preview under the current path filter.

## Unknowns and limits

- Current GitHub Pages settings, custom domain and environment state: Pages settings endpoint was not retrievable through the available read-only connector.
- Current live response/body/headers/cache and whether it still serves run #17: public URLs were inaccessible through the web reader; a direct HTTP request could not resolve DNS from this environment.
- Actual device service-worker registrations/caches: no phone/browser inspection occurred.
- Portfolio deployment and scripts: outside this repository and not inspected here.

No CSP, COOP/COEP, Permissions Policy, service-worker or cross-origin-isolation claim is made from workflow success.

**NOT RUN:** no new CI, browser test, public HTTP/header request, phone inspection, Pages settings read or deployment. No product or infrastructure decision changed.
