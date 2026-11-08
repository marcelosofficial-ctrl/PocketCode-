# STRATEGY PROGRAM: design, PoCo, App Store, website, LinkedIn, governance (tracker)

Started 2026-11-08 by Claude from the owner's master brief. The brief's requirements are the master; findings here support them. Status values: DONE (evidence in repo), PARTIAL, NOT STARTED, BLOCKED. Tags as in other docs.

| # | Deliverable | Status | Evidence / where | Next step | Blocker or owner decision |
|---|---|---|---|---|---|
| 1 | Apple design engineering research | NOT STARTED | none | read Apple HIG pages and Liquid Glass docs; target the real stacks: PoCo today is one static HTML file (prototypes/mobile-runner/index.html, 17 KB) | RevDev UI source is not on GitHub: none of the owner's 12 repositories contains it and DevRelay-Missions has no app folder (VERIFIED by listing); so no RevDev UI inspection is possible until the PC returns |
| 2 | RevDev modernization plan | BLOCKED (partly) | website claims .NET 8 / WPF (UNVERIFIED by source) | document-level plan only; do not touch product | PC access |
| 3 | PoCo product and architecture research | PARTIAL | repo has 100+ research docs; open-source reuse in kit/docs/REUSE_BACKLOG.md | context-engineering and provider-caching research (Anthropic, OpenAI, Google differ) | none |
| 4 | iPhone-only App Store roadmap | DONE (first pass) | IPHONE_ONLY_APP_STORE_ROADMAP_20261108.md | owner decisions G0 | $99 spend, name |
| 5 | Website audit and PoCo plan | PARTIAL | WEBSITE_AUDIT_AND_POCO_PAGE_PLAN_20261108.md | read index.astro, ja pages, other project pages | none |
| 6 | LinkedIn alignment | BLOCKED | the profile URL is public in the site header but LinkedIn cannot be read from this environment | owner pastes the About, Experience and project text | LinkedIn text |
| 7 | GitHub governance audit | PARTIAL | GOVERNANCE_AUDIT_20261108.md (PocketCode); RevDev audit pending | RevDev rules audit | none |
| 8 | Development efficiency research | PARTIAL | kit/docs/WORK_PROTOCOL.md, PLUGIN_LESSONS.md, REUSE_BACKLOG.md | repo-map extract, CI strategy, parallel review pattern | none |
| 9 | Unified cross-AI handoff | PARTIAL | BOOT.md, STATE.md, NEXT_TASK.md, INBOX files | keep updated each pass | none |

## Ground rules for every AI working this program
- Do not claim anything about PoCo that is not built. The website page and LinkedIn text come last and use only VERIFIED facts.
- Do not change the website design. Reuse its existing classes and components.
- Do not merge RevDev and PoCo code or weaken either repo's boundaries. RevDev material stays in the private repo.
- No deployment, enrollment, purchase, secret change or PC action without the owner's explicit authorization.

## Research questions queued for the next passes
1. Apple design: which HIG principles can be expressed in CSS and JavaScript for the PWA and later in SwiftUI (typography with Dynamic Type, spacing, continuous corners, spring motion that respects Reduce Motion, haptics, materials); what Liquid Glass actually requires versus a CSS imitation.
2. PoCo context engineering: repository map and extracts (Aider-style), project instructions across providers, compression, prompt caching (provider-specific: check Anthropic, OpenAI and Google documentation separately), model routing, structured tool schemas.
3. Differentiation: compare Happy, Vibe Kanban, CloudCLI, Cline and Aider mobile or remote flows (licences already in REUSE_BACKLOG.md).
