# Website audit, unit 2: home page (EN and JA) and the Japanese project pages (2026-11-15)

Research only. Nothing was changed in the portfolio repo, nothing deployed. Continues WEBSITE_AUDIT_AND_POCO_PAGE_PLAN_20261108.md (unit 1 read BaseLayout, global.css, revdev.astro). Tags: VERIFIED = read in source or on a public GitHub release page this pass; INFERRED; UNKNOWN; NOT READ. Every change below is a proposal for owner approval; keep the existing design and classes.

## 1. Source identity
Repo marcelosofficial-ctrl/portfolio (public, Astro), default branch, HEAD commit NOT captured. Blob SHAs read: src/pages/index.astro 0fbb3d070b62; src/pages/ja/index.astro d88b65d23e73; src/pages/ja/projects/[slug].astro 137fc7975cac; src/layouts/BaseLayout.astro 88f610117a47; astro.config.mjs 8063c8b29f7a (site https://marcelosofficial-ctrl.github.io, base /portfolio). Public release pages used for cross-checks: CrashScope v1.2.0, EasyFlix 1.4.0, GapTrace 1.0.0, ExactArtifact (all github.com/marcelosofficial-ctrl/<repo>/releases).

## 2. Read / not read
Read in full: EN home, JA home, the single JA project template (it generates all nine /ja/projects/<slug>/ pages), BaseLayout, astro.config.mjs.
NOT READ: ja/about, ja/contact, ja/resume and ja/resume/*, their EN pairs, EN project pages other than revdev (unit 1), stylesheets, public assets, README/PROJECT-GOALS, site CI. The deployed site was not fetched (URL not retrievable by the fetch tool), so findings are source-level.

## 3. Findings, fix-first order

### Misleading to visitors
| # | Finding | Evidence | Proposed fix |
|---|---|---|---|
| H1 | Five JA project pages have a primary button labelled like a release or package, but it links to the GitHub profile root: reseller-ai ("Source / case study"), rainmeter-clock ("1.0.0 package"), exactartifact ("1.0.0 release"), gaptrace ("1.0.0 release"), configtrace ("1.0.1 release"). | VERIFIED in [slug].astro (href = https://github.com/marcelosofficial-ctrl). Public release pages exist for GapTrace and ExactArtifact (VERIFIED). | Point GapTrace and ExactArtifact to their /releases pages. For the other three the owner must confirm the repository URL (UNKNOWN; do not guess). EN pages NOT READ: check whether they share this. |
| H2 | JA RevDev page: the button labelled "公開リリースなし" (no public release) links to the portfolio repo itself. Evidence text says the team is working on "最終リリースライフサイクルの受け入れ" (final release-lifecycle acceptance). EN home says "final release-lifecycle hardening before any public release". Stack ".NET 8 · WPF", "5 PROVIDERS", the "REAL PRODUCT CAPTURE" caption and the READY / GUARDED / PERSISTED chips cannot be checked from public sources. | VERIFIED wording in ja/projects/[slug].astro, index.astro and ja/index.astro. Public-source verification of RevDev claims: none (no RevDev application source in the owner's public repos, per unit 1). | Make the RevDev button a non-download link to the case study, or drop it. Remove "final" and "受け入れ" (use "hardening" / "強化") and keep "ACTIVE DEVELOPMENT · ACCEPTANCE PENDING" from unit 1. Owner to confirm the stack, provider count and capture against RevDev's own records; details are deliberately not recorded in this public repo. |
| H3 | CrashScope and EasyFlix JA pages make a direct .exe download the primary button with no signing notice. The EasyFlix 1.4.0 release notes say the binaries are not code-signed and Windows may warn. CrashScope notes only mention a future signing policy. | VERIFIED: EasyFlix filename matches the release's recommended download; CrashScope filename UNVERIFIED. | Add one plain sentence beside each download (unsigned, expect a Windows warning, checksums on the release). Check the EN pages for the same gap. |

### Accessibility, localization, structure
| # | Finding | Evidence | Proposed fix |
|---|---|---|---|
| M1 | JA carousel: slides 2 to 4 say "英語のケーススタディ ↗" (English case study) but link to the Japanese pages /ja/projects/...; slide 1 says "日本語ケーススタディ". | VERIFIED in ja/index.astro. | Use the Japanese label on all four. |
| M2 | On /ja/ the shared carousel script overwrites the Japanese aria-label of the rotation toggle with English at load, and writes English live-region announcements ("Slide N of M: ..."). Screen-reader users on the Japanese site hear English. | VERIFIED in BaseLayout.astro (updateRotationToggle, render with announce). | Pass localized strings through the existing define:vars. |
| M3 | Body links are root-absolute ("/about/", "/projects/crashscope/", "/ja/...") while the site base is /portfolio. Only a runtime script adds the prefix; with JavaScript off, or for any non-rendering crawler or preview bot, they point outside the site. Nav and footer already use withBase at build time. | VERIFIED: astro.config.mjs base, hrefs in index.astro, ja/index.astro and [slug].astro, prefix script in BaseLayout. | Build body hrefs with the same base helper as the nav. No visual change. |
| M4 | CrashScope limitation parity: EN home says NVIDIA real-hardware validation remains outstanding and names the second-PC test; the JA home and JA page omit it. The CrashScope 1.2.0 release notes also say NVIDIA validation is not claimed. | VERIFIED. | Add the same sentence in Japanese. |
| M5 | VektorDeck: the JA page shows "CAPTURE UPDATE PENDING / REAL PRODUCT CAPTURE TO FOLLOW", while the home card (EN and JA) shows shots/vektordeck-dashboard.webp as the card image. Either the capture exists (page stale) or the home image is not a real capture. Status also differs: page "1.0.0 RELEASED · SOURCE AVAILABLE", home card "1.0.0", proof strip "source available"; no VektorDeck release page was found in this pass. | VERIFIED wording; truth UNKNOWN. | Owner to say which is true, then align the three places. |

### Copy and polish (low)
- L1: all nine `lessons` strings in the JA template end with an ASCII "." instead of "。". Seven of nine eyebrows are still English (RevDev, Retro, VektorDeck, MinimalClock, ExactArtifact, GapTrace, ConfigTrace); CrashScope and EasyFlix are Japanese. VERIFIED.
- L2: JA EasyFlix media paths are hard-coded "/portfolio/easyflix/..." instead of the base helper; fine today, breaks if the base or domain changes. VERIFIED.
- L3: the MinimalClock card ships a static fallback (MON07, SEP 2026, 23:26:01) in the HTML; JS replaces it, but a no-JS view or crawler snapshot shows an old date. VERIFIED.
- L4: the Retro panel is labelled "DECISION ENGINE / LIVE MODEL" in EN but "FIELD MODEL" in JA. It shows illustrative rows (A-042 to A-044) and static badges (INTEGRITY: OK, FOREIGN KEYS: 0, EVIDENCE: LINKED) with no SAMPLE label. Suggest "FIELD MODEL" and "SAMPLE DATA". In EN the "NO GUI RELEASE" chip sits inside an aria-hidden panel; JA states it in visible text. VERIFIED.
- L5: JA-only biography detail not in EN home: electrical work in Canada, customer-facing work in Australia and Japan, "flexible with overseas time zones". Both languages claim "4,000+ hands-on electrical trade hours". UNVERIFIED here; check against the résumé and the LinkedIn export (tracker row 6, waiting).
- L6: the JA Retro status note talks about the portfolio itself ("ポートフォリオでは判断パイプラインとして正確に表現しています") rather than to the visitor. Copy suggestion only.
- L7: the JA project pages are condensed summaries of one shared template, far shorter than EN pages such as revdev.astro; their closing text says they carry the same status and access boundaries, which H1 to H3 and M5 show is not guaranteed.

## 4. Cross-checks that passed (VERIFIED)
- EasyFlix: 1.4.0 is the first public release; 219/219 tests; installer plus portable; matches "INSTALLER + PORTABLE WIN-X64".
- GapTrace 1.0.0: peak working set 16.2 MB and CPU 0.016 s match the site.
- ExactArtifact: 22 automated tests, CLI and WPF GUI match (release notes say "validated local release candidate").
- CrashScope 1.2.0 is the latest release; WPF hosting the React dashboard through WebView2 matches "WPF/WebView2 desktop shell".
- Retro numbers are internally consistent: 1 BUY + 7 MAYBE + 41 RESEARCH = 49 physical copies. Carousel has 5 slides and 5 dots in both languages.
- BaseLayout: canonical, hreflang en/ja/x-default, JA lang attribute and JA OG image alt are present; the language preference redirect and the JA "switch to English" link store the choice so they do not bounce.
- NOT verified this pass: CrashScope 266/266, 0.2365% CPU, 91.71 MB; EasyFlix .NET 10 and MIT; GapTrace being Go; ConfigTrace Rust and 4.3 MB; VektorDeck 11.15 GB and 0 blockers.

## 5. Next unit (small, read-only)
Read ja/about, ja/contact, ja/resume (+ resume/software, resume/support) and their EN pairs for claim parity; check the EN pages for H1 to H3; then the other EN project pages against their repository READMEs and CI. Prepare exact copy changes on a branch for owner review; deploying is a separate owner authorization. Tracker row 5 in STRATEGY_PROGRAM_20261108.md and the INDEX.md row were not edited (whole-file rewrites; left to the lead writer).
