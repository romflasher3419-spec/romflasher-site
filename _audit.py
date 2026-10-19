"""Independent read-only audit of every written guide.

The writers each self-check with set_article.py, but that is the same code that
accepted the draft. This is the second pair of eyes: it never writes anything, it
just reads all 184 content files and complains if one of them drifted.

    python _audit.py
"""

import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")

# Devanagari, Gurmukhi, Bengali, Tamil, Telugu, Kannada, Malayalam, Arabic.
SCRIPTS = re.compile("[\u0900-\u097f\u0a00-\u0a7f\u0980-\u09ff\u0b80-\u0bff"
                     "\u0c00-\u0c7f\u0c80-\u0cff\u0d00-\u0d7f\u0600-\u06ff]")

# English is the rule. Straight quotes, dashes and ellipsis are fine; curly
# quotes and the like are not, because they came from somewhere else.
ODD = re.compile("[\u2018\u2019\u201c\u201d\u00a0\u2013]")

HINGLISH = re.compile(r"(?i)\b(hai|hain|nahi|nahin|kya|kaise|kaisa|kar|karo|karne|"
                      r"ke liye|se pehle|mera|meri|aap|apna|apni|bahut|thoda|dekho|"
                      r"dekhe|chahiye|hoga|hogi|raha|rahi|liye|wala|wali)\b")

BANNED = re.compile(r"(?i)\b(subscribe|bell icon|hit like|thumbs up|comment below|"
                    r"share this video|watch more|stay tuned|unlock code|"
                    r"paid app|premium app|locked app)")

MIN_SUMMARY, MAX_SUMMARY = 80, 600
MIN_BODY, MAX_BODY = 1800, 12000


def main():
    files = sorted(glob.glob(os.path.join(CONTENT, "*.json")))
    bad = []
    written = 0
    tools_missing = 0
    bodies, summaries = [], []

    for path in files:
        with io.open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        name = os.path.basename(path)
        body = data.get("body") or ""
        summary = data.get("summary") or ""
        faq = data.get("faq") or []
        if not body:
            continue
        written += 1
        bodies.append(len(body))
        summaries.append(len(summary))
        blob = summary + body + json.dumps(faq)

        if SCRIPTS.search(blob):
            bad.append("%s: non-Latin script found" % name)
        if ODD.search(blob):
            found = sorted(set(ODD.findall(blob)))
            bad.append("%s: curly/odd punctuation %r" % (name, found))
        if HINGLISH.search(blob):
            bad.append("%s: Hinglish word %r"
                       % (name, HINGLISH.search(blob).group(0)))
        if BANNED.search(blob):
            bad.append("%s: banned phrase %r" % (name, BANNED.search(blob).group(0)))
        if not (MIN_SUMMARY <= len(summary) <= MAX_SUMMARY):
            bad.append("%s: summary is %d chars" % (name, len(summary)))
        if not (MIN_BODY <= len(body) <= MAX_BODY):
            bad.append("%s: body is %d chars" % (name, len(body)))
        if not (2 <= len(faq) <= 6):
            bad.append("%s: %d FAQ pair(s)" % (name, len(faq)))
        if "rom flasher" not in blob.lower():
            tools_missing += 1

    print("files      : %d" % len(files))
    print("written    : %d" % written)
    print("summary    : min %d, avg %d, max %d"
          % (min(summaries, default=0), sum(summaries) // max(len(summaries), 1),
             max(summaries, default=0)))
    print("body       : min %d, avg %d, max %d"
          % (min(bodies, default=0), sum(bodies) // max(len(bodies), 1),
             max(bodies, default=0)))
    print("problems   : %d" % len(bad))
    for line in bad:
        print("   - %s" % line)
    if tools_missing:
        # Not a fault: a guide does not have to name the app, because every page
        # already carries the tool link and the download button.
        print("note       : %d guide(s) never name the app in text" % tools_missing)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
