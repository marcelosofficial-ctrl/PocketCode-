# Apple-style design engineering spec for the PoCo web app (research and proposal, 2026-11-08; corrected 2026-11-10)

Status: PROPOSED. Nothing here is implemented. Correction note 2026-11-10: fixed a CSS bug in section 3 (see RED_TEAM_CORRECTIONS_CLAUDE_20261110.md). Target stack: the current prototype is one static HTML file (prototypes/mobile-runner/index.html, about 17 KB) served from GitHub Pages and installed on the iPhone from Safari (see NO_SPEND_PWA_PATH_20261108.md). RevDev is out of scope here: its UI source is not on GitHub, and the site claims .NET 8 / WPF (UNVERIFIED), so a RevDev design spec waits for PC access. Tags: VERIFIED = read on an Apple primary page (accessed 2026-11-08); SECONDARY = summaries and skill-pack pages; INFERRED; UNKNOWN = test on the iPhone.

## 1. What actually makes it feel like Apple (and what does not)
- **Liquid Glass is a navigation-layer material, not a content style.** HIG Materials (VERIFIED): Liquid Glass forms a functional layer for controls and navigation floating above content; do not use it in the content layer; use standard materials (blur, vibrancy) for content-layer structure; limit glass effects to the most important functional elements; the clear variant only over visually rich backgrounds, with a dimming layer (35% opacity suggested) over bright content. So "glass everywhere" is the opposite of the guidance.
- **Motion is purposeful and optional.** HIG Motion (VERIFIED): gratuitous or excessive animation can distract people or make them feel disconnected or uncomfortable; make motion optional. Secondary packs add: keep transitions short (about 200 to 400 ms), provide a crossfade alternative under Reduce Motion, pair haptics only with confirmations and errors.
- **Typography and size:** use the system font, a documented type ramp, text that scales with the user's setting; touch targets of at least 44 by 44 points with 8 to 12 point gaps (SECONDARY, matches long-standing HIG practice).
- **The rest is craft:** consistent spacing, hierarchy, real responsiveness (no input delay), continuity (elements move from where they were), and honesty of state. In PoCo the last one is functional: unknown, incomplete or degraded evidence must never look like PASS or FAIL (BOOT constraint 6).

## 2. Principles for PoCo
1. Content first: the run output, evidence and diff are the content layer; flat, standard surfaces.
2. Glass only on the top bar and bottom action bar, at most two glass surfaces on screen, never stacked.
3. State is never decoration: every state has an icon, a text label and a colour; colour is never the only signal.
4. Motion explains cause and continuity; nothing animates just to look alive; all motion has a Reduce Motion variant.
5. Never block interaction for an animation; animations are interruptible.
6. Performance over polish: if an effect drops frames on the iPhone 12, remove the effect.

## 3. Design tokens (CSS custom properties; values are provisional and must be tuned on the device)
```css
:root {
  color-scheme: light dark;
  /* 4 pt spacing grid */
  --space-1: 4px; --space-2: 8px; --space-3: 12px; --space-4: 16px; --space-5: 24px; --space-6: 32px;
  /* type ramp in rem so it follows the user's text size */
  --text-caption: 0.75rem; --text-footnote: 0.8125rem; --text-body: 1rem;
  --text-headline: 1.0625rem; --text-title: 1.375rem; --text-largetitle: 2rem;
  --font: -apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif;
  --font-mono: ui-monospace, "SF Mono", Menlo, monospace;
  /* semantic colours (provisional) */
  --bg: #ffffff; --bg-grouped: #f2f2f7; --surface: #ffffff;
  --label: #111114; --label-2: #5b5b63; --separator: rgba(60, 60, 67, 0.29);
  --accent: #0a84ff;
  --state-pass: #1f8a4c; --state-fail: #c62828; --state-incomplete: #b26a00; --state-unknown: #5b5b63;
  /* shape */
  --radius-control: 12px; --radius-card: 16px; --radius-sheet: 24px;
  /* motion */
  --dur-fast: 150ms; --dur-base: 250ms; --dur-slow: 350ms;
  --ease-out: cubic-bezier(0.22, 1, 0.36, 1);
  /* spring-like curve via linear(); sample points are illustrative: generate real ones from damping and stiffness and tune by feel */
  --spring-soft: linear(0, 0.2 6%, 0.62 14%, 0.92 24%, 1.03 34%, 1.02 44%, 0.995 58%, 1);
}
@media (prefers-color-scheme: dark) {
  :root { --bg: #000000; --bg-grouped: #000000; --surface: #1c1c1e; --label: #f5f5f7;
          --label-2: #a1a1a6; --separator: rgba(84, 84, 88, 0.6); }
}
/* Dynamic Type hook in WebKit. Do NOT add a font-size declaration after this line: it would override the size this shorthand provides. UNKNOWN until verified on the device. */
html { font: -apple-system-body; }
body { font-family: var(--font); font-size: var(--text-body); color: var(--label); background: var(--bg-grouped); }
```
- `linear()` easing is supported in Safari at least since 17.4 (a 17.4 release note lists a fix to it; VERIFIED). Do not impose universal physics values: treat the spring curve as a tunable token per interaction.
- Continuous (squircle) corners: the CSS `corner-shape` property exists in the specification and in some engines but Safari support is UNKNOWN to me; use `border-radius` and add `@supports (corner-shape: squircle) { .card { corner-shape: squircle; } }` as progressive enhancement only.

## 4. Components (each with a state, a size rule and an accessibility rule)
**Top bar and bottom action bar (the only glass):**
```css
.bar {
  position: sticky; top: 0; padding: env(safe-area-inset-top) var(--space-4) var(--space-2);
  background: color-mix(in srgb, var(--bg) 72%, transparent);
  -webkit-backdrop-filter: blur(20px) saturate(1.4); backdrop-filter: blur(20px) saturate(1.4);
  border-bottom: 0.5px solid var(--separator);
}
@media (prefers-reduced-transparency: reduce) { .bar { background: var(--bg); -webkit-backdrop-filter: none; backdrop-filter: none; } }
```
(`backdrop-filter` interoperability was improved in Safari 17.4, VERIFIED; `prefers-reduced-transparency` support in Safari is UNKNOWN, so also keep an opaque fallback under `@supports not (backdrop-filter: blur(1px))`.)
**Grouped list rows** for projects, runs and files: 44 px minimum height, inset grouped background, chevron only when it navigates.
**Buttons:** 44 px minimum hit area, a clear primary action per screen, destructive actions separated.
**Bottom sheet** for run details and the context picker; interruptible (section 5).
**State pill (functional core):**
```html
<span class="state" data-state="unknown" role="status"><svg aria-hidden="true">...</svg><span class="state-label">UNKNOWN</span></span>
```
States PASS, FAIL, INCOMPLETE, UNKNOWN each have a distinct icon and label; UNKNOWN and INCOMPLETE are never styled like PASS or FAIL.
**Logs and diffs:** monospace, a virtualized or `content-visibility: auto` list, copy as an explicit button (no clipboard polling).

## 5. Motion standards
- Durations: 150 ms for feedback, 250 ms for most transitions, 350 ms for sheets; nothing longer without a reason.
- Animate `transform` and `opacity` only; never animate layout properties.
- Interruptible, using the Web Animations API so a reverse starts from the current position:
```js
const reduce = matchMedia('(prefers-reduced-motion: reduce)');
let anim;
function openSheet(el) {
  anim?.cancel();
  anim = reduce.matches
    ? el.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 120, fill: 'both' })
    : el.animate([{ transform: 'translateY(100%)' }, { transform: 'translateY(0)' }],
        { duration: 350, easing: getComputedStyle(document.documentElement).getPropertyValue('--spring-soft'), fill: 'both' });
}
function closeSheet() { anim?.reverse(); }
```
- Reduce Motion: replace movement with a short crossfade; no parallax; no auto-playing loops.
- Input is never blocked while an animation runs.

## 6. Accessibility requirements
Text scales (rem units, test at the largest accessibility size); contrast at least 4.5 to 1 for body text; every interactive element has an accessible name; run state changes use `aria-live="polite"`; visible `:focus-visible` for keyboard and switch control; no information by colour alone; Reduce Motion and Reduce Transparency honoured; test with VoiceOver.
**Haptics:** iOS Safari has no general haptics API (UNKNOWN to confirm). Safari 17.4 added `<input type="checkbox" switch>` (VERIFIED, release notes); reports say toggling it produces a haptic tick on iPhone (SECONDARY, UNVERIFIED). Use it only for genuine on/off settings; do not simulate haptics.

## 7. Performance
Limit `backdrop-filter` to two small bars; avoid large blurred shadows; no animated gradients; keep Pyodide in a Web Worker so the main thread stays responsive; measure on the iPhone 12 and drop any effect that costs frames; WebKit memory is limited (see the no-spend path document).

## 8. Migration plan that keeps working behaviour
1. Add the token block to index.html without changing any markup; map existing colours and sizes to tokens.
2. Apply the type ramp and spacing, then check nothing overflows at the largest text size.
3. Replace components one at a time (bars, rows, buttons, state pill, sheet), testing after each.
4. Keep `scripts/check_mobile_prototype.py` passing (it checks source patterns). The CI workflow only triggers on scripts/ changes, so prototype edits are not checked automatically: add `prototypes/**` to its path filter when editing begins (INFERRED; I have not read the checker).
5. iPhone checklist after every step: install, offline, largest text size, Reduce Motion on, Reduce Transparency on, dark mode, landscape, one-handed reach.

## 9. Queued research (not done)
Verify on the iPhone: `-apple-system-body` Dynamic Type behaviour, `prefers-reduced-transparency`, haptic behaviour of the switch input, `corner-shape` support. Read the HIG pages on typography, layout, buttons, sheets and accessibility directly (this pass read Materials and Motion; other points come from secondary summaries). For RevDev: Windows options (WPF with Fluent-style libraries, WinUI 3, Mica and acrylic materials) once the UI source is inspected; Apple's glass is not a Windows pattern and should not be ported.

## Sources (accessed 2026-11-08)
developer.apple.com/design/human-interface-guidelines/materials (Liquid Glass and standard materials); developer.apple.com/design/human-interface-guidelines/foundations/motion; developer.apple.com Safari 17.4 release notes (checkbox switch, backdrop-filter, linear() fix); secondary HIG summaries (skill packs on skills.lc, playbooks.com, smithery.ai); cssportal.com (corner-shape); a WWDC25 design lab summary on the Apple Developer forums.
