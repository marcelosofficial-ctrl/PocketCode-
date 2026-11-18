# Site fix plan: decisions, status and exact targets (Claude, owner-delegated; updated 2026-11-18)

Context: the owner's GitHub and portfolio site exist to get a remote job (and to hold personal apps built for fun and learning). Rule used for every decision: **each public claim must match what a reader can verify by clicking through to the linked repository or release page.** Honest, checkable claims are a hiring signal; an overstated claim costs more than it gains. Finding ids (H, M, L, N) refer to WEBSITE_AUDIT_HOME_AND_JA_20261115.md and WEBSITE_AUDIT_ABOUT_CONTACT_RESUME_20261115.md.

## Status
- **Merged and deployed (portfolio pull requests, squash merges, build check read before each merge, "Run succeeded: Deploy portfolio" email after):** #29 (a4fa98c, résumé, about and JA project pages), #28 (7d54862, Astro 7.3.2 to 7.4.7, dependabot), #30 (6903ce4, RevDev, EasyFlix and CrashScope pages), #31 (4547ebf, contact pages). The deploy for #31 was not yet confirmed when this was written.
- **Profile README** (marcelosofficial-ctrl/marcelosofficial-ctrl, commit 8808e14): VektorDeck described as a public source release (MIT) with no installer.
- **Access:** Claude's GitHub connector uses a fine-grained token that covers every repository since 2026-11-17. The connector's pull-request creation form fails on the owner's phone, so the owner opens the compare link in Safari and taps Create pull request; Claude then reads the check runs and merges.

## Corrections to the audits
- M3 (unit 2) and N9 (unit 3), root-absolute body links needing JavaScript, are not defects: deploy-pages.yml rewrites every href and src that starts with "/" to "/portfolio/..." in the built HTML. L2 (hard-coded image paths) was harmless for the same reason.
- The EN project pages for GapTrace (read 2026-11-18) match the verified release facts (16.2 MB, 0.016 s); the EasyFlix and CrashScope READMEs match the site too.

## Decisions and where each stands
| # | Decision | Status |
|---|---|---|
| S1 | VektorDeck: "1.0.0 public source release (MIT), no packaged installer" everywhere. | DONE on résumé, about, JA project pages and the profile README. Left: home pages (EN proof strip "source available"; harmless understatement) and the EN VektorDeck page ("Source available"; same). |
| S2 | RevDev: "Active development · acceptance pending · no public release"; no "final"; no "beta-ready". | DONE on résumés, about, the EN and JA RevDev pages. Left: home pages (EN "final release-lifecycle hardening before any public release"; JA acceptance wording). |
| S3 | Remove the secondary-school name from the résumé pages. | DONE on all six pages. Left: the PDF (public/resume/Marcelo_Ellwanger_Software_QA_Resume.pdf) needs a fresh file from the owner (open the résumé page, Print / Save as PDF, upload to that path). |
| S4 | JA project buttons point at real pages. | DONE. |
| S5 | Unsigned-installer notes next to the CrashScope and EasyFlix downloads. | DONE on the EN and JA project pages. |
| S6 | Japanese parity (NVIDIA caveat, test machine, labels, full stops, 266 test count). | DONE except the JA home page carousel labels ("英語のケーススタディ" on three Japanese links) and the JA home CrashScope caveat. |
| S7 | Localized carousel aria text on /ja/ (BaseLayout); static clock fallback. | NOT DONE (large files). |
| S8 | Leave: LinkedIn as the only public contact; Retro carousel numbers. | no change |
| S9 | Contact pages: EasyFlix added to the evidence paths. | DONE (#31). |

## Decision on the two home pages (2026-11-18)
index.astro (56 KB) and ja/index.astro (59 KB) need only about six small text edits, but the connector replaces whole files and these files are mostly long repeated decorative markup, so a transcription slip would change the visuals of the front page for little gain. Decision: do not rewrite them with this connector. The exact edits, for any tool with a real patch capability (a local editor, Claude Code):
1. EN home RevDev card status note: replace "final release-lifecycle hardening before any public release" with "release-lifecycle hardening; acceptance is pending and there is no public release".
2. EN home proof strip: replace "VektorDeck source available" with "VektorDeck public source release (MIT)".
3. EN home Retro panel: replace "LIVE MODEL" with "FIELD MODEL".
4. JA home: change the three carousel link labels "英語のケーススタディ ↗" to "日本語ケーススタディ ↗"; add the CrashScope NVIDIA caveat sentence; replace the "受け入れ" RevDev wording as on the JA RevDev page.
5. Both homes: the RevDev carousel and card show a screenshot captioned "REAL PRODUCT CAPTURE / REVDEV / DASHBOARD" while the RevDev page says the public screenshot set is pending and no mock dashboard is used. The owner must say whether shots/revdev-dashboard.webp is a real capture; if not, change the caption or remove the image.
6. VektorDeck: the JA case page says "CAPTURE UPDATE PENDING" while the home card shows a dashboard image; same question.

## Verified facts used (GitHub release and repository pages)
- CrashScope v1.2.0: 266/266 .NET tests (Core 30, Infrastructure 37, Agent 179, Desktop 20); installer unsigned; NVIDIA validation outstanding.
- EasyFlix v1.4.0: 219/219 tests; installers unsigned; MIT; WPF/.NET 10.
- MinimalClock 1.0.0 and ConfigTrace v1.0.1 releases exist; VektorDeck has no releases or tags (README: completed public source release, MIT); Retro-Game-Vision-Pipeline has no releases.

## Delivery method
Branch from main, pull request (the owner taps Create pull request in Safari), read the build check (npm run build:verify on every pull request to main), squash merge, then the Pages deployment builds and verifies again before publishing, so a failing build never replaces the live site. Files are replaced whole, so line endings may show as changed in the diff.
