# Provider-neutral recipe and durable task manifest proposal

**Date:** 2026-11-05  
**Status:** Architecture proposal only. Not a frozen schema, implementation, runtime selection, provider selection, or amendment to canonical acceptance.  
**Authority:** `PRODUCT/EXECUTION_LOOP_ACCEPTANCE.md`, existing LOOP-01..14 and CASE-01..16, the owner decision register, and the execution-boundary/security documents remain authoritative.

## Executive decision

Adopt a small, versioned *recipe manifest* as the declarative plan for bounded work, and a separate immutable *run record* as the identity of one requested execution. Do not make a chat transcript, provider session, MCP task handle, workflow framework run ID, or mobile notification the product's source of truth.

A manifest describes what may be done. A run records what was actually requested. An attempt records one execution try. A step attempt records one bounded operation try. Evidence records what an authoritative observer actually observed. A derived report projects those facts into user-facing status.

This is a provider-neutral contract proposal. It does not select a runner, sandbox, backend, workflow engine, AI provider, or mobile framework.

## Why this is the right next abstraction

PocketCode's product thesis is not simply "run code on a phone" or "chat with an AI agent". Existing tools already offer local interpreters, remote coding sessions, agent task queues, progress, and cross-device continuation. The differentiator we can still pursue is a user-visible, durable chain from intent to exact attempt, observed execution, retained evidence, recovery, and approved correction.

A recipe makes a multi-pass task bounded and inspectable before execution. A durable run record lets the task inbox survive app closure, device changes, provider loss, and interrupted observation. Step-level evidence prevents an AI summary from becoming its own proof.

## Open-source source review and concrete reuse decisions

The following source-level observations informed this proposal. Blob hashes identify the exact files inspected; repository commit IDs pin the reviewed tree where available.

| Project and reviewed source | Observed implementation detail | Decision |
|---|---|---|
| LangGraph checkpoint base, `libs/checkpoint/README.md`, blob `a3e702b1ff81a6684c2ee8808fef3b1a5e84ade6`, tree `302a4d4caf7fa90d78efa4e9f0636a6d72d24ac8` | Separates a thread ID from a particular checkpoint ID. Stores pending writes from successful sibling nodes when another node fails, so resume need not rerun completed nodes. | Adopt the identity distinction and completed-step preservation as design invariants. Do not adopt LangGraph as the task model or assume its state is an execution receipt. |
| LangGraph Postgres saver, `libs/checkpoint-postgres/langgraph/checkpoint/postgres/__init__.py`, blob `d1e3cac5978766992fc30b12cecd3bae6765d824` | Checkpoints have explicit persistence APIs and migration/setup lifecycle; persistence is a configured storage responsibility, not an in-memory promise. | Treat persistence capability and durability as adapter facts that must be declared and tested. No Postgres dependency is selected. |
| LangGraph checkpoint serializer guidance, same checkpoint README | Default serializer permits broad Python type deserialization unless strict mode or an explicit allowlist is configured. | Security warning: never deserialize untrusted task/checkpoint data into arbitrary runtime types. Use a strict, versioned data-only schema and explicit type allowlists. |
| Hatchet Python task summary, `sdks/python/hatchet_sdk/clients/rest/models/v1_task_summary.py`, blob `d3b1655c6efd22d30788b13235e5f887d3695a56`, reviewed tree `806c6055edf0969cee16fd35c2c70f307703dbdc` | Task projections expose external task ID, attempt, retry count, idempotency key, parent task, workflow version, status, start/finish, output, error, and eviction state. | Adopt these as useful projection dimensions, not as one overloaded ID or as proof that output is trustworthy. Preserve task/run/attempt/step identities separately. |
| Hatchet Python workflow configuration, `sdks/python/hatchet_sdk/runnables/workflow.py`, blob `fd4427e1e0b67755348a77cc0f6e9d58b996fff4` | Workflow configuration resolves execution timeout, schedule timeout, retries and backoff from explicit task defaults. | Adopt explicit, resolved per-run budgets. A recipe default must be materialized into the run record so a later recipe edit cannot silently change an active run. |
| Temporal Python workflow context, `temporalio/workflow/_context.py`, blob `a33759c37a48317714529f0c2df73d2672b560db`, reviewed tree `1845f25aeac33114b9c46fbccfac19976129f796` | Workflow identity and attempt metadata are explicit; the context includes workflow ID, run ID, attempt, retry policy and timeout information. | Adopt distinct stable workflow/run identity and attempt metadata. Do not copy Temporal's deterministic workflow runtime or server requirement. |

### Existing copied code

PocketCode already has isolated, research-only copies of small upstream helpers: OpenHands atomic text writer, Mini-Coding-Agent workspace path guard, and MCP Tasks poll-interval helper. Their isolated tests do not validate product integration. No additional code is copied in this pass: the new findings are primarily data-contract and lifecycle semantics, and copying framework internals before selecting a runtime would create an unowned dependency.

## Proposed conceptual model

These records are logically distinct even if a future storage adapter places them in related tables or files.

1. **Recipe definition**: immutable ID plus version; declares a bounded, typed plan.
2. **Run request**: immutable run ID; pins the exact recipe version, normalized input, policy version, and resolved budgets.
3. **Attempt**: immutable attempt ID and monotonic attempt number; represents one actual execution try of the run.
4. **Step definition**: stable step ID within the recipe version; declares dependencies, permissions, budget and expected evidence.
5. **Step attempt**: unique ID for one execution of one step within one attempt; retry never overwrites earlier evidence.
6. **Approval**: a narrowly scoped authorization record bound to one exact operation.
7. **Evidence receipt**: append-only observation with source, time, integrity metadata and association to the exact run/attempt/step.
8. **Derived report**: versioned projection of the evidence. It is not itself primary evidence and cannot self-verify.

### Identity rules

- `recipe_id` identifies the logical recipe; `recipe_version` identifies immutable content.
- `run_id` identifies one requested run and never changes when the UI reconnects.
- `attempt_id` identifies one execution attempt. Retrying creates a new attempt or step-attempt identity; it does not rewrite a prior one.
- `step_id` is stable within a recipe version; `step_attempt_id` identifies the actual try.
- Provider task IDs, MCP task handles, remote job IDs and process IDs are adapter references, never replacements for product IDs.
- A resume operation resumes observation or continues from a verified checkpoint. It must not silently submit the original side-effecting request again.
- All externally supplied IDs and references are untrusted until bound to the expected tenant, endpoint, protocol generation, run, operation and policy.

## Proposed recipe manifest fields

This is a conceptual schema, not frozen JSON.

| Section | Required meaning |
|---|---|
| Identity | Stable recipe ID, immutable version, schema version, human title, purpose and provenance |
| Inputs | Typed fields, required/optional, bounds, enumerations, safe defaults, normalization rules, secret classification and validation errors |
| Steps | Stable step IDs, explicit dependencies, declared action/tool, bounded input/output schema, expected evidence, timeout and retry policy |
| Permissions | Per-step read/write/network/process/artifact scopes; explicit allow/ask/deny; default deny |
| Approval | Whether human approval is required, exact target, operation ID, canonical argument digest, policy version and expiry |
| Budgets | Maximum passes, steps, wall time, output bytes, artifact bytes, concurrency and provider/compute budget (default zero unless separately authorized) |
| Parallelism | Explicit safety class and declared resource keys; no implicit parallel execution |
| Recovery | Checkpoint boundary, resumability class, idempotency semantics, reconciliation method and whether re-execution is forbidden |
| Outputs | Typed result schema, required evidence sources, artifact policy, retention/deletion behavior |
| Acceptance mapping | References to existing canonical LOOP/CASE requirements, without defining or renumbering acceptance cases |

The run record must store the *resolved* values of defaults and budgets plus the exact manifest digest. Future recipe changes cannot mutate an in-flight run's meaning.

## Step dependency and parallel-safety model

A recipe is a directed acyclic graph. Reject unknown dependencies, cycles, duplicate step IDs, unbounded fan-out, excessive depth, unknown permission names, invalid schemas, and unsupported action types before execution.

Every step must declare one safety class:

- **READ_ONLY**: no mutation to workspace, remote state, user data or external systems. Can be parallel only when resource scopes are disjoint and concurrency is within budget.
- **MUTATING_IDEMPOTENT**: changes state but has a documented idempotency key and reconciliation path. Serialize by default. Parallel only with proven isolation and distinct resource keys.
- **MUTATING_NON_IDEMPOTENT**: side effect cannot safely be repeated. Require exact approval when policy says so, serialize, and never automatically retry after an ambiguous outcome.
- **EXTERNAL_OR_UNKNOWN**: permission or effect cannot be proven. Deny by default or require a higher-level explicit approval; never treat as read-only.

A read-only label is a declared claim until the adapter enforces and tests it. A step cannot mark itself read-only based on generated text.

## Approval binding

Approval is a capability for one operation, not blanket consent for a task or session. Bind it to:

- tenant/user and run ID;
- attempt ID and step-attempt ID where applicable;
- exact operation ID and target resource;
- canonical argument digest and schema version;
- permission/policy version;
- expiry and one-time or bounded-use semantics.

Any changed target, argument, policy, attempt, or expired approval invalidates it. Approval of a plan does not authorize later tool calls that were not in that plan. Rejection is a terminal fact for that operation and must not be retried under a different identity without a new approval.

## Lifecycle and verdict separation

Do not collapse these axes into a single status.

**Run/attempt lifecycle:** CREATED, VALIDATING, READY, WAITING_FOR_APPROVAL, QUEUED, RUNNING, PAUSED, SUCCEEDED, PROGRAM_FAILED, TIMED_OUT, CANCEL_REQUESTED, CANCELLED, REJECTED, INFRASTRUCTURE_FAILED, INTERRUPTED, UNKNOWN.

**Step-attempt lifecycle:** BLOCKED, READY, RUNNING, SUCCEEDED, FAILED, TIMED_OUT, CANCELLED, SKIPPED_BY_POLICY, INTERRUPTED, UNKNOWN.

**Observation quality:** CONSISTENT, MISSING, CONTRADICTORY, STALE, UNTRUSTED.

**Cleanup:** PENDING, CONFIRMED, FAILED, UNKNOWN.

**Artifact release:** QUARANTINED, ELIGIBLE, RELEASED, REVOKED, UNKNOWN.

These are proposed vocabulary labels, not a replacement for canonical LOOP/CASE semantics. A provider reporting "completed" is not enough to claim the user program succeeded. An interrupted or unknown execution must not be reported as PASS. Cleanup and artifact release remain independent gates. Preserve the canonical CASE-04 trusted-timeout result as INCOMPLETE / timed_out.

## Evidence and recovery rules

- Record immutable evidence at the observation boundary: source, adapter version, event ID/sequence, observed timestamp, run/attempt/step identity, payload length, digest, and trust classification.
- Preserve stdout and stderr separately; truncation and byte limits are explicit evidence, not silently discarded.
- Store exact source bytes or a stable content-addressed reference where possible. A parsed summary or canonicalized projection is a separate artifact from the original bytes.
- Persist the run/attempt/step reference and exact prepared request before detaching a UI or dispatching a remote request.
- Acknowledge only the exact operation ID and payload digest that was sent. A late acknowledgement cannot clear a newer pending mutation.
- Checkpoint completed step results independently. If one sibling fails, resume must preserve already verified successful siblings. This is a checkpoint optimization, not proof that the underlying side effect is idempotent.
- On ambiguous mutation outcome, reconcile target state before deciding whether a retry is safe. Never blindly replay non-idempotent actions.
- A generated agent summary cannot be the sole evidence source for its own claimed success. Evidence must come from the runner, filesystem, process supervisor, transport read-back, or other independently specified observer.
- Deletion and retention must distinguish user-visible report removal from immutable audit/evidence retention and legal/security obligations. Do not assume one global retention period.

## Provider-neutral illustrative manifest

The following illustrates the intended shape only. It is not a production schema and must not be parsed as trusted executable instructions.

```yaml
schema_version: 1
recipe:
  id: pocketcode.python-task
  version: 1
  title: Run and verify a bounded Python task
  inputs:
    source:
      type: text
      max_bytes: 65536
      required: true
    expected:
      type: json
      required: false
  budgets:
    max_passes: 2
    max_steps: 5
    wall_time_seconds: 30
    output_bytes: 262144
    artifact_bytes: 1048576
    max_parallel_steps: 1
    provider_budget: 0
  steps:
    - id: validate-input
      action: source.validate
      safety: READ_ONLY
      depends_on: []
      evidence: [validation_receipt]
    - id: execute
      action: runner.execute
      safety: MUTATING_NON_IDEMPOTENT
      depends_on: [validate-input]
      approval: required_by_policy
      evidence: [child_lifecycle, stdout, stderr, exit_observation]
    - id: verify
      action: result.verify
      safety: READ_ONLY
      depends_on: [execute]
      evidence: [verification_receipt]
  outputs:
    required: [verdict, evidence_receipt]
```

The action names above are illustrative capability identifiers. The manifest does not grant those capabilities; the selected adapter and policy must independently enforce them.

## Acceptance traceability without changing canonical IDs

This proposal adds no test IDs and changes no acceptance text. It provides a future implementation mapping to be completed against the exact canonical case descriptions.

| Existing suite | Manifest/lifecycle concern to trace |
|---|---|
| LOOP-01..14 | End-to-end loop semantics: task creation, bounded execution, continuation, interruption/recovery, user approval, result publication and report correctness, using the exact existing case definitions |
| CASE-01..16 | Execution evidence and report semantics: trusted lifecycle, child-exit provenance, timeout/cancellation/rejection, contradictory or missing evidence, cleanup, artifacts and identity, using the exact existing case definitions |
| D-01..D-08 | Remain owner-open. This proposal does not close or supersede any decision. |

Before implementation, create a row-by-row traceability table quoting the exact canonical requirement and identifying the manifest field, enforcement boundary, evidence source, and test layer. Do not infer individual case meanings from the numeric IDs alone.

## Required test layers before product adoption

1. **Schema/pure tests:** invalid IDs, versions, input types, duplicate fields, cycle detection, dependency validation, budget resolution, policy default-deny, approval digest mismatch, expiry and strict boolean/type handling.
2. **Deterministic state-machine tests:** duplicate events, stale sequence, contradictory terminal facts, interrupted step, resume from checkpoint, successful sibling preservation, retry identity and attempt history.
3. **Persistence/transaction tests:** crash between write and dispatch, crash after remote acceptance but before acknowledgement, late acknowledgement after newer operation, corrupted or unsupported schema version, concurrent claims.
4. **Adapter tests:** endpoint/protocol/task ID mismatch, cancellation capability absent, polling hints malformed, child vs wrapper exit, process still alive after cancellation, stdout/stderr overflow and cleanup unknown.
5. **Host/product tests:** exact iOS/Android process lifecycle, app suspension, filesystem/document-provider behavior, actual runner containment and network policy. These remain NOT RUN until the host exists and is authorized.

## Non-goals and rejection list

- No mandatory LangGraph, Hatchet, Temporal, MCP Tasks, Goose, OpenHands, or provider SDK.
- No arbitrary Python object deserialization from a task record or checkpoint.
- No agent-defined permissions or self-approved tool calls.
- No implicit parallelism for shared workspaces or external mutations.
- No "exactly once" claim based only on an idempotency key, queue status, task ID or matching hash.
- No conflation of a task session, run, attempt, process, remote task handle and evidence receipt.
- No automatic retry of an ambiguous non-idempotent action.
- No acceptance-suite renumbering or weakening.

## Proposed next sequence

1. Ask Claude to review the identity model, lifecycle separation and recovery semantics for omissions or over-specification.
2. Ask Gemini to attack the permission, approval, serialization, parallelism and evidence trust boundaries.
3. Reconcile both reviews against canonical LOOP/CASE and D-01..D-08 without changing them.
4. Only after owner review, decide whether this contract should become a schema specification and whether a small existing library can implement a bounded piece.
5. Select a runtime/host only after the product's $0 constraint, iOS/Android lifecycle, execution boundary and security evidence are supportable.
