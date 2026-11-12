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


## Addendum: shared origin and iOS storage correction (2026-11-12)

A second read-only source inspection expanded the audit to the separate `marcelosofficial-ctrl/portfolio` repository. Its current `main` configures Astro with `site: https://marcelosofficial-ctrl.github.io` and `base: /portfolio`. The PocketCode preview URL and portfolio URL therefore share the same scheme, host and port; only their paths differ.

**VERIFIED:** portfolio `src/layouts/BaseLayout.astro` includes an inline script that reads the `marcelo-language` key from `localStorage`. The current portfolio tree has no service-worker, web-manifest, `_headers` or `_redirects` path. This is source evidence, not a live browser inventory.

**Security consequence:** browser storage is origin-scoped, not path-scoped. MDN states that all documents with the same origin share localStorage. Therefore, any same-origin script executing on either path can access origin storage written by the other path. The current portfolio script is not evidence of malicious behaviour; it demonstrates that ordinary same-origin JavaScript has the relevant privilege. Treat the entire `marcelosofficial-ctrl.github.io` host as one browser trust domain.

Until a real origin boundary or explicit owner-accepted threat model exists, do not persist provider credentials, auth tokens, private source, secrets or sensitive artifacts on this shared origin. A different repository, URL path or unsandboxed iframe is not isolation. The opaque-origin child protocol protects the child from parent-origin access; it does not split the trusted parent page from other same-origin pages.

### Corrected WebKit persistence statement

The official WebKit Tracking Prevention page documents deletion of script-writable storage after seven days without user interaction under its stated conditions. It also explicitly exempts the first-party domain of Home Screen web applications from this 7-day cap and says their website data is isolated from Safari. Do not generalize the Safari-tab rule to standalone Home Screen web apps. This exemption is not a backup guarantee and does not rule out quota eviction, user deletion, device loss, app removal or other storage failures. Safari, Home Screen web app and WKWebView must be tested separately.

### Acceptance probes added

| ID | Probe | Required evidence | Current |
|---|---|---|---|
| PG-04 | Harmless cross-path storage marker | Write random non-sensitive marker on one path, read from other path, then delete; never use real data | NOT RUN |
| PG-05 | Script inventory on both paths | Exact live script URLs/hashes and inline-script inventory | PARTIAL: source inspection only |
| PG-06 | Storage/service-worker inventory | localStorage, IndexedDB, Cache Storage, OPFS, registrations, quota estimate and persist() result | NOT RUN |
| PG-07 | iOS install-mode comparison | Safari tab vs Home Screen app vs WKWebView; OS/browser versions; cold start, force quit and export/restore | NOT RUN |
| PG-08 | Live response policy | Status, redirects, CSP, COOP/COEP, Permissions-Policy, Referrer-Policy and cache headers for both paths | NOT RUN |

### Sources opened 2026-11-12

- WebKit Tracking Prevention: https://webkit.org/tracking-prevention/
- MDN Web Storage API: https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API
- MDN Origin glossary: https://developer.mozilla.org/en-US/docs/Glossary/Origin
- MDN Same-origin policy: https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy
- GitHub Pages publishing-source documentation: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
- GitHub Pages custom workflow documentation: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

No code, hosting, DNS, Pages setting, workflow or deployment changes were made. No live response headers or device storage behaviour were verified.
