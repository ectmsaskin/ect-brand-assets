"""ECT brand-assets v1.4.0 — top app-bar, Python edition.

Mirrors templates/app-bar.html.j2 for codebases that render HTML without
Jinja (e.g. ect-qa's f-string layer). Both must be updated together;
tests/test_lockup_parity.py enforces equivalence.
"""
from html import escape

from .lockup import render_lockup


def render_app_bar(
    app_key: str,
    app_name: str,
    tagline: str = "",
    variant: str = "auto",
    asset_base: str = "/brand",
    primary_nav_html: str = "",
    user_name: str = "",
    logout_href: str = "/auth/logout",
    theme_toggle_label: str = "",
) -> str:
    """Render the canonical ECT app-bar header as an HTML string.

    primary_nav_html is interpolated raw (the caller is responsible for
    escaping any user-supplied content inside it). user_name and
    logout_href are escaped here.
    """
    lockup = render_lockup(
        app_key=app_key,
        app_name=app_name,
        tagline=tagline,
        variant=variant,
        asset_base=asset_base,
    )

    nav_block = f'\n    {primary_nav_html}' if primary_nav_html else ''

    user_block = ""
    if user_name:
        user_block = (
            f'\n    <span class="ect-app-bar__user">{escape(user_name)}</span>'
            f'\n    <a href="{escape(logout_href)}" class="nav-btn">Logout</a>'
        )

    return (
        f'<header class="ect-app-bar">'
        f'\n  {lockup}'
        f'\n  <div class="ect-app-bar__nav">'
        f'{nav_block}'
        f'\n    <span class="ect-app-bar__nav-sep"></span>'
        f'\n    <button id="theme-toggle" class="nav-btn action" onclick="toggleTheme()" type="button">{escape(theme_toggle_label)}</button>'
        f'{user_block}'
        f'\n  </div>'
        f'\n</header>'
    )
