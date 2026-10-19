"""How far along the writing is.

    python _progress.py          # totals + per-wave table
    python _progress.py --short  # one line
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    done, missing = [], []
    for path in sorted(glob.glob(os.path.join(HERE, "content", "*.json"))):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        (done if data.get("body") else missing).append(data["id"])
    total = len(done) + len(missing)
    print("%d / %d written (%d left)" % (len(done), total, len(missing)))
    if "--short" in sys.argv:
        return 0

    left = set(missing)
    wave_dir = os.path.join(HERE, "waves")
    for path in sorted(glob.glob(os.path.join(wave_dir, "wave_*.txt"))):
        with open(path, encoding="utf-8") as fh:
            ids = [x.strip() for x in fh if x.strip()]
        todo = [i for i in ids if i in left]
        print("  %-14s %d/%d %s" % (os.path.basename(path), len(ids) - len(todo),
                                    len(ids), "DONE" if not todo else "left: " + ",".join(todo)))
    if missing:
        print("missing ids: %s" % ",".join(missing))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
