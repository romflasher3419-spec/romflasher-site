"""One-off: move the look of the site out of build.py and into static/.

After this runs, build.py:
  * no longer carries the stylesheet or the favicon as Python strings
  * copies everything in static/ into dist/static/

Run once, from this folder:  & "C:\\Python315\\python.exe" _apply_style.py
"""

import io
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build.py")


def main():
    with io.open(BUILD, encoding="utf-8") as fh:
        text = fh.read()
    before = len(text)

    for label, pattern in (("drop FAVICON", r'FAVICON = """.*?"""\n\n'),
                           ("drop STYLE", r'STYLE = """.*?"""\n\n')):
        text, hits = re.subn(pattern, "", text, flags=re.S)
        print("  %-14s %d" % (label, hits))

    old = (
        '    with open(os.path.join(DIST, "static", "style.css"), "w",\n'
        '              encoding="utf-8", newline="\\n") as fh:\n'
        '        fh.write(STYLE.lstrip("\\n"))\n'
        '    with open(os.path.join(DIST, "static", "favicon.svg"), "w",\n'
        '              encoding="utf-8", newline="\\n") as fh:\n'
        "        fh.write(FAVICON)\n"
        '    for extra in ("channel.jpg", "channel.svg", "channel.png"):\n'
        "        src = os.path.join(STATIC, extra)\n"
        "        if os.path.exists(src):\n"
        '            shutil.copy2(src, os.path.join(DIST, "static", extra))\n'
    )
    new = (
        "    # static/ is the single source of truth: css, icons, avatar\n"
        "    for name in sorted(os.listdir(STATIC)):\n"
        "        src = os.path.join(STATIC, name)\n"
        "        if os.path.isfile(src):\n"
        '            shutil.copy2(src, os.path.join(DIST, "static", name))\n'
    )
    if old in text:
        text = text.replace(old, new)
        print("  %-14s %d" % ("static copy", 1))
    else:
        print("  !! static copy block not found - nothing written")
        return 1

    with io.open(BUILD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("  build.py %d -> %d chars" % (before, len(text)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
