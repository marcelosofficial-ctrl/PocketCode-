# iPhone-only build and App Store roadmap for PoCo (research, 2026-11-08)

Status: RESEARCH and PROPOSED. Nothing here is implemented or approved. Sources accessed 2026-11-08. Tags: VERIFIED = read on a primary page (Apple, GitHub docs) or in this repo; SECONDARY = news, blog or forum; INFERRED = my reasoning; UNKNOWN = not established.

## 1. Bottom line
- **Recommended path (PROPOSED):** keep the web UI as the product core, wrap it in a thin native iOS shell (Capacitor), build, sign and upload with GitHub Actions on macOS runners, distribute through TestFlight, submit through App Store Connect in Safari. Everything is operated from the iPhone: commits by AI connectors or an iOS git client, runs and logs in the GitHub mobile app or Safari.
- **Cost:** the Apple Developer Program is US$99 per membership year (VERIFIED, developer.apple.com/programs/whats-included). It is the one unavoidable cost for TestFlight and the App Store and conflicts with the $0 rule (D-005), so it is an owner decision. GitHub Actions on standard hosted runners is free for PUBLIC repositories (VERIFIED, GitHub billing docs) and this repository is public, so macOS builds cost $0. For private repositories the free allowance is 2,000 minutes a month and macOS minutes count 10x (VERIFIED, same docs), about 200 macOS minutes.
- **$0 interim:** the existing static prototype is already published to GitHub Pages by the workflow "Publish mobile prototype preview" (VERIFIED in .github/workflows/preview-prototype.yml: it deploys prototypes/mobile-runner/index.html from main). Opening it in Safari and choosing Add to Home Screen gives a testable app with no Apple account. Limits (INFERRED, partly SECONDARY): no App Store presence, browser storage eviction rules, WebAssembly memory ceilings (one Pyodide iOS app reports about 300 MB heap), no background execution.
- **Not first choices:** Xcode Cloud needs a workflow configured in Xcode 15 or later (VERIFIED, Apple get-started page), so it is not phone-only; keep it as an option if you ever borrow a Mac once. React Native or Expo and native SwiftUI both mean a rewrite of a UI that is currently one 17 KB HTML file; decide later.

## 2. The pipeline stage by stage
| Stage | From the iPhone | Runs in the cloud | One-time setup | Cost | Limits | Security |
|---|---|---|---|---|---|---|
| DESIGN | Safari preview of the Pages prototype; AI-written CSS | none | design tokens in the repo | $0 | no native Liquid Glass or haptics in a browser (INFERRED) | none |
| EDIT | GitHub web editor in Safari; AI connectors (the current way); an iOS git client such as Working Copy (paid features UNKNOWN, verify before paying) | none | token permissions (done for Claude) | $0 to small | GitHub mobile app file editing UNKNOWN | fine-grained tokens, expiry |
| COMMIT | same as above | CI starts on push | branch policy | $0 | rapid pushes cause red intermediate runs | no secrets in commits |
| BUILD | start and watch a workflow in the GitHub mobile app or Safari | macOS runner (macos-14, macos-15, macos-26 preview listed in GitHub docs, VERIFIED) | add an ios-shell folder and a build workflow (unsigned simulator build first, no Apple account needed) | $0 on a public repo | no local Xcode, debugging by logs | pin action versions |
| SIGN | create an App Store Connect API key in Safari | CI signs with the key (automatic signing or fastlane; INFERRED, standard practice, test it) | Apple Developer Program, app record, bundle ID, API key | $99 per year | key lives in CI secrets | see section 5 |
| TEST | install from TestFlight on the iPhone 12 (iOS support of an iPhone 12 UNKNOWN for the newest OS; check) | build upload from CI | internal testers | included | external testers need a beta review | none |
| DISTRIBUTE | TestFlight link | Apple | none | included | 90-day build expiry (UNKNOWN, verify) | none |
| SUBMIT | App Store Connect in Safari: metadata, privacy answers, Notes for Review | Apple review | privacy policy URL, screenshots (iPhone captures work) | included | review outcome is not guaranteed | do not claim unbuilt features |

## 3. Options compared
| Option | Fit | Evidence and caveats |
|---|---|---|
| GitHub Actions macOS + Capacitor shell | BEST fit: reuses the web UI, free on a public repo | Capacitor wraps a web app in a native WKWebView shell (INFERRED from its public design; verify version and plugins before committing). Needs 4.2 minimum-functionality care (section 4) |
| Xcode Cloud | optional later | 25 compute hours a month included with membership (VERIFIED). Workflow creation needs Xcode (VERIFIED); App Store Connect on the web can edit workflows and launch builds (VERIFIED) |
| Expo and EAS Build | only if the UI becomes React Native | EAS free-tier limits not checked (UNKNOWN); a rewrite; JavaScript-bundle updates are tolerated by App Review but native changes need a new binary (SECONDARY) |
| Native SwiftUI | best Apple fidelity, biggest rewrite | revisit once the product loop is proven |
| Working Copy | phone-side git | features and price UNKNOWN; not needed while AI connectors commit |
| Codemagic and similar | alternatives | not researched |

## 4. Apple rules that shape PoCo (Guideline 2.5.2, 4.7, 4.2)
- **2.5.2 (VERIFIED text, quoted in several sources and Apple forum threads):** apps must be self-contained in their bundles and may not download, install or execute code that introduces or changes features or functionality of the app. A narrow exception: educational apps designed to teach, develop or let students test executable code may, in limited circumstances, download code that is not used for other purposes, and must make that source fully viewable and editable by the user (SECONDARY quotations; read the live page before submitting).
- **4.7 (VERIFIED, Apple news 2025):** the November 13, 2025 revision clarified that HTML5 and JavaScript mini apps and mini games are in scope. PoCo must not look like a store for mini apps.
- **2026 enforcement (SECONDARY, 9to5Mac and others citing The Information):** Apple reportedly blocked updates to vibe-coding apps and pulled at least one, citing 2.5.2. PoCo lets AI produce code that may run on the device, so this is the main review risk.
- **Existing evidence for on-device Python:** Python IDE and Jupyter-style apps and at least one Pyodide-based iOS app are in the store (SECONDARY). That suggests the category is allowed, not that PoCo is.
- **Design rules for compliance (PROPOSED):** (R1) bundle Pyodide and every executable asset inside the app binary; never fetch executable code from a CDN at run time; (R2) AI-generated code is data shown to the user, who must see it, can edit it and presses Run; no automatic execution; (R3) no catalog or sharing of runnable mini apps; (R4) remote execution on the owner's own machine over SSH is not execution on the device; provider API calls are ordinary network use; (R5) include real native value (share sheet, file picker, Keychain, haptics, offline) so the app is not a bare web wrapper (4.2); (R6) explain these points in the Notes for Review; (R7) keep claims in the store listing to what is built.

## 5. Security precautions
- The repository is public and AI connectors can write to it. A prompt-injected agent could edit a workflow to leak signing secrets. Mitigation (PROPOSED): keep signing in a GitHub Environment with required reviewers (owner approval for each signing run), keep the Apple key out of any workflow that runs on pull requests, pin third-party actions by commit, and remove the token's Workflows permission once the pipeline is stable.
- Give the App Store Connect API key the lowest role that works; store it only as an environment secret; rotate it if any doubt; never print it in logs.

## 6. Roadmap with gates
| Gate | Work | Who | Evidence for done |
|---|---|---|---|
| G0 | Owner decisions: name PoCo (see below), spend of $99, Apple ID to enroll | owner | decision recorded in DECISIONS.md |
| G1 | Harden the Pages prototype as the $0 test vehicle; test on the iPhone 12 | AI + owner | device notes with exact build |
| G2 | Add ios-shell and an unsigned simulator build workflow on macOS runners | AI | green run for the exact commit |
| G3 | Enroll, create app record, bundle ID, API key (Safari) | owner | screenshot-free confirmation, key stored as environment secret |
| G4 | Signed build and TestFlight upload from CI, with required-reviewer gate | AI + owner approval | TestFlight build visible on the iPhone |
| G5 | Internal TestFlight on the iPhone 12 | owner | notes |
| G6 | Compliance pass against section 4 rules; Notes for Review draft | AI | checklist with evidence |
| G7 | Submit | owner | App Store Connect status |

## 7. Name check before any public step (INFERRED risk)
POCO is also a widely used open-source C++ library family and a Xiaomi phone brand. This may affect App Store name availability, search and trademark. Check the App Store Connect name reservation, a trademark search for the owner's jurisdictions, and the domain, before rebranding the repository or the store listing.

## 8. Unknowns
Free-tier details for EAS and Codemagic; Working Copy features and price; GitHub mobile app editing; iPhone 12 iOS support for the newest OS and TestFlight expiry; Capacitor current version and plugin needs; whether review accepts PoCo's AI-code flow (only a real submission answers that).

## 9. Sources (accessed 2026-11-08)
developer.apple.com/programs/whats-included; developer.apple.com/xcode-cloud and its get-started page; developer.apple.com/news?id=ey6d8onl (4.7 update); docs.github.com About billing for GitHub Actions and Supported runners; this repository's .github/workflows/preview-prototype.yml; 9to5mac.com report on vibe-coding apps; ptkd.com and Capgo explainers on 2.5.2; Apple developer forum threads on 2.5.2 and 4.7.
