# PocketCode — Artifact Release-Time Validation Falsification Checklist

**Status:** Research/test specification only. NOT RUN. No artifact store, API, provider, or runtime selected. Not canonical acceptance; no implementation or deployment authorized.

## Purpose

D-07 defines the evidence needed before PocketCode can safely return output files to a user. A historical execution PASS is not a permanent authorization to download an artifact. Release is a separate decision that must validate the current caller, exact job/attempt/tenant association, quarantine and safety metadata, size/type/path rules, and the exact bytes about to be returned.

## Boundary clarification: no universal artifact gate

The release checks below apply when a concrete artifact exists and a caller requests its release/download. They do **not** require every successful execution to produce an artifact. Artifact-free tasks may have an empty output-file list and still satisfy execution PASS when the applicable execution acceptance criteria are met.

Keep these facts independent:
- **Execution verdict:** derived from trusted terminal evidence and the relevant LOOP/CASE requirements.
- **Artifact state:** whether an expected artifact was produced, is absent, unavailable, partial, or quarantined.
- **Release decision:** whether the exact artifact version is currently authorized and safe to return to this caller.

A historical execution PASS never grants release permission. Conversely, absence of an artifact does not retroactively fail an otherwise valid artifact-free execution. If a particular case explicitly requires a named output, that case-specific requirement controls; do not generalize it into a universal gate.

## Proposed release invariant — owner review required

An artifact may be released only when all applicable checks succeed for the exact immutable artifact version and requesting principal at the release boundary:

1. **Current authorization:** authenticate caller and re-check current authorization immediately before release. Revocation after execution must deny release even if the historical run passed.
2. **Scope binding:** artifact tenant, job, attempt, and manifest identity match the requested authorized result. Never resolve an artifact solely by user-controlled filename or globally guessable ID.
3. **Trusted manifest:** only a trusted coordinator/storage publisher can mark an artifact manifest complete and releasable. Program-produced JSON/metadata cannot grant release permission.
4. **Safe object identity:** use an opaque artifact ID and a storage-controlled object reference. Validate any display name separately. Do not concatenate untrusted names into filesystem paths.
5. **Path and object safety:** reject traversal, absolute paths, device aliases, unexpected symlinks/reparse points, hard-link/path-swap hazards where relevant, and any object outside the designated store. Prefer APIs that open a pre-authorized object handle rather than validate a path then reopen it.
6. **Metadata allowlist:** enforce configured maximum file size/count, allowed media type/extension policy, filename rules, and any archive-specific constraints. Treat content-type supplied by the program as untrusted.
7. **Quarantine and lifecycle:** deny artifacts that are pending, quarantined, incomplete, deleted, expired, or tied to an unresolved required gate. A historical PASS does not override a later quarantine or failed release gate.
8. **Exact-byte integrity:** bind manifest to the immutable object version and cryptographic digest/size; verify the exact stored bytes being released, not only a digest recorded at initial run completion.
9. **Race-resistant release:** avoid time-of-check/time-of-use gaps between authorization/metadata/digest checks and byte return. Use immutable object versions/handles or an equivalent atomic snapshot. If bytes change during verification or streaming, abort and do not report successful download.
10. **Bounded response:** enforce maximum bytes and request/range limits before and during transfer. Do not allow repeated ranges or retries to bypass the total limit. Any partial transfer must be labeled as partial and must not be represented as a completed artifact.
11. **Safe HTTP/client behavior:** set a safe attachment disposition and validated display filename; do not execute HTML/SVG or other active content inline by default. Use appropriate content-type policy and anti-sniffing behavior at the actual HTTP boundary.
12. **Non-disclosing denial:** unauthorized/wrong-tenant callers must not learn other tenants' artifact existence, filename, digest, size, job IDs, or quarantine reason beyond the approved generic response.
13. **Audit and history separation:** record allow/deny reason and exact object version/digest without leaking secrets. A release denial does not rewrite a historical execution PASS; the report should separately show release status.
14. **No implicit repair:** do not silently re-create, substitute, or fetch a “similar” artifact if the requested version is missing, unsafe, or digest-mismatched.

## AR-01..AR-14 — falsification cases

| ID | Setup / fault | Required assertion | Evidence boundary |
|---|---|---|---|
| AR-01 | Historical run PASS; revoke authorization before download | Release denied; no bytes; historical execution verdict remains PASS; release status separately denied | API/storage integration |
| AR-02 | Request artifact from another tenant/job/attempt, including guessed opaque IDs | No bytes and no cross-scope metadata disclosure; result association never silently changes | Authenticated API integration |
| AR-03 | Replace stored bytes after manifest creation but before release; keep old digest | Digest/version mismatch denies release and quarantines or flags the object; zero unverified bytes returned | Immutable store / final-byte integration |
| AR-04 | Swap path/object between validation and open; use symlink/reparse point or traversal-style name | No access outside controlled store; use a stable object handle/version; unsafe object is denied | Filesystem/object-store integration on target platform |
| AR-05 | Manifest is absent, incomplete, malformed, untrusted, or disagrees with stored metadata | Deny release; do not infer trust from program output or file existence alone | Coordinator + store integration |
| AR-06 | Artifact is quarantined, pending, deleted, expired, or run has unresolved required gate | Deny release despite historical PASS; record independent release status | State/store integration |
| AR-07 | Oversized object, excessive artifact count, disallowed media type, extension/type mismatch, or malformed filename | Deny or safely transform only under an explicit approved rule; enforce size/count before unbounded read | API/storage integration |
| AR-08 | Content claims text but contains active HTML/SVG/script or a mismatched binary type | Never serve active content inline by default; enforce actual configured type policy; no trusting program-supplied MIME metadata | HTTP boundary integration |
| AR-09 | Digest matches metadata initially but bytes change while being streamed or object version changes | Abort/deny completion; never claim full successful verified download; ensure the delivered bytes match the verified immutable version | Storage/streaming integration |
| AR-10 | Request uses range requests, repeated retries, or many parallel downloads to exceed aggregate cap | Enforce per-object and request/session bounds; partial ranges are explicit and cannot bypass limits | API/stream integration |
| AR-11 | Unauthorized user asks for nonexistent ID, existing other-tenant ID, and quarantined other-tenant ID | Responses do not disclose existence or distinct sensitive metadata across those cases | Authenticated API side-channel review/test |
| AR-12 | User-controlled filename includes traversal, separators, reserved device names, control characters, Unicode confusables or misleading extension | Storage identity remains opaque; display name is normalized/allowlisted; no path is derived from the name | Pure validation + target-platform integration |
| AR-13 | Authorization revoked between initial request check and final byte return | Release boundary rechecks or uses a documented authorization snapshot/lease semantics; if revocation should apply immediately, zero bytes after revocation | Concurrency integration |
| AR-14 | Two concurrent release requests race with quarantine, object deletion, or replacement | Every returned byte stream is bound to an authorized immutable object version; unsafe transition denies or terminates release; no stale manifest bypass | Storage concurrency integration |

## Required release decision record

Illustrative fields, not a frozen public schema:

- authenticated principal/tenant and authorization decision/version;
- artifact opaque ID, manifest ID/version, job ID and attempt ID;
- current lifecycle/quarantine state and required-gate status;
- immutable storage object/version reference;
- expected digest, expected size, and actual verified digest/size;
- allowed media type and validated display filename;
- release decision, timestamp/sequence, and bounded reason code;
- whether transfer completed, was partial, or was aborted.

Do not put secret-bearing output or sensitive raw filesystem paths into audit logs. Keep raw storage location internal and bounded.

## Required implementation choices before integration testing

- Is the store filesystem-backed or object-store-backed? What immutable version/conditional read primitive does it provide?
- How are bytes hashed and size-checked without unbounded buffering?
- Is the digest computed at trusted publication and rechecked against the exact version read for release?
- What is the policy for symlinks/reparse points, hard links, archives, active content, and platform-specific names?
- What are maximum object size, object count, range count, transfer time, and retry budgets?
- What is the authorization revocation consistency contract during a long transfer?
- How are quarantine, deletion, retention expiry, and manifest publication ordered atomically?
- What does the client show when a transfer is denied, aborted, or partial? How is a retry bound to the same immutable version?

If the chosen store/API cannot answer these questions, the corresponding guarantee remains BLOCKED/UNKNOWN.

## Stop conditions

Do not claim artifact-release safety if:

- Authorization is checked only when execution completes.
- A PASS report itself grants download permission.
- Caller-provided path/name is used as the storage identity.
- Metadata is validated, then a mutable path is reopened without a race-resistant binding.
- The digest describes earlier bytes rather than the exact object version returned.
- Artifact ownership is inferred from filename or user-supplied JSON.
- Quarantine or changed authorization is ignored for historical PASS artifacts.
- The system streams unbounded bytes before checking size.
- A partial or aborted transfer is displayed as a complete download.
- Denials leak another tenant's artifact existence or metadata.
- A fake/in-memory test is described as proof of real storage/HTTP behavior.

## Evidence ladder

- **PURE/UNIT TESTED:** name/metadata validation and release predicate only.
- **FAKE-ADAPTER TESTED:** coordinator projection and denial branches under synthetic storage faults.
- **STORE INTEGRATION TESTED:** immutable object versions, digest/size checks, atomic publication, quarantine and concurrent mutation behavior.
- **API/HTTP INTEGRATION TESTED:** authorization, tenant scoping, safe response headers, streaming/range limits, non-disclosure, revocation races.
- **DEVICE ACCEPTED:** phone can distinguish available, denied, quarantined, partial, aborted and completed downloads.

Lower evidence levels do not substitute for the actual storage or HTTP boundary.

## Traceability

- D-07 in `AI_COLLAB/OWNER_DECISION_REGISTER_20261029.md`.
- COORD-09; FAKE-13/14/17 in existing coordinator/envelope plans.
- LOOP-10/11/12; CASE-08/14/15.
- Related helper/source review: FLA-13 covers portable input-name validation; it is not by itself a complete artifact-release audit.

**Current result:** SPECIFIED ONLY / NOT RUN. No implementation, store, provider, account, billing, workload, merge, or deployment action was performed.


## Cross-decision audit pointer — 2026-10-29
See [CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md](CROSS_DECISION_CONTRADICTION_AUDIT_AND_IMPLEMENTATION_GATES_20261029.md) for cross-boundary invariants, unresolved interface questions, and the proposed G0-G7 evidence gate sequence. This pointer does not close owner decisions or promote specification/fake-test evidence to provider, persistence, HTTP, or device integration evidence.
