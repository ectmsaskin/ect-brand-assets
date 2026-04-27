# Changelog

All notable changes to the ECT brand asset kit are documented here.

This project follows [Semantic Versioning](https://semver.org/):
- **MAJOR** — breaking visual change (e.g., medallion frame redesigned, palette swap). Downstream apps will look different.
- **MINOR** — new app added to the pantheon, new variant added, new file format. Backward compatible.
- **PATCH** — visual refinement to an existing mark, color tweak within tolerance, file regeneration with no design change.

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
