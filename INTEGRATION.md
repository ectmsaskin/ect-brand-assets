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
| **Asgard** parent portal (asgard.eastcoasttowing.com) | any | `svg/{variant}/asgard.svg` — Asgard is the portal mark, not a pantheon member |

## Brand colors (CSS variables)

As of v1.2.0 the canonical tokens live in **`css/brand-tokens.css`**.
`<link>` it from your `<head>` (via your serving alias for the
submodule path):

```html
<link rel="stylesheet" href="/brand/css/brand-tokens.css">
```

Apps stop redefining these values themselves — the `<link>` is the
single source of truth. The seven tokens, for reference:

```css
--ect-blue:        #214080; /* primary */
--ect-yellow:      #f3e830; /* accent */
--ect-yellow-soft: #f6f46f;
--ect-black:       #231f20;
--ect-gray-700:    #757575;
--ect-gray-500:    #acacac;
--ect-gray-200:    #e4e4e4;
```

Typeface: **Montserrat** (semibold for wordmarks, regular for body).
The `--ect-font-sans` token in `brand-tokens.css` declares it; load
the actual font file via Google Fonts in your `<head>`.

## Theme toggle (dark / light)

As of v1.2.0 the shared theme-toggle script lives at
**`js/theme-toggle.js`**. Drop it into your `<head>`:

```html
<script src="/brand/js/theme-toggle.js"></script>
```

Then anywhere a user can click:

```html
<button id="theme-toggle" onclick="toggleTheme()" type="button">☀ Light</button>
```

The script:
- reads `localStorage.ect-theme` synchronously on load (no flash of
  wrong palette);
- toggles `.light` / `.dark` on `<html>`;
- updates the button label to indicate the **opposite** theme;
- defers to `prefers-color-scheme` when the user hasn't picked.

For the toggle to actually flip colors, your app stylesheet must
provide both branches:

```css
:root.dark   { /* dark values */ }
:root.light  { /* light values */ }
@media (prefers-color-scheme: dark) {
  :root:not(.light) { /* dark values */ }
}
```

The `:not(.light)` clause is what makes the explicit user choice win
over OS preference.

## Lockup (v1.3.0+)

The medallion + wordmark lockup is now a shared partial. Apps stop
hand-rolling the markup — `<include>` the partial (Jinja apps) or call
`render_lockup()` (f-string apps).

Load the companion stylesheet alongside `brand-tokens.css`:

```html
<link rel="stylesheet" href="/brand/css/brand-tokens.css">
<link rel="stylesheet" href="/brand/css/brand-lockup.css">
```

### Jinja apps

Wire the partial directory into the Flask app's loader once:

```python
import jinja2
app.jinja_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader('vendor/ect-brand-assets/templates'),
])
```

Then in any template:

```jinja
{% with app_key="huginn", app_name="HUGINN", tagline="Call attribution · raven of thought" %}
  {% include 'lockup.html.j2' %}
{% endwith %}
```

### f-string / non-Jinja apps

Load `python/lockup.py` from the submodule (the hyphenated path isn't
a valid Python package name, so import via `importlib`):

```python
import importlib.util, pathlib
_path = pathlib.Path(__file__).parent / "vendor" / "ect-brand-assets" / "python" / "lockup.py"
_spec = importlib.util.spec_from_file_location("ect_brand_lockup", _path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
render_lockup = _mod.render_lockup
```

Then interpolate in your HTML f-string:

```python
return f"""<header>{render_lockup("heimdall", "HEIMDALL", "Scorecard Admin")}</header>..."""
```

### Parameters

| Param | Default | Notes |
|---|---|---|
| `app_key` | required | Pantheon key, lowercase: `heimdall`, `huginn`, `muninn`, `mimir`, `bifrost`, `yggdrasil`, `asgard`. |
| `app_name` | required | Wordmark text. CSS uppercases it; pass any case. |
| `tagline` | `""` | Optional secondary line. Empty string suppresses it. |
| `variant` | `"auto"` | `"light"`, `"dark"`, `"icon"`, or `"auto"` (emits both light+dark with CSS theme-swap). |
| `asset_base` | `"/brand"` | URL prefix for SVGs. Override only if you mount the submodule somewhere else. |
| `medallion_alt` | `""` | Alt text. Empty (default) marks the medallion decorative. |
| `modifier` | `""` | Extra class on the lockup container. Use `"ect-brand-lockup--compact"` for sidebars. |

### Class contract (stable across MINOR releases)

```
.ect-brand-lockup
  .ect-brand-lockup__medallion
    .ect-brand-lockup__medallion--light
    .ect-brand-lockup__medallion--dark
  .ect-brand-lockup__wordmark
    .ect-brand-lockup__name
    .ect-brand-lockup__tag

.ect-brand-lockup--compact   /* modifier */
```

Renaming any of these is a MAJOR. Apps may rely on these for overrides.

## App-bar (v1.4.0+)

The app-bar is the canonical top header for the apps that use a top-nav
layout (Heimdall, Huginn, Muninn, Asgard). It composes the lockup,
holds a slot for app-specific primary nav, and standardizes the
theme-toggle / user / logout cluster on the right.

Mimir intentionally does NOT use the app-bar — its sidebar is the
primary nav for a chat-app surface, which doesn't fit a top header.

Load the companion stylesheets (in this order — appbar depends on
both):

```html
<link rel="stylesheet" href="/brand/css/brand-tokens.css">
<link rel="stylesheet" href="/brand/css/brand-lockup.css">
<link rel="stylesheet" href="/brand/css/brand-appbar.css">
```

### Jinja apps

```jinja
{%- set primary_nav_html %}
  <a href="{{ url_for('dashboard.calls') }}" class="nav-btn {% if active=='calls' %}active{% endif %}">Calls</a>
  <a href="{{ url_for('admin.users') }}" class="nav-btn {% if active=='users' %}active{% endif %}">Users</a>
{% endset %}
{% with app_key="huginn", app_name="HUGINN", tagline="Call attribution",
        primary_nav_html=primary_nav_html,
        user_name=current_user.name %}
  {% include 'app-bar.html.j2' %}
{% endwith %}
```

Apps role-gate links inside `primary_nav_html` themselves (with
`{% if user.is_admin %}...{% endif %}`); the partial doesn't try to
read role state.

### f-string apps (Heimdall)

```python
from branding import render_app_bar, build_primary_nav

html = f"""<!DOCTYPE html>
<html>
<head>...</head>
<body>
{render_app_bar(
    app_key='heimdall',
    app_name='HEIMDALL',
    tagline='Scorecard Admin',
    primary_nav_html=build_primary_nav(active='scorecard'),
    user_name=g.user.name,
)}
<main>...</main>
</body></html>
"""
```

### Parameters

| Param | Default | Notes |
|---|---|---|
| `app_key` | required | Pantheon key (passes through to lockup). |
| `app_name` | required | Wordmark text (passes through to lockup). |
| `tagline` | `""` | Lockup tagline. |
| `variant` | `"auto"` | Lockup variant. |
| `asset_base` | `"/brand"` | Lockup asset URL prefix. |
| `primary_nav_html` | `""` | Pre-rendered HTML for the nav slot. Caller is responsible for HTML-escaping any user-supplied content inside. |
| `user_name` | `""` | When non-empty, renders user span + Logout link. |
| `logout_href` | `"/auth/logout"` | Logout URL. |
| `theme_toggle_label` | `""` | Default text shown before theme-toggle.js sets it. Empty is fine — JS fills it on `DOMContentLoaded`. |

### Class contract

```
.ect-app-bar
  (lockup goes here)
  .ect-app-bar__nav
    (caller's primary_nav_html with .nav-btn anchors)
    .ect-app-bar__nav-sep    /* flex spacer pushing user info right */
    button#theme-toggle.nav-btn.action
    .ect-app-bar__user
    a.nav-btn                /* Logout */
```

`.nav-btn` styling lives in `brand-appbar.css` and is consistent
across all apps using the partial. Modifiers `.active` (filled
surface bg) and `.action` (transparent bg, used for icon-only
toggle) are stable and load-bearing.

### Theme-aware tokens

`brand-tokens.css` v1.4.0 added `--ect-nav-text`, `--ect-nav-text-bright`,
`--ect-nav-border`, `--ect-nav-surface`, `--ect-nav-bg` semantic tokens.
They're driven by `:root.light` / `:root.dark` (set by theme-toggle.js)
with `prefers-color-scheme` as fallback. Apps don't need to define these —
they inherit them from `brand-tokens.css`.

## Impersonation banner (v1.5.0+)

When a super-admin uses Asgard to impersonate another user, Asgard's
`/auth/verify` adds an `X-Impersonated-By: <super_admin_email>` header.
nginx forwards this to the sibling app via the
`asgard-{auth-request,proxy-headers}.conf` snippets.

Sibling apps render a sticky yellow banner at the top of every page so
the super-admin can see they're not viewing as themselves. The banner
auto-renders only when the header is present; invisible during normal
use.

### Loading

```html
<link rel="stylesheet" href="/brand/css/brand-tokens.css">
<link rel="stylesheet" href="/brand/css/brand-impersonation.css">
```

### Jinja apps

```jinja
{% include 'impersonation-banner.html.j2' %}
```

The partial reads `request.headers` directly and `current_user` from
Flask-Login — no extra context needed. Place it at the very top of
`<body>`, above the app-bar.

### f-string apps (Heimdall)

```python
from branding import render_impersonation_banner

html = f"""<!DOCTYPE html>
<html>...
<body>
{render_impersonation_banner(
    impersonated_by=request.headers.get('X-Impersonated-By', ''),
    current_user_email=g.user['email'] if g.user else '',
)}
{render_app_bar(...)}
..."""
```

### Parameters

| Param | Default | Notes |
|---|---|---|
| `impersonated_by` | required | the X-Impersonated-By header value; empty = render nothing |
| `current_user_email` | `""` | the impersonated target's email (for display) |
| `asgard_admin_url` | Asgard prod | where the "Stop in Asgard" link points |

### Class contract

```
.ect-impersonation-banner
  span (text)
    strong (highlighted emails)
  .ect-impersonation-banner__link  /* "Stop in Asgard" */
```

### nginx requirement

The header only reaches sibling Flask apps if nginx is configured to
forward it. The shared snippet pattern adds:

```nginx
# /etc/nginx/snippets/asgard-auth-request.conf
auth_request_set $impersonated_by $upstream_http_x_impersonated_by;

# /etc/nginx/snippets/asgard-proxy-headers.conf
proxy_set_header X-Impersonated-By $impersonated_by;
```

Apps that don't include those snippets won't see the header and the
banner will silently never render.

## Don't

- Don't recolor the medallions outside the palette.
- Don't use the icon variant inside dense in-product surfaces (it's too loud).
- Don't use the light variant on dark surfaces (low contrast).
- Don't modify the SVG/PNG/ICO files in this repo from a downstream app — submit a PR upstream instead.
- Don't ship just the wordmark without the medallion in primary brand surfaces.

## Fleet management (multi-app teams)

If you're applying this brand kit across many apps, the per-app
INTEGRATION steps above stop scaling: keeping every app on the same
pinned version, auditing compliance, and onboarding new apps becomes
its own problem. We recommend a small meta-infrastructure layer
that sits *above* the consuming repos, not inside any of them.

Reference layout — at the working root that contains all app repos
as siblings, create a `.ect-brand/` directory with:

```
.ect-brand/
  STANDARDS.md                           # written compliance rubric
  PANTHEON.md                            # canonical slug manifest
  README.md                              # how to add a new app, how to bump
  templates/
    BRAND.md.template                    # per-app drop-in
    brand-tokens.css                     # canonical CSS variables
    ci-github-brand-submodule.yml        # CI guard for submodule consumers
    ci-github-brand-copied.yml           # CI guard for static-bundle consumers
  scripts/
    scaffold-brand.sh                    # one-command onboarding
    audit-brand.sh                       # programmatic compliance check
```

`scaffold-brand.sh <slug>` validates the slug against PANTHEON.md,
adds this repo as a submodule at `vendor/ect-brand-assets`, pins it
to the latest tag, drops a populated `BRAND.md`, and commits on a
`brand/initial` branch. `audit-brand.sh` walks every Git repo at the
working root and reports a Markdown table of pass/fail per check, per
app — exits non-zero on any drift, with a `--quiet` mode for CI.

The meta layer is **shared dev tooling**, not app code — don't vendor
`.ect-brand/` into any individual app's repo. The point of separating
the meta layer from the apps is that fleet-wide bumps become a
one-line loop (`for d in */; do (cd "$d" && git submodule update
--remote vendor/ect-brand-assets); done`), and compliance is a single
audit run.

The ECT team's reference implementation lives at `/opt/.ect-brand/`
on their deploy host. Borrow the templates and scripts as a starting
point — they're not ECT-specific beyond the SSH remote URL and slug
list.

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
