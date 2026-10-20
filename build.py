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

SITE = "Rom Flasher"
TAGLINE = "Custom ROMs, flashing guides and a free Android tool"

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
CUSTOM_DOMAIN = os.environ.get("ROMFLASHER_DOMAIN", "").strip().strip("/")
SITE_URL = (os.environ.get("ROMFLASHER_SITE_URL", "").strip()
            or (("https://" + CUSTOM_DOMAIN) if CUSTOM_DOMAIN else PAGES_URL)
            ).rstrip("/")

# ------------------------------------------------------- switch-on-when-set
# Each of these is off while empty, so nothing half-configured ever ships.
# Paste the value, rebuild, and that one feature turns itself on.
GA4_ID = os.environ.get("ROMFLASHER_GA4", "")          # "G-XXXXXXXXXX"
ADS_PUBLISHER = os.environ.get("ROMFLASHER_ADS", "")   # "pub-0000000000000000"

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
GOOGLE_VERIFY = os.environ.get("ROMFLASHER_GOOGLE", "")  # Search Console token
BING_VERIFY = os.environ.get("ROMFLASHER_BING", "")      # Bing Webmaster token
# Search Console can also verify by serving a file at the site root. Either the
# file name ("google8e8e....html") or the whole "google-site-verification: ..."
# line is accepted here; only the name survives into the built file.
GOOGLE_FILE_NAME = os.environ.get("ROMFLASHER_GOOGLE_FILE", "").strip()
if GOOGLE_FILE_NAME.lower().startswith("google-site-verification:"):
    GOOGLE_FILE_NAME = GOOGLE_FILE_NAME.split(":", 1)[1].strip()
if GOOGLE_FILE_NAME and not GOOGLE_FILE_NAME.endswith(".html"):
    GOOGLE_FILE_NAME += ".html"
TOOL_URL = "https://github.com/romflasher3419-spec/rom-flasher-tool/releases/latest"
REPO_URL = "https://github.com/romflasher3419-spec/rom-flasher-tool"
CHANNEL_URL = "https://www.youtube.com/@Rom_Flasher"

# /releases/latest/download/<asset> always points at the newest build, so the
# button on the download page never has to be edited again.
APK_URL = REPO_URL + "/releases/latest/download/app-release.apk"
RELEASES_URL = REPO_URL + "/releases"

APP = {
    "version": "v1.2.3",
    "released": "20 Oct 2026",
    "size": "8.3 MB",
    "bytes": "8708397",
    "sha256": "D010C2047963FE37A6BB7E8F1E508733B130D3DC5126EF622E1C1FC5286DB1B6",
    "android": "Android 8.0 or newer",
}

# ---------------------------------------------------------------------------
# Remote feature flags for the app  ->  dist/app-config.json
#
# The app reads this on every launch. Edit APP_HIDE to switch cards off, and
# APP_NOTICE to put a line under the header. Bump APP_REV so the change is
# easy to spot in the log.
#
# House rules:
#   * APP_HIDE lists what to HIDE. Anything not listed stays visible, so an
#     empty list - the normal state - shows every card in the app.
#   * APP_NOTICE is "" in normal times.
#   * Valid names are exactly the keys in app_config_json() below. A name that
#     is not in that list is dropped at build time, with a warning, instead of
#     silently hiding the wrong thing on people's phones.
# ---------------------------------------------------------------------------
APP_REV = 2
APP_HIDE = []          # e.g. ["payloadDumper"] - card disappears completely
APP_SOON = []          # e.g. ["payloadDumper"] - card stays, blurred, "coming soon"
APP_NOTICE = ""        # e.g. "Payload Dumper is being rebuilt. Back soon."

# The line drawn across a card that is in APP_SOON. One string, so the whole
# app says the same thing and there is nothing to keep in step by hand.
APP_SOON_LABEL = "\U0001F527 Back with fixes soon"

# The switch names the app understands. Keep in step with RemoteConfig.Feature
# in the Android project - tests catch a drift, but naming them here too makes
# the two sides readable together.
APP_FEATURES = [
    "fastboot", "sideload", "customImage", "advancedReboot", "slotManager",
    "tools", "payloadDumper", "appManager", "rootWizard", "kernel",
    "fileManager", "romDownloader",
]


def app_config_json():
    """Build dist/app-config.json, warning loudly about unknown switch names."""
    unknown = [x for x in APP_HIDE if x not in APP_FEATURES]
    for bad in unknown:
        print("  [WARN] app-config: '%s' is not a known feature - dropped" % bad)
    unknown = [x for x in APP_SOON if x not in APP_FEATURES]
    for bad in unknown:
        print("  [WARN] app-config: '%s' is not a known feature - dropped" % bad)
    hide = [x for x in APP_HIDE if x in APP_FEATURES]
    soon = [x for x in APP_SOON if x in APP_FEATURES]
    # A card cannot be both gone and blurred; hide wins, and that is worth
    # saying out loud rather than shipping a config that contradicts itself.
    for name in soon:
        if name in hide:
            print("  [WARN] app-config: '%s' is in both hide and soon - "
                  "hiding it" % name)
    soon = [x for x in soon if x not in hide]
    payload = {
        "rev": APP_REV,
        "hide": hide,
        "soon": soon,
        "soonLabel": APP_SOON_LABEL,
        "notice": APP_NOTICE,
    }
    if hide or soon or APP_NOTICE:
        print("     app-config: rev %d | hiding %s | soon %s | notice %s"
              % (APP_REV, hide or "nothing", soon or "nothing",
                 "set" if APP_NOTICE else "none"))
    return json.dumps(payload, indent=1, ensure_ascii=False) + "\n"

# Where "send me a message" lands. FormSubmit needs no account: the first
# submission mails an activation link to this address, one click and it is live.
CONTACT_EMAIL = "vrohit3419@gmail.com"
FORM_ENDPOINT = "https://formsubmit.co/ajax/" + CONTACT_EMAIL

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
YT_LOGO = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor">'
           '<path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4'
           '.5A3 3 0 0 0 .5 6.2 31 31 0 0 0 0 12a31 31 0 0 0 .5 5.8 3 3 0 0 0 2.1'
           ' 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1A31 31 0 0 0 24'
           ' 12a31 31 0 0 0-.5-5.8zM9.5 15.6V8.4l6.3 3.6-6.3 3.6z"/></svg>')

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
    """A sane, de-duplicated keyword list for a page."""
    parts = []
    if item:
        parts += [clean_device(item.get("device")), item.get("rom"),
                  item.get("android")]
        parts += list(item.get("tags") or [])
    parts += list(extra)
    parts += list(SEO_CORE)

    seen, out = set(), []
    for value in parts:
        value = (value or "").strip()
        key = value.lower()
        if len(value) < 2 or key in seen:
            continue
        seen.add(key)
        out.append(value)
    return ", ".join(out[:30])

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


def analytics_head():
    """Analytics + AdSense, loaded only after the visitor says yes.

    Nothing is fetched, no cookie is set, and no banner is even shown while the
    IDs below are empty - so the site stays completely clean until it is
    actually earning something.
    """
    if not (GA4_ID or ADS_PUBLISHER):
        return ""
    return """<script>
(function(){
  var GA=%(ga)s, ADS=%(ads)s, KEY='rf-consent';
  function load(){
    if(GA){var s=document.createElement('script');s.async=true;
      s.src='https://www.googletagmanager.com/gtag/js?id='+GA;
      document.head.appendChild(s);
      window.dataLayer=window.dataLayer||[];
      window.gtag=function(){dataLayer.push(arguments);};
      gtag('js',new Date());gtag('config',GA);}
    if(ADS){var a=document.createElement('script');a.async=true;
      a.crossOrigin='anonymous';
      a.src='https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-'+ADS;
      document.head.appendChild(a);}
  }
  var choice=null;
  try{choice=localStorage.getItem(KEY);}catch(e){}
  if(choice==='yes'){load();return;}
  if(choice==='no'){return;}
  function banner(){
    var b=document.createElement('div');
    b.className='consent';
    b.innerHTML='<p>This site would like to set cookies for analytics and ads. '\
      +'They tell me which guides actually helped. Nothing loads until you say yes.</p>'\
      +'<div class="row"><button type="button" class="btn" id="rf-ok">That is fine</button>'\
      +'<button type="button" class="btn ghost" id="rf-no">No thanks</button></div>';
    document.body.appendChild(b);
    document.getElementById('rf-ok').onclick=function(){
      try{localStorage.setItem(KEY,'yes');}catch(e){}
      b.parentNode.removeChild(b);load();};
    document.getElementById('rf-no').onclick=function(){
      try{localStorage.setItem(KEY,'no');}catch(e){}
      b.parentNode.removeChild(b);};
  }
  if(document.readyState==='loading'){
    document.addEventListener('DOMContentLoaded',banner);}else{banner();}
})();
</script>""" % {"ga": json.dumps(GA4_ID), "ads": json.dumps(ADS_PUBLISHER)}


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

    Google's review crawler looks for the loader tag in the raw HTML, so it has
    to sit in <head> outside the consent gate. Loading the loader also does not
    serve or request a single ad: Google keeps every request idle until an
    <ins class="adsbygoogle"> is pushed, and those are only pushed by
    ad_slot(), which in turn only renders once the visitor accepts. So the
    privacy promise stays exactly as written - no cookie, no ad, no tracking
    before consent.

    Only emitted while ADS_PUBLISHER is set, so a half-finished setup can never
    ship the tag.
    """
    if not ADS_PUBLISHER:
        return ""
    return ('<script async src="https://pagead2.googlesyndication.com/pagead/'
            'js/adsbygoogle.js?client=ca-%s" crossorigin="anonymous"></script>'
            % html.escape(ADS_PUBLISHER))


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
    if len(toc) < 3:
        return ""
    items = "".join('<li><a href="#%s">%s</a></li>' % (anchor, html.escape(text))
                    for anchor, text in toc)
    return ('<nav class="toc" aria-label="On this page"><b>On this page</b>'
            "<ol>%s</ol></nav>" % items)


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


def md(text):
    """Block markdown: ## headings, - / 1. lists, > quotes, paragraphs."""
    out, ul, ol, mode = [], [], [], None

    def flush():
        nonlocal mode
        if mode == "ul" and ul:
            out.append("<ul>" + "".join("<li>%s</li>" % inline(b) for b in ul) + "</ul>")
            ul.clear()
        if mode == "ol" and ol:
            out.append("<ol>" + "".join("<li>%s</li>" % inline(b) for b in ol) + "</ol>")
            ol.clear()
        mode = None

    for raw in (text or "").splitlines():
        line = raw.rstrip()
        if not line.strip():
            flush()
            continue
        if line.lstrip().startswith("#"):
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
        else:
            flush()
            out.append("<p>%s</p>" % inline(line))
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


# ------------------------------------------------------------------ layout

# The pointer glow: two blurred orbs rendered on every page. The markup is the
# light itself, the script only moves it, and both are skipped on touch devices
# (see the media query in style.css).
CURSOR_LIGHT = ('<div class="cursorlight" id="cursorlight" aria-hidden="true">'
                '<i class="orb"></i><i class="core"></i></div>')

CURSOR_LIGHT_JS = """<script>
(function(){
  var layer = document.getElementById('cursorlight');
  if(!layer) return;
  try{
    if(window.matchMedia('(hover:none)').matches ||
       window.matchMedia('(pointer:coarse)').matches) return;
  }catch(e){}
  var orb = layer.getElementsByClassName('orb')[0];
  var core = layer.getElementsByClassName('core')[0];
  if(!orb || !core) return;

  var tx = -9999, ty = -9999;                 // where the pointer is right now
  var ox = tx, oy = ty;                       // the wide, slow light
  var cx = tx, cy = ty;                       // the bright one that keeps up
  var raf = 0, still = 0;

  function place(node, x, y){
    node.style.transform = 'translate3d(' + x.toFixed(2) + 'px,' + y.toFixed(2) + 'px,0)';
  }

  function frame(){
    ox += (tx - ox) * 0.07;  oy += (ty - oy) * 0.07;
    cx += (tx - cx) * 0.30;  cy += (ty - cy) * 0.30;
    place(orb, ox, oy);
    place(core, cx, cy);
    var caught = Math.abs(tx - ox) < 0.4 && Math.abs(ty - oy) < 0.4 &&
                 Math.abs(tx - cx) < 0.4 && Math.abs(ty - cy) < 0.4;
    still = caught ? still + 1 : 0;
    if(still > 24){ raf = 0; return; }        // it has caught up; stop drawing
    raf = requestAnimationFrame(frame);
  }
  function start(){ if(!raf) raf = requestAnimationFrame(frame); }

  window.addEventListener('pointermove', function(e){
    tx = e.clientX; ty = e.clientY;
    if(!layer.className.match(/\\bon\\b/)){
      layer.className += ' on';
      ox = cx = tx; oy = cy = ty;             // arrive, do not fly in from a corner
      place(orb, ox, oy); place(core, cx, cy);
    }
    start();
  }, {passive:true});

  function hide(){ layer.className = layer.className.replace(/\\s*\\bon\\b/, ''); }
  document.addEventListener('mouseleave', hide);
  window.addEventListener('blur', hide);
})();
</script>"""


def page(title, description, body, path="", extra_head="", keywords="",
         og_type="website", image=None):
    """Assemble a full page. `path` is where it will live inside dist/."""
    up = "../" * path.count("/")
    canon = "%s/%s" % (SITE_URL, path) if path else SITE_URL + "/"
    desc = html.escape((description or title)[:300])
    title_esc = html.escape(title)
    img = image or (SITE_URL + "/static/app.png")

    head = "\n".join([
        "<!doctype html>",
        '<html lang="en">',
        "<head>",
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        "<title>%s</title>" % title_esc,
        '<meta name="description" content="%s">' % desc,
        '<meta name="keywords" content="%s">' % html.escape(keywords or keywords_for()),
        '<meta name="robots" content="index,follow,max-image-preview:large,'
        'max-snippet:-1,max-video-preview:-1">',
        '<meta name="author" content="%s">' % SITE,
        '<meta name="theme-color" content="#05070c">',
        '<meta name="rating" content="general">',
        '<link rel="canonical" href="%s">' % canon,
        '<link rel="icon" type="image/svg+xml" href="%sstatic/favicon.svg">' % up,
        '<link rel="apple-touch-icon" sizes="180x180" '
        'href="%sstatic/apple-touch-icon.png">' % up,
        '<link rel="manifest" href="%ssite.webmanifest">' % up,
        '<link rel="preconnect" href="https://www.youtube.com">',
        '<link rel="preconnect" href="https://i.ytimg.com">',
        '<link rel="dns-prefetch" href="https://www.youtube-nocookie.com">',
        verify_head(),
        adsense_verify(),
        analytics_head(),
        '<link rel="stylesheet" href="%sstatic/style.css">' % up,
        '<link rel="alternate" type="application/rss+xml" title="%s" '
        'href="%sfeed.xml">' % (SITE, up),
        '<meta property="og:type" content="%s">' % og_type,
        '<meta property="og:site_name" content="%s">' % SITE,
        '<meta property="og:locale" content="en_US">',
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
        CURSOR_LIGHT,
        '<header class="top"><div class="wrap">',
        '  <a class="brand" href="%sindex.html"><img class="applogo" '
        'src="%sstatic/app.png" alt="Rom Flasher tool icon" width="30" '
        'height="30"><span class="brandtx"><span class="brandname">Rom<b>Flasher</b></span>'
        '<span class="brandsub">All-In-One Android Tool</span></span></a>' % (up, up),
        "  <nav>",
        "    <span class=\"navplain\">",
        '    <a href="%sindex.html">Home</a>' % up,
        '    <a href="%svideos.html">Guides</a>' % up,
        '    <a href="%sapps.html">Tool</a>' % up,
        "    </span>",
        '    <a class="navbtn hot" href="%sdownload.html">Download</a>' % up,
        '    <a class="navbtn donate" href="%sdonate.html">%sCoffee</a>' % (up, COFFEE_LOGO),
        '    <a class="navbtn gh" href="%s" rel="noopener" '
        'aria-label="Rom Flasher tool on GitHub">%sGitHub</a>' % (REPO_URL, GH_LOGO),
        '    <a class="yt" href="%s" rel="noopener">%sYouTube</a>' % (CHANNEL_URL, YT_LOGO),
        "  </nav>",
        "</div></header>",
    ])

    # a new query string every time the stylesheet changes, so no stale css
    head = head.replace('static/style.css"',
                        'static/style.css?v=%s"' % ASSET_VER)

    browse = ('<p class="browse">'
              '<a href="%sbrands.html">Brands</a> &middot; '
              '<a href="%sroms.html">ROMs</a> &middot; '
              '<a href="%svideos.html">All guides</a> &middot; '
              '<a href="%syears.html">By year</a> &middot; '
              '<a href="%stopics.html">Topics</a></p>'
              % ((up,) * 5))
    foot = """<footer><div class="wrap">
  <p><strong>%s</strong> &middot; %s</p>
  %s
  <p>
    <a href="%sabout.html">About</a> &middot;
    <a href="%scontact.html">Contact</a> &middot;
    <a href="%sprivacy.html">Privacy</a> &middot;
    <a href="%sterms.html">Terms</a> &middot;
    <a href="%sdownload.html">Download the tool</a> &middot;
    <a href="%sdonate.html">Buy me a coffee</a> &middot;
    <a href="%sdownload.html#talk-to-me">Send a message</a> &middot;
    <a href="%s" rel="noopener">YouTube channel</a>
  </p>
  <p class="dis">Not affiliated with Xiaomi, POCO, Redmi or any ROM project.
  Flashing is at your own risk &mdash; read the <a href="%sterms.html">terms</a> first.</p>
</div></footer>
</body>
</html>
""" % (SITE, TAGLINE, browse, up, up, up, up, up, up, up, CHANNEL_URL, up)

    # the pointer light is moved by a script, so it belongs at the end of body
    foot = foot.replace("</body>", CURSOR_LIGHT_JS + "\n</body>")
    return head + body + "\n" + foot


def card(item, up=""):
    tags = "".join('<span class="tag">%s</span>' % html.escape(t)
                   for t in (item.get("tags") or [])[:3])
    foot = []
    if clean_device(item.get("device")):
        foot.append(html.escape(clean_device(item["device"])))
    if item.get("published"):
        foot.append(nice_date(item["published"]))
    else:
        foot.append("%s views" % item.get("views", 0))
    return ('<a class="card" href="%srom/%s.html">'
            "<h3>%s</h3><p>%s</p>%s<span class=\"foot\">%s</span></a>"
            % (up, html.escape(item["slug"]), html.escape(item["title"]),
               html.escape(item.get("blurb") or ""), tags,
               " &middot; ".join(foot)))


# ------------------------------------------------------------------- pages
def build_home(items, path="index.html"):
    by_views = sorted(items, key=lambda x: -(x.get("views") or 0))[:9]
    by_date = sorted(items, key=lambda x: x.get("published") or "", reverse=True)[:9]
    body = """<section class="hero"><div class="wrap">
<h1>Flash <em>any ROM, any phone</em> &mdash; with steps that actually work.</h1>
<p>%s. Every video gets a written page here, so you can follow along without
pausing the video twenty times.</p>
<a class="btn" href="download.html">Download Rom Flasher (free)</a>
<a class="btn ghost" href="videos.html">Browse all %d guides</a>
</div></section>
<div class="wrap">
%s
<h2>Newest guides</h2>
<div class="grid">%s</div>
<h2>Most watched</h2>
<div class="grid">%s</div>
</div>""" % (TAGLINE, len(items), ad_slot("hub"),
             "".join(card(x) for x in by_date),
             "".join(card(x) for x in by_views))

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

    return page("%s \u2014 %s" % (SITE, TAGLINE), TAGLINE, body, path,
                extra_head=head, keywords=keywords_for())


def build_guides(items, path="videos.html"):
    """All guides with a real date column, sortable, plus year chips."""
    rows = []
    for i, x in enumerate(items):
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

    body = """<div class="wrap"><section style="padding:32px 0 0">
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

    body = """<div class="wrap"><section style="padding:32px 0 0">
<h1>%s &mdash; custom ROM and flashing guides (%d)</h1>
<p class="dis">Every <strong>%s</strong> video on the Rom Flasher channel, newest
first, with the date it went live. %s %s</p>
<p><a class="btn" href="%sdownload.html">Download the free Rom Flasher tool</a>
<a class="btn ghost" href="%svideos.html">All %d guides</a></p>

<table><thead><tr><th>Guide</th><th>Released</th><th>Views</th></tr></thead>
<tbody>%s</tbody></table>

<h2>Questions people ask</h2>
%s

<h2>Other phones</h2>
<div class="chips">%s</div>
</section></div>""" % (html.escape(name), count, html.escape(name), rom_line,
                       brand_line, up, up, total, table, faq_html, siblings)

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

    return page("%s flashing guides \u2014 custom ROM, root, recovery | %s"
                % (name, SITE),
                "All %d Rom Flasher guides for the %s: custom ROMs, fastboot "
                "flashing, root and recovery, newest first with dates."
                % (count, name),
                body, path, extra_head=head,
                image=newest_thumb(rows) or (SITE_URL + "/static/app.png"),
                keywords=keywords_for(item={"device": name, "tags": roms}))


HUB_KINDS = {
    "brand": {"dir": "brand", "index": "brands.html", "word": "brand",
              "h1": "%s &mdash; flashing guides (%d)",
              "title": "%s flashing guides \u2014 custom ROM, root, recovery",
              "label": "Brands"},
    "rom": {"dir": "roms", "index": "roms.html", "word": "ROM",
            "h1": "%s &mdash; guides and installs (%d)",
            "title": "%s guides \u2014 install, download, fixes",
            "label": "ROMs"},
    "year": {"dir": "year", "index": "years.html", "word": "year",
             "h1": "Flashing guides from %s (%d)",
             "title": "Android flashing and custom ROM guides from %s",
             "label": "Years"},
    "topic": {"dir": "topic", "index": "topics.html", "word": "topic",
              "h1": "%s &mdash; Android guides (%d)",
              "title": "%s guides \u2014 Android root, ROM and recovery",
              "label": "Topics"},
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
    else:
        first = ("What do these %s guides cover?" % name,
                 "%d guides on this one job, across every phone it has been "
                 "done on." % count)
        covered = ("Which phones do these %s guides cover?" % name,
                   "%s." % ", ".join(devices[:8]) if devices else
                   "Whatever is listed above.")

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
    return "".join('<div class="faq"><h3>%s</h3><p>%s</p></div>' % (q, a)
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
        for k in ("brand", "rom", "year", "topic") if k != kind)

    body = """<div class="wrap"><section style="padding:32px 0 0">
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

    return page("%s | %s" % (cfg["title"] % html.escape(name), SITE),
                "Every Rom Flasher guide for %s: custom ROMs, root, recovery and "
                "fastboot steps, newest first with dates. %d in total."
                % (name, count),
                body, path, extra_head=head, og_type="website",
                image=newest_thumb(rows) or (SITE_URL + "/static/app.png"),
                keywords=keywords_for(extra=(name, "%s guides" % name,
                                             "%s flashing" % name)))


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
    }[kind]

    body = ('<div class="wrap"><section style="padding:32px 0 0">'
            "<h1>%s</h1><p class=\"dis\">%s</p><div class=\"grid\">%s</div>"
            "<p><a class=\"btn ghost\" href=\"videos.html\">All %d guides</a></p>"
            "</section></div>" % (head_line[0], head_line[1], cards, total))

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
    return page("%s \u2014 %s" % (head_line[0], SITE), head_line[1], body,
                cfg["index"], extra_head=head,
                keywords=keywords_for(extra=(head_line[0],
                                             cfg["label"].lower())))


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

    out = ['<article>', '<div class="prose">',
           '<div class="head">', avatar_html, "<div>",
           "<h1>%s</h1>" % html.escape(item["title"]),
           '<p class="meta"><span class="who">Rom Flasher</span> &middot; %s</p>'
           % " &middot; ".join(meta),
           "</div></div>"]

    if item.get("tags"):
        out.append('<div class="tags"><span class="tagslabel">Tags</span>%s</div>'
                   % "".join('<span class="tag">%s</span>' % html.escape(t)
                             for t in item["tags"]))

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

    if item.get("url"):
        vid = video_id_of(item["url"])
        watch = html.escape(item["url"])
        out.append(
            '<div class="videobox"><div class="frame">'
            '<iframe frameborder="0" src="https://www.youtube.com/embed/%s'
            '?autoplay=1&amp;mute=1&amp;loop=1&amp;playlist=%s&amp;rel=0'
            '&amp;modestbranding=1&amp;playsinline=1" title="%s" '
            'allow="accelerometer; autoplay; clipboard-write; encrypted-media; '
            'gyroscope; picture-in-picture" allowfullscreen '
            'referrerpolicy="strict-origin-when-cross-origin"></iframe></div>'
            '<p class="hint">The video starts muted so it does not blast at you '
            '&mdash; tap the speaker to hear it, or '
            '<a href="%s" rel="noopener">open it on YouTube</a>.</p>'
            '<script>if(location.protocol==="file:"){var f=document.querySelector'
            '(".videobox .frame iframe");if(f){var a=document.createElement("a");'
            'a.className="ytposter";a.href="%s";a.target="_blank";a.rel="noopener";'
            'a.style.backgroundImage="url(https://i.ytimg.com/vi/%s/hqdefault.jpg)";'
            'a.innerHTML="<span>Play it on YouTube</span>";f.replaceWith(a);}}'
            '</script></div>'
            % (html.escape(vid), html.escape(vid), html.escape(item["title"]),
               watch, watch, html.escape(vid)))

    out.append(
        '<div class="cta"><div class="ctatext"><strong>No PC in the room?</strong>'
        '<span>The free Rom Flasher tool runs the whole flash from the phone in '
        'your hand &mdash; USB-OTG cable, no laptop, no command line.</span></div>'
        '<a class="btn dark" href="%sdownload.html">%sDownload the free Rom '
        'Flasher tool</a></div>' % (up, DL_LOGO))

    body = (item.get("body") or "").strip()
    desc = (item.get("video_description") or "").strip()
    steps = steps_from_md(body)
    toc = []

    if body:
        rendered, toc = heading_ids(md(body))
        tools = [toc_html(toc)]
        if len(steps) >= 3:
            tools.append(
                '<button class="copybtn steps" type="button" '
                'data-label="Copy the %d steps" data-steps="%s">Copy the %d '
                'steps</button>'
                % (len(steps),
                   html.escape(json.dumps(steps, ensure_ascii=False), quote=True),
                   len(steps)))
        tools = [t for t in tools if t]
        if tools:
            out.append('<div class="arttools">%s</div>' % "".join(tools))
        out.append(rendered)
    elif desc:
        out.append('<div class="notice">This page is the video in text form. '
                   'The full write-up is being filled in by hand &mdash; until then '
                   'the complete description is below.</div>')
        out.append(md(desc_to_md(desc)))

    links = item.get("links") or []
    if links:
        rows = "\n".join(
            "<li>%s<a href=\"%s\" rel=\"nofollow noopener\">%s</a></li>"
            % (("<strong>%s</strong> &mdash; " % html.escape(l["label"]))
               if l.get("label") else "",
               html.escape(l["url"]), html.escape(l["url"]))
            for l in links)
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
        faq_html = "".join('<div class="faq"><h3>%s</h3>%s</div>'
                           % (inline(f.get("q", "")), md(f.get("a", "")))
                           for f in faq)
        out.append("<h2>Common questions</h2>%s" % faq_html)

    out.append(ad_slot("article", up))

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
        "author": {"@type": "Organization", "name": SITE, "url": SITE_URL},
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

    return page(item["title"], item.get("blurb") or item["title"],
                "\n".join(out), path, extra_head=head,
                keywords=keywords_for(item), og_type="article",
                image=thumb or (SITE_URL + "/static/app.png"))


def simple(path, h1, title, block, description=None, keywords="", extra_head="",
           og_type="website"):
    body = ('<article><div class="prose"><h1>%s</h1>\n%s\n</div></article>'
            % (h1, block))
    return page(title, description or h1, body, path, extra_head=extra_head,
                keywords=keywords, og_type=og_type)


def feedback_form(anchor=True, lead=""):
    """A message box that lands in a real inbox - no account, no GitHub trip.

    Posts to FormSubmit with fetch() so the visitor never leaves the page. The
    very first submission mails an activation link to CONTACT_EMAIL; after that
    one click every message is delivered straight away.
    """
    return """%s<form class="fbform" id="feedback" action="%s" method="POST">
  <input type="hidden" name="_subject" value="New message from the Rom Flasher website">
  <input type="hidden" name="_template" value="table">
  <input type="hidden" name="_captcha" value="false">
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
  if(!f||!window.fetch) return;
  f.addEventListener('submit',function(e){
    e.preventDefault();
    var note=f.querySelector('.fbnote'),btn=f.querySelector('button[type=submit]');
    var label=btn.innerHTML;
    btn.disabled=true;btn.textContent='Sending...';
    note.className='fbnote';note.textContent='Sending...';
    fetch(f.action,{method:'POST',headers:{'Accept':'application/json'},
                    body:new FormData(f)})
      .then(function(r){return r.json();})
      .then(function(d){
        var ok=d&&(d.success===true||d.success==='true');
        if(ok){f.reset();note.className='fbnote ok';
               note.textContent='Got it - thank you! Your message is in my inbox.';}
        else{note.className='fbnote bad';
             note.textContent='That did not go through. Give it one more try?';}
      })
      .catch(function(){note.className='fbnote bad';
        note.textContent='Network hiccup. Try again in a second, or mail %s.';})
      .then(function(){btn.disabled=false;btn.innerHTML=label;});
  });
})();
</script>""" % (lead, FORM_ENDPOINT, CONTACT_EMAIL, CONTACT_EMAIL, CONTACT_EMAIL)


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
<li>More devices and regions added to the stock ROM downloader</li>
<li>Faster fixes when a build misbehaves on one exact model</li>
<li>Fewer evenings lost to dead mirrors and broken packages</li>
</ul>

<p>Thank you for keeping this going. &nbsp;ðŸ’›</p>
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
                              "and both keep the free tool free.")


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
            "Custom images: <code>boot</code>, <code>init_boot</code>, <code>super</code>, <code>vbmeta</code>",
            "Sparse-chunk engine for big 4&ndash;8&nbsp;GB partitions",
            "A/B slot manager, and a confirmation before anything risky",
        ]),
        ("Tools &amp; recovery", [
            "IMEI / EFS backup and restore",
            "Kernel backup, restore and flash, plus a boot-loop rescue",
            "Root wizard for KernelSU and Magisk",
            "App installer for <code>.apk</code>, <code>.xapk</code> and <code>.apkm</code>",
            "Debloater, file manager, full device info, live command terminal",
        ]),
        ("Stock ROM downloader", [
            "Region-wise stock ROMs for Xiaomi, POCO, OnePlus, OPPO, realme, "
            "vivo / iQOO and Google Pixel",
            "Recovery and fastboot packages from one picker",
            "Parallel multi-segment downloads, fastest mirror picked for you, "
            "with failover",
            "An IDM-style download popup so you can carry on using the app",
        ]),
        ("Extras", [
            "Payload dumper with SHA-256 verification",
            "ROM-wise backup picker",
            "Video guides inside the app",
            "Cancel an extraction at any point",
        ]),
    ]
    feats = "".join(
        '<div class="feat"><h3>%s</h3><ul>%s</ul></div>'
        % (name, "".join("<li>%s</li>" % line for line in lines))
        for name, lines in features)

    faq_html = "".join('<div class="faq"><h3>%s</h3><p>%s</p></div>' % (q, a)
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
      <span class="gicon">&#11015;</span>
      <span>Download {ver} for Android<small>{size} &middot; Android 8.0+ &middot;
      free, no sign-in</small></span></a>
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

<h2>The small things that make it work</h2>
<p>Cables are the number one reason a phone never shows up in fastboot. These are
the three I actually keep in the drawer.</p>
{gear}

<h2>Fresh in {ver}</h2>
<p>This build adds a thin control line between this site and the app. The app
reads one small file here on every launch, so a card can be taken down for repair
or a short notice shown without a new APK and without asking anyone to
update.</p>
<p>That file is an <b>override list</b>, which is what makes it safe: anything it
does not mention stays visible, a broken or missing file hides nothing, and with
no internet the app just runs on its last good copy. It is never a paywall, and
right now it hides nothing at all &mdash; your dashboard is exactly what it was.</p>
<p>A card can also be put <b>on hold instead of removed</b>. It stays exactly where
it is, blurred, with a line across it, and tapping it does nothing &mdash; so a
feature under repair never leaves a gap where a familiar button used to be. As
with everything else here, if the app cannot reach this site it shows every card
normally, so nobody is ever locked out of a working build.</p>
<p>The update rule is unchanged too. When a newer Rom Flasher is out, one dialog
appears with <b>Update</b>, which opens this site, and <b>Close</b>, which closes
the app. Closing is not a way past it &mdash; open the app again and the same
dialog is there until you install the new build. And if the check cannot get a
straight answer, the app opens normally, so nobody is locked out of a working
build.</p>

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
""".format(apk=APK_URL, rel=RELEASES_URL, yt=CHANNEL_URL, gh=GH_LOGO,
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
                "ROMs, sideload packages, back up kernels and pull stock ROMs over "
                "USB-OTG \u2014 no PC, no sign-in, %s." % APP["size"],
                '<article><div class="prose">%s</div></article>' % body,
                "download.html", extra_head=head,
                keywords=keywords_for(item={"tags": [
                    "download rom flasher", "rom flasher apk",
                    "rom flasher latest version", "free rom flasher tool",
                    "android rom flasher apk", "flash rom apk", "otg flasher"]}),
                image=SITE_URL + "/static/app.png")



def build_static(items):
    out = {}
    n = len(items)

    out["apps.html"] = simple("apps.html", "The Rom Flasher tool",
                              "Tool \u2014 free Android flashing app | %s" % SITE, """
<p><strong>Rom Flasher</strong> is a free Android app that flashes the
<em>other</em> phone. One phone runs the tool, a USB-OTG cable joins the two,
and the app drives fastboot, recovery and sideloading for you.</p>
<p>No PC, no Termux, and no typing commands into a black window.</p>
<h2>What it does</h2>
<ul>
<li>Flashes fastboot ROMs and custom images (<code>boot</code>,
<code>init_boot</code>, <code>super</code>, <code>vbmeta</code>)</li>
<li>Sideloads ROMs, GApps and Magisk from recovery</li>
<li>Backs up and restores IMEI / EFS and kernels, and rescues a boot-loop</li>
<li>Pulls region-wise stock ROMs without leaving the app</li>
<li>Roots with KernelSU or Magisk, debloats, and shows the real device info</li>
<li>Keeps a live command log, so a failure can be pasted into a support thread</li>
</ul>
<h2>What it is not</h2>
<ul>
<li>It cannot unlock a bootloader &mdash; only the manufacturer can do that</li>
<li>It is not a Windows program; it runs on the phone itself</li>
<li>It is free, with no sign-in and nothing to type in</li>
</ul>
<h2>Get it</h2>
<p><a class="btn" href="download.html">Download the free Rom Flasher tool</a>
<a class="btn dark" href="%s" rel="noopener">%sSource on GitHub</a>
<a class="btn yt" href="%s" rel="noopener">Videos</a>
<a class="btn gold" href="donate.html">%sBuy me a coffee</a></p>
""" % (REPO_URL, GH_LOGO, CHANNEL_URL, COFFEE_LOGO),
                              keywords=keywords_for(extra=(
                                  "rom flasher tool", "android flashing app",
                                  "flash rom app", "usb otg flasher",
                                  "app installer apk xapk", "debloater")))

    out["download.html"] = build_download()
    out["donate.html"] = build_donate()

    out["about.html"] = simple("about.html", "About", "About \u2014 %s" % SITE, """
<p>This is the written half of the <strong>Rom Flasher</strong> channel. Every
video gets a page here with the same steps in text, so nothing has to be watched
at 0.5x with a finger on pause.</p>
<h2>How these guides are written</h2>
<p>Each one is written after actually doing the job on the device named in the
title. Steps that only work on one firmware version are called out. So are the
parts that are genuinely fiddly.</p>
<h2>What is covered</h2>
<ul>
<li>Bootloader unlocking, and the waiting period that comes with it</li>
<li>Custom ROM installs, from recovery and from fastboot</li>
<li>Rooting, kernels, custom recoveries and fixing bootloops</li>
<li>Honest battery, camera and performance notes after flashing</li>
</ul>
<h2>The tool and the channel</h2>
<p><a href="download.html">The free Rom Flasher tool</a> is open source and lives
on <a href="%s" rel="noopener">GitHub</a>. New videos land on
<a href="%s" rel="noopener">YouTube</a>. %d guides so far.</p>
""" % (REPO_URL, CHANNEL_URL, n))

    out["privacy.html"] = simple("privacy.html", "Privacy Policy",
                                 "Privacy \u2014 %s" % SITE, """
<p class="dis">Last updated: %s.</p>
<h2>What this site stores</h2>
<p>Nothing. These are static files. There is no login, no comment box and no
database. Standard server logs (IP address, user agent, page requested) may be
kept by the host for security and abuse prevention.</p>
<h2>Cookies and advertising</h2>
<p>Analytics and advertising scripts do not load, and no banner is even shown,
until you say yes. If you accept, advertising may be served by third-party
vendors, including Google. Google uses cookies to serve ads based on your prior
visits to this and other websites &mdash; that is what makes an ad relevant
instead of random. Say no and the site keeps working exactly the same.</p>
<p>You can opt out of personalised advertising at
<a href="https://www.google.com/settings/ads" rel="noopener">Google Ads Settings</a>,
or opt out of third-party vendor cookies at
<a href="https://www.aboutads.info" rel="noopener">aboutads.info</a>.</p>
<h2>Affiliate links</h2>
<p>Some gear links on the download page are affiliate links. If you buy through
them, the channel earns a small commission and the price you pay does not
change. They are never the reason a recommendation exists &mdash; the cable
recommendations are the ones I use.</p>
<h2>Embedded videos</h2>
<p>Pages here embed YouTube players. Once a player loads, YouTube's own terms and
privacy policy apply, and its cookies may be set.</p>
<h2>Outbound links</h2>
<p>File downloads, forum threads and store links point to other people's servers.
This site does not control them and cannot vouch for what they host.</p>
<h2>Contact</h2>
<p>Use the <a href="contact.html">contact page</a>. Content removal requests are
honoured where the claim is valid.</p>
""" % BUILT_ON)

    out["terms.html"] = simple("terms.html", "Terms of Use", "Terms \u2014 %s" % SITE, """
<p>By reading and following anything on this site you accept the points below.</p>
<h2>Risk is yours</h2>
<p>Unlocking a bootloader, flashing a ROM, changing a recovery or writing to a
partition can wipe data, trip security features, void a warranty or leave a
device unbootable. You carry that risk, and you should not start without a
backup and a way to recover.</p>
<h2>Accuracy</h2>
<p>Guides are written from real attempts on the hardware named in them. Devices,
firmware and file layouts change without notice, and regional variants differ.
Check each step against your own unit before running it.</p>
<h2>Files and third parties</h2>
<p>Download links point to third-party hosts. This site does not own, review or
warrant those files. Verify checksums wherever they are published.</p>
<h2>No affiliation</h2>
<p>This site is not affiliated with Xiaomi, POCO, Redmi, Google, or with any ROM,
recovery or kernel project. All trademarks belong to their owners and their
licences still apply.</p>
<h2>Advertising</h2>
<p>Ads may appear on these pages. An ad is not an endorsement.</p>
""")

    out["contact.html"] = simple("contact.html", "Contact", "Contact \u2014 %s" % SITE, """
<h2>Talk to me</h2>
<p>The quickest way to reach a real person is the box below. It lands straight in
my inbox and I answer every message.</p>
%s
<h2>Or on GitHub</h2>
<p>Found a bug with a log to match? Open an issue on the
<a href="%s/issues" rel="noopener">GitHub repository</a>, so anyone hit by the
same thing can find the fix.</p>
<h2>Guide requests</h2>
<p>Name the exact model and variant. "Redmi Note 13 Pro 5G, 8/256 global" gets
picked up long before "do my phone".</p>
""" % (feedback_form(), REPO_URL))

    out["404.html"] = simple("404.html", "Page not found",
                             "Not found \u2014 %s" % SITE, """
<p>That address does not exist here. Try <a href="index.html">the home page</a>
or <a href="videos.html">the full list of guides</a>.</p>
""")
    return out


def build_feed(items):
    newest = sorted(items, key=lambda x: x.get("published") or "", reverse=True)[:40]
    entries = []
    for x in newest:
        link = "%s/rom/%s.html" % (SITE_URL, x["slug"])
        entries.append(
            "<item><title>%s</title><link>%s</link><guid>%s</guid>"
            "<pubDate>%s</pubDate><description>%s</description></item>"
            % (html.escape(x["title"]), link, link,
               x.get("published") or BUILT_ON,
               html.escape(x.get("blurb") or x["title"])))
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<rss version="2.0"><channel>\n'
            "<title>%s</title><link>%s</link><description>%s</description>\n%s\n"
            "</channel></rss>\n" % (SITE, SITE_URL, TAGLINE, "\n".join(entries)))


# ------------------------------------------------------------------- build
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

    # static/ is the single source of truth: css, icons, avatar
    for name in sorted(os.listdir(STATIC)):
        src = os.path.join(STATIC, name)
        if os.path.isfile(src):
            shutil.copy2(src, os.path.join(DIST, "static", name))

    write("index.html", build_home(items))
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

    # The app's remote feature flags. Read by Rom Flasher on every launch; see
    # RemoteConfig.kt. Kept here so the file the app fetches and the file we
    # shipped are always the same one, and so a typo is caught at build time
    # rather than silently hiding a card from everyone.
    write("app-config.json", app_config_json())

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

    newest_date = max((x.get("published") or BUILT_ON for x in items),
                      default=BUILT_ON)
    static_urls = [("", "1.0", "daily", newest_date),
                   ("videos.html", "0.9", "daily", newest_date),
                   ("brands.html", "0.6", "weekly", newest_date),
                   ("roms.html", "0.6", "weekly", newest_date),
                   ("topics.html", "0.6", "weekly", newest_date),
                   ("years.html", "0.5", "monthly", newest_date),
                   ("download.html", "0.95", "weekly", BUILT_ON),
                   ("donate.html", "0.4", "monthly", BUILT_ON),
                   ("apps.html", "0.8", "weekly", newest_date),
                   ("about.html", "0.5", "monthly", BUILT_ON),
                   ("contact.html", "0.4", "monthly", BUILT_ON),
                   ("privacy.html", "0.3", "yearly", BUILT_ON),
                   ("terms.html", "0.3", "yearly", BUILT_ON)]
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
    for kind, kind_hubs in group_hubs.items():
        cfg = HUB_KINDS[kind]
        entries.append('<url><loc>%s/%s</loc><lastmod>%s</lastmod>'
                       '<changefreq>weekly</changefreq>'
                       '<priority>0.6</priority></url>'
                       % (SITE_URL, cfg["index"], newest_date))
        entries += ['<url><loc>%s/%s/%s.html</loc><lastmod>%s</lastmod>'
                    '<changefreq>weekly</changefreq><priority>0.6</priority></url>'
                    % (SITE_URL, cfg["dir"], hub["slug"],
                       max(x.get("published") or BUILT_ON for x in hub["rows"]))
                    for hub in kind_hubs.values()]
    write("sitemap.xml",
          '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
          + "\n".join(entries) + "\n</urlset>\n")
    write("robots.txt",
          "User-agent: *\nAllow: /\n\n"
          "User-agent: Googlebot-Image\nAllow: /\n\n"
          "Sitemap: %s/sitemap.xml\n" % SITE_URL)
    write("feed.xml", build_feed(items))

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
