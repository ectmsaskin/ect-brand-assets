# Changelog

All notable changes to the ECT brand asset kit are documented here.

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** — breaking visual change (e.g., medallion frame redesigned, palette swap). Downstream apps will look different.
- **MINOR** — new app added to the pantheon, new variant added, new file format. Backward compatible.
- **PATCH** — visual refinement to an existing mark, color tweak within tolerance, file regeneration with no design change.

## [1.6.0] — 2026-05-02

### Changed
- **`css/brand-appbar.css` — `.nav-btn` restyled to highlight-on-hover.**
  Default state has a transparent border (was a 1px outline against
  `--ect-nav-border`). Hover paints the background to a new
  `--ect-nav-hover-bg` token. `.active` paints to `--ect-nav-border`,
  giving active links a stronger paint than hover.
  - `.nav-btn.action` (theme-toggle / logout) keeps a subtle border so
    it still reads as an icon-style button rather than a text link.
  - Class API is unchanged — every existing `<a class="nav-btn">` keeps
    working. The visual change is the hover treatment.

### Added
- **`--ect-nav-hover-bg` token** (`css/brand-tokens.css`) — subtler
  highlight color paired with `--ect-nav-border` for the new
  hover/active paint pattern. Defined for both `:root` (dark) and
  `:root.light` and the `prefers-color-scheme: light` media query.
- **`.nav-group` / `.nav-group-label` classes** (`css/brand-appbar.css`)
  — optional infrastructure for apps that want to split the primary
  nav into labeled clusters (e.g. Heimdall's Operate / Admin / Docs
  split). Apps opt in by wrapping `<a class="nav-btn">` anchors inside
  `<div class="nav-group">` with a leading
  `<span class="nav-group-label">`. Groups separate by
  `margin-left: 12px` between adjacent groups.

### Class contract
The `.nav-group`, `.nav-group-label`, and `--ect-nav-hover-bg` names
are now stable. Renames are MAJOR.

### Notes
- Backward compatible at the class-API level — no class names removed
  or renamed. Visual presentation does change for any app that bumps
  the submodule pin and renders `<a class="nav-btn">` inside an
  `.ect-app-bar`. Each app opts in deliberately by bumping its
  vendored pin to v1.6.0.
- The new highlight-on-hover style aligns with the Heimdall redesign
  mockup (`docs/design/heimdall-redesign.html` in the Heimdall repo)
  and is the recommended direction for the rest of the pantheon.

## [1.5.0] — 2026-04-27

### Added
- **`templates/impersonation-banner.html.j2`** — sticky yellow banner
  shown when the current request carries an `X-Impersonated-By` header
  (set by Asgard's `/auth/verify` when a super-admin is impersonating).
  Renders nothing when the header is absent. Reads
  `request.headers` directly; no extra context required.
- **`python/impersonation_banner.py`** — `render_impersonation_banner()`
  helper for f-string apps. Caller passes the header value + current
  user's email; returns the banner HTML or empty string.
- **`css/brand-impersonation.css`** — companion stylesheet defining
  the `.ect-impersonation-banner` class tree. Apps `<link>` it after
  `brand-tokens.css`.
- Extended `tests/test_lockup_parity.py` with 3 impersonation parity
  cases + escaping check.

### Class contract
The `.ect-impersonation-banner` and `.ect-impersonation-banner__link`
classes are now stable. Renames are MAJOR.

### Notes
- Backward compatible: additive only. Apps on v1.4.0 can bump freely.
  The banner only renders when an impersonation session is active —
  invisible during normal use.
- Asgard's existing custom banner (added when impersonation shipped)
  consolidates onto the shared partial in this release.

## [1.4.0] — 2026-04-26

### Added
- **`templates/app-bar.html.j2`** — shared Jinja2 partial for the canonical
  top header (Heimdall, Huginn, Muninn, Asgard). Composes the lockup,
  holds a `primary_nav_html` slot, then `nav-sep` + theme-toggle + user
  + logout cluster on the right.
- **`python/app_bar.py`** — `render_app_bar()` Python helper for f-string
  apps (Heimdall). Caller assembles the primary nav HTML separately.
- **`css/brand-appbar.css`** — companion stylesheet defining the
  `.ect-app-bar` class tree and the canonical `.nav-btn` styling
  (`.active` and `.action` modifiers stable).
- **Theme-aware semantic tokens** added to `brand-tokens.css`:
  `--ect-nav-text`, `--ect-nav-text-bright`, `--ect-nav-border`,
  `--ect-nav-surface`, `--ect-nav-bg`. Driven by `:root.light` /
  `:root.dark` with `prefers-color-scheme` fallback.
- Extended `tests/test_lockup_parity.py` with 4 app-bar parity cases +
  escaping checks for `user_name` / `theme_toggle_label`.

### Class contract
The `.ect-app-bar` / `.ect-app-bar__nav` / `.ect-app-bar__nav-sep` /
`.ect-app-bar__user` tree, plus `.nav-btn` / `.nav-btn.active` /
`.nav-btn.action` inside it, are now stable. Renames are MAJOR.

### Notes
- Mimir is intentionally NOT migrated to the app-bar — its sidebar
  layout is its primary nav and doesn't fit a top header. The
  partial is for top-nav apps only.
- Backward compatible: no existing files moved or renamed. Apps on
  v1.3.0 can bump freely; lockup-only consumers don't pick up the
  app-bar unless they `<link>` `brand-appbar.css`.
- Apps adopting the app-bar should default to dark `:root` (with
  `:root.light` overrides) to align with the new `--ect-nav-*` token
  defaults. Muninn was the only outlier and gets aligned during its
  v1.4.0 migration.

## [1.3.0] — 2026-04-26

### Added
- **`templates/lockup.html.j2`** — shared Jinja2 partial for the
  canonical medallion + wordmark lockup. Apps `{% include %}` it
  instead of hand-rolling `<div class="logo">` markup. Parameters:
  `app_key`, `app_name`, `tagline`, `variant`, `asset_base`,
  `medallion_alt`, `modifier`.
- **`python/lockup.py`** — `render_lockup()` Python helper that emits
  the same HTML contract for codebases that don't use Jinja
  (currently ect-qa). Both must be updated together.
- **`css/brand-lockup.css`** — companion stylesheet defining the
  `.ect-brand-lockup` class tree, theme-swap behavior, and a
  `--compact` modifier. Apps `<link>` it after `brand-tokens.css`.
- **`BRAND.md`** — design notes documenting lockup intent, wordmark
  casing convention, tagline pattern, and "when not to use the lockup."
- **`tests/test_lockup_parity.py`** — asserts the Jinja partial and
  Python helper emit equivalent HTML across 8 cases + verifies HTML
  escaping. Runnable as a plain script (no pytest required).

### Class contract
The `.ect-brand-lockup` class tree (`__medallion`, `__wordmark`,
`__name`, `__tag`, `--light`, `--dark`, `--compact`) is now stable.
Renaming any of these is MAJOR.

### Notes
- Backward compatible: no existing files moved or renamed. Apps on
  v1.2.0 can bump freely; lockup files are additive.
- The `.ect-wordmark` / `.ect-wordmark__tag` rules in `brand-tokens.css`
  (added v1.2.0, never adopted) are deprecated in favor of
  `.ect-brand-lockup__name` / `__tag`. Removal targeted for v2.0.0.

## [1.2.0] — 2026-04-26

### Added
- **`css/brand-tokens.css`** — the seven canonical palette variables
  (`--ect-blue`, `--ect-yellow`, `--ect-yellow-soft`, `--ect-black`,
  `--ect-gray-700`, `--ect-gray-500`, `--ect-gray-200`) plus
  Montserrat as the canonical sans + a small set of semantic aliases
  (`--ect-color-text-primary` etc.). Apps `<link>` this from the
  submodule and stop redefining the tokens in their own stylesheets.
- **`js/theme-toggle.js`** — extracted shared theme-toggle script.
  Adds `.light` / `.dark` to `<html>` based on localStorage, with
  `prefers-color-scheme` as a fallback. Apps `<script src=...>` it
  instead of copy-pasting the same JS into every base.html.

### Notes
- Backward compatible: no existing files moved or renamed. Apps on
  v1.1.0 can bump freely; the new files are additive.
- The `<button id="theme-toggle">` element is the contract — name your
  toggle that ID and the script wires up automatically.

## [1.1.0] — 2026-04-26

### Added
- **Asgard medallion** — the portal mark. Central citadel keep + six realm orbs in hexagonal halo, representing the home of the pantheon. Used by `asgard.eastcoasttowing.com` and any future parent surface that represents the pantheon collectively.
- 3 new SVG masters (`svg/{light,dark,icon}/asgard.svg`).
- 21 new PNG renders for Asgard at all 7 sizes across all 3 variants.
- 1 new multi-resolution `.ico` favicon (`favicon/asgard.ico`).
- Asgard section in the brand reference HTML, clearly labeled as the portal mark (not a pantheon member).

### Notes
- Asgard is **not** a pantheon app. Don't include it in app directory grids alongside Heimdall/Huginn/etc. — it represents the directory.
- Backward compatible: no existing files renamed or removed. v1.0.0 consumers can bump freely.

## [1.0.0] — 2026-04-26

### Added
- Initial pantheon: Heimdall, Huginn, Muninn, Bifrost, Yggdrasil, Mimir.
- Three variants per app: light (blue strokes on neutral), dark (white strokes on dark with yellow accents), icon (yellow medallion on solid blue).
- 18 SVG masters at 1024×1024.
- 126 PNG renders (7 sizes × 6 apps × 3 variants).
- 6 multi-resolution `.ico` favicons.
- Printable HTML brand reference page combining all variants, wordmark lockups, palette, and usage guide.
- Build scripts for regenerating SVGs, PNGs, favicons, and reference page.
- Wordmark lockup design pattern (medallion + Montserrat 700 wordmark).
