# Site fix plan: decisions and exact targets (Claude, owner-delegated, 2026-11-16)

Context: the owner's GitHub and portfolio site exist to get a remote job (and to hold personal apps built for fun and learning). Rule used for every decision: **each public claim must match what a reader can verify by clicking through to the linked repository or release page.** Honest, checkable claims are a hiring signal; an overstated claim costs more than it gains. This file turns the findings of WEBSITE_AUDIT_HOME_AND_JA_20261115.md (ids H, M, L) and WEBSITE_AUDIT_ABOUT_CONTACT_RESUME_20261115.md (ids N) into decisions. Nothing here has been applied to the portfolio yet (see Blocker).

## Blocker
Claude's GitHub connector authenticates with a fine-grained personal access token. On 2026-11-16 creating a branch in marcelosofficial-ctrl/portfolio returned HTTP 403 "Resource not accessible by personal access token" (read works because the repository is public). The same token returns 404 for the private repository LingoMingle. Fix on the owner's side: GitHub, Settings, Developer settings, Personal access tokens, Fine-grained tokens (github.com/settings/personal-access-tokens), open the token, Repository access: add portfolio and LingoMingle; Repository permissions: Contents Read and write, Pull requests Read and write. Until then this plan waits.

## Decisions
| # | Decision | Why | Findings covered |
|---|---|---|---|
| S1 | VektorDeck is described everywhere (EN and JA, about, résumé, cards, case page) as "1.0.0 public source release (MIT), no packaged installer". Remove "SHIPPED", "released" without that qualifier, and "source available". | VERIFIED: its README calls 1.0.0 "the completed public source release" and says a packaged installer is post-1.0 scope; GitHub shows no releases and no tags; license is MIT. | M5, N1 |
| S2 | RevDev is described everywhere as "Active development · acceptance pending · no public release". Delete "final" and "最終", delete "beta-ready" from the résumé summaries (use "in-development"), and write the RevDev feature list as "Designing and building ..." instead of "Added ...". | public sources cannot confirm RevDev's state, so only the hedged wording is safe | H2, N2, N3 |
| S3 | Remove the secondary-school name (and its city) from every résumé page, EN and JA; keep the post-secondary credential and "Canada". | privacy; employers do not need it | owner decision from N8 |
| S4 | Fix the Japanese project-page buttons: GapTrace -> github.com/marcelosofficial-ctrl/GapTrace/releases; ExactArtifact -> .../ExactArtifact/releases; MinimalClock ("rainmeter-clock") -> .../MinimalClock/releases/tag/1.0.0; ConfigTrace -> .../ConfigTrace/releases/tag/v1.0.1; Retro Game Vision ("reseller-ai") -> repository .../Retro-Game-Vision-Pipeline labelled "Source repository" (no releases exist); VektorDeck -> repository, labelled "Source (MIT)"; RevDev -> no external button (no public repository). | VERIFIED: the release pages for GapTrace, ExactArtifact, MinimalClock and ConfigTrace exist; Retro and VektorDeck have none | H1, H2 |
| S5 | Next to the CrashScope and EasyFlix download buttons add one sentence (EN and JA): the installer is not code-signed, Windows may show a SmartScreen warning, SHA-256 checksums are on the release page. | VERIFIED: both release notes say the installers are unsigned | H3 |
| S6 | Japanese parity: add the CrashScope sentence that NVIDIA real-hardware validation is outstanding; add the test machine to the JA performance figures; JA carousel and about links use the Japanese label; end the nine JA lesson strings with "。"; JA EasyFlix image path uses the base helper. | VERIFIED: CrashScope 1.2.0 notes (266/266 .NET tests, NVIDIA not claimed, test machines named) | M1, M4, N5, N8, L1, L2 |
| S7 | Technical fixes in a later, separate change: localized carousel aria text on /ja/ (BaseLayout), build-time base path for body links, static clock fallback. | accessibility and no-JS robustness; touches the large files | M2, M3, L3 |
| S8 | Leave as they are: LinkedIn as the only public contact (owner's choice; recruiters expect it); Retro carousel numbers (scope unknown, low value); EN/JA bio wording beyond the leads. Add EasyFlix to the contact page evidence paths (N7). | low risk or owner-only facts | N6, N7 |
| S9 | Add EasyFlix to the contact page evidence paths and align the EN and JA about leads on teaching experience (list it in both, since all résumé pages already do). | consistency | N4, N7 |

## Verified facts used (GitHub release and repository pages, 2026-11-16)
- CrashScope v1.2.0: 266/266 .NET tests (Core 30, Infrastructure 37, Agent 179, Desktop 20); local installer unsigned, SmartScreen may warn; NVIDIA hardware validation outstanding and not claimed; test machines named (Ryzen 5 7500F with Radeon RX 9070 XT, and an Intel i5-3210M second PC). This closes the earlier UNVERIFIED note on 266/266.
- MinimalClock 1.0.0: release with a .rmskin package. ConfigTrace v1.0.1 and v1.0.0: releases exist; 4.3 MB working set and 16 tests are in the 1.0.0 notes.
- VektorDeck: no releases, no tags; README: "completed public source release", MIT, packaged installer post-1.0.
- Retro-Game-Vision-Pipeline: repository exists, no releases.

## Delivery method
1. One branch from main, for example site/claims-and-privacy-fixes-2026-11-16, then a pull request into main. The portfolio's CI workflow (ci.yml) runs npm run build:verify on every pull request to main, and Claude can read pull-request check runs, so a broken build is caught before anything goes live. The Pages deployment runs only on pushes to main, so merging is the single go-live step and stays the owner's tap.
2. Order: PR 1 = résumé and about pages (S1, S2, S3, S9, N-findings); PR 2 = the JA project template (S4, S5, S6); PR 3 = home pages and BaseLayout (S6 remainder, S7).
3. Each file is replaced whole (the connector has no patch call), re-fetched after the write, and compared by blob SHA; large files (index.astro 56 KB, ja/index.astro 59 KB) are touched only in PR 3.
4. Every changed line must be traceable to a finding id above; no design, class or layout changes.
