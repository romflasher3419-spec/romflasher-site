# Rom Flasher — the site

The written half of the **Rom Flasher** YouTube channel. Every video on the
channel gets one page here with the same steps in text, its real description,
its download links and the questions people actually ask.

**Live:** https://romflasher3419-spec.github.io/romflasher-site/
**Repo:** https://github.com/romflasher3419-spec/romflasher-site

| | |
|---|---|
| Pages built | 236 (184 guides + device, brand, ROM, year and topic hubs) |
| Home page | `index.html` |
| Guide list | `videos.html` (search, filter, sort, dates) |
| Tool page | `download.html` — the direct APK button |
| Generator | `build.py` (Python standard library only) |
| Output | `dist/` — never edited by hand |

---

## Where things live

```
content/<videoId>.json   one guide: title, device, rom, description, links,
                         views, tags, and the written summary/body/faq
drafts/<videoId>.md      the article as it was handed in (::summary ::body ::faq)
waves/wave_NN.txt        the video IDs handed out per writing batch
static/                  style.css, the app icon, favicon, channel art
build.py                 builds every page from content/
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

### Going live on romflasher.in

The site only moves once the domain's DNS answers, and each step below makes the
next one safe. Skipping ahead - especially writing the CNAME early - takes the
working site offline.

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
   CNAME  www    romflasher3419-spec.github.io
   ```

   The apex goes to GitHub's four addresses, **not** to a CNAME of the
   `github.io` host - an apex CNAME breaks the mail and any other records on the
   same name.
3. **Wait, then check.** DNS spreads in minutes, but a slow resolver can take an
   hour.

   ```powershell
   python _dnscheck.py romflasher.in
   ```

   It lists whatever is still missing, then prints `READY` and exits 0 when the
   domain truly answers from GitHub Pages.
4. **Register the domain with Pages** - GitHub → **Settings → Pages → Custom
   domain** → `romflasher.in` → **Save**. Wait for *DNS check successful*, then
   tick **Enforce HTTPS**. The certificate is only issued at this point, so
   HTTPS failing before here is normal, not a fault.
5. **Switch the site over** - GitHub → **Settings → Secrets and variables →
   Actions → Variables → New variable**:

   ```
   ROMFLASHER_DOMAIN = romflasher.in
   ```

   Then push anything (or re-run *Build and publish the site*). That single
   variable writes `dist/CNAME` and points every canonical URL, sitemap entry
   and structured-data `url` at the new home. Nothing else needs editing.
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
| `ROMFLASHER_AMAZON` | adds your Associates tag to the gear links |
| `ROMFLASHER_GOOGLE` | Search Console verification meta tag |
| `ROMFLASHER_BING` | Bing Webmaster verification meta tag |

Analytics and ads are loaded by a small consent gate: nothing is fetched, no
cookie is set and no banner is shown until the visitor accepts. Decline and the
site behaves exactly the same.

`ads.txt` is only written when `ROMFLASHER_ADS` is set — a wrong `ads.txt` on a
real AdSense site is worse than no file at all.

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
