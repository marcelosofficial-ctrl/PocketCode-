# BOOT: PocketCode

## Identity
- Phone-first, provider-neutral AI orchestration control plane for iOS and Android.
- Repo: https://github.com/marcelosofficial-ctrl/PocketCode-
- Active branch: `pocketcode-ai-workflow-director-research-2026-10-28`
- Verified handoff HEAD: `04f4db211d4bfdee76989c1dbe6c8bb9079e9bb0` (2026-11-07). Fetch the live branch before consequential work.

## Hard constraints
1. $0 default. No paid provider, host, workload, account or billing commitment.
2. Must remain useful without a PC.
3. Do not select a provider, runtime, database, backend or cloud platform prematurely.
4. Context transfer is explicit and user-controlled. No clipboard polling or intrusive overlays.
5. Treat submitted code as hostile. Local WASM/Pyodide/JSC are not hostile-code sandboxes.
6. PocketCode and RevDev stay separate in repos, roadmaps, clients, adapters, runtimes, security boundaries, acceptance suites and release gates.
7. Public repo: no secrets. No history rewrite, force-push, release or deployment without owner approval. PR #2/#3 remain untouched.
8. Chat messages are not proof. Verify files, commits and exact-SHA test results.

## Read order
1. `AI_COLLAB/kit/instances/pocketcode/STATE.md`
2. `AI_COLLAB/kit/instances/pocketcode/NEXT_TASK.md`
3. `AI_COLLAB/kit/instances/pocketcode/INDEX.md`
4. Open only task-specific source/spec sections. Read `CHECKPOINT.md` for the last concise checkpoint.

## Working rules
One chat = one bounded task. Normal mode unless the task requires a security/architecture challenge. Keep outputs compact; checkpoint each completed unit. Label VERIFIED / INFERRED / UNKNOWN and PASS / FAIL / NOT RUN. One primary writer per task; other AIs review read-only.

## Roles
- Claude: lead developer and architecture/implementation reviewer.
- Gemini: co-developer and independent security/spec auditor.
- ChatGPT: continuity holder, evidence reconciler, acceptance architect and coordinator.
