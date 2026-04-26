"""Convert each SVG to PNG at 7 sizes."""
from pathlib import Path
import cairosvg

ROOT = Path(__file__).parent
SVG_DIR = ROOT / "svg"
PNG_DIR = ROOT / "png"
SIZES = [1024, 512, 256, 128, 64, 32, 16]
VARIANTS = ["light", "dark", "icon"]
APPS = ["heimdall", "huginn", "muninn", "bifrost", "yggdrasil", "mimir", "asgard"]


def main():
    count = 0
    for variant in VARIANTS:
        for app in APPS:
            svg_path = SVG_DIR / variant / f"{app}.svg"
            svg_bytes = svg_path.read_bytes()
            for size in SIZES:
                out_dir = PNG_DIR / variant / app
                out_dir.mkdir(parents=True, exist_ok=True)
                out_path = out_dir / f"{app}_{size}.png"
                cairosvg.svg2png(
                    bytestring=svg_bytes,
                    write_to=str(out_path),
                    output_width=size,
                    output_height=size,
                )
                count += 1
    print(f"Wrote {count} PNG files.")


if __name__ == "__main__":
    main()
