# ECT Application Pantheon — Brand Asset Kit

Norse-themed identity system for East Coast Towing's internal applications. Six apps, three color variants each, designed as a unified medallion family.

## The pantheon

| App | Function | Mythological role |
|---|---|---|
| **Heimdall** | QA pipeline | Watcher of the bridge; sees all data crossing into the system |
| **Huginn** | Call attribution | Odin's raven of thought; scouts and reports |
| **Muninn** | Customer knowledge base | Odin's raven of memory; stores and recalls |
| **Bifrost** | Integrations · ETL | Rainbow bridge connecting realms |
| **Yggdrasil** | Data warehouse | World tree; structural foundation of the data realms |
| **Mimir** | Business intelligence | Guardian of the well of wisdom; queried for insight |

Plus the **Asgard** mark — the home of the gods. Used by `asgard.eastcoasttowing.com`, the parent portal that displays the pantheon. Asgard is *not* a pantheon member; it represents the pantheon collectively.

## Three variants per app

- **Light** — blue strokes on neutral surfaces. Use for in-product UI, docs, sidebars, dashboards.
- **Dark** — white strokes with yellow accents on dark surfaces. Use for dark-mode UI, login screens, splash.
- **Icon** — yellow medallion on solid blue. The canonical app icon. Use for app icons, favicons, marketing.

## Folder structure

```
ect_pantheon/
├── README.md                      ← this file
├── BRAND.md                       ← design notes (lockup intent, casing, taglines)
├── INTEGRATION.md                 ← how downstream apps consume this kit
├── CHANGELOG.md                   ← release notes
├── VERSION                        ← single-line version pin
├── svg/
│   ├── light/{app}.svg            ← 6 light-variant masters
│   ├── dark/{app}.svg             ← 6 dark-variant masters
│   └── icon/{app}.svg             ← 6 icon-variant masters (canonical)
├── png/
│   ├── light/{app}/{app}_{size}.png
│   ├── dark/{app}/{app}_{size}.png
│   └── icon/{app}/{app}_{size}.png
│       Sizes: 1024, 512, 256, 128, 64, 32, 16 px
├── favicon/
│   └── {app}.ico                  ← 6 multi-resolution .ico (16/32/48/64/128/256)
├── css/
│   ├── brand-tokens.css           ← canonical CSS variables (v1.2.0+)
│   ├── brand-lockup.css           ← lockup component styling (v1.3.0+)
│   └── brand-appbar.css           ← top app-bar styling (v1.4.0+)
├── js/
│   └── theme-toggle.js            ← shared dark/light toggle (v1.2.0+)
├── templates/
│   ├── lockup.html.j2             ← Jinja partial for the medallion+wordmark lockup
│   └── app-bar.html.j2            ← Jinja partial for the top header (v1.4.0+)
├── python/
│   ├── lockup.py                  ← Python render_lockup() helper
│   └── app_bar.py                 ← Python render_app_bar() helper (v1.4.0+)
├── tests/
│   └── test_lockup_parity.py      ← asserts Jinja and Python emit equivalent HTML
├── reference/
│   └── ect_pantheon_brand_reference.html   ← printable brand reference
└── build_*.py                     ← regeneration scripts
```

## Quick start

- **Need to drop a logo into product UI?** → `svg/light/{app}.svg`
- **Building a dark-mode login screen?** → `svg/dark/{app}.svg`
- **Setting an app icon for iOS / Android / desktop?** → `png/icon/{app}/{app}_1024.png`
- **Setting a browser tab favicon?** → `favicon/{app}.ico`
- **Need a printable brand reference?** → open `reference/ect_pantheon_brand_reference.html` in a browser, then print.

## Brand colors used

| Hex | Use |
|---|---|
| `#214080` | Primary blue (medallion strokes in light variant; icon background) |
| `#f3e830` | Electric yellow (accents everywhere; medallion in icon variant) |
| `#231f20` | Near-black (body text; dark variant background) |
| `#e4e4e4` | Light gray (light variant cell background) |
| `#757575` | Mid gray (taglines, secondary text) |

Typeface: **Montserrat** (semibold for wordmarks, regular for body).

## Regenerating

If you change the source designs in `build_svgs.py`, regenerate everything with:

```bash
python3 build_svgs.py        # writes 18 SVG masters
python3 build_pngs.py        # renders 126 PNGs
python3 build_favicons.py    # builds 6 .ico files
python3 build_reference.py   # builds the HTML reference
```

Requires: `cairosvg`, `pillow` (`pip install cairosvg pillow`).
