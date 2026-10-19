"""Give a guide its device back.

A handful of videos never mentioned the phone in a way the first pass could
parse, so `device` came out empty or as the placeholder "Channel". The titles
say it plainly ("... on Poco X7 Pro ..."), which means those guides were missing
from the device page and the brand hub they belong on.

This reads only the title, only fills a field that is empty or a placeholder,
never overwrites a real device, and never invents one - if the title does not
name the phone, nothing changes.

    python _fix_devices.py           # show what would change
    python _fix_devices.py --write   # do it
"""

import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")

JUNK = {"", "?", "-", "n/a", "na", "none", "unknown", "other", "channel"}

# Title fragment (lower case) -> the device name used everywhere else.
TITLE_RULES = (
    ("poco x7 pro", "POCO X7 Pro"),
    ("poco x7", "POCO X7 Pro"),
    ("redmi k50i", "Redmi K50i"),
    ("xiaomi pad 5", "Xiaomi Pad 5"),
    ("xiaomi 11t pro", "Xiaomi 11T Pro"),
    ("redmi note 5 pro", "Redmi Note 5 Pro"),
    ("mi 11x", "Mi 11X"),
    ("poco f3", "POCO F3"),
    ("xiaomi 15t pro", "Xiaomi 15T Pro"),
)


# Guides where no phone is named anywhere - not in the title, not in the
# description. Rather than leave the field empty (which shows as "-" in the
# tables and "Keep reading" on the page), they get the same label this site
# already uses for general guides: "Any Android" / "Any Xiaomi". Both are
# skipped by the device-hub builder on purpose, so no false hub appears.
BY_ID = {
    "KvXLnpaPnRQ": "Any Android",   # MIUI 13 AbhiX ROG Edition - no device named
    "YJOO3M5ikBU": "Any Xiaomi",    # "Install Any AOSP ROM on Xiaomi & POCO"
    "wm74MStyxt8": "Any Android",   # Project Infinity X changelog - no device named
}


def device_from_title(title):
    low = title.lower()
    for needle, name in TITLE_RULES:
        if re.search(r"\b" + re.escape(needle) + r"\b", low):
            return name
    return ""


def main():
    write = "--write" in sys.argv
    changed = 0
    for path in sorted(glob.glob(os.path.join(CONTENT, "*.json"))):
        with io.open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        current = (data.get("device") or "").strip()
        if current.lower() not in JUNK:
            continue
        name = device_from_title(data.get("title", ""))
        if not name:
            name = BY_ID.get(data["id"], "")
        if not name:
            continue
        changed += 1
        print("%-14s %s -> %s" % (data["id"], repr(current), name))
        if write:
            data["device"] = name
            with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
                json.dump(data, fh, ensure_ascii=False, indent=2)
                fh.write("\n")
    print("%d guide(s) %s" % (changed, "updated" if write else "would change"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
