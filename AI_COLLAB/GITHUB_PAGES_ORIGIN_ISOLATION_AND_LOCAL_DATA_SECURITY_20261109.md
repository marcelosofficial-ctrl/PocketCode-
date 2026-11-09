# GitHub Pages origin isolation and local-data security review

**Date:** 2026-11-09  
**Status:** Primary-source research / security finding / NOT IMPLEMENTED / NOT DEVICE-TESTED  
**Scope:** Owner-approved $0 GitHub Pages PWA direction and its browser-local persistence boundary.  
**Authority:** This document adds a deployment-origin threat finding. It does not select a domain, change D-006, authorize a migration, or alter canonical LOOP/CASE/D IDs.

## 1. Executive finding

**HIGH PRIORITY, CONDITIONAL ON PROJECT-PAGES HOSTING:** GitHub Pages project sites normally use `https://<owner>.github.io/<repository>`. Browser origin is the scheme + hostname + port tuple. The URL path is not part of the origin. Therefore two project sites under the same `<owner>.github.io` hostname are same-origin even when their repository paths differ.

That has a direct PocketCode consequence: if PocketCode is deployed as a project site on the account's shared `github.io` hostname, another same-origin site hosted under that hostname can potentially access PocketCode's origin-scoped IndexedDB, OPFS and other same-origin storage through JavaScript. A path prefix, separate repository, separate service-worker scope, obscure database name or random storage key is **not** a browser security boundary.

This is more consequential than ordinary storage eviction. PocketCode's local workspace may contain user code, imported files, AI conversation context, execution output, credentials accidentally pasted by a user, and reports. Same-origin hostile or compromised content could read or modify those records if it executes with the same origin.

**VERIFIED platform rule:** origin ignores path; same-origin storage is shared by origin.  
**VERIFIED GitHub Pages rule:** project sites use the owner hostname plus repository path.  
**INFERRED PocketCode risk:** if the deployed app uses that shared project-site hostname, sibling same-origin Pages content is inside the browser storage trust boundary.  
**UNKNOWN:** actual PocketCode Pages URL, custom-domain configuration, other content hosted on the same hostname, service-worker scope and whether any sensitive data is currently stored there.

## 2. Evidence

1. GitHub documents project-site default locations as `http(s)://<owner>.github.io/<repositoryname>`, distinct from user/organization sites at `http(s)://<owner>.github.io`: [GitHub Pages: What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).
2. MDN defines origin as protocol, host and port. Paths do not distinguish origins; its examples explicitly classify different paths on the same host as same-origin: [Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Defenses/Same-origin_policy).
3. MDN says IndexedDB databases are associated with an origin, and every origin has its own set of databases: [IndexedDB basic terminology](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Basic_Terminology).
4. WebKit describes storage quotas and eviction per origin, including IndexedDB and File System storage: [Updates to Storage Policy](https://webkit.org/blog/14403/updates-to-storage-policy/).
5. GitHub Pages is static hosting for HTML, CSS and JavaScript from repositories. A separate repository does not imply a separate browser origin: [What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages).

The platform facts are source-verified. Whether the conditional risk applies to the live PocketCode deployment requires checking its actual URL and sibling Pages content.

## 3. Security impact and threat model

If the app runs at `https://OWNER.github.io/PocketCode-/`, any other page served at `https://OWNER.github.io/OTHER-PROJECT/` has the same origin tuple. Its JavaScript can attempt to open the same IndexedDB database names and request the same origin-private storage. Same-origin policy does not isolate paths.

Potential impacts include:
- Confidentiality: read project source, imported files, reports, task history and stored context.
- Integrity: alter local command/attempt state, receipts, artifact manifests or recovery records.
- Availability: delete databases or origin data, consume quota, corrupt app-managed records or interfere with service-worker registrations within its scope.
- Evidence integrity: forge or alter local records unless a separate trusted boundary authenticates and verifies them. Hashes stored beside attacker-editable bytes do not solve this.

This is not a remote internet attacker automatically reading browser storage. The attacker needs script execution in same-origin content, a compromised dependency/build, a malicious sibling Pages site or another same-origin injection path. It is nevertheless a material deployment architecture risk when the hostname is shared with independently maintained content.

A service-worker path scope can limit which URLs the worker controls. It does **not** change the origin or isolate IndexedDB/OPFS from same-origin scripts. A unique database name is namespace hygiene, not access control.

## 4. Deployment options, without choosing one

| Option | Origin isolation | Cost / tradeoff | Status |
|---|---|---|---|
| GitHub Pages project site on shared `OWNER.github.io` | **No isolation from sibling paths on that hostname** | $0 and simplest; sibling same-origin code remains in the trust boundary | Conditional risk; do not treat as hostile-content isolated |
| Dedicated custom hostname for PocketCode | Separate origin if hostname is distinct and not shared with other untrusted content | Domain registration/renewal may cost money; conflicts with current D-006 unless owner approves | Not selected; no spend authorized |
| Separate GitHub Pages user/organization hostname under a distinct account/host | Separate origin if hostname differs | Requires a separately controlled hostname/account arrangement; ownership and maintenance implications | Not selected; research only |
| Native wrapper / alternate hosting origin | Can provide a different origin or stronger OS boundary depending on implementation | Adds build/distribution/maintenance complexity and may violate current no-spend/phone-only constraints | Not selected |

Do not recommend buying a domain or changing the approved GitHub Pages path without an explicit owner decision. First inspect the actual published URL and whether any sibling same-origin site exists. If the shared origin is retained, explicitly accept the same-origin content trust boundary and keep secrets out of browser storage.

## 5. Required guardrails if shared-origin GitHub Pages is retained

1. Treat every script and every page hosted on `OWNER.github.io` as part of PocketCode's trusted computing base, regardless of repository or URL path.
2. Do not store provider API keys, GitHub tokens, passwords, long-lived bearer tokens, signing keys or other reusable credentials in IndexedDB, OPFS, LocalStorage, Cache Storage, service-worker state or application files.
3. Never load third-party scripts, analytics, widgets or executable dependencies without pinned versions, integrity/provenance review and a clear need. Avoid dynamic script execution and unsafe HTML insertion.
4. Apply a restrictive Content Security Policy and other suitable response headers where GitHub Pages configuration permits. Verify the actual deployed headers; a meta CSP cannot express every header-only directive and does not protect against every same-origin compromise.
5. Keep app data schema namespaced by product and schema version to avoid accidental collisions, but do not call namespacing isolation.
6. Keep immutable per-attempt artifact staging paths. Never let retries or stale workers write into a shared/final artifact path. A stale worker may still write its own abandoned staging object; only a current-fence transaction may publish a manifest reference to it.
7. On launch, verify database schema/version and integrity invariants. Treat missing or malformed records as recovery-required, not empty success.
8. Provide explicit user-controlled export/backup for important projects and reports. Local persistence, even when browser storage is persistent, is not a backup.
9. Make the product warning accurate: browser-local data is available to scripts executing in the same origin and may be lost through clearing, eviction, corruption or device loss.
10. Do not present a hash as proof of producer identity or trustworthy execution. An attacker with same-origin write access can often replace both data and its stored hash.

## 6. New acceptance requirements to add to the PWA test plan

These are proposed PocketCode-specific acceptance cases, not canonical LOOP/CASE IDs.

| ID | Scenario | Expected result |
|---|---|---|
| ORIGIN-01 | Resolve deployed app URL and compute scheme/host/port origin | Record exact origin and Pages project/user/custom-domain type |
| ORIGIN-02 | Deploy or create a controlled sibling path on the same host and attempt to open the app's test IndexedDB database | Demonstrate that path separation is not a security boundary; do not use real user data |
| ORIGIN-03 | Same-origin sibling script attempts to enumerate/read app database names and records | Test confirms exposure under shared origin; production decision must either isolate hostname or accept threat boundary |
| ORIGIN-04 | Same-origin sibling attempts OPFS access and known app directory lookup | Document actual access behavior; no assumption that path or service-worker scope protects it |
| ORIGIN-05 | Verify service-worker scope for project subpath | Confirm worker scope limits control, while documenting that it does not isolate origin storage |
| ORIGIN-06 | Inject a controlled script into app build/test page | CSP and dependency controls prevent unauthorized script execution where configured; record remaining limits |
| ORIGIN-07 | Stale worker writes after losing local fence | It can write only to its unique abandoned staging path; it cannot publish or overwrite the current artifact |
| ORIGIN-08 | Attempt to reuse an artifact path across attempts/fence generations | Reject; every artifact version/staging path is unique and immutable after verification |
| ORIGIN-09 | Export and restore a project backup into a clean browser origin | Verify schema, byte length, digest, receipt/attempt references and recovery state before marking restored |
| ORIGIN-10 | Storage quota failure during metadata or artifact write | No false committed/saved UI; preserve recoverable staging evidence and show export/recovery guidance |

Run these tests with synthetic data and a controlled sibling page. Never expose real workspace contents to a test page.

## 7. Related durability findings confirmed during this review

### IndexedDB commit and durability

The W3C IndexedDB 3.0 document is a Working Draft, not a final Recommendation. It specifies atomic transaction semantics and a `complete` event after successful commit. Its `strict` durability value is a **hint**: the user agent may wait until changes are verified on persistent media, and the specification notes the flush can cost latency and battery. It is not a universal promise against browser bugs, storage eviction, user clearing or device loss. Keep the app rule: show “committed locally” only after transaction completion; show the actual durability hint/availability separately; never say “backed up” or “power-loss proof” based on the hint alone. Sources: [W3C IndexedDB 3.0](https://www.w3.org/TR/IndexedDB/) and [MDN IDBTransaction.durability](https://developer.mozilla.org/en-US/docs/Web/API/IDBTransaction/durability).

### OPFS and IndexedDB are separate commit domains

OPFS sync-access-handle `flush()` persists writes made through that handle, and the handle is dedicated-worker-only. It does not create an atomic transaction with IndexedDB metadata. Therefore the two-domain staging protocol in `PWA_LOCAL_STORAGE_AND_RECOVERY_CONTRACT_20261109.md` remains necessary: unique staging identity, write/flush, readback verification, then one IndexedDB transaction to publish the immutable manifest/receipt reference. Sources: [File System Standard](https://fs.spec.whatwg.org/) and [MDN flush()](https://developer.mozilla.org/en-US/docs/Web/API/FileSystemSyncAccessHandle/flush).

### SQLite guardrail if it is ever evaluated

SQLite WAL's documented reset bug affected versions through 3.51.2 under a specific multi-connection/process write/checkpoint race; it is fixed in 3.51.3 and later. WAL with `synchronous=NORMAL` can lose recently committed transactions after power failure or OS crash; `FULL` adds a WAL sync per commit and is the documented durable WAL setting. Rollback-journal durability differs; `EXTRA` may be needed for the strongest documented power-loss behavior there. Do not reduce this to “SQLite is ACID.” Pin and inspect the actual linked SQLite build, journal mode, synchronous setting, VFS and filesystem. Sources: [SQLite WAL](https://www.sqlite.org/wal.html), [SQLite PRAGMA synchronous](https://www.sqlite.org/pragma.html), [SQLite 3.51.3 release notes](https://www.sqlite.org/releaselog/3_51_3.html).

## 8. Recommended next work

1. Confirm the exact GitHub Pages deployment URL and site type from repository Pages settings or the live site. Do not infer it from the repository name.
2. If it is a shared `OWNER.github.io` project path, inventory other content under that host and decide whether that content is trusted.
3. Add origin isolation to the product threat model before any real user workspace data is persisted.
4. Add ORIGIN-01..10 to the proposed PWA acceptance plan without changing canonical CASE IDs.
5. Preserve the no-spend rule. If adequate origin isolation requires a paid domain or hosting, surface that as an owner decision rather than silently changing direction.

## 9. Verification boundary

- **VERIFIED:** GitHub Pages project-site URL structure; origin tuple excludes path; IndexedDB is origin-scoped; WebKit storage policy is origin-scoped; IndexedDB strict durability is a hint; OPFS flush is a file-level persistence operation; SQLite WAL durability/version constraints described above.
- **INFERRED:** sibling project pages on the same `github.io` host can access PocketCode origin storage if PocketCode is served from that same origin.
- **UNKNOWN:** actual PocketCode deployed URL, sibling-site inventory, deployed CSP/headers, worker scope, storage API behavior on the owner's device.
- **NOT RUN:** controlled sibling-origin access test, device storage tests, browser crash/power-loss tests, export/restore tests, app integration tests.
- No code/tests, canonical identifiers, owner decisions, runtime/provider/database/hosting choices or spending were changed.
