"""One screen that says where the romflasher.in switch-over actually stands.

    python _flip_status.py

Checks the live site, the committed CNAME, the repo variable and the Pages
settings, and prints what is done and what still needs a hand. Read-only: it
never changes anything, so it is safe to run at any point.

The one step it cannot do for you is Enforce HTTPS - the Pages API accepts the
write and drops it. Everything else here is a plain yes/no.
"""

import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

REPO = "romflasher3419-spec/romflasher-site"
DOMAIN = "romflasher.in"
GH_PAGES_IPS = {"185.199.108.153", "185.199.109.153",
                "185.199.110.153", "185.199.111.153"}

HERE = os.path.dirname(os.path.abspath(__file__))


def gh(*args):
    """Run a gh command and hand back its stdout, or None if it failed."""
    try:
        out = subprocess.run(["gh", *args], capture_output=True, text=True,
                             timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    return out.stdout.strip()


def get(url, timeout=25):
    """Fetch a URL and return (status, body). Never raises."""
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "flip-status"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8", "replace")
        except Exception:
            pass
        return e.code, body
    except Exception as e:                       # DNS, TLS, timeout
        return None, str(e)


def main():
    ok, todo = [], []

    # ---------------------------------------------------------- 1. the live site
    status, body = get("https://%s/" % DOMAIN)
    if status == 200 and "Rom Flasher" in body:
        ok.append("https://%s/ answers with the site" % DOMAIN)
    else:
        todo.append("https://%s/ did not answer (status %s)" % (DOMAIN, status))

    # --------------------------------------------- 2. the site calls itself .in
    status, body = get("https://%s/sitemap.xml" % DOMAIN)
    if status == 200 and ("https://%s/" % DOMAIN) in body:
        n = body.count("<loc>")
        ok.append("sitemap is live, %d URLs, all on %s" % (n, DOMAIN))
    else:
        todo.append("sitemap.xml not readable on %s (status %s)" % (DOMAIN, status))

    # ------------------------------------------------- 3. committed dist/CNAME
    cname = os.path.join(HERE, "dist", "CNAME")
    if os.path.exists(cname):
        with open(cname, encoding="utf-8") as fh:
            got = fh.read().strip()
        if got == DOMAIN:
            ok.append("dist/CNAME is %s" % got)
        else:
            todo.append("dist/CNAME says %r, expected %r" % (got, DOMAIN))
    else:
        todo.append("dist/CNAME is missing - rebuild with ROMFLASHER_DOMAIN set")

    # ------------------------------------------------------ 4. repo variable
    out = gh("variable", "list", "--repo", REPO, "--json", "name,value")
    if out is not None:
        try:
            vars_ = {v["name"]: v["value"] for v in json.loads(out)}
        except (ValueError, KeyError):
            vars_ = {}
        if vars_.get("ROMFLASHER_DOMAIN") == DOMAIN:
            ok.append("repo variable ROMFLASHER_DOMAIN = %s" % DOMAIN)
        else:
            todo.append("repo variable ROMFLASHER_DOMAIN is not %s" % DOMAIN)

        slots = [k for k in ("ROMFLASHER_SLOT_ARTICLE", "ROMFLASHER_SLOT_LIST",
                             "ROMFLASHER_SLOT_HUB") if vars_.get(k)]
        if vars_.get("ROMFLASHER_ADS") and slots:
            ok.append("ads on: publisher + %d slot(s) set" % len(slots))
        else:
            todo.append("ads off (needs ROMFLASHER_ADS + a slot id)")
    else:
        todo.append("could not read repo variables (is gh signed in?)")

    # ---------------------------------------------------------- 5. Pages state
    out = gh("api", "repos/%s/pages" % REPO)
    if out is not None:
        try:
            pages = json.loads(out)
        except ValueError:
            pages = {}
        if pages.get("cname") == DOMAIN:
            ok.append("Pages custom domain = %s" % DOMAIN)
        else:
            todo.append("Pages custom domain is %r" % pages.get("cname"))
        if pages.get("https_enforced"):
            ok.append("Enforce HTTPS is on")
        else:
            todo.append("Enforce HTTPS is OFF -> tick it in Settings -> Pages "
                        "(the API accepts the write and drops it)")
    else:
        todo.append("could not read Pages settings")

    # ----------------------------------------------------- 6. app source line
    app = os.path.join(os.path.expanduser("~"), "Documents", "ROM_Flasher_Tool",
                       "app", "src", "main", "java", "com", "romflasher", "tool",
                       "ui", "SiteLink.kt")
    if os.path.exists(app):
        with open(app, encoding="utf-8") as fh:
            src = fh.read()
        line = [l.strip() for l in src.splitlines()
                if l.strip().startswith("const val SITE_URL")]
        if line and ("https://%s/" % DOMAIN) in line[0]:
            ok.append("app SiteLink.kt points at %s (source is private, so "
                      "this needs a rebuild + release by hand)" % DOMAIN)
        else:
            todo.append("app SiteLink.kt still points elsewhere: %s"
                        % (line[0] if line else "not found"))

    # ------------------------------------------------------------------ report
    print("romflasher.in - switch-over status")
    print("-" * 46)
    for line in ok:
        print("  OK    %s" % line)
    if todo:
        print("")
        for line in todo:
            print("  TODO  %s" % line)
    print("")
    print("%d done, %d to do" % (len(ok), len(todo)))
    return 0 if not todo else 1


if __name__ == "__main__":
    sys.exit(main())
