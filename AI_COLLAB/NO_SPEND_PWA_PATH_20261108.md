# NO-SPEND PATH: installable web app (PWA) instead of the App Store (2026-11-08)

Owner decision 2026-11-08: no spending. This overrides the paid steps of IPHONE_ONLY_APP_STORE_ROADMAP_20261108.md: no Apple Developer Program (US$99 per year), no TestFlight, no signed native build, no App Store submission. Gates G3 to G7 of that roadmap are DEFERRED until the owner approves spending or a Mac becomes available. G0 to G2 are replaced by the plan below. Tags: SECONDARY = articles and vendor blogs read 2026-11-08; INFERRED; UNKNOWN.

## What the $0 path is
PoCo ships as an installable web app served from GitHub Pages, which the repository already does for the static prototype (VERIFIED: .github/workflows/preview-prototype.yml deploys prototypes/mobile-runner/index.html from main). The owner opens it in Safari and chooses Share, then Add to Home Screen.

## What iOS allows, as reported (SECONDARY; confirm on the owner's iPhone)
- Web push works only for web apps added to the Home Screen, and only after the user grants permission following a tap (iOS 16.4 and later).
- WebKit documents that Safari's seven-day cap on script-writable storage does not apply to Home Screen web apps, and that their data is kept separate from Safari's. Installing is therefore what makes local state persistent. A non-installed page reportedly gets about 50 MB class quotas and can be evicted.
- There is no automatic install prompt on iOS; the user must install manually.
- All iOS browsers use the WebKit engine, so Pyodide in Safari and in a Home Screen web app share the same memory behaviour (a Pyodide iOS app reports about 300 MB heap and no way to interrupt a running cell; INFERRED that the same applies here).
- UNKNOWN until tested: haptic feedback from the web, exact storage quota on the owner's iPhone 12, behaviour after restarts.

## Consequences for the product design (PROPOSED)
1. Install-first onboarding: explain Add to Home Screen at first run; warn when running un-installed that data may be evicted.
2. Export and backup are core features (they already match the project principle "exportable"): one tap to export the project and the evidence as a file.
3. Local execution is Pyodide in a Web Worker with a memory guard and a visible "too big, use remote" path; the Pyodide files are hosted with the app on Pages, not fetched from a third-party CDN at run time.
4. A browser cannot open SSH. Remote execution needs a small service the owner runs on their own machine (WebSocket or HTTPS over a private network). That is a later design item, not part of the $0 prototype.
5. A browser page cannot do true Liquid Glass or system haptics; polish comes from typography, spacing, continuous corner radii, spring-like CSS motion that respects prefers-reduced-motion, and safe-area handling.

## $0 next steps (no spending, no deployment beyond the existing Pages workflow)
1. Add a web app manifest, icons and a service worker to the prototype so it installs and works offline (change on a branch; the Pages workflow runs from main, so nothing deploys until a merge the owner approves).
2. Write an iPhone test checklist for the owner: install, offline, storage after a day and after a restart, Pyodide memory ceiling, clipboard actions.
3. Define design tokens (type scale, spacing, radii, motion durations) in the prototype stylesheet as the basis of the design specification.

## When to revisit
If the owner approves the US$99 fee, or a Mac is borrowed for one-time Xcode Cloud setup, resume at G3 of the iPhone roadmap. There is no free, phone-only way to produce a TestFlight or App Store build (INFERRED).

## Sources (accessed 2026-11-08)
magicbell.com PWA iOS limitations guide; monterail.com PWA for Apple iOS; ecorpit.com PWA 2026 guide (cites WebKit documentation on Home Screen web apps and ITP); itnext.io PWAs on iOS (reports an iOS 17.4 EU change); abratabia.com PWA on iOS; developer.apple.com programs page for the fee.
