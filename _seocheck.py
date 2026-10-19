"""Sanity-check the built dist/: SEO tags, JSON-LD validity, notes."""
import glob
import io
import json
import os
import re

DIST = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dist")

pages = sorted(glob.glob(os.path.join(DIST, "**", "*.html"), recursive=True))
bad_ld, no_kw, no_desc, no_canon, types = [], [], [], [], {}
total_blocks = 0


def count_types(node, bag):
    """Count every @type in a block, including the nested ones.

    A CollectionPage carries its ItemList inside mainEntity and a FAQPage hides
    its Questions - those are the rich results that matter, so the report has to
    be able to see them.
    """
    if isinstance(node, dict):
        value = node.get("@type")
        if isinstance(value, str):
            bag[value] = bag.get(value, 0) + 1
        elif isinstance(value, list):
            for one in value:
                bag[one] = bag.get(one, 0) + 1
        for child in node.values():
            count_types(child, bag)
    elif isinstance(node, list):
        for child in node:
            count_types(child, bag)


for p in pages:
    t = io.open(p, encoding="utf-8").read()
    rel = os.path.relpath(p, DIST)
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', t, re.S):
        total_blocks += 1
        raw = m.group(1)
        try:
            obj = json.loads(raw)
        except Exception as e:
            bad_ld.append("%s: %s" % (rel, e))
            continue
        count_types(obj, types)
    if 'name="keywords"' not in t:
        no_kw.append(rel)
    if 'name="description"' not in t:
        no_desc.append(rel)
    if 'rel="canonical"' not in t:
        no_canon.append(rel)
    if t.count("<title>") != 1 or t.count("</head>") != 1:
        bad_ld.append("%s: head structure" % rel)

print("pages                :", len(pages))
print("json-ld blocks       :", total_blocks)
print("json-ld parse errors :", len(bad_ld))
for b in bad_ld[:10]:
    print("   -", b)
print("missing keywords     :", len(no_kw), no_kw[:5])
print("missing description  :", len(no_desc), no_desc[:5])
print("missing canonical    :", len(no_canon), no_canon[:5])
print()
print("schema types:")
for k, v in sorted(types.items(), key=lambda kv: -kv[1]):
    print("   %-22s %d" % (k, v))

sm = io.open(os.path.join(DIST, "sitemap.xml"), encoding="utf-8").read()
print()
print("sitemap urls         :", sm.count("<url>"))
print("sitemap device urls  :", sm.count("/device/"))
print("sitemap has download :", "/download.html" in sm)

# keyword length distribution
lens = []
for p in pages:
    t = io.open(p, encoding="utf-8").read()
    m = re.search(r'<meta name="keywords" content="([^"]*)"', t)
    if m:
        lens.append(len(m.group(1)))
print("keywords meta chars  : min %d, avg %d, max %d"
      % (min(lens), sum(lens) // len(lens), max(lens)))
print("total dist size      : %.1f MB"
      % (sum(os.path.getsize(f) for f in glob.glob(os.path.join(DIST, "**", "*"),
                                                   recursive=True) if os.path.isfile(f))
         / 1048576.0))
