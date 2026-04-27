# Changelog

All notable changes to the ECT brand asset kit are documented here.

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** — breaking visual change (e.g., medallion frame redesigned, palette swap). Downstream apps will look different.
- **MINOR** — new app added to the pantheon, new variant added, new file format. Backward compatible.
- **PATCH** — visual refinement to an existing mark, color tweak within tolerance, file regeneration with no design change.

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
