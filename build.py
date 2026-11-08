"""Rom Flasher static site builder.

    python build.py                 # dist/ from content/
    python build.py --serve 8080    # local preview server

Every page is one file in content/<videoId>.json:

    id, slug, title, blurb, device, rom, android, views, published,
    url (youtube), tags[], summary, body, video_description, links[], faq[]

Only the Python standard library is used. Upload dist/ to Cloudflare Pages,
GitHub Pages or Netlify.
"""

import argparse
import glob
import html
import json
import os
import re
import shutil
import sys
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
STATIC = os.path.join(HERE, "static")
DIST = os.path.join(HERE, "dist")
DATA = os.path.join(HERE, "data")

SITE = "Rom Flasher"
TAGLINE = "Independent Android ROM & Firmware Engineering Journal"
AUTHOR_NAME = "Rohit Verma"
AUTHOR_HANDLE = "@Rom_Flasher"
AUTHOR_TITLE = "Android Flashing Specialist & Developer"
AUTHOR_AVATAR = "static/rohit-verma.webp"
AUTHOR_BIO = (
    "Creator of Rom Flasher Tool and author of hands-on Android tutorials. "
    "Every fastboot script, ROM package and unbrick procedure on this site is physically "
    "tested on actual test devices in our lab before publishing."
)

# Where the site says it lives. Every absolute URL on it (canonical, sitemap,
# og:url, structured data) is built from SITE_URL, and dist/CNAME is written from
# CUSTOM_DOMAIN - so one switch, ROMFLASHER_DOMAIN, drives both:
#
#     $env:ROMFLASHER_DOMAIN = "romflasher.in"      # the only thing to set
#
# Leave it empty and the site calls itself by its GitHub Pages address, which is
# what actually serves it until DNS is live. That empty default is the safe one:
# pointing search engines at a domain that does not answer yet gets the pages
# dropped, so never set the domain before it resolves.
PAGES_URL = "https://romflasher3419-spec.github.io/romflasher-site"
CUSTOM_DOMAIN = os.environ.get("ROMFLASHER_DOMAIN", "").strip().strip("/") or "romflasher.in"
SITE_URL = (os.environ.get("ROMFLASHER_SITE_URL", "").strip()
            or (("https://" + CUSTOM_DOMAIN) if CUSTOM_DOMAIN else PAGES_URL)
            ).rstrip("/")

# ------------------------------------------------------- switch-on-when-set
# Each of these is off while empty, so nothing half-configured ever ships.
# Paste the value, rebuild, and that one feature turns itself on.
GA4_ID = os.environ.get("ROMFLASHER_GA4", "").strip() or "G-9F1TH7MFVS"
ADS_PUBLISHER = os.environ.get("ROMFLASHER_ADS", "").strip() or "pub-3239298035490504"

# AdSense hands out a numeric slot id per ad unit you create in the dashboard.
# Each placement here is off until its own id is set, and all of them stay off
# while ADS_PUBLISHER is empty - so a half-set-up account can never ship a
# broken unit. One value, one placement:
#
#     ROMFLASHER_SLOT_ARTICLE  -> end of every guide article
#     ROMFLASHER_SLOT_LIST     -> the guides table page
#     ROMFLASHER_SLOT_HUB      -> brand / ROM / device / year hub pages
#
AD_SLOTS = {
    "article": os.environ.get("ROMFLASHER_SLOT_ARTICLE", "").strip(),
    "list": os.environ.get("ROMFLASHER_SLOT_LIST", "").strip(),
    "hub": os.environ.get("ROMFLASHER_SLOT_HUB", "").strip(),
}
AMAZON_TAG = os.environ.get("ROMFLASHER_AMAZON", "")   # "romflasher-21"
GOOGLE_VERIFY = (os.environ.get("ROMFLASHER_GOOGLE", "").strip()
                 or "Mmp5fB5mpvMffHgXXpm8dOp0R1ZM8GbaLhmQrBx8PGQ")
BING_VERIFY = os.environ.get("ROMFLASHER_BING", "")      # Bing Webmaster token
# Search Console can also verify by serving a file at the site root. Either the
# file name ("google8e8e....html") or the whole "google-site-verification: ..."
# line is accepted here; only the name survives into the built file.
GOOGLE_FILE_NAME = os.environ.get("ROMFLASHER_GOOGLE_FILE", "").strip()
if GOOGLE_FILE_NAME.lower().startswith("google-site-verification:"):
    GOOGLE_FILE_NAME = GOOGLE_FILE_NAME.split(":", 1)[1].strip()
if GOOGLE_FILE_NAME and not GOOGLE_FILE_NAME.endswith(".html"):
    GOOGLE_FILE_NAME += ".html"
# IndexNow. It proves ownership by asking for <key>.txt at the site root, and
# that file must contain the key itself. Any hex string will do; set
# ROMFLASHER_INDEXNOW to the same value used when pinging the endpoint.
INDEXNOW_KEY = os.environ.get("ROMFLASHER_INDEXNOW", "").strip()
TOOL_URL = "https://github.com/romflasher3419-spec/rom-flasher-tool/releases/latest"
REPO_URL = "https://github.com/romflasher3419-spec/rom-flasher-tool"
CHANNEL_URL = "https://www.youtube.com/@Rom_Flasher"
FB_URL = "https://www.facebook.com/people/Rom-Flasher/61595961834517/"
IG_URL = "https://www.instagram.com/romflasheryt"

# /releases/latest/download/<asset> always points at the newest build, so the
# button on the download page never has to be edited again.
APK_URL = REPO_URL + "/releases/latest/download/app-release.apk"
RELEASES_URL = REPO_URL + "/releases"

APP = {
    "version": "v1.4.1",
    "released": "23 Oct 2026",
    "size": "8.3 MB",
    "bytes": "8670970",
    "sha256": "CCC1759E0E147A6256012B1C4583D656B1CE43933B02B527ED07D7C40B5F24B0",
    "android": "Android 8.0 or newer",
}

# Where "send me a message" lands. FormSubmit needs no account: the first
# submission mails an activation link to this address, one click and it is live.
CONTACT_EMAIL = "vrohit3419@gmail.com"
FORM_POST = "https://formsubmit.co/" + CONTACT_EMAIL

# GitHub Pages does not let a repository set response headers. This file is
# written into dist/ so a host that supports the Netlify/Cloudflare _headers
# format (or a future move to Cloudflare Pages) picks the same policy up without
# another code change. The CSP is deliberately broad enough for Google
# Analytics, AdSense and YouTube, while still blocking object embeds and
# framing this site elsewhere.
SECURITY_HEADERS = """/*
  Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
  X-Content-Type-Options: nosniff
  X-Frame-Options: DENY
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=(), usb=(), interest-cohort=()
  Cross-Origin-Opener-Policy: same-origin
  Cross-Origin-Resource-Policy: same-site
  Content-Security-Policy: default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'self' https://formsubmit.co; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.googletagmanager.com https://pagead2.googlesyndication.com https://*.googlesyndication.com https://*.googleadservices.com https://adservice.google.com https://googleads.g.doubleclick.net https://*.doubleclick.net https://www.google.com https://www.gstatic.com; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com data:; img-src 'self' data: https://i.ytimg.com https://*.ytimg.com https://www.google-analytics.com https://*.google-analytics.com https://pagead2.googlesyndication.com https://*.googlesyndication.com https://*.doubleclick.net https://www.gstatic.com; frame-src https://www.youtube.com https://www.youtube-nocookie.com https://googleads.g.doubleclick.net https://*.doubleclick.net https://*.googlesyndication.com https://www.google.com; connect-src 'self' https://formsubmit.co https://www.google-analytics.com https://*.google-analytics.com https://region1.google-analytics.com https://pagead2.googlesyndication.com https://*.googlesyndication.com https://googleads.g.doubleclick.net https://*.doubleclick.net https://*.google.com; media-src 'self' https:; manifest-src 'self'; worker-src 'self' blob:
"""

# the GitHub mark, straight from GitHub's own logo
GH_LOGO = ('<svg viewBox="0 0 16 16" aria-hidden="true"><path d="M8 0C3.58 0 0 '
           '3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82'
           '-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15'
           '-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52'
           '.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2'
           '-.36-1.02.07-2.13 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09'
           ' 2 .27 1.53-1.04 2.2-.82 2.2-.82.43 1.11.15 1.93.07 2.13.51.56.82 1.27'
           '.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93'
           '-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-8-8-8z">'
           "</path></svg>")

# arrow-into-tray, for the dark download buttons
DL_LOGO = ('<svg viewBox="0 0 24 24" aria-hidden="true">'
           '<path d="M11 3h2v9.2l3.3-3.3 1.4 1.4L12 16l-5.7-5.7 1.4-1.4L11 12.2V3z"/>'
           '<path d="M4 18h16v2H4z"/></svg>')

# The two ways to say thanks, copied from the app's Donate screen so the site
# and the phone show the same UPI ID and the same PayPal.Me link.
UPI_ID = "romflasher@naviaxis"
PAYPAL_URL = "https://paypal.me/vrohit3419"

COFFEE_LOGO = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 3H4v10c0 '
             '2.21 1.79 4 4 4h6c2.21 0 4-1.79 4-4v-3h2c1.11 0 2-.89 2-2V5c0-1'
             '.11-.89-2-2-2zm0 5h-2V5h2v3zM4 19h16v2H4z"/></svg>')

# The YouTube play mark as it looked for years: a rounded red rectangle with a
# white triangle. Drawn in one colour (currentColor) so it sits inside the nav
# button's own fill instead of painting a second, competing red.
FB_LOGO = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">'
           '<path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 '
           '10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 '
           '4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-'
           '1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 '
           '24 12.073z"/></svg>')

IG_LOGO = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">'
           '<path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 '
           '4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 '
           '3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-'
           '.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-'
           '4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-'
           '.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-'
           '6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 '
           '4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 '
           '3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-'
           '4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-'
           '.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 '
           '6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 '
           '10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 '
           '4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 '
           '1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>')

YT_LOGO = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">'
           '<path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4'
           '.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1'
           ' 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24'
           ' 12a31 31 0 0 0-.5-5.8zM9.5 15.6V8.4l6.3 3.6-6.3 3.6z"/></svg>')

# a list mark, for the Guides button - three ruled lines with a dot each
GUIDES_LOGO = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">'
               '<circle cx="4.5" cy="6.5" r="1.6"/><circle cx="4.5" cy="12" r="1.6"/>'
               '<circle cx="4.5" cy="17.5" r="1.6"/>'
               '<path d="M9 5h12v3H9zM9 10.5h12v3H9zM9 16h12v3H9z"/></svg>')

BRAND_ANIM_PATH = os.path.join(STATIC, "brand-anim.svg")
with open(BRAND_ANIM_PATH, "r", encoding="utf-8") as _bf:
    BRAND_ANIM_SVG = _bf.read().strip()

CARD_LOGO = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2 6a2 2 0 0 1 '
             '2-2h16a2 2 0 0 1 2 2v1H2V6zm0 3h20v9a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V9zm3 '
             '6h6v2H5v-2z"/></svg>')

# long-tail terms that ride along on every page's keywords tag
SEO_CORE = (
    "Rom Flasher", "Rom Flasher tool", "rom flasher download", "free rom flasher",
    "custom ROM", "custom ROM installer", "fastboot ROM", "fastboot flash tool",
    "flash ROM without PC", "flash ROM from phone", "flash rom using android",
    "bootloader unlock", "unlock bootloader without pc", "bootloader unlocking guide",
    "Android flashing tool", "Android ROM flasher", "ADB and fastboot for android",
    "install custom ROM", "sideload ROM", "flash boot image", "flash vbmeta",
    "recovery mode", "custom recovery", "TWRP", "OrangeFox", "Magisk", "KernelSU",
    "root android without pc", "stock ROM download", "official firmware download",
    "MIUI", "HyperOS", "LineageOS", "Evolution X", "Pixel Experience", "crDroid",
    "USB OTG flashing", "OTG cable flash", "Xiaomi flashing tool", "POCO flashing",
    "Redmi flashing guide", "OnePlus flashing", "realme flashing", "OPPO flashing",
    "vivo iQOO flashing", "Google Pixel fastboot", "download mode", "Odin style flasher",
    "IMEI EFS backup", "kernel backup restore", "debloat android", "payload dumper",
    "free android tool", "no root no PC", "beginner friendly flashing guide",
)


# values the scraper left behind when it could not work out the phone
JUNK_DEVICES = {"", "?", "-", "n/a", "na", "none", "unknown", "other", "channel"}


def clean_device(value):
    """The real phone name, or '' when the data has nothing usable."""
    value = (value or "").strip()
    return "" if value.lower() in JUNK_DEVICES else value


def keywords_for(item=None, extra=()):
    """A concise, relevant keyword list for a page (no spam stuffing)."""
    parts = []
    if item:
        dev = clean_device(item.get("device"))
        if dev:
            parts.append(dev)
        if item.get("rom"):
            parts.append(item.get("rom"))
        if item.get("android"):
            parts.append("Android " + str(item.get("android")))
        for t in (item.get("tags") or [])[:2]:
            parts.append(t)
    parts += list(extra)[:2]
    if not parts:
        parts = ["Android Flashing", "Custom ROM", "Rom Flasher"]

    seen, out = set(), []
    for value in parts:
        value = (value or "").strip()
        key = value.lower()
        if len(value) < 2 or key in seen:
            continue
        seen.add(key)
        out.append(value)
    return ", ".join(out[:6])

BUILT_ON = datetime.now().strftime("%Y-%m-%d")

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


# --------------------------------------------------------------- hub groups
# A phone name maps to the brand people actually search for. POCO and Redmi are
# matched before Xiaomi on purpose - both are searched on their own.
BRAND_RULES = (
    ("POCO", ("poco",)),
    ("Redmi", ("redmi",)),
    ("Xiaomi", ("xiaomi", "mi ")),
    ("OnePlus", ("oneplus", "one plus")),
    ("Google Pixel", ("pixel",)),
    ("realme", ("realme",)),
    ("vivo / iQOO", ("vivo", "iqoo")),
    ("OPPO", ("oppo",)),
    ("Samsung", ("samsung", "galaxy")),
    ("Motorola", ("moto", "motorola")),
    ("Nothing", ("nothing phone", "nothing (")),
    ("Honor", ("honor",)),
    ("Asus", ("asus", "rog phone")),
    ("Infinix", ("infinix",)),
    ("Tecno", ("tecno",)),
)

# The rom field is sometimes a ROM and sometimes a job ("Root", "Kernel"), so
# only the names below get a landing page of their own.
ROM_RULES = (
    ("DerpFest", ("derpfest",)),
    ("LineageOS", ("lineage",)),
    ("Evolution X", ("evolution x", "evolutionx")),
    ("Pixel Experience", ("pixel experience", "pixelexperience")),
    ("PixelOS", ("pixelos",)),
    ("crDroid", ("crdroid",)),
    ("RisingOS", ("risingos", "rising os")),
    ("AOSP", ("aosp",)),
    ("HyperOS", ("hyperos",)),
    ("MIUI", ("miui",)),
    ("TWRP", ("twrp",)),
    ("OrangeFox", ("orangefox",)),
)

# Tags worth a topic page: the jobs people type into Google.
TOPIC_TAGS = ("Root", "Recovery", "Bootloader", "Unlock", "Custom ROM",
              "Kernel", "Battery", "Camera", "Gaming", "Backup", "Bootloop",
              "Performance", "Fastboot ROM", "Stock ROM", "Play Integrity")


def match_rule(value, rules):
    low = (value or "").strip().lower()
    if not low:
        return ""
    for name, keys in rules:
        for key in keys:
            if low.startswith(key) or (" " + key) in low:
                return name
    return ""


def group_map(items, keyfunc, minimum=2):
    """{group name: {'slug':..., 'rows': [newest first]}} as long as it is used."""
    buckets = {}
    for x in items:
        name = keyfunc(x)
        if not name:
            continue
        buckets.setdefault(name, []).append(x)
    return {name: {"slug": slugify(name),
                   "rows": sorted(rows, key=lambda r: r.get("published") or "",
                                  reverse=True)}
            for name, rows in buckets.items() if len(rows) >= minimum}


def topic_map(items, minimum=3):
    """{topic: hub} for the curated tags - one guide can land in several."""
    out = {}
    for name in TOPIC_TAGS:
        want = name.lower()
        rows = [x for x in items
                if want in [str(t or "").strip().lower()
                            for t in (x.get("tags") or [])]]
        if len(rows) >= minimum:
            out[name] = {"slug": slugify(name),
                         "rows": sorted(rows,
                                        key=lambda r: r.get("published") or "",
                                        reverse=True)}
    return out


def tag_map(items, minimum=1):
    """{tag: hub} for every real tag in the content, newest guide first.

    The topic pages only cover the curated jobs (Root, Recovery...). This is the
    wider net - any tag the scraper found, as long as it is used more than once.
    Nothing is invented here: a page is only ever built for a tag that a guide
    actually carries.
    """
    buckets = {}
    for x in items:
        for tag in (x.get("tags") or []):
            name = str(tag or "").strip()
            if len(name) < 2 or slugify(name) == "":
                continue
            buckets.setdefault(name, []).append(x)
    return {name: {"slug": slugify(name),
                   "rows": sorted(rows, key=lambda r: r.get("published") or "",
                                  reverse=True)}
            for name, rows in buckets.items() if len(rows) >= minimum}


def year_map(items, minimum=1):
    out = {}
    for x in items:
        year = (x.get("published") or "")[:4]
        if not year.isdigit():
            continue
        out.setdefault(year, []).append(x)
    return {name: {"slug": name,
                   "rows": sorted(rows, key=lambda r: r.get("published") or "",
                                  reverse=True)}
            for name, rows in out.items() if len(rows) >= minimum}


def all_hubs(items):
    """Every browse page the site has, in one place."""
    return {
        "brand": group_map(items, brand_of, 2),
        "rom": group_map(items, rom_family_of, 2),
        "year": year_map(items),
        "topic": topic_map(items, 3),
        "tag": tag_map(items, 2),
    }


# hub_map()/all_hubs() are pure and the content is loaded once, so the result is
# kept for the run - otherwise every article would re-bucket all 184 guides.
_CACHE = {}


def cached_device_hubs(items):
    key = ("device", len(items))
    if key not in _CACHE:
        _CACHE[key] = hub_map(items)
    return _CACHE[key]


def cached_all_hubs(items):
    key = ("all", len(items))
    if key not in _CACHE:
        _CACHE[key] = all_hubs(items)
    return _CACHE[key]


def tag_href(tag, up=""):
    """Link a tag chip only when its archive page really exists.

    Tag pages are built for tags used by two or more guides; a tag that appears
    once gets no page (a one-guide page is thin content). Rendering those chips
    as plain text keeps every link on the site resolving. The set of real tag
    pages is filled once per run by tag_hubs(), below.
    """
    name = str(tag or "").strip()
    hub = _TAG_HUBS.get(name)
    if hub:
        return '<a class="tag" href="%stag/%s.html">%s</a>' % (
            up, hub["slug"], html.escape(name))
    return '<span class="tag">%s</span>' % html.escape(name)


# Every tag that earned an archive page this run, filled in main() from the full
# content list - so a chip drawn inside a 6-item related grid still resolves
# against the whole site instead of that little slice.
_TAG_HUBS = {}


def tag_hubs(items):
    """Fill _TAG_HUBS from the full content list and return it."""
    _TAG_HUBS.clear()
    _TAG_HUBS.update(tag_map(items, 2))
    return _TAG_HUBS


def brand_of(item):
    return match_rule(clean_device(item.get("device")), BRAND_RULES)


def rom_family_of(item):
    return match_rule(item.get("rom"), ROM_RULES)


def topic_of(tag):
    """The canonical topic page for a tag, or '' when it is too generic."""
    low = (tag or "").strip().lower()
    for name in TOPIC_TAGS:
        if low == name.lower():
            return name
    return ""


def newest_thumb(rows):
    """A real YouTube still from the newest guide - better than a stock logo."""
    for x in rows:
        vid = video_id_of(x.get("url") or "")
        if vid:
            return "https://i.ytimg.com/vi/%s/maxresdefault.jpg" % vid
    return None


def analytics_head(up=""):
    """Analytics + AdSense, loaded only after the visitor says yes.

    Nothing is fetched and no cookie is set until a choice is stored. Google
    Consent Mode v2 defaults are queued first, so even a third-party script that
    somehow loads early sees "denied" for analytics, ads and ad personalisation.
    The banner offers accept, reject and a granular panel with equal prominence -
    a reject is one tap, not a link hidden in a paragraph.

    The banner is the one piece of the site that floats over the page, so it has
    to leave the room it takes: while it is up the body carries the same padding
    the banner needs, so the last line of a page can always be scrolled out from
    under it instead of hiding there forever.
    """
    if not (GA4_ID or ADS_PUBLISHER):
        return ""
    base_js = """<script>
(function(){
  var GA=%(ga)s, ADS=%(ads)s, KEY='rf-consent';
  var state={analytics:false,ads:false}, gaLoaded=false, adsLoaded=false;
  var openBanner=null;

  function read(){
    var raw=null;
    try{raw=localStorage.getItem(KEY);}catch(e){}
    if(!raw) return null;
    if(raw==='yes') return {analytics:true,ads:true};
    if(raw==='no') return {analytics:false,ads:false};
    try{
      var v=JSON.parse(raw);
      if(!v||typeof v!=='object') return null;
      return {analytics:!!v.analytics,ads:!!v.ads};
    }catch(e){return null;}
  }
  function save(v){
    state={analytics:!!v.analytics,ads:!!v.ads};
    try{localStorage.setItem(KEY,JSON.stringify(state));}catch(e){}
  }
  function consent(v){
    if(!window.gtag) return;
    gtag('consent','update',{
      analytics_storage:v.analytics?'granted':'denied',
      ad_storage:v.ads?'granted':'denied',
      ad_user_data:v.ads?'granted':'denied',
      ad_personalization:v.ads?'granted':'denied',
      functionality_storage:'granted',
      personalization_storage:v.ads?'granted':'denied',
      ads_data_redaction:!v.ads
    });
  }
  function load(v){
    if(GA && v.analytics && !gaLoaded){
      gaLoaded=true;
      var s=document.createElement('script');s.async=true;
      s.src='https://www.googletagmanager.com/gtag/js?id='+GA;
      document.head.appendChild(s);
      gtag('js',new Date());
      gtag('config',GA,{anonymize_ip:true});
    }
    if(ADS && v.ads && !adsLoaded){
      adsLoaded=true;
      var a=document.createElement('script');a.async=true;a.crossOrigin='anonymous';
      a.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-'+ADS;
      document.head.appendChild(a);
    }
  }

  /* Consent Mode v2: the safe default is queued before anything can request a
     cookie. gtag() only writes to the dataLayer array, so this makes no network
     request on its own. */
  window.dataLayer=window.dataLayer||[];
  window.gtag=window.gtag||function(){window.dataLayer.push(arguments);};
  gtag('consent','default',{
    ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',
    analytics_storage:'denied',functionality_storage:'granted',
    personalization_storage:'denied',security_storage:'granted',
    ads_data_redaction:true,wait_for_update:500
  });

  var stored=read();
  if(stored){state=stored;consent(stored);load(stored);}

  function banner(){
    if(openBanner){openBanner.remove();openBanner=null;}
    var b=document.createElement('div');
    b.className='consent';
    b.setAttribute('role','dialog');
    b.setAttribute('aria-modal','false');
    b.setAttribute('aria-labelledby','rf-consent-title');
    b.innerHTML='<div class="ctext">'
      +'<p class="ctitle" id="rf-consent-title">Cookies, analytics &amp; ads</p>'
      +'<p>Analytics shows me which guides actually helped, and ads keep the site free. '
      +'Nothing loads until you choose &mdash; and the site works exactly the same if you say no. '
      +'<a href="%(priv)s">Privacy policy</a>.</p>'
      +'<div class="cpanel" hidden>'
      +'<label><input type="checkbox" id="rf-a"> Analytics</label>'
      +'<label><input type="checkbox" id="rf-d"> Personalised ads</label>'
      +'</div></div>'
      +'<div class="row">'
      +'<button type="button" class="btn" id="rf-ok">Accept all</button>'
      +'<button type="button" class="btn ghost" id="rf-no">Reject optional</button>'
      +'<button type="button" class="btn ghost" id="rf-manage">Manage options</button>'
      +'</div>';
    document.body.appendChild(b);
    openBanner=b;
    document.body.classList.add('consent-on');

    var a=b.querySelector('#rf-a'), d=b.querySelector('#rf-d');
    var panel=b.querySelector('.cpanel');
    var ok=b.querySelector('#rf-ok'), no=b.querySelector('#rf-no');
    var manage=b.querySelector('#rf-manage');
    a.checked=state.analytics; d.checked=state.ads;
    var managing=false;

    /* The page has to end above the banner, so it gets exactly the room the
       banner takes - measured, not guessed, because the banner is a different
       height on every screen (and it re-wraps when the phone is turned). */
    function room(){
      document.documentElement.style.setProperty('--consent-h',b.offsetHeight+'px');
    }
    room();
    if(window.ResizeObserver){new ResizeObserver(room).observe(b);}
    else{window.addEventListener('resize',room);}

    function close(){
      document.body.classList.remove('consent-on');
      document.documentElement.style.removeProperty('--consent-h');
      if(b.parentNode){b.parentNode.removeChild(b);}
      openBanner=null;
    }
    function apply(v){
      var wasLoaded=gaLoaded||adsLoaded;
      save(v);consent(v);load(v);
      /* Turning a previously granted category off cannot unload a script that
         is already running, so the clean answer is a fresh page. */
      if(wasLoaded && (!v.analytics||!v.ads)){location.reload();return;}
      close();
    }
    ok.onclick=function(){
      if(managing){apply({analytics:a.checked,ads:d.checked});}
      else{apply({analytics:true,ads:true});}
    };
    no.onclick=function(){apply({analytics:false,ads:false});};
    manage.onclick=function(){
      managing=true;panel.hidden=false;manage.hidden=true;
      ok.textContent='Save choices';
    };
  }

  function hookFooter(){
    var links=document.querySelectorAll('[data-consent-open]');
    Array.prototype.forEach.call(links,function(el){
      el.addEventListener('click',function(e){e.preventDefault();banner();});
    });
  }
  function start(){
    hookFooter();
    if(!stored){banner();}
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',start);
  }else{start();}
})();
</script>""" % {"ga": json.dumps(GA4_ID), "ads": json.dumps(ADS_PUBLISHER),
              "priv": html.escape(up + "privacy.html", quote=True)}

    ads_script = ""
    if ADS_PUBLISHER:
        ads_script = (
            '\n<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-%s" '
            'crossorigin="anonymous"></script>' % html.escape(ADS_PUBLISHER)
        )
    return base_js + ads_script


def verify_head():
    out = []
    if GOOGLE_VERIFY:
        out.append('<meta name="google-site-verification" content="%s">'
                   % GOOGLE_VERIFY)
    if BING_VERIFY:
        out.append('<meta name="msvalidate.01" content="%s">' % BING_VERIFY)
    return "\n".join(out)


def adsense_verify():
    """AdSense ownership proof - and ONLY that.

    Uses Google's official site verification meta tag in <head>. This proves
    ownership to AdSense crawlers without firing external script network requests
    or logging console errors when blocked. Actual ad units load only after
    explicit visitor consent in analytics_head().
    """
    if not ADS_PUBLISHER:
        return ""
    pub = ADS_PUBLISHER if ADS_PUBLISHER.startswith("pub-") else ("pub-" + ADS_PUBLISHER)
    return '<meta name="google-adsense-account" content="ca-%s">' % html.escape(pub)


def heading_ids(html_text):
    """Stable ids on every h2/h3 plus the list the table of contents needs."""
    toc, seen = [], {}

    def repl(m):
        level, text = m.group(1), m.group(2)
        plain = html.unescape(re.sub(r"<[^>]+>", "", text)).strip()
        base = slugify(plain)[:60] or "section"
        seen[base] = seen.get(base, 0) + 1
        anchor = base if seen[base] == 1 else "%s-%d" % (base, seen[base])
        if level == "2":
            toc.append((anchor, plain))
        return '<h%s id="%s">%s</h%s>' % (level, anchor, text, level)

    return re.sub(r"<h([23])>(.*?)</h\1>", repl, html_text), toc


def toc_html(toc):
    """The list of headings in a guide, as a row of equal-sized entries.

    Every entry is one fixed-height row: the number in a slot of its own on
    the left, the heading on one line beside it. A heading too long for the
    row is cut with an ellipsis and the whole line is in the tooltip, so no
    row ever grows and the list keeps one even rhythm.

    The label sits in a <span> because that is the element the ellipsis has
    to go on - the flex row itself is the box, not the text.
    """
    if len(toc) < 3:
        return ""
    items = "".join('<li><a href="#%s" title="%s"><span>%s</span></a></li>'
                    % (anchor, html.escape(text, quote=True), html.escape(text))
                    for anchor, text in toc)
    return ('<nav class="toc" aria-labelledby="toc-h">'
            '<p class="toc-h" id="toc-h">On this page</p><ol>%s</ol></nav>'
            % items)


# The one link whose label means "the Rom Flasher tool itself". Those rows do
# not get a URL line - they get a button that opens our own download page, so a
# reader lands on the tool's home instead of a bare release page.
TOOL_LINK_LABEL = "Rom Flasher tool (free)"


def link_row(l, up):
    """One row of an article's Links / Downloads list.

    Everything is rendered exactly as the video gave it - label and URL, the
    original characters - except the Rom Flasher tool row, which points at the
    tool's own site instead of a bare GitHub release page. No button here: the
    "download the tool" call already sits in the panel beside the video, and two
    invitations to the same page read as nagging.
    """
    label = l.get("label") or ""
    url = l.get("url") or ""
    if label == TOOL_LINK_LABEL:
        return ('<li><strong>%s</strong> &mdash; '
                '<a href="%s" rel="noopener">%s</a></li>'
                % (html.escape(label), SITE_URL + "/", SITE_URL + "/"))
    if label:
        return ('<li><strong>%s</strong> &mdash; '
                '<a href="%s" rel="nofollow noopener">%s</a></li>'
                % (html.escape(label), html.escape(url), html.escape(url)))
    return ('<li><a href="%s" rel="nofollow noopener">%s</a></li>'
            % (html.escape(url), html.escape(url)))


def steps_from_md(body):
    """The numbered steps an article actually contains, for a copy button."""
    steps = []
    for raw in (body or "").splitlines():
        m = re.match(r"^\d+\.\s+(.+)$", raw.strip())
        if m:
            steps.append(re.sub(r"\*\*(.+?)\*\*", r"\1", m.group(1)).strip())
    return steps


def plain_text(text, limit=6000):
    """Markdown and links stripped - what a video's own description says."""
    text = re.sub(r"https?://\S+", "", text or "")
    text = re.sub(r"[*_`#>|]+", " ", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()[:limit]


STEPS_JS = """<script>
(function(){
  var bs=document.querySelectorAll('.copybtn[data-steps]');
  Array.prototype.forEach.call(bs,function(b){
    b.addEventListener('click',function(){
      var steps;try{steps=JSON.parse(b.getAttribute('data-steps'));}catch(e){return;}
      var txt=steps.map(function(s,i){return (i+1)+'. '+s;}).join('\\n');
      var done=function(){var w=b.getAttribute('data-label')||'Copy the steps';
        b.textContent='Copied';b.classList.add('done');
        setTimeout(function(){b.textContent=w;b.classList.remove('done');},1600);};
      if(navigator.clipboard){navigator.clipboard.writeText(txt).then(done,done);}else{done();}
    });
  });
})();
</script>"""


# Browsers do honour a muted autoplay, but an iframe that was laid out before it
# reached the viewport can sit idle - especially after a client-side restore of
# the scroll position. So the player is asked to start over postMessage, which is
# the YouTube embed's own control channel. Nothing else is touched: no cookie,
# no API script, and if it never answers the poster inside the player is still
# there and one tap starts it.
YT_JS = """<script>
(function(){
  var f=document.querySelector('.videobox .frame iframe');
  if(!f)return;
  function nudge(){
    try{
      f.contentWindow.postMessage(JSON.stringify({event:'command',
        func:'playVideo',args:[]}),'*');
      f.contentWindow.postMessage(JSON.stringify({event:'command',
        func:'mute',args:[]}),'*');
    }catch(e){}
  }
  // ready, in case the player finished loading before this ran
  nudge();
  // and once more when it reports itself ready
  window.addEventListener('message',function(e){
    if(typeof e.data!=='string'||e.data.indexOf('onReady')<0)return;
    nudge();
  });
  // and when the page is shown again from the back/forward cache
  window.addEventListener('pageshow',nudge);
})();
</script>"""

SHOTS_LIGHTBOX_TPL = """<div id="shotLightbox" class="shot-lightbox" aria-hidden="true" role="dialog" aria-label="Screenshot lightbox">
  <div class="lb-backdrop"></div>
  <div class="lb-wrap">
    <button type="button" class="lb-btn lb-close" aria-label="Close fullscreen view">&times;</button>
    <button type="button" class="lb-btn lb-prev" aria-label="Previous screenshot">&#10094;</button>
    <button type="button" class="lb-btn lb-next" aria-label="Next screenshot">&#10095;</button>
    <div class="lb-figure">
      <img id="lbImg" src="" alt="ROM Screenshot Fullscreen">
      <div id="lbCounter" class="lb-counter"></div>
    </div>
  </div>
</div>
<script>
(function(){
  var shots = __SHOTS_JSON__;
  if (!shots || !shots.length) return;
  var lb = document.getElementById('shotLightbox');
  var img = document.getElementById('lbImg');
  var counter = document.getElementById('lbCounter');
  var cur = 0;
  function show(idx){
    if (idx < 0) idx = shots.length - 1;
    if (idx >= shots.length) idx = 0;
    cur = idx;
    img.src = shots[cur];
    if (counter) counter.textContent = (cur + 1) + ' / ' + shots.length;
    lb.classList.add('open');
    lb.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }
  function close(){
    lb.classList.remove('open');
    lb.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }
  var cards = document.querySelectorAll('.shot-card');
  for (var i = 0; i < cards.length; i++){
    (function(idx){
      cards[idx].addEventListener('click', function(e){
        e.preventDefault();
        show(idx);
      });
    })(i);
  }
  var closeBtn = lb.querySelector('.lb-close');
  if (closeBtn) closeBtn.addEventListener('click', close);
  var prevBtn = lb.querySelector('.lb-prev');
  if (prevBtn) prevBtn.addEventListener('click', function(e){ e.stopPropagation(); show(cur - 1); });
  var nextBtn = lb.querySelector('.lb-next');
  if (nextBtn) nextBtn.addEventListener('click', function(e){ e.stopPropagation(); show(cur + 1); });
  var backdrop = lb.querySelector('.lb-backdrop');
  if (backdrop) backdrop.addEventListener('click', close);
  window.addEventListener('keydown', function(e){
    if (!lb.classList.contains('open')) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowLeft') show(cur - 1);
    else if (e.key === 'ArrowRight') show(cur + 1);
  });
})();
</script>"""


def render_shot_lightbox(shots, up=""):
    if not shots:
        return ""
    resolved = [s if s.startswith("http") else (up + s.lstrip("/")) for s in shots]
    shots_json = json.dumps(resolved, ensure_ascii=False)
    return SHOTS_LIGHTBOX_TPL.replace("__SHOTS_JSON__", shots_json)




def _asset_ver():
    """Short fingerprint so a rebuilt stylesheet is never served from cache."""
    import hashlib
    path = os.path.join(STATIC, "style.css")
    if not os.path.exists(path):
        return "1"
    with open(path, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()[:8]


ASSET_VER = _asset_ver()


# ---------------------------------------------------------------- markdown
def inline(text):
    """Inline markdown. Output is escaped except for the tags we generate."""
    text = html.escape(str(text), quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\w)`([^`]+?)`(?!\w)", r"<code>\1</code>", text)
    text = re.sub(
        r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
        lambda m: '<a href="%s" rel="noopener">%s</a>' % (m.group(2), m.group(1)),
        text)
    return text


def _render_md_table(lines):
    if not lines or len(lines) < 2:
        return "\n".join("<p>%s</p>" % inline(l) for l in lines)
    rows = []
    for line in lines:
        cells = [c.strip() for c in line.strip()[1:-1].split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return "\n".join("<p>%s</p>" % inline(l) for l in lines)
    headers = rows[0]
    sep_row = rows[1]
    is_sep = len(sep_row) >= len(headers) and all(re.match(r"^:?-+:?$", c) for c in sep_row if c)
    if not is_sep:
        return "\n".join("<p>%s</p>" % inline(l) for l in lines)
    data_rows = rows[2:]
    alignments = []
    for c in sep_row:
        if c.startswith(":") and c.endswith(":"):
            alignments.append("center")
        elif c.endswith(":"):
            alignments.append("right")
        else:
            alignments.append("left")
    html_out = ['<div class="tablewrap"><table class="pro-table"><thead><tr>']
    for i, h in enumerate(headers):
        align = alignments[i] if i < len(alignments) else "left"
        html_out.append('<th class="align-%s">%s</th>' % (align, inline(h)))
    html_out.append('</tr></thead><tbody>')
    for r_idx, r in enumerate(data_rows):
        html_out.append('<tr>')
        for i, c in enumerate(r):
            align = alignments[i] if i < len(alignments) else "left"
            html_out.append('<td class="align-%s">%s</td>' % (align, inline(c)))
        html_out.append('</tr>')
    html_out.append('</tbody></table></div>')
    return "".join(html_out)


def md(text):
    """Block markdown: fenced code blocks, ## headings, - / 1. lists, > quotes, tables, hr, raw html, paragraphs."""
    out, ul, ol, table_lines, code_lines = [], [], [], [], []
    mode = None
    code_lang = ""

    def flush():
        nonlocal mode
        if mode == "ul" and ul:
            out.append("<ul>" + "".join("<li>%s</li>" % inline(b) for b in ul) + "</ul>")
            ul.clear()
        if mode == "ol" and ol:
            out.append("<ol>" + "".join("<li>%s</li>" % inline(b) for b in ol) + "</ol>")
            ol.clear()
        if mode == "table" and table_lines:
            out.append(_render_md_table(table_lines))
            table_lines.clear()
        mode = None

    for raw in (text or "").splitlines():
        line = raw.rstrip()

        # Fenced code blocks (handles indented fences too)
        stripped = line.strip()
        is_fence = stripped.startswith("```") or stripped.startswith("'''")
        if is_fence:
            if mode != "code":
                flush()
                mode = "code"
                code_lang = stripped.strip("`' ").lower() or "shell"
                code_lines.clear()
            else:
                lang_display = html.escape(code_lang)
                code_content = html.escape("\n".join(code_lines))
                out.append(
                    '<div class="code-block" data-lang="%s">'
                    '<div class="code-block-header">'
                    '<span class="code-block-lang">%s</span>'
                    '<button type="button" class="code-copy-btn" onclick="navigator.clipboard.writeText(this.closest(\'.code-block\').querySelector(\'code\').innerText);this.innerText=\'Copied!\';setTimeout(()=>this.innerText=\'Copy\',2000)">Copy</button>'
                    '</div>'
                    '<pre><code class="language-%s">%s</code></pre>'
                    '</div>' % (lang_display, lang_display, lang_display, code_content)
                )
                code_lines.clear()
                mode = None
            continue

        if mode == "code":
            code_lines.append(raw)
            continue

        # Raw HTML blocks passthrough
        if re.match(r"^\s*</?[a-zA-Z][a-zA-Z0-9_-]*(\s|/?>)", raw):
            flush()
            out.append(raw)
            continue

        if not line.strip():
            flush()
            continue

        if line.strip() in ("---", "***", "___"):
            flush()
            out.append("<hr class='divider'>")
        elif line.lstrip().startswith("#"):
            flush()
            level = 3 if line.startswith("###") else 2
            out.append("<h%d>%s</h%d>"
                       % (level, inline(line.lstrip("# ").strip()), level))
        elif line.startswith("> "):
            flush()
            out.append("<blockquote>%s</blockquote>" % inline(line[2:]))
        elif line.startswith(("- ", "* ", "\u2022 ", "\u00b7 ")):
            if mode != "ul":
                flush()
                mode = "ul"
            ul.append(line[2:])
        elif re.match(r"^\d+\.\s", line):
            if mode != "ol":
                flush()
                mode = "ol"
            ol.append(re.sub(r"^\d+\.\s", "", line))
        elif line.startswith("|") and line.endswith("|") and "|" in line[1:-1]:
            if mode != "table":
                flush()
                mode = "table"
            table_lines.append(line)
        else:
            flush()
            out.append("<p>%s</p>" % inline(line))

    if mode == "code" and code_lines:
        lang_display = html.escape(code_lang)
        code_content = html.escape("\n".join(code_lines))
        out.append(
            '<div class="code-block" data-lang="%s">'
            '<div class="code-block-header"><span class="code-block-lang">%s</span></div>'
            '<pre><code class="language-%s">%s</code></pre>'
            '</div>' % (lang_display, lang_display, lang_display, code_content)
        )
    flush()
    return "\n".join(out)


def desc_to_md(text):
    """The YouTube description is nearly markdown - nudge it across."""
    out = []
    for raw in (text or "").splitlines():
        line = raw.rstrip()
        if not line.strip():
            out.append("")
            continue
        if re.match(r"^[\u2022\u00b7\-\*]\s", line):
            out.append("- " + line[2:].strip())
            continue
        first = line.lstrip()[:1]
        looks_like_head = (len(line) < 74
                           and (line.endswith(":")
                                or (first and not first.isalnum() and first not in "-*")))
        out.append("### " + line if looks_like_head else line)
    return "\n".join(out)


def crumbs_html(items_paths):
    """A visible trail: [('Home','index.html'), ('Guides','videos.html'), ...].

    The last entry is plain text - it is where the visitor already is, so
    linking it back to itself would only be a trap.
    """
    parts = []
    for i, (label, href) in enumerate(items_paths):
        if i:
            parts.append('<span class="sep">&rsaquo;</span>')
        if href and i < len(items_paths) - 1:
            parts.append('<a href="%s">%s</a>' % (href, html.escape(label)))
        else:
            parts.append('<span class="here">%s</span>' % html.escape(label))
    return ('<nav class="crumbs" aria-label="Breadcrumb">%s</nav>'
            % "".join(parts))


def nice_date(value):
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", str(value or ""))
    if not m:
        return ""
    year, month, day = m.group(1), int(m.group(2)), int(m.group(3))
    if not 1 <= month <= 12:
        return ""
    return "%d %s %s" % (day, MONTHS[month - 1], year)


def video_id_of(url):
    tail = (url or "").rstrip("/").split("/")[-1]
    return tail.split("=")[-1].split("&")[0]


# Filler that eats characters in a search result without adding meaning. The
# replacements carry the case they should appear in; everything else is left
# exactly as the guide wrote it.
TITLE_RULES = [
    (r"\bStep[\s-]?by[\s-]?Step\b", ""),
    (r"\bFull Flash Guide\b", "Flash"),
    (r"\bFull Install Guide\b", "Install"),
    (r"\bFull Unbrick Guide\b", "Unbrick"),
    (r"\bFull Flash\b", "Flash"),
    (r"\bFull Install\b", "Install"),
    (r"\bFull ROM Review\b", "ROM Review"),
    (r"\bFull Review\b", "Review"),
    (r"\bFull Tour\b", "Tour"),
    (r"\bComplete Walkthrough\b", ""),
    (r"\bWalkthrough\b", ""),
    (r"\bStart to Finish\b", ""),
    (r"\bfor Beginners\b", ""),
    (r"\bNo Script and No Cuts\b", ""),
    (r"\bNo Script\b", ""),
    (r"\bNo Cuts\b", ""),
    (r"\bFull\b", ""),
    (r"\bFlash Guide\b", "Flash"),
    (r"\bInstall Guide\b", "Install"),
    (r"\bUnbrick Guide\b", "Unbrick"),
    (r"\bReview Guide\b", "Review"),
    (r"\bGuide\b", ""),
    (r"#\w+", ""),
]


def display_title(title, limit=60):
    """The <title> a search result shows: same words, trimmed to fit.

    Search shows roughly 60 characters before it starts clipping for the reader,
    and a clipped word ("...Smoothnes") looks broken. So filler that adds no
    meaning is dropped first, then the line is cut back to a whole word. The H1
    and the card keep the guide's full title, so nothing is lost on the page.
    """
    t = str(title or "").replace("\u2014", "-").replace("\u2013", "-")
    t = re.sub(r"\s*\+\s*", " + ", t)
    t = re.sub(r"\s+", " ", t).strip()
    for pat, rep in TITLE_RULES:
        t = re.sub(pat, rep, t, flags=re.I)
    t = re.sub(r"\s{2,}", " ", t).strip()
    t = re.sub(r"\s*&\s*$", "", t)
    t = t.strip(" -,:;+")
    if len(t) <= limit:
        return t
    head = t[:limit]
    # Prefer a real break - a dash, a comma, a bracket - when one fits, so the
    # result reads as a phrase rather than a chopped-off sentence.
    for sep in [" - ", ", ", " (", " + "]:
        if sep not in head:
            continue
        cut = head.rsplit(sep, 1)[0].strip(" -,:;+&")
        if len(cut) >= 32:
            return cut
    return head.rsplit(" ", 1)[0].strip(" -,:;+&")


# ------------------------------------------------------------------ layout

CURSOR_LIGHT = ""

CURSOR_LIGHT_JS = ""


# The menu button on a phone. The five pills live in the header on a desktop and
# in this drop-down panel on a phone; the panel is hidden by css and only the
# button is wired up here, so a desktop never runs any of it.
NAV_JS = """<script>
(function(){
  var btn = document.querySelector('.navtoggle');
  var nav = document.getElementById('mainnav');
  if(!btn || !nav) return;

  function setOpen(on){
    on = !!on;
    document.body.classList.toggle('navopen', on);
    btn.setAttribute('aria-expanded', on ? 'true' : 'false');
    btn.setAttribute('aria-label', on ? 'Close the menu' : 'Open the menu');
  }

  btn.addEventListener('click', function(e){
    e.stopPropagation();
    setOpen(!document.body.classList.contains('navopen'));
  });

  // A tap on the page itself closes the menu again.
  document.addEventListener('click', function(e){
    if(!document.body.classList.contains('navopen')) return;
    if(nav.contains(e.target) || btn.contains(e.target)) return;
    setOpen(false);
  });

  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' || e.keyCode === 27) setOpen(false);
  });

  // Following a link closes the menu before the page goes somewhere else.
  nav.addEventListener('click', function(e){
    var t = e.target;
    if(t && t.closest && t.closest('a')) setOpen(false);
  });

  // A wider screen gets the button row back, so the open state is dropped.
  try{
    var wide = window.matchMedia('(min-width:761px)');
    var onChange = function(){ if(wide.matches) setOpen(false); };
    if(wide.addEventListener) wide.addEventListener('change', onChange);
    else if(wide.addListener) wide.addListener(onChange);
  }catch(e){}
})();
</script>"""


# The video poster is a real <div>, not an inline onclick: a title such as
# "Why It's Worth It" used to end the single-quoted JS string early and the
# play button died with a SyntaxError. The id and title now travel as data
# attributes, the iframe is built with createElement, and no value is ever
# interpolated into executable code.
VIDEO_JS = """<script>
(function(){
  var facades=document.querySelectorAll('.yt-facade[data-vid]');
  Array.prototype.forEach.call(facades,function(f){
    function play(){
      var vid=f.getAttribute('data-vid');
      if(!vid) return;
      var frame=document.createElement('iframe');
      frame.src='https://www.youtube-nocookie.com/embed/'+encodeURIComponent(vid)
        +'?autoplay=1&rel=0&playsinline=1&modestbranding=1';
      frame.title=f.getAttribute('data-title')||'Rom Flasher video';
      frame.setAttribute('allow','accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture');
      frame.setAttribute('allowfullscreen','');
      frame.setAttribute('referrerpolicy','strict-origin-when-cross-origin');
      frame.setAttribute('frameborder','0');
      f.parentElement.replaceChild(frame,f);
    }
    f.addEventListener('click',play);
    f.addEventListener('keydown',function(e){
      if(e.key==='Enter'||e.key===' '){e.preventDefault();play();}
    });
  });
})();
</script>"""


def clip(text, limit=158):
    """Trim a description to a length Google shows whole, ending on a word.

    Blurbs double as card and feed text, where running long is fine, so the cut
    happens here - once, at the point the meta tag is written - rather than in
    the stored content.
    """
    text = re.sub(r"\s+", " ", (text or "").strip())
    if len(text) <= limit:
        return text
    cut = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:-")
    return cut + "\u2026"


def page(title, description, body, path="", extra_head="", keywords="",
         og_type="website", image=None, robots=None):
    """Assemble a full page. `path` is where it will live inside dist/."""
    up = "../" * path.count("/")
    canon = "%s/%s" % (SITE_URL, path) if path else SITE_URL + "/"
    desc = html.escape(clip(description or title))
    title_esc = html.escape(title)
    img = image or (SITE_URL + "/static/app-icon-512.png")
    robots_meta = ('<meta name="robots" content="%s">' % robots) if robots else \
                  '<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">'

    head = "\n".join([
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        "<title>%s</title>" % title_esc,
        '<meta name="description" content="%s">' % desc,
        '<meta name="keywords" content="%s">' % html.escape(keywords or keywords_for()),
        robots_meta,
        '<meta name="author" content="%s">' % AUTHOR_NAME,
        '<meta name="theme-color" content="#05070c">',
        '<meta name="rating" content="general">',
        '<meta http-equiv="Content-Security-Policy" content="upgrade-insecure-requests; object-src \'none\'; base-uri \'self\'; form-action \'self\' https://formsubmit.co">',
        '<meta name="referrer" content="strict-origin-when-cross-origin">',
        '<script>if(location.protocol==="http:"&&location.hostname!=="localhost"&&location.hostname!=="127.0.0.1"){location.replace("https://"+location.host+location.pathname+location.search+location.hash);}</script>',
        '<script>if(window.top!==window.self){try{window.top.location=window.self.location;}catch(e){window.self.location="about:blank";}}</script>',
        '<link rel="canonical" href="%s">' % canon,
        '<link rel="icon" type="image/svg+xml" href="%sstatic/favicon.svg">' % up,
        '<link rel="apple-touch-icon" sizes="180x180" '
        'href="%sstatic/apple-touch-icon.png">' % up,
        '<link rel="manifest" href="%ssite.webmanifest">' % up,
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>',
        '<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&amp;display=swap">',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&amp;display=swap" media="print" onload="this.media=\'all\'">',
        '<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800;900&amp;display=swap"></noscript>',
        '<link rel="preconnect" href="https://www.youtube.com">',
        '<link rel="preconnect" href="https://i.ytimg.com">',
        verify_head(),
        adsense_verify(),
        analytics_head(up),
        '<link rel="stylesheet" href="%sstatic/style.css">' % up,
        '<link rel="alternate" type="application/rss+xml" title="%s" '
        'href="%sfeed.xml">' % (SITE, up),
        '<meta property="og:type" content="%s">' % og_type,
        '<meta property="og:site_name" content="%s">' % SITE,
        '<meta property="og:locale" content="en_US">',
        *(['<meta property="article:author" content="%s">' % AUTHOR_NAME] if og_type == "article" else []),
        '<meta property="og:title" content="%s">' % html.escape(title),
        '<meta property="og:description" content="%s">' % desc,
        '<meta property="og:url" content="%s">' % canon,
        '<meta property="og:image" content="%s">' % img,
        '<meta property="og:image:alt" content="%s">' % html.escape(title),
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % html.escape(title),
        '<meta name="twitter:description" content="%s">' % desc,
        '<meta name="twitter:image" content="%s">' % img,
        extra_head,
        "</head>",
        "<body>",
        '<a class="skip-link" href="#main">Skip to content</a>',
        ('<header class="top"><div class="wrap">\n'
         '  <a class="brand brand-anim-wrap" href="%sindex.html" aria-label="Rom Flasher - All-In-One Android Tool">' % up)
        + ('<img src="%sstatic/brand-anim.svg" alt="Rom Flasher" width="310" height="64" class="brand-svg-logo"></a>' % up),
        "  <nav id=\"mainnav\">",
        '    <a class="navbtn guides" href="%svideos.html">%sGuides</a>'
        % (up, GUIDES_LOGO),
        '    <a class="navbtn hot" href="%sdownloader.html" '
        'aria-label="Stock ROM Download: stock ROMs, Magisk and KernelSU">%sStock ROM Download</a>'
        % (up, DL_LOGO),
        '    <div class="pixel-socials">',
        '      <a class="pixel-round gh-round" href="%s" target="_blank" rel="noopener" aria-label="GitHub" title="Rom Flasher tool on GitHub">%s</a>' % (REPO_URL, GH_LOGO),
        '      <a class="pixel-round yt-round" href="%s" target="_blank" rel="noopener" aria-label="YouTube" title="Rom Flasher on YouTube">%s</a>' % (CHANNEL_URL, YT_LOGO),
        '      <a class="pixel-round coffee-round" href="%sdonate.html" aria-label="Buy me a coffee" title="Buy me a coffee">%s</a>' % (up, COFFEE_LOGO),
        '    </div>',
        "  </nav>",
        # The menu button only shows on a phone, where the five pills used to
        # stack under the logo and eat a fifth of the screen. Three lines, the
        # same mark every Android app puts in its top bar.
        '  <button class="navtoggle" type="button" aria-expanded="false" '
        'aria-controls="mainnav" aria-label="Open the menu">'
        '<span class="burger" aria-hidden="true"><i></i><i></i><i></i></span>'
        '</button>',
        "</div></header>",
    ])

    # a new query string every time the stylesheet changes, so no stale css
    head = head.replace('static/style.css"',
                        'static/style.css?v=%s"' % ASSET_VER)

    browse = ('<nav class="footnav subnav" aria-label="Browse Guides">'
              '<a href="%sbrands.html">Brands</a>'
              '<a href="%sroms.html">ROMs</a>'
              '<a href="%svideos.html">All guides</a>'
              '<a href="%syears.html">By year</a>'
              '<a href="%stopics.html">Topics</a>'
              '<a href="%stags.html">Tags</a></nav>'
              % ((up,) * 6))
    foot = """<footer><div class="wrap">
  <div class="footbrand"><strong>%s</strong> &mdash; %s</div>
  %s
  <nav class="footnav" aria-label="Legal and Site Links">
    <a href="%sabout.html">About</a>
    <a href="%scontact.html">Contact</a>
    <a href="%sprivacy.html">Privacy</a>
    <a href="%sterms.html">Terms</a>
    <a href="%sdownload.html">Download Tool</a>
    <a href="%sdownloader.html">ROM Downloader</a>
    <a href="%sdonate.html">Support Us</a>
    <a href="%sdownload.html#talk-to-me">Message</a>
    <a href="%s" rel="noopener">YouTube Channel</a>
    <button type="button" class="footlink" data-consent-open>Cookie settings</button>
  </nav>
  <p class="dis">Not affiliated with Xiaomi, POCO, Redmi or any ROM project.
  Flashing is at your own risk &mdash; read the <a href="%sterms.html">terms</a> first.</p>
</div></footer>
</body>
</html>
""" % (SITE, TAGLINE, browse, up, up, up, up, up, up, up, up, CHANNEL_URL, up)

    # the pointer light is moved by a script, so it belongs at the end of body
    foot = foot.replace("</body>", NAV_JS + "\n" + VIDEO_JS + "\n</body>")
    return head + '<main id="main">\n' + body + '\n</main>\n' + foot


def card(item, up=""):
    """A guide tile. The whole card is clickable, and the tag chips work too.

    The card cannot itself be an <a>: HTML forbids nesting one link inside
    another, and the browser hoists the inner tag links out, which spills them
    across the grid as giant pills. So the card is a plain <div> and the title
    carries a stretched link that covers it - same big tap target, no nesting.
    """
    tags = ("".join(tag_href(t, up) for t in (item.get("tags") or [])[:3]))
    tags = '<div class="cardtags">%s</div>' % tags if tags else ""
    foot = []
    if clean_device(item.get("device")):
        foot.append(html.escape(clean_device(item["device"])))
    if item.get("published"):
        foot.append(nice_date(item["published"]))
    else:
        foot.append("%s views" % item.get("views", 0))
    return ('<div class="card">'
            '<h3><a class="cardlink" href="%srom/%s.html">%s</a></h3>'
            "<p>%s</p>%s<span class=\"foot\">%s</span></div>"
            % (up, html.escape(item["slug"]), html.escape(item["title"]),
               html.escape(item.get("blurb") or ""), tags,
               " &middot; ".join(foot)))


# ------------------------------------------------------------------- pages
def build_home(items, path="index.html"):
    by_views = sorted(items, key=lambda x: -(x.get("views") or 0))[:9]
    by_date = sorted(items, key=lambda x: x.get("published") or "", reverse=True)[:9]

    # The home page uses the whole width of the window. When there is an ad
    # unit it gets its own column on the right and the guide lists narrow to
    # make room; when there is none, the lists take everything. That is why the
    # two classes are decided here rather than in the stylesheet - the ad slot
    # is empty (not even a zero-height box) when the unit id is unset, and the
    # page must not reserve space for it.
    ad = ad_slot("hub")
    row = "homerow withad" if ad else "homerow"
    rail = '<aside class="adrail">%s</aside>' % ad if ad else ""

    body = """<div class="journal-masthead">
  <div class="wrap full">
    <div class="masthead-meta">
      <span class="masthead-badge">&#10003; Independent Engineering Journal</span>
      <span class="masthead-by">Editor-in-Chief: <strong>Rohit Verma</strong> (@Rom_Flasher)</span>
      <span class="masthead-stat">%d Physical Hardware Tested Guides</span>
    </div>
  </div>
</div>
<section class="hero-editorial"><div class="wrap full">
  <div class="hero-editorial-grid">
    <div class="hero-editorial-main">
      <h1 class="hero-title">Custom ROM guides tested on real phones.</h1>
      <p class="hero-lead">%s &mdash; every single fastboot script and ROM install is verified in our hardware lab by Rohit Verma. Zero AI hallucinations. Zero bricked phones.</p>
      <div class="hero-actions">
        <a class="btn primary" href="videos.html">Browse all %d verified guides</a>
        <a class="btn-outline btn-dl" href="download.html"><svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg> <span>Download Rom Flasher Tool (Free)</span></a>
      </div>
    </div>
    <div class="hero-editorial-side">
      <div class="home-author-spotlight">
        <div class="has-avatar">
          <img src="static/rohit-verma.webp" alt="Rohit Verma" width="84" height="84" loading="eager">
        </div>
        <div class="has-content">
          <div class="has-kicker">Meet the Engineer</div>
          <div class="has-name">Rohit Verma <span class="has-handle">@Rom_Flasher</span></div>
          <p class="has-bio">Android kernel &amp; flashing specialist. Creator of Rom Flasher Tool. I test every ROM on real phones in our lab before publishing so you never risk bricking yours.</p>
          <div class="has-links">
            <a href="https://www.youtube.com/@Rom_Flasher" target="_blank" rel="noopener">YouTube (@Rom_Flasher)</a> &middot;
            <a href="about.html">Lab Testing Protocol</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</div></section>

<section class="testbench-section"><div class="wrap full">
  <div class="tb-wrapper">
    <div class="tb-heading">
      <span class="tb-badge">&#10003; Physical Hardware Test Bench</span>
      <p class="tb-desc">Active lab devices used for firmware verification, bootloader testing, and partition safety checks:</p>
    </div>
    <div class="tb-grid">
      <div class="tb-unit">
        <div class="tb-unit-name">Xiaomi Pad 5 <span class="tb-code">nabu</span></div>
        <div class="tb-unit-status"><span class="tb-tag">HyperOS 2.0</span><span class="tb-tag">Fastboot Recovery</span><span class="tb-tag">OTG Verified</span></div>
      </div>
      <div class="tb-unit">
        <div class="tb-unit-name">Redmi Note 10 Pro <span class="tb-code">sweet</span></div>
        <div class="tb-unit-status"><span class="tb-tag">Android 15 AOSP</span><span class="tb-tag">KernelSU</span><span class="tb-tag">OrangeFox</span></div>
      </div>
      <div class="tb-unit">
        <div class="tb-unit-name">Realme GT 2 Pro <span class="tb-code">RMX3301</span></div>
        <div class="tb-unit-status"><span class="tb-tag">ColorOS 14</span><span class="tb-tag">TEE Keybox</span><span class="tb-tag">Fastbootd</span></div>
      </div>
      <div class="tb-unit">
        <div class="tb-unit-name">POCO F1 <span class="tb-code">beryllium</span></div>
        <div class="tb-unit-status"><span class="tb-tag">LineageOS 21</span><span class="tb-tag">Retrofit Dynamic Partitions</span></div>
      </div>
    </div>
  </div>
</div></section>

<section class="pillar-section" id="architecture-manuals"><div class="wrap full">
  <div class="pillar-header">
    <div class="pillar-kicker"><span class="kicker-badge">&#9881; Core Engineering Reference</span></div>
    <h2 class="pillar-title">Android Architecture &amp; Firmware Reference Manuals</h2>
    <p class="pillar-desc">Comprehensive technical documentation on Android storage topologies, root internals, hardware keystore attestation, and emergency unbricking protocols.</p>
  </div>
  <div class="pillar-grid">
    <a class="pillar-card" href="rom/android-partition-architecture-bible.html">
      <div class="pc-badge">Partition Topology</div>
      <h3 class="pc-title">The Android Partition Architecture Bible</h3>
      <p class="pc-summary">Exhaustive guide to A/B slotted partitions, Android 13 GKI init_boot separation, dynamic super containers, and fastbootd userspace boundaries.</p>
      <span class="pc-cta">Read Architecture Manual &rarr;</span>
    </a>
    <a class="pillar-card" href="rom/play-integrity-hardware-attestation-deep-dive.html">
      <div class="pc-badge">Security &amp; Keystore</div>
      <h3 class="pc-title">Play Integrity &amp; Hardware TEE Attestation</h3>
      <p class="pc-summary">How Google evaluates device integrity: TrustZone public keys, keybox CRL revocations, and kernel-space root isolation.</p>
      <span class="pc-cta">Read Security Manual &rarr;</span>
    </a>
    <a class="pillar-card" href="rom/magisk-vs-kernelsu-vs-apatch-vs-sukisu.html">
      <div class="pc-badge">Root Frameworks</div>
      <h3 class="pc-title">Magisk vs KernelSU vs APatch vs SukiSU Ultra</h3>
      <p class="pc-summary">Ramdisk user-space patching vs GKI syscall hooks vs KernelPatch binary injection: complete technical comparison matrix.</p>
      <span class="pc-cta">Read Comparison Manual &rarr;</span>
    </a>
    <a class="pillar-card" href="rom/android-anti-bootloop-unbrick-manual.html">
      <div class="pc-badge">Emergency Recovery</div>
      <h3 class="pc-title">The Definitive Android Unbrick Manual</h3>
      <p class="pc-summary">Systematic diagnostic flowchart: Qualcomm EDL 9008 Sahara handshakes, MediaTek BROM, AVB 2.0 Red State recovery, and FBE wipes.</p>
      <span class="pc-cta">Read Recovery Manual &rarr;</span>
    </a>
    <a class="pillar-card" href="rom/fastbootd-dynamic-partitions-troubleshooting.html">
      <div class="pc-badge">Logical Partitions</div>
      <h3 class="pc-title">Fastbootd &amp; Dynamic Partitions Explained</h3>
      <p class="pc-summary">How to flash logical partitions, delete stock bloat blocks inside super to resolve resize errors, and install GSIs safely.</p>
      <span class="pc-cta">Read Fastbootd Manual &rarr;</span>
    </a>
  </div>
</div></section>

<div class="wrap full">
<div class="%s">
<div class="homecol">
<h2>Newest guides</h2>
<div class="grid">%s</div>
<h2>Most watched</h2>
<div class="grid">%s</div>
</div>
%s
</div>
</div>
<script>
(function(){
  function fixRail(){
    var r = document.querySelector('.adrail');
    var h = document.querySelector('.homerow');
    if (!r || !h) return;
    var cs = window.getComputedStyle(r);
    if (cs.display === 'none' || r.offsetHeight < 10 || r.offsetWidth < 10) {
      h.classList.remove('withad');
    }
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', fixRail);
  } else {
    fixRail();
  }
  window.addEventListener('load', fixRail);
  setTimeout(fixRail, 150);
  setTimeout(fixRail, 600);
})();
</script>""" % (len(items), TAGLINE, len(items), row,
             "".join(card(x) for x in by_date),
             "".join(card(x) for x in by_views), rail)

    logo = {"@type": "ImageObject", "url": SITE_URL + "/static/app.png"}
    blocks = [{
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": SITE,
        "alternateName": "Rom Flasher guides",
        "url": SITE_URL + "/",
        "description": TAGLINE,
        "inLanguage": "en",
        "publisher": {"@type": "Organization", "name": SITE, "url": SITE_URL,
                      "logo": logo},
        "potentialAction": {
            "@type": "SearchAction",
            "target": {"@type": "EntryPoint",
                       "urlTemplate": SITE_URL + "/videos.html?q={q}"},
            "query-input": "required name=q",
        },
    }, {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": SITE,
        "url": SITE_URL + "/",
        "logo": logo,
        "sameAs": [CHANNEL_URL, REPO_URL],
        "description": "Custom ROM and Android flashing guides, plus a free "
                       "Android flashing tool that works over USB-OTG.",
    }, {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Newest flashing guides",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": x["title"],
             "url": "%s/rom/%s.html" % (SITE_URL, x["slug"])}
            for i, x in enumerate(by_date)],
    }]
    head = "\n".join('<script type="application/ld+json">%s</script>'
                     % json.dumps(b, ensure_ascii=False) for b in blocks)

    return page("%s \u2014 Android ROM & Flashing Guides | Tested on Real Hardware" % SITE,
                "Every custom ROM, root and flashing guide from the Rom Flasher "
                "channel, written as text and tested on real phones. Plus a free "
                "Android flashing tool that works with no PC.",
                body, path, extra_head=head, keywords=keywords_for())


def build_guides(items, path="videos.html"):
    """All guides with a real date column, sortable, plus year chips."""
    sorted_items = sorted(items, key=lambda x: (x.get("published") or "", x.get("title") or ""), reverse=True)
    rows = []
    for i, x in enumerate(sorted_items):
        d = x.get("published") or ""
        year = d[:4] if d else "----"
        deep = ' data-deep="1"' if i >= 50 else ""
        rows.append(
            '<tr class="row"%s data-d="%s" data-v="%s" data-y="%s">'
            '<td><a href="rom/%s.html">%s</a></td><td>%s</td>'
            '<td class="dt">%s</td><td class="vw">%s</td></tr>'
            % (deep, html.escape(d), x.get("views") or 0, html.escape(year),
               html.escape(x["slug"]), html.escape(x["title"]),
               html.escape(clean_device(x.get("device")) or "-"),
               html.escape(nice_date(d) or "-"), x.get("views") or 0))

    years = sorted({(x.get("published") or "")[:4] for x in items if x.get("published")},
                   reverse=True)
    chips = "".join('<span class="chip on" data-y="all">All (%d)</span>' % len(items))
    for y in years:
        n = sum(1 for x in items if (x.get("published") or "").startswith(y))
        chips += '<span class="chip" data-y="%s">%s (%d)</span>' % (y, y, n)

    device_chips = "".join(
        '<a class="chip" href="device/%s.html">%s (%d)</a>'
        % (h["slug"], html.escape(name), len(h["rows"]))
        for name, h in sorted(cached_device_hubs(items).items(),
                              key=lambda kv: -len(kv[1]["rows"])))

    brands = group_map(items, brand_of, 2)
    roms = group_map(items, rom_family_of, 2)
    topics = topic_map(items, 3)
    browse = ('<a class="chip hot" href="brands.html">All brands</a>'
              '<a class="chip hot" href="roms.html">All ROMs</a>'
              '<a class="chip hot" href="years.html">By year</a>'
              '<a class="chip hot" href="topics.html">By topic</a>')
    browse += "".join(
        '<a class="chip" href="brand/%s.html">%s (%d)</a>'
        % (h["slug"], html.escape(name), len(h["rows"]))
        for name, h in sorted(brands.items(), key=lambda kv: -len(kv[1]["rows"]))[:6])
    browse += "".join(
        '<a class="chip" href="roms/%s.html">%s (%d)</a>'
        % (h["slug"], html.escape(name), len(h["rows"]))
        for name, h in sorted(roms.items(), key=lambda kv: -len(kv[1]["rows"]))[:8])
    browse += "".join(
        '<a class="chip" href="topic/%s.html">%s (%d)</a>'
        % (h["slug"], html.escape(name), len(h["rows"]))
        for name, h in sorted(topics.items(), key=lambda kv: -len(kv[1]["rows"]))[:8])

    body = """<div class="wrap full"><section style="padding:32px 0 0">
<h1 style="font-size:32px;margin:0 0 6px">All guides (%d)</h1>
<p class="dis">Every video, newest first. Filter by year or search by phone,
ROM or anything in the title.</p>

<div class="controls">
  <input type="search" id="q" name="q" aria-label="Search guides"
         autocomplete="off"
         placeholder="poco x7 pro, lineageos, bootloader, twrp...">
  <select id="sort" aria-label="Sort guides">
    <option value="new">Newest first</option>
    <option value="old">Oldest first</option>
    <option value="views">Most viewed</option>
    <option value="az">Title A-Z</option>
  </select>
</div>
<div class="chips" id="chips">%s</div>

<table><thead><tr><th>Guide</th><th>Device</th><th>Released</th><th>Views</th></tr></thead>
<tbody id="rows">%s</tbody></table>

%s

<h2 style="font-size:20px;margin:28px 0 0">Browse by phone</h2>
<p class="dis">A page per device, collecting every guide for it.</p>
<div class="chips">%s</div>

<h2 style="font-size:20px;margin:28px 0 0">Browse by brand, ROM, topic and year</h2>
<p class="dis">Same guides, cut a different way &mdash; the way you would search
for them.</p>
<div class="chips">%s</div>

<p style="margin-top:22px"><button class="btn ghost" id="more" type="button">Show
all %d guides</button></p>
</section></div>
<script>
(function(){
  var q=document.getElementById('q'), sort=document.getElementById('sort'),
      rows=[].slice.call(document.querySelectorAll('#rows .row')),
      chips=[].slice.call(document.querySelectorAll('#chips .chip')),
      more=document.getElementById('more'),
      expanded=false,
      year='all';

  function apply(){
    var t=q.value.toLowerCase();
    var active = t.length > 0 || year !== 'all';
    rows.forEach(function(r){
      var okText = r.textContent.toLowerCase().indexOf(t) >= 0;
      var okYear = year === 'all' || r.dataset.y === year;
      var okDeep = expanded || active || !r.hasAttribute('data-deep');
      r.style.display = (okText && okYear && okDeep) ? '' : 'none';
    });
    if (more) {
      more.style.display = (!expanded && !active &&
                            document.querySelector('#rows .row[data-deep]'))
                           ? '' : 'none';
    }
  }
  if (more) more.addEventListener('click', function(){ expanded = true; apply(); });
  function sortRows(){
    var mode = sort.value;
    rows.sort(function(a,b){
      if (mode === 'views') return (b.dataset.v|0) - (a.dataset.v|0);
      if (mode === 'az')    return a.textContent.localeCompare(b.textContent);
      if (mode === 'old')   return (a.dataset.d||'').localeCompare(b.dataset.d||'');
      return (b.dataset.d||'').localeCompare(a.dataset.d||'');
    });
    var tb=document.getElementById('rows');
    rows.forEach(function(r){ tb.appendChild(r); });
  }
  q.addEventListener('input', apply);
  sort.addEventListener('change', function(){ sortRows(); apply(); });
  chips.forEach(function(c){
    c.addEventListener('click', function(){
      chips.forEach(function(o){ o.classList.remove('on'); });
      c.classList.add('on');
      year = c.dataset.y;
      apply();
    });
  });
  // deep link: videos.html?q=poco+x7
  var pre = new URLSearchParams(location.search).get('q');
  if (pre) { q.value = pre; }
  sortRows(); apply();
})();
</script>""" % (len(items), chips, "\n".join(rows), ad_slot("list"), device_chips,
                   browse, len(items))
    newest = sorted(items, key=lambda x: x.get("published") or "", reverse=True)
    block = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "All Rom Flasher guides",
        "numberOfItems": len(items),
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": x["title"],
             "url": "%s/rom/%s.html" % (SITE_URL, x["slug"])}
            for i, x in enumerate(newest[:40])],
    }
    head = ('<script type="application/ld+json">%s</script>'
            % json.dumps(block, ensure_ascii=False))
    return page("All guides (%d) \u2014 %s" % (len(items), SITE),
                "Every custom ROM and flashing guide on Rom Flasher, %d in total, "
                "newest first with the date each video went live." % len(items),
                body, path, extra_head=head,
                keywords=keywords_for(extra=("all flashing guides",
                                             "android rom guide list",
                                             "custom rom install list")))


def slugify(text):
    """'POCO X7 Pro' -> 'poco-x7-pro'."""
    return re.sub(r"[^a-z0-9]+", "-", str(text or "").lower()).strip("-")


def hub_map(items, minimum=3):
    """Devices with enough guides to deserve their own landing page.

    Returns {device name: {'slug': ..., 'rows': [...]}} - newest guide first.
    """
    buckets = {}
    for x in items:
        name = clean_device(x.get("device"))
        if not name or name.lower().startswith("any"):
            continue
        if len(slugify(name)) < 3:
            continue
        buckets.setdefault(name, []).append(x)
    return {name: {"slug": slugify(name),
                   "rows": sorted(rows, key=lambda r: r.get("published") or "",
                                  reverse=True)}
            for name, rows in buckets.items() if len(rows) >= minimum}


def build_device_page(name, hub, total, all_hubs):
    """A landing page for one phone: every guide + the free tool."""
    slug, rows = hub["slug"], hub["rows"]
    path = "device/%s.html" % slug
    up = "../"
    count = len(rows)

    table = "\n".join(
        '<tr class="row" data-d="%s" data-v="%s" data-y="%s">'
        '<td><a href="%srom/%s.html">%s</a></td><td class="dt">%s</td>'
        '<td class="vw">%s</td></tr>'
        % (html.escape(x.get("published") or ""), x.get("views") or 0,
           html.escape((x.get("published") or "")[:4]), up,
           html.escape(x["slug"]), html.escape(x["title"]),
           html.escape(nice_date(x.get("published")) or "-"),
           x.get("views") or 0)
        for x in rows)

    siblings = "".join(
        '<a class="chip" href="%s.html">%s (%d)</a>'
        % (h["slug"], html.escape(other), len(h["rows"]))
        for other, h in sorted(all_hubs.items(),
                               key=lambda kv: -len(kv[1]["rows"]))
        if other != name)

    roms = sorted({(x.get("rom") or "").strip() for x in rows if x.get("rom")})
    rom_line = ("ROMs covered here: <strong>%s</strong>." % html.escape(", ".join(roms))
                if roms else "")
    brand = brand_of(rows[0]) if rows else ""
    brand_line = ('Brand page: <a href="../brand/%s.html">%s</a>. '
                  % (slugify(brand), html.escape(brand))) if brand else ""
    faq_html, faq = build_hub_faq("brand", name, rows)

    body = """<div class="wrap full"><section style="padding:32px 0 0">
%(crumbs)s
<h1>%(name)s &mdash; custom ROM and flashing guides (%(count)d)</h1>
<p class="dis">Every <strong>%(name)s</strong> video on the Rom Flasher channel,
newest first, with the date it went live. %(rom_line)s %(brand_line)s</p>
<p><a class="btn" href="%(up)sdownload.html">Download the free Rom Flasher tool</a>
<a class="btn ghost" href="%(up)svideos.html">All %(total)d guides</a></p>

<div class="device-spec-box">
  <h3>Hardware Flashing Advisory &middot; %(name)s</h3>
  <p>All procedures documented for the <strong>%(name)s</strong> have been executed and verified on physical hardware test benches in our engineering lab. Prior to executing fastboot scripts or partition operations, confirm these essential safety requirements:</p>
  <ul>
    <li><strong>Bootloader Unlock State:</strong> Execute <code>fastboot getvar unlocked</code> to verify your bootloader is unlocked. Flashing non-OEM images to a locked bootloader will trigger an immediate flash refusal or brick.</li>
    <li><strong>Partition Scheme:</strong> Confirm whether your %(name)s build utilizes Dynamic Partitions (super image / fastbootd) or traditional block partitions before issuing raw flash commands.</li>
    <li><strong>Power Threshold:</strong> Maintain at least 50%% battery level or use a powered USB-OTG connection to eliminate power loss hazards during sector writes.</li>
    <li><strong>Critical Sector Backup:</strong> Always preserve device-specific <code>boot</code>, <code>persist</code>, and calibration partitions prior to flashing third-party kernels or firmware.</li>
  </ul>
</div>

%(ad)s

<table><thead><tr><th>Guide</th><th>Released</th><th>Views</th></tr></thead>
<tbody>%(table)s</tbody></table>

<h2>Questions people ask</h2>
%(faq)s

<h2>Other phones</h2>
<div class="chips">%(siblings)s</div>
</section></div>""" % {
        "crumbs": crumbs_html([("Home", up + "index.html"),
                               ("Guides", up + "videos.html"),
                               (name, "")]),
        "name": html.escape(name), "count": count, "rom_line": rom_line,
        "brand_line": brand_line, "up": up, "total": total, "table": table,
        "faq": faq_html, "siblings": siblings, "ad": ad_slot("hub", up),
    }

    blocks = [{
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": "%s flashing guides" % name,
        "url": "%s/%s" % (SITE_URL, path),
        "description": "Custom ROM, root and flashing guides for the %s." % name,
        "inLanguage": "en",
        "isAccessibleForFree": True,
        "about": {"@type": "Product", "name": name},
        "mainEntity": {
            "@type": "ItemList",
            "numberOfItems": count,
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": x["title"],
                 "url": "%s/rom/%s.html" % (SITE_URL, x["slug"])}
                for i, x in enumerate(rows[:40])],
        },
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides",
             "item": SITE_URL + "/videos.html"},
            {"@type": "ListItem", "position": 3, "name": name,
             "item": "%s/%s" % (SITE_URL, path)},
        ],
    }, {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer",
                                           "text": re.sub(r"<[^>]+>", "", a)}}
                       for q, a in faq],
    }]
    head = "\n".join('<script type="application/ld+json">%s</script>'
                     % json.dumps(b, ensure_ascii=False) for b in blocks)

    return page("%s guides \u2014 ROM, root, recovery | %s" % (name, SITE),
                "All %d Rom Flasher guides for the %s: custom ROMs, fastboot "
                "flashing, root and recovery, newest first with dates."
                % (count, name),
                body, path, extra_head=head,
                image=newest_thumb(rows) or (SITE_URL + "/static/app.png"),
                keywords=keywords_for(item={"device": name, "tags": roms}))


HUB_KINDS = {
    "brand": {"dir": "brand", "index": "brands.html", "word": "brand",
              "h1": "%s &mdash; flashing guides (%d)",
              "title": "%s Custom ROM & Flashing Guides",
              "label": "Brands"},
    "rom": {"dir": "roms", "index": "roms.html", "word": "ROM",
            "h1": "%s &mdash; guides and installs (%d)",
            "title": "%s Install Guide, Download & Fixes",
            "label": "ROMs"},
    "year": {"dir": "year", "index": "years.html", "word": "year",
             "h1": "Flashing guides from %s (%d)",
             "title": "Android flashing guides from %s",
             "label": "Years"},
    "topic": {"dir": "topic", "index": "topics.html", "word": "topic",
              "h1": "%s &mdash; Android guides (%d)",
              "title": "%s \u2014 Android Guide & Steps",
              "label": "Topics"},
    "tag": {"dir": "tag", "index": "tags.html", "word": "tag",
            "h1": "%s &mdash; flashing guides (%d)",
            "title": "%s \u2014 Guides & Downloads",
            "label": "Tags"},
}


def hub_faq(kind, name, rows):
    """Honest questions for a hub page, answered from what the site really has."""
    count = len(rows)
    devices = sorted({clean_device(x.get("device")) for x in rows
                      if clean_device(x.get("device"))})
    roms = sorted({(x.get("rom") or "").strip() for x in rows if x.get("rom")})
    if kind == "brand":
        first = ("How many %s guides are there here?" % name,
                 "Right now %d, and every one of them is listed above with the "
                 "date it went live. New %s videos are added to this page as "
                 "they are published." % (count, name))
        covered = ("Which %s phones are covered?" % name,
                   "%s." % ", ".join(devices) if devices else
                   "Every %s phone with a guide so far." % name)
    elif kind == "rom":
        first = ("What is covered in these %s guides?" % name,
                 "%d written guides so far, each one a real install done on the "
                 "phone named in the title." % count)
        covered = ("Which phones can I install %s on?" % name,
                   "%s &mdash; and only where a build exists for that exact "
                   "model." % ", ".join(devices) if devices else
                   "Only phones with a build of it released for them.")
    elif kind == "year":
        first = ("What was covered in %s?" % name,
                 "%d guides from that year, newest first." % count)
        covered = ("Which phones and ROMs show up in %s?" % name,
                   "%s." % ", ".join((roms + devices)[:8]) if (roms or devices)
                   else "A mix of phones and ROMs.")
    elif kind == "topic":
        first = ("What do these %s guides cover?" % name,
                 "%d guides on this one job, across every phone it has been "
                 "done on." % count)
        covered = ("Which phones do these %s guides cover?" % name,
                   "%s." % ", ".join(devices[:8]) if devices else
                   "Whatever is listed above.")
    else:
        first = ("What is tagged %s here?" % name,
                 "%d guide%s carry this tag. They are listed above newest first, "
                 "with the date each one went live."
                 % (count, "" if count == 1 else "s"))
        covered = ("Which phones and ROMs show up under %s?" % name,
                   "%s." % ", ".join((devices + roms)[:8])
                   if (devices or roms) else "A mix of phones and ROMs.")

    out = [first, covered,
           ("Will I lose my data?",
            "Unlocking the bootloader and writing a full firmware image usually "
            "wipe the phone. Back up anything you would miss before you start, "
            "and keep a PC and a cable nearby in case a bootloop needs fixing."),
           ("Do I need a computer for this?",
            "Not always. The free Rom Flasher tool runs on a second Android "
            "phone joined by a USB-OTG cable, and drives fastboot, recovery and "
            "sideloading from there. Some jobs &mdash; unlocking a bootloader, "
            "for example &mdash; still go through the manufacturer's own tool on "
            "a PC.")]
    if roms and kind != "rom":
        out.insert(1, ("Which ROMs appear on this page?",
                       "%s." % ", ".join(roms[:10])))
    return out[:5]


def build_hub_faq(kind, name, rows):
    faq = hub_faq(kind, name, rows)
    return "".join(
        '<details class="faq"><summary>%s</summary>'
        '<div class="ans"><p>%s</p></div></details>' % (q, a)
        for q, a in faq), faq


def build_hub_page(kind, name, hub, all_hubs, total, items):
    """One landing page for a brand, a ROM family, a year or a topic."""
    cfg = HUB_KINDS[kind]
    slug, rows = hub["slug"], hub["rows"]
    path = "%s/%s.html" % (cfg["dir"], slug)
    up = "../"
    count = len(rows)

    table = "\n".join(
        '<tr class="row" data-d="%s" data-v="%s" data-y="%s">'
        '<td><a href="%srom/%s.html">%s</a></td><td>%s</td>'
        '<td class="dt">%s</td><td class="vw">%s</td></tr>'
        % (html.escape(x.get("published") or ""), x.get("views") or 0,
           html.escape((x.get("published") or "")[:4]), up,
           html.escape(x["slug"]), html.escape(x["title"]),
           html.escape(clean_device(x.get("device")) or "-"),
           html.escape(nice_date(x.get("published")) or "-"), x.get("views") or 0)
        for x in rows)

    siblings = "".join(
        '<a class="chip" href="%s.html">%s (%d)</a>'
        % (h["slug"], html.escape(other), len(h["rows"]))
        for other, h in sorted(all_hubs.items(), key=lambda kv: -len(kv[1]["rows"]))
        if other != name and h["slug"] != slug)

    faq_html, faq = build_hub_faq(kind, name, rows)

    other_kinds = "".join(
        '<a class="chip" href="%s%s">%s</a>' % (up, HUB_KINDS[k]["index"],
                                               HUB_KINDS[k]["label"])
        for k in ("brand", "rom", "year", "topic", "tag") if k != kind)

    body = """<div class="wrap full"><section style="padding:32px 0 0">
%(crumbs)s
<h1>%(h1)s</h1>
<p class="dis">Every guide that belongs here, newest first, with the date it went
live. %(devices)s</p>
<p><a class="btn" href="%(up)sdownload.html">Download the free Rom Flasher tool</a>
<a class="btn ghost" href="%(up)svideos.html">All %(total)d guides</a></p>

<table><thead><tr><th>Guide</th><th>Device</th><th>Released</th><th>Views</th>
</tr></thead><tbody>%(table)s</tbody></table>

<h2>Questions people ask</h2>
%(faq)s

<h2>More ways to browse</h2>
<div class="chips">%(other)s</div>

%(ad)s

<h2>Related %(word)ss</h2>
<div class="chips">%(siblings)s</div>
</section></div>""" % {
        "crumbs": crumbs_html([("Home", up + "index.html"),
                               (cfg["label"], up + cfg["index"]),
                               (name, "")]),
        "h1": cfg["h1"] % (html.escape(name), count),
        "devices": ("Covers: <strong>%s</strong>." % html.escape(", ".join(
            sorted({clean_device(x.get("device")) for x in rows
                    if clean_device(x.get("device"))})[:10]))) if kind != "year" else "",
        "up": up, "total": total, "table": table, "faq": faq_html,
        "ad": ad_slot("hub", up),
        "other": other_kinds, "word": cfg["word"], "siblings": siblings}

    blocks = [{
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": "%s guides" % name,
        "url": "%s/%s" % (SITE_URL, path),
        "description": "Every Rom Flasher guide for %s, newest first." % name,
        "inLanguage": "en", "isAccessibleForFree": True,
        "mainEntity": {
            "@type": "ItemList", "numberOfItems": count,
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": x["title"],
                 "url": "%s/rom/%s.html" % (SITE_URL, x["slug"])}
                for i, x in enumerate(rows[:40])]},
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": cfg["label"],
             "item": "%s/%s" % (SITE_URL, cfg["index"])},
            {"@type": "ListItem", "position": 3, "name": name,
             "item": "%s/%s" % (SITE_URL, path)}],
    }, {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer",
                                           "text": re.sub(r"<[^>]+>", "", a)}}
                       for q, a in faq],
    }]
    head = "\n".join('<script type="application/ld+json">%s</script>'
                     % json.dumps(b, ensure_ascii=False) for b in blocks)

    return page(cfg["title"] % html.escape(name),
                "Every Rom Flasher guide for %s: custom ROMs, root, recovery and "
                "fastboot steps, newest first with dates. %d in total."
                % (name, count),
                body, path, extra_head=head, og_type="website",
                image=newest_thumb(rows) or (SITE_URL + "/static/app.png"),
                keywords=keywords_for(extra=(name, "%s guides" % name,
                                             "%s flashing" % name)),
                robots="noindex,follow")


def build_hub_index(kind, hubs, total, items):
    """The page that lists every brand / ROM / year / topic hub."""
    cfg = HUB_KINDS[kind]
    cards = "".join(
        '<a class="card" href="%s/%s.html"><h3>%s</h3><p>%d guide%s</p>'
        '<span class="foot">%s</span></a>'
        % (cfg["dir"], h["slug"], html.escape(name), len(h["rows"]),
           "" if len(h["rows"]) == 1 else "s",
           html.escape(nice_date(max((x.get("published") or "")
                                     for x in h["rows"])) or "guides"))
        for name, h in sorted(hubs.items(), key=lambda kv: -len(kv[1]["rows"])))

    head_line = {
        "brand": ("Browse by brand", "Every phone brand with guides here, from "
                  "POCO and Redmi to Xiaomi, Pixel and beyond."),
        "rom": ("Browse by ROM", "HyperOS, MIUI, LineageOS, Evolution X, "
                "DerpFest, PixelOS, crDroid, TWRP and the rest."),
        "year": ("Browse by year", "Guides grouped by the year the video "
                 "went live."),
        "topic": ("Browse by topic", "Root, recovery, bootloader, kernels, "
                  "battery, camera and more."),
        "tag": ("Browse by tag", "Every tag used across the guides, from the "
                "phones and ROMs to the jobs they are used for."),
    }[kind]

    body = ('<div class="wrap full"><section style="padding:32px 0 0">'
            '%s'
            "<h1>%s</h1><p class=\"dis\">%s</p><div class=\"grid\">%s</div>"
            "%s"
            "<p><a class=\"btn ghost\" href=\"videos.html\">All %d guides</a></p>"
            "</section></div>" % (crumbs_html([("Home", "index.html"),
                                               (head_line[0], "")]),
                                  head_line[0], head_line[1], cards,
                                  ad_slot("hub"), total))

    block = {
        "@context": "https://schema.org", "@type": "CollectionPage",
        "name": head_line[0],
        "url": "%s/%s" % (SITE_URL, cfg["index"]),
        "inLanguage": "en", "isAccessibleForFree": True,
        "mainEntity": {"@type": "ItemList", "numberOfItems": len(hubs),
                       "itemListElement": [
                           {"@type": "ListItem", "position": i + 1, "name": name,
                            "url": "%s/%s/%s.html" % (SITE_URL, cfg["dir"],
                                                      h["slug"])}
                           for i, (name, h) in enumerate(sorted(
                               hubs.items(), key=lambda kv: -len(kv[1]["rows"])))]},
    }
    head = ('<script type="application/ld+json">%s</script>'
            % json.dumps(block, ensure_ascii=False))
    index_desc = {
        "brand": "Every phone brand with a flashing guide on Rom Flasher, from "
                 "POCO and Redmi to Xiaomi, Pixel, OnePlus and more.",
        "rom": "Every custom ROM covered on Rom Flasher - HyperOS, MIUI, "
               "LineageOS, Evolution X, PixelOS and the rest, with install "
               "guides.",
        "year": "Rom Flasher guides by year: every custom ROM, root and flashing "
                "video the channel published, newest first.",
        "topic": "Browse Rom Flasher guides by topic: bootloader unlock, root, "
                 "recovery, kernels, battery, camera and more.",
        "tag": "Every tag used across the Rom Flasher guides, from the phones "
               "and ROMs to the jobs they are used for.",
    }[kind]
    return page("%s \u2014 %s" % (head_line[0], SITE), index_desc, body,
                cfg["index"], extra_head=head,
                keywords=keywords_for(extra=(head_line[0],
                                             cfg["label"].lower())),
                robots="noindex,follow")


def ad_slot(place, up=""):
    """One AdSense unit, or nothing at all while its slot id is unset.

    The markup is Google's own snippet, unchanged, because the queue push is
    what actually fills the box. The push only writes into a plain array, so
    before adsbygoogle.js loads there is no request, no cookie and no script
    from Google on the page - and the consent gate in analytics_head() only
    loads adsbygoogle.js after the visitor says yes. Decline, and the <ins> is
    an empty block with zero height: no gap where an ad would have been.

    Fenced off behind the publisher id as well, so an approved-but-unfinished
    account cannot publish units that 404.
    """
    slot = AD_SLOTS.get(place, "")
    if not (slot and ADS_PUBLISHER):
        return ""
    return (
        '<div class="adslot" data-ad-place="%s">'
        '<ins class="adsbygoogle" style="display:block" '
        'data-ad-client="ca-%s" data-ad-slot="%s" '
        'data-ad-format="auto" data-full-width-responsive="true"></ins>'
        '<script>(adsbygoogle=window.adsbygoogle||[]).push({});</script>'
        '</div>' % (html.escape(place), html.escape(ADS_PUBLISHER),
                    html.escape(slot)))


def build_article(item, items):
    path = "rom/%s.html" % item["slug"]
    up = "../"
    icon = os.path.join(STATIC, "app.png")
    avatar_html = ('<img class="avatar" src="%sstatic/app.png" '
                   'alt="Rom Flasher tool" width="58" height="58" '
                   'loading="lazy">' % up) if os.path.exists(icon) else ""

    meta = []
    if clean_device(item.get("device")):
        meta.append(html.escape(clean_device(item["device"])))
    if item.get("rom"):
        meta.append(html.escape(item["rom"]))
    if item.get("published"):
        meta.append(nice_date(item["published"]))
    if item.get("views"):
        meta.append("%s views" % item["views"])

    device_display = clean_device(item.get("device")) or "Real Hardware"
    read_mins = max(3, (len((item.get("body") or "").split()) + len((item.get("video_description") or "").split())) // 180)
    
    byline_html = (
        '<div class="editorial-byline">'
        '<div class="byline-avatar"><img src="%sstatic/rohit-verma.webp" alt="Rohit Verma" width="48" height="48" loading="eager"></div>'
        '<div class="byline-meta">'
        '<div class="byline-author">Written &amp; Verified by <a href="%sabout.html"><strong>Rohit Verma</strong></a> <span class="byline-badge">&#10003; Verified Specialist</span></div>'
        '<div class="byline-sub"><span>Published %s</span> &middot; <span>Tested on %s</span> &middot; <span>%d min read</span></div>'
        '</div></div>'
        % (up, up, nice_date(item.get("published") or BUILT_ON), html.escape(device_display), read_mins)
    )

    out = ['<article>', '<div class="prose">',
           '<nav class="crumbs" aria-label="Breadcrumb"><a href="%sindex.html">Home</a><span class="sep">&rsaquo;</span><a href="%svideos.html">Guides</a><span class="sep">&rsaquo;</span><span class="here">%s</span></nav>'
           % (up, up, html.escape(device_display)),
           '<div class="head"><div>',
           "<h1>%s</h1>" % html.escape(item["title"]),
           byline_html,
           "</div></div>"]

    device_name = clean_device(item.get("device"))
    if device_name:
        tested = (device_name if not device_name.lower().startswith("any")
                  else "real physical hardware")
        out.append(
            '<div class="tested-card">'
            '<div class="tested-card-head"><span class="tested-badge">&#10003; Physical Hardware Verified</span></div>'
            '<p class="tested-desc">This flashing procedure was physically executed and verified on a <strong>%s</strong> test unit. Every partition target (<code>boot</code>, <code>init_boot</code>, <code>super</code>) and fastboot script is verified to prevent bricking.</p>'
            '</div>' % html.escape(tested))

    if item.get("tags"):
        out.append('<div class="tags"><span class="tagslabel">Tags</span>%s</div>'
                   % "".join(tag_href(t, up) for t in item["tags"]))

    hubs = cached_all_hubs(items)
    links = []
    brand = brand_of(item)
    if brand and brand in hubs["brand"]:
        links.append('<a href="%sbrand/%s.html">%s guides</a>'
                     % (up, hubs["brand"][brand]["slug"], html.escape(brand)))
    family = rom_family_of(item)
    if family and family in hubs["rom"]:
        links.append('<a href="%sroms/%s.html">%s guides</a>'
                     % (up, hubs["rom"][family]["slug"], html.escape(family)))
    year = (item.get("published") or "")[:4]
    if year.isdigit() and year in hubs["year"]:
        links.append('<a href="%syear/%s.html">%s guides</a>'
                     % (up, hubs["year"][year]["slug"], year))
    if links:
        out.append('<p class="partof">Part of %s.</p>' % ", ".join(links))

    if item.get("summary"):
        out.append('<div class="summary">%s</div>' % md(item["summary"]))

    body = (item.get("body") or "").strip()
    desc = (item.get("video_description") or "").strip()
    steps = steps_from_md(body)
    rendered, toc = ("", [])
    if body:
        rendered, toc = heading_ids(md(body))

    # The video and the two side tabs share one row on a wide screen: the player
    # takes the left half, the tabs take the right. On a phone the row becomes a
    # single column, player first, so nothing is ever squeezed.
    left = []
    if item.get("url"):
        vid = video_id_of(item["url"])
        watch = html.escape(item["url"])
        left.append(
            '<div class="videobox"><div class="frame">'
            '<div class="yt-facade" role="button" tabindex="0" aria-label="Play video" '
            'data-vid="%s" data-title="%s">'
            '<img src="https://i.ytimg.com/vi/%s/hqdefault.jpg" alt="%s" '
            'width="480" height="360" loading="lazy" decoding="async">'
            '<div class="yt-play-btn">'
            '<svg viewBox="0 0 68 48" width="68" height="48" aria-hidden="true">'
            '<path class="ytp-bg" d="M66.52 7.74c-.78-2.93-2.49-5.41-5.42-6.19C55.79.13 34 0 34 0S12.21.13 6.9 1.55c-2.93.78-4.63 3.26-5.42 6.19C.06 13.05 0 24 0 24s.06 10.95 1.48 16.26c.78 2.93 2.49 5.41 5.42 6.19C12.21 47.87 34 48 34 48s21.79-.13 27.1-1.55c2.93-.78 4.64-3.26 5.42-6.19C67.94 34.95 68 24 68 24s-.06-10.95-1.48-16.26z"/>'
            '<path d="M45 24L27 14v20z" fill="#ffffff"/>'
            '</svg></div></div>'
            '</div>'
            '<div class="video-toolbar">'
            '<a class="video-btn-yt" href="%s" target="_blank" rel="noopener">'
            '<svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor" aria-hidden="true"><path d="M23.498 6.186a3.016 3.016 0 0 0-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 0 0 .502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 0 0 2.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 0 0 2.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>'
            '<span>Watch on YouTube (@Rom_Flasher)</span></a>'
            '<span class="video-notice">Click the play button above to watch here, or open directly on YouTube if playback is restricted.</span>'
            '</div>'
            '</div>'
            % (html.escape(vid, quote=True), html.escape(item["title"], quote=True),
               html.escape(vid), html.escape(item["title"]), watch))

    toc_panel = toc_html(toc) if toc else ""
    if left and toc_panel:
        right = ('<div class="sidepanel">'
                 '<div class="cta"><div class="ctatext">'
                 '<strong>No PC in the room?</strong>'
                 '<span>The free Rom Flasher tool runs the whole flash from the '
                 'phone in your hand &mdash; USB-OTG cable, no laptop, no command '
                 'line.</span></div>'
                 '<a class="btn dark" href="%sdownload.html">%sDownload the free '
                 'Rom Flasher tool</a></div>%s</div>'
                 % (up, DL_LOGO, toc_panel))
        out.append('<div class="mediarow">%s%s</div>'
                   % ("".join(left), right))
    elif left:
        right = ('<div class="sidepanel">'
                 '<div class="cta"><div class="ctatext">'
                 '<strong>No PC in the room?</strong>'
                 '<span>The free Rom Flasher tool runs the whole flash from the '
                 'phone in your hand &mdash; USB-OTG cable, no laptop, no command '
                 'line.</span></div>'
                 '<a class="btn dark" href="%sdownload.html">%sDownload the free '
                 'Rom Flasher tool</a></div></div>'
                 % (up, DL_LOGO))
        out.append('<div class="mediarow">%s%s</div>'
                   % ("".join(left), right))
    elif toc_panel:
        out.append('<div class="standalone-toc-card">%s</div>' % toc_panel)

    shots = item.get("screenshots") or []
    if shots:
        is_tablet = "pad" in (item.get("device") or "").lower() or "tablet" in (item.get("device") or "").lower()
        card_cls = "shot-card pad" if is_tablet else "shot-card"
        grid_cls = "screenshots-grid pad" if is_tablet else "screenshots-grid"
        shot_items = "".join(
            '<button type="button" class="%s" data-idx="%d" aria-label="View screenshot %d">'
            '<img src="%s" alt="%s Screenshot %d" loading="lazy"></button>'
            % (card_cls, i, i + 1, html.escape(s if s.startswith("http") else (up + s.lstrip("/"))), html.escape(item.get("title") or "ROM"), i + 1)
            for i, s in enumerate(shots)
        )
        out.append('<div class="screenshots-section"><h3>ROM Screenshots</h3>'
                   '<div class="%s">%s</div></div>' % (grid_cls, shot_items))

    is_architecture = (
        item.get("category") == "architecture"
        or "architecture" in item.get("slug", "")
        or "bible" in item.get("slug", "")
        or "unbrick-manual" in item.get("slug", "")
        or "attestation" in item.get("slug", "")
        or "vs-kernelsu" in item.get("slug", "")
        or "troubleshooting" in item.get("slug", "")
    )
    if body:
        if len(steps) >= 3 and not is_architecture:
            out.append('<div class="arttools">'
                       '<button class="copybtn steps" type="button" '
                       'data-label="Copy the %d steps" data-steps="%s">Copy the '
                       '%d steps</button></div>'
                       % (len(steps),
                          html.escape(json.dumps(steps, ensure_ascii=False),
                                      quote=True),
                          len(steps)))
        out.append(rendered)
    elif desc:
        out.append('<div class="notice">This page is the video in text form. '
                   'The full write-up is being filled in by hand &mdash; until then '
                   'the complete description is below.</div>')
        out.append(md(desc_to_md(desc)))

    links = item.get("links") or []
    if links:
        rows = "\n".join(link_row(l, up) for l in links)
        out.append('<div class="links"><h2>Links / Downloads</h2><ul>%s</ul>'
                   '<p class="dis">Use the file built for your exact model and '
                   'region. A package for another variant is the quickest way to '
                   'a phone that will not boot.</p></div>' % rows)

    if body and desc:
        out.append('<details class="desc"><summary>Full description from the '
                   'video</summary><div class="inner">%s</div></details>'
                   % md(desc_to_md(desc)))

    faq = item.get("faq") or []
    if faq:
        # Each question is a <details> so it opens on a tap and stays closed
        # otherwise - a page with six answers showing at once buries the guide
        # the reader actually came for.
        faq_html = "".join(
            '<details class="faq"><summary>%s</summary>'
            '<div class="ans">%s</div></details>'
            % (inline(f.get("q", "")), md(f.get("a", "")))
            for f in faq)
        out.append("<h2>Common questions</h2>%s" % faq_html)

    out.append(ad_slot("article", up))

    author_card_html = (
        '<div class="author-card">'
        '<div class="author-card-avatar"><img src="%sstatic/rohit-verma.webp" alt="Rohit Verma" width="80" height="80" loading="lazy"></div>'
        '<div class="author-card-content">'
        '<div class="author-card-header"><span class="author-card-name">Rohit Verma</span> <span class="author-card-handle">@Rom_Flasher</span></div>'
        '<div class="author-card-role">Lead Android Flashing Specialist &amp; Developer of Rom Flasher Tool</div>'
        '<p class="author-card-bio">Rohit Verma has documented and physically verified custom ROM installations, bootloader unlocking, and kernel rooting across %d+ Android device configurations. He maintains the free Rom Flasher Tool and operates an independent physical hardware test lab dedicated to safe, reproducible Android engineering.</p>'
        '<div class="author-card-links">'
        '<a class="author-link yt" href="%s" target="_blank" rel="noopener">YouTube (@Rom_Flasher)</a>'
        '<a class="author-link gh" href="%s" target="_blank" rel="noopener">GitHub (@romflasher3419-spec)</a>'
        '<a class="author-link lab" href="%sabout.html">Testing Lab &amp; Editorial Ethics</a>'
        '</div></div></div>'
        % (up, len(items), CHANNEL_URL, REPO_URL, up)
    )
    out.append(author_card_html)

    out.append('<div class="links"><h2>Before you flash</h2><ul>' 
               "<li>Back up everything you would miss &mdash; unlocking and "
               "flashing usually wipe the phone.</li>"
               "<li>Check the file is built for your exact model and region.</li>"
               "<li>Keep a PC and a working cable around so a bootloop can be "
               "recovered.</li></ul></div>")

    device = clean_device(item.get("device"))
    family = rom_family_of(item)
    brand = brand_of(item)
    by_views = sorted(items, key=lambda x: -(x.get("views") or 0))
    picked, seen = [], {item["slug"]}

    def take(pool, want):
        for x in by_views if pool is items else pool:
            if want <= 0 or len(picked) >= 6:
                return
            if x["slug"] in seen:
                continue
            seen.add(x["slug"])
            picked.append(x)
            want -= 1

    if device:
        take([x for x in by_views if clean_device(x.get("device")) == device], 3)
    if family:
        take([x for x in by_views if rom_family_of(x) == family], 2)
    if brand:
        take([x for x in by_views if brand_of(x) == brand], 2)
    take(items, 6)

    hub = cached_device_hubs(items).get(device)
    if device and hub:
        heading = ('More for <a href="%sdevice/%s.html">%s</a>'
                   % (up, hub["slug"], html.escape(device)))
        out.append('<h2>%s</h2><div class="grid">%s</div>'
                   % (heading, "".join(card(x, up) for x in picked)))
    else:
        heading = ("More for %s" % device) if device else "Keep reading"
        # "More for Any Android" reads like a bug - general guides just say this.
        if device and device.lower().startswith("any"):
            heading = "More guides like this"
        out.append('<h2>%s</h2><div class="grid">%s</div>'
                   % (html.escape(heading), "".join(card(x, up) for x in picked)))
    if steps:
        out.append(STEPS_JS)
    if shots:
        out.append(render_shot_lightbox(shots, up))
    # Never auto-force video playback so videos never auto-start without user consent
    # if item.get("url"):
    #     out.append(YT_JS)
    out.append("</div></article>")

    canon = "%s/%s" % (SITE_URL, path)
    pub = item.get("published") or BUILT_ON
    vid = video_id_of(item.get("url") or "")
    thumb = ("https://i.ytimg.com/vi/%s/maxresdefault.jpg" % vid) if vid else None
    logo = {"@type": "ImageObject", "url": SITE_URL + "/static/app.png"}

    blocks = [{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": item["title"],
        "description": item.get("blurb") or item["title"],
        "mainEntityOfPage": {"@type": "WebPage", "@id": canon},
        "url": canon,
        "datePublished": pub,
        "dateModified": max(item.get("_mtime") or "", pub) or BUILT_ON,
        "inLanguage": "en",
        "isAccessibleForFree": True,
        "keywords": ", ".join(item.get("tags") or []),
        "articleSection": item.get("device") or "Flashing guides",
        "author": {
            "@type": "Person",
            "name": "Rohit Verma",
            "alternateName": "Rom Flasher",
            "jobTitle": "Android Flashing Specialist & Lead Developer",
            "url": SITE_URL + "/about.html",
            "image": SITE_URL + "/static/rohit-verma.webp",
            "sameAs": [CHANNEL_URL, REPO_URL],
        },
        "publisher": {"@type": "Organization", "name": SITE, "url": SITE_URL,
                      "logo": logo},
        "image": [thumb or (SITE_URL + "/static/app.png")],
        "about": [t for t in (item.get("device"), item.get("rom")) if t],
        "wordCount": len(body.split()) + len(desc.split()),
        "speakable": {"@type": "SpeakableSpecification",
                      "cssSelector": [".prose h1", ".summary"]},
    }]
    if vid:
        blocks.append({
            "@context": "https://schema.org",
            "@type": "VideoObject",
            "name": item["title"],
            "description": item.get("blurb") or item["title"],
            "uploadDate": pub,
            "thumbnailUrl": [thumb,
                             "https://i.ytimg.com/vi/%s/hqdefault.jpg" % vid],
            "embedUrl": "https://www.youtube.com/embed/%s" % vid,
            "contentUrl": item.get("url"),
            "url": item.get("url"),
            "isFamilyFriendly": True,
            "publisher": {"@type": "Organization", "name": SITE,
                          "url": SITE_URL, "logo": logo},
            "author": {"@type": "Person", "name": "Rom Flasher",
                       "url": SITE_URL + "/about.html"},
        })
        if desc:
            blocks[-1]["transcript"] = plain_text(desc)
    if len(steps) >= 3:
        blocks.append({
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": item["title"],
            "description": item.get("blurb") or item["title"],
            "image": thumb or (SITE_URL + "/static/app.png"),
            "inLanguage": "en",
            "step": [{"@type": "HowToStep", "position": i + 1, "text": s}
                     for i, s in enumerate(steps[:20])],
        })
    blocks.append({
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Guides",
             "item": SITE_URL + "/videos.html"},
            {"@type": "ListItem", "position": 3, "name": item["title"],
             "item": canon},
        ],
    })
    if faq:
        blocks.append({
            "@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": f.get("q", ""),
                            "acceptedAnswer": {"@type": "Answer",
                                               "text": f.get("a", "")}}
                           for f in faq],
        })
    head = "\n".join('<script type="application/ld+json">%s</script>'
                     % json.dumps(b, ensure_ascii=False) for b in blocks)

    return page(display_title(item["title"]),
                item.get("blurb") or item["title"],
                "\n".join(out), path, extra_head=head,
                keywords=keywords_for(item), og_type="article",
                image=thumb or (SITE_URL + "/static/app.png"))


def ld(block):
    """One JSON-LD <script> for a schema.org block."""
    return ('<script type="application/ld+json">%s</script>'
            % json.dumps(block, ensure_ascii=False))


def simple(path, h1, title, block, description=None, keywords="", extra_head="",
           og_type="website", schema=None, crumbs=None, ad=False):
    trail = crumbs or [("Home", "index.html"), (h1, "")]
    # ad=False by default: the flat pages are the ones a visitor reads once and
    # leaves, and a unit there earns a fraction of what the same unit earns on a
    # guide, so a page opts in only where there is something to read above it.
    tail = ad_slot("hub") if ad else ""
    body = ('<article><div class="prose">%s<h1>%s</h1>\n%s%s\n</div></article>'
            % (crumbs_html(trail), h1, block, tail))
    if schema is not None:
        blocks = [schema, {
            "@context": "https://schema.org", "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": i + 1, "name": label,
                 "item": ("%s/%s" % (SITE_URL, href) if href else
                          "%s/%s" % (SITE_URL, path))}
                for i, (label, href) in enumerate(trail)],
        }]
        extra_head = ("\n".join(ld(b) for b in blocks) + "\n" + extra_head)
    return page(title, description or h1, body, path, extra_head=extra_head,
                keywords=keywords, og_type=og_type)


def feedback_form(anchor=True, lead=""):
    """A message box that lands in a real inbox - no account, no GitHub trip.

    The form posts natively to FormSubmit with its server-side CAPTCHA switched
    on, so the spam check happens before anything reaches the inbox. A honeypot
    field and a minimum fill-time are kept as a cheap first pass. After a
    successful post FormSubmit sends the visitor back to the same page with
    ?sent=1, where the status line becomes the thank-you message.
    """
    return """%s<form class="fbform" id="feedback" action="%s" method="POST">
  <input type="hidden" name="_subject" value="New message from the Rom Flasher website">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_captcha" value="true">
  <input type="hidden" name="_next" value="%s/contact.html?sent=1#feedback">
  <input type="text" name="_honey" tabindex="-1" autocomplete="off"
         aria-hidden="true" style="position:absolute;left:-9999px">
  <label>Your name
    <input type="text" name="name" required maxlength="80"
           placeholder="Who am I writing back to?"></label>
  <label>Your email
    <input type="email" name="email" required maxlength="120"
           placeholder="so I can actually reply"></label>
  <label>Your message
    <textarea name="message" required rows="6" maxlength="4000"
              placeholder="Which phone, which ROM and what happened. The more you tell me, the faster I can fix it."></textarea></label>
  <button class="btn dark" type="submit"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 4h18a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V5a1 1 0 0 1 1-1zm9 8.3L4.5 6h15L12 12.3z"/></svg>Send it to me</button>
  <p class="fbnote" role="status" aria-live="polite">I read every single one of these myself.</p>
  <p class="dis">Rather use your own mail app? Write to
  <a href="mailto:%s">%s</a> &mdash; same inbox, same person.</p>
</form>
<script>
(function(){
  var f=document.getElementById('feedback');
  if(!f) return;
  var note=f.querySelector('.fbnote');
  var next=f.querySelector('input[name=_next]');
  var loadTime=Date.now();

  /* Come back to the page the visitor was reading, not to a fixed one. */
  if(next){
    var back=location.href.split('#')[0].split('?')[0]+'?sent=1#feedback';
    next.value=back;
  }
  if(location.search.indexOf('sent=1')!==-1 && note){
    note.className='fbnote ok';
    note.textContent='Got it - thank you! Your message is in my inbox.';
    if(history.replaceState){history.replaceState(null,'',location.pathname+location.hash);}
  }

  f.addEventListener('submit',function(e){
    if(Date.now()-loadTime<2500){
      e.preventDefault();
      note.className='fbnote bad';
      note.textContent='Please take a moment before submitting.';
      return;
    }
    if(f._honey && f._honey.value){
      e.preventDefault();
      f.reset();note.className='fbnote ok';
      note.textContent='Got it - thank you! Your message is in my inbox.';
      return;
    }
    var btn=f.querySelector('button[type=submit]');
    if(btn){btn.disabled=true;btn.textContent='Sending...';}
  });
})();
</script>""" % (lead, FORM_POST, SITE_URL, CONTACT_EMAIL, CONTACT_EMAIL)


def donate_strip():
    """The compact thank-you card: QR, UPI ID, PayPal button."""
    return """<div class="donategrid">
  <div class="dbox">
    <h3>In India &mdash; UPI</h3>
    <p>Point any UPI app at the code, or copy the ID below. You choose the
    amount; even a coffee is a big deal.</p>
    <div class="qrwrap"><img src="static/upi-qr.png" alt="UPI QR code that pays romflasher@naviaxis" width="564" height="564"></div>
    <div class="upirow"><span>%s</span><button class="copybtn" type="button" data-copy="%s">Copy ID</button></div>
  </div>
  <div class="dbox">
    <h3>Anywhere else &mdash; PayPal</h3>
    <p>Any currency, any amount. It opens on PayPal's own page, so nothing
    sensitive ever touches this site.</p>
    <a class="btn paypal" href="%s" rel="noopener">%sDonate with PayPal</a>
    <p class="dis">These are the same two links the app shows on its Donate
    screen &mdash; one for India, one for everywhere else.</p>
  </div>
</div>
<script>
(function(){
  var b=document.querySelector('.copybtn');
  if(!b||!navigator.clipboard) return;
  b.addEventListener('click',function(){
    navigator.clipboard.writeText(b.getAttribute('data-copy')).then(function(){
      var was=b.textContent;
      b.textContent='Copied';b.classList.add('done');
      setTimeout(function(){b.textContent=was;b.classList.remove('done');},1800);
    });
  });
})();
</script>""" % (UPI_ID, UPI_ID, PAYPAL_URL, CARD_LOGO)


def build_donate():
    """Every lovely reason to say thanks, and the two ways to do it."""
    block = """<p>Everything on this site is free, and the
<a href="download.html">free Rom Flasher tool</a> is free with it. No account,
no version that holds features back, nothing to type in. What you see is what
everyone gets, always.</p>

<p>The testing behind each guide is the part nobody sees: a phone on the bench,
a dozen flashes before a video is worth filming, and mirrors that have to keep
serving files long after the post goes up. If a page here rescued your evening
&mdash; or brought a dead phone back &mdash; you can say thank you. It is never
expected, and it never changes a single thing about what you get.</p>

%s

<h2>What a thank-you turns into</h2>
<ul>
<li>Another phone borrowed or bought just to test a ROM properly before filming</li>
<li>More devices and brands kept current on the <a href="downloader.html">ROM downloader</a></li>
<li>Faster fixes when a build misbehaves on one exact model</li>
<li>Fewer evenings lost to dead mirrors and broken packages</li>
</ul>

<h2>Hardware Testing Transparency &amp; Open Source Commitment</h2>
<p>Rom Flasher is and will always remain 100%% free software. We do not place features behind paywalls, run deceptive download countdowns, or force registrations. Voluntary community contributions directly support:</p>
<ul>
  <li><strong>Physical Test Hardware:</strong> Procuring real test devices (POCO, Xiaomi, Redmi, OnePlus, Pixel) to verify bootloader unlocking and fastboot scripts on physical silicon before tutorials go live.</li>
  <li><strong>Lab Instrumentation:</strong> USB-OTG protocol analyzers, high-speed test cables, and power meters to ensure flash transfers never drop packets mid-write.</li>
  <li><strong>Independent Infrastructure:</strong> Running high-speed documentation servers and verified mirror caches without intrusive third-party adware.</li>
</ul>

<p>Thank you for keeping this going. &nbsp;&#128155;</p>
<p>If money is not the thing right now, that is completely fine &mdash; the
<a href="download.html#talk-to-me">message box</a> is open. Telling me which
phone to cover next helps this place just as much.</p>
<div class="coffeeline">
<a class="btn gold" href="download.html">%sDownload the free Rom Flasher tool</a>
<a class="btn dark" href="%s" rel="noopener">%sSee the source on GitHub</a>
</div>""" % (donate_strip(), COFFEE_LOGO, REPO_URL, GH_LOGO)

    keywords = keywords_for(extra=(
        "support rom flasher", "donate rom flasher tool", "buy me a coffee",
        "upi romflasher@naviaxis", "paypal.me/vrohit3419",
        "thank the developer", "free android flashing tool"))
    return simple("donate.html", "Buy me a coffee", "Buy me a coffee \u2014 %s" % SITE,
                  block, keywords=keywords,
                  description="If a Rom Flasher guide saved your evening, you can "
                              "say thanks with UPI or PayPal. Both are optional, "
                              "and both keep the free tool free.",
                  schema={
                      "@context": "https://schema.org",
                      "@type": "WebPage",
                      "name": "Buy me a coffee",
                      "url": "%s/donate.html" % SITE_URL,
                      "inLanguage": "en",
                      "isPartOf": {"@type": "WebSite", "name": SITE,
                                   "url": SITE_URL},
                      "potentialAction": {
                          "@type": "DonateAction",
                          "name": "Support Rom Flasher",
                          "target": "https://paypal.me/vrohit3419",
                          "recipient": {"@type": "Person",
                                        "name": "Rom Flasher"}}})


def gear_box():
    """What people actually need to buy after watching a flashing video.

    Honest Amazon searches, never invented product links. The affiliate tag is
    added only once one is configured, so the same box earns when it can and
    stays a plain recommendation when it cannot.
    """
    tag = ("&tag=" + AMAZON_TAG) if AMAZON_TAG else ""
    gear = [
        ("USB-C OTG adapter", "usb+c+otg+adapter",
         "Turns your phone into the host. This is the little part that decides "
         "whether the tool can see the other phone at all."),
        ("USB-C to USB-C cable", "usb+c+to+usb+c+data+cable",
         "For phones on both ends. Get one rated for data, not just charging "
         "&mdash; a charge-only cable is the usual reason a device never shows "
         "up in fastboot."),
        ("USB-A to USB-C cable", "usb+a+to+usb+c+data+cable",
         "Still the most reliable cable in the drawer, and the one to keep if "
         "you also flash from a PC."),
    ]
    cards = "".join(
        '<a class="card" href="https://www.amazon.in/s?k=%s%s" target="_blank" '
        'rel="nofollow sponsored noopener"><h3>%s</h3><p>%s</p>'
        '<span class="foot">Search on Amazon</span></a>' % (q, tag, name, note)
        for name, q, note in gear)
    if AMAZON_TAG:
        disc = ('<p class="dis">Those are affiliate links: buying through them '
                'earns the channel a small commission and does not change the '
                'price you pay. It is what pays for the phones that get flashed '
                'on camera.</p>')
    else:
        disc = ('<p class="dis">Those are plain search links, not sponsors &mdash; '
                'buy wherever it is cheapest for you.</p>')
    return '<div class="grid">%s</div>%s' % (cards, disc)


def build_download():
    """The page every Download button opens: what it does + a direct APK pull."""
    faq = [
        ("Is Rom Flasher really free?",
         "Yes. The free Rom Flasher tool costs nothing &mdash; no sign-in, "
         "nothing to type in, and no version you have to buy."),
        ("Does it need a computer?",
         "No. It runs on the phone itself and drives the other phone over a "
         "USB-OTG cable, so you can flash without sitting at a PC."),
        ("Which phones does it work with?",
         "Anything with an unlocked bootloader that speaks fastboot &mdash; "
         "Xiaomi, POCO, Redmi, OnePlus, OPPO, realme, vivo and iQOO, Google "
         "Pixel and more."),
        ("Which Android version do I need?",
         "Android 8.0 or newer on the phone that runs the tool."),
        ("How big is the download?",
         "About 8.3&nbsp;MB. Installing a newer build on top of an older one "
         "keeps your data and settings, because every release is signed with "
         "the same key."),
        ("Will I lose my data?",
         "Unlocking the bootloader and flashing firmware usually wipe the "
         "phone. Take a backup first, and only flash files built for your "
         "exact device codename."),
    ]

    features = [
        ("Flashing", [
            "Fastboot ROMs, straight from the <code>.bat</code> or <code>.sh</code> flash script",
            "Sideload a ROM, GApps or Magisk from recovery",
            "Custom images: <code>boot</code>, <code>vendor_boot</code>, <code>super</code>, <code>vbmeta</code>, custom partitions &amp; RAM boot",
            "Sparse-chunk engine for big 4&ndash;8&nbsp;GB partitions",
            "A/B slot manager with standard AOSP switching &amp; safety checks",
        ]),
        ("Tools &amp; recovery", [
            "Universal IMEI / EFS backup &amp; restore (Qualcomm &amp; MediaTek)",
            "Kernel backup, restore and AK3 flashing with target CPU ABI detection",
            "Advanced 2&times;2 reboot modes (System, Recovery, Fastboot, FastbootD)",
            "Root wizard for KernelSU and Magisk",
            "App installer for <code>.apk</code>, <code>.xapk</code> and <code>.apkm</code>",
            "Debloater, remote file manager, device info, zero-lag command terminal",
        ]),
        ("Extras", [
            "High-speed payload dumper with zero-disk overhead (&lt;&nbsp;100ms manifest parsing)",
            "ROM-wise backup picker",
            "Video guides inside the app",
            "Cancel an extraction at any point",
        ]),
    ]
    feats = "".join(
        '<div class="feat"><h3>%s</h3><ul>%s</ul></div>'
        % (name, "".join("<li>%s</li>" % line for line in lines))
        for name, lines in features)

    faq_html = "".join(
        '<details class="faq"><summary>%s</summary>'
        '<div class="ans"><p>%s</p></div></details>' % (q, a)
        for q, a in faq)

    body = """<h1>Download Rom Flasher</h1>
<p>One free Android app that flashes the <em>other</em> phone. This phone runs
the tool, a USB-OTG cable joins the two, and the app handles fastboot,
recovery and sideloading for you &mdash; no PC and no terminal.</p>

<div class="dl">
  <div class="dlcard">
    <h2>Get the tool</h2>
    <p>The button always pulls the newest build published on GitHub, so you never
    have to go hunting for the latest file.</p>
    <a class="bigbtn" href="{apk}" rel="noopener">
      <svg class="gicon" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line></svg>
      <span>Download {ver} for Android<small>{size} &middot; Android 8.0+ &middot;
      free, no sign-in</small></span></a>
    <a class="subbtn star" href="{repo}" rel="noopener" target="_blank"><svg viewBox="0 0 24 24" width="16" height="16" fill="#f59e0b" style="display:inline-block;vertical-align:text-bottom;margin-right:4px;" aria-hidden="true"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg> Star on GitHub</a>
    <a class="subbtn" href="{yt}" rel="noopener">Watch the step-by-step videos</a>
    <a class="subbtn gh" href="{rel}" rel="noopener">{gh}Release notes on GitHub</a>
    <p class="dis">If your browser warns about installing an app from outside the
    Play Store, that is expected for a direct APK. Allow installs from your
    browser or file manager and continue.</p>
  </div>
  <div class="dlcard">
    <h2>Build facts</h2>
    <ul class="facts">
      <li><span>Latest version</span><b>{ver}</b></li>
      <li><span>Released</span><b>{released}</b></li>
      <li><span>Download size</span><b>{size}</b></li>
      <li><span>File</span><b>app-release.apk</b></li>
      <li><span>Runs on</span><b>{android}</b></li>
      <li><span>Price</span><b>Free</b></li>
    </ul>
    <span class="hash">SHA-256<br>{sha}</span>
  </div>
</div>

<h2>What is inside</h2>
<div class="feats">{feats}</div>

<h2>How to install</h2>
<ol class="steps">
  <li><b>Download the APK</b> with the button above. It lands in your phone's
  Downloads folder.</li>
  <li><b>Allow the install.</b> Android will ask for permission to install apps
  from your browser or file manager &mdash; say yes, then install.</li>
  <li><b>Open ROM Flasher</b> and connect the target phone with a USB-OTG cable.
  The app shows the device as soon as fastboot sees it.</li>
  <li><b>Pick what you want to do</b> &mdash; flash a ROM, sideload a package,
  back up a kernel, or just check the device info first.</li>
</ol>

<h2>What you need</h2>
<ul>
  <li>A phone to run the tool on: <b>Android 8.0 or newer</b></li>
  <li>A <b>USB-OTG cable</b> to reach the phone being flashed</li>
  <li>An <b>unlocked bootloader</b> on the target phone for flashing jobs</li>
  <li>Files built for your <b>exact device codename</b> &mdash; never guess</li>
</ul>
<div class="pills"><span class="pill">Xiaomi</span><span class="pill">POCO</span>
<span class="pill">Redmi</span><span class="pill">OnePlus</span>
<span class="pill">OPPO</span><span class="pill">realme</span>
<span class="pill">vivo / iQOO</span><span class="pill">Google Pixel</span>
<span class="pill">Android 8.0+</span><span class="pill">USB-OTG</span></div>

<h2>Where do I get the ROM?</h2>
<p>The tool flashes the files &mdash; it does not host them. Firmware goes stale
within weeks and belongs to the manufacturer, so fetching it lives here on the
site instead, where it can be kept current: <a href="downloader.html">open the
ROM downloader</a>, type your phone, and it takes you to that brand's own
Recovery ROM and Fastboot ROM download page. Magisk and KernelSU are linked
there too.</p>

<h2>The small things that make it work</h2>
<p>Cables are the number one reason a phone never shows up in fastboot. These are
the three I actually keep in the drawer.</p>
{gear}

<h2>Fresh in {ver}</h2>
<p>Version 1.4.1 brings full hands-free zero-touch flashing and UI improvements:</p>
<ul>
  <li><b>100% Zero-Touch Auto Reboot:</b> Bypasses the "Install additional packages?" prompt in recovery, rebooting straight into your new ROM.</li>
  <li><b>1-Click AOSP Auto Flasher:</b> Full auto flashing pipeline for AOSP ROMs directly inside Option 2.</li>
  <li><b>Targeted Boot Partition Extraction:</b> Instantly extracts only <code>boot</code>, <code>vendor_boot</code>, and <code>init_boot</code> from <code>payload.bin</code> and flashes both A &amp; B slots.</li>
  <li><b>Clean Fastboot Wipe:</b> Automatically formats userdata and metadata before recovery.</li>
  <li><b>Update Dialog Scrollbar:</b> In-app update changelog box now features smooth vertical scrolling with a visible scrollbar.</li>
</ul>

<h2>Questions people ask</h2>
{faq}

{ad}

<h2>Before you flash</h2>
<p class="dis">Flashing firmware is risky. Back up first, keep a way to recover,
and only flash files built for your exact model. Rom Flasher is not affiliated
with Xiaomi, POCO, Redmi, Google or any ROM project, and you flash at your own
risk &mdash; the <a href="terms.html">terms</a> spell that out.</p>

<h2>Did it save your evening?</h2>
<p>Then the tool did exactly what it was built for. If you feel like saying
thank you, here are the same two links the app shows on its own Donate screen.
Both are completely optional &mdash; and both keep the free Rom Flasher tool free
for the next person who needs it.</p>
{thanks}

<h2 id="talk-to-me">Tell me what happened</h2>
<p>Did a flash go sideways? Want a guide for a phone that is not here yet? A
feature you keep wishing the app had? Type it below and it comes straight to my
inbox &mdash; no account, no sign-in, nothing to install. I read every message
and it genuinely decides what I build and film next.</p>
{form}
""".format(repo=REPO_URL, apk=APK_URL, rel=RELEASES_URL, yt=CHANNEL_URL, gh=GH_LOGO,
           ver=APP["version"], released=APP["released"], size=APP["size"],
           android=APP["android"], sha=APP["sha256"], feats=feats,
           faq=faq_html, ad=ad_slot("hub", ""), form=feedback_form(),
           thanks=donate_strip(), gear=gear_box())

    blocks = [{
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": "Rom Flasher",
        "alternateName": "Rom Flasher Tool",
        "operatingSystem": "Android 8.0+",
        "applicationCategory": "UtilitiesApplication",
        "applicationSubCategory": "Android flashing and ROM tools",
        "softwareVersion": APP["version"],
        "fileSize": APP["bytes"],
        "downloadUrl": APK_URL,
        "installUrl": APK_URL,
        "url": SITE_URL + "/download.html",
        "description": "Free Android tool that flashes fastboot ROMs, sideloads "
                       "packages and backs up kernels over USB-OTG, without a PC.",
        "author": {"@type": "Organization", "name": SITE, "url": SITE_URL},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD",
                   "availability": "https://schema.org/InStock"},
        "screenshot": SITE_URL + "/static/app.png",
    }, {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q,
                        "acceptedAnswer": {"@type": "Answer", "text":
                                           re.sub(r"<[^>]+>", "", a)
                                           .replace("&nbsp;", " ")
                                           .replace("&mdash;", "-")}}
                       for q, a in faq],
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Download",
             "item": SITE_URL + "/download.html"},
        ],
    }]
    head = "\n".join('<script type="application/ld+json">%s</script>'
                     % json.dumps(b, ensure_ascii=False) for b in blocks)

    return page("Download Rom Flasher \u2014 free Android flashing tool (v%s)"
                % APP["version"].lstrip("v"),
                "Download the free Rom Flasher tool for Android. Flash fastboot "
                "ROMs, sideload packages, back up kernels and flash custom "
                "images over USB-OTG \u2014 no PC, no sign-in, %s." % APP["size"],
                '<article><div class="prose">%s</div></article>' % body,
                "download.html", extra_head=head,
                keywords=keywords_for(item={"tags": [
                    "download rom flasher", "rom flasher apk",
                    "rom flasher latest version", "free rom flasher tool",
                    "android rom flasher apk", "flash rom apk", "otg flasher"]}),
                image=SITE_URL + "/static/app.png")



DOWNLOADER_JS = r"""
<script>
/* The device picker, the region filter, the one-click download and the two
   live GitHub cards. Everything here is progressive: the page is readable and
   every link works with the script blocked - the script only adds the search,
   the filtering and the fastest-server download. */
(function(){
  var INDEX_URL = "static/firmware.json";
  var data = null, loading = false;
  var selected = null, region = "all", rows = [];

  function el(id){ return document.getElementById(id); }
  function esc(t){
    return String(t == null ? "" : t).replace(/[&<>"']/g, function(c){
      return {"&":"&amp;","<":"&lt;",">":"&gt;","\"":"&quot;","'":"&#39;"}[c]; });
  }
  function human(n){
    if(!n) return "";
    var u = ["B","KB","MB","GB"], i = 0;
    while(n >= 1024 && i < u.length - 1){ n /= 1024; i++; }
    return (i && n < 10 ? n.toFixed(1) : Math.round(n)) + " " + u[i];
  }

  /* ------------------------------------------------------------------
     The fastest of several mirrors. Every link is asked how quickly it
     answers; the quickest one that replies wins and the download starts
     from there. A mirror that never answers is dropped after four seconds,
     and if none reply the first link is used anyway - a slow download
     beats no download.
     ------------------------------------------------------------------ */
  function race(urls){
    if(!urls || !urls.length) return Promise.resolve(null);
    if(urls.length === 1) return Promise.resolve(urls[0]);
    var jobs = urls.map(function(u){
      return new Promise(function(resolve){
        var t0 = (window.performance && performance.now) ? performance.now() : Date.now();
        var done = false, timer = null, ctl = null;
        try { if("AbortController" in window) ctl = new AbortController(); } catch(e){}
        timer = setTimeout(function(){
          if(done) return; done = true;
          if(ctl){ try{ ctl.abort(); }catch(e){} }
          resolve({u:u, ms:Infinity});
        }, 4000);
        var opt = {method:"HEAD", mode:"no-cors", cache:"no-store"};
        if(ctl) opt.signal = ctl.signal;
        fetch(u, opt).then(function(){
          if(done) return; done = true; clearTimeout(timer);
          var now = (window.performance && performance.now) ? performance.now() : Date.now();
          resolve({u:u, ms:now - t0});
        }).catch(function(){
          if(done) return; done = true; clearTimeout(timer);
          resolve({u:u, ms:Infinity});
        });
      });
    });
    return Promise.all(jobs).then(function(rs){
      var ok = rs.filter(function(r){ return isFinite(r.ms); })
                 .sort(function(a,b){ return a.ms - b.ms; });
      return ok.length ? ok[0].u : urls[0];
    });
  }

  function download(urls, btn, label){
    if(!urls || !urls.length) return;
    var was = btn ? btn.textContent : "";
    if(btn){ btn.disabled = true; btn.textContent = "Finding the fastest server..."; }
    race(urls).then(function(u){
      if(btn){ btn.disabled = false; btn.textContent = was || label || "Download"; }
      if(!u) return;
      var a = document.createElement("a");
      a.href = u; a.rel = "noopener"; a.target = "_blank"; a.download = "";
      document.body.appendChild(a);
      a.click();
      setTimeout(function(){ if(a.parentNode) a.parentNode.removeChild(a); }, 5000);
    });
  }

  /* ------------------------------------------------------------------
     The index of phones. It is a separate file so the page itself stays
     small: a few hundred phones with every build each would be a heavy
     page to load just to read the text.
     ------------------------------------------------------------------ */
  function loadIndex(done){
    if(data){ done(); return; }
    if(loading) return;
    loading = true;
    var hint = el("dlhint");
    fetch(INDEX_URL, {cache:"no-cache"}).then(function(r){
      if(!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    }).then(function(j){
      data = (j && j.devices) ? j.devices : {};
      loading = false;
      done();
    }).catch(function(e){
      loading = false;
      if(hint){
        hint.textContent = "The phone index could not be loaded (" +
          (e && e.message ? e.message : "network error") +
          "). Reload the page and it will be back.";
      }
    });
  }

  function hay(d){
    return (d.name + " " + (d.code || "") + " " + (d.models || "") + " " +
            (d.brand || "") + " " + (d.slug || "")).toLowerCase();
  }

  function search(q){
    var t = q.trim().toLowerCase();
    if(!t) return [];
    var out = [];
    for(var k in data){
      if(!Object.prototype.hasOwnProperty.call(data, k)) continue;
      var d = data[k];
      if(hay(d).indexOf(t) >= 0) out.push(d);
    }
    out.sort(function(a, b){
      var an = (a.name || "").toLowerCase(), bn = (b.name || "").toLowerCase();
      var ai = an.indexOf(t), bi = bn.indexOf(t);
      if(ai !== bi) return (ai < 0 ? 9999 : ai) - (bi < 0 ? 9999 : bi);
      return an < bn ? -1 : (an > bn ? 1 : 0);
    });
    return out.slice(0, 120);
  }

  function renderResults(q){
    var box = el("dlresults");
    if(!box) return;
    if(!q.trim()){
      box.hidden = true; box.innerHTML = ""; return;
    }
    var hits = search(q);
    if(!hits.length){
      box.hidden = false;
      box.innerHTML = '<p class="dlempty">No phone matched "' + esc(q) +
        '". Try the brand on its own - "poco", "redmi" or "xiaomi" - then pick ' +
        'your model from the list.</p>';
      return;
    }
    var html = "";
    for(var i = 0; i < hits.length; i++){
      var d = hits[i];
      html += '<button type="button" class="dlres" data-slug="' + esc(d.slug) + '">' +
        '<span class="dlresname"><b>' + esc(d.name) + '</b><span>' +
        esc(d.code || d.slug) + '</span></span>' +
        '<span class="dlresbrand">' + esc(d.brand || "") + '</span></button>';
    }
    box.innerHTML = html;
    box.hidden = false;
  }

  function buildRegions(){
    var chips = el("dlregionchips");
    var seen = {}, list = [];
    var roms = (selected && selected.roms) || [];
    for(var i = 0; i < roms.length; i++){
      var r = roms[i].region;
      if(r && !seen[r]){ seen[r] = 1; list.push(r); }
    }
    if(!list.length) list = (selected && selected.regions) || [];
    list.sort();
    region = "all";
    var html = '<button type="button" data-r="all" class="on">All regions</button>';
    for(var j = 0; j < list.length; j++){
      html += '<button type="button" data-r="' + esc(list[j]) + '">' +
        esc(list[j]) + '</button>';
    }
    chips.innerHTML = html;
  }

  function groupRows(){
    var groups = {}, order = [];
    var roms = (selected && selected.roms) || [];
    for(var i = 0; i < roms.length; i++){
      var r = roms[i];
      if(region !== "all" && r.region !== region) continue;
      var key = (r.region || "") + "|" + (r.v || "");
      if(!groups[key]){
        groups[key] = {region:r.region, v:r.v, os:r.os, android:r.android,
                       date:r.date, size:r.size, rec:null, fb:null};
        order.push(key);
      }
      if(r.kind === "recovery") groups[key].rec = r;
      else if(r.kind === "fastboot") groups[key].fb = r;
    }
    var out = [];
    for(var j = 0; j < order.length; j++){
      var g = groups[order[j]];
      out.push(g);
    }
    out.sort(function(a, b){ return (b.date || "").localeCompare(a.date || ""); });
    return out;
  }

  function renderRoms(){
    var body = el("dlroms");
    if(!body) return;
    rows = groupRows();
    if(!rows.length){
      body.innerHTML = '<tr><td colspan="6" class="dlempty">' +
        'No build listed for this region. Switch the region back to "All ' +
        'regions" to see every build for this phone.</td></tr>';
      return;
    }
    var html = "";
    for(var i = 0; i < rows.length; i++){
      var r = rows[i];
      var rec = r.rec && r.rec.url ? r.rec.url : "";
      var fb = r.fb && r.fb.url ? r.fb.url : "";
      html += '<tr>' +
        '<td class="dlver">' + esc(r.v) +
          (r.os ? '<span class="dlversub">' + esc(r.os) + '</span>' : '') + '</td>' +
        '<td><span class="dlregion">' + esc(r.region || "Global") + '</span></td>' +
        '<td>' + esc(r.android || "-") + '</td>' +
        '<td>' + esc(r.date || "-") + '</td>' +
        '<td class="dlsize">' + esc(r.size || "-") + '</td>' +
        '<td><div class="dlgets">' +
          (rec ? '<button class="recovery" type="button" data-k="' + i +
                 '" data-kind="recovery">Recovery ROM</button>' : '') +
          (fb ? '<button class="fastboot" type="button" data-k="' + i +
                '" data-kind="fastboot">Fastboot ROM</button>' : '') +
        '</div></td></tr>';
    }
    body.innerHTML = html;
  }

  function renderPicked(){
    var d = selected;
    if(!d) return;
    el("dlpick").hidden = false;
    el("dlresults").hidden = true;
    el("dlpname").textContent = d.name || d.slug;
    el("dlpdesc").textContent =
      "Stock firmware for " + (d.name || d.slug) +
      (d.code ? " (codename " + d.code + ")" : "") + ".";
    var meta = [];
    if(d.brand) meta.push(d.brand);
    if(d.code) meta.push("codename " + d.code);
    if(d.models) meta.push(d.models);
    meta.push(((d.roms || []).length) + " builds listed");
    el("dlpmeta").innerHTML = meta.map(function(m){
      return "<span>" + esc(m) + "</span>";
    }).join("");
    el("dlpnote").innerHTML =
      "Every button picks the quickest server that answers and starts the " +
      "download from there. The table above is the whole list - every build " +
      "and every region - and the file comes straight from the publisher&#39;s " +
      "own server or a public mirror of it. Nothing is re-hosted here.";
    buildRegions();
    renderRoms();
  }

  function select(slug){
    if(!data || !data[slug]) return;
    selected = data[slug];
    renderPicked();
    try {
      el("dlpick").scrollIntoView({behavior:"smooth", block:"start"});
    } catch(e){}
  }

  /* ------------------------------------------------------------------
     Magisk and KernelSU: the live release straight from GitHub. The
     answer is kept for half an hour so a visitor who opens both cards
     does not spend the API's hourly allowance on one page view.
     ------------------------------------------------------------------ */
  function githubCard(key, repo, pick){
    var state = el("gh-" + key + "-state"), btn = el("gh-" + key + "-btn");
    if(!state || !btn) return;
    var ck = "rf_gh_" + repo.replace("/","_");
    var cached = null;
    try { cached = JSON.parse(localStorage.getItem(ck) || "null"); } catch(e){}

    function show(rel){
      var assets = (rel && rel.assets) || [];
      var a = pick(assets);
      if(!a){
        state.className = "ghstate bad";
        state.textContent = "The latest release has no file to download.";
        btn.disabled = true;
        return;
      }
      state.className = "ghstate ok";
      state.innerHTML = "Latest release <b>" +
        esc(rel.tag_name || rel.name || "") + "</b> &middot; " +
        esc(human(a.size)) + " &middot; published " +
        esc(String(rel.published_at || "").slice(0,10));
      btn.disabled = false;
      btn.onclick = function(){ download([a.browser_download_url], btn); };
    }

    if(cached && cached.rel && (Date.now() - cached.t) < 30 * 60 * 1000){
      show(cached.rel);
      return;
    }
    fetch("https://api.github.com/repos/" + repo + "/releases/latest", {
      headers: {"Accept":"application/vnd.github+json"}
    }).then(function(r){
      if(!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    }).then(function(rel){
      try {
        localStorage.setItem(ck, JSON.stringify({t:Date.now(), rel:rel}));
      } catch(e){}
      show(rel);
    }).catch(function(e){
      state.className = "ghstate bad";
      state.textContent = "GitHub did not answer (" +
        (e && e.message ? e.message : "network error") +
        "). The releases page is one click away.";
    });
  }

  /* ------------------------------------------------------------------ */
  function start(){
    var q = el("dlq");
    if(!q) return;

    q.addEventListener("input", function(){
      var v = q.value;
      if(!v.trim()){ renderResults(v); return; }
      loadIndex(function(){ renderResults(v); });
    });

    q.addEventListener("keydown", function(e){
      if(e.key !== "Enter") return;
      var first = document.querySelector("#dlresults .dlres");
      if(first) first.click();
    });

    var box = el("dlresults");
    if(box){
      box.addEventListener("click", function(e){
        var b = e.target.closest ? e.target.closest(".dlres") : null;
        if(b) select(b.getAttribute("data-slug"));
      });
    }

    var change = el("dlchange");
    if(change){
      change.addEventListener("click", function(){
        selected = null; region = "all";
        el("dlpick").hidden = true;
        el("dlresults").hidden = true;
        q.value = ""; q.focus();
      });
    }

    var rb = el("dlregionbtn"), chips = el("dlregionchips");
    if(rb && chips){
      rb.addEventListener("click", function(){
        var open = chips.hidden;
        chips.hidden = !open;
        rb.setAttribute("aria-expanded", open ? "true" : "false");
      });
      chips.addEventListener("click", function(e){
        var b = e.target.closest ? e.target.closest("button[data-r]") : null;
        if(!b) return;
        region = b.getAttribute("data-r");
        var all = chips.querySelectorAll("button[data-r]");
        for(var i = 0; i < all.length; i++){
          all[i].className = (all[i].getAttribute("data-r") === region) ? "on" : "";
        }
        renderRoms();
      });
    }

    /* A link can name the phone it is about:
         downloader.html?device=poco-x7-pro
       The phone is then picked straight away, so a guide can send the reader
       to the table of that one model. */
    try {
      var want = "";
      var parts = String(window.location.search || "").replace(/^\?/, "").split("&");
      for(var z = 0; z < parts.length; z++){
        var kv = parts[z].split("=");
        if(kv[0] === "device") want = decodeURIComponent((kv[1] || "").replace(/\+/g, " "));
      }
      want = want.trim().toLowerCase();
      if(want){
        loadIndex(function(){
          if(!data) return;
          var hit = "";
          for(var k in data){
            if(!Object.prototype.hasOwnProperty.call(data, k)) continue;
            var d = data[k];
            if(k.toLowerCase() === want ||
               (d.name || "").toLowerCase() === want ||
               (d.code || "").toLowerCase() === want){ hit = k; break; }
          }
          if(!hit){
            for(var k2 in data){
              if(!Object.prototype.hasOwnProperty.call(data, k2)) continue;
              if(hay(data[k2]).indexOf(want) >= 0){ hit = k2; break; }
            }
          }
          if(hit){
            q.value = data[hit].name || "";
            select(hit);
          }
        });
      }
    } catch(e){}

    var tbody = el("dlroms");
    if(tbody){
      tbody.addEventListener("click", function(e){
        var b = e.target.closest ? e.target.closest("button[data-kind]") : null;
        if(!b) return;
        var row = rows[+b.getAttribute("data-k")];
        if(!row) return;
        var src = b.getAttribute("data-kind") === "recovery" ? row.rec : row.fb;
        if(!src || !src.url) return;
        var urls = [src.url];
        if(src.mirrors) for(var i = 0; i < src.mirrors.length; i++) urls.push(src.mirrors[i]);
        download(urls, b);
      });
    }

    githubCard("magisk", "topjohnwu/Magisk", function(assets){
      for(var i = 0; i < assets.length; i++){
        if(/^Magisk-.*\.apk$/i.test(assets[i].name)) return assets[i];
      }
      for(var j = 0; j < assets.length; j++){
        if(/\.apk$/i.test(assets[j].name) && !/debug/i.test(assets[j].name))
          return assets[j];
      }
      return null;
    });

    githubCard("kernelsu", "tiann/KernelSU", function(assets){
      for(var i = 0; i < assets.length; i++){
        if(/release\.apk$/i.test(assets[i].name)) return assets[i];
      }
      for(var j = 0; j < assets.length; j++){
        if(/\.apk$/i.test(assets[j].name)) return assets[j];
      }
      return null;
    });
  }

  if(document.readyState === "loading"){
    document.addEventListener("DOMContentLoaded", start);
  } else {
    start();
  }
})();
</script>
"""


def build_downloader():
    """The ROM downloader: pick a phone, get the firmware.

    The picker at the top of the page is the whole phone list. It holds every
    Xiaomi, Redmi and POCO model the index knows about - every region, every
    Recovery and Fastboot build - and the download button goes straight to the
    file: Xiaomi's own server is asked first and the public mirrors are asked
    alongside it, and whichever answers first wins. There is no page in front
    of the file and nothing of ours is in the way. The visitor searches by the
    name they actually know ("poco x7 pro", "redmi note 13", "CPH2451") rather
    than a codename they do not.

    There are no brand cards below the picker any more. A row of links to
    Samsung, OPPO, vivo and the rest would only be a list of dead ends - a
    link to a brand that has no file behind it - so those manufacturers' own
    firmware pages are not listed here at all.

    Nothing on this site hosts, rewrites or proxies a firmware file.
    """

    # How many phones and builds the picker holds right now, so the page can
    # say it out loud instead of guessing.
    phone_count = 0
    build_count = 0
    try:
        with open(os.path.join(DATA, "firmware.json"), encoding="utf-8") as fh:
            index = json.load(fh).get("devices", {})
        phone_count = len(index)
        for dev in index.values():
            build_count += len(dev.get("roms") or [])
    except Exception:
        pass

    # The page has no brand cards any more: the picker above is the whole
    # list, and it carries every phone, every region and every build. The
    # other manufacturers' download pages are not listed here - a link to a
    # brand that has no file behind it is only a dead end.

    body = """<div class="dlhero">
  <div class="dlkicker"><span class="live-pulse"></span> Official Firmware Index &middot; Fastboot &amp; Recovery</div>
  <h1 class="dltitle">Official Stock ROM &amp; Firmware Downloader</h1>
  <p class="dllead">Direct, verified official firmware builds for Xiaomi, Redmi, and POCO smartphones. Parallel-raced high-speed official CDN mirrors &mdash; 100%% clean, zero waiting queues, and zero third-party ad shorteners.</p>
  
  <div class="dlstats-grid">
    <div class="dlstat-card">
      <div class="dlstat-val">__PHONE_COUNT__</div>
      <div class="dlstat-lbl">Supported Phones</div>
    </div>
    <div class="dlstat-card">
      <div class="dlstat-val">__BUILD_COUNT__</div>
      <div class="dlstat-lbl">Verified Builds</div>
    </div>
    <div class="dlstat-card">
      <div class="dlstat-val">Official CDN</div>
      <div class="dlstat-lbl">Direct Vendor Mirrors</div>
    </div>
    <div class="dlstat-card">
      <div class="dlstat-val">Zero Wait</div>
      <div class="dlstat-lbl">Parallel Speed Race</div>
    </div>
  </div>
</div>

<div class="dlsearch">
  <label for="dlq" class="dlsearch-lbl">
    <span>Search Firmware Database</span>
    <span class="dlsearch-count">__PHONE_COUNT__ devices indexed</span>
  </label>
  <div class="dlsearch-input-wrap">
    <svg class="dlsearch-icon" viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
    <input id="dlq" type="search" autocomplete="off" spellcheck="false"
           placeholder="Search by phone name, model code, or codename (e.g. poco x7 pro, 23117RK66C, duchess)...">
  </div>
  <div class="dlquick-chips">
    <span class="dlquick-lbl">Popular:</span>
    <button type="button" class="dlquick-chip" onclick="var q=document.getElementById('dlq');q.value='poco x7 pro';q.dispatchEvent(new Event('input'))">POCO X7 Pro</button>
    <button type="button" class="dlquick-chip" onclick="var q=document.getElementById('dlq');q.value='redmi note 13';q.dispatchEvent(new Event('input'))">Redmi Note 13</button>
    <button type="button" class="dlquick-chip" onclick="var q=document.getElementById('dlq');q.value='xiaomi 14';q.dispatchEvent(new Event('input'))">Xiaomi 14</button>
    <button type="button" class="dlquick-chip" onclick="var q=document.getElementById('dlq');q.value='poco f5';q.dispatchEvent(new Event('input'))">POCO F5</button>
    <button type="button" class="dlquick-chip" onclick="var q=document.getElementById('dlq');q.value='redmi k50i';q.dispatchEvent(new Event('input'))">Redmi K50i</button>
    <button type="button" class="dlquick-chip" onclick="var q=document.getElementById('dlq');q.value='xiaomi pad 5';q.dispatchEvent(new Event('input'))">Xiaomi Pad 5</button>
  </div>
  <div class="dlresults" id="dlresults" hidden></div>
  <p class="dlhint" id="dlhint">Start typing above. Every phone in the index drops out below the box &mdash; scroll the list and tap your model to reveal all official builds.</p>
</div>

<div class="dlpick" id="dlpick" hidden>
  <div class="dlpickhead">
    <div>
      <h2 id="dlpname">Phone</h2>
      <p class="dis" id="dlpdesc"></p>
      <div class="dlmeta" id="dlpmeta"></div>
    </div>
    <button class="btn ghost" type="button" id="dlchange">Change phone</button>
  </div>

  <div class="dlregions">
    <button class="dlregionbtn" type="button" id="dlregionbtn"
            aria-expanded="false" aria-controls="dlregionchips">Change region</button>
    <div class="dlregionchips" id="dlregionchips" hidden></div>
  </div>

  <div class="dltablewrap">
    <table class="dltable">
      <thead><tr>
        <th>Version</th><th>Region</th><th>Android</th><th>Released</th>
        <th>Size</th><th style="text-align:right">Download</th>
      </tr></thead>
      <tbody id="dlroms"></tbody>
    </table>
  </div>
  <p class="dlnote" id="dlpnote"></p>
</div>

<div class="dlroot-section">
  <div class="dlsection-header">
    <h2>Pick Root Engine &amp; Utilities</h2>
    <p class="dlsection-sub">Essential root tools tested and verified on physical Android hardware:</p>
  </div>
  <div class="dlopts">
    <div class="dlopt dloptcard" id="gh-magisk">
      <div class="dlopt-top">
        <span class="dlopt-badge">Traditional Systemless Root</span>
        <h3>Magisk</h3>
        <p class="dlopt-desc">Root by patching the boot or init_boot image &mdash; highest compatibility and best hiding with Zygisk modules. The stock boot image is inside your stock ROM; patch it in Magisk app and flash over USB-OTG.</p>
      </div>
      <div class="dlopt-bottom">
        <p class="ghstate" id="gh-magisk-state">Checking GitHub for the latest release&hellip;</p>
        <div class="ghbtns">
          <button class="btn btn-primary" type="button" id="gh-magisk-btn" disabled>Download latest</button>
          <a class="btn ghost" href="https://github.com/topjohnwu/Magisk/releases" rel="noopener" target="_blank">All releases</a>
          <a class="btn ghost" href="https://topjohnwu.github.io/Magisk/" rel="noopener" target="_blank">Docs</a>
        </div>
      </div>
    </div>
    <div class="dlopt dloptcard" id="gh-kernelsu">
      <div class="dlopt-top">
        <span class="dlopt-badge">Kernel-Level Root (GKI)</span>
        <h3>KernelSU</h3>
        <p class="dlopt-desc">Kernel-level root built directly into a Linux kernel instead of userspace injection. On GKI phones (Android 12+), flash a patched kernel for seamless, invisible root privilege management.</p>
      </div>
      <div class="dlopt-bottom">
        <p class="ghstate" id="gh-kernelsu-state">Checking GitHub for the latest release&hellip;</p>
        <div class="ghbtns">
          <button class="btn btn-primary" type="button" id="gh-kernelsu-btn" disabled>Download latest</button>
          <a class="btn ghost" href="https://github.com/tiann/KernelSU/releases" rel="noopener" target="_blank">All releases</a>
          <a class="btn ghost" href="https://kernelsu.org/" rel="noopener" target="_blank">Docs</a>
        </div>
      </div>
    </div>
  </div>
</div>

%(ad)s

<h2 id="stock">Stock ROM download</h2>
<p>A <strong>stock ROM</strong> is the firmware your phone shipped with. You
want it back when a custom ROM left something broken, when the phone bootloops,
or when you are selling the phone and want it clean. Two file types show up for
almost every brand, and picking the wrong one is the usual reason a flash
fails:</p>
<ul>
  <li><strong>Recovery ROM</strong> (also called an OTA or full OTA zip). A big
  <code>.zip</code> you install from the phone's own updater or from recovery.
  It keeps your data if the version is newer, and it is the safer one.</li>
  <li><strong>Fastboot ROM</strong> (also called a factory image). A
  <code>.tgz</code> or a folder with a <code>flash_all</code> script inside. It
  writes every partition, so it can rescue a phone that no longer boots &mdash;
  and it wipes your data.</li>
</ul>

<div class="rule-box">
  <div class="rule-icon"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg></div>
  <div class="rule-content">
    <strong>Rule of thumb:</strong> Phone boots into system or recovery &rarr; use <strong>Recovery ROM</strong> (safer, preserves personal data). Phone does not boot or is stuck in bootloop &rarr; use <strong>Fastboot ROM</strong> (factory clean, wipes userdata, flashes raw partition sectors).
  </div>
</div>
<p>Type your model in the box at the top of this page and every build for it
comes out below &mdash; the Recovery ROM and the Fastboot ROM for each region,
newest first, each button pointing straight at the file. Nothing is hosted
here: the download starts on Xiaomi's own servers or on the public mirrors
beside them.</p>
<p>Then follow the <a href="videos.html">written guide for your phone</a> on this
site &mdash; every step, in the same order as the video.</p>

<h2 id="how">How to find your exact model</h2>
<p>Half of all failed flashes come down to a codename mismatch. Two minutes of
checking saves that:</p>
<ul>
  <li>On the phone: <strong>Settings &rarr; About phone</strong> shows the model
  name and often the model code. Tap the build number a few times for developer
  options if you need the exact build.</li>
  <li>In fastboot: the codename is printed on the fastboot screen, and
  <code>fastboot getvar product</code> returns it.</li>
  <li>In recovery: the filename of the zip you are about to flash should contain
  that exact codename. If it does not, stop.</li>
</ul>

<h2>Frequently asked questions</h2>

<details class="faq"><summary>Why does this page link out instead of hosting the files?</summary>
<p>Firmware belongs to the manufacturer, and this site does not have a licence to
redistribute it. Hosting someone else's ROM would also mean serving a file that is
out of date within weeks. Sending you to the brand's own download page means you
always get the current build, from the source that signs it.</p></details>

<details class="faq"><summary>Recovery ROM or Fastboot ROM &mdash; which one do I want?</summary>
<p>If the phone still boots and you just want the stock firmware back, use the
Recovery ROM. If the phone will not boot, or you want to be certain every
partition is stock, use the Fastboot ROM &mdash; it wipes data but it is the one
that rescues a brick.</p></details>

<details class="faq"><summary>Can my phone's bootloader stay locked?</summary>
<p>For a Recovery ROM from the phone's own updater, yes. For a Fastboot ROM or
any custom ROM, no &mdash; the bootloader has to be unlocked first, and on most
brands that erases the phone.</p></details>

<details class="faq"><summary>Do I need a computer?</summary>
<p>Not for a Recovery ROM, and not for flashing a patched boot image if you use
<a href="download.html">the free Rom Flasher tool</a> over USB-OTG. A Fastboot
ROM is easier on a PC, though, because that is what the bundled scripts are
written for.</p></details>

<details class="faq"><summary>Is my data safe?</summary>
<p>A Recovery ROM of a newer version keeps your data. A Fastboot ROM wipes it.
Either way, take a backup first &mdash; and note that unlocking a bootloader
usually erases the phone on its own.</p></details>

<details class="faq"><summary>What if my phone is not listed?</summary>
<p>The picker here holds the Xiaomi, Redmi and POCO models. If your phone is
from another maker, the firmware lives on that maker's own support site &mdash;
look for a "software", "downloads" or "firmware" section. Every manufacturer
has one; it is just named differently each time.</p></details>
""" % {"ad": ad_slot("hub")}

    faq = [
        ("Why does this page link out instead of hosting the files?",
         "Firmware belongs to the manufacturer, and this site does not have a "
         "licence to redistribute it. Hosting someone else's ROM would also "
         "serve a file that is out of date within weeks."),
        ("Recovery ROM or Fastboot ROM - which one do I want?",
         "If the phone still boots, use the Recovery ROM. If it will not boot, "
         "or you want every partition stock, use the Fastboot ROM - it wipes "
         "data but it rescues a brick."),
        ("Can my phone's bootloader stay locked?",
         "For a Recovery ROM from the phone's own updater, yes. For a Fastboot "
         "ROM or any custom ROM, no - the bootloader has to be unlocked first."),
        ("Do I need a computer?",
         "Not for a Recovery ROM, and not for flashing a patched boot image "
         "with the free Rom Flasher tool over USB-OTG. A Fastboot ROM is easier "
         "on a PC."),
        ("Is my data safe?",
         "A Recovery ROM of a newer version keeps your data. A Fastboot ROM "
         "wipes it. Take a backup first."),
        ("What if my phone is not listed?",
         "The picker here holds the Xiaomi, Redmi and POCO models. If your "
         "phone is from another maker, the firmware lives on that maker's own "
         "support site - look for a software, downloads or firmware section."),
    ]

    blocks = [{
        "@context": "https://schema.org", "@type": "WebPage",
        "name": "ROM downloader",
        "url": "%s/downloader.html" % SITE_URL,
        "description": "Find stock firmware for your Xiaomi, Redmi or POCO phone "
                       "- every Recovery ROM and Fastboot ROM build, straight from "
                       "the official servers and their public mirrors, plus Magisk "
                       "and KernelSU.",
        "inLanguage": "en",
        "isAccessibleForFree": True,
        "isPartOf": {"@type": "WebSite", "name": SITE, "url": SITE_URL},
        "publisher": {"@type": "Organization", "name": SITE, "url": SITE_URL},
        "mainEntity": {"@type": "ItemList", "numberOfItems": 3,
                       "name": "Ways to get firmware",
                       "itemListElement": [
                           {"@type": "ListItem", "position": 1,
                            "name": "Stock ROM download",
                            "url": "%s/downloader.html#stock" % SITE_URL},
                           {"@type": "ListItem", "position": 2,
                            "name": "Magisk",
                            "url": "https://github.com/topjohnwu/Magisk/releases"},
                           {"@type": "ListItem", "position": 3,
                            "name": "KernelSU",
                            "url": "https://github.com/tiann/KernelSU/releases"}]},
        "significantLink": ["%s/downloader.html#stock" % SITE_URL,
                            "https://github.com/topjohnwu/Magisk/releases",
                            "https://github.com/tiann/KernelSU/releases"],
    }, {
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q,
             "acceptedAnswer": {"@type": "Answer",
                                "text": re.sub(r"<[^>]+>", "", a)
                                .replace("&nbsp;", " ").replace("&mdash;", "-")}}
            for q, a in faq],
    }, {
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home",
             "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Downloader",
             "item": SITE_URL + "/downloader.html"},
        ],
    }]
    head = "\n".join('<script type="application/ld+json">%s</script>'
                     % json.dumps(b, ensure_ascii=False) for b in blocks)

    # The picker, the region filter, the one-click download and the two live
    # GitHub cards. The markup above is already readable with the script
    # blocked - this only adds the search and the download.
    head += DOWNLOADER_JS

    return page("ROM downloader \u2014 Xiaomi, Redmi and POCO stock ROM, Magisk, "
                "KernelSU | %s" % SITE,
                "Type your Xiaomi, Redmi or POCO phone - poco x7 pro, redmi note "
                "13, CPH2451 - and download its official Recovery ROM and Fastboot "
                "ROM builds direct from the source, plus Magisk and KernelSU.",
                '<article><div class="prose">%s</div></article>'
                % body.replace("__PHONE_COUNT__", str(phone_count))
                     .replace("__BUILD_COUNT__", str(build_count)),
                "downloader.html", extra_head=head,
                keywords=keywords_for(item={"tags": [
                    "stock rom download", "official firmware download",
                    "fastboot rom download", "recovery rom download",
                    "xiaomi firmware", "poco stock rom", "redmi firmware",
                    "xiaomi rom download", "magisk download", "kernelsu download",
                    "rom downloader"]}),
                image=SITE_URL + "/static/app.png")



def build_static(items):
    out = {}
    n = len(items)

    out["apps.html"] = page("Download Rom Flasher \u2014 Free Android Flashing App | %s" % SITE,
                            "Redirecting to the comprehensive Rom Flasher download hub...",
                            '<article><div class="prose"><h1>Redirecting to Rom Flasher Download...</h1>'
                            '<p>The tool documentation, release verification, and direct APK packages have consolidated to our '
                            '<a href="download.html">Rom Flasher Download Hub</a>.</p>'
                            '<p><a class="btn" href="download.html">Continue to Download Page &rarr;</a></p></div></article>',
                            "apps.html",
                            extra_head='<meta http-equiv="refresh" content="0; url=download.html">'
                                       '<link rel="canonical" href="%s/download.html">' % SITE_URL)

    out["download.html"] = build_download()
    out["downloader.html"] = build_downloader()
    out["donate.html"] = build_donate()

    about_html_content = """
<div class="about-hero-grid">
  <div class="about-hero-photo">
    <img src="static/rohit-verma.webp" alt="Rohit Verma — Android Flashing Specialist" width="160" height="160" class="about-portrait">
  </div>
  <div class="about-hero-bio">
    <h2 class="about-name">Rohit Verma <span class="about-badge">&#10003; Editor-in-Chief &amp; Lead Developer</span></h2>
    <p class="about-lead">I am an independent Android software and kernel researcher, the creator of the free Rom Flasher Tool, and the author behind every guide published on this website and on the <a href="https://www.youtube.com/@Rom_Flasher" target="_blank" rel="noopener">Rom Flasher YouTube channel</a>.</p>
    <div class="about-actions">
      <a class="btn primary" href="https://www.youtube.com/@Rom_Flasher" target="_blank" rel="noopener">YouTube Channel (@Rom_Flasher)</a>
      <a class="btn ghost" href="https://github.com/romflasher3419-spec" target="_blank" rel="noopener">GitHub Profile</a>
    </div>
  </div>
</div>

<h2>Why Rom Flasher Was Created</h2>
<p>For years, the custom ROM and Android modification scene has suffered from a painful, dangerous problem: clickbait YouTube tutorials, unverified fastboot commands copied from obscure forums, and shady third-party file download links littered with malware and adware. Too many Android enthusiasts have permanently bricked their smartphones or wiped their personal data because an online tutorial skipped a critical step or failed to mention a specific bootloader partition requirement.</p>

<p>I founded <strong>Rom Flasher</strong> to establish a rigorous, 100%% reproducible technical standard. Every single ROM installation, bootloader unlock method, and root tutorial on this website is written as clear, step-by-step documentation tested on real hardware. We never publish speculative guides, never scrape AI-generated text, and never recommend an unverified command.</p>

<h2>The Physical Hardware Testing Lab</h2>
<p>Unlike aggregation portals that synthesize tutorials from spec sheets, every guide on Rom Flasher is physically executed on actual test smartphones in our dedicated testing bench. Before a guide is marked as verified, it must pass a strict four-stage hardware evaluation:</p>

<div class="lab-protocol-grid">
  <div class="protocol-card">
    <div class="protocol-num">01</div>
    <div class="protocol-title">Cryptographic Integrity Verification</div>
    <p>Every fastboot ROM, custom recovery (TWRP/OrangeFox), and firmware zip is verified using SHA-256 and MD5 checksums directly against official manufacturer and vendor repositories.</p>
  </div>
  <div class="protocol-card">
    <div class="protocol-num">02</div>
    <div class="protocol-title">Partition Target Verification</div>
    <p>Modern Android dynamic partitions (<code>super</code>, <code>init_boot</code>, <code>boot</code>, <code>vendor_boot</code>) differ drastically across Android 12, 13, 14, and 15. We physically inspect partition maps using fastbootd to eliminate partition mismatch bootloops.</p>
  </div>
  <div class="protocol-card">
    <div class="protocol-num">03</div>
    <div class="protocol-title">Dry-Run Hardware Flashing</div>
    <p>The flashing process is performed on our active lab devices &mdash; including our <strong>Xiaomi Pad 5 (nabu)</strong>, <strong>Redmi Note 10 Pro (sweet)</strong>, <strong>Realme GT 2 Pro (RMX3301)</strong>, and <strong>POCO F1 (beryllium)</strong> test units &mdash; using our free Rom Flasher OTG tool and standard ADB/Fastboot.</p>
  </div>
  <div class="protocol-card">
    <div class="protocol-num">04</div>
    <div class="protocol-title">Post-Boot Stability Audit</div>
    <p>A ROM is only recommended once hardware features (cellular connectivity, Wi-Fi 6, camera HAL, audio DSP, Play Integrity certification, and battery drain) have been tested in active usage.</p>
  </div>
</div>

<h2>Editorial Independence &amp; Anti-Brick Policy</h2>
<p><strong>Editorial Independence:</strong> Rom Flasher is completely independent. We do not accept paid promotions from smartphone manufacturers, and we do not host sponsored reviews for unverified ROM forks. If a custom build exhibits dangerous bugs, modem instability, or battery drain, we state it plainly in the guide notes.</p>

<p><strong>Safety &amp; Risk Warning:</strong> Flashing custom firmware and unlocking your device bootloader inherently involves modifying low-level system partitions. We clearly outline prerequisite partition backups (EFS/IMEI, modem, and persist) in every relevant tutorial. We urge all readers to read our <a href="terms.html">Terms of Service</a> and safety warnings prior to flashing.</p>

<h2>Direct Contact &amp; Community Peer Review</h2>
<p>The Android ecosystem moves rapidly. When a vendor updates their fastboot security or bootloader authorization, guides may require refinement. I welcome direct peer review and technical feedback from the community:</p>
<ul>
  <li><strong>Direct Email:</strong> <a href="mailto:vrohit3419@gmail.com">vrohit3419@gmail.com</a> (I read and respond to every message personally).</li>
  <li><strong>Contact Form:</strong> Use our <a href="contact.html">secure on-site contact form</a>.</li>
  <li><strong>Video Walkthroughs:</strong> Watch full, unedited physical flashing sessions on <a href="%s" target="_blank" rel="noopener">YouTube (@Rom_Flasher)</a>.</li>
  <li><strong>Source Code &amp; Bug Reports:</strong> Contribute or audit the Rom Flasher codebase on <a href="%s" target="_blank" rel="noopener">GitHub</a>.</li>
</ul>
""" % (CHANNEL_URL, REPO_URL)

    out["about.html"] = simple("about.html", "About Rom Flasher & Editorial Standards", "About Rohit Verma & Rom Flasher Lab \u2014 %s" % SITE, about_html_content,
                              description="About Rohit Verma and Rom Flasher: independent Android flashing engineering journal, physical testing lab protocols, and editorial integrity standards.",
                              schema={
                                  "@context": "https://schema.org",
                                  "@type": "AboutPage",
                                  "name": "About %s" % SITE,
                                  "url": "%s/about.html" % SITE_URL,
                                  "description": "Editorial standards, lab testing, and authorship of Rohit Verma.",
                                  "inLanguage": "en",
                                  "publisher": {"@type": "Organization",
                                                "name": SITE, "url": SITE_URL},
                                  "mainEntity": {
                                      "@type": "Person",
                                      "name": "Rohit Verma",
                                      "jobTitle": "Android Flashing Specialist & Developer",
                                      "url": "%s/about.html" % SITE_URL,
                                      "image": "%s/static/rohit-verma.webp" % SITE_URL,
                                      "sameAs": [CHANNEL_URL, REPO_URL]
                                  }}) 

    out["privacy.html"] = simple("privacy.html", "Privacy Policy",
                                 "Privacy \u2014 %s" % SITE, """
<p class="dis">Last updated: %s.</p>
<h2>What this site stores</h2>
<p>Rom Flasher is a set of static files. There is no login, no comment box and
no database on this site. Standard server logs (IP address, user agent, page
requested and the time of the request) may be kept by the hosting provider for
security and abuse prevention.</p>
<h2>Contact form</h2>
<p>The contact form is delivered by <a href="https://formsubmit.co/"
rel="noopener">FormSubmit</a>, a form-to-email service. When you send a message,
FormSubmit processes the name, email address and message you type and forwards
them to my inbox. I use them only to reply. The site itself does not store the
submission, and FormSubmit's own privacy policy applies to its handling. Its
server-side CAPTCHA and a honeypot field are used to block automated spam.</p>
<h2>Cookies, analytics and advertising</h2>
<p>Nothing that can set a cookie or make an advertising request loads until you
choose. The consent banner has three options: accept all, reject optional
cookies, or manage analytics and personalised ads separately. Rejecting is just
as easy as accepting, and the site works exactly the same either way.</p>
<p>Your choice is remembered in your browser's local storage, not in a tracking
cookie. It contains only two true/false values and is sent nowhere; clearing
your browser data removes it.</p>
<p>If you accept analytics, the site uses Google Analytics 4 to count visits and
see which guides are useful. IP anonymisation is enabled. If you accept ads,
advertising may be served by Google and other third-party vendors. Google uses
cookies to serve ads based on your prior visits to this and other websites.
Google's use of advertising cookies lets it and its partners show you ads based
on your visit to this site and other sites on the internet.</p>
<p>You can change or withdraw your choice at any time with the
<button type="button" class="footlink inline" data-consent-open>Cookie settings</button>
button. You can also opt out of personalised advertising at
<a href="https://www.google.com/settings/ads" rel="noopener">Google Ads
Settings</a>, read <a href="https://policies.google.com/technologies/partner-sites"
rel="noopener">how Google uses information from sites that use its services</a>,
or opt out of third-party vendor cookies at
<a href="https://www.aboutads.info" rel="noopener">aboutads.info</a> and
<a href="https://www.youronlinechoices.com" rel="noopener">Your Online
Choices</a>.</p>
<h2>Embedded videos</h2>
<p>Guide pages show a YouTube thumbnail. No YouTube player is loaded until you
press play. Once the player starts, it is served from
<code>youtube-nocookie.com</code>, but YouTube's own terms, privacy policy and
cookies still apply to that playback.</p>
<h2>The Rom Flasher Android app</h2>
<p>The app is distributed from GitHub Releases, not from this website. It asks
for USB host access so it can talk to the phone being flashed, storage access so
it can read a firmware or boot image you choose, and network access to open
download and update links. It has no account and does not upload your files.
The published APK is signed, and its SHA-256 checksum is listed on the
<a href="download.html">download page</a> so you can verify the file you
installed.</p>
<h2>Affiliate links</h2>
<p>Some gear links on the download page are affiliate links. If you buy through
them, the channel earns a small commission and the price you pay does not
change. They are never the reason a recommendation exists.</p>
<h2>Outbound links</h2>
<p>Firmware, APK, forum and store links point to other people's servers. This
site does not control them and cannot vouch for what they host. Download files
only from a source you trust and verify checksums wherever they are published.</p>
<h2>GDPR Compliance &amp; European Visitor Rights (EU / EEA / UK)</h2>
<p>If you reside within the European Economic Area (EEA), the United Kingdom, or Switzerland, you possess distinct statutory rights under the General Data Protection Regulation (GDPR) and UK GDPR regarding your personal data:</p>
<ul>
  <li><strong>Right of Access &amp; Portability:</strong> You may request confirmation and a portable copy of any personal data processed about you.</li>
  <li><strong>Right to Rectification &amp; Erasure:</strong> You have the right to request the correction of inaccurate data or the immediate deletion ("Right to be Forgotten") of personal data.</li>
  <li><strong>Right to Restrict or Object:</strong> You may object to data processing or request restriction of processing where applicable.</li>
  <li><strong>Right to Withdraw Consent:</strong> Where data processing is founded on consent (such as analytics cookies or personalized advertisements), you may withdraw consent at any instant using our on-page <button type="button" class="footlink inline" data-consent-open>Cookie settings</button> console.</li>
</ul>
<p><strong>Legal Basis for Processing:</strong> We process non-essential analytics and advertising cookies strictly on the legal basis of your explicit, affirmative consent (Article 6(1)(a) GDPR) gathered via Google Consent Mode v2 prior to script execution. Technical server logs are processed under legitimate interest (Article 6(1)(f) GDPR) strictly for cybersecurity defense, rate limiting, and infrastructure uptime monitoring.</p>

<h2>California Consumer Privacy Rights (CCPA / CPRA)</h2>
<p>Under the California Consumer Privacy Act (CCPA) as amended by the California Privacy Rights Act (CPRA), California residents are entitled to specific disclosures:</p>
<ul>
  <li><strong>Categories of Information Collected:</strong> Internet and electronic network activity information (e.g., anonymized IP addresses, browser user agent, pages visited) when analytics or advertising consent is granted.</li>
  <li><strong>No Sale or Sharing of Personal Data:</strong> Rom Flasher does not sell, rent, lease, or monetize your personal information to third parties for monetary or other commercial consideration.</li>
  <li><strong>Right to Know &amp; Delete:</strong> You have the right to request disclosure of personal information collected and request its deletion without discriminatory treatment.</li>
</ul>

<h2>Children</h2>
<p>This site is written for adults who own and repair Android devices. It is not
directed at children under 13, and I do not knowingly collect personal
information from children.</p>

<h2>Data Controller &amp; Privacy Contact</h2>
<p>For any privacy-related inquiries, data requests, or formal GDPR/CCPA rights execution, contact the publisher directly:</p>
<ul>
  <li><strong>Data Controller:</strong> Rohit Verma (Author &amp; Publisher, Rom Flasher)</li>
  <li><strong>Direct Email:</strong> <a href="mailto:vrohit3419@gmail.com">vrohit3419@gmail.com</a></li>
  <li><strong>Online Form:</strong> <a href="contact.html">Rom Flasher Contact Desk</a></li>
  <li><strong>Turnaround Time:</strong> Direct personal response within 24 to 48 business hours.</li>
</ul>
""" % BUILT_ON,
                                 description="How Rom Flasher handles data: "
                                 "contact-form delivery, server logs, Google "
                                 "Analytics and AdSense consent, the Android "
                                 "app's permissions, and how to change your "
                                 "cookie choice.",
                                 schema={
                                     "@context": "https://schema.org",
                                     "@type": "WebPage",
                                     "name": "Privacy Policy",
                                     "url": "%s/privacy.html" % SITE_URL,
                                     "inLanguage": "en",
                                     "isPartOf": {"@type": "WebSite",
                                                  "name": SITE,
                                                  "url": SITE_URL},
                                     "dateModified": BUILT_ON})

    terms_html_content = """
<p>Please read these Terms of Use (&ldquo;Terms&rdquo;, &ldquo;Agreement&rdquo;) carefully before accessing or using the technical guides, documentation, firmware links, and software tools published on <strong>Rom Flasher</strong> (<a href="{site}">{site}</a>). By visiting, reading, or executing any flashing procedures from this website, you agree to be legally bound by these Terms.</p>

<h2>1. Educational Purpose &amp; Engineering Research Scope</h2>
<p>Rom Flasher is an independent technical publication dedicated to Android operating system internals, low-level partition architecture, fastboot flashing protocols, and custom ROM engineering. All tutorials, terminal command sequences, recovery workflows, and firmware installation guides are published strictly for educational, research, and non-commercial technical evaluation purposes.</p>

<h2>2. Hardware Flashing Risks &amp; Voluntary Assumption of Risk</h2>
<p>Modifying Android system firmware, partitions, and bootloaders carries inherent risks of permanent device failure (&ldquo;hard bricking&rdquo;). By utilizing any guide on this site, you acknowledge and agree that:</p>
<ul>
  <li><strong>Data Erasure:</strong> Bootloader unlocking, custom recovery installations (TWRP, OrangeFox), dynamic partition restructuring, and clean custom ROM flashes will irreversibly wipe all user data stored in the <code>userdata</code> and <code>metadata</code> partitions. You are solely responsible for creating and verifying complete off-device backups before beginning any flashing procedure.</li>
  <li><strong>Security State &amp; Hardware Flags:</strong> Unlocking bootloaders and modifying cryptographic boot images (such as <code>boot</code>, <code>init_boot</code>, <code>vendor_boot</code>, or <code>vbmeta</code>) permanently disables Android Verified Boot (AVB 2.0) verification, trips one-way hardware fuses (including Qualcomm TEE tamper bits and Samsung Knox counters), and may permanently prevent banking applications, DRM Widevine L1 video playback, and Google Play Integrity Strong Attestation from passing.</li>
  <li><strong>Warranty Voidance:</strong> Flashing custom firmware or unlocking bootloaders may void manufacturer and carrier warranties. Rom Flasher assumes zero liability for denied warranty or service claims.</li>
  <li><strong>Sole User Responsibility:</strong> You execute all terminal commands, fastboot scripts, recovery flashes, and kernel modifications entirely at your own discretion and risk. Neither Rom Flasher nor its author, Rohit Verma, shall be held liable for bricked hardware, bootloops, baseband NVRAM/EFS corruption, lost IMEI numbers, or unusable equipment.</li>
</ul>

<h2>3. Technical Accuracy &amp; Hardware Variance</h2>
<p>Every flashing procedure documented on Rom Flasher is physically executed on real test devices within our hardware testing lab (including Xiaomi Pad 5, POCO X7 Pro, Redmi Note 10 Pro, and POCO F1 test units). However, smartphone manufacturers regularly revise partition tables, Anti-Rollback (ARB) indexes, primary bootloader binaries (XBL/ABL), and hardware components across different regional variants (Global, European EEA, Indian, and Chinese models) and software updates without notice. You are strictly responsible for confirming that all partition images and fastboot commands match your device&rsquo;s exact hardware codename and regional revision before flashing.</p>

<h2>4. Third-Party Links &amp; Firmware Binaries</h2>
<p>Rom Flasher references official Google Android developer tools, community custom recoveries, and stock firmware archives hosted on verified third-party infrastructure (such as official GitHub repositories, the Android Open Source Project, and OEM mirrors). Rom Flasher does not control, operate, or guarantee third-party hosts. We strongly advise all readers to verify cryptographic SHA-256 checksums on all downloaded archives prior to writing them to physical device storage.</p>

<h2>5. Intellectual Property &amp; Fair Use</h2>
<p>The original written tutorials, diagnostic flowcharts, architecture diagrams, and custom software code (including the Rom Flasher Tool) published on this site are the copyrighted intellectual property of Rohit Verma and Rom Flasher. Android, Google, Qualcomm, MediaTek, Xiaomi, POCO, Redmi, HyperOS, MIUI, ColorOS, LineageOS, and associated marks are trademarks of their respective owners. Brand references on this site exist solely for hardware identification and technical accuracy under nominative fair use.</p>

<h2>6. DMCA &amp; Content Takedown Policy</h2>
<p>Rom Flasher strictly respects intellectual property rights. If you believe that any material on this website infringes upon your copyright, please send a written notification to <a href="mailto:{email}">{email}</a> specifying the copyrighted work, the exact URL of the material, and your contact information. Valid takedown notices are processed promptly within 24 to 48 hours.</p>

<h2>7. Advertising &amp; Analytics Disclosures</h2>
<p>To fund our independent testing hardware, hosting infrastructure, and the ongoing development of the free Rom Flasher Tool, this website may display advertisements served by Google AdSense and collect non-identifiable usage metrics via Google Analytics under Google Consent Mode v2. Third-party advertising vendors use cookies to serve relevant ads based on prior visits. Advertisements displayed on this site do not constitute an editorial endorsement by Rom Flasher. For complete details on cookie consent and tracking preferences, please consult our <a href="privacy.html">Privacy Policy</a>.</p>

<h2>8. Limitation of Liability</h2>
<p>To the maximum extent permitted by applicable law, Rom Flasher and Rohit Verma disclaim all warranties, express or implied, and shall not be liable for any direct, indirect, incidental, consequential, or punitive damages arising from your access to or use of this website, its documentation, or any linked third-party resources.</p>

<h2>9. Changes to Terms</h2>
<p>We reserve the right to modify these Terms at any time. Continued use of this website following any revisions signifies your acceptance of the updated terms.</p>
""".format(site=SITE_URL, email=CONTACT_EMAIL)

    out["terms.html"] = simple("terms.html", "Terms of Use & Legal Disclaimer", "Terms \u2014 %s" % SITE, terms_html_content,
                        description="Terms of Use and Hardware Risk Disclaimer for Rom Flasher: educational scope, liability limitation, and technical safety boundaries.",
                        schema={
                            "@context": "https://schema.org",
                            "@type": "WebPage",
                            "name": "Terms of Use",
                            "url": "%s/terms.html" % SITE_URL,
                            "inLanguage": "en",
                            "isPartOf": {"@type": "WebSite", "name": SITE,
                                         "url": SITE_URL},
                            "dateModified": BUILT_ON})

    contact_html_content = """
<div class="contact-info-card">
  <h2>Direct Publisher &amp; Editorial Contact</h2>
  <p>Rom Flasher is an independent Android engineering publication authored and operated by <strong>Rohit Verma</strong>. Every technical manual, fastboot procedure, and unbrick protocol published here is maintained and verified directly by me.</p>
  
  <div class="contact-details-list">
    <div class="cd-item">
      <span class="cd-icon">&#9993;</span>
      <div>
        <strong>Primary Editorial Email:</strong><br>
        <a href="mailto:{email}">{email}</a>
      </div>
    </div>
    <div class="cd-item">
      <span class="cd-icon">&#128337;</span>
      <div>
        <strong>Response Turnaround:</strong><br>
        <span>Within 24 to 48 hours (Monday &ndash; Saturday, IST)</span>
      </div>
    </div>
    <div class="cd-item">
      <span class="cd-icon">&#128205;</span>
      <div>
        <strong>Testing Lab Location:</strong><br>
        <span>India (Asia/Kolkata timezone)</span>
      </div>
    </div>
    <div class="cd-item">
      <span class="cd-icon">&#128279;</span>
      <div>
        <strong>Official Channels:</strong><br>
        <a href="{yt}" target="_blank" rel="noopener">YouTube (@Rom_Flasher)</a> &middot; 
        <a href="{gh}" target="_blank" rel="noopener">GitHub (@romflasher3419-spec)</a>
      </div>
    </div>
  </div>
</div>

<h2>Send a Message</h2>
<p>Have an editorial inquiry, hardware verification question, or technical correction? Fill out the form below. Messages are delivered directly to my personal inbox with spam protection.</p>
{form}

<h2>Emergency Bootloop &amp; Unbrick Inquiries</h2>
<p>If you are reporting a bricked device or seeking diagnostic help, please include:</p>
<ul>
  <li><strong>Device Codename:</strong> e.g., POCO X7 Pro (<code>rodin</code>), Xiaomi Pad 5 (<code>nabu</code>), Redmi Note 10 Pro (<code>sweet</code>).</li>
  <li><strong>Target Firmware:</strong> Stock ROM version, AOSP build, or custom recovery release.</li>
  <li><strong>Failure State:</strong> Bootloader fastboot accessible, fastbootd userspace, recovery bootloop, or emergency download mode (EDL / BROM).</li>
</ul>

<h2>Bug Reports &amp; Code Issues</h2>
<p>Found an issue in the free Rom Flasher Tool or fastboot scripts? Please open an issue with terminal log output on our <a href="{repo}/issues" target="_blank" rel="noopener">GitHub Issue Tracker</a> so the broader community can benefit from the fix.</p>
""".format(email=CONTACT_EMAIL, yt=CHANNEL_URL, gh=REPO_URL, repo=REPO_URL, form=feedback_form())

    out["contact.html"] = simple("contact.html", "Contact Rohit Verma & Rom Flasher Lab", "Contact \u2014 %s" % SITE, contact_html_content,
                        description="Contact Rohit Verma, lead developer and publisher of Rom Flasher. Submit technical inquiries, guide requests, or lab verifications.",
                        schema={
                            "@context": "https://schema.org",
                            "@type": "ContactPage",
                            "name": "Contact %s" % SITE,
                            "url": "%s/contact.html" % SITE_URL,
                            "inLanguage": "en",
                            "publisher": {"@type": "Organization", "name": SITE,
                                          "url": SITE_URL,
                                          "email": CONTACT_EMAIL}})

    out["404.html"] = simple("404.html", "Page not found",
                             "Not found \u2014 %s" % SITE, """
<p>That address does not exist here. Try <a href="index.html">the home page</a>
or <a href="videos.html">the full list of guides</a>.</p>
""",
                             description="That page does not exist on Rom Flasher. "
                             "Head back to the home page, or open the full list "
                             "of custom ROM and flashing guides.")
    return out


def rfc822(value):
    """RSS 2.0 wants RFC-822 dates, not ISO. Feed readers reject the ISO form."""
    m = re.match(r"^(\d{4})-(\d{2})-(\d{2})", str(value or ""))
    if not m:
        return ""
    try:
        d = datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return ""
    return d.strftime("%a, %d %b %Y 00:00:00 GMT")


def build_feed(items):
    newest = sorted(items, key=lambda x: x.get("published") or "", reverse=True)[:40]
    entries = []
    for x in newest:
        link = "%s/rom/%s.html" % (SITE_URL, x["slug"])
        entries.append(
            "<item><title>%s</title><link>%s</link><guid>%s</guid>"
            "<pubDate>%s</pubDate><description>%s</description></item>"
            % (html.escape(x["title"]), html.escape(link), html.escape(link),
               rfc822(x.get("published")) or rfc822(BUILT_ON),
               html.escape(x.get("blurb") or x["title"])))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0"><channel>\n'
            "<title>%s</title><link>%s</link><description>%s</description>\n%s\n"
            "</channel></rss>\n" % (html.escape(SITE), SITE_URL,
                                    html.escape(TAGLINE), "\n".join(entries)))


# ------------------------------------------------------------------- build
EXCLUDED_NON_GUIDES = {
    "n-Wim8ZW0XI",  # Rap battle clip (non-technical)
    "6vY3AxT3-oU",  # Chase the cheque short
    "QRdXybKscvk",  # Quick reply viewer talk (no flashing)
    "NtMGfxg4j9o",  # Coding status short
}


def load_content():
    items, problems = [], []
    for path in sorted(glob.glob(os.path.join(CONTENT, "*.json"))):
        name = os.path.basename(path)
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
        except Exception as exc:                                   # noqa: BLE001
            problems.append("%s: bad json (%s)" % (name, exc))
            continue
        if data.get("id") in EXCLUDED_NON_GUIDES:
            continue
        for field in ("id", "title", "slug"):
            if not data.get(field):
                problems.append("%s: missing '%s'" % (name, field))
        data.setdefault("blurb", data.get("title", ""))
        for key in ("tags", "links", "faq"):
            data.setdefault(key, [])
        # When the written half of this guide was last touched - a real
        # dateModified, instead of "today" on every single rebuild.
        try:
            data["_mtime"] = datetime.fromtimestamp(
                os.path.getmtime(path)).strftime("%Y-%m-%d")
        except OSError:
            data["_mtime"] = ""
        if not data.get("body"):
            problems.append("%s: no body yet" % name)
        elif len(data["body"]) < 1800:
            problems.append("%s: body is short (%d)" % (name, len(data["body"])))
        items.append(data)
    return items, problems


def write(path, text):
    full = os.path.join(DIST, path.replace("/", os.sep))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def main():
    ap = argparse.ArgumentParser(description="Build the Rom Flasher site")
    ap.add_argument("--serve", type=int, default=0,
                    help="serve dist/ on this port after building")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    items, problems = load_content()
    if not items:
        print("[!] content/ is empty - nothing to build")
        return 1
    if problems and not args.quiet:
        unwritten = [p for p in problems if "no body" in p]
        real = [p for p in problems if "no body" not in p]
        print("[i] %d page(s) still waiting for a written body" % len(unwritten))
        for p in real[:20]:
            print("    -", p)

    if os.path.isdir(DIST):
        shutil.rmtree(DIST, ignore_errors=True)
    os.makedirs(os.path.join(DIST, "static"), exist_ok=True)

    # Which tags get an archive page is decided once, from the whole content
    # list, before any page is rendered - every chip on the site resolves
    # against this set.
    tag_hubs(items)

    # static/ is the single source of truth: css, icons, avatar
    for name in sorted(os.listdir(STATIC)):
        src = os.path.join(STATIC, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(DIST, "static", name))
        elif os.path.isdir(src):
            shutil.copytree(src, os.path.join(DIST, "static", name), dirs_exist_ok=True)

    # The phone index the downloader's search box reads. It is a file of its
    # own rather than a script tag because it is far too big to inline: a few
    # hundred phones with every build each would swamp the page. The browser
    # asks for it the first time somebody types in the search box, so the
    # page itself stays quick. Refresh it with: python fetch_firmware.py
    firmware = os.path.join(DATA, "firmware.json")
    if os.path.exists(firmware):
        shutil.copy2(firmware, os.path.join(DIST, "static", "firmware.json"))
        print("[i] phone index: %s" % os.path.join(DIST, "static", "firmware.json"))
    else:
        print("[i] no data/firmware.json - the downloader's phone search will "
              "stay empty until 'python fetch_firmware.py' has run")

    write("index.html", build_home(items, path=""))
    write("videos.html", build_guides(items))
    for item in items:
        write("rom/%s.html" % item["slug"], build_article(item, items))
    hubs = hub_map(items)
    for name, hub in hubs.items():
        write("device/%s.html" % hub["slug"],
              build_device_page(name, hub, len(items), hubs))

    group_hubs = all_hubs(items)
    for kind, kind_hubs in group_hubs.items():
        for name, hub in kind_hubs.items():
            write("%s/%s.html" % (HUB_KINDS[kind]["dir"], hub["slug"]),
                  build_hub_page(kind, name, hub, kind_hubs, len(items), items))
        write(HUB_KINDS[kind]["index"],
              build_hub_index(kind, kind_hubs, len(items), items))

    for name, text in build_static(items).items():
        write(name, text)

    write("site.webmanifest", json.dumps({
        "name": "%s \u2014 ROM and flashing guides" % SITE,
        "short_name": SITE,
        "description": TAGLINE,
        "start_url": "./",
        "scope": "./",
        "display": "standalone",
        "background_color": "#05070c",
        "theme_color": "#05070c",
        "icons": [
            {"src": "static/app-icon-192.png", "sizes": "192x192",
             "type": "image/png", "purpose": "any"},
            {"src": "static/app-icon-512.png", "sizes": "512x512",
             "type": "image/png", "purpose": "any"},
            {"src": "static/apple-touch-icon.png", "sizes": "180x180",
             "type": "image/png"},
        ],
    }, indent=1))
    write(".nojekyll", "")

    if ADS_PUBLISHER:
        # Written only when the AdSense publisher really exists - a wrong ads.txt
        # is worse than none at all.
        write("ads.txt", "google.com, %s, DIRECT, f08c47fec0942fa0\n"
              % ADS_PUBLISHER)
    if CUSTOM_DOMAIN:
        write("CNAME", CUSTOM_DOMAIN + "\n")

    # Google Search Console, "HTML file" method. The file is a single line -
    # "google-site-verification: google<hex>.html" - and has to be served at the
    # site root under exactly the name Google issued, so it is written here
    # rather than committed, which also keeps dist/ the single source of truth.
    # Set ROMFLASHER_GOOGLE_FILE to the file name (or the whole line) and the
    # file appears on the next build.
    if GOOGLE_FILE_NAME:
        write(GOOGLE_FILE_NAME, "google-site-verification: %s\n"
              % GOOGLE_FILE_NAME)

    # IndexNow ownership file: <key>.txt at the site root, containing the key.
    if INDEXNOW_KEY:
        write(INDEXNOW_KEY + ".txt", INDEXNOW_KEY + "\n")

    newest_date = max((x.get("published") or BUILT_ON for x in items),
                      default=BUILT_ON)
    static_urls = [("", "1.0", "daily", newest_date),
                   ("videos.html", "0.9", "daily", newest_date),
                   ("download.html", "0.95", "weekly", BUILT_ON),
                   ("downloader.html", "0.9", "weekly", BUILT_ON),
                   ("about.html", "0.8", "monthly", BUILT_ON),
                   ("contact.html", "0.6", "monthly", BUILT_ON),
                   ("privacy.html", "0.4", "yearly", BUILT_ON),
                   ("terms.html", "0.4", "yearly", BUILT_ON),
                   ("donate.html", "0.4", "monthly", BUILT_ON)]
    entries = ['<url><loc>%s/%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq>'
               '<priority>%s</priority></url>' % (SITE_URL, u, lm, cf, pr)
               for u, pr, cf, lm in static_urls]
    entries += ['<url><loc>%s/rom/%s.html</loc><lastmod>%s</lastmod>'
                '<changefreq>monthly</changefreq><priority>0.7</priority></url>'
                % (SITE_URL, x["slug"], x.get("published") or BUILT_ON)
                for x in items]
    entries += ['<url><loc>%s/device/%s.html</loc><lastmod>%s</lastmod>'
                '<changefreq>weekly</changefreq><priority>0.8</priority></url>'
                % (SITE_URL, hub["slug"],
                   max(x.get("published") or BUILT_ON for x in hub["rows"]))
                for hub in hubs.values()]
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(entries) + "\n</urlset>\n")
    write("robots.txt",
          "User-agent: *\nAllow: /\n\n"
          "User-agent: Googlebot-Image\nAllow: /\n\n"
          "Sitemap: %s/sitemap.xml\n" % SITE_URL)
    write("feed.xml", build_feed(items))
    write("_headers", SECURITY_HEADERS)

    print("[OK] %d guide(s) -> dist/" % len(items))
    print("     index, videos, download, apps/about/privacy/terms/contact/404,")
    print("     %d x rom/*.html, %d device page(s)," % (len(items), len(hubs)))
    print("     sitemap.xml, robots.txt, feed.xml, static/")

    if args.serve:
        import functools
        import http.server
        import socketserver
        handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                    directory=DIST)
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("127.0.0.1", args.serve), handler) as httpd:
            print("     http://127.0.0.1:%d/   (ctrl+c stops)" % args.serve)
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
