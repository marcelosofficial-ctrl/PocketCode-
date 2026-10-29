# PocketCode Decision Log

Only record decisions that have actually been made. Proposals belong in the open questions section until approved.

## D-001: Unified PC-and-phone product direction; separate development boundaries
- **Status:** Accepted
- **Decision:** RevDev and PocketCode are intended to converge into one broader PC-and-phone product/program. During discovery and development, keep their repositories, roadmaps, implementations, acceptance suites, evidence, and release gates separately managed. This decision does not authorize a repository merge, shared-code migration, shared runtime, frontend rewrite, or change to either project's execution/security boundary. Those choices require a separately reviewed, evidence-backed integration plan.
- **Product roles:** RevDev remains the PC-side guarded developer-operations/control-plane path; PocketCode remains the phone-first path.
- **Reason:** Preserve the owner's unified product vision without prematurely selecting integration topology or treating unverified implementation compatibility as fact.

## D-002: Use GitHub as durable project source of truth
- **Status:** Accepted
- **Decision:** Keep product requirements, architecture, safety baseline, roadmap, decisions, and verified status in this repository.
- **Reason:** Multiple AI assistants and future chats need shared, inspectable state independent of conversational memory.

## D-003: Public repository contains no secrets
- **Status:** Accepted
- **Decision:** Treat all committed repository contents as public. Never commit credentials, tokens, private user data, or secret deployment configuration.
- **Reason:** The owner created this repository as public.

## D-004: Validate before committing to a stack or business model
- **Status:** Accepted
- **Decision:** Do not select a runtime vendor, framework, AI provider, monetization plan, or native-app strategy until relevant research and proof points are available.
- **Reason:** Avoid expensive premature commitments.

## D-005: Keep PocketCode at zero spend by default
- **Status:** Accepted
- **Decision:** Work within a $0 budget unless the owner explicitly changes this constraint. Do not start paid trials, attach payment methods, enable billing, purchase services, or run potentially billable workloads without explicit approval.
- **Reason:** The owner has stated they do not want to spend money. Progress should prioritize validation, static prototype improvements, local checks, and careful design over cloud execution experiments.
- **Operational detail:** Promotional credits and advertised free tiers are not proof of zero cost. Conserve GitHub Actions minutes and do not trigger deployments for documentation-only changes.
- **Reference:** [Zero-budget work plan](PRODUCT/ZERO_BUDGET_WORK_PLAN.md).

## Proposed, not yet decided
- Start with a mobile-first PWA.
- Use a remote isolated Python runtime for the first vertical slice.
- Add JavaScript/Node.js or PowerShell later based on evidence.
- Use copy/paste AI handoff before building direct integrations.
- Offer a free tier or paid plans.
- Choose a specific cloud provider, sandbox vendor, or framework.
