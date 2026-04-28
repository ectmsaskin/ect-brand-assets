"""Parity check between Jinja partials and Python helpers.

Both must emit identical HTML for the same inputs (modulo whitespace).
If this test fails, sync templates/*.j2 and python/*.py.

Usage:
    python3 tests/test_lockup_parity.py        # direct script run
    python3 -m pytest tests/                   # via pytest if available
"""
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from jinja2 import Environment, FileSystemLoader
from python.lockup import render_lockup
from python.app_bar import render_app_bar
from python.impersonation_banner import render_impersonation_banner


def _normalize(html: str) -> str:
    """Collapse whitespace runs to single spaces, drop whitespace between tags."""
    html = re.sub(r"\s+", " ", html).strip()
    html = re.sub(r">\s+<", "><", html)
    return html


LOCKUP_CASES = [
    {"app_key": "heimdall", "app_name": "HEIMDALL"},
    {"app_key": "heimdall", "app_name": "HEIMDALL", "tagline": "QA pipeline"},
    {"app_key": "huginn", "app_name": "HUGINN", "variant": "light"},
    {"app_key": "mimir", "app_name": "MIMIR", "variant": "dark"},
    {"app_key": "asgard", "app_name": "ASGARD", "tagline": "East Coast Towing"},
    {"app_key": "muninn", "app_name": "MUNINN", "modifier": "ect-brand-lockup--compact"},
    {"app_key": "heimdall", "app_name": "HEIMDALL", "medallion_alt": "Heimdall logo"},
    {"app_key": "heimdall", "app_name": "HEIMDALL", "asset_base": "/brand/"},
]

APPBAR_CASES = [
    {"app_key": "heimdall", "app_name": "HEIMDALL", "tagline": "Scorecard Admin"},
    {
        "app_key": "huginn", "app_name": "HUGINN",
        "tagline": "Call attribution",
        "primary_nav_html": '<a href="/calls" class="nav-btn active">Calls</a>',
        "user_name": "Mike Saskin",
    },
    {
        "app_key": "asgard", "app_name": "ASGARD",
        "tagline": "East Coast Towing",
        "user_name": "Mike Saskin",
        "logout_href": "/auth/logout",
    },
    {
        "app_key": "muninn", "app_name": "MUNINN",
        "primary_nav_html": '<a href="/accounts" class="nav-btn">Accounts</a><a href="/users" class="nav-btn">Users</a>',
        "user_name": "Mike Saskin",
        "theme_toggle_label": "☀ Light",
    },
]


def _env():
    return Environment(
        loader=FileSystemLoader(str(ROOT / "templates")),
        keep_trailing_newline=False,
    )


def test_lockup_parity():
    env = _env()
    template = env.get_template("lockup.html.j2")
    for kwargs in LOCKUP_CASES:
        jinja_html = template.render(**kwargs)
        python_html = render_lockup(**kwargs)
        assert _normalize(jinja_html) == _normalize(python_html), (
            f"\n  case:   {kwargs}"
            f"\n  JINJA:  {_normalize(jinja_html)!r}"
            f"\n  PYTHON: {_normalize(python_html)!r}"
        )


def test_appbar_parity():
    env = _env()
    template = env.get_template("app-bar.html.j2")
    for kwargs in APPBAR_CASES:
        jinja_html = template.render(**kwargs)
        python_html = render_app_bar(**kwargs)
        assert _normalize(jinja_html) == _normalize(python_html), (
            f"\n  case:   {kwargs}"
            f"\n  JINJA:  {_normalize(jinja_html)!r}"
            f"\n  PYTHON: {_normalize(python_html)!r}"
        )


def test_html_escaping():
    """Caller-supplied values must be HTML-escaped to prevent injection."""
    out = render_lockup(
        app_key="x", app_name='HEIM<script>alert(1)</script>DALL',
        tagline='Tag with "quotes" & ampersand',
    )
    assert "<script>" not in out, "raw <script> tag leaked through"
    assert "&lt;script&gt;" in out, "expected escaped <script>"
    assert "&amp;" in out, "expected escaped ampersand"
    assert "&quot;" in out, "expected escaped quote"

    # primary_nav_html is interpolated raw (caller's responsibility), but
    # user_name and theme_toggle_label must be escaped by the helper.
    out = render_app_bar(
        app_key="x", app_name="X",
        primary_nav_html='<a href="/x">link</a>',
        user_name='Bob<script>alert(1)</script>',
        theme_toggle_label='Light & Dark',
    )
    assert '<a href="/x">link</a>' in out, "primary_nav_html should pass through"
    assert "Bob<script>" not in out, "user_name not escaped"
    assert "&lt;script&gt;" in out, "expected escaped script in user_name"
    assert "Light &amp; Dark" in out, "theme_toggle_label not escaped"


IMPERSONATION_CASES = [
    {"impersonated_by": "", "current_user_email": ""},  # not impersonating — empty
    {
        "impersonated_by": "msaskin@eastcoasttowing.com",
        "current_user_email": "rvarner@eastcoasttowing.com",
    },
    {
        "impersonated_by": "boss@eastcoasttowing.com",
        "current_user_email": "intern@eastcoasttowing.com",
        "asgard_admin_url": "https://asgard.example.com/admin/users",
    },
]


def test_impersonation_banner_parity():
    env = _env()
    template = env.get_template("impersonation-banner.html.j2")
    for kwargs in IMPERSONATION_CASES:
        # Jinja partial reads from request.headers — simulate via a dict.
        class _Req:
            def __init__(self, headers):
                self.headers = headers

        class _User:
            def __init__(self, email):
                self.email = email
                self.is_authenticated = bool(email)

        render_kwargs = {
            "request": _Req({"X-Impersonated-By": kwargs["impersonated_by"]}),
            "current_user": _User(kwargs["current_user_email"]),
        }
        if "asgard_admin_url" in kwargs:
            render_kwargs["asgard_admin_url"] = kwargs["asgard_admin_url"]
        jinja_html = template.render(**render_kwargs)
        py_kwargs = {k: v for k, v in kwargs.items() if v != ""}
        if "impersonated_by" not in py_kwargs:
            py_kwargs["impersonated_by"] = ""
        if "current_user_email" not in py_kwargs:
            py_kwargs["current_user_email"] = ""
        python_html = render_impersonation_banner(**py_kwargs)
        assert _normalize(jinja_html) == _normalize(python_html), (
            f"\n  case:   {kwargs}"
            f"\n  JINJA:  {_normalize(jinja_html)!r}"
            f"\n  PYTHON: {_normalize(python_html)!r}"
        )


def test_impersonation_banner_escaping():
    """Both arms must HTML-escape user-controlled values."""
    out = render_impersonation_banner(
        impersonated_by='evil@example.com<script>alert(1)</script>',
        current_user_email='target@example.com" onclick="x',
    )
    assert "<script>" not in out
    assert "&lt;script&gt;" in out
    assert "&quot;" in out


if __name__ == "__main__":
    test_lockup_parity()
    test_appbar_parity()
    test_impersonation_banner_parity()
    test_html_escaping()
    test_impersonation_banner_escaping()
    print(f"OK — {len(LOCKUP_CASES)} lockup + {len(APPBAR_CASES)} app-bar + "
          f"{len(IMPERSONATION_CASES)} impersonation parity cases + escaping checks passed")
