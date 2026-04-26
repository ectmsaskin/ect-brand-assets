# Integration Guide

How to consume the ECT brand asset kit from a downstream app.

## Recommended pattern: Git submodule

Add this repository as a submodule of your app at `vendor/ect-brand-assets/`:

```bash
git submodule add <repo-url> vendor/ect-brand-assets
git submodule update --init --recursive
```

Now your code can reference assets at:

```
vendor/ect-brand-assets/svg/light/heimdall.svg
vendor/ect-brand-assets/svg/icon/huginn.svg
vendor/ect-brand-assets/png/icon/yggdrasil/yggdrasil_1024.png
vendor/ect-brand-assets/favicon/mimir.ico
```

## Pinning to a version

Submodules pin to a specific commit. To pin to a tagged release:

```bash
cd vendor/ect-brand-assets
git fetch --tags
git checkout v1.0.0
cd ../..
git add vendor/ect-brand-assets
git commit -m "Pin brand assets to v1.0.0"
```

## Updating when the brand kit evolves

When a new version is released:

```bash
cd vendor/ect-brand-assets
git fetch --tags
git checkout v1.1.0       # or whatever the new version is
cd ../..
git add vendor/ect-brand-assets
git commit -m "Bump brand assets to v1.1.0"
```

Read the `CHANGELOG.md` before bumping a MAJOR version — those contain breaking visual changes.

## Variant rules

Use the right variant for each context. **Do not deviate.**

| Context | Variant | File |
|---|---|---|
| Browser favicon | icon | `favicon/{app}.ico` |
| OS app icon (iOS/Android/desktop) | icon | `png/icon/{app}/{app}_1024.png` (downsize as platform requires) |
| PWA manifest icons | icon | `png/icon/{app}/{app}_{size}.png` |
| Login screen / splash / marketing hero | icon | `svg/icon/{app}.svg` (or 1024 PNG) |
| In-product header / sidebar (light theme) | light | `svg/light/{app}.svg` |
| In-product header / sidebar (dark theme) | dark | `svg/dark/{app}.svg` |
| README hero / docs | light | `svg/light/{app}.svg` |
| Loading / empty state | match theme | corresponding `svg/{variant}/{app}.svg` |
| **Toolbox** parent portal (toolbox.eastcoasttowing.com) | any | `svg/{variant}/asgard.svg` — Asgard is the toolbox's own mark, not a pantheon member |

## Brand colors (CSS variables)

```css
:root {
  --ect-blue:        #214080; /* primary */
  --ect-yellow:      #f3e830; /* accent */
  --ect-yellow-soft: #f6f46f;
  --ect-black:       #231f20;
  --ect-gray-700:    #757575;
  --ect-gray-500:    #acacac;
  --ect-gray-200:    #e4e4e4;
}
```

Typeface: **Montserrat** (semibold for wordmarks, regular for body).

## Wordmark

When pairing the medallion with the app name in a header, navigation, or hero:

```html
<div class="brand-lockup">
  <img src="vendor/ect-brand-assets/svg/light/heimdall.svg" alt="" class="medallion">
  <div class="wordmark">
    <div class="name">HEIMDALL</div>
    <div class="tag">QA pipeline</div>
  </div>
</div>
```

```css
.medallion        { width: 48px; height: 48px; }
.wordmark .name   { font: 700 22px/1 Montserrat; letter-spacing: 3px; color: var(--ect-blue); }
.wordmark .tag    { font: 400 12px/1 Montserrat; color: var(--ect-gray-700); }
```

On dark surfaces, swap medallion to `svg/dark/{app}.svg` and `.name` color to `var(--ect-yellow)`.

## Don't

- Don't recolor the medallions outside the palette.
- Don't use the icon variant inside dense in-product surfaces (it's too loud).
- Don't use the light variant on dark surfaces (low contrast).
- Don't modify the SVG/PNG/ICO files in this repo from a downstream app — submit a PR upstream instead.
- Don't ship just the wordmark without the medallion in primary brand surfaces.

## Regenerating assets (maintainers only)

If you're maintaining this repo and need to change the source designs:

```bash
pip install cairosvg pillow
python3 build_svgs.py        # 18 SVG masters
python3 build_pngs.py        # 126 PNG renders
python3 build_favicons.py    # 6 .ico files
python3 build_reference.py   # HTML reference page
```

Then bump the VERSION file, update CHANGELOG.md, commit, and tag the release.
