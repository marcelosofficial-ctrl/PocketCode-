# Gemini Instructions for PocketCode

Read AGENTS.md first. It contains the shared rules for all agents and contributors. Then read AI_COLLAB/BOOT.md, AI_COLLAB/STATE.md, AI_COLLAB/NEXT_TASK.md and AI_COLLAB/INBOX_gemini.md (together under 2,000 words). Do not open the large history files whole. Report back by appending to AI_COLLAB/INBOX_chatgpt.md or by committing a findings file; if you cannot write to GitHub, ask the owner to paste your report into AI_COLLAB/GEMINI_REVIEW_<date>.md.

(Older instruction, still valid for research tasks: AI_COLLAB/GEMINI_HANDOFF.md describes the multi-pass protocol; keep AI_COLLAB/GEMINI_PROGRESS_LOG.md updated and consolidate final research in AI_COLLAB/MASTER_RESEARCH_IMPLEMENTATION_PLAN.md. Do not stop after a one-pass summary.)

Use PROJECT_STATUS.md, PRODUCT_SPEC.md, ARCHITECTURE.md, SECURITY.md, ROADMAP.md, and DECISIONS.md as current project references, by section. Inspect the repository before relying on prior chat context.

For research, distinguish sourced facts from assumptions and include links and dates. For code review, focus on correctness, edge cases, tests, mobile usability, and whether tests actually demonstrate the claimed behavior.

Do not duplicate another agent's implementation task. Do not claim unrun tests passed. Never commit secrets or personal data to this public repository. Do not change repository visibility, publish releases, or incur paid service costs without owner approval.

Keep the product provider-neutral and validation-first unless a documented decision changes that direction. Do not recommend a public code runner before its isolation and operational safeguards have been reviewed.
