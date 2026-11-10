# STRATEGY PROGRAM: design, PoCo, App Store, website, LinkedIn, governance (tracker)

Started 2026-11-08 by Claude from the owner's master brief. The brief's requirements are the master; findings here support them. Status values: DONE (evidence in repo), PARTIAL, NOT STARTED, BLOCKED, WAITING. Tags as in other docs.

| # | Deliverable | Status | Evidence / where | Next step | Blocker or owner decision |
|---|---|---|---|---|---|
| 1 | Apple design engineering research | PARTIAL (web app done; RevDev blocked) | APPLE_DESIGN_ENGINEERING_SPEC_20261108.md | verify the UNKNOWN items on the iPhone; read the remaining HIG pages | RevDev UI source is not on GitHub (VERIFIED by listing) |
| 2 | RevDev modernization plan | BLOCKED (partly) | website claims .NET 8 / WPF (UNVERIFIED by source) | document-level plan only | PC access |
| 3 | PoCo product and architecture research | PARTIAL | kit/docs/REUSE_BACKLOG.md; many research docs | context engineering and provider caching (Anthropic, OpenAI, Google differ) | none |
| 4 | iPhone-only App Store roadmap | DONE (first pass); paid steps DEFERRED by D-006 | IPHONE_ONLY_APP_STORE_ROADMAP_20261108.md; NO_SPEND_PWA_PATH_20261108.md | PWA hardening | none |
| 5 | Website audit and PoCo plan | PARTIAL | WEBSITE_AUDIT_AND_POCO_PAGE_PLAN_20261108.md | read index.astro, ja pages, other project pages | none |
| 6 | LinkedIn alignment | WAITING | owner requested the LinkedIn data export (about 24 hours) | audit the exported file against verified facts | export file |
| 7 | GitHub governance audit | PARTIAL | GOVERNANCE_AUDIT_20261108.md (PocketCode); RevDev entry rules done | RevDev rules audit | none |
| 8 | Development efficiency research | PARTIAL | kit/docs/WORK_PROTOCOL.md, PLUGIN_LESSONS.md, REUSE_BACKLOG.md | repo-map extract, CI strategy | none |
| 9 | Unified cross-AI handoff | PARTIAL | BOOT, STATE, NEXT_TASK, INBOX files in both repos | keep updated | none |

## Ground rules for every AI working this program
- Do not claim anything about PoCo that is not built. The website page and LinkedIn text come last and use only VERIFIED facts.
- Do not change the website design. Reuse its existing classes and components.
- Do not merge RevDev and PoCo code or weaken either repo's boundaries. RevDev material stays in the private repo.
- No deployment, purchase, secret change or PC action without the owner's explicit authorization. D-006: no spending.

## Research questions queued
1. PoCo context engineering: repository map and extracts (Aider-style), project instructions across providers, compression, prompt caching (check Anthropic, OpenAI and Google documentation separately), model routing, structured tool schemas.
2. Differentiation: compare Happy, Vibe Kanban, CloudCLI, Cline and Aider mobile or remote flows (licences in REUSE_BACKLOG.md).
3. Remaining HIG pages (typography, layout, sheets, accessibility) for the web spec.
