"""Tell Bing (and the other IndexNow engines) that the site changed.

IndexNow is the opposite of waiting to be crawled: you hand the engines the
URLs you just published and they queue them straight away. One POST reaches
Bing, Yandex, Seznam and Naver because they share the same endpoint.

    python _indexnow.py                # every URL in the sitemap
    python _indexnow.py <url> [url..]  # just these

The key has to be readable first, so this only works once the build that
wrote <key>.txt has been deployed and is live:

    https://romflasher.in/<key>.txt   ->   <key>

Exit code 0 means the engines accepted the submission. 200 or 202 both count.
"""

import json
import os
import sys
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(HERE, "dist")

SITE_URL = "https://romflasher.in"
ENDPOINT = "https://api.indexnow.org/indexnow"
KEY = os.environ.get("ROMFLASHER_INDEXNOW", "").strip()
HOST = SITE_URL.split("//", 1)[1]


def sitemap_urls():
    path = os.path.join(DIST, "sitemap.xml")
    if not os.path.isfile(path):
        sys.exit("[X] dist/sitemap.xml is missing - run build.py first")
    with open(path, encoding="utf-8") as fh:
        body = fh.read()
    urls = []
    marker = "<loc>"
    while True:
        i = body.find(marker)
        if i < 0:
            break
        body = body[i + len(marker):]
        j = body.find("</loc>")
        if j < 0:
            break
        urls.append(body[:j])
    return urls


def check_key_live():
    """The engines fetch <key>.txt before trusting the submission."""
    probe = "%s/%s.txt" % (SITE_URL, KEY)
    try:
        with urllib.request.urlopen(probe, timeout=20) as r:
            served = r.read().decode("utf-8").strip()
    except urllib.error.HTTPError as e:
        sys.exit("[X] %s answered %s - deploy the build that writes it first"
                 % (probe, e.code))
    except Exception as e:
        sys.exit("[X] could not reach %s (%s)" % (probe, e))
    if served != KEY:
        sys.exit("[X] %s contains %r, expected %r" % (probe, served, KEY))
    print("[OK] %s serves the key" % probe)


def submit(urls):
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": "%s/%s.txt" % (SITE_URL, KEY),
        "urlList": urls,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        ENDPOINT, data=data,
        headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code


# One request carries at most 10,000 URLs, but a batch that big from a host the
# engine has never seen is often answered 403. Sending them in small groups is
# both within the spec and accepted in practice.
BATCH = 100


def main():
    if not KEY:
        sys.exit("[X] ROMFLASHER_INDEXNOW is not set")
    args = [a for a in sys.argv[1:] if a.strip()]
    if args:
        urls = [a if a.startswith("http") else "%s/%s" % (SITE_URL, a.lstrip("/"))
                for a in args]
    else:
        urls = sitemap_urls()
    if not urls:
        sys.exit("[X] nothing to submit")

    check_key_live()
    print("     submitting %d url(s) to %s" % (len(urls), ENDPOINT))
    ok = 0
    bad = []
    for i in range(0, len(urls), BATCH):
        chunk = urls[i:i + BATCH]
        status = submit(chunk)
        if status in (200, 202):
            ok += len(chunk)
        else:
            bad.append((status, i // BATCH + 1))
        print("     batch %d/%d (%d urls) -> %s"
              % (i // BATCH + 1, (len(urls) + BATCH - 1) // BATCH,
                 len(chunk), status))

    if not bad:
        print("[OK] IndexNow accepted all %d url(s)" % ok)
        return 0
    print("[!] %d url(s) accepted, %d batch(es) refused: %s"
          % (ok, len(bad), ", ".join("#%d->%s" % (b, s) for s, b in bad)))
    for status, _ in bad:
        if status == 400:
            print("    400 - the payload was malformed")
        elif status == 403:
            print("    403 - the key file did not match")
        elif status == 422:
            print("    422 - the URLs belong to another host, or the key is invalid")
        elif status == 429:
            print("    429 - too many submissions, wait and retry")
    return 1


if __name__ == "__main__":
    sys.exit(main())
