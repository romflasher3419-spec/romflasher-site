"""Grow the app icon into the sizes the web and Android want.

    python make_icons.py

Reads static/app.png (the tool's own icon) and writes the PWA / Apple touch
sizes next to it. Run once; build.py just copies static/ into dist/.
"""

import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
STATIC = os.path.join(HERE, "static")
SRC = os.path.join(STATIC, "app.png")

SIZES = [(180, "apple-touch-icon.png"),
         (192, "app-icon-192.png"),
         (512, "app-icon-512.png"),
         (32, "favicon-32.png")]


def main():
    base = Image.open(SRC).convert("RGBA")
    print("source %s %dx%d" % (os.path.basename(SRC), *base.size))
    for size, name in SIZES:
        out = os.path.join(STATIC, name)
        base.resize((size, size), Image.LANCZOS).save(out, "PNG",
                                                      optimize=True)
        print("  %-24s %dx%d  %d bytes"
              % (name, size, size, os.path.getsize(out)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
