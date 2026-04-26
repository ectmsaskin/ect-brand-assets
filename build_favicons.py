"""Generate multi-resolution .ico favicons from the icon variant PNGs."""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).parent
PNG_DIR = ROOT / "png" / "icon"
FAV_DIR = ROOT / "favicon"
APPS = ["heimdall", "huginn", "muninn", "bifrost", "yggdrasil", "mimir", "asgard"]
ICO_SIZES = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]


def main():
    count = 0
    for app in APPS:
        # Use the 256px PNG as the source so PIL can downsample cleanly
        src = PNG_DIR / app / f"{app}_256.png"
        img = Image.open(src)
        out = FAV_DIR / f"{app}.ico"
        img.save(out, format="ICO", sizes=ICO_SIZES)
        count += 1
        print(f"  {out.relative_to(ROOT)}")
    print(f"\nWrote {count} .ico files.")


if __name__ == "__main__":
    main()
