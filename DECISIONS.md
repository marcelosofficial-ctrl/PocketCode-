# PocketCode Decision Log

Only record decisions that have actually been made. Proposals belong in the open questions section until approved.

## D-001: Keep PocketCode separate from RevDev
- **Status:** Accepted
- **Decision:** PocketCode is a separate product and repository. Do not combine its code, roadmap, or project state with RevDev.
- **Reason:** Different product purpose and lifecycle.

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

## Proposed, not yet decided
- Start with a mobile-first PWA.
- Use a remote isolated Python runtime for the first vertical slice.
- Add JavaScript/Node.js or PowerShell later based on evidence.
- Use copy/paste AI handoff before building direct integrations.
- Offer a free tier or paid plans.
- Choose a specific cloud provider, sandbox vendor, or framework.
