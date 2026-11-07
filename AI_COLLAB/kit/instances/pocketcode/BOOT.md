# BOOT: PocketCode   (pre-filled from the 2026-11-06 handoff; VERIFY every fact against the live branch)

## Identity
- Phone-first, provider-neutral AI orchestration control plane for iOS and Android: bounded AI work, many providers and execution environments, durable task state, recovery, evidence-backed outcomes.
- Repo: marcelosofficial-ctrl/PocketCode- | Active branch: pocketcode-ai-workflow-director-research-2026-10-28 | Handoff HEAD: c4c93e27bc3b1c20aaf046727fc6e62c86c5aedc (verify live) | Default branch main is STALE (README still says "Discovery").
- Collaboration docs: AI_COLLAB/. Source and tests: scripts/. Entry files: AGENTS.md, CLAUDE.md, GEMINI.md.

## Hard constraints
1. $0 default budget. No paid dependency or provider commitment assumed.
2. Must stay useful without a PC.
3. Provider-neutral. Do not pick a model provider, runtime, database or cloud platform early (no SQLite/Postgres/Redis choice yet).
4. Context transfer is explicit and user-controlled: no clipboard polling, no hidden overlays, no implicit capture.
5. Remote execution (SSH/Tailscale, future cloud fallback) is not an assumed production dependency. Local mobile execution is for light tasks; WASM/Pyodide/JSC are options to evaluate.
6. PocketCode and RevDev stay separate: repos, roadmaps, adapters, acceptance suites, release gates, security boundaries. Never merge code or runtimes.
7. Evidence rules: the event journal prototype (21/21 local tests) is in-memory, not durable, not cryptographic, and its fence-check plus append is not atomic. Coordinator tests (14/14) ran on test doubles, not the canonical checkout. Full Python suite: NOT RUN. Never call any of this durable, secure or product-integrated.
8. Public repo: never commit secrets. No history rewrite, force-push, visibility change or release without owner approval. PRs #2 and #3 are open drafts: do not modify them.
9. Chat messages are not proof; the commit is.

## Read order
1. STATE.md  2. NEXT_TASK.md  3. INDEX.md. Then on demand: AI_COLLAB/EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md, AI_COLLAB/EVENT_JOURNAL_MODEL_20261106.md, AI_COLLAB/CHAT_WORK_LOG.md (last 30 lines only), scripts/.

## Working rules
One chat = one task. Normal mode unless NEXT_TASK says Think. About 350 lines per turn. Checkpoint after each unit. Tag claims VERIFIED / INFERRED / UNKNOWN. Move, never delete.

## Roles
Claude: lead developer and reviewer. Gemini: co-developer and independent security/spec auditor. ChatGPT: continuity holder, evidence reconciler, acceptance architect, coordinator. One primary implementer per task.
