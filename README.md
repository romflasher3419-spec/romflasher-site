# Rom Flasher — the site

The written half of the **Rom Flasher** YouTube channel. Every video on the
channel gets one page here with the same steps in text, its real description,
its download links and the questions people actually ask.

**Live:** https://romflasher.in/
**Repo:** https://github.com/romflasher3419-spec/romflasher-site

| | |
|---|---|
| Pages built | 237 (184 guides + device, brand, ROM, year and topic hubs) |
| Home page | `index.html` (full width; the ad rail appears only when an ad is on) |
| Guide list | `videos.html` (search, filter, sort, dates) |
| ROM downloader | `downloader.html` (search a phone, change region, one-click ROM) |
| Tool page | `download.html` — the direct APK button |
| Generator | `build.py` (Python standard library only) |
| ROM index | `data/firmware.json` (built by `fetch_firmware.py`) |
| Output | `dist/` — never edited by hand |

---

## Where things live

```
content/<videoId>.json   one guide: title, device, rom, description, links,
                         views, tags, and the written summary/body/faq
drafts/<videoId>.md      the article as it was handed in (::summary ::body ::faq)
waves/wave_NN.txt        the video IDs handed out per writing batch
static/                  style.css, the app icon, favicon, channel art
data/firmware.json       the ROM index the downloader page reads (458 phones)
data/catalog.json        the same list, trimmed, for reference
build.py                 builds every page from content/
fetch_firmware.py        rebuilds data/firmware.json from the public firmware
                         trackers - run it, then commit the result
set_article.py           merges a draft into content/<id>.json
_seocheck.py             structured data + SEO head check
qa.py                    page / summary / link checks  (qa.py --links)
make_qr.py               regenerates static/upi-qr.png from the app's payload
make_icons.py            regenerates the PWA / Apple touch icons from app.png
make_waves.py            rebuilds the wave files + prints progress
_progress.py             how many guides are written, per wave
_audit.py                independent read-only audit of every written guide
_fix_devices.py          gives a guide its device back from the title
WRITER.md                the binding writing rules for every article
```

## Build it

```powershell
C:\Python315\python.exe build.py            # -> dist/
C:\Python315\python.exe build.py --serve    # preview on :8080
C:\Python315\python.exe _seocheck.py        # structured data, canonicals, meta
C:\Python315\python.exe qa.py --links       # every internal link
```

## The ROM downloader

`downloader.html` never hosts a firmware file. It reads an index of every
phone, every region and every Recovery / Fastboot build that the public
trackers know, with the **direct** download link for each one - and the
download button goes straight to the file, with no page of ours in front of it.

```powershell
C:\Python315\python.exe fetch_firmware.py                 # refresh the whole index
C:\Python315\python.exe fetch_firmware.py --brand poco    # one brand (preview file)
C:\Python315\python.exe fetch_firmware.py --slug poco-f5  # one phone (preview file)
C:\Python315\python.exe fetch_firmware.py --list          # what is in the index
C:\Python315\python.exe fetch_firmware.py --no-mirrors    # skip the mirror check
```

A filtered run (`--brand`, `--slug`, `--limit`) writes a preview file beside
the index instead of overwriting it, so the full index and the names in it
always survive.

### Where the data comes from

| Source | What it gives |
|---|---|
| `XiaomiFirmwareUpdater/miui-updates-tracker` - `data/latest.yml` | every Recovery and Fastboot build, with Xiaomi's own CDN link, the region and the release date |
| `XiaomiFirmwareUpdater/miui-updates-tracker` - `data/devices.yml` | the device names behind each codename |
| `xmfirmwareupdater.com/data/devices/latest.yml` | a second pair of mirrors (GitHub and OSDN) for the Recovery ROM |
| `xmfirmwareupdater.com/data/firmware_devices.yml` | the pretty name of each codename |

All four are public files with `Access-Control-Allow-Origin: *` and no key, so
the index can be built anywhere - including the refresh workflow on GitHub.

The names, the brands and the model numbers that were worked out by hand are
kept in the index that is already in the repo: the script reads the previous
`data/firmware.json`, matches it by codename and only replaces the links. That
is why the same phone keeps its page slug from one refresh to the next.

### The mirrors

Every build gets a list of mirrors next to its own link:

1. Xiaomi's own CDN (`bigota.d.miui.com` / `cdn.cnbj1.fds.api.mi-img.com`),
2. the Singapore copy on the public Aliyun bucket,
3. GitHub and OSDN, where the second index has the same build.

The Aliyun copy is **checked with a HEAD request while the index is built**, and
only the ones that really hold the file are written in. That matters: a mirror
that is missing would answer faster than a good one and win the race in the
browser, and the download would break.

On the page: type a brand ("poco"), tap the phone from the scroll list, hit
**Change region** to narrow it to one region, then press **Recovery ROM** or
**Fastboot ROM**. The button races every link with a short HEAD request and
opens the first one that answers, so the download starts from the quickest
server - and the file itself comes straight from that server. Magisk and
KernelSU are fetched live from GitHub the same way.

Keep the index fresh by running `fetch_firmware.py` and committing the new
`data/firmware.json` - the workflow only rebuilds `dist/`.

## Write one article

```powershell
C:\Python315\python.exe set_article.py "--id=<videoId>" "--file=drafts/<videoId>.md"
C:\Python315\python.exe set_article.py --missing     # what is still empty
C:\Python315\python.exe make_waves.py --status       # batch progress
C:\Python315\python.exe _progress.py                 # totals + per-wave table
```

The draft format is three sections — `::summary`, `::body`, `::faq` — and the
rules (English only, lengths, the banned word list, never invent a link) are in
`WRITER.md`. The checker refuses anything that breaks them.

## Deploy

Nothing is uploaded by hand. **Push to `main` and
[`.github/workflows/deploy.yml`](.github/workflows/deploy.yml) rebuilds `dist/`
and publishes it to GitHub Pages.** The workflow runs `_seocheck.py` and
`qa.py --links`, so a broken build never goes live.

### Going live on romflasher.in — DONE

> **Status: live.** `romflasher.in` is registered at Hostinger (DNS served by
> `horizon/orbit.dns-parking.com`), the nine records below are in place, the
> custom domain is set on Pages, and the repo variable `ROMFLASHER_DOMAIN` is
> `romflasher.in`. The site answers on **https://romflasher.in/** and every
> canonical, sitemap and structured-data URL points there.
>
> The steps are kept here because the same order is what makes a domain move
> safe: DNS first, then Pages, then the variable that rewrites the URLs, then
> the app. Skipping ahead - especially writing the CNAME early - takes the
> working site offline.

1. **Buy `romflasher.in`** at a registrar that takes UPI (Hostinger, GoDaddy
   India, BigRock and Namecheap all sell `.in`). Turn auto-renew on.
2. **Add the DNS records** in that registrar's DNS zone editor:

   ```
   A      @      185.199.108.153
   A      @      185.199.109.153
   A      @      185.199.110.153
   A      @      185.199.111.153
   AAAA   @      2606:50c0:8000::153
   AAAA   @      2606:50c0:8001::153
   AAAA   @      2606:50c0:8002::153
   AAAA   @      2606:50c0:8003::153
   CNAME  www    romflasher.in
   ```

   The apex goes to GitHub's four addresses, **not** to a CNAME of the
   `github.io` host - an apex CNAME breaks the mail and any other records on the
   same name. (A `www` CNAME of `romflasher3419-spec.github.io` also works, and
   is what GitHub's own docs show; the apex must still be the four A records.)
   On Hostinger the parking record is an `A` for `@` pointing at `2.57.91.91` -
   that one has to be edited, not left alongside the new four, or half the
   visitors land on the parking page. TTL must be 60-86400 there; `0` is
   rejected.
3. **Wait, then check.** DNS spreads in minutes, but a slow resolver can take an
   hour.

   ```powershell
   python _dnscheck.py romflasher.in
   ```

   It lists whatever is still missing, then prints `READY` and exits 0 when the
   domain truly answers from GitHub Pages.
   `python _flip_status.py` is the read-only counterpart: one screen saying which
   of these seven steps are actually done, and which still need a hand. It never
   changes anything, so it is safe to run at any point.
4. **Register the domain with Pages** - GitHub → **Settings → Pages → Custom
   domain** → `romflasher.in` → **Save**. Wait for *DNS check successful*, then
   tick **Enforce HTTPS**. The certificate is only issued at this point, so
   HTTPS failing before here is normal, not a fault. Both can be done from the
   CLI instead (the endpoint is `PUT`, not `PATCH`, and the body field is
   `https_enforcement`, while the response calls it `https_enforced`):

   ```powershell
   gh api -X PUT repos/romflasher3419-spec/romflasher-site/pages `
     -F cname=romflasher.in -F https_enforcement=true
   gh api repos/romflasher3419-spec/romflasher-site/pages/health   # DNS verdict
   ```
5. **Switch the site over** - GitHub → **Settings → Secrets and variables →
   Actions → Variables → New variable**:

   ```
   ROMFLASHER_DOMAIN = romflasher.in
   ```

   Then push anything (or re-run *Build and publish the site*). That single
   variable writes `dist/CNAME` and points every canonical URL, sitemap entry
   and structured-data `url` at the new home. Nothing else needs editing. From
   the CLI: `gh variable set ROMFLASHER_DOMAIN --body romflasher.in`, then
   `gh workflow run deploy.yml`.
6. **Tell the app** - one line in the tool repo, at
   `app/src/main/java/com/romflasher/tool/ui/SiteLink.kt`:

   ```kotlin
   const val SITE_URL = "https://romflasher.in/"
   ```

   Rebuild and publish the app so the footer pill opens the new address.
7. **Search Console** - add `romflasher.in` as a property, verify with
   `ROMFLASHER_GOOGLE`, and submit `https://romflasher.in/sitemap.xml`.

> The old `github.io/romflasher-site` address keeps working: Pages redirects it
> to the custom domain. Every link in the site is relative, so the move to a
> domain root is clean - no page has to be rewritten.

## Switches (all off until you fill them in)

Everything below is read from the environment, so the site never ships
half-configured. Set them in `.github/workflows/deploy.yml` (or as repo
variables: *Settings → Secrets and variables → Actions → Variables*).

| Variable | What it turns on |
|---|---|
| `ROMFLASHER_DOMAIN` | the custom domain: writes `dist/CNAME` **and** the canonical URLs |
| `ROMFLASHER_SITE_URL` | overrides just the URLs, when they differ from the domain |
| `ROMFLASHER_GA4` | Google Analytics 4 — **only after the visitor says yes** |
| `ROMFLASHER_ADS` | AdSense: the loader **and** a correct `ads.txt` |
| `ROMFLASHER_SLOT_ARTICLE` | ad unit at the end of every guide article |
| `ROMFLASHER_SLOT_LIST` | ad unit under the guides table |
| `ROMFLASHER_SLOT_HUB` | ad unit on the home page and the hub pages |
| `ROMFLASHER_AMAZON` | adds your Associates tag to the gear links |
| `ROMFLASHER_GOOGLE` | Search Console verification meta tag |
| `ROMFLASHER_BING` | Bing Webmaster verification meta tag |

Analytics and ads are loaded by a small consent gate: nothing is fetched, no
cookie is set and no banner is shown until the visitor accepts. Decline and the
site behaves exactly the same.

`ads.txt` is only written when `ROMFLASHER_ADS` is set — a wrong `ads.txt` on a
real AdSense site is worse than no file at all.

### Ad placements

The three `ROMFLASHER_SLOT_*` values are the numeric unit ids AdSense shows next
to each ad unit you create (Ads → By ad unit → the id in the snippet). Each unit
is off on its own, and all of them stay off while `ROMFLASHER_ADS` is empty, so
a half-set-up account cannot publish units that 404.

```powershell
gh variable set ROMFLASHER_ADS          --body "pub-0000000000000000"
gh variable set ROMFLASHER_SLOT_ARTICLE --body "1234567890"
gh variable set ROMFLASHER_SLOT_LIST    --body "1234567891"
gh variable set ROMFLASHER_SLOT_HUB     --body "1234567892"
gh workflow run deploy.yml
```

The markup is Google's own snippet, unchanged, because the queue push is what
fills the box. That push only writes into a plain array — before
`adsbygoogle.js` loads there is no request, no cookie and no Google script on the
page, and the consent gate only loads that script after the visitor accepts.
Decline and each `<ins>` is an empty zero-height block, so no gap is left where
an ad would have been. With the switches empty, no wrapper is emitted at all.

## Search engines

1. **Google Search Console** → add the property, copy the `content="…"` value
   from the HTML tag it gives you into `ROMFLASHER_GOOGLE`, push.
2. **Bing Webmaster Tools** → same thing into `ROMFLASHER_BING`.
3. Submit `sitemap.xml` in both (239 URLs, real `lastmod` dates per page).
4. Ask for indexing of `index.html`, `videos.html` and `download.html` once.

## What the pages carry for search

* `Article` + `VideoObject` (with the video's real description as `transcript`)
  + `FAQPage` + `BreadcrumbList` on every guide.
* `HowTo` with real `HowToStep`s on every guide that has numbered steps.
* `speakable` so assistant-style search can read the summary out loud.
* `CollectionPage` + `ItemList` on every device / brand / ROM / year / topic hub.
* `SoftwareApplication` + `Offer` on the tool page.
* Real `dateModified` per guide (the content file's date, not "today" every day).
* Per-guide `og:image` from that video's own thumbnail.

## Donations

The UPI ID, the PayPal link and the QR payload are copied from the app's own
`DonateDialog.kt`, so the site and the app take you to the same two places.
`make_qr.py` regenerates `static/upi-qr.png` if they ever change.

## Keep in sync with the app

* App repo: https://github.com/romflasher3419-spec/rom-flasher-tool
* The app's footer has a **Guides & website** pill (`SiteLink.kt`) that opens
  this site. One constant to change when the domain moves.
* The app README links here too.
