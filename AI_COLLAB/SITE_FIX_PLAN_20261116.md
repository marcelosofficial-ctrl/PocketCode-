# Site fix plan: decisions, status and exact targets (Claude, owner-delegated; updated 2026-11-18)

Context: the owner's GitHub and portfolio site exist to get a remote job (and to hold personal apps built for fun and learning). Rule used for every decision: **each public claim must match what a reader can verify by clicking through to the linked repository or release page.** Honest, checkable claims are a hiring signal; an overstated claim costs more than it gains. Findings ids (H, M, L, N) refer to WEBSITE_AUDIT_HOME_AND_JA_20261115.md and WEBSITE_AUDIT_ABOUT_CONTACT_RESUME_20261115.md.

## Status
- **PR 1 merged:** portfolio pull request #29 (squash commit a4fa98c, 2026-11-18). Its build check (npm run build:verify) succeeded on the head commit 73f4b0f before the merge (check run read through the pull-request API; GitHub run email "PR run succeeded: CI" 2026-11-18 00:10 UTC). The Pages deployment workflow runs on the push to main; its result was NOT confirmed when this was written.
- **Access:** Claude's GitHub connector uses a fine-grained token; since 2026-11-17 it covers every repository, so branch writes and merges work. The connector's pull-request creation form fails on the owner's phone, so the owner opens the compare link in Safari and taps Create pull request; Claude then reads the check runs and merges.

## Correction to the audits
M3 (unit 2) and N9 (unit 3) said body links such as "/about/" are root-absolute and only gain the /portfolio base through a runtime script. That is not a defect in the deployed site: deploy-pages.yml rewrites every href and src that starts with "/" to "/portfolio/..." in the built HTML (step "Normalize root-relative links for GitHub Pages"), so the links work without JavaScript. Read in unit 4 on 2026-11-17. The hard-coded "/portfolio/easyflix/..." image paths (L2) are harmless for the same reason; PR #29 switched them to the base helper anyway.

## Decisions and where each stands
| # | Decision | Why | Status |
|---|---|---|---|
| S1 | VektorDeck is described everywhere (EN and JA) as "1.0.0 public source release (MIT), no packaged installer". | VERIFIED: README says "completed public source release", packaged installer is post-1.0; GitHub shows no releases and no tags; MIT. | DONE on the résumé, about and JA project pages (PR #29). TODO: home pages (EN and JA proof strip "source available", card tag) and the EN project pages. |
| S2 | RevDev: "Active development · acceptance pending · no public release"; no "final", no "beta-ready"; feature list in building tense. | public sources cannot confirm RevDev's state | DONE on the résumé, about and JA project pages. TODO: home pages (EN "final release-lifecycle hardening", JA acceptance wording). |
| S3 | Remove the secondary-school name from every résumé page. | privacy | DONE on all six résumé pages. TODO: the PDF (public/resume/Marcelo_Ellwanger_Software_QA_Resume.pdf) may still contain it; it needs regenerating from the page (Print / Save as PDF) and replacing. |
| S4 | JA project buttons point at real pages: GapTrace and ExactArtifact /releases, MinimalClock releases/tag/1.0.0, ConfigTrace releases/tag/v1.0.1, Retro Game Vision and VektorDeck repositories; RevDev has no external button. | VERIFIED release pages exist | DONE (PR #29). |
| S5 | CrashScope and EasyFlix download buttons carry an unsigned-installer note. | VERIFIED: both release notes say unsigned | DONE on the JA project pages. TODO: the EN project pages (not read). |
| S6 | Japanese parity: NVIDIA caveat, test machine, JA labels, full stops, base helper; JA support résumé test count 239 corrected to 266. | VERIFIED against CrashScope 1.2.0 notes | DONE except the JA home page (carousel link labels "英語のケーススタディ", CrashScope caveat). |
| S7 | Technical: localized carousel aria text on /ja/ (BaseLayout); static clock fallback. (Base-path links dropped: see Correction.) | accessibility | TODO, touches the large files. |
| S8 | Leave: LinkedIn as the only public contact; Retro carousel numbers. | owner's choice or low value | no change |
| S9 | Contact page: add EasyFlix to the evidence paths (EN and JA); VektorDeck capture status (page says capture pending while the home card shows an image: owner or Claude to confirm the image is a real capture). | consistency | TODO |

## Verified facts used (GitHub release and repository pages, 2026-11-16)
- CrashScope v1.2.0: 266/266 .NET tests (Core 30, Infrastructure 37, Agent 179, Desktop 20); local installer unsigned, SmartScreen may warn; NVIDIA hardware validation outstanding and not claimed; test machines named.
- MinimalClock 1.0.0: release with a .rmskin package. ConfigTrace v1.0.1 and v1.0.0: releases exist.
- VektorDeck: no releases, no tags; README: "completed public source release", MIT.
- Retro-Game-Vision-Pipeline: repository exists, no releases.

## Delivery method
Branch from main, pull request, read the build check (npm run build:verify runs on every pull request to main), then squash merge; the push to main triggers the Pages deployment, which builds and verifies again before publishing, so a failing build never replaces the live site. Files are replaced whole (no patch call), so line endings may show as changed in the diff. Next change set (PR 2): home pages EN and JA, contact pages, EN project pages, then the PDF.
