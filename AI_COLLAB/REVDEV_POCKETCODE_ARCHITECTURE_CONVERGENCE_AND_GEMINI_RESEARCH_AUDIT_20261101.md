# RevDev + PocketCode Architecture Convergence and Gemini Research Audit

**Date:** 2026-11-01  
**Status:** Architecture analysis and candidate triage only. No adoption decision, implementation, test execution, provider call, account, spend, merge, deployment, or host action.  
**Branch:** `pocketcode-execution-boundary-crosswalk-2026-11-01`  
**Scope:** Review the owner-supplied Gemini open-source report against current project constraints and the existing lifecycle/trust work. Identify genuinely shareable contracts without merging product-specific execution/security models.

## 1. Executive verdict

Gemini's report is a useful candidate inventory and research accelerator. It is not yet a reliable implementation plan. Several recommendations are directionally valuable, but the report mixes four different evidence levels: upstream project facts, architectural patterns, proposed product designs, and unsupported quantitative or security claims. Those must not be treated as equivalent.

The most important conclusion is **share contracts and evidence semantics, not execution engines**. RevDev and PocketCode can converge toward one coherent PC-and-phone product/program while retaining distinct runtime adapters, authorization boundaries, persistence implementations, failure models, and acceptance suites.

Recommended convergence shape:

1. A small, versioned, language-neutral **task and evidence contract** shared by both products.
2. A shared vocabulary for identity, lifecycle observations, idempotency intent, event provenance, execution outcome, job disposition, evidence completeness, and artifact-release decisions.
3. Product-owned coordinators and durable stores that implement those contracts according to their actual runtime constraints.
4. Product-owned execution adapters: Windows/PowerShell/process/filesystem for RevDev; browser/mobile, user-owned remote hosts, and any future approved provider adapters for PocketCode.
5. Separate security policies, acceptance suites, release gates, and runtime evidence. No acceptance result transfers automatically between products.

**No common runtime, queue library, MCP mandate, provider, or shared-code extraction is approved by this document.**

## 2. Evidence discipline and current boundaries

The current PocketCode status describes a discovery/MVP-definition phase. Execution location remains undecided. The first product proof is still a fixed, bounded task comparison, with the same task evaluated across manual, browser-local/WASM, on-device, user-owned remote-PC, and hosted alternatives only when appropriately authorized. Budget remains $0. The static prototype is not an execution backend.

PocketCode's recent coordinator documents are design/test specifications, not implementation proof. In particular:
- `UNIFIED_COORDINATOR_FAILURE_INJECTION_SPEC_20261101.md` is a proposed failure-injection and state-machine specification; new cases are NOT RUN.
- `UNIFIED_COORDINATOR_ADVERSARIAL_REVIEW_20261101.md` records design-level findings; no owner decision is closed by it.
- `LIFECYCLE_ORDERING_AND_EVIDENCE_PRESERVATION_REVIEW_20261101.md` identifies lifecycle-ordering risks; proposed LIFE cases are NOT RUN.
- `POCKETCODE_EXECUTION_BOUNDARY_TRUST_CROSSWALK_20261101.md` and prior report/lifecycle reviews are design/evidence reconciliations, not live service proof.

RevDev remains a Windows-local automation product whose current source, installed binary, runtime, watcher, queue, and sink are UNKNOWN until PC access returns. Its publisher/orphan/retry/recovery P0 remains release-blocking. RelayRef v0.9's Python reference result (293/293) does not prove C# integration, Windows product behavior, or current host state. C# specs remain proposed, not integrated. P8U/P0-D runtime acceptance remains NOT RUN in the required live shape.

The products are intended to converge at the product/program level. Their repositories, roadmaps, implementations, evidence, acceptance suites, security boundaries, and release gates remain separately managed during development. This is not permission to merge repositories or share a runtime.

## 3. Convergence architecture: what should be shared

### 3.1 Shareable domain-neutral contracts

These are candidates for a versioned schema/specification, not necessarily a common executable library.

| Contract area | Shared minimum | Must remain product-owned |
|---|---|---|
| Task packet | Stable task ID; objective; scoped inputs; constraints; explicit allowed/denied actions; acceptance criteria; non-goals; requested output | Product-specific task types, UI, policy and validation |
| Work plan | Stable step IDs; dependency/order; expected completion evidence; retry classification; bounded attempts | Scheduler, concurrency, prioritization, worker allocation |
| Identity | Distinguish task/job, attempt, execution instance, event, evidence object, artifact, release decision | Identity generation, persistence, tenancy/account model |
| Lifecycle vocabulary | Accepted, queued, claimed, dispatch-intent, started, running, cancellation-requested, cancelled, terminal, unknown/reconciliation-required | Legal transitions and operational semantics for each adapter |
| Outcome/disposition | Separate execution outcome from job/coordination disposition; PASS/FAIL/INCOMPLETE semantics grounded in authoritative evidence | Product-specific terminal-state mapping and acceptance tests |
| Idempotency | Explicit operation identity, request fingerprint, scope, retention assumptions, duplicate/ambiguous-response behavior | Atomicity mechanism and actual guarantee supported by store/provider |
| Event envelope | Schema version, event identity, source namespace, subject identity, sequence/scope, timestamp provenance, payload digest, producer | Trusted ingress, authentication, ordering, dedupe and projection rules |
| Evidence envelope | Provenance, capture time, source, boundedness, completeness, truncation/unknown state, content digest | Collector implementation, retention, access controls, storage |
| Artifact contract | Artifact identity, digest, size/type, expected-vs-optional state, authorization decision, transfer status | Filesystem/object store, download channel, mobile share and Windows publication |
| Continuation capsule | Exact checkpoint, completed steps, unresolved items, next action, source pins and evidence references | Chat/provider-specific adapters and context limits |
| Audit/trace | Correlation IDs, actor/action/result, policy revision, causal links | Local event store, telemetry backend, privacy and retention |

### 3.2 Shared specification before shared code

The safest first convergence deliverable is a small, versioned JSON Schema or equivalent language-neutral contract plus golden fixtures. It should define field meaning and negative cases, not prescribe a particular database or process model. Both products should independently implement adapters and run their own tests against the fixtures.

Do not prematurely create a shared package that imports Windows APIs, browser APIs, provider SDKs, MCP libraries, database clients, or runtime-specific process abstractions. A shared package should remain dependency-light and should not become a second coordinator.

### 3.3 What is not safely shareable

- Queue scheduling and worker leasing implementation.
- Process creation, process-tree termination, shell invocation, environment construction.
- File watcher debounce, Windows path normalization, NTFS semantics, file locks, cleanup.
- Mobile browser storage, iOS lifecycle/memory behavior, share sheets, background suspension.
- SSH key handling, remote host bootstrap, Linux sandbox setup, network/egress policy.
- Provider dispatch, cancellation, token retention and reconciliation.
- Artifact publication, download authorization and byte-transfer semantics.
- Product-specific release gates and acceptance IDs.

## 4. High-risk coupling to avoid

### 4.1 A shared state machine must not flatten unlike lifecycles

PocketCode's proposed coordinator has explicit dispatch-intent, provider-start, event-ingress, output collection, report publication, release authorization, and transfer-completion boundaries. RevDev's current P0 concerns publisher/orphan/retry/recovery around local mission and queue operations. Similar words do not prove identical transition semantics.

A shared vocabulary is useful. A single universal transition graph is not yet justified. In particular, `accepted` is not `started`; a cancellation request is not effective termination; execution PASS is not publication permission; release authorization is not proof that transfer completed; and a successful child process does not prove all script-reported checks passed.

### 4.2 Do not share a single authorization or policy engine by assumption

The authority to run a PowerShell process on the owner's Windows machine is materially different from permission to run untrusted code in a mobile browser, on a user-owned remote Linux machine, or in a hosted sandbox. A common envelope can carry policy context and decision evidence, but each execution boundary needs its own enforcement point, capability set, trusted identity, and tests.

### 4.3 Do not equate MCP with job orchestration

MCP standardizes client/server interaction around tools, resources and prompts, with transports and authorization mechanisms defined by the protocol/SDK. It does not by itself provide the products' durable job identity, atomic reservations, provider idempotency, worker fencing, crash recovery, evidence retention, report history, artifact-release authorization, or transfer receipts. Keep those in the product coordinator and contracts.

### 4.4 Do not force one queue/database across both products

A durable queue is a candidate implementation for RevDev, not automatically a PocketCode dependency. PocketCode may need a local/browser journal, a remote coordinator, or no durable local execution queue for its first bounded MVP. RevDev's Windows process and queue recovery semantics must be proven in its target environment before selecting or replacing its queue.

## 5. Gemini candidate-by-candidate audit

The ratings below are this review's triage, not a claim that every upstream code path or license has been fully audited.

| Candidate | Useful contribution | Main caveat / correction | Current disposition |
|---|---|---|---|
| Cline SDK | Layering between shared contracts, model providers, stateless agent loop, stateful core, and host apps is a strong architecture reference | Cline is a substantial evolving runtime, not a drop-in transport-neutral host abstraction. Its own architecture separates agent loop from persistent host lifecycle and provider concerns. Avoid importing its cloud/account assumptions | Study architecture; do not adopt wholesale |
| Aider repo map | AST/tag-based repository summaries can reduce prompt scope and improve navigation | Token reduction claims such as 80% are unsubstantiated for our workload. Python implementation and Tree-sitter dependencies may not fit a mobile TypeScript bundle directly. Must benchmark against fixed tasks and compare simpler symbol indexing | High-value experiment, not direct vendoring decision |
| River | Durable background-job design, transactional insertion, retry scheduling and worker coordination are relevant to RevDev | Current Go source includes a `riverdriver/riversqlite` package, so SQLite support is not merely a non-Go/polyglot feature. However, the driver source explicitly labels it early testing with minimal real-world use, warns about SQLite's single-operation concurrency and `SQLITE_BUSY`, recommends a one-connection pool workaround, and notes slower row-at-a-time completion/InsertMany behavior than Postgres. This makes River more plausible technically but materially weakens the claim that it is a production-ready direct fit for RevDev. Required transaction semantics, Windows deployment, migration/operational cost, and process-supervision needs still require verification. Queue leasing is not proof of fencing an already-issued external process or provider call | Strong RevDev candidate for source-level feasibility study only; not selected |
| MCP TypeScript SDK | Useful standard interface for tool discovery/invocation and resource/prompt exchange | SDK is TypeScript/Node/Bun/Deno oriented; current main branch is v2 and documents the 2026-07-28 spec, while v1.x is separate. It is not a shared Go/.NET/PowerShell implementation. MCP is not the durable mission/event/evidence protocol | Optional adapter boundary; pin version and transport/security profile before use |
| DevPod | Client-only provider abstraction and devcontainer-based remote environment model are relevant to user-owned remote hosts | DevPod is a desktop-oriented developer-environment manager. Its provider/SSH approach does not automatically solve phone UX, mobile SSH key custody, agent protocol, host trust, execution authorization, or a zero-cost reachable host. Provider repo freshness and support must be checked | Architectural reference for future remote-host adapter; not MVP prerequisite |
| isomorphic-git | Browser-compatible Git implementation with pluggable filesystem and HTTP clients | Upstream README explicitly warns LightningFS can apply file operations out of order and crash can corrupt a repo; `fs.flush()` after Git operations is a mitigation. Browser CORS constraints can require a proxy. This introduces durability, credential and network-path concerns | Candidate for isolated prototype experiment only |
| LightningFS | IndexedDB-backed filesystem adapter for isomorphic-git | It implements only a subset of Node fs and serializes access through a mutex/cache. It is not a general sandbox, not equivalent to durable native filesystem semantics, and its own companion README highlights ordering/crash caveats | Evaluate only alongside crash/reload and Safari tests |
| Pyodide | A credible browser-local Python runtime for bounded tasks | Must use the existing fixed-task comparison and real device measurements. Avoid generic memory ceilings or claims that WASM memory bounds prevent all browser/process exhaustion. Browser tab eviction, WebView lifecycle, package loading and CPU blocking remain relevant | Existing MVP candidate; no runtime selection |
| nsjail / bubblewrap | Linux namespace/seccomp sandbox references for a future remote Linux executor | Not applicable to iOS browser sandboxing or Windows PowerShell. They are not plug-and-play; kernel features, user namespaces, mounts, seccomp policy, UID/GID mapping and host configuration matter. A sandbox does not alone solve network egress, secrets, persistence or kernel escape risk | Remote Linux hardening research only |
| OpenHands | Event-driven agent execution and event stream concepts | Large platform and its environment model may exceed $0 budget/phone-first MVP. Event stream patterns can be studied without adopting platform | Study selected concepts only |
| Hatchet | Workflow/DAG design and scheduling concepts | Adds distributed control-plane complexity; no demonstrated need for PocketCode MVP or RevDev before core recovery gaps are understood | Defer |
| Temporal | Mature durable workflow semantics | Operational complexity and infrastructure overhead likely disproportionate to current scope; no need to select now | Defer, not a blanket technical rejection |
| Inngest | Event-driven workflow patterns | Gemini's SSPL statement needs version/component-specific legal review; do not generalize from a label or SDK license to every distribution mode | No adoption; re-check legal facts if reconsidered |
| Daytona | Historical execution-environment patterns | Repo split/private-core claim needs exact current source evidence; hosted execution conflicts with current $0/no-provider constraints unless owner changes them | Defer |
| SWE-agent | Shell/task interface design and agent-computer interaction | Useful interaction patterns, but not a durable coordinator or security boundary | Study selected patterns |

## 6. Important corrections to Gemini's report

1. **River's Go SQLite support exists, but is explicitly early-stage.** The current Go tree contains `riverdriver/riversqlite` and a separate `riverdriver/riverpgxv5`. The SQLite driver's own source says it is in early testing with minimal real-world use, describes SQLite's single-operation concurrency and `SQLITE_BUSY` risk, suggests a one-connection pool, and documents slower row-at-a-time completion/InsertMany behavior. So Gemini was right that River has a Go SQLite driver, but calling it a production-ready direct dependency for RevDev is premature. The current root Go module depends on `riverpgxv5`, not `riversqlite`, which is another reason to inspect the exact integration and version. Evaluate Postgres and SQLite separately against RevDev's offline/local requirements, contention profile, recovery semantics, Windows operation and backup strategy.
2. **Queue leases are not universal fencing.** A queue can coordinate ownership of a row/job, but it cannot retract an external process start already issued, stop a detached child, revoke a provider request in flight, or guarantee no duplicate side effect. RevDev and PocketCode must test process/provider effects beyond the queue's transaction boundary.
3. **MCP is not the universal shared orchestration layer.** It is a tool/context interaction protocol. It can be an adapter at the tool boundary, but cannot replace our coordinator state, durable identity, idempotency, event provenance, authorization, evidence, recovery, or release model.
4. **The MCP SDK version is moving.** The official TypeScript SDK README says `main` is v2, implementing the 2026-07-28 MCP spec; v1.x remains on a separate branch. The Gemini report does not pin an SDK release or spec version. Do not put an unpinned SDK in a shared architecture.
5. **isomorphic-git + LightningFS is not a risk-free local Git layer.** Upstream README explicitly warns of out-of-order file operations and possible repository corruption after a crash, suggesting `fs.flush()` after Git operations. It also documents browser CORS limitations and the need for a proxy in common remote operations. Both affect a mobile-first design materially.
6. **DevPod is not proof of a phone-ready remote runtime.** Its own README describes a client-only tool for reproducible DevContainer environments, controlled by a local computer and provider abstraction. Adapting the provider pattern is reasonable; adopting DevPod wholesale on a phone is not established.
7. **Memory numbers are not portable safety limits.** A generic iOS Jetsam threshold such as 1.5–3.8 GB is not a safe product budget. Termination depends on device, OS, process class, concurrent memory pressure and workload. We need device-specific measurements and graceful recovery, not a fixed internet-derived ceiling.
8. **Pyodide size/load statements need exact version and artifact measurement.** A compressed download size does not equal resident memory, startup cost, peak heap, package cost, or execution headroom. Measure the actual pinned runtime and workload on target devices.
9. **nsjail/bubblewrap do not secure a generic remote host by declaration.** Their protection depends on kernel support and correct configuration. They are Linux-only tools and cannot be presented as the sandbox for PocketCode's local iOS/Android runtime or RevDev's Windows process runner.
10. **Credential-in-RAM and temporary environment variables are not sufficient secret controls.** Environment variables can be inherited, inspected by child processes or exposed in diagnostics/crash dumps. Stdin is not automatically safe either. Define narrowly scoped capabilities, short-lived credentials, explicit redaction, process visibility assumptions and revocation; never put secrets in logs, reports, workspace files or agent-visible context unless specifically required.
11. **The 9–14 month development-time reduction is unsupported.** No baseline, work breakdown, productivity model, benchmark, integration estimate or confidence interval is supplied. Remove it from planning and do not use it for schedule decisions.
12. **License summaries are not legal conclusions.** Confirm exact repository license files, vendored file provenance, transitive dependencies, version tags and distribution model. In particular, do not infer all River polyglot implementations share identical licensing or that a package dependency automatically eliminates all MPL obligations. Maintain an SBOM/notice review before distribution.
13. **MCP agent-to-agent delegation is not automatic.** MCP clients and servers expose tools/resources/prompts. Parent-child task semantics, authorization delegation, budget limits, cancellation, identity and durable reconciliation still require product-defined contracts.
14. **AST repo maps and full tool traces are not automatically safe evidence.** They may expose secrets, personal data, proprietary source, prompt content or command arguments. Evidence collection needs minimization, redaction, access controls, retention and integrity checks.

## 7. Product-specific recommendations

### 7.1 PocketCode

**Do now, in discovery/specification:**
- Keep the first product proof narrow: one deterministic CSV-to-CSV transformation or comparable bounded task, with known input, expected output, timeout, cancellation, report and file handoff.
- Compare manual copy/paste, browser-local Pyodide, and user-owned remote PC only as separate arms of the same task. Do not choose hosted execution or a provider under the current $0 constraint.
- Use Cline's layered separation as a reference: UI/host adapter, agent loop, model/provider adapter, execution adapter, durable coordinator. Do not import its entire runtime.
- Prototype Aider-style repository summaries only if code-editing becomes a demonstrated MVP requirement. The first MVP may not need a repo-wide AST map.
- If testing browser Git, create a disposable workspace and specifically test interrupted writes, reload/crash recovery, `flush`, quota exhaustion, CORS, auth refresh and repository integrity. Do not use LightningFS as trusted evidence storage by default.
- Keep remote SSH as a future user-owned-host adapter with a distinct host identity, explicit trust enrollment, key custody, least privilege, host-side policy enforcement and audit. Tailscale/WireGuard provide transport/networking, not execution authorization or sandboxing.

**Do not do yet:**
- Do not mandate MCP across the application before the first bounded task demonstrates a need for third-party tool interoperability.
- Do not add a general-purpose mobile terminal or unrestricted shell to the MVP.
- Do not claim browser/WASM memory safety from WASM bounds alone.
- Do not implement a remote Linux sandbox until a specific host model and threat model are chosen.
- Do not add a full DevPod dependency to the mobile application.

### 7.2 RevDev

**Do now, while PC unavailable:**
- Continue the publisher/orphan/retry/recovery design and test-acceptance work using exact source pins and existing handoffs. Do not replace the current queue or infer runtime behavior.
- Treat River as a candidate for a later isolated source-level comparison against RevDev's actual queue contract: durable enqueue, atomic claim, lease expiry, retry/backoff, uniqueness/idempotency, cancellation, graceful shutdown, job history, SQLite behavior, Windows support and migration cost.
- Define a small adapter boundary between mission coordinator and storage/queue so a future comparison does not force a rewrite.
- Keep PowerShell 5.1, process-tree termination, file watcher and Windows filesystem semantics in the RevDev adapter and acceptance suite.
- MCP may be evaluated for agent tool connectivity, but do not let it replace RelayRef authorization or the existing task/mission policy boundary.

**When PC access returns:**
- First read-only inventory and exact source/installed/runtime comparison.
- Reproduce and close P0 publisher/orphan/retry/recovery gaps with existing canonical acceptance and PowerShell 5.1 tests.
- Only after that compare River against the observed requirements. Do not introduce a queue migration while current queue/runtime identity is unknown.

## 8. Proposed shared contract and fixture work

The next low-risk convergence artifact should be a schema-and-fixture proposal, not code. Suggested minimal records:

- `TaskEnvelope`: `schema_version`, `task_id`, `created_at`, `objective`, `input_refs`, `constraints`, `allowed_actions`, `denied_actions`, `acceptance_ref`, `non_goals`.
- `WorkStep`: `step_id`, `kind`, `depends_on`, `attempt_policy`, `completion_evidence_required`.
- `ExecutionAttempt`: `attempt_id`, `execution_target_kind`, `target_identity_ref`, `started_at`, `ended_at`, `termination_source`, `exit_code`, `exit_code_provenance`.
- `LifecycleEvent`: `event_id`, `event_source`, `subject_kind`, `subject_id`, `attempt_id`, `source_sequence`, `observed_at`, `payload_digest`, `schema_version`.
- `Outcome`: `execution_outcome` and `job_disposition` as separate axes; PASS/FAIL/INCOMPLETE only where the source is authoritative.
- `EvidenceRef`: `evidence_id`, `kind`, `source`, `captured_at`, `completeness`, `truncation_state`, `digest`, `size`, `retention_ref`.
- `ArtifactRef`: `artifact_id`, `expectedness` (required/optional/not-applicable/unknown), `digest`, `size`, `media_type`, `integrity_state`.
- `ReleaseDecision`: `decision_id`, `artifact_id`, `policy_revision`, `authorized_at`, `authorization_scope`, `revocation_state`.
- `TransferRecord`: `transfer_id`, `release_decision_id`, `started_at`, `bytes_sent`, `completion_state`, `client_receipt_state`.
- `ContinuationCheckpoint`: exact source refs, completed step IDs, current disposition, unresolved questions, next action and evidence references.

These names are illustrative, not frozen. Do not merge the PocketCode D-01..D-08 owner decisions, RevDev OD-01..OD-08, RelayRef rules, AEC/LOOP/CASE, AWC/P8U/P0-D, or other acceptance namespaces. A shared fixture may be reused only when its semantics truly match; product-specific tests must wrap or extend it.

## 9. Proposed architecture layers

```text
                         SHARED CONTRACTS (versioned, language-neutral)
      Task / Step / Identity / Lifecycle vocabulary / Outcome / Evidence / Artifact
                                     |
                     +---------------+----------------+
                     |                                |
              REVDEV ADAPTERS                    POCKETCODE ADAPTERS
        Windows mission coordinator          Mobile product coordinator
        Queue/store implementation           Local journal / remote coordinator
        PowerShell process supervisor        Browser/WASM execution adapter
        Windows watcher + file policy        User-owned SSH / future provider adapter
        Publisher + local result sink        Mobile file/share + future artifact service
        RelayRef / host authorization        Device + host + provider authorization
                     |                                |
            REVDEV ACCEPTANCE                    POCKETCODE ACCEPTANCE
       P8U / P0-D / RelayRef / PS5.1          AEC / LOOP / CASE / lifecycle / mobile
```

The diagram describes separation of responsibilities, not current implemented topology.

## 10. Decision register

| ID | Recommendation | Status |
|---|---|---|
| CONV-01 | Define shared domain-neutral contracts before shared code | Recommended for next spec pass |
| CONV-02 | Keep product coordinators, queue stores and execution adapters separate | Recommended architectural guardrail |
| CONV-03 | Treat MCP as optional tool adapter, not lifecycle authority | Recommended |
| CONV-04 | Evaluate River only against RevDev's real queue contract after PC evidence returns | Deferred, not selected |
| CONV-05 | Run a bounded Aider-style repo-map experiment only when repo-context need is demonstrated | Deferred |
| CONV-06 | Treat isomorphic-git/LightningFS as an experimental workspace option with crash/CORS tests | Deferred |
| CONV-07 | Treat DevPod SSH as a remote-host reference, not a mobile runtime dependency | Deferred |
| CONV-08 | Keep nsjail/bubblewrap confined to a future Linux remote-execution threat model | Deferred |
| CONV-09 | Remove the 9–14 month acceleration claim from planning | Required correction |
| CONV-10 | Await Claude's independent research before finalizing candidate shortlist | Open |

## 11. Source review notes and links

Primary sources consulted in this pass:

- Cline SDK architecture: https://github.com/cline/cline/blob/main/sdk/ARCHITECTURE.md
- River repository: https://github.com/riverqueue/river
- River Go SQLite driver source: https://github.com/riverqueue/river/blob/master/riverdriver/riversqlite/river_sqlite_driver.go (explicit early-testing, concurrency and performance caveats; inspected source blob `7d1044bfc81eaea0923f5aea79904eddaeedf34d`)
- River Go SQLite module: https://github.com/riverqueue/river/blob/master/riverdriver/riversqlite/go.mod (inspected source blob `56626124568d6651f0a619cd8703779122ffc08f`)
- River Go PostgreSQL driver module: https://github.com/riverqueue/river/blob/master/riverdriver/riverpgxv5/go.mod (inspected source blob `0b12271aea219e514ca9c5e4c8c1ed4489a76ddb`)
- MCP TypeScript SDK README: https://github.com/modelcontextprotocol/typescript-sdk/blob/main/README.md (main is v2; v1.x is separate; SDK package supports Node.js, Bun and Deno)
- isomorphic-git README: https://github.com/isomorphic-git/isomorphic-git (browser filesystem and HTTP adapters; LightningFS crash-ordering warning; browser CORS constraints)
- LightningFS README: https://github.com/isomorphic-git/lightning-fs (subset filesystem API backed by browser storage)
- DevPod README: https://github.com/loft-sh/devpod (client-only DevContainer environment manager with provider backends)
- DevPod SSH provider: https://github.com/loft-sh/devpod-provider-ssh
- Aider repository map source: https://github.com/paul-gauthier/aider/blob/main/aider/repomap.py (exact source extraction and dependency analysis still outstanding)
- Pyodide: https://github.com/pyodide/pyodide
- nsjail: https://github.com/google/nsjail
- bubblewrap: https://github.com/containers/bubblewrap

Some direct source-file retrieval attempts did not return usable file content in this pass. Those candidates are marked for further verification rather than treated as fully audited. Repository-level metadata is not a substitute for a pinned release, license-file review, dependency audit, or compatibility test.

## 12. Next actions

1. Wait for Claude's independent three-pass report. Do not restart Gemini's broad candidate search. Reconcile disagreements against primary sources and project requirements.
2. Build a candidate scorecard with columns for exact use case, source file/module, current maintenance, license/version, platform fit, dependency/footprint cost, security boundary, integration effort, measurable benefit, and evidence confidence.
3. Prioritize **one fixed-task experiment** over architecture expansion: validate PocketCode's browser-local path against the manual baseline; no provider or spend.
4. Draft the language-neutral shared contract only after Claude's research is reconciled. Start with TaskEnvelope, Outcome, EvidenceRef and ArtifactRef; include negative fixtures for unknown, partial, truncated, timeout, cancellation, duplicate events and artifact-not-required.
5. Keep RevDev queue selection deferred until PC access and read-only inventory restore exact source/runtime evidence.

## 13. Non-actions and guardrails

This review did not change source code, tests, PR #2 or PR #3; did not create a provider/account, execute a workload, run Actions, spend money, merge, deploy, install software, mutate a queue, or access the unavailable PC. No upstream project is approved for adoption. No acceptance test has passed as a result of this research. The user's $0 budget, phone-only period, HOSTED_DENY and no-unapproved-host-action constraints remain in force.
