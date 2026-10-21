"""Build the ROM index the downloader page reads.

The downloader page needs one thing the site cannot make up: for a given
phone, which stock builds exist, which region each one is for, and where the
file is. That list changes every month, so it is fetched, cached and committed
rather than written by hand.

Where the data comes from
-------------------------
Two public, script-friendly indexes, both of them the ones the flashing
world already points people at:

* `XiaomiFirmwareUpdater/miui-updates-tracker` publishes a YAML file with
  every Xiaomi / Redmi / POCO build it tracks - the Recovery ROM *and* the
  Fastboot ROM, with the version, the Android version, the release date, the
  size and the real download link on Xiaomi's own CDN.
* `xmfirmwareupdater.com` publishes the same Recovery builds with a second
  pair of mirrors, so a slow CDN can be side-stepped.

Both are read with a plain GET, both send `Access-Control-Allow-Origin: *`,
and neither needs a key, a login or a token.

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
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
CACHE = os.path.join(ROOT, ".firmware-cache")
OUT = os.path.join(DATA, "firmware.json")
CATALOG = os.path.join(DATA, "catalog.json")

TRACKER = "https://raw.githubusercontent.com/XiaomiFirmwareUpdater/miui-updates-tracker/master"
XFU = "https://xmfirmwareupdater.com"

TRACKER_LATEST = TRACKER + "/data/latest.yml"
TRACKER_DEVICES = TRACKER + "/data/devices.yml"
XFU_LATEST = XFU + "/data/devices/latest.yml"
XFU_DEVICES = XFU + "/data/firmware_devices.yml"

# Xiaomi keeps a second copy of the OTA bucket in Singapore. The tracker's own
# code races the two when it reads a file's headers, so it is the same pair
# of mirrors - and the Singapore one is usually the quicker of the two.
ALIYUNS = "bkt-sgp-miui-ota-update-alisgp.oss-ap-southeast-1.aliyuncs.com"
BIGOTA = "bigota.d.miui.com"

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# The region a build is meant for. The tracker's file names carry a short code
# and the device names carry the long one; both are mapped to one word.
REGION_BY_CODE = {
    "global": "Global", "eea": "EEA", "in": "India", "ru": "Russia",
    "tw": "Taiwan", "tr": "Turkey", "id": "Indonesia", "jp": "Japan",
    "sg": "Singapore", "cn": "China", "kr": "Korea",
}
REGION_WORDS = ["Global", "EEA", "Europe", "India", "Russia", "Taiwan",
                "Turkey", "Indonesia", "Japan", "China", "Singapore", "Korea"]
REGION_BY_NAME = {"Europe": "EEA"}


# --------------------------------------------------------------- tiny http

def fetch(url, cache=True, ttl=86400):
    """GET a url, through the on-disk cache when the copy is fresh enough."""
    key = re.sub(r"[^a-zA-Z0-9]+", "_", url)[-120:]
    path = os.path.join(CACHE, key + ".txt")
    if cache and os.path.exists(path):
        age = time.time() - os.path.getmtime(path)
        if age < ttl:
            with open(path, "r", encoding="utf-8", errors="replace") as fh:
                return fh.read()
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/plain,*/*",
        "Accept-Language": "en-US,en;q=0.9",
    })
    with urllib.request.urlopen(req, timeout=60) as resp:
        text = resp.read().decode("utf-8", "replace")
    if cache:
        os.makedirs(CACHE, exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    return text


def head_size(url):
    """Content-Length of a file, or None when the server will not say."""
    try:
        req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=20) as resp:
            length = resp.headers.get("Content-Length")
            if resp.status == 200 and length:
                return int(length)
    except Exception:
        return None
    return None


# --------------------------------------------------------------- tiny yaml

def parse_items(txt):
    """Read the list-of-dicts YAML the two indexes are written in.

    It is a flat list of blocks with at most one level of nesting, so a small
    indentation reader is enough - and it keeps this script on the standard
    library, like the rest of the site.
    """
    items = []
    cur = None
    sub_key = None
    sub_indent = -1
    for raw in txt.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip())
        line = raw.strip()
        if line.startswith("- "):
            cur = {}
            items.append(cur)
            sub_key = None
            sub_indent = -1
            line = line[2:].strip()
            if not line:
                continue
        if cur is None or ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if value == "":
            cur[key] = {}
            sub_key = key
            sub_indent = indent
        elif sub_key and indent > sub_indent and isinstance(cur.get(sub_key), dict):
            cur[sub_key][key] = value
        else:
            cur[key] = value
            sub_key = None
    return items


def parse_map(txt):
    """Read the `key: value` YAML the device list is written in."""
    out = {}
    for line in txt.splitlines():
        if ":" not in line or line.startswith(" "):
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip().strip("'\"")
        if key and value:
            out[key] = value
    return out


def parse_list_map(txt):
    """Read the `key:` followed by `- item` YAML the tracker names use."""
    out = {}
    key = None
    for raw in txt.splitlines():
        if not raw.strip():
            continue
        if raw.lstrip().startswith("- "):
            if key:
                out[key].append(raw.lstrip()[2:].strip().strip("'\""))
            continue
        if ":" in raw and not raw.startswith(" "):
            key = raw.split(":", 1)[0].strip()
            out[key] = []
            rest = raw.split(":", 1)[1].strip()
            if rest:
                out[key].append(rest.strip().strip("'\""))
            key = key
    return out


# ----------------------------------------------------------------- helpers

def region_of_name(name):
    """The region word a device name ends with, if it has one."""
    for word in REGION_WORDS:
        if name.endswith(" " + word):
            return REGION_BY_NAME.get(word, word)
    return "China"


def strip_region(name, region):
    """'POCO F5 India' -> 'POCO F5'."""
    for word in REGION_WORDS:
        if name.endswith(" " + word):
            return name[: -len(word)].strip()
    return name


def brand_of(name):
    """The brand a device name starts with."""
    low = name.lower()
    if low.startswith("poco"):
        return "POCO"
    if low.startswith("redmi"):
        return "Redmi"
    if low.startswith("xiaomi"):
        return "Xiaomi"
    if low.startswith("mi ") or low.startswith("mi4") or low.startswith("mi5") \
            or low.startswith("mi6") or low.startswith("mi7") or low.startswith("mi8") \
            or low.startswith("mi9") or low.startswith("mi10") or low.startswith("mi11") \
            or low.startswith("mix ") or low.startswith("mipad") or low.startswith("mi band"):
        return "Xiaomi"
    return "Xiaomi"


def os_name(version):
    """'OS3.0.4.0.VMRMIXM' -> 'HyperOS 3', 'V14.0.1.0.TMRCNXM' -> 'MIUI 14'."""
    if not version:
        return ""
    if version.startswith("OS"):
        major = version[2:].split(".")[0]
        return "HyperOS " + major if major else "HyperOS"
    if version.startswith("V"):
        major = version[1:].split(".")[0]
        if major.isdigit() and int(major) >= 13:
            return "MIUI " + major
        return "MIUI " + major if major else "MIUI"
    return ""


def size_text(n):
    """Bytes -> '5.8 GB'."""
    if not n:
        return ""
    units = ["B", "KB", "MB", "GB", "TB"]
    size = float(n)
    i = 0
    while size >= 1024 and i < len(units) - 1:
        size /= 1024.0
        i += 1
    return ("%.1f %s" % (size, units[i])) if i else ("%d %s" % (size, units[i]))


def base_codename(codename):
    """'marble_in_global' -> 'marble'."""
    return codename.split("_")[0]


def aliyun_mirror(url):
    """The Singapore copy of a bigota file, if the URL is one."""
    if not url:
        return ""
    if BIGOTA in url:
        return url.replace(BIGOTA, ALIYUNS)
    return ""


# --------------------------------------------------------------- the build

def collect():
    """Read both indexes and return {base_codename: raw device}."""
    print("reading the update tracker index ...")
    tracker = parse_items(fetch(TRACKER_LATEST))
    print("  %d build(s)" % len(tracker))
    print("reading the tracker device names ...")
    tnames = parse_list_map(fetch(TRACKER_DEVICES))
    print("  %d name(s)" % len(tnames))
    print("reading the mirror index ...")
    xfu = parse_items(fetch(XFU_LATEST))
    print("  %d build(s)" % len(xfu))
    print("reading the device list ...")
    dnames = parse_map(fetch(XFU_DEVICES))
    print("  %d device(s)" % len(dnames))

    raw = {}

    def device(code):
        if code not in raw:
            raw[code] = {"code": code, "names": {}, "regions": [], "roms": []}
        return raw[code]

    # ---- the tracker: every Recovery and Fastboot build it knows ----------
    for rec in tracker:
        codename = rec.get("codename") or ""
        link = rec.get("link") or ""
        if not codename or not link:
            continue
        link = link.replace("http://", "https://")
        code = base_codename(codename)
        dev = device(code)
        raw_name = rec.get("name") or code
        region = region_of_name(raw_name)
        short = strip_region(raw_name, region)
        dev["names"][short] = dev["names"].get(short, 0) + 1
        dev["regions"].append(region)
        kind = "fastboot" if (rec.get("method") or "").lower() == "fastboot" else "recovery"
        version = rec.get("version") or ""
        dev["roms"].append({
            "v": version,
            "region": region,
            "kind": kind,
            "os": os_name(version),
            "android": rec.get("android") or "",
            "date": rec.get("date") or "",
            "size": rec.get("size") or "",
            "url": link,
            "mirrors": [],
        })

    # ---- the mirror index: a second pair of servers for the Recovery ROM --
    by_key = {}
    for dev in raw.values():
        for rom in dev["roms"]:
            if rom["kind"] == "recovery":
                by_key[(dev["code"], rom["region"], rom["v"])] = rom

    for rec in xfu:
        downloads = rec.get("downloads") or {}
        versions = rec.get("versions") or {}
        filename = rec.get("filename") or ""
        if not filename.startswith("fw_"):
            continue
        parts = filename[3:].split("_")
        if len(parts) < 2:
            continue
        code = parts[0]
        region = REGION_BY_NAME.get(rec.get("region") or "", rec.get("region") or "China")
        version = versions.get("miui") or ""
        rom = by_key.get((code, region, version))
        if not rom:
            continue
        for key in ("github", "osdn"):
            url = downloads.get(key) or ""
            if url and url not in rom["mirrors"]:
                rom["mirrors"].append(url)

    # ---- a name for every device -----------------------------------------
    for code, dev in raw.items():
        pretty = dnames.get(code) or ""
        if pretty:
            dev["name"] = pretty.split("/")[0].strip()
        else:
            best = ""
            best_count = 0
            for nm, count in sorted(dev["names"].items()):
                if count > best_count:
                    best, best_count = nm, count
            dev["name"] = best or code
        if not dev["name"]:
            items = tnames.get(code) or []
            dev["name"] = strip_region(items[0], region_of_name(items[0])) if items else code
    return raw


def slugify(name):
    """'POCO F5 Pro' -> 'poco-f5-pro'."""
    out = re.sub(r"[^a-zA-Z0-9]+", "-", name.lower()).strip("-")
    return out or "device"


def load_previous():
    """The index this script wrote last time, if there is one.

    It holds the friendly device names, the brand and the model numbers that
    were worked out by hand. The links in it are no good - they point at a
    page that sits in front of the file - but the naming is, so it is kept
    and only the links are replaced.
    """
    if not os.path.exists(OUT):
        return {}
    try:
        with open(OUT, encoding="utf-8") as fh:
            return json.load(fh).get("devices", {})
    except Exception:
        return {}


def build_devices(raw, previous):
    """Turn the raw builds into the device list the page shows.

    One phone can be sold under several names - the same codename is the POCO
    F5 in most of the world and the Redmi Note 12 Turbo in China - so a
    codename can carry more than one entry. The names, brands and model
    numbers come from the previous index; the builds come from the trackers.
    """
    prev_by_code = {}
    for slug, dev in previous.items():
        prev_by_code.setdefault(dev.get("code") or slug, []).append((slug, dev))

    devices = {}
    used_slugs = set()

    for code in sorted(raw):
        dev = raw[code]
        roms = dev["roms"]
        olds = prev_by_code.get(code) or []
        if olds:
            # Xiaomi reuses a codename across several phones - `serenity` is the
            # POCO C71, the C81X, the Redmi A5 and the A7 - and the trackers
            # cannot tell them apart. Each name therefore keeps the builds for
            # the regions it used to list. A name with no build of its own
            # falls back to the whole codename, so no phone ends up empty.
            entries = []
            for slug, old in olds:
                regions = set(old.get("regions") or [])
                mine = [r for r in roms if r["region"] in regions]
                if not mine:
                    mine = list(roms)
                entries.append((slug, old, mine))
        else:
            entries = [(slugify(dev["name"]), {}, list(roms))]

        for slug, old, mine in entries:
            # The same file can be listed twice by a tracker, and the newest
            # build has to be the one the table shows first.
            seen = set()
            clean = []
            for rom in sorted(mine, key=lambda r: (r.get("date") or "", r.get("v") or ""),
                              reverse=True):
                key = (rom["kind"], rom["url"])
                if key in seen:
                    continue
                seen.add(key)
                clean.append(rom)
            mine = clean
            name = old.get("name") or dev["name"]
            brand = old.get("brand") or brand_of(name)
            models = old.get("models") or ""
            regions = sorted({r["region"] for r in mine if r["region"]},
                             key=lambda r: (r != "Global", r))
            base_slug = old.get("slug") or slug
            slug = base_slug
            n = 2
            while slug in used_slugs:
                slug = "%s-%d" % (base_slug, n)
                n += 1
            used_slugs.add(slug)
            devices[slug] = {
                "slug": slug,
                "code": code,
                "name": name,
                "brand": brand,
                "models": models,
                "regions": regions,
                "count": len(mine),
                "roms": mine,
            }
    return devices


def add_mirrors(devices, limit=0):
    """Check the Singapore copy of every file and keep the ones that answer.

    A mirror that is missing would answer faster than a good one and win the
    race, so each candidate is asked once here, at build time, and only the
    ones that really have the file are written into the index.
    """
    jobs = []
    for dev in devices.values():
        for rom in dev["roms"]:
            candidate = aliyun_mirror(rom["url"])
            if candidate:
                jobs.append((rom, candidate))
    if limit:
        jobs = jobs[:limit]
    print("checking %d mirror(s) ..." % len(jobs))
    done = [0]

    def run(job):
        rom, candidate = job
        size = head_size(candidate)
        done[0] += 1
        if done[0] % 200 == 0:
            print("  %d/%d" % (done[0], len(jobs)))
        if size:
            rom["mirrors"].insert(0, candidate)
            if not rom.get("size"):
                rom["size"] = size_text(size)
            rom["bytes"] = size
        return size

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(run, jobs))
    print("  %d mirror(s) answered" % sum(1 for j in jobs if j[0].get("bytes")))


def main():
    ap = argparse.ArgumentParser(description="Refresh the ROM index.")
    ap.add_argument("--brand", help="only this brand (poco, redmi, xiaomi)")
    ap.add_argument("--slug", help="only one device")
    ap.add_argument("--limit", type=int, default=0, help="stop after N devices")
    ap.add_argument("--rebuild", action="store_true", help="ignore the cache")
    ap.add_argument("--list", action="store_true", help="list what is indexed")
    ap.add_argument("--no-mirrors", action="store_true",
                    help="do not check the second copy of every file")
    args = ap.parse_args()

    if args.list:
        if not os.path.exists(OUT):
            print("[!] there is no index yet - run this without --list")
            return 1
        with open(OUT, encoding="utf-8") as fh:
            data = json.load(fh)
        devices = data.get("devices", {})
        print("%d device(s), %d build(s)"
              % (len(devices), sum(len(d.get("roms", [])) for d in devices.values())))
        want = (args.brand or args.slug or "").lower()
        for code in sorted(devices):
            dev = devices[code]
            if want and want not in code.lower() and want not in dev["name"].lower():
                continue
            print("  %-28s %-34s %d build(s)  %s"
                  % (code, dev["name"], len(dev.get("roms", [])),
                     ", ".join(dev.get("regions", []))))
        return 0

    previous = load_previous()
    raw = collect()
    devices = build_devices(raw, previous)
    preview = False
    if args.brand:
        keep = {c: d for c, d in devices.items()
                if d["brand"].lower() == args.brand.lower()}
        devices = keep
        preview = True
    if args.slug:
        want = args.slug.lower()
        devices = {c: d for c, d in devices.items()
                   if c.lower() == want or want in d["name"].lower()}
        preview = True
    if args.limit:
        devices = dict(list(devices.items())[:args.limit])
        preview = True

    if not args.no_mirrors:
        add_mirrors(devices)

    # the newest build of every region first, then the rest
    for dev in devices.values():
        dev["roms"].sort(key=lambda r: (r["date"] or "", r["v"]), reverse=True)

    out = {
        "source": "XiaomiFirmwareUpdater update tracker + xmfirmwareupdater mirrors",
        "generated": time.strftime("%Y-%m-%d"),
        "devices": {c: devices[c] for c in sorted(devices)},
    }
    os.makedirs(DATA, exist_ok=True)

    # A filtered run is only a look at one part of the index. It is written
    # beside the real one so the full index - and the names in it - survive.
    out_path = OUT
    cat_path = CATALOG
    if preview:
        tag = (args.brand or args.slug or "part").lower().replace(" ", "-")
        out_path = os.path.join(DATA, "preview-%s.json" % tag)
        cat_path = os.path.join(DATA, "preview-%s.catalog.json" % tag)

    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, separators=(",", ":"))
    size = os.path.getsize(out_path)
    builds = sum(len(d["roms"]) for d in out["devices"].values())
    print("[OK] %d device(s), %d build(s) -> %s (%.2f MB)"
          % (len(out["devices"]), builds, out_path, size / 1048576.0))

    catalog = {
        "generated": out["generated"],
        "devices": sorted(
            [{"slug": d["slug"], "name": d["name"], "brand": d["brand"],
              "code": d["code"], "regions": d["regions"],
              "builds": len(d["roms"])}
             for d in out["devices"].values()],
            key=lambda d: (d["brand"], d["name"])),
    }
    with open(cat_path, "w", encoding="utf-8") as fh:
        json.dump(catalog, fh, ensure_ascii=False, indent=1)
    print("[OK] catalog -> %s" % cat_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
