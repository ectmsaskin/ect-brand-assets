"""Parity check between the Jinja partial and the Python helper.

Both must emit identical HTML for the same inputs (modulo whitespace).
If this test fails, sync templates/lockup.html.j2 and python/lockup.py.

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


def _normalize(html: str) -> str:
    """Collapse runs of whitespace to single spaces and trim."""
    return re.sub(r"\s+", " ", html).strip()


CASES = [
    {"app_key": "heimdall", "app_name": "HEIMDALL"},
    {"app_key": "heimdall", "app_name": "HEIMDALL", "tagline": "QA pipeline"},
    {"app_key": "huginn", "app_name": "HUGINN", "variant": "light"},
    {"app_key": "mimir", "app_name": "MIMIR", "variant": "dark"},
    {"app_key": "asgard", "app_name": "ASGARD", "tagline": "East Coast Towing"},
    {"app_key": "muninn", "app_name": "MUNINN", "modifier": "ect-brand-lockup--compact"},
    {"app_key": "heimdall", "app_name": "HEIMDALL", "medallion_alt": "Heimdall logo"},
    {"app_key": "heimdall", "app_name": "HEIMDALL", "asset_base": "/brand/"},
]


def _env():
    return Environment(
        loader=FileSystemLoader(str(ROOT / "templates")),
        keep_trailing_newline=False,
    )


def test_jinja_python_parity():
    env = _env()
    template = env.get_template("lockup.html.j2")
    for kwargs in CASES:
        jinja_html = template.render(**kwargs)
        python_html = render_lockup(**kwargs)
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


if __name__ == "__main__":
    test_jinja_python_parity()
    test_html_escaping()
    print(f"OK — {len(CASES)} parity cases + escaping check passed")
