"""Quick look at what the builder actually produced.

    python qa.py                       # summary of the whole dist/
    python qa.py --slug <slug>         # inspect one built page
    python qa.py --links               # check every internal link resolves
"""

import argparse
import glob
import io
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")
CONTENT = os.path.join(HERE, "content")


def text(path):
    return io.open(path, encoding="utf-8").read()


def strip(t):
    return re.sub(r"<[^>]+>", "", t)


def show_slug(slug):
    path = os.path.join(DIST, "rom", "%s.html" % slug)
    if not os.path.exists(path):
        hits = glob.glob(os.path.join(DIST, "rom", "*%s*.html" % slug))
        if not hits:
            print("[!] no built page matches %r" % slug)
            return 1
        path = hits[0]
    t = text(path)
    print("file        :", os.path.relpath(path, HERE))
    print("size        :", len(t), "chars")

    m = re.search(r"<title>(.*?)</title>", t, re.S)
    print("title       :", m.group(1).strip() if m else "-")
    m = re.search(r'<meta name="description" content="(.*?)">', t, re.S)
    print("description :", (m.group(1)[:110] + "...") if m else "-")

    m = re.search(r'<div class="head">(.*?)</div>\s*</div>', t, re.S)
    if m:
        head = m.group(1)
        print("icon        :", "app.png" if "app.png" in head else "MISSING")
        h1 = re.search(r"<h1>(.*?)</h1>", head, re.S)
        print("h1          :", h1.group(1).strip() if h1 else "-")
        meta = re.search(r'<p class="meta">(.*?)</p>', head, re.S)
        print("meta        :", strip(meta.group(1)).strip() if meta else "-")
    else:
        print("avatar      : head block NOT FOUND")

    m = re.search(r'<iframe[^>]+src="([^"]+)"', t)
    print("embed       :", m.group(1) if m else "none")
    if m:
        for flag in ("autoplay=1", "mute=1", "loop=1", "playlist="):
            print("   %-12s %s" % (flag, "ok" if flag in m.group(1) else "MISSING"))

    print("sections    :", ", ".join(sorted(set(
        strip(x).strip()[:40] for x in re.findall(r"<h2>(.*?)</h2>", t, re.S)))))
    print("links       :", len(re.findall(r'<li><strong>', t))
          or len(re.findall(r"<li>", t)))
    print("faq blocks  :", len(re.findall(r'<div class="faq">', t)))
    print("full desc   :", "shown" if "Full description" in t else
          ("expanded as main text" if "This page is the video in text form" in t
           else "none"))
    return 0


def summary():
    pages = glob.glob(os.path.join(DIST, "rom", "*.html"))
    bodies = glob.glob(os.path.join(CONTENT, "*.json"))
    import json
    written = 0
    with_date = 0
    with_links = 0
    for p in bodies:
        d = json.load(io.open(p, encoding="utf-8"))
        written += 1 if (d.get("body") or "").strip() else 0
        with_date += 1 if d.get("published") else 0
        with_links += 1 if d.get("links") else 0

    print("built pages      :", len(pages))
    print("content files    :", len(bodies))
    print("  with a body    :", written, "(still to write: %d)" % (len(bodies) - written))
    print("  with a date    :", with_date)
    print("  with links     :", with_links)
    print()
    for name in ("index.html", "videos.html", "download.html", "apps.html",
                 "about.html", "privacy.html", "terms.html", "contact.html",
                 "404.html", "sitemap.xml", "robots.txt", "feed.xml"):
        p = os.path.join(DIST, name)
        print("  %-14s %s" % (name, ("%d chars" % len(text(p))) if os.path.exists(p) else "MISSING"))
    css = os.path.join(DIST, "static", "style.css")
    print("  static/        ", ", ".join(sorted(os.listdir(os.path.join(DIST, "static"))))
          if os.path.isdir(os.path.join(DIST, "static")) else "MISSING")
    print()

    t = text(os.path.join(DIST, "videos.html"))
    chips = re.findall(r'<span class="chip[^"]*" data-y="([^"]+)">([^<]+)</span>', t)
    print("year chips       :", ", ".join("%s=%s" % (y, n) for y, n in chips))
    rows = re.findall(r'data-d="([^"]*)"', t)
    print("rows with date   :", sum(1 for r in rows if r))
    print("rows without     :", sum(1 for r in rows if not r))

    t = text(os.path.join(DIST, "index.html"))
    print("home cards       :", len(re.findall(r'<a class="card"', t)))
    print("header buttons   : GitHub %d, YouTube %d"
          % (t.count("github.com/romflasher3419-spec"),
             t.count("youtube.com/@Rom_Flasher")))
    return 0


def link_check():
    """Every href/src we emit should point at something that exists."""
    problems = []
    for path in glob.glob(os.path.join(DIST, "**", "*.html"), recursive=True):
        page_dir = os.path.dirname(path)
        rel_page = os.path.relpath(path, DIST)
        depth = rel_page.count(os.sep)
        # Inline JS builds hrefs as text too - only look at real markup.
        markup = re.sub(r"<script\b.*?</script>", " ", text(path),
                         flags=re.S | re.I)
        for attr in re.findall(r'(?:href|src)="([^"]+)"', markup):
            if attr.startswith(("http://", "https://", "mailto:", "#", "data:")):
                continue
            target = os.path.normpath(
                os.path.join(page_dir, attr.split("#")[0].split("?")[0]))
            if not os.path.exists(target):
                problems.append("%s -> %s" % (rel_page, attr))
    print("internal links checked, %d broken" % len(problems))
    for p in problems[:25]:
        print("   x", p)
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug")
    ap.add_argument("--links", action="store_true")
    args = ap.parse_args()
    if not os.path.isdir(DIST):
        print("[!] dist/ is missing - run build.py first")
        return 1
    if args.slug:
        return show_slug(args.slug)
    if args.links:
        return link_check()
    return summary()


if __name__ == "__main__":
    sys.exit(main())
