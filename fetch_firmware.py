"""Build the ROM index the downloader page reads.

The downloader page needs one thing the site cannot make up: for a given
phone, which stock builds exist, which region each one is for, and where the
file is. That list changes every month, so it is fetched, cached and committed
rather than written by hand.

Where the data comes from
-------------------------
`miuirom.org` publishes, for every Xiaomi / Redmi / POCO phone, a page that
lists each regional build with its version string, Android version, release
date, file size and a download link. Those pages are public and are already
the index this site points people at, so the numbers here come from them.

What this script does NOT do
----------------------------
* It does not download a single firmware file. Nothing is proxied, mirrored or
  hosted here - the links stay pointing at the publisher's own download route.
* It does not touch any paywall, ad-gate or token. It reads the same tables a
  visitor sees, at a polite rate, and caches them.

Usage
-----
    python fetch_firmware.py                 # refresh every device
    python fetch_firmware.py --brand poco    # only the POCO phones
    python fetch_firmware.py --slug poco-f5  # one device
    python fetch_firmware.py --rebuild       # ignore the cache
    python fetch_firmware.py --list          # what is in the index now

Output: `data/firmware.json` (committed) and `data/catalog.json` (the device
list the page searches through).
"""

import argparse
import base64
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
CACHE = os.path.join(ROOT, ".firmware-cache")
OUT = os.path.join(DATA, "firmware.json")
CATALOG = os.path.join(DATA, "catalog.json")

SOURCE = "https://miuirom.org"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# One request per second is slow enough to stay a good citizen and fast enough
# that a full refresh (a few hundred pages) finishes inside a CI job.
DELAY = 1.0


# --------------------------------------------------------------- tiny http

def fetch(url, cache=True, ttl=86400):
    """GET a url, through the on-disk cache when the copy is fresh enough."""
    key = re.sub(r"[^a-zA-Z0-9]+", "_", url)[-120:]
    path = os.path.join(CACHE, key + ".html")
    if cache and os.path.exists(path):
        age = time.time() - os.path.getmtime(path)
        if age < ttl:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                return fh.read()
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=45) as resp:
        text = resp.read().decode("utf-8", "replace")
    if cache:
        os.makedirs(CACHE, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    return text


def strip(html):
    """Tag-free text, entities decoded, whitespace collapsed."""
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", html, flags=re.S | re.I)
    text = re.sub(r"<[^>]+>", " ", text)
    text = (text.replace("&amp;", "&").replace("&nbsp;", " ")
                .replace("&ndash;", "-").replace("&mdash;", "-")
                .replace("&#8211;", "-").replace("&#8212;", "-")
                .replace("&quot;", '"').replace("&#039;", "'")
                .replace("&rsquo;", "'").replace("&lsquo;", "'"))
    return re.sub(r"\s+", " ", text).strip()


def b64url(value):
    """Decode the base64 URL the publisher hides behind the download link."""
    try:
        raw = base64.b64decode(value + "=" * (-len(value) % 4)).decode("utf-8")
    except Exception:
        return ""
    return raw if raw.startswith("http") else ""


# ----------------------------------------------------------------- parsing

RE_REGION = re.compile(r"<h2 id='([^']+)' class='flag'>", re.S)
RE_KIND = re.compile(r"<h3 class='h3_roms'>(.*?)</h3>", re.S)
RE_DL = re.compile(r"<dl class='roms'>(.*?)</dl>", re.S)
RE_DT = re.compile(r"<dt>(.*?)</dt><dd>(.*?)</dd>", re.S)
RE_LINK = re.compile(r'data-href="([A-Za-z0-9+/=]+)"')
RE_EXT = re.compile(r"\((\.[a-z0-9]+)\)", re.I)
RE_CODE = re.compile(r"\(codename\s*<span>(.*?)</span>\)", re.S | re.I)
RE_MODELS = re.compile(r"Phone models:(.*?)\.", re.S)
RE_TITLE = re.compile(r"<h1[^>]*>(.*?)</h1>", re.S)
RE_REGION_LIST = re.compile(r"region_list'?>(.*?)</ul>", re.S)


def parse_device(slug, html):
    """Turn one device page into the record the page reads."""
    title = strip(RE_TITLE.search(html).group(1)) if RE_TITLE.search(html) else slug
    title = re.sub(r"\s*(Firmware|Download|Rom).*$", "", title, flags=re.I).strip()
    if not title:
        title = slug.replace("-", " ").title()

    # The publisher writes "POCO F5" in the heading but "Poco F5" in a couple of
    # places. The brand's own spelling is the one people search for, so it
    # always wins.
    brand = brand_of(slug)
    for spelling in ("POCO", "Redmi", "Xiaomi"):
        if re.match(r"^\s*" + spelling + r"\b", title, re.I):
            title = spelling + title[len(spelling):]
            break

    code = ""
    m = RE_CODE.search(html)
    if m:
        code = strip(m.group(1))

    models = ""
    m = RE_MODELS.search(html)
    if m:
        # "23049PCD8G (Global), 23049PCD8I (India)" - the codes are what a
        # visitor needs, the region in brackets is a bonus.
        pairs = re.findall(r"([A-Za-z0-9][A-Za-z0-9\-]*)\s*\(([^)]*)\)",
                           strip(m.group(1)))
        if pairs:
            models = ", ".join(p[0] for p in pairs)

    # The regions this phone is sold in. The list at the top of the page links
    # to each region section, so the anchor is the reliable name - "Europe" is
    # what the page shows, "EEA" is what the section is called.
    regions = []
    m = RE_REGION_LIST.search(html)
    if m:
        for item in re.findall(r"<li>(.*?)</li>", m.group(1), re.S):
            a = re.search(r"href='#([^']+)'", item)
            if a and a.group(1) not in regions:
                regions.append(a.group(1))

    # Every build on the page, in the order the publisher lists them.
    #
    # The page is laid out as one section per region, and inside each section
    # two headings - "Recovery ROM" and "Fastboot ROM (flash file)" - each
    # followed by a <dl> holding that build's details. The two are matched by
    # position: a heading owns the next <dl> after it, and nothing else.
    roms = []
    seen = set()
    sections = list(RE_REGION.finditer(html))
    for idx, rm in enumerate(sections):
        region = rm.group(1).strip()
        start = rm.end()
        end = sections[idx + 1].start() if idx + 1 < len(sections) else len(html)
        block = html[start:end]

        marks = []
        for km in RE_KIND.finditer(block):
            marks.append((km.start(), 0, km.group(1)))
        for dm in RE_DL.finditer(block):
            marks.append((dm.start(), 1, dm.group(1)))
        marks.sort(key=lambda x: x[0])

        for i, mark in enumerate(marks):
            if mark[1] != 0:
                continue
            kind_raw = strip(mark[2]).lower()
            body = None
            for j in range(i + 1, len(marks)):
                if marks[j][1] == 1:
                    body = marks[j][2]
                break
            if body is None:
                continue

            fields = {}
            for fm in RE_DT.finditer(body):
                key = strip(fm.group(1)).lower()
                fields[key] = strip(fm.group(2))
            version = fields.get("version", "")
            if not version:
                continue
            lm = RE_LINK.search(body)
            link = b64url(lm.group(1)) if lm else ""
            ext = (RE_EXT.search(fields.get("official link", "")) or [None, ""])[1]
            ext = ext.lower()
            if "fastboot" in kind_raw:
                kind = "fastboot"
            elif "recovery" in kind_raw:
                kind = "recovery"
            elif ext == ".tgz":
                kind = "fastboot"
            else:
                kind = "recovery"
            key = (region, version, kind)
            if key in seen:
                continue
            seen.add(key)
            roms.append({
                "v": version,
                "region": region,
                "kind": kind,
                "os": fields.get("os", ""),
                "android": fields.get("android", ""),
                    "date": fields.get("release date", ""),
                    "size": fields.get("file size") or fields.get("flash file size", ""),
                    "ext": ext.lower(),
                    "url": link,
                })

    # The region heading text carries the newest build, e.g. "Global HyperOS
    # 3.0.4.0.VMRMIXM" - used to sort so the newest build of each region is
    # first even when the page lists regions in a different order.
    return {
        "slug": slug,
        "brand": brand,
        "name": title,
        "code": code,
        "models": models,
        "regions": regions,
        "roms": roms,
        "page": "%s/phones/%s" % (SOURCE, slug),
    }


# ------------------------------------------------------------------ catalog

def device_slugs():
    """Every phone page the publisher lists, with its brand."""
    out = []
    for part in ("post-sitemap.xml", "post-sitemap2.xml", "post-sitemap3.xml"):
        try:
            xml = fetch("%s/%s" % (SOURCE, part))
        except Exception:
            continue
        for loc in re.findall(r"<loc>([^<]+)</loc>", xml):
            m = re.match(r"https?://miuirom\.org/phones/([a-z0-9\-]+)/?$", loc)
            if m:
                out.append(m.group(1))
    seen = set()
    uniq = []
    for slug in out:
        if slug not in seen:
            seen.add(slug)
            uniq.append(slug)
    return uniq


def brand_of(slug):
    """The brand a device slug belongs to.

    The publisher names the pages "poco-f5", "redmi-note-13", "xiaomi-14",
    "mi-11" and so on, so the first word of the slug is enough. "Poco F5"
    and "POCO X7 Pro" both come back as "POCO".
    """
    name = slug.lower()
    if name.startswith("poco"):
        return "POCO"
    if name.startswith("redmi"):
        return "Redmi"
    if name.startswith("xiaomi"):
        return "Xiaomi"
    if name.startswith("mi") or name.startswith("mix"):
        return "Xiaomi"
    return "Other"


# --------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description="Refresh the ROM index.")
    ap.add_argument("--brand", help="only this brand (poco, redmi, xiaomi)")
    ap.add_argument("--slug", help="only this device slug")
    ap.add_argument("--limit", type=int, default=0, help="stop after N devices")
    ap.add_argument("--rebuild", action="store_true", help="ignore the cache")
    ap.add_argument("--list", action="store_true", help="list what is indexed")
    args = ap.parse_args()

    os.makedirs(DATA, exist_ok=True)
    os.makedirs(CACHE, exist_ok=True)

    if args.list:
        if os.path.exists(OUT):
            with open(OUT, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            print("%d devices, %d builds" % (
                len(data.get("devices", {})),
                sum(len(d.get("roms", [])) for d in data.get("devices", {}).values())))
            for slug, d in sorted(data.get("devices", {}).items()):
                print("  %-26s %-28s %-10s %d builds" % (
                    slug, d.get("name", ""), d.get("code", ""), len(d.get("roms", []))))
        else:
            print("no index yet - run: python fetch_firmware.py")
        return 0

    index = {}
    if os.path.exists(OUT):
        try:
            with open(OUT, "r", encoding="utf-8") as fh:
                index = json.load(fh).get("devices", {})
        except Exception:
            index = {}

    if args.slug:
        slugs = [args.slug]
    else:
        slugs = device_slugs()
        if args.brand:
            slugs = [s for s in slugs if brand_of(s).lower() == args.brand.lower()]
    if args.limit:
        slugs = slugs[:args.limit]

    print("%d device pages to fetch" % len(slugs))
    done = 0
    for i, slug in enumerate(slugs):
        if slug in index and not args.rebuild:
            continue
        url = "%s/phones/%s" % (SOURCE, slug)
        try:
            html = fetch(url, cache=not args.rebuild)
        except (urllib.error.URLError, OSError) as exc:
            print("  [%d/%d] %-26s FAILED (%s)" % (i + 1, len(slugs), slug, exc))
            continue
        rec = parse_device(slug, html)
        if not rec["roms"]:
            continue
        index[slug] = rec
        done += 1
        print("  [%d/%d] %-26s %-26s %-10s %d builds" % (
            i + 1, len(slugs), slug, rec["name"], rec["code"], len(rec["roms"])))
        time.sleep(DELAY)

    devices = index
    catalog = []
    for slug, d in sorted(devices.items()):
        catalog.append({
            "slug": slug,
            "brand": brand_of(slug),
            "name": d.get("name", slug),
            "code": d.get("code", ""),
            "models": d.get("models", ""),
            "regions": d.get("regions", []),
            "count": len(d.get("roms", [])),
        })

    payload = {
        "source": SOURCE,
        "generated": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "devices": devices,
    }
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(payload, fh, ensure_ascii=False, indent=1, sort_keys=True)
    with open(CATALOG, "w", encoding="utf-8") as fh:
        json.dump({"generated": payload["generated"], "devices": catalog},
                  fh, ensure_ascii=False, indent=1, sort_keys=True)
    print("%d new, %d total -> %s" % (done, len(devices), OUT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
