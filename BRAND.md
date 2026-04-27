# ECT Pantheon — Brand Design Notes

This file documents the design intent behind the brand kit. For
mechanical integration steps, see `INTEGRATION.md`.

## The lockup

The medallion + wordmark lockup is the canonical brand surface in
product chrome (headers, sidebars, login screens). Three pieces:

1. **Medallion** — the identity. A pantheon mark recognizable at any
   size from a 16px favicon to a 1024px splash.
2. **Wordmark** — the name in Montserrat 700, uppercase, with 3px
   letter-spacing. Legibility at small sizes; the medallion alone is
   not enough to identify an app for users still learning the
   pantheon.
3. **Tagline** (optional) — one short line of context. Use it on
   pages where the surrounding chrome doesn't make the app's
   function obvious. Skip it where it would be redundant.

The lockup as a unit is what the brand kit ships. Apps `<include>` the
partial (or call `render_lockup()`) — they do not hand-roll the markup.

### Wordmark casing

Wordmarks render uppercase via CSS (`text-transform: uppercase` in
`.ect-brand-lockup__name`). Pass the app name in whatever case
makes sense for accessibility — screen readers handle "Mimir" better
than "MIMIR" — and let the stylesheet handle the visual.

### Tagline pattern

Recommended pattern: `"<Function> · <mythological role>"`. Examples:

- HEIMDALL — "QA pipeline · watcher of the bridge"
- HUGINN — "Call attribution · raven of thought"
- MIMIR — "Business intelligence · guardian of the well"

The pattern is not enforced. Apps can opt out (Mimir and Muninn
currently do) or pick whatever copy works for the surface. The goal
is voluntary convergence, not consistency for its own sake.

## When NOT to use the lockup

- **Favicons** — use just the medallion (`favicon/{app}.ico` or
  `png/icon/{app}/{app}_16.png`). The wordmark is illegible at
  16–32px.
- **Splash / loading screens** — use just the icon variant
  (`svg/icon/{app}.svg`) centered on the canvas. The wordmark is
  redundant when the app is the only thing on screen.
- **OS app icons** — use the icon variant (`png/icon/...`). The
  wordmark goes underneath in the OS chrome, not inside the icon.
- **Marketing hero / landing page** — the wordmark + medallion can
  appear separately and at scale. The lockup partial is sized for
  product chrome, not marketing layouts.

## Variant choice in the lockup

The partial defaults to `variant="auto"` — emits both light and
dark medallions, and CSS shows the right one based on the theme
(`:root.light` / `:root.dark` set by `js/theme-toggle.js`). Use
auto unless you have a reason not to.

Override with `variant="light"`, `"dark"`, or `"icon"` when:

- The surface is permanently a single theme regardless of user
  toggle (e.g. Mimir's chat sidebar is always dark).
- The lockup appears in a context where the icon variant is the
  right read (login screens — but consider whether you want a
  lockup at all there; a standalone medallion is usually better).

Don't pass `variant="icon"` inside in-product chrome — it's too
loud. Use light or dark.

## Navigation: app-bar vs sidebar

The pantheon doesn't try to make every app look identical — it
makes them feel like siblings. The app-bar is the strongest signal
of that family resemblance, and it's the right pattern for any
app whose information architecture fits on a top horizontal nav
(roughly: ≤7 primary destinations, no list-primary content area).

**Apps that should use the app-bar partial:**

- Heimdall, Huginn, Muninn, Asgard

**Apps that should NOT:**

- Mimir — its primary nav is the conversation list; a sidebar is
  the right read for a chat surface.
- Future apps that are list-primary (file browser, ticket queue,
  inbox) or have many primary destinations (≥10). Build a sidebar.

The app-bar standardizes:

- Identity (lockup, top-left)
- Primary nav (caller-controlled HTML slot, immediately right of
  the lockup, role-gated by the app)
- A flex spacer (`.ect-app-bar__nav-sep`) pushing system actions
  to the far right
- System actions cluster (theme toggle → user name → logout)

### When to add an item to the primary nav vs to a per-page menu

The primary nav is for destinations a user reaches multiple times
per session. One-shot actions (export, settings page that's edited
rarely, admin entry points) are better as a dropdown / overflow
menu inside the nav, not a top-level link. Heimdall historically
crammed too many items into the primary nav; if you find yourself
adding a 7th or 8th, ask whether some belong in an overflow.

### Active-state convention

Exactly one nav-btn should have `.active` per page. The class is
applied by the caller (the partial doesn't know what page the
user is on). The visual is "filled with `--ect-nav-surface`,
brighter text, normal border" — matches the established
Heimdall/Huginn pattern.

### Theme toggle

Always renders. The button is icon-only — `theme-toggle.js` fills
in `☀ Light` / `☽ Dark` on `DOMContentLoaded`. Don't pre-fill the
label in markup unless you have a reason; the JS will overwrite
it after first paint and an empty button is fine in the meantime.
