# NO-SPEND PATH: installable web app (PWA) instead of the App Store

**Owner decision 2026-11-08: no spending.** This overrides the paid steps of `IPHONE_ONLY_APP_STORE_ROADMAP_20261108.md`: no Apple Developer Program, no TestFlight, no signed native build and no App Store submission. Gates G3 to G7 are DEFERRED until the owner separately approves spending or a Mac becomes available. D-006 remains unchanged.

**Evidence status refreshed 2026-11-09:** VERIFIED = primary documentation opened; INFERRED = design conclusion; UNKNOWN = not checked on the owner's device.

## 1. What the $0 path is

PoCo's no-spend distribution path is an installable web app served from GitHub Pages. The repository already deploys the static prototype from main through `.github/workflows/preview-prototype.yml` (VERIFIED from the repository workflow). The owner opens the site in Safari and manually chooses Share → Add to Home Screen. No product deployment or merge is authorized by this note.

## 2. iOS Home Screen behavior

- **VERIFIED:** WebKit's Safari 26.0 release notes (2025-09-15) say every site added to the Home Screen on iOS 26/iPadOS 26 opens as a web app by default. The Add to Home Screen interface includes an **Open as Web App** switch; turning it off makes it a browser bookmark instead. The user remains in control.
- **VERIFIED:** On iOS 26, a Web App Manifest is no longer required for the Home Screen icon to open as a web app. A manifest and defined icons still improve app identity and configuration, and older iOS versions still need the earlier manifest/meta-tag behavior where applicable.
- **VERIFIED:** WebKit's current Tracking Prevention documentation explicitly exempts a Home Screen web app's first-party domain from ITP's seven-day cap on script-writable storage. It also says Home Screen web-app data is isolated from Safari. IndexedDB, LocalStorage, SessionStorage, service-worker registrations and cache are among the storage types affected by the seven-day Safari rule.
- **Important limitation:** the ITP exemption is not a permanent backup or blanket eviction exemption. WebKit storage is still quota-limited and may be affected by storage pressure or quota failures. The Storage API's `persist()` request is heuristic; `estimate()` is an estimate and does not guarantee space. Explicit user clearing and device loss remain outside app protection.
- **VERIFIED:** WebKit's iOS 17+ storage policy describes Home Screen web apps as having the same origin and overall quotas as browser apps. These are upper limits, not a promise that an operation will fit.
- **VERIFIED:** iOS/iPadOS in the EU permits qualifying browser apps to use alternative browser engines under Apple's entitlements from iOS 17.4/iPadOS 18. Safari itself remains WebKit, but the claim “all iOS browsers use WebKit” is not valid as a universal statement. Identify the actual engine for each tested browser; do not transfer Safari results automatically.
- **SECONDARY / owner device confirmation pending:** web push on iOS/iPadOS requires a Home Screen web app, user permission and user interaction before requesting it. Keep push outside the core local persistence and recovery contract.
- **UNKNOWN until tested on the owner's iPhone:** exact iOS/Safari build, storage quota, whether `navigator.storage.persist()` is granted, OPFS behavior, Web Locks availability, Web Push behavior, haptics, memory ceiling and restart/force-close recovery.

## 3. Storage and backup consequence

Install-first onboarding is useful, but installation alone must not be described as permanent data retention. The app must:
1. Check `navigator.storage.estimate()` and handle `QuotaExceededError` on every storage write.
2. Check `navigator.storage.persisted()`; optionally request `persist()` after explaining why. Show whether the result is persistent or best-effort.
3. Keep command/attempt/event/receipt metadata in one transactional local store. Do not leave IndexedDB transactions open across network calls or user-code execution.
4. Stage large artifact bytes, read them back, verify exact length and digest, then commit the receipt manifest. The OPFS file write and IndexedDB manifest transaction are not one atomic cross-API commit.
5. Provide explicit project/evidence export and import with manifest and hash verification. A user-managed export is separate from browser-origin storage.
6. Never delete accepted attempts or receipts automatically to free space. Any cache cleanup must be distinguishable from user data and ask before removing user-owned artifacts.

The complete proposed contract, crash matrix and 22 PWA acceptance cases are in `AI_COLLAB/PWA_LOCAL_STORAGE_AND_RECOVERY_CONTRACT_20261109.md`.

## 4. Execution and background limitations

- **INFERRED from platform constraints:** foreground local execution is the dependable MVP contract. Persist attempt intent before starting a worker; after worker/tab/app loss, reconcile from stored events and mark an attempt unresolved/incomplete unless a trusted terminal observation exists.
- **VERIFIED:** service workers are event-driven and may be terminated by the browser; `waitUntil()` does not guarantee indefinite execution. Do not promise that arbitrary user code continues after the PWA is closed or the device suspends it.
- **VERIFIED:** Background Sync remains marked Limited availability / not Baseline by MDN, and the fetched WebKit Background Sync request still shows NEW. Use it only as an optional feature-detected enhancement; foreground recovery must work without it.
- **INFERRED:** a web worker can isolate UI responsiveness but is not a process-level security boundary or an OS child-process supervisor. Do not convert worker disappearance into a fabricated child exit code or termination acknowledgement.
- Pyodide/WASM remains for trusted light tasks only. Untrusted code still requires a disposable externally constrained boundary before public execution claims.

## 5. Product consequences (PROPOSED)

1. Install onboarding distinguishes iOS 26+ (“Add to Home Screen”, leave **Open as Web App** enabled) from older versions (manifest/meta-tag standalone compatibility).
2. Local data status visibly distinguishes best-effort, persistence requested/granted and export-backed states.
3. Project and evidence export are core features, not optional debugging tools.
4. Execution UI makes foreground requirements and interrupted/unknown outcomes explicit; no background-completion promise.
5. Pyodide assets are hosted with the app on Pages, not fetched from a third-party CDN at runtime.
6. Remote execution remains a later adapter and requires a separately reviewed service the owner runs or an explicitly approved host; no server or spend is selected here.
7. Interface polish uses typography, spacing, continuous radii, reduced-motion-aware CSS animation and safe-area handling; no website redesign or change to the owner's current website is authorized.

## 6. No-spend next steps

1. Keep the PWA implementation proposal on a branch. The current Pages workflow deploys from main; no deploy occurs until an owner-approved merge.
2. Before source implementation, turn `PWA_LOCAL_STORAGE_AND_RECOVERY_CONTRACT_20261109.md` into a work packet and run its platform test matrix on real supported iOS and Android browsers.
3. Record the owner's exact iOS/Safari build and the `persist()` result without clearing or modifying existing user projects.
4. Add manifest/icons and a service worker for identity/offline cache behavior; do not treat either as the source of durable task state.
5. Define design tokens (type scale, spacing, radii, motion durations) in the prototype stylesheet as the design basis.

## 7. When to revisit the paid roadmap

Only if the owner explicitly changes D-006 or approves the required spend, resume at G3 of the iPhone roadmap. A no-spend GitHub Pages PWA does not provide a signed native binary, TestFlight or App Store submission.

## 8. Primary sources refreshed 2026-11-09

- WebKit, [Tracking Prevention](https://webkit.org/tracking-prevention/): explicit Home Screen origin exemption from ITP's seven-day script-writable storage cap.
- WebKit, [Full Third-Party Cookie Blocking and More](https://webkit.org/blog/10218/full-third-party-cookie-blocking-and-more/): ITP storage purge and Home Screen origin isolation.
- WebKit, [Updates to Storage Policy](https://webkit.org/blog/14403/updates-to-storage-policy/): quotas, eviction, persistent mode and heuristic approval.
- WebKit, [Safari 26.0 features](https://webkit.org/blog/17333/webkit-features-in-safari-26-0/): Add to Home Screen / Open as Web App change.
- Apple Developer, [Alternative browser engines in the EU](https://developer.apple.com/support/alternative-browser-engines/): qualifying alternative browser engines and iOS/iPadOS version requirements.
- W3C, [IndexedDB 3.0](https://www.w3.org/TR/IndexedDB-3/) and [Service Workers 2026 CRD](https://www.w3.org/TR/2026/CRD-service-workers-20261029/).
- MDN, [Storage quotas](https://developer.mozilla.org/en-US/docs/Web/API/Storage_API/Storage_quotas_and_eviction_criteria), [OPFS](https://developer.mozilla.org/en-US/docs/Web/API/File_System_API/Origin_private_file_system), [Background Sync](https://developer.mozilla.org/en-US/docs/Web/API/Background_Synchronization_API), [Web Locks](https://developer.mozilla.org/en-US/docs/Web/API/Web_Locks_API).

No product source/test was changed by this note. No deployment, owner device test, native build, spend or runtime/provider selection occurred.
