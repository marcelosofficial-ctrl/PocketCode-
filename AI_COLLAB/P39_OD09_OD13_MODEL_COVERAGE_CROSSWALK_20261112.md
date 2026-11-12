# P39 OD-09..OD-13 model coverage crosswalk

Date: 2026-11-12  
Status: source-pinned static coverage audit; no implementation or tests executed.  
Authority: `P39_OWNER_DELEGATED_DECISIONS_20261111.md`. This note does not change OD-09..OD-13, LOOP-01..14, CASE-01..16 or D-IDs.

## 1. Exact source pins

Active branch: `pocketcode-ai-workflow-director-research-2026-10-28`.

| File | Blob SHA |
|---|---|
| `scripts/execution_projection.py` | `f32237c8c5ee5d62b0416b3dd867515ce567c21b` |
| `scripts/test_execution_projection.py` | `cbd756cce1bc42a6aab0d5c48d8fac6f56cce7c1` |
| `scripts/result_receipts.py` | `0d1588f8590b57e0bf7447c7d5c519186ff0f39d` |
| `scripts/test_result_receipts.py` | `d1f3546d15a6f5473b9a8eda43ea7a1fee0bca7c` |
| `scripts/event_journal.py` | `371a175739b9cb65cd4d59bb4cd5b3c1c4953564` |
| `scripts/test_event_journal.py` | `333cf5ec856d4244c3f84da9e82bb2fa126607b5` |
| `AI_COLLAB/P39_OWNER_DELEGATED_DECISIONS_20261111.md` | `a72a4351d97f3723f8aac0b1f66cd400532136cb` |

The modules describe themselves as pure/in-memory reference models. The execution projection requires callers to authenticate, authorize, deduplicate, validate policy and persist observations first. Its lifecycle, exit and failure observation types carry `attempt_id` and positive sequence but no canonical `ExecutionId`, `CommandId`, EffectId or tenant field; the helper validates attempt equality but cannot itself establish the full identity chain. The event journal accepts an `AuthenticatedProducer` value supplied by a trusted adapter; it does not verify keys, signatures, certificates, sessions or external credentials.

## 2. Policy-to-model coverage

| Decision | Existing model evidence | Remaining gap / disposition |
|---|---|---|
| **OD-09 required policy/egress barrier** | `project_verdict()` fails closed on missing lifecycle/child evidence, rejects wrapper and embedded exits as child exit, and requires coordinator success + natural child exit 0 for PASS. | Its inputs contain no policy/egress barrier, barrier identity, version or verification result. A zero child exit can therefore project PASS without the helper knowing whether the mandatory barrier exists. Existing tests have no barrier-missing/mismatch case. This is a real integration gap; do not infer OD-09 conformance from child-exit tests. |
| **OD-10 three separate projections** | `VerdictProjection` is execution-only. `ResultReceipt` stores execution_outcome, collection_state, lifecycle_disposition, cleanup_state, evidence references, artifacts and uncertainties. `release_artifact()` independently checks current authorization, latest receipt, artifact membership, integrity and quarantine. | No integrated overall job/evidence disposition combines lifecycle, policy, collection and cleanup; no single authoritative three-projection reducer or provenance chain is implemented. The pieces are separate models and their values are constructor/caller inputs. PASS candidate, overall completeness and artifact release are not yet unified or authenticated. |
| **OD-11 typed coordinator-resolved projection and renderer** | `execution_projection.py` defines typed lifecycle, exit and failure observations with attempt IDs, producer class, kind and sequence; tests cover child/wrapper/signal/embedded distinction, wrong producer and attempt, contradictions and malformed types. | It is not connected to authenticated ingress, durable accepted observations or a production caller. Its observation records do not carry canonical `ExecutionId` (nor the full CommandId/EffectId/tenant scope), and the helper validates only attempt binding plus a positive sequence value; it does not reduce a complete ordered observation stream. `format_report()` still accepts a generic mapping and calls the legacy status/exit-code helper. The formatter can reclassify ambiguous raw inputs and does not consume a sealed coordinator-resolved projection. EventJournal's producer type is model input, not cryptographic authentication. |
| **OD-12 same-attempt termination/cleanup acknowledgement** | Execution projection distinguishes signal termination, wrapper exit and embedded SystemExit/exception. ResultReceipt has a cleanup_state field; tests verify malformed values and receipt version immutability. | No termination request/ack state machine or authoritative controller acknowledgement is represented. `ExitObservation` has no acknowledgement identity/source or explicit ExecutionId; `ResultReceipt.cleanup_state` is supplied as a string and is not proven against an exact DispatchAttemptId + ExecutionId acknowledgement. Tests do not prove controller-confirmed termination. |
| **OD-13 client-confirmed exact artifact receipt** | `ReleaseGrant` records server-side bytes_transferred and transfer_sha256; completion checks full recorded length and stored content digest. `PublicationAttempt` records receipt ID, destination, attempt number, a success-derived disposition, time and optional idempotency key. | `PublicationAttempt` contains receipt ID, destination, attempt number, disposition, observed timestamp and optional idempotency key. `publish_report()` takes a caller-supplied boolean `success` and stores `published`/`failed`; this is not a destination-generated acknowledgement. Neither that record nor `ReleaseGrant` binds an authenticated client acknowledgement to exact ArtifactId, object version, digest and byte range. Transfer progress/completion is the sender/model's own observation; report-publication success is not recipient acknowledgement. No client-observation/client-ack state or receiver identity is modeled. |

## 3. Important distinctions

- `execution_projection.project_verdict()` has useful typed fail-closed semantics but is not an evidence authenticator, policy barrier verifier, durable reducer or overall job/artifact projection.
- `ResultReceiptStore` does preserve immutable receipt revisions and artifact manifests and checks the latest receipt and local bytes at the release boundary. This is meaningful model coverage, but it is a separate in-memory model and not a production release service.
- `ReleaseGrantEvent` and `PublicationAttempt` are local model records. Their sequence/attempt fields do not prove a remote publisher, client or transport acknowledged the exact bytes.
- EventJournal authenticates only by consuming a pre-constructed test/input object. Its own docstring explicitly disclaims key/signature/certificate/session verification.
- Browser worker CANCEL_ACK is separately narrowed in the opaque-origin protocol to acknowledgement of the supervisor invoking terminate() on its exact Worker. It does not establish native child wait status, renderer/OS teardown or exact artifact receipt.

## 4. Minimum future coverage after a separate gate

1. OD-09: missing, stale, wrong-scope and contradictory policy/egress barrier blocks PASS and release; preserve child exit 0 as a raw fact.
2. OD-10: test execution verdict, overall evidence/job disposition and artifact disposition independently and in combination; missing required collection/cleanup/integrity makes overall INCOMPLETE without rewriting raw execution facts.
3. OD-11: authenticated ingress and immutable coordinator reducer; renderer accepts only resolved projection/version and cannot reclassify status from caller-supplied exit metadata.
4. OD-12: termination request, controller action, same-attempt/same-ExecutionId acknowledgement and cleanup confirmation are distinct; missing/wrong/late acknowledgement remains UNKNOWN and blocks release where required.
5. OD-13: separate emitted, client-observed and client-acknowledged states; acknowledgement binds authenticated receiver, ArtifactId, immutable object version, SHA-256 and exact byte range. Retry same receipt/bytes without rerunning execution.

These are future acceptance requirements, not implemented tests. No canonical CASE IDs are created or closed.

## 5. Evidence status

- VERIFIED: source methods, dataclass fields and test names were inspected at the blob pins above.
- INFERRED: these are the remaining model-level proof boundaries for OD-09..OD-13.
- UNKNOWN: authenticated coordinator, policy barrier integration, durable evidence store, termination controller, transport and client acknowledgement.
- NOT RUN: all tests in this audit. No source/test files changed; P39 implementation/adapter gate remains CLOSED.
