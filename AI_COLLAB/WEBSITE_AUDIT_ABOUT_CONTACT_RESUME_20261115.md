# Website audit, unit 3: about, contact and résumé pages (EN and JA) (2026-11-15)

Research only. Nothing changed in the portfolio repo, nothing deployed. Continues WEBSITE_AUDIT_HOME_AND_JA_20261115.md (unit 2; finding ids H1 to L7 and the rule that every change is a proposal for owner approval apply here too). Tags: VERIFIED = read in source or in GitHub repository metadata this pass; INFERRED; UNKNOWN; NOT READ.

## 1. Source identity
Repo marcelosofficial-ctrl/portfolio (public, Astro), default branch, HEAD commit NOT captured. Blob SHAs read: src/pages/about.astro 6e70b9b23f5e; ja/about.astro 98c529698ac6; contact.astro 3b35b1f06aee; ja/contact.astro a493fdc2ec37; resume.astro afa50ee3132a; ja/resume.astro 68b0e480d47b; resume/software.astro edb6d3841692. Repository metadata (license, language, visibility) read through GitHub search on 2026-11-15.
NOT READ: ja/resume/software, ja/resume/support, resume/support, 404 page, the PDF itself (public/resume/Marcelo_Ellwanger_Software_QA_Resume.pdf exists, 116,613 bytes), portfolio-qr.svg (QR target UNKNOWN), stylesheets, EN project pages vs READMEs, site deploy workflow.

## 2. New findings, fix-first order
| # | Finding | Evidence | Proposed fix |
|---|---|---|---|
| N1 | VektorDeck release claim differs by language. JA about says "SHIPPED PRODUCT" and that it was released as 1.0; the JA résumé says "2026年リリース" and "リリース". EN about says "COMPLETED PRODUCT ... Source available" and both EN résumés say "Source available". The repository is public and MIT-licensed; no release page was found this pass. Extends unit-2 finding M5. | VERIFIED wording in all five pages; license VERIFIED from repo metadata; release existence UNKNOWN. | Make JA match EN, or link the real release. Also reconsider "source available": an MIT repository is open source. |
| N2 | RevDev status wording is not aligned. JA résumé: working on "最終検証" (final verification) before public release. EN general résumé: "public release remains pending final acceptance and approval". EN Software/QA résumé says features were "Added" (five-provider hub, typed actions, liveness state, failure learning, Windows packaging) in delivered tense. Extends H2. | VERIFIED wording. Public sources cannot confirm the stack (.NET 8, WPF), the provider count or the feature list. | One wording everywhere, such as "implemented; acceptance pending; no public release" if the owner confirms that is true. Avoid "final". Owner checks every RevDev claim against RevDev's own records (private details are deliberately not recorded here). |
| N3 | "beta-ready" appears in the EN general and Software/QA résumé summaries ("released, field-tested and beta-ready"). No page names which project is beta-ready. The JA general résumé says "継続開発中" (in continued development) instead. | VERIFIED wording; claim UNVERIFIED. | Name the project and its evidence, or drop the term. |
| N4 | EN about lead lists electrical work, operations, customer-facing roles and software but not teaching; the JA lead adds "教育" (education). All résumé pages list English teaching (Australia and Japan, 2023 to 2025). | VERIFIED. | Align the two leads. |
| N5 | Performance figures are scoped differently. EN general résumé names the test machine (Ryzen 5 7500F + Radeon RX 9070 XT); EN Software/QA résumé says "ConfigTrace-off" and adds private memory; the JA résumé gives 0.2365% CPU and 91.71/94.58 MB with the 1.1 scope but no machine. | VERIFIED. Figures themselves UNVERIFIED (not re-measured). | Add the machine to JA, or drop the numbers there. |
| N6 | Home carousel shows Retro Game Vision as "49 physical copies / 48 directly readable / 55 compatible obs." while résumés say 750+ canonical items, 1,000+ physical observations, 1,800+ market observations. Likely different scopes, but the carousel does not say so. | VERIFIED wording; relation UNKNOWN. | Label the carousel figures (for example "latest intake") if that is what they are. |
| N7 | Contact page paths cite CrashScope, VektorDeck and Retro Game Vision as evidence but not EasyFlix, the only 1.4 public release with installer and portable build. The "current builds" panel does list EasyFlix. | VERIFIED. | Add EasyFlix to the hiring and collaboration paths. |
| N8 | JA about: the EasyFlix link is labelled "ケーススタディ（英語）↗" (English) but points to /ja/projects/easyflix/ (a Japanese summary page). Same mismatch as unit-2 M1. | VERIFIED. | Use the Japanese label. |
| N9 | Body links on all seven pages are root-absolute ("/resume/software/", "/contact/", "/#work", PDF download "/resume/Marcelo_...pdf") and only gain the /portfolio base through the runtime script, as in unit-2 M3. With JavaScript off, the résumé PDF link and every internal link miss the site. | VERIFIED in source plus astro.config base. | Same fix as M3 (build-time base helper). |

## 3. Owner decisions (not defects)
- Every résumé page, EN and JA, publishes a secondary-school name and country, plus a specific city for the electrical work. Decide whether the school name is needed on a public page.
- The only public contact route is LinkedIn; there is no email or form. Intentional per the page text, but it is a single dependency.
- The JA résumé has no PDF download; the EN Software/QA résumé does. The PDF was not read, so it may differ from the page (check N1 to N3 in it).
- Retro-Game-Vision-Pipeline shows no recognized license on GitHub (NOASSERTION) while the other public repos are MIT. If the site implies open source, confirm; if all rights are reserved, say so.

## 4. Cross-checks that passed (VERIFIED, GitHub repository metadata 2026-11-15)
- EasyFlix: WPF/.NET 10, MIT, public; matches the site. GapTrace: Go. ConfigTrace: Rust. ExactArtifact: C# with CLI and WPF GUI. CrashScope: C#, MIT, WebView2 and WPF topics. VektorDeck and MinimalClock: public, MIT.
- JA and EN pages agree on: 4,000+ hours, five languages, EasyFlix 219 tests and MIT, CrashScope 266/266 and the second-PC validation, the contact route, availability wording.
- Bio items that were JA-only on the home page (Canada, Australia, Japan) are present on the EN about and résumé pages, so unit-2 L5 is mostly closed. The 4,000+ hours, the employers and the credentials remain self-claims; the check is the LinkedIn export (tracker row 6, waiting).
- NOT verified: CrashScope 266/266 and the performance figures; QR target; PDF content.

## 5. Next unit (small, read-only)
Read ja/resume/software, ja/resume/support, resume/support and the 404 page; decode or visually check the QR target; read the PDF (outline only); then the EN project pages against their repository READMEs and CI, and the site's deploy workflow. After that, prepare exact copy changes for H1 to H3, M1 to M5 and N1 to N9 on a branch for owner review; deploying stays a separate owner authorization.
