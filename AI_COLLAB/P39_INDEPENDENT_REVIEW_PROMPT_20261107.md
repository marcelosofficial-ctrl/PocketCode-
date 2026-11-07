# PocketCode P39 independent adversarial review brief

**Review date:** 2026-11-07  
**Repository:** https://github.com/marcelosofficial-ctrl/PocketCode-  
**Active branch:** pocketcode-ai-workflow-director-research-2026-10-28  
**Current documentation HEAD:** 6a9e84ab1735291c5f2d7e50d152ea083047af14  
**Tested source/test commit:** 744cb4dc7cd4994647c84ac7476d0c78a21f0540  
**Exact-head CI:** https://github.com/marcelosofficial-ctrl/PocketCode-/actions/runs/42365455316 (266/266 passed)

## Assignment

Perform an independent adversarial architecture, correctness and security review of the release-grant recovery/concurrency work. Do not edit the repository, create commits, open/modify PRs, or claim tests you did not run. Return findings with severity, exact file/line or symbol, concrete counterexample/interleaving, impact, and a specific correction. Separate VERIFIED source-backed facts from INFERRED conclusions and UNKNOWN assumptions. If a file is inaccessible, say NOT REVIEWED.

## Project context and non-negotiable boundaries

PocketCode is a phone-first, provider-neutral Agentic Orchestration Control Plane for iOS and Android. Its product direction is a PC-and-phone program with RevDev, but repositories, roadmaps, clients, adapters, runtimes, security boundaries, acceptance suites and release gates remain separate. No shared runtime or repository merge is implied.

- $0 default budget. No paid provider, host, workload, account, subscription or billing commitment.
- No provider, runtime, app framework, database, storage engine, backend or cloud host selected.
- Phone-first; do not require the owner's PC.
- Explicit paste-to-context; no clipboard polling or intrusive overlays.
- Treat submitted code as hostile. Local WASM/Pyodide/JSC are convenience execution, not hostile-code sandboxes.
- No secrets in public repository.
- Preserve canonical LOOP/CASE/D IDs and semantics; do not rewrite CASE-04.
- Unknown/degraded evidence must not become product PASS/FAIL.
- No PR #2/#3/#4 changes, merge, deployment, installation, secret access, hosted workload or provider call.
- The current release-grant and outbox implementations are sequential in-memory models, not production adapters.

## Read these exact files first

1. [P39 research and red-team packet](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/RELEASE_GRANT_ADAPTER_RESEARCH_AND_REDTAM_20261107.md)
2. [P37 concurrency and crash contract](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/RELEASE_GRANT_CONCURRENCY_AND_CRASH_CONTRACT_20261107.md)
3. [Durable adapter contract](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-11-28/AI_COLLAB/DURABLE_ADAPTER_CONTRACT_20261106.md)
4. [Reference model](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/744cb4dc7cd4994647c84ac7476d0c78a21f0540/scripts/release_grant_conformance.py)
5. [Reference model tests](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/744cb4dc7cd4994647c84ac7476d0c78a21f0540/scripts/test_release_grant_conformance.py)
6. [Existing release-grant implementation](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/744cb4dc7cd4994647c84ac7476d0c78a21f0540/scripts/result_receipts.py)
7. [Existing release-grant tests](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/744cb4dc7cd4994647c84ac7476d0c78a21f0540/scripts/test_result_receipts.py)
8. [Fake outbox model](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/scripts/fake_outbox.py)
9. [Event journal model](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/scripts/event_journal.py)
10. [Project status](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/PROJECT_STATUS.md)
11. [Roadmap](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/ROADMAP.md)
12. [State ledger](https://github.com/marcelosofficial-ctrl/PocketCode-/blob/pocketcode-ai-workflow-director-research-2026-10-28/AI_COLLAB/STATE_LEDGER_20261106.md)

**Note:** Link 3 is the intended existing file path. If any link is unavailable, locate it through the active branch tree and report its exact status rather than guessing.

## Claude-specific review focus

Act as lead developer and architecture/implementation reviewer. Prioritize:
- Is the stable receipt-head lock/CAS contract sufficient to prevent first-head, successor and grant races?
- Are commit linearization and ambiguous-response recovery correctly defined?
- Are stable intent fingerprint and current authorization proof separated without permitting cross-scope replay?
- Are all grant/event/outbox writes atomic and are all event-order gaps recoverable?
- Are fence epochs durable across deletion, restore and migration?
- Can a stale worker continue a network stream after losing its lease, and what exact transport primitive is required?
- Does the sequential model accurately represent the required state machine, or does it encode assumptions that would fail in a real adapter?
- Identify missing tests, incorrect assertions, unhandled states and portability assumptions.

Return: (1) blocking findings, (2) high-risk findings, (3) proposed minimal corrections, (4) exact adapter contract clauses needing changes, (5) recommended next implementation slice. Do not implement.

## Gemini-specific review focus

Act as co-developer and independent security/spec auditor. Prioritize:
- Threat-model the caller-supplied authorization and producer identity boundary.
- Test principal/tenant isolation, request-key collisions, object-version substitution, replay after revocation and stale proof.
- Challenge event identity, digest provenance, event ordering, gap deferral and consumer idempotency.
- Challenge lease expiry, fencing-token authority, stale stream behavior and fence reset after recovery/restore.
- Identify any claim that overstates what the in-memory model or 266/266 CI proves.
- Check whether PostgreSQL, SQLite, DynamoDB, etcd, Redis and Temporal research accurately reflects their official guarantees and whether any important caveat is missing.
- Flag licensing or maintenance claims that are not supported by official project sources.

Return: (1) exploitable or correctness-critical counterexamples, (2) security boundary corrections, (3) missing adversarial tests, (4) source-backed research corrections, (5) a risk-ranked disposition: ACCEPT / ACCEPT WITH CHANGES / REJECT. Do not implement.

## Shared output requirements

- Review exact branch/code pins above, not an old memory of the project.
- Quote exact method names and line numbers.
- Give a reproducible schedule or input for each finding.
- Distinguish a model-level failure from a production-adapter failure.
- Do not recommend a database or service without evidence about the actual target deployment topology and $0 budget.
- Do not invent CI results. The 266/266 run is exact for source/test SHA 744cb4dc7cd4994647c84ac7476d0c78a21f0540. The latest branch HEAD 6a9e84ab1735291c5f2d7e50d152ea083047af14 adds only ledger/work-log/entrypoint documentation after that tested source/test commit.
- Return the complete review in a standalone Markdown document suitable for committing to a review branch, but do not commit it yourself.

## Required final section

End with:
- Findings ranked by severity.
- Any assumptions that could not be verified.
- Exact files and line ranges reviewed.
- Whether the reviewer recommends the next step be model correction, adapter implementation planning, or further research.
