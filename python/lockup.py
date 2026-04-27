"""ECT brand-assets v1.3.0 — medallion + wordmark lockup, Python edition.

Mirrors templates/lockup.html.j2 for codebases that render HTML without
Jinja (e.g. ect-qa's f-string layer). Both must be updated together;
tests/test_lockup_parity.py enforces equivalence.
"""
from html import escape


def render_lockup(
    app_key: str,
    app_name: str,
    tagline: str = "",
    variant: str = "auto",
    asset_base: str = "/brand",
    medallion_alt: str = "",
    modifier: str = "",
) -> str:
    base = asset_base.rstrip("/")
    alt = escape(medallion_alt)
    aria = "true" if not medallion_alt else "false"
    name_html = escape(app_name)
    key = escape(app_key)
    cls = "ect-brand-lockup" + (f" {escape(modifier)}" if modifier else "")

    if variant == "auto":
        medallion_html = (
            f'\n  <img class="ect-brand-lockup__medallion ect-brand-lockup__medallion--light" '
            f'src="{base}/svg/light/{key}.svg" alt="{alt}" aria-hidden="{aria}">'
            f'\n  <img class="ect-brand-lockup__medallion ect-brand-lockup__medallion--dark" '
            f'src="{base}/svg/dark/{key}.svg" alt="{alt}" aria-hidden="{aria}">'
        )
    else:
        medallion_html = (
            f'\n  <img class="ect-brand-lockup__medallion" '
            f'src="{base}/svg/{escape(variant)}/{key}.svg" '
            f'alt="{alt}" aria-hidden="{aria}">'
        )

    tag_html = (
        f'\n    <div class="ect-brand-lockup__tag">{escape(tagline)}</div>'
        if tagline else ""
    )

    return (
        f'<div class="{cls}" data-app="{key}">'
        f'{medallion_html}'
        f'\n  <div class="ect-brand-lockup__wordmark">'
        f'\n    <div class="ect-brand-lockup__name">{name_html}</div>'
        f'{tag_html}'
        f'\n  </div>'
        f'\n</div>'
    )
