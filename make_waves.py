"""Split the unwritten articles into small waves for the writers.

    python make_waves.py --size 8        # write waves/wave_01.txt ...
    python make_waves.py --status        # how far along are we

A wave file is just one video id per line. Devices are kept together so a writer
handles one phone family at a time and the tone stays consistent.
"""

import argparse
import glob
import io
import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(HERE, "content")
WAVES = os.path.join(HERE, "waves")


def load():
    rows = []
    for path in sorted(glob.glob(os.path.join(CONTENT, "*.json"))):
        d = json.load(io.open(path, encoding="utf-8"))
        rows.append(d)
    return rows


def status():
    rows = load()
    done = [r for r in rows if (r.get("body") or "").strip()]
    todo = [r for r in rows if not (r.get("body") or "").strip()]
    print("total   : %d" % len(rows))
    print("written : %d" % len(done))
    print("left    : %d" % len(todo))
    print()
    by = defaultdict(lambda: [0, 0])
    for r in rows:
        key = r.get("device") or "(no device)"
        by[key][0 if (r.get("body") or "").strip() else 1] += 1
    print("%-20s %8s %8s" % ("device", "written", "left"))
    for key in sorted(by, key=lambda k: -sum(by[k])):
        print("%-20s %8d %8d" % (key, by[key][0], by[key][1]))
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--size", type=int, default=8)
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    if args.status:
        return status()

    rows = [r for r in load() if not (r.get("body") or "").strip()]
    rows.sort(key=lambda r: (-(r.get("views") or 0)))
    by_device = defaultdict(list)
    for r in rows:
        by_device[r.get("device") or "(no device)"].append(r["id"])

    order = sorted(by_device, key=lambda k: -len(by_device[k]))
    queue = []
    for device in order:
        queue.extend(by_device[device])

    os.makedirs(WAVES, exist_ok=True)
    for old in glob.glob(os.path.join(WAVES, "wave_*.txt")):
        os.remove(old)

    made = 0
    for i in range(0, len(queue), args.size):
        chunk = queue[i:i + args.size]
        made += 1
        path = os.path.join(WAVES, "wave_%02d.txt" % made)
        with io.open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(chunk) + "\n")

    print("unwritten : %d" % len(queue))
    print("waves     : %d files of up to %d in %s" % (made, args.size, WAVES))
    for n in range(1, made + 1):
        path = os.path.join(WAVES, "wave_%02d.txt" % n)
        ids = io.open(path, encoding="utf-8").read().split()
        print("  wave_%02d  %d" % (n, len(ids)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
