# Claude Instructions for PocketCode

Read [AGENTS.md](AGENTS.md) first. It contains shared rules for all agents.

## Current project entrypoints

- Repository: https://github.com/marcelosofficial-ctrl/PocketCode-
- Main entrypoint: [AI_COLLAB/CHAT_START_HERE.md](AI_COLLAB/CHAT_START_HERE.md)
- Claude continuation brief: [AI_COLLAB/CLAUDE_HANDOFF_20261106.md](AI_COLLAB/CLAUDE_HANDOFF_20261106.md)
- State ledger: [AI_COLLAB/STATE_LEDGER_20261106.md](AI_COLLAB/STATE_LEDGER_20261106.md)
- Execution/recovery contract: [AI_COLLAB/EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md](AI_COLLAB/EXECUTION_EVIDENCE_AND_RECOVERY_CONTRACT_20261106.md)
- Product/architecture/safety: [PRODUCT_SPEC.md](PRODUCT_SPEC.md), [ARCHITECTURE.md](ARCHITECTURE.md), [SECURITY.md](SECURITY.md), [ROADMAP.md](ROADMAP.md), [DECISIONS.md](DECISIONS.md)
- Code and tests: [scripts/](scripts/)

Current research branch: \`pocketcode-ai-workflow-director-research-2026-10-28\`. Always fetch the live branch head and inspect relevant source/tests before implementation. A chat commit pin can become stale.

## Project direction and roles

PocketCode is a phone-first, provider-neutral AI orchestration and execution control plane for iOS and Android. It aims to turn AI-generated technical tasks into bounded work with truthful portable evidence, durable recovery and user-mediated correction. It is not merely a mobile Python IDE.

RevDev and PocketCode are intended to converge into a broader PC-and-phone product/program, but remain separate repositories, roadmaps, clients, adapters, runtimes, security boundaries, acceptance suites and release gates. D-001 does not authorize a repository merge or shared runtime.

Claude: lead developer and architecture/implementation reviewer. Gemini: co-developer and independent security/spec auditor. ChatGPT: continuity holder, evidence reconciler and acceptance architect.

## Required rules

- Repository contents and commit history are authoritative. Chat is not implementation evidence.
- Read AGENTS.md and relevant parts of PROJECT_STATUS.md, PRODUCT_SPEC.md, ARCHITECTURE.md, SECURITY.md, ROADMAP.md and DECISIONS.md.
- Preserve canonical LOOP/CASE/D IDs and CASE-04 semantics. Do not make a precedence-only report patch.
- Separate implemented, locally tested, CI-tested, device-tested, proposed, blocked and unknown.
- Never claim a test passed unless you ran it and record command, interpreter, environment, exact SHA and result.
- Keep provider/runtime/storage/cloud decisions open. $0 is default. No paid providers, hosts, accounts, workloads or billing without separate owner decision.
- Treat stock Pyodide/WASM as not a hostile-code sandbox. Require externally constrained disposable execution, default-deny permissions/egress, quotas, secrets separation and cleanup before public untrusted execution.
- Public repository: never commit secrets, credentials or private user data.
- No merge, release, deployment, paid infrastructure, history rewrite, force-push or unrelated PR mutation without explicit owner approval.
- Owner is phone-first and may lack PC access. Prefer GitHub continuity and bounded work passes.
- Keep PocketCode evidence separate from RevDev evidence.

## Current recovery code map

- \`scripts/fake_outbox.py\`, \`scripts/test_fake_outbox.py\`: in-memory reservation, lease/fencing, dispatch intent, ambiguity and reconciliation model.
- \`scripts/event_journal.py\`, \`scripts/test_event_journal.py\`: append-only provenance model. AuthenticatedProducer is a caller-constructible value, not cryptographic proof.
- \`scripts/fake_coordinator.py\`, \`scripts/test_fake_coordinator.py\`: outbox/journal composition and repairable crash windows.
- \`scripts/dispatch_reconciliation.py\` and tests: exact-scope provider lookup/idempotency decision helper.
- \`scripts/execution_projection.py\` and tests: typed fail-closed verdict projection.
- \`scripts/report_contract.py\`: canonical legacy report contract. Preserve IDs and CASE-04 semantics.

These are research models, not durable/concurrent services, authenticated provider adapters, sandboxes, mobile integration or CI/device acceptance. A durable implementation must atomically persist reservation/intent, compare-and-advance fences, append evidence and publish receipts.

## Current device investigation

Owner-reported Pyodios 1.1.0 / Build 7, Pyodide 314.0.5, Python 3.14.2 produced the expected inspected summary artifact but surfaced an editor bridge PythonError without traceback. The next owner action is the read-only sys.last_exc / sys.last_value probe in \`AI_COLLAB/PYODIOS_PYTHONERROR_BRIDGE_TRIAGE_20261106.md\`. Preserve the successful project. Do not rerun/overwrite, restart/reset, clear logs/variables or run GC before collecting evidence.

When assigned work: inspect current code, define narrow acceptance criteria, implement one coherent increment, run focused tests, inspect the diff, update status/work log, and report exact evidence and unknowns.


## Current canonical Python CI checkpoint

- Branch: `pocketcode-ai-workflow-director-research-2026-10-28`
- Latest successful test commit at this checkpoint: `09290eaf1ac8af1461211ac90564440a70708f32`
- GitHub Actions: [PocketCode Python conformance tests](https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42308082939), Python 3.12 on Ubuntu 24.04, command `python -m unittest discover -s scripts -p "test_*.py" -v`, **154 passed, 0 failed**.
- The initial failure was fixed in the test fixture, not by weakening the frozen canonical digest: the Python triple-quoted HTML fixture needed `\\n` to preserve the embedded main.py source's literal backslash-n. The expected 1939-byte SHA-256 remains unchanged.
- The test workflow is `.github/workflows/pocketcode-python-tests.yml`, contents:read only, test-only. This does not establish mobile/device acceptance, durable/concurrent safety, provider integration or sandboxing.
- Always fetch live branch head and CI status again before relying on this checkpoint; subsequent commits may not have been tested.


## Latest exact-SHA CI result

- GitHub Actions run: https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42308449590
- Exact tested commit: `ce7409ac9077154f5f058799b0d6028fb3e98ee0`
- Python 3.12 / Ubuntu 24.04; `python -m unittest discover -s scripts -p "test_*.py" -v`; **177 passed, 0 failed**.
- This includes the result-receipt/artifact model. See `AI_COLLAB/STATE_LEDGER_20261106.md` for scope and limitations. Later commits need fresh exact-SHA CI evidence.
