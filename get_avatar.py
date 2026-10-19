"""Fetch the channel avatar into static/ so the site can show it next to titles.

    python get_avatar.py                  # tries the known channel avatar
    python get_avatar.py --handle @X      # some other channel

Writes static/channel.jpg (or static/channel.svg as a fallback), which build.py
copies into dist/static/.
"""

import argparse
import os
import re
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "static")
HANDLE = "@Rom_Flasher"

HEADERS = {
    "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                   "AppleWebKit/537.36 (KHTML, like Gecko) "
                   "Chrome/124.0.0.0 Safari/537.36"),
    "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.youtube.com/",
}

# Found on https://www.youtube.com/@Rom_Flasher (the identifier part is stable)
KNOWN = ("https://yt3.ggpht.com/"
         "jDERtZJulSTIVkw7XKsdLxpQGhntBj9RJqZ25RQIp2D7AF61hj96d3AvIjlG5sH1sp-c7nR5IiXF")


def via_urllib(url):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=25) as resp:
        return resp.read()


def via_curl(url):
    tmp = os.path.join(OUT_DIR, "_avatar.tmp")
    proc = subprocess.run(
        ["curl.exe", "-sSL", "--max-time", "25", "-o", tmp,
         "-H", "User-Agent: " + HEADERS["User-Agent"],
         "-H", "Referer: https://www.youtube.com/", url],
        capture_output=True, text=True)
    if proc.returncode == 0 and os.path.exists(tmp):
        with open(tmp, "rb") as fh:
            blob = fh.read()
        os.remove(tmp)
        return blob
    raise OSError((proc.stderr or "curl failed").strip()[:120])


def looks_like_image(blob):
    return len(blob) > 1500 and (blob[:3] == b"\xff\xd8\xff"
                                 or blob[:4] == b"\x89PNG"
                                 or blob[:4] == b"RIFF"
                                 or blob[:6] in (b"GIF87a", b"GIF89a"))


def candidates(url):
    out = [url]
    if "yt3.ggpht.com" in url:
        out.append(url.replace("yt3.ggpht.com", "yt3.googleusercontent.com"))
    return out


def scrape_handle(handle):
    """Read the channel page and pull the newest avatar URL out of it."""
    page = via_urllib("https://www.youtube.com/%s" % handle).decode("utf-8", "replace")
    found = re.findall(r"https://yt3\.ggpht\.com/[A-Za-z0-9_\-/=.]+", page)
    if not found:
        return []
    found = sorted(set(re.sub(r"=(s|w)\d+.*$", "", u) for u in found),
                   key=len, reverse=True)
    return [u + "=s176-c-k-c0x00ffffff-no-rj" for u in found[:3]]


def write_fallback(reason):
    os.makedirs(OUT_DIR, exist_ok=True)
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" '
           'width="96" height="96">\n'
           '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
           '<stop offset="0" stop-color="#ff6b35"/>'
           '<stop offset="1" stop-color="#ff2d55"/></linearGradient></defs>\n'
           '<rect width="96" height="96" rx="48" fill="url(#g)"/>\n'
           '<text x="48" y="62" font-family="Segoe UI,Arial,sans-serif" font-size="34" '
           'fill="#ffffff" font-weight="700" text-anchor="middle">RF</text>\n'
           "</svg>\n")
    path = os.path.join(OUT_DIR, "channel.svg")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(svg)
    print("[!] no avatar downloaded (%s)" % reason)
    print("    using generated %s" % path)
    return path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--handle", default=HANDLE)
    args = ap.parse_args()
    os.makedirs(OUT_DIR, exist_ok=True)

    urls = []
    try:
        urls += scrape_handle(args.handle)
    except Exception as exc:                                       # noqa: BLE001
        print("[i] channel page scrape failed: %s" % str(exc)[:100])
    urls += candidates(KNOWN + "=s176-c-k-c0x00ffffff-no-rj")

    errors = []
    for url in urls:
        for name, fn in (("urllib", via_urllib), ("curl", via_curl)):
            try:
                blob = fn(url)
                if looks_like_image(blob):
                    path = os.path.join(OUT_DIR, "channel.jpg")
                    with open(path, "wb") as fh:
                        fh.write(blob)
                    print("[OK] %s bytes via %s" % (len(blob), name))
                    print("     %s" % path)
                    return 0
                errors.append("%s/%s: not an image (%d bytes)" % (name, url[:40], len(blob)))
            except Exception as exc:                               # noqa: BLE001
                errors.append("%s/%s: %s" % (name, url[:40], str(exc)[:80]))
        if len(errors) > 6:
            break

    for e in errors[:6]:
        print("    x", e)
    write_fallback("all hosts refused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
