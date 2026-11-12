# $0 deployment-origin options: supplemental comparison

Date: 2026-11-12
Status: research only; no provider selected, account created, repository connected or deployment performed.
Authority: D-005/D-006 remain unchanged. This document supplements GITHUB_PAGES_ORIGIN_ISOLATION_AND_LOCAL_DATA_SECURITY_20261109.md and PAGES_READ_ONLY_SOURCE_AUDIT_20261112.md.

## 1. Decision question

Can PocketCode retain a $0 public preview while moving browser-local app data off the shared `marcelosofficial-ctrl.github.io` origin, without buying a domain or weakening the phone-first/no-spend constraints?

Short answer: a separate provider-assigned hostname can create a different browser origin from the portfolio. Cloudflare Pages and Netlify currently document free static hosting and provider subdomains. That is a viable research path, not approval to migrate. Hosting on a new origin is not by itself a complete security design and does not make browser data durable, private from the hosting provider, or safe from compromised PocketCode code.

## 2. Verified platform facts

- GitHub Pages project sites default to `https://<owner>.github.io/<repository>`; paths do not create distinct origins. The portfolio and PocketCode preview currently share scheme, host and port. A second repository or different path does not isolate origin-scoped storage. [1][2]
- Cloudflare Pages assigns a unique `<PROJECT_NAME>.pages.dev` production subdomain and supports Git-provider integration. The current Free limits document 500 builds/month, one concurrent build, up to 20,000 files and 25 MiB per asset; static asset requests are free and unlimited. Pages supports a `_headers` file for response headers. [3][4][5]
- Netlify assigns a project subdomain of the form `[site-name].netlify.app`. Its Free plan is $0 with 300 monthly credits and a hard limit; when the limit is reached, projects pause until the next billing cycle. Production deploys consume credits, and bandwidth/requests also count. [6][7][8]
- Vercel assigns `.vercel.app` URLs and advertises a free Hobby plan, but its current terms restrict Hobby to personal/non-commercial use and reserve broad rights to use Hobby-submitted content for AI/model training. That makes it unsuitable as a default candidate for a product that may become commercial or handle private user code/context. [9]
- Sandboxed documents without `allow-same-origin` receive an opaque origin and cannot access localStorage/cookies or some JavaScript APIs. This protects the child from parent-origin storage access; it is not a storage solution for the parent app. [10]

## 3. Option comparison

| Option | Browser-origin effect | $0 / operational fit | Risks and limits | Disposition |
|---|---|---|---|---|
| Keep GitHub Pages at current project URL | Same origin as portfolio; no sibling-path isolation | Already owner-approved; no migration work | Same-origin scripts remain in one trust domain; current deployed subtree is only a static simulation | Keep for non-sensitive preview only |
| Cloudflare Pages `.pages.dev` | Distinct origin from `marcelosofficial-ctrl.github.io` when project subdomain is used | Current static Pages Free limits appear adequate for a prototype; Git integration documented | New provider account/integration, terms and limits; deployment/rollback/headers must be reviewed; no proof of runtime/device compatibility | Strongest candidate for a later $0 feasibility spike, not selected |
| Netlify `.netlify.app` | Distinct origin from GitHub Pages when using its provider subdomain | Free tier exists, but monthly hard cap can pause site | Production deploys, requests and bandwidth consume credits; availability can pause at limit; provider account/integration | Secondary candidate; weaker continuity under usage spikes |
| Vercel `.vercel.app` | Distinct origin from GitHub Pages | Free Hobby tier exists | Hobby is personal/non-commercial only; current terms allow Hobby content to be used for model training; service may be changed/removed | Exclude from default product shortlist |
| Buy/use separate custom domain | Distinct origin if dedicated hostname | Not compatible with current $0 default unless already owned | Registration/renewal and DNS ownership/maintenance; custom domain does not itself isolate compromised app code | Not permitted under current decision |
| Keep app origin but store sensitive data in opaque iframe | Child is isolated from parent origin storage | No hosting migration | Opaque child cannot use ordinary origin storage; does not protect parent app from same-origin portfolio scripts | Not a viable parent data-storage fix |

A different provider hostname is an origin boundary relative to the existing portfolio, not a blanket trust boundary. Same-origin scripts in the new PocketCode deployment can still access its storage. Supply-chain compromise, XSS in PocketCode itself, browser extensions, device compromise, provider-side access and user export/import remain separate threats. Do not put credentials or reusable secrets in browser storage.

## 4. Recommended staged path, without changing D-006

1. Keep the currently approved GitHub Pages URL as a static, non-sensitive preview only. Do not store private source, provider credentials, auth tokens, secrets or sensitive artifacts there.
2. If owner later wants a persistent-data prototype, run a bounded read-only comparison of Cloudflare Pages and Netlify account terms, project ownership, exact free limits, headers, build integration, Git permissions, deletion/rollback and export. No account creation or GitHub OAuth grant during research.
3. If the owner separately approves a feasibility spike, test only a synthetic app with synthetic data on a provider-assigned subdomain. Verify scheme/host/port, response headers, CSP, cross-origin storage separation from the portfolio, service-worker scope, cold start and export/restore. Do not copy real user data.
4. Only after evidence and a separate owner decision should the project consider migrating the public preview. Preserve GitHub as source of truth; hosting must not become the only copy of user artifacts.
5. Before persistent user data, independently prove the browser storage/recovery contract: staged writes, read-back digest, immutable manifest commit, quota/eviction handling, explicit export/import and device-specific recovery. A new origin does not solve eviction or durability.

## 5. Gate and evidence

VERIFIED: provider-published URLs, selected free-tier limits/terms and current Pages origin facts cited below.
INFERRED: a distinct provider-assigned hostname is a different origin from the current GitHub Pages host under the web origin tuple rule.
UNKNOWN: account eligibility, current account entitlements, actual deployed response headers, actual provider project configuration, service-worker state, and target-device behaviour.
NOT RUN: account creation, GitHub app authorization, migration, deploy, cross-origin marker test, storage test, device test or billing test.

No provider selected. No code, workflow, repository setting, DNS, hosting, deployment, storage engine or product decision changed. D-005/D-006 and the P39 implementation/adapter gate remain unchanged.

## Sources

1. GitHub Pages site types and default URLs: https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
2. MDN origin-scoped Web Storage: https://developer.mozilla.org/en-US/docs/Web/API/Web_Storage_API
3. Cloudflare Pages static deployment and `.pages.dev` URL: https://developers.cloudflare.com/pages/framework-guides/deploy-anything/
4. Cloudflare Pages Free limits: https://developers.cloudflare.com/pages/platform/limits/
5. Cloudflare Pages response headers: https://developers.cloudflare.com/pages/configuration/headers/
6. Netlify default subdomain: https://docs.netlify.com/manage/domains/domains-fundamentals/understand-domains/
7. Netlify Free credits and pause behaviour: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/billing-faq-for-credit-based-plans/
8. Netlify credit usage: https://docs.netlify.com/manage/accounts-and-billing/billing/billing-for-credit-based-plans/how-credits-work/
9. Vercel Terms of Service (2026-10-19): https://vercel.com/legal/terms
10. MDN CSP sandbox and opaque origins: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/sandbox
