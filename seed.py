"""Turn the YouTube batch files into website article stubs.

    python seed.py                 # create content/*.json (never overwrites)
    python seed.py --force         # rebuild the stubs
    python seed.py --report        # what devices / ROMs came out

Reads  C:/Users/vrohi/.romflasher/batches/*.txt   (original title, views, description)
       C:/Users/vrohi/.romflasher/generated/*.json  (the new English title + description)
Writes romflasher-site/content/<videoId>.json

A stub already carries everything a writer needs: the final title, the real
links, the device, the ROM name and the view count. Only `summary`, `body` and
`faq` are left for the writer.
"""

import argparse
import glob
import io
import json
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
ROMFLASHER = r"C:\Users\vrohi\.romflasher"
BATCHES = os.path.join(ROMFLASHER, "batches")
GENERATED = os.path.join(ROMFLASHER, "generated")

RECORD = re.compile(
    r"VIDEO ID:\s*(?P<id>[\w-]+)\s*\n"
    r"ORIGINAL TITLE:\s*(?P<otitle>.+?)\s*\n"
    r"VIEWS:\s*(?P<views>\d+)\s*\n"
    r"CURRENT LIVE TAGS:\s*(?P<tags>.*?)\s*\n"
    r"-+\s*\n"
    r"ORIGINAL DESCRIPTION:\s*\n(?P<odesc>.*?)\n-+\s*\n"
    r"TRANSCRIPT",
    re.S,
)

EMOJI = re.compile(
    "[" "\U0001F000-\U0001FAFF" "\U00002600-\U000027BF" "\U0001F1E6-\U0001F1FF"
    "\U00002190-\U000021FF" "\U0000FE0F" "\U00002B00-\U00002BFF" "]+"
)

URL = re.compile(r"https?://[^\s\)\]\>\}\"']+")

# links that should never go on the site
DROP = re.compile(
    r"(youtube\.com|youtu\.be|/subscribe|sub_confirmation|@Rom_Flasher|"
    r"instagram\.com|twitter\.com|x\.com/|facebook\.com|t\.me/|whatsapp|"
    r"play\.google\.com/store/apps)", re.I)

# ---------------------------------------------------------------- devices
DEVICE_PATTERNS = [
    r"POCO\s+[XFCM]\d+\s*(?:Pro|Plus|Ultra|5G)?",
    r"Redmi\s+K\d+\s*i?",
    r"Redmi\s+Note\s+\d+\s*(?:Pro\+?|Pro|Turbo|5G|4G)?",
    r"Redmi\s+Turbo\s+\d+",
    r"Redmi\s+\d+\s*(?:Pro|Plus|C|A|5G)?",
    r"(?:Xiaomi|Mi|MI)\s+Pad\s+\d+\s*(?:Pro|Plus)?",
    r"Xiaomi\s+\d+\s*[TSPK]?\s*(?:Pro|Plus|Ultra|Lite|Max|5G)?",
    r"(?:Mi|MI)\s+\d+\s*[A-Z]*\s*(?:Pro|Plus|Ultra|Lite)?",
    r"Pixel\s+\d+\s*(?:a|Pro|XL)?",
    r"OnePlus\s+\d+\s*(?:T|Pro|R)?",
    r"Samsung\s+Galaxy\s+[A-Z]\d+",
    r"Realme\s+\w+",
    r"iQOO\s+\w+",
    r"Motorola\s+\w+",
]

# non-technical uploads (shorts, talk) get grouped under the channel
CHANNEL_ONLY = re.compile(
    r"\b(shorts?|rap|battle|cheque|tech talk|update|live tools|help desk|"
    r"coding|zero filters|talk)\b", re.I)


def normalize_device(name):
    name = re.sub(r"\s+", " ", name).strip()
    name = re.sub(r"^(MI|Mi|mi)\s+Pad\b", "Xiaomi Pad", name)
    name = re.sub(r"^(MI|Mi)\s+", "Mi ", name)
    name = re.sub(r"^Poco\b", "POCO", name)
    name = re.sub(r"^REDMI\b", "Redmi", name)
    name = re.sub(r"^XIAOMI\b", "Xiaomi", name)
    return name

ROM_PATTERNS = [
    (r"\bHyperOS\s*\d?\.?\d*", "HyperOS"),
    (r"\bMIUI\s*\d+", "MIUI"),
    (r"\bLineageOS\s*\d*", "LineageOS"),
    (r"\bEvolution\s*X\b", "Evolution X"),
    (r"\bPixelOS\b", "PixelOS"),
    (r"\bPixel\s*Experience\b", "Pixel Experience"),
    (r"\bcrDroid\b", "crDroid"),
    (r"\bDerpFest\b", "DerpFest"),
    (r"\bRisingOS\b", "RisingOS"),
    (r"\bAOSP\b", "AOSP"),
    (r"\bAxionOS\b", "AxionOS"),
    (r"\bProject\s+Matrixx\b", "Project Matrixx"),
    (r"\bNameless\b", "Nameless ROM"),
    (r"\bParanoid\b", "Paranoid Android"),
    (r"\bOrangeFox\b", "OrangeFox"),
    (r"\bTWRP\b", "TWRP"),
    (r"\bMagisk\b", "Magisk"),
    (r"\bKernelSU\b", "KernelSU"),
    (r"\bAPatch\b", "APatch"),
    (r"\bKernel\b", "Kernel"),
    (r"\bFastboot\s+ROM\b", "Fastboot ROM"),
    (r"\bRecovery\s+ROM\b", "Recovery ROM"),
    (r"\bRoot\b|\bRooting\b", "Root"),
    (r"\bUnlock\b.{0,20}\bBootloader\b", "Bootloader unlock"),
    (r"\bStock\s+ROM\b|\bBack\s+to\s+Stock\b", "Stock ROM"),
    (r"\bBootloop\b", "Bootloop fix"),
    (r"\bFRP\b", "FRP"),
    (r"\bPlay\s+Integrity\b|\bSafetyNet\b", "Play Integrity"),
    (r"\bGCam\b|\bGoogle\s+Camera\b", "GCam"),
]

TOPICS = [
    "Flash", "Install", "Root", "Unlock", "Bootloader", "Recovery", "Kernel",
    "HyperOS", "MIUI", "Custom ROM", "Debloat", "Backup", "Restore", "Bootloop",
    "Battery", "Performance", "Gaming", "Camera", "GCam", "Update", "Downgrade",
]

GENERIC = re.compile(r"any\s+(android|xiaomi|phone|device)", re.I)


def clean(text):
    text = EMOJI.sub(" ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip(" -|·.")


def slugify(title, vid):
    base = clean(title).lower()
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    words, out = base.split("-"), []
    for w in words:
        if len("-".join(out + [w])) > 62:
            break
        out.append(w)
    base = "-".join(out) or vid
    return base


def first_sentence(text):
    text = clean(text)
    if not text:
        return ""
    m = re.split(r"(?<=[.!?])\s+", text, maxsplit=1)
    s = m[0].strip()
    if len(s) > 158:
        s = s[:155].rsplit(" ", 1)[0] + "..."
    return s


def device_from_generic(hay):
    m = GENERIC.search(hay)
    if not m:
        return ""
    return "Any Xiaomi" if m.group(1).lower().startswith("xia") else "Any Android"


def pick_device(text, tags):
    hay = " ".join([text, tags])
    for pat in DEVICE_PATTERNS:
        m = re.search(pat, hay)
        if m:
            return normalise_device(clean(m.group(0)))
    generic = device_from_generic(hay)
    if generic:
        return generic
    if re.search(r"\b(shorts?|rap battle|cheque|tech talk|desk|live)\b", hay, re.I):
        return "Channel"
    return ""


def normalise_device(name):
    name = re.sub(r"\s+", " ", name).strip()
    name = re.sub(r"^(?:\U0001F600)?", "", name)
    name = re.sub(r"^(?:MI|Mi)\s+pad", "Xiaomi Pad", name, flags=re.I)
    name = re.sub(r"^(?:MI|Mi)\s+", "Mi ", name)
    name = re.sub(r"^(?:POCO|Poco)\b", "POCO", name)
    name = re.sub(r"^(?:REDMI|Redmi)\b", "Redmi", name)
    return name


def pick_rom(text):
    for pat, name in ROM_PATTERNS:
        if re.search(pat, text, re.I):
            return name
    return ""


def pick_tags(text, device, rom):
    out = []
    for word in TOPICS:
        if re.search(r"\b%s\b" % re.escape(word), text, re.I):
            out.append(word)
    if device and device != "Any Android":
        out.insert(0, device)
    if rom:
        out.insert(0, rom)
    seen, uniq = set(), []
    for t in out:
        if t.lower() not in seen:
            seen.add(t.lower())
            uniq.append(t)
    return uniq[:5]


def blocks_from_batches():
    found = {}
    for path in sorted(glob.glob(os.path.join(BATCHES, "*.txt"))):
        text = io.open(path, encoding="utf-8", errors="replace").read()
        for m in RECORD.finditer(text):
            found[m.group("id")] = {
                "id": m.group("id"),
                "original_title": clean(m.group("otitle")),
                "views": int(m.group("views")),
                "live_tags": clean(m.group("tags")),
                "original_desc": m.group("odesc"),
            }
    return found


def load_generated():
    out = {}
    for path in sorted(glob.glob(os.path.join(GENERATED, "*.json"))):
        try:
            data = json.load(io.open(path, encoding="utf-8"))
        except Exception:                                          # noqa: BLE001
            continue
        out[data["id"]] = data
    return out


def load_dates():
    """publishedAt for every video, from the API backups."""
    out = {}
    for name in ("backup-videos-20261018-180903.json", "extra_videos.json"):
        path = os.path.join(ROMFLASHER, name)
        if not os.path.exists(path):
            continue
        try:
            data = json.load(io.open(path, encoding="utf-8"))
        except Exception:                                          # noqa: BLE001
            continue
        items = data.get("items", []) if isinstance(data, dict) else data
        for item in items:
            raw = str(item.get("publishedAt") or "").strip()
            if re.match(r"^\d{8}$", raw):                          # 20261019
                out[item["id"]] = "%s-%s-%s" % (raw[:4], raw[4:6], raw[6:8])
            elif re.match(r"^\d{4}-\d{2}-\d{2}", raw):             # 2026-10-18T09:12
                out[item["id"]] = raw[:10]
    return out


def strip_filler(description):
    """Drop the links block and the hashtag line - those are rendered elsewhere."""
    text = re.split(r"🔗\s*LINKS\s*/\s*DOWNLOADS\s*:", description or "", maxsplit=1)[0]
    out = []
    for line in text.splitlines():
        if re.match(r"^\s*#[A-Za-z0-9_#\s]+$", line):
            continue
        out.append(line)
    return "\n".join(out).strip()


BULLET = re.compile(r"^[•\-\*]\s*(?P<label>[^\n]{2,90}?)\s*[—–-]\s*(?P<url>https?://\S+)\s*$", re.M)


def labels_from(description):
    """Pull the '• 🧩 MIUI Fastboot ROM — https://…' bullets into a url -> label map."""
    out = {}
    for m in BULLET.finditer(description or ""):
        label = clean(m.group("label"))
        label = re.sub(r"^[^\w]+", "", label).strip()
        label = label.replace("Rom Flasher Tool (Free Android App)", "Rom Flasher tool (free)")
        url = m.group("url").rstrip(".,;)")
        if label and url not in out:
            out[url] = label
    return out


def links_from(description, tool_url):
    known = labels_from(description)
    links, seen = [], set()
    for url in URL.findall(description or ""):
        url = url.rstrip(".,;)")
        if DROP.search(url) or url in seen:
            continue
        seen.add(url)
        low = url.lower()
        if url in known:
            label = known[url]
        elif "github.com/romflasher3419-spec/rom-flasher-tool" in low:
            label = "Rom Flasher tool (free)"
        elif "drive.google.com" in low:
            label = "Google Drive download"
        elif "sourceforge" in low:
            label = "SourceForge download"
        elif "mega.nz" in low:
            label = "MEGA download"
        elif "androidfilehost" in low:
            label = "AndroidFileHost download"
        elif "firmware" in low or "miui" in low or "xiaomi" in low:
            label = "Official firmware"
        elif low.endswith(".zip"):
            label = "ROM / recovery zip"
        elif low.endswith((".img", ".tar", ".tar.gz", ".7z")):
            label = "Image / archive"
        else:
            label = ""
        links.append({"label": label, "url": url})
    return links


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="overwrite existing stubs")
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    os.makedirs(CONTENT, exist_ok=True)
    batches = blocks_from_batches()
    generated = load_generated()
    dates = load_dates()

    print("batches : %d video(s)" % len(batches))
    print("generated: %d video(s)" % len(generated))
    print("dates   : %d video(s)" % len(dates))

    ids = sorted(set(batches) | set(generated))
    tool_url = "https://github.com/romflasher3419-spec/rom-flasher-tool/releases/latest"

    devices, roms, made, skipped, used_slugs = Counter(), Counter(), 0, 0, {}
    for vid in ids:
        gen = generated.get(vid, {})
        batch = batches.get(vid, {})
        title = clean(gen.get("title") or batch.get("original_title") or vid)
        description = gen.get("description") or ""

        slug = slugify(title, vid)
        if slug in used_slugs and used_slugs[slug] != vid:
            slug = "%s-%s" % (slug, vid[-4:])
        used_slugs[slug] = vid

        text = " ".join([title, description[:1200], batch.get("live_tags", "")])
        device = pick_device(title, batch.get("live_tags", "")) or pick_device(text, "")
        rom = pick_rom(title) or pick_rom(text)

        stub = {
            "id": vid,
            "slug": slug,
            "title": title,
            "blurb": first_sentence(description) or title,
            "device": device,
            "rom": rom,
            "android": "",
            "views": batch.get("views", 0),
            "published": dates.get(vid, ""),
            "url": "https://youtu.be/%s" % vid,
            "tags": pick_tags(text, device, rom),
            "summary": "",
            "body": "",
            "video_description": strip_filler(description),
            "links": links_from(description, tool_url),
            "faq": [],
        }

        path = os.path.join(CONTENT, "%s.json" % vid)
        if os.path.exists(path):
            try:
                old = json.load(io.open(path, encoding="utf-8"))
            except Exception:                                      # noqa: BLE001
                old = {}
            # never throw away writing that is already in place
            for keep in ("summary", "body", "faq", "android"):
                if old.get(keep):
                    stub[keep] = old[keep]
            if old.get("body") and not args.force:
                skipped += 1
                continue
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(stub, fh, ensure_ascii=False, indent=1)
        made += 1
        devices[device or "(unknown)"] += 1
        roms[rom or "(unknown)"] += 1

    print("written : %d   skipped: %d" % (made, skipped))

    if args.report or made:
        print("\ndevices:")
        for name, n in devices.most_common():
            print("   %-28s %d" % (name, n))
        print("\nroms / topics:")
        for name, n in roms.most_common():
            print("   %-28s %d" % (name, n))
    return 0


if __name__ == "__main__":
    sys.exit(main())
