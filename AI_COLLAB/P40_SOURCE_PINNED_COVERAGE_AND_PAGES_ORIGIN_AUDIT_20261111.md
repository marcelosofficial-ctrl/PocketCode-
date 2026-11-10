# P40 source-pinned coverage and Pages origin audit

**Date:** 2026-11-11  
**Target:** `marcelosofficial-ctrl/PocketCode-`  
**Branch:** `pocketcode-ai-workflow-director-research-2026-10-28`  
**Audited HEAD:** `3545c1e15da6041906bf9cf886c9acdd0a5e7e07`  
**Status:** STATIC SOURCE AUDIT / RESEARCH COMPLETE / NO IMPLEMENTATION  
**Authority:** P39 consensus matrix, OD-01..OD-13 owner register, D-006, canonical LOOP-01..14 and CASE-01..16. No canonical ID or owner decision is changed.

## 1. Ranked gaps

1. **Grant-event consumer trust and aggregate parity (BLOCKING):** first-delivery consumer trusts a supplied digest, and progress increments the aggregate version without a corresponding event/outbox record.
2. **Relay ownership and fencing (HIGH):** the effect-dispatch fake outbox has worker leases and fencing, but the separate release-grant event relay has no relay claim/fence and its delivered marker is an unguarded update.
3. **Revocation and receipt boundary (HIGH):** the receipt store rechecks caller-supplied authorization snapshots, while the grant model does not revalidate current policy on worker claim; neither proves active-transfer cancellation or client receipt.
4. **Pages deployment freshness (HIGH):** the last successful Pages workflow deploy is tied to an older main commit, and the active branch does not trigger the automatic deploy.
5. **Shared-origin storage trust (HIGH):** a second public Pages project, `portfolio`, is configured on the same account host as PocketCode. Different repository paths do not isolate browser origin storage or script privileges.

## 2. Exact source and test pins

All pins below were read from the active branch tree at the audited HEAD.

| File | Blob SHA | What it actually models |
|---|---|---|
| `scripts/release_grant_conformance.py` | `f9107fe46d60bbb5cd7115daf2513cd751221986` | In-memory receipt-head CAS, grant reservation, grant event/outbox, worker lease and event consumer |
| `scripts/test_release_grant_conformance.py` | `e3bbe94838807a1f9214042af262a2497c057fd7` | Reservation, receipt CAS, worker claim/progress, event duplicate/gap and injected pre-commit failures |
| `scripts/fake_outbox.py` | `813957e5061d40cba2ebb5e2936edcbac645820b` | Effect dispatch reservation, send intent, worker lease/fence and provider reconciliation |
| `scripts/test_fake_outbox.py` | `67951a77f87e9523c9080970068fd158680f23a9` | Effect dispatch recovery, stale worker fencing, ambiguous send and idempotent receiver |
| `scripts/event_journal.py` | `371a175739b9cb65cd4d59bb4cd5b3c1c4953564` | In-memory append-only event evidence, payload digest, duplicate/conflict quarantine and local fence checks |
| `scripts/test_event_journal.py` | `333cf5ec856d4244c3f84da9e82bb2fa126607b5` | Source/audience allow-list, duplicate identity, fence and quarantine cases |
| `scripts/execution_projection.py` | `f32237c8c5ee5d62b0416b3dd867515ce567c21b` | Pure typed verdict projection for coordinator lifecycle, child wait and trusted runtime observations |
| `scripts/test_execution_projection.py` | `cbd756cce1bc42a6aab0d5c48d8fac6f56cce7c1` | Projection precedence, contradictory evidence and malformed typed observations |
| `scripts/result_receipts.py` | `0d1588f8590b57e0bf7447c7d5c519186ff0f39d` | In-memory artifact/receipt revisions and synchronous release checks |
| `scripts/test_result_receipts.py` | `d1f3546d15a6f5473b9a8eda43ea7a1fee0bca7c` | Artifact digest, receipt revisions, authorization snapshot, latest receipt and release behavior |

## 3. Source-level findings and corrected coverage

### 3.1 Release-grant aggregate and event consumer

**VERIFIED:** `reserve()` stages a grant, v1 event and outbox item, then exposes all three at one in-memory commit point. Its injected `after_grant`, `after_event` and `before_commit` failures leave all three collections unchanged. `test_crash_after_staged_grant_leaves_no_partial_state`, `test_crash_after_staged_event_leaves_no_partial_state`, `test_crash_before_commit_leaves_no_partial_state` and `test_successful_commit_lost_response_replays_original_grant` cover this sequential model behavior.

**VERIFIED:** `record_progress()` increments `aggregate_version` on every accepted call, including an equal `progress_bytes` value, and updates the grant to `transferring`. It does not append a matching grant event or outbox item. This conflicts with the intended no-op/version/event parity contract in the existing P39 consensus. The current test `test_progress_is_monotonic_and_bounded_by_pinned_object_length` checks decrease and upper bound, but not equal-progress replay or event/outbox parity.

**VERIFIED:** `consume_event()` accepts the next event version after checking only duplicate identity/digest and version gap. On first delivery it does not recompute the digest from canonical semantic bytes, verify that the grant exists, validate the event source against the expected source, or prove the event's producer. The `GrantEvent` contains a digest but not the canonical payload bytes needed for recomputation. Existing tests prove duplicate handling, changed digest for an already-seen identity and gap deferral. They do not prove first-delivery authenticity or envelope integrity.

**Correction:** P39-EVENT-05/06 remain BLOCKING. Do not describe the existing event consumer as authenticating a producer or validating canonical payload integrity. A forged first-delivery test cannot be made meaningful without a specified canonical envelope and trusted ingress boundary. That is a contract/design dependency, not a test-only patch.

### 3.2 Two outboxes, two different guarantees

**VERIFIED:** `FakeOutboxStore` is an effect-dispatch model. It has a lease owner, expiry and increasing fence; `mark_dispatching()` requires the current lease; expiry before send is reclaimable; expiry after send intent requires reconciliation; provider acceptance is not repeated merely because an acknowledgement was lost. Its tests include `test_stale_worker_is_fenced_after_reclaim`, `test_crash_after_dispatch_intent_requires_reconciliation`, `test_lost_ack_found_reconciles_without_second_dispatch` and `test_final_exact_absence_allows_same_attempt_retry`.

**VERIFIED:** the grant-event outbox in `ReleaseGrantContractModel` is separate. The model has `mark_outbox_delivered(source, event_id)`, which flips a boolean after checking only that the item exists. It has no relay claim, lease, relay fence, predecessor-order cursor or stale relay acknowledgement check. The worker lease in that model protects grant transfer progress, not grant-event publication.

**Correction:** never use FakeOutbox's lease/fence tests as evidence that the grant-event relay is fenced. P39-OUTBOX-04/05 must be split by responsibility. Effect-dispatch recovery is covered by `test_fake_outbox.py`; grant-event relay takeover is currently NOT IMPLEMENTED / NOT TESTABLE in the current model.

### 3.3 Journal producer identity is an adapter assertion

**VERIFIED:** `EventJournal.append()` recomputes SHA-256 from immutable payload bytes and checks source, audience, producer identity fields, duplicate identity, event scope and the current in-memory fence. `AuthenticatedProducer` is a typed object accepted by the model; `_validate_producer()` does not verify a credential or signature. The module's own contract places adapter verification before the append call.

**Correction:** journal tests establish fail-closed behavior for supplied producer metadata, not cryptographic producer authentication, persistent fence continuity or atomic database check-and-append. Keep producer authentication and atomic fencing as adapter obligations.

### 3.4 Receipt and execution projection boundaries

**VERIFIED:** `ResultReceiptStore.release_artifact()` checks a supplied `ReleaseAuthorization` snapshot on each call, including attempt, receipt revision, artifact membership and authorization flags. Its tests explicitly include `test_release_rechecks_authorization_on_each_request` and `test_release_authorization_is_a_caller_supplied_snapshot`. It does not authenticate or fetch a policy authority, and its documented release operation is synchronous, not an in-flight stream.

**VERIFIED:** `ReleaseGrantContractModel.claim_worker()` checks grant state and worker lease, but does not fetch a fresh policy decision or revalidate a policy epoch. A successful reservation's stored authorization provenance remains immutable. Thus post-reservation revocation-before-claim is not established by this model.

**VERIFIED:** `project_verdict()` accepts typed lifecycle, exit and program-failure observations and is explicitly a pure projection helper. It does not model Worker error/messageerror, a guest-accessible message channel, cancellation acknowledgement, cleanup, output-stream closure, OPFS readback or IndexedDB receipt commit. The receipt store can record collection/lifecycle/cleanup fields, but that does not prove the referenced observations were authentic or that storage is durable.

**Correction:** keep P39/EP/PYO model assertions separate from browser, adapter and device acceptance. Do not report an EP projection test as a worker lifecycle test, and do not report a receipt-store test as IndexedDB/OPFS durability.

## 4. Corrected P40 execution boundary

The revised `P40_MODEL_ONLY_EXECUTION_PROTOCOL_20261110.md` now distinguishes six lanes:

1. **Release-grant model:** reservation atomicity, idempotency, receipt-head CAS and worker progress. Add equal-progress/no-op and event parity assertions only after the gate opens; the current implementation is expected to fail the intended parity contract.
2. **Grant-event consumer:** duplicate and gap behavior can be checked in the existing model. First-delivery authentication, digest recomputation and tenant/grant binding remain BLOCKED until canonical envelope and ingress authority are specified.
3. **Effect-dispatch fake outbox:** test its existing lease, fencing, send-intent and reconciliation semantics without attributing those guarantees to grant-event publication.
4. **Event journal:** test byte digest, append-only conflict quarantine and local fence behavior. Authentication and durable atomicity remain adapter acceptance.
5. **Receipt store:** test immutable artifact/receipt identity, revision chains and supplied-snapshot release decisions. No stream cancellation, external policy lookup or browser storage claims.
6. **Execution projection:** test only typed lifecycle/child-exit projection and contradictory evidence. Worker lifecycle, cleanup, output and receipt ordering remain separate future adapter/device tests.

No current model-only run is authorized while P39/P40 is CLOSED. Do not create new canonical LOOP/CASE/D IDs or reuse existing PYO-CTRL IDs for a different threat. The detailed test sequence and stop conditions are in the revised protocol.

## 5. Pages deployment: exact workflow evidence

**VERIFIED:** current repository metadata reports Pages enabled. The active branch and `main` both contain `.github/workflows/preview-prototype.yml`. It automatically deploys only on pushes to `main` when `prototypes/mobile-runner/index.html` or the workflow file changes. It also supports manual `workflow_dispatch`. The workflow uploads `prototypes/mobile-runner` as the site root.

**VERIFIED:** the latest Pages workflow run in the repository's 75-run Actions listing was run `39433670146`, completed successfully on 2026-10-20 at commit `90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c`. Its job log confirms:
- checkout SHA `90cc378df1f7c7f1b5f5535c322eddcfbfb9b26c`;
- six static prototype-checker unit tests passed;
- static source checker passed;
- Pages artifact upload succeeded;
- `actions/deploy-pages@v4` reported success;
- environment URL output: `https://marcelosofficial-ctrl.github.io/PocketCode-/`.

**VERIFIED:** `main` is now at `03e65ef35d8b22cb4337ac7097b2a31247c3721e`, later than the last Pages workflow deploy. The active research branch is at `3545c1e15da6041906bf9cf886c9acdd0a5e7e07`. Neither later docs-only branch activity nor an active-branch push triggers the automatic Pages deploy under the current workflow path/branch filter.

**UNKNOWN:** whether an out-of-band Pages deployment occurred after that workflow run; current live response headers, redirects, HTML/meta CSP and repository Pages settings. A direct browser open of the exact logged URL was not accessible to the available browser tool. The workflow log is authoritative for the successful deployment at that time, not a live-origin/header probe today.

**Correction:** replace the old generic statement “Pages workflow deploys the prototype” with “last verified workflow deployment used main SHA 90cc378 on 2026-10-20; automatic deploy is main/path filtered.” Do not claim current live content equals that artifact without a fresh Pages deployment/settings/live response check.

## 6. Shared-origin implications for local storage

**VERIFIED:** GitHub's public Pages docs describe the default user/organization site as `https://<owner>.github.io` and a project site as `https://<owner>.github.io/<repositoryname>`. GitHub also documents that a user/organization custom domain can apply by default to all project sites owned by that account.

**VERIFIED:** the owner repository listing returned 21 repositories, 11 public. Repository metadata checks found exactly two public repositories with Pages enabled: `PocketCode-` and `portfolio`. The `portfolio` repository reports homepage `https://marcelosofficial-ctrl.github.io/portfolio/`; the last verified PocketCode Pages workflow log reports `https://marcelosofficial-ctrl.github.io/PocketCode-/`.

**VERIFIED:** the two URLs share scheme, host and port; only the path differs. The browser same-origin tuple is scheme, host and port. Path is not part of the origin. MDN explicitly gives two different paths on the same host as same-origin. OWASP states that localStorage has no path-level isolation, that multiple apps on one origin share the same localStorage object, and that IndexedDB is origin-scoped and should not be treated as confidential. OWASP's Micro-Frontend Security guidance says separate repositories do not create browser security boundaries and recommends a dedicated origin for a less-trusted feature.

**VERIFIED:** GitHub repository code search returned no matches for `localStorage`, `indexedDB`, `navigator.serviceWorker`, `navigator.locks` or `postMessage` in the portfolio repository. This is only a bounded search result, not proof that generated dependencies, inline scripts, built output or unindexed files never use those APIs. The portfolio's large `src/pages/index.astro` was not opened whole.

**INFERRED:** a script executing on either project site has same-origin browser privileges for the shared host. A compromised or XSS-affected portfolio page could therefore access PocketCode origin storage if such data exists there. No malicious behavior or exploit was observed.

**Immediate zero-spend rule:** treat both Pages projects as one browser trust domain until an owner-approved origin boundary exists. Do not store session identifiers, credentials, provider tokens or other secrets in localStorage or IndexedDB. Treat persisted browser data as untrusted on read. Namespacing keys by repository or path is hygiene, not a security boundary. No hosting/domain migration is selected or authorized.

## 7. New research, maintenance and licence review

| Source | Freshness/maintenance evidence opened | Licence / legitimate reuse |
|---|---|---|
| [GitHub Pages: What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages) | Official GitHub documentation; opened 2026-11-11 | Documentation reference; no code copied |
| [GitHub Pages: custom domains across repositories](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/about-custom-domains-and-github-pages) | Official GitHub documentation; opened 2026-11-11 | Documentation reference; no code copied |
| [MDN: Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy) | MDN reference opened 2026-11-11 | Documentation reference; no code copied |
| [OWASP HTML5 Security](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html) | Community-maintained series; official OWASP project page reports 121 sheets and 456 contributors | CC BY-SA 4.0; link to canonical guidance rather than copying its working Markdown |
| [OWASP Micro-Frontend Security](https://github.com/OWASP/CheatSheetSeries/blob/master/cheatsheets/Micro_Frontend_Security_Cheat_Sheet.md) | Opened current repository version 2026-11-11 | CC BY-SA 4.0; use as a reference, not as a copied implementation |
| [W3C Web Locks API](https://www.w3.org/TR/web-locks/) | W3C Working Draft dated 2026-11-09; explicitly a work in progress | W3C Software and Document License for reports; no code copied |
| [W3C Web Locks repository](https://github.com/w3c/web-locks) | Active upstream repository; links its test suite to web-platform-tests | Reports under W3C Software and Document License; test-suite contributions under W3C 3-clause BSD |
| [web-platform-tests](https://github.com/web-platform-tests/wpt) | Cross-browser platform test suite; W3C Web Locks spec links its Web Locks tests | 3-Clause BSD; use relevant tests as browser-conformance references only after target browser/version selection |

### Applied research conclusions

- A Web Lock is cooperative coordination within an origin, not a durable fence. The 2026-11-09 W3C Working Draft says `steal` releases the old lock and rejects its released promise, but the old callback may continue without exclusivity guarantees. An abort signal only aborts a request before it is granted. Every protected durable mutation still needs an atomic fence check.
- OWASP explicitly warns against user-supplied Worker scripts, recommends validating Worker messages, and says IndexedDB does not provide confidentiality. This strengthens the rule that a Worker is not a security sandbox for hostile code.
- A private `MessagePort` can provide a narrower capability channel only when the untrusted guest cannot access the port or its sender. It does not isolate code sharing the same privileged realm. Existing PYO-CTRL tests already cover the conditional channel-spoofing threat; no duplicate IDs are added here.
- WPT is the legitimate upstream reference for browser API conformance. It is preferable to inventing a PocketCode-specific reimplementation of Web Locks semantics. No WPT code was copied or added.

## 8. Red-team corrections to previous work

1. **P40 previously treated its four slices as if all assertions mapped to current models.** They do not. This audit pins the model files and separates the effect outbox, grant-event outbox, journal, receipt store and verdict projection.
2. **P40 A1 said no-op progress would not advance version, but the model permits equal progress and increments the aggregate version.** The protocol now marks equal-progress/no-op parity as a missing assertion and expected model gap, not an existing passing behavior.
3. **P40 A3 said the consumer should reject altered semantic fields while retaining a digest, but the current GrantEvent carries no canonical payload bytes.** That rejection cannot be proven by the current consumer. The test is now BLOCKED pending a canonical envelope and trusted ingress definition.
4. **P40 B1 could be read as applying FakeOutbox fencing to grant-event publication.** The two outboxes are now explicitly separated; grant-event `mark_outbox_delivered` has no relay fence.
5. **P40 D grouped worker/output/receipt lifecycle into a pure verdict test.** The projection helper has no worker, cleanup, stream-close or durable receipt inputs. Those are now separate acceptance layers.
6. **Previous Pages evidence stopped at “URL unknown”.** The deployment job log supplies the successful deployment URL and SHA, but also proves that the last known deploy is older than current main. Live headers and current serving state remain unknown.
7. **Previous origin work did not explicitly convert path-vs-origin rules into an account-host storage threat.** The public `portfolio` Pages project now confirms a second project path on the same host. No exploit is claimed.

## 9. Decision and verification status

- **VERIFIED:** exact source/test blobs listed above; successful Pages workflow run and deployment SHA/URL; main-only automatic trigger; two public Pages repositories on the same host; same-origin path semantics; OWASP storage and Worker guidance; W3C Web Locks Working Draft status and licence; WPT 3-Clause BSD licence.
- **INFERRED:** a script executing on either Pages project has the same browser-origin privileges; a compromised sibling page could access PocketCode origin storage if it exists there.
- **UNKNOWN:** whether an out-of-band deployment occurred; live headers and current response; generated portfolio scripts and complete sibling deployment state; target iOS/Android storage behavior; real Pyodios Worker topology; durable adapter.
- **NOT RUN:** source tests, P40 tests, browser/device tests, live Pages response/header probe, origin sibling test, Worker spoof test and any deployment.
- No source/test code, canonical IDs, runtime, provider, database, transport, dependency, PR, DNS, Pages setting or owner decision was changed. P39/P40 remains CLOSED; OD-01..OD-13 remain OPEN.
