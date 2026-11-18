# STRATEGY PROGRAM: design, PoCo, App Store, website, LinkedIn, governance (tracker)

Started 2026-11-08 by Claude from the owner's master brief. The brief's requirements are the master; findings here support them. Status values: DONE (evidence in repo), PARTIAL, NOT STARTED, BLOCKED, WAITING. Tags as in other docs. Updated 2026-11-18 by Claude (rows 3, 5, 6, 7).

| # | Deliverable | Status | Evidence / where | Next step | Blocker or owner decision |
|---|---|---|---|---|---|
| 1 | Apple design engineering research | PARTIAL (web app done; RevDev blocked) | APPLE_DESIGN_ENGINEERING_SPEC_20261108.md | verify the UNKNOWN items on the iPhone; read the remaining HIG pages | RevDev UI source is not on GitHub (VERIFIED by listing) |
| 2 | RevDev modernization plan | BLOCKED (partly) | website claims .NET 8 / WPF (UNVERIFIED by source) | document-level plan only | PC access |
| 3 | PoCo product and architecture research | DONE for context engineering and provider caching; rest PARTIAL | PROVIDER_CACHING_AND_CONTEXT_ENGINEERING_20261110.md (indexed by ChatGPT 2026-11-12); kit/docs/REUSE_BACKLOG.md | differentiation comparison (research question 2) | none |
| 4 | iPhone-only App Store roadmap | DONE (first pass); paid steps DEFERRED by D-006 | IPHONE_ONLY_APP_STORE_ROADMAP_20261108.md; NO_SPEND_PWA_PATH_20261108.md | PWA hardening | none |
| 5 | Website audit and PoCo plan | MOSTLY DONE | WEBSITE_AUDIT_AND_POCO_PAGE_PLAN_20261108.md; WEBSITE_AUDIT_HOME_AND_JA_20261115.md; WEBSITE_AUDIT_ABOUT_CONTACT_RESUME_20261115.md; SITE_FIX_PLAN_20261116.md; portfolio PRs #29 and #30 merged and deployed 2026-11-18 | home pages EN/JA wording, contact pages, EN project pages other than RevDev/EasyFlix/CrashScope, PDF résumé refresh; PoCo page only after the name clearance (O-7) | PDF needs the owner to upload a fresh file |
| 6 | LinkedIn alignment | PARTIAL | draft text in LINKEDIN_DRAFT_20261118.md, built only from facts verified on the site and the repositories | audit the owner's real LinkedIn export against it when the export arrives | export file |
| 7 | GitHub governance audit | DONE | GOVERNANCE_AUDIT_20261108.md (PocketCode); GOVERNANCE_AUDIT_REVDEV_20261116.md in the private RevDev repository (decisions recorded there) | lead tasks from the RevDev audit (items 4, 6 to 9, 12, 14, 16) | none |
| 8 | Development efficiency research | PARTIAL | kit/docs/WORK_PROTOCOL.md, PLUGIN_LESSONS.md, REUSE_BACKLOG.md; AI_PLATFORM_INSTRUCTIONS.md (startup-set reuse rule, per-AI instruction blocks) | repo-map extract, CI strategy | none |
| 9 | Unified cross-AI handoff | DONE for instruction blocks and start files; keep updated | BOOT, STATE, NEXT_TASK, INBOX files in the repositories; AI_PLATFORM_INSTRUCTIONS.md; kit/templates/new-project/ | keep updated | none |

## Ground rules for every AI working this program
- Do not claim anything about PoCo that is not built. The website page and LinkedIn text come last and use only VERIFIED facts.
- Do not change the website design. Reuse its existing classes and components.
- Do not merge RevDev and PoCo code or weaken either repo's boundaries. RevDev material stays in the private repo.
- No deployment, purchase, secret change or PC action without the owner's explicit authorization (the owner delegated website merges to Claude on 2026-11-17 when the build check passes). D-006: no spending.

## Research questions queued
1. Differentiation: compare Happy, Vibe Kanban, CloudCLI, Cline and Aider mobile or remote flows (licences in REUSE_BACKLOG.md).
2. Remaining HIG pages (typography, layout, sheets, accessibility) for the web spec.
3. Repo-map extracts and a CI strategy that fit a phone-only workflow.
