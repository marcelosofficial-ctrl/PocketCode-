# Claude Instructions for PocketCode

Read AGENTS.md first. It contains the shared rules for all agents and contributors.

Before implementation, inspect PROJECT_STATUS.md, PRODUCT_SPEC.md, ARCHITECTURE.md, SECURITY.md, ROADMAP.md, and DECISIONS.md as relevant. Treat the repository as the source of truth; do not infer that an idea discussed in chat has been implemented.

Act as the primary implementer only when a task is explicitly assigned. For review tasks, review requirements, edge cases, tests, and diffs without duplicating the implementation.

Do not claim tests passed without running them and recording evidence. The repository is public, so never commit secrets or personal data. Do not make irreversible repository, release, infrastructure, or billing changes without owner approval.

Keep proposed architecture provider-neutral until a decision is documented. Code execution is a high-risk boundary and requires isolation, quotas, network restrictions, and cleanup.
