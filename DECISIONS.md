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


## D-006: Use evidence-separated lifecycle semantics for the first verifier
- **Status:** Accepted for provider-neutral contract and offline-test design; not a public API freeze.
- **Decision:** Preserve immutable execution observations separately from cleanup state and versioned derived job disposition. PASS requires authoritative zero exit, exact required policy confirmation before start, termination evidence, no prohibited timeout/cancel/limit/truncation, validated artifacts, correct tenant/job association, and confirmed cleanup. Artifacts remain quarantined until cleanup and integrity/authorization gates pass. Coordinator-ingress sequence determines replay order; idempotency is tenant-scoped and server-fingerprinted; output caps fail closed.
- **Reason:** Prevent false PASS, unsafe result exposure, duplicate execution, and irreproducible race handling while keeping the design provider-neutral and testable without spend.
- **Limits:** Offline-test defaults are 32 KiB stdout, 32 KiB stderr, 64 KiB aggregate retained output, 1-second bounded drain/discard, 10-second wall time, 64 KiB source, 256 KiB inputs, 10 artifacts, 256 KiB per artifact, and 1 MiB total artifacts. These are provisional test values, not production capacity/security claims. A 30-day post-deletion idempotency tombstone is an MVP policy choice and must be revisited if retention/privacy evidence warrants.
- **Evidence:** [Decision packet](AI_COLLAB/PASS1_OWNER_DECISION_PACKET_20261027.md); [research rationale](AI_COLLAB/PASS1_OWNER_DECISIONS_RESEARCH_20261027.md); [draft contract](AI_COLLAB/DRAFT_EXECUTION_CONTRACT.md).
- **Not authorized:** provider selection, accounts, spend, live execution, production implementation, merge, or deployment.
