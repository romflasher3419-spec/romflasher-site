"""Is the domain really pointing at GitHub Pages yet?

Run this BEFORE flipping the site to the custom domain. Writing a CNAME into
the repo while the DNS still answers somewhere else (or nowhere at all) makes
Pages redirect the working github.io address to a domain that does not reply,
and the site goes dark for everyone until the DNS catches up.

    python _dnscheck.py romflasher.in

Exit code 0 means the apex resolves to GitHub Pages and it is safe to set
ROMFLASHER_DOMAIN. Exit code 1 means wait - and the output says what to fix.
"""

import re
import socket
import subprocess
import sys

PAGES_HOST = "romflasher3419-spec.github.io"

# GitHub Pages' documented addresses for a custom apex domain. We ask GitHub's
# own host for its live addresses too, so a change on their side shows up here
# instead of silently failing later.
GH_IPV4 = ("185.199.108.153", "185.199.109.153",
           "185.199.110.153", "185.199.111.153")
GH_IPV6 = ("2606:50c0:8000::153", "2606:50c0:8001::153",
           "2606:50c0:8002::153", "2606:50c0:8003::153")


def resolve(host):
    """Every address a name resolves to, or [] when it resolves to nothing."""
    try:
        infos = socket.getaddrinfo(host, None)
    except (socket.gaierror, UnicodeError, OSError):
        return []
    seen = []
    for info in infos:
        ip = info[4][0]
        if ip not in seen:
            seen.append(ip)
    return seen


def split(addrs):
    v4 = sorted(a for a in addrs if ":" not in a)
    v6 = sorted(a for a in addrs if ":" in a)
    return v4, v6


def cname_of(host):
    """The CNAME target of a name, when the local resolver will tell us."""
    for cmd in (["nslookup", "-type=CNAME", host],
                ["dig", "+short", "CNAME", host]):
        try:
            out = subprocess.run(cmd, capture_output=True, text=True, timeout=20)
        except (OSError, subprocess.SubprocessError):
            continue
        text = out.stdout or ""
        for line in text.splitlines():
            m = re.search(r"canonical name\s*=\s*(\S+)", line, re.I)
            if m:
                return m.group(1).rstrip(".")
        m = re.search(r"^(\S+\.)\s*$", text.strip(), re.M)
        if m and m.group(1).rstrip(".").lower() != host.lower():
            return m.group(1).rstrip(".")
    return ""


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip())
        return 2
    domain = argv[1].strip().lower().lstrip(".").split("/")[0]
    www = "www." + domain

    print("Checking %s against GitHub Pages (%s)" % (domain, PAGES_HOST))
    print("-" * 62)

    live = resolve(PAGES_HOST)
    live_v4, live_v6 = split(live)
    known_v4 = set(live_v4) or set(GH_IPV4)
    known_v6 = set(live_v6) or set(GH_IPV6)
    print("GitHub Pages answers on : %s" % (", ".join(live_v4) or "?"))

    apex = resolve(domain)
    apex_v4, apex_v6 = split(apex)
    print("")
    print("apex  %-24s : %s" % (domain, ", ".join(apex_v4) or "does not resolve"))
    if apex_v6:
        print("apex  %-24s : %s (IPv6)" % ("", ", ".join(apex_v6)))

    if not apex:
        print("")
        print("NOT READY - the domain does not answer yet.")
        print("Add the records at your registrar, then run this again:")
        print("")
        for ip in GH_IPV4:
            print("    A      @      %s" % ip)
        for ip in GH_IPV6:
            print("    AAAA   @      %s" % ip)
        print("    CNAME  www    %s" % PAGES_HOST)
        return 1

    foreign_v4 = [ip for ip in apex_v4 if ip not in known_v4]
    foreign_v6 = [ip for ip in apex_v6 if ip not in known_v6]
    missing_v4 = [ip for ip in sorted(known_v4) if ip not in apex_v4]

    www_target = cname_of(www)
    if www_target:
        print("www   %-24s : CNAME -> %s" % (www, www_target))
    else:
        www_addrs = resolve(www)
        print("www   %-24s : %s" % (www, ", ".join(sorted(www_addrs)) or "does not resolve"))

    print("")
    problems = []
    if foreign_v4 or foreign_v6:
        problems.append("the apex also points somewhere else: %s"
                        % ", ".join(foreign_v4 + foreign_v6))
    if missing_v4:
        problems.append("missing A record(s): %s" % ", ".join(missing_v4))
    if www_target and www_target.lower() not in (PAGES_HOST, www, domain):
        problems.append("www points at %s, not %s" % (www_target, PAGES_HOST))

    if problems:
        print("NOT READY")
        for p in problems:
            print("  - " + p)
        print("")
        print("Fix those at the registrar, wait for the change to spread")
        print("(minutes, sometimes an hour), then run this again.")
        return 1

    print("READY - %s resolves to GitHub Pages." % domain)
    if missing_v4:
        print("  (some A records are still missing, but the ones in place are right)")
    print("")
    print("Safe to go ahead, in this order:")
    print("  1. GitHub -> Settings -> Pages -> Custom domain -> %s" % domain)
    print("  2. wait for the DNS check to pass, then tick Enforce HTTPS")
    print("  3. GitHub -> Settings -> Secrets and variables -> Actions -> Variables")
    print("       add ROMFLASHER_DOMAIN = %s" % domain)
    print("  4. push anything to main (or re-run the workflow) to rebuild")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main(sys.argv))
    except KeyboardInterrupt:
        raise SystemExit(130)
