"""Merge a written draft into content/<videoId>.json.

    python set_article.py --id -n5Kb8536xs --file drafts/-n5Kb8536xs.md
    python set_article.py --id -n5Kb8536xs --stdin
    python set_article.py --check            # validate every content file
    python set_article.py --missing          # list the ones still unwritten

Draft format (plain text, three sections, order free):

    ::summary
    Two or three sentences that answer the search query straight away.

    ::body
    ## A heading
    A paragraph.

    - a bullet
    - another one

    ::faq
    Q: Why does the script close immediately?
    A: The image folder is in the wrong place. It must sit next to the .bat.

    Q: Will this wipe my data?
    A: Yes. A fastboot ROM flashes the full image, so back up first.

Rules the checker enforces - English only, no Devanagari, none of the banned
lines (subscribe / like / comment / share / watch more / unlock code / paid app),
and the summary + body lengths stay inside the SEO window.
"""

import argparse
import glob
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
DRAFTS = os.path.join(HERE, "drafts")

DEVANAGARI = re.compile("[\u0900-\u097F\uA8E0-\uA8FF]")
BANNED = re.compile(
    r"(subscribe|hit\s+the\s+bell|bell\s+icon|comment\s+below|let\s+me\s+know\s+in\s+the\s+comments|"
    r"hit\s+like|thumbs?\s+up|like\s+this\s+video|share\s+this\s+video|watch\s+more|"
    r"stay\s+tuned|2k\s+subscriber|unlock\s+code|paid\s+app|premium\s+app|"
    r"buy\s+the\s+app|purchase\s+the\s+app|locked\s+app)", re.I)

MIN_SUMMARY, MAX_SUMMARY = 80, 600
MIN_BODY, MAX_BODY = 1800, 12000
MIN_FAQ, MAX_FAQ = 2, 6


def parse_draft(text):
    parts = {"summary": [], "body": [], "faq": []}
    current = None
    for line in text.replace("\r\n", "\n").split("\n"):
        marker = re.match(r"^::(summary|body|faq)\s*$", line.strip(), re.I)
        if marker:
            current = marker.group(1).lower()
            continue
        if current:
            parts[current].append(line)
    return parts


def faq_from(lines):
    out, q, buf = [], None, []
    for line in lines:
        m = re.match(r"^\s*Q:\s*(.+)$", line)
        if m:
            if q:
                out.append({"q": q, "a": "\n".join(buf).strip()})
            q, buf = m.group(1).strip(), []
            continue
        if re.match(r"^\s*A:\s*", line):
            buf.append(re.sub(r"^\s*A:\s*", "", line))
            continue
        if q:
            buf.append(line)
    if q:
        out.append({"q": q, "a": "\n".join(buf).strip()})
    return [f for f in out if f["q"] and f["a"]]


def check_piece(name, text, lo, hi, problems):
    n = len(text.strip())
    if n < lo:
        problems.append("%s short (%d < %d)" % (name, n, lo))
    if n > hi:
        problems.append("%s long (%d > %d)" % (name, n, hi))
    if DEVANAGARI.search(text):
        problems.append("%s has Devanagari (must be English)" % name)
    bad = BANNED.search(text)
    if bad:
        problems.append("%s has banned text %r" % (name, bad.group(0)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--id")
    ap.add_argument("--file")
    ap.add_argument("--stdin", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--missing", action="store_true")
    ap.add_argument("--force", action="store_true", help="write even if warnings")
    args = ap.parse_args()

    os.makedirs(DRAFTS, exist_ok=True)

    if args.check or args.missing:
        rows = []
        for path in sorted(glob.glob(os.path.join(CONTENT, "*.json"))):
            data = json.load(io.open(path, encoding="utf-8"))
            body = (data.get("body") or "").strip()
            rows.append((os.path.basename(path), len(body), len(data.get("faq") or [])))
        empty = [r for r in rows if r[1] == 0]
        print("content files : %d" % len(rows))
        print("written       : %d" % (len(rows) - len(empty)))
        print("still empty   : %d" % len(empty))
        if args.missing:
            for name, _, _ in empty:
                print("   ", name)
        if args.check:
            problems = []
            for name, blen, nfaq in rows:
                if blen == 0:
                    continue
                data = json.load(io.open(os.path.join(CONTENT, name), encoding="utf-8"))
                check_piece(name + " summary", data.get("summary", ""),
                            MIN_SUMMARY, MAX_SUMMARY, problems)
                check_piece(name + " body", data.get("body", ""),
                            MIN_BODY, MAX_BODY, problems)
                if not (MIN_FAQ <= nfaq <= MAX_FAQ):
                    problems.append("%s faq count %d" % (name, nfaq))
                if not any("github.com/romflasher3419-spec" in (l.get("url") or "")
                           for l in data.get("links") or []):
                    problems.append("%s missing the tool link" % name)
                if data.get("device") == "":
                    problems.append("%s has no device" % name)
            print("problems      : %d" % len(problems))
            for p in problems[:60]:
                print("   -", p)
        return 0

    if not args.id:
        print("need --id")
        return 2
    path = os.path.join(CONTENT, "%s.json" % args.id)
    if not os.path.exists(path):
        print("[!] no content file for %s" % args.id)
        return 1

    if args.file:
        text = io.open(args.file, encoding="utf-8", errors="replace").read()
    elif args.stdin:
        text = sys.stdin.read()
    else:
        found = sorted(glob.glob(os.path.join(DRAFTS, "%s.*" % args.id)))
        if not found:
            print("[!] no draft for %s in drafts/ - use --file" % args.id)
            return 1
        text = io.open(found[0], encoding="utf-8", errors="replace").read()
    parts = parse_draft(text)

    summary = "\n".join(parts["summary"]).strip()
    body = "\n".join(parts["body"]).strip()
    faq = faq_from(parts["faq"])

    problems = []
    check_piece("summary", summary, MIN_SUMMARY, MAX_SUMMARY, problems)
    check_piece("body", body, MIN_BODY, MAX_BODY, problems)
    if not (MIN_FAQ <= len(faq) <= MAX_FAQ):
        problems.append("faq count %d" % len(faq))

    path = os.path.join(CONTENT, "%s.json" % args.id)
    data = json.load(io.open(path, encoding="utf-8"))
    data["summary"], data["body"], data["faq"] = summary, body, faq
    if problems:
        print("[!] %d warning(s):" % len(problems))
        for p in problems:
            print("    -", p)
        if not args.force:
            print("[!] not written (use --force to accept)")
            return 1
    with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=1)
    print("[OK] %s  summary=%d body=%d faq=%d"
          % (args.id, len(summary), len(body), len(faq)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
