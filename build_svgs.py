"""Generate 18 standalone SVG files for the ECT Norse pantheon.
6 apps x 3 variants (light, dark, icon).
"""
from pathlib import Path

OUT = Path(__file__).parent / "svg"

APPS = ["heimdall", "huginn", "muninn", "bifrost", "yggdrasil", "mimir", "asgard"]

DESCRIPTIONS = {
    "heimdall": "QA pipeline. Almond eye watching from the bridge.",
    "huginn": "Call attribution. Raven facing left, gathering signals.",
    "muninn": "Customer knowledge base. Raven facing right, holding memory.",
    "bifrost": "Integrations and ETL. Three nested arches of the rainbow bridge.",
    "yggdrasil": "Data warehouse. Stylized world tree with realm orbs.",
    "mimir": "Business intelligence. Chalice of wisdom from the well.",
    "asgard": "Asgard. Central citadel surrounded by six realm orbs — the home of the pantheon.",
}

VARIANTS = {
    "light": {
        "stroke": "#214080",
        "accent": "#f3e830",
        "ring_inner_op": "0.6",
        "bg": None,  # transparent
        "eye_fill": "#e4e4e4",  # behind Heimdall pupil
    },
    "dark": {
        "stroke": "#e4e4e4",
        "accent": "#f3e830",
        "ring_inner_op": "0.5",
        "bg": None,
        "eye_fill": "#231f20",
    },
    "icon": {
        "stroke": "#f3e830",
        "accent": "#ffffff",
        "ring_inner_op": "0.55",
        "bg": "#214080",
        "eye_fill": "#214080",
    },
}


def medallion_frame(stroke, accent, ring_inner_op):
    return f'''
    <circle cx="0" cy="0" r="52" fill="none" stroke="{stroke}" stroke-width="2"/>
    <circle cx="0" cy="0" r="44" fill="none" stroke="{stroke}" stroke-width="0.6" opacity="{ring_inner_op}"/>
    <g stroke="{stroke}" stroke-width="1.6" fill="none">
      <path d="M 0 -48 C -14 -38 -14 -28 0 -22 C 14 -28 14 -38 0 -48"/>
      <path d="M 48 0 C 38 -14 28 -14 22 0 C 28 14 38 14 48 0"/>
      <path d="M 0 48 C 14 38 14 28 0 22 C -14 28 -14 38 0 48"/>
      <path d="M -48 0 C -38 14 -28 14 -22 0 C -28 -14 -38 -14 -48 0"/>
    </g>
    <circle cx="0" cy="-32" r="2.5" fill="{accent}"/>
    <circle cx="32" cy="0" r="2.5" fill="{accent}"/>
    <circle cx="0" cy="32" r="2.5" fill="{accent}"/>
    <circle cx="-32" cy="0" r="2.5" fill="{accent}"/>'''


def heimdall_center(stroke, accent, eye_fill):
    return f'''
    <path d="M -22 0 Q 0 -14 22 0 Q 0 14 -22 0 Z" fill="{eye_fill}" stroke="{stroke}" stroke-width="2.2" stroke-linejoin="round"/>
    <circle cx="0" cy="0" r="6.5" fill="{stroke}"/>
    <circle cx="1.5" cy="-1.5" r="2.2" fill="{accent}"/>'''


def huginn_center(stroke, accent):
    # Raven facing left
    return f'''
    <ellipse cx="2" cy="3" rx="14" ry="8" fill="{stroke}"/>
    <path d="M 12 -2 L 22 -4 L 20 8 Z" fill="{stroke}"/>
    <circle cx="-10" cy="-3" r="7" fill="{stroke}"/>
    <path d="M -16 -4 L -26 -2 L -16 2 Z" fill="{stroke}"/>
    <circle cx="-10" cy="-4" r="1.6" fill="{accent}"/>'''


def muninn_center(stroke, accent):
    # Raven facing right (mirror of Huginn)
    return f'''
    <ellipse cx="-2" cy="3" rx="14" ry="8" fill="{stroke}"/>
    <path d="M -12 -2 L -22 -4 L -20 8 Z" fill="{stroke}"/>
    <circle cx="10" cy="-3" r="7" fill="{stroke}"/>
    <path d="M 16 -4 L 26 -2 L 16 2 Z" fill="{stroke}"/>
    <circle cx="10" cy="-4" r="1.6" fill="{accent}"/>'''


def bifrost_center(stroke, accent):
    # Three pronounced arches with anchor dots
    return f'''
    <path d="M -26 18 Q 0 -22 26 18" stroke="{stroke}" stroke-width="3.5" fill="none" stroke-linecap="round"/>
    <path d="M -19 18 Q 0 -13 19 18" stroke="{stroke}" stroke-width="3" fill="none" stroke-linecap="round"/>
    <path d="M -12 18 Q 0 -4 12 18" stroke="{stroke}" stroke-width="2.6" fill="none" stroke-linecap="round"/>
    <circle cx="-26" cy="18" r="4" fill="{accent}"/>
    <circle cx="26" cy="18" r="4" fill="{accent}"/>'''


def yggdrasil_center(stroke, accent, eye_fill):
    # Stylized world tree: thick trunk, 3 branches up, 3 roots down, 6 realm orbs, prominent center
    return f'''
    <rect x="-3.5" y="-9" width="7" height="18" rx="1.5" fill="{stroke}"/>
    <path d="M -3 -9 Q -10 -14 -18 -20" stroke="{stroke}" stroke-width="2.8" fill="none" stroke-linecap="round"/>
    <path d="M 0 -9 L 0 -20" stroke="{stroke}" stroke-width="2.8" fill="none" stroke-linecap="round"/>
    <path d="M 3 -9 Q 10 -14 18 -20" stroke="{stroke}" stroke-width="2.8" fill="none" stroke-linecap="round"/>
    <path d="M -3 9 Q -10 14 -18 20" stroke="{stroke}" stroke-width="2.8" fill="none" stroke-linecap="round"/>
    <path d="M 0 9 L 0 20" stroke="{stroke}" stroke-width="2.8" fill="none" stroke-linecap="round"/>
    <path d="M 3 9 Q 10 14 18 20" stroke="{stroke}" stroke-width="2.8" fill="none" stroke-linecap="round"/>
    <circle cx="-18" cy="-20" r="3.5" fill="{accent}"/>
    <circle cx="0" cy="-20" r="4" fill="{accent}"/>
    <circle cx="18" cy="-20" r="3.5" fill="{accent}"/>
    <circle cx="-18" cy="20" r="3.5" fill="{accent}"/>
    <circle cx="0" cy="20" r="4" fill="{accent}"/>
    <circle cx="18" cy="20" r="3.5" fill="{accent}"/>
    <circle cx="0" cy="0" r="5.5" fill="{eye_fill}" stroke="{stroke}" stroke-width="2"/>
    <circle cx="0" cy="0" r="2.2" fill="{accent}"/>'''


def mimir_center(stroke, accent, eye_fill):
    # Chalice of wisdom
    return f'''
    <path d="M -15 -16 L -10 4 L 10 4 L 15 -16 Z" fill="{stroke}"/>
    <ellipse cx="0" cy="-16" rx="15" ry="4" fill="{eye_fill}" stroke="{stroke}" stroke-width="1.8"/>
    <circle cx="0" cy="-15" r="3" fill="{accent}"/>
    <rect x="-3" y="4" width="6" height="10" fill="{stroke}"/>
    <ellipse cx="0" cy="16" rx="11" ry="3.5" fill="{stroke}"/>'''


def asgard_center(stroke, accent, eye_fill):
    # Citadel keep + six realm orbs in hexagonal halo
    return f'''
    <circle cx="-11" cy="-19" r="3" fill="{accent}"/>
    <circle cx="11" cy="-19" r="3" fill="{accent}"/>
    <circle cx="22" cy="0" r="3" fill="{accent}"/>
    <circle cx="11" cy="19" r="3" fill="{accent}"/>
    <circle cx="-11" cy="19" r="3" fill="{accent}"/>
    <circle cx="-22" cy="0" r="3" fill="{accent}"/>
    <rect x="-13" y="9" width="26" height="3" rx="1" fill="{stroke}"/>
    <rect x="-5" y="-13" width="10" height="22" fill="{stroke}"/>
    <path d="M -7 -13 L 0 -22 L 7 -13 Z" fill="{stroke}"/>
    <rect x="-2" y="4" width="4" height="5" fill="{eye_fill}"/>
    <rect x="-1" y="-7" width="2" height="4" fill="{eye_fill}"/>'''


CENTERS = {
    "heimdall": lambda v: heimdall_center(v["stroke"], v["accent"], v["eye_fill"]),
    "huginn": lambda v: huginn_center(v["stroke"], v["accent"]),
    "muninn": lambda v: muninn_center(v["stroke"], v["accent"]),
    "bifrost": lambda v: bifrost_center(v["stroke"], v["accent"]),
    "yggdrasil": lambda v: yggdrasil_center(v["stroke"], v["accent"], v["eye_fill"]),
    "mimir": lambda v: mimir_center(v["stroke"], v["accent"], v["eye_fill"]),
    "asgard": lambda v: asgard_center(v["stroke"], v["accent"], v["eye_fill"]),
}


def build_svg(app, variant_name, v):
    """Build a 1024x1024 standalone SVG."""
    # Background: filled rounded square for icon, transparent otherwise
    bg = ""
    if v["bg"]:
        bg = f'<rect x="0" y="0" width="1024" height="1024" rx="180" fill="{v["bg"]}"/>'

    # Scale medallion: native r=52, want to fill ~75% of 1024 canvas
    # Target diameter ~768, so radius 384, scale = 384/52 = ~7.4
    scale = 7.4
    cx = 512
    cy = 512

    title = f"{app.capitalize()} — ECT pantheon — {variant_name} variant"
    desc = DESCRIPTIONS[app] + f" Rendered in the {variant_name} color treatment."

    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" role="img">
  <title>{title}</title>
  <desc>{desc}</desc>
  {bg}
  <g transform="translate({cx}, {cy}) scale({scale})">
    {medallion_frame(v["stroke"], v["accent"], v["ring_inner_op"])}
    {CENTERS[app](v)}
  </g>
</svg>
'''


def main():
    count = 0
    for variant_name, v in VARIANTS.items():
        for app in APPS:
            svg = build_svg(app, variant_name, v)
            path = OUT / variant_name / f"{app}.svg"
            path.write_text(svg)
            count += 1
            print(f"  {path.relative_to(OUT.parent)}")
    print(f"\nWrote {count} SVG files.")


if __name__ == "__main__":
    main()
