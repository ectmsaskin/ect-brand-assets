"""Build a printable HTML brand reference page that combines all variants."""
from pathlib import Path

ROOT = Path(__file__).parent
SVG_DIR = ROOT / "svg"
OUT = ROOT / "reference" / "ect_pantheon_brand_reference.html"

APPS = [
    ("heimdall", "QA pipeline", "Watcher of Bifrost. The data quality gate."),
    ("huginn", "Call attribution", "Odin's raven of thought. Tracks marketing source for inbound calls."),
    ("muninn", "Customer knowledge base", "Odin's raven of memory. Long-term store of customer signal."),
    ("bifrost", "Integrations · ETL", "The rainbow bridge. Connects operational systems to the warehouse."),
    ("yggdrasil", "Data warehouse", "The world tree. Structural foundation that holds the data of all realms."),
    ("mimir", "Business intelligence", "Guardian of the well of wisdom. Queried for insight."),
]

# Asgard is the toolbox's own mark — the parent surface, not a member of the pantheon.
ASGARD = ("asgard", "Toolbox · the realm of the gods", "Central citadel surrounded by six realm orbs. The home where the pantheon gathers.")

COLORS = [
    ("#214080", "primary blue", "buttons, headers, primary marks"),
    ("#f3e830", "electric yellow", "accents, highlights, app icon background contrast"),
    ("#f6f46f", "yellow tint", "subtle backgrounds, hover states"),
    ("#231f20", "near-black", "body text, dark surfaces"),
    ("#757575", "dark gray", "secondary text, dividers"),
    ("#acacac", "mid gray", "borders, disabled states"),
    ("#e4e4e4", "light gray", "page backgrounds, light surfaces"),
]


def read_svg(variant, app):
    """Return SVG content with XML declaration stripped (so it inlines cleanly)."""
    raw = (SVG_DIR / variant / f"{app}.svg").read_text()
    if raw.startswith("<?xml"):
        raw = raw.split("?>", 1)[1].lstrip()
    return raw


def color_swatch(hex_code, name, use):
    text_color = "#231f20" if hex_code in ("#f3e830", "#f6f46f", "#e4e4e4", "#acacac") else "#ffffff"
    return f'''
    <div class="swatch" style="background:{hex_code};color:{text_color}">
      <div class="swatch-hex">{hex_code}</div>
      <div class="swatch-name">{name}</div>
      <div class="swatch-use">{use}</div>
    </div>'''


def app_row(app_id, label, story):
    cells = []
    for variant, bg in [("light", "#e4e4e4"), ("dark", "#231f20"), ("icon", "transparent")]:
        svg = read_svg(variant, app_id)
        cells.append(f'<div class="cell" style="background:{bg}"><div class="mark">{svg}</div></div>')
    return f'''
    <section class="app-row">
      <div class="app-meta">
        <h3>{app_id.upper()}</h3>
        <p class="tagline">{label}</p>
        <p class="story">{story}</p>
      </div>
      <div class="variants">
        <div class="variant-block">
          <div class="variant-label">light</div>
          {cells[0]}
          <div class="variant-use">in-product · docs · sidebars</div>
        </div>
        <div class="variant-block">
          <div class="variant-label">dark</div>
          {cells[1]}
          <div class="variant-use">dark mode · login · splash</div>
        </div>
        <div class="variant-block">
          <div class="variant-label">icon</div>
          {cells[2]}
          <div class="variant-use">app icon · favicon · marketing</div>
        </div>
      </div>
    </section>'''


def lockup_row(app_id, label):
    svg = read_svg("light", app_id)
    return f'''
    <div class="lockup-row">
      <div class="lockup-mark">{svg}</div>
      <div class="lockup-text">
        <div class="lockup-name">{app_id.upper()}</div>
        <div class="lockup-tag">{label}</div>
      </div>
    </div>'''


def main():
    swatches = "\n".join(color_swatch(h, n, u) for h, n, u in COLORS)
    rows = "\n".join(app_row(a, l, s) for a, l, s in APPS)
    asgard_row = app_row(*ASGARD)
    lockups = "\n".join(lockup_row(a, l) for a, l, _ in APPS + [ASGARD])

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>ECT Application Pantheon — Brand Reference</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap');

* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
  font-family: 'Montserrat', system-ui, -apple-system, sans-serif;
  color: #231f20;
  background: #ffffff;
  line-height: 1.5;
  font-size: 14px;
}}
.page {{
  max-width: 900px;
  margin: 0 auto;
  padding: 60px 40px;
}}
header.title-block {{
  border-bottom: 2px solid #214080;
  padding-bottom: 24px;
  margin-bottom: 40px;
}}
header.title-block .eyebrow {{
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 3px;
  color: #757575;
  text-transform: uppercase;
}}
header.title-block h1 {{
  font-size: 36px;
  font-weight: 700;
  color: #214080;
  letter-spacing: 1px;
  margin-top: 8px;
}}
header.title-block p {{
  margin-top: 8px;
  color: #757575;
  font-size: 14px;
}}
h2 {{
  font-size: 11px;
  font-weight: 600;
  letter-spacing: 3px;
  color: #757575;
  text-transform: uppercase;
  margin-bottom: 20px;
  padding-bottom: 8px;
  border-bottom: 1px solid #e4e4e4;
}}
section {{ margin-bottom: 48px; }}

.palette {{
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}}
.swatch {{
  aspect-ratio: 1;
  padding: 12px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border-radius: 4px;
  font-size: 10px;
}}
.swatch-hex {{ font-weight: 600; font-family: 'Courier New', monospace; }}
.swatch-name {{ font-weight: 500; font-size: 11px; }}
.swatch-use {{ font-size: 9px; opacity: 0.85; }}

.app-row {{
  display: grid;
  grid-template-columns: 200px 1fr;
  gap: 32px;
  margin-bottom: 40px;
  padding-bottom: 32px;
  border-bottom: 1px solid #e4e4e4;
  page-break-inside: avoid;
}}
.app-row:last-child {{ border-bottom: none; }}
.app-meta h3 {{
  font-size: 22px;
  font-weight: 700;
  color: #214080;
  letter-spacing: 2px;
  margin-bottom: 4px;
}}
.app-meta .tagline {{
  font-size: 12px;
  color: #757575;
  text-transform: uppercase;
  letter-spacing: 1px;
  font-weight: 600;
  margin-bottom: 12px;
}}
.app-meta .story {{
  font-size: 13px;
  color: #231f20;
  line-height: 1.5;
}}
.variants {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 12px;
}}
.variant-block {{
  text-align: center;
}}
.variant-label {{
  font-size: 10px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: #757575;
  margin-bottom: 6px;
}}
.cell {{
  aspect-ratio: 1;
  border-radius: 8px;
  padding: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 0.5px solid #acacac;
}}
.cell .mark {{ width: 100%; height: 100%; }}
.cell svg {{ width: 100%; height: 100%; display: block; }}
.variant-use {{
  font-size: 9px;
  color: #757575;
  margin-top: 6px;
  text-transform: lowercase;
}}

.lockups {{
  display: flex;
  flex-direction: column;
  gap: 6px;
}}
.lockup-row {{
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 12px 18px;
  background: #e4e4e4;
  border-radius: 8px;
}}
.lockup-mark {{ width: 48px; height: 48px; flex-shrink: 0; }}
.lockup-mark svg {{ width: 100%; height: 100%; display: block; }}
.lockup-text {{ display: flex; flex-direction: column; }}
.lockup-name {{
  font-size: 20px;
  font-weight: 700;
  color: #214080;
  letter-spacing: 3px;
}}
.lockup-tag {{
  font-size: 11px;
  color: #757575;
}}

.usage-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}}
.usage-card {{
  padding: 16px;
  border: 1px solid #e4e4e4;
  border-radius: 8px;
}}
.usage-card h4 {{
  font-size: 14px;
  font-weight: 600;
  color: #214080;
  margin-bottom: 6px;
}}
.usage-card p {{
  font-size: 12px;
  color: #231f20;
  line-height: 1.5;
}}
.usage-card .when {{
  margin-top: 8px;
  font-size: 11px;
  color: #757575;
  font-weight: 500;
}}

footer.file-index {{
  margin-top: 48px;
  padding-top: 24px;
  border-top: 1px solid #e4e4e4;
  font-size: 11px;
  color: #757575;
  line-height: 1.7;
}}
footer.file-index code {{
  font-family: 'Courier New', monospace;
  background: #f6f4f0;
  padding: 1px 5px;
  border-radius: 3px;
  font-size: 10px;
}}

@media print {{
  body {{ font-size: 12px; }}
  .page {{ padding: 30px 24px; max-width: none; }}
  header.title-block {{ margin-bottom: 24px; }}
  header.title-block h1 {{ font-size: 28px; }}
  section {{ margin-bottom: 24px; page-break-inside: avoid; }}
  .app-row {{ page-break-inside: avoid; }}
  .palette {{ page-break-inside: avoid; }}
}}
</style>
</head>
<body>
<div class="page">

  <header class="title-block">
    <div class="eyebrow">East Coast Towing · Brand Reference</div>
    <h1>The Application Pantheon</h1>
    <p>Norse-themed naming and identity system for ECT internal applications. Six apps plus the Asgard toolbox mark, three color variants each, designed as a unified medallion family.</p>
  </header>

  <section>
    <h2>Brand Palette</h2>
    <div class="palette">
      {swatches}
    </div>
  </section>

  <section>
    <h2>Pantheon · all six apps · all three variants</h2>
    {rows}
  </section>

  <section>
    <h2>Asgard · the toolbox mark</h2>
    <p style="font-size:13px;color:#757575;margin-bottom:16px;line-height:1.6">Asgard is the home of the gods — the realm where the pantheon gathers. It is the canonical mark for <strong style="color:#214080">toolbox.eastcoasttowing.com</strong>, the parent portal that displays all six apps. Asgard is NOT a member of the pantheon directory itself; it represents the directory.</p>
    {asgard_row}
  </section>

  <section>
    <h2>Wordmark Lockups · for navigation and headers</h2>
    <div class="lockups">
      {lockups}
    </div>
  </section>

  <section>
    <h2>Variant Usage Guide</h2>
    <div class="usage-grid">
      <div class="usage-card">
        <h4>Light variant</h4>
        <p>Blue strokes on neutral surfaces. The everyday in-product mark.</p>
        <p class="when">Use for: dashboards, internal docs, sidebars, navigation tiles, slide decks, light-themed UI.</p>
      </div>
      <div class="usage-card">
        <h4>Dark variant</h4>
        <p>White strokes with yellow accents on dark surfaces. The dark-mode swap of the light variant.</p>
        <p class="when">Use for: dark-mode UI, login screens, splash pages, terminal-themed interfaces.</p>
      </div>
      <div class="usage-card">
        <h4>Icon variant</h4>
        <p>Yellow medallion on solid blue. The canonical app icon. Brand-forward.</p>
        <p class="when">Use for: app icons (iOS/Android), favicons, marketing surfaces, swag, splash heroes.</p>
      </div>
    </div>
  </section>

  <footer class="file-index">
    <strong style="color:#214080">File index</strong><br>
    <code>svg/{{light,dark,icon}}/{{slug}}.svg</code> — 21 standalone SVG masters at 1024×1024<br>
    <code>png/{{light,dark,icon}}/{{slug}}/{{slug}}_{{size}}.png</code> — 147 PNG renders at 1024 / 512 / 256 / 128 / 64 / 32 / 16<br>
    <code>favicon/{{slug}}.ico</code> — 7 multi-resolution Windows-style favicons<br>
    <br>
    Pantheon apps: heimdall · huginn · muninn · bifrost · yggdrasil · mimir<br>
    Toolbox mark: asgard
  </footer>

</div>
</body>
</html>
'''
    OUT.write_text(html)
    size_kb = OUT.stat().st_size / 1024
    print(f"Wrote {OUT.relative_to(ROOT)} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
