# Claude continuation brief: PocketCode (2026-11-06)

Repository: https://github.com/marcelosofficial-ctrl/PocketCode-  
Research branch: \`pocketcode-ai-workflow-director-research-2026-10-28\`  
Branch: https://github.com/marcelosofficial-ctrl/PocketCode-/tree/pocketcode-ai-workflow-director-research-2026-10-28  
Always fetch the live branch head before work. The commit that adds this brief is not a permanent latest pin.

## Mission

PocketCode is a phone-first, provider-neutral AI orchestration and execution control plane for iOS and Android. It aims to turn AI-generated technical tasks into bounded execution, truthful evidence and artifacts, durable recovery, and user-mediated correction through any AI assistant. It is not another generic mobile Python IDE.

MVP hypothesis: explicit paste/import; bounded execution; honest lifecycle/stdout/stderr/exit evidence; real artifact listing/export; compact copyable evidence report; distinct preserved attempts. Later candidates include CSV/JSON validation, file conversion, test execution, multi-file workspaces, remote SSH/Tailscale adapters and optional cloud adapters. GUI automation, arbitrary package installation, open internet and direct AI integrations are not MVP commitments.

## Architecture and non-decisions

- $0 default. No paid provider, account, host, workload or billing commitment.
- No provider, model, runtime, app framework, database, storage engine, backend or cloud host selected.
- Local mobile WASM/Pyodide/JSC are candidates for lightweight tasks, not hostile-code sandboxes.
- SSH/Tailscale and optional cloud execution remain adapter candidates.
- Untrusted execution requires disposable externally constrained isolation, default-deny permissions/egress, quotas, secrets separation and cleanup.
- Explicit paste-to-context. No clipboard polling or intrusive overlays.
- RevDev and PocketCode share product direction only. Keep repositories, roadmaps, clients, adapters, runtimes, security boundaries, acceptance suites and release gates separate. No repo merge/shared runtime implied.

## Roles

Claude: lead developer and architecture/implementation reviewer. Gemini: co-developer and independent security/spec auditor. ChatGPT: continuity holder, evidence reconciler, acceptance architect and cross-project coordinator.

## Read first

- [AGENTS.md](../AGENTS.md), [CLAUDE.md](../CLAUDE.md)
- [CHAT_START_HERE.md](CHAT_START_HERE.md)
- [STATE_LEDGER_20261106.md](STATE_LEDGER_20261106.md)
- [CHAT_WORK_LOG.md](CHAT_WORK_LOG.md)
- [PROJECT_STATUS.md](../PROJECT_STATUS.md), [PRODUCT_SPEC.md](../PRODUCT_SPEC.md), [ARCHITECTURE.md](../ARCHITECTURE.md), [SECURITY.md](../SECURITY.md), [ROADMAP.md](../ROADMAP.md), [DECISIONS.md](../DECISIONS.md)
- [EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md](EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md)
- [VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md](VERDICT_EVIDENCE_EXIT_PROVENANCE_MATRIX_20261105.md)
- [SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md](SEMANTIC_DECISIONS_AND_REPORT_PROJECTION_20261029.md)
- [TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md](TRANSITION_AND_REPORT_PROJECTION_MATRIX_20261029.md)
- [AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md](AI_WORKFLOW_DIRECTOR_CONFORMANCE_TEST_SPEC_20261028.md)
- [AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES_20261028.md](AI_WORKFLOW_DIRECTOR_CANONICAL_FIXTURES_20261028.md)
- [POCKETCODE_TASK_EVIDENCE_RECOVERY_RESEARCH_20261106.md](POCKETCODE_TASK_EVIDENCE_RECOVERY_RESEARCH_20261106.md)
- [OPEN_SOURCE_AGENT_ARCHITECTURE_AND_CODE_ADOPTION_REVIEW_2026-11-05.md](../RESEARCH/OPEN_SOURCE_AGENT_ARCHITECTURE_AND_CODE_ADOPTION_REVIEW_2026-11-05.md)
- [CODE_LEVEL_OPEN_SOURCE_REUSE_REVIEW_20261105.md](../RESEARCH/CODE_LEVEL_OPEN_SOURCE_REUSE_REVIEW_20261105.md)
- [REMOTE_EXECUTION_EVENT_RECOVERY_AND_SCHEDULER_COMPETITOR_AUDIT_20261105.md](../RESEARCH/REMOTE_EXECUTION_EVENT_RECOVERY_AND_SCHEDULER_COMPETITOR_AUDIT_20261105.md)
- [MOBILE_INTERRUPTION_RECOVERY_AND_OPEN_SOURCE_SYNC_AUDIT_20261105.md](../RESEARCH/MOBILE_INTERRUPTION_RECOVERY_AND_OPEN_SOURCE_SYNC_AUDIT_20261105.md)
- [FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md](FOUR_MONTH_PHONE_ONLY_MASTER_PLAN_20261028.md), [POCKETCODE_CONTINUITY_HUB_20261028.md](POCKETCODE_CONTINUITY_HUB_20261028.md)
- [PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md](PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md)

## Current recovery implementation map

Inspect branch versions:
- \`scripts/fake_outbox.py\` and \`scripts/test_fake_outbox.py\`: in-memory reservation, lease/fence, dispatch intent, ambiguous-send recovery, reconciliation and fake idempotent receiver.
- \`scripts/event_journal.py\` and \`scripts/test_event_journal.py\`: append-only event provenance, exact immutable bytes, source-scoped identity, duplicate replay and conflict quarantine. AuthenticatedProducer is caller-constructible and is not cryptographic proof.
- \`scripts/fake_coordinator.py\` and \`scripts/test_fake_coordinator.py\`: composition and repairable crash windows.
- \`scripts/dispatch_reconciliation.py\` and tests: exact-scope provider lookup/idempotency decision helper.
- \`scripts/execution_projection.py\` and tests: typed fail-closed execution verdict projection.
- \`scripts/report_contract.py\`: canonical legacy report contract. Preserve IDs and CASE-04 semantics.

All above are research/conformance models, not production coordinator services, durable storage, concurrency-safe transactions, authenticated provider adapters, sandboxing, mobile integration or CI/device acceptance.

## Canonical semantics

- Preserve LOOP/CASE/D IDs and CASE-04 wording unless a separately reviewed decision changes them. Trusted lifecycle timed_out remains INCOMPLETE/timed_out.
- Keep CommandId, EffectId, DispatchAttemptId, ExecutionId, observation sequence and ResultReceipt distinct.
- Matching EffectId/fingerprint authorizes exact-scope lookup/reconciliation, not blind replay.
- Ambiguous post-send state must reconcile before retry. Eventually consistent or non-authoritative not-found is not final absence.
- Same logical effect retries reuse stable effect/attempt identities and exact request. A genuinely new attempt requires a new DispatchAttemptId and explicit authorization.
- Exact event replay requires same event identity, immutable payload bytes and occurrence timestamp. Conflicts are quarantined, never overwritten.
- Producer occurrence time and coordinator observation order are distinct. Coordinator sequence orders accepted events.
- Do not infer child exit, sandbox success, cleanup or artifact releasability from wrapper/interpreter/transport results.

## Current device evidence

Owner-reported Pyodios 1.1.0 / Build 7, Pyodide 314.0.5, Python 3.14.2. An unchanged canonical main.py/items.csv run generated the expected inspected summary.json (grand total string 10.75; notebook 7.00 and pen 3.75) but Editor showed [Bridge/executePython] PythonError. Error Log contained only Editor: PythonError, no traceback. Classification: artifact-level functional success, bridge error unresolved, full run inconclusive. Native process exit, stderr and bridge root cause unknown. Export/read-back, relaunch persistence, malformed-input and PocketCode acceptance not run.

Next owner action: read-only sys.last_exc / sys.last_value probe in the Pyodios triage file, in the existing session. Preserve the successful project. Do not rerun/overwrite, restart/reset, clear logs/variables or run GC before collecting evidence.

## Next engineering gate

Continue fake coordinator composition:
1. Exercise reservation/dispatch-intent and all crash boundaries.
2. Verify event append/replay and outbox acknowledgement repair.
3. Rebuild lifecycle projections after interruption.
4. Add adversarial tests for stale workers, duplicate/conflicting events, stable timestamps, partial writes and mismatched attempt identity.
5. Only after semantics stabilize, design a durable adapter with atomic reservation/intent, fence compare-and-advance, append and receipt publication. Test concurrency and process/power loss before selecting storage.

Do not select SQLite/Postgres/Redis/cloud/provider as a side effect. Any SQLite candidate must pin a version/build with the WAL-reset fix (3.51.3 or supported backport). MCP Tasks remain experimental; A2A stream/history is not an authoritative execution receipt.

## Change protocol

Inspect current branch/source, define narrow acceptance criteria, implement one coherent increment, run focused tests in a real checkout, inspect diff, update ledger/work log. Record exact commit, paths, commands, interpreter, results and limitations. Never promote a stubbed contract-harness result to canonical repository test evidence.
