#!/usr/bin/env python3
"""Render the Token Radar dashboard with headless Chrome's built-in --screenshot.

Three shots at 1440x900:
  1-board.png    - the ranked board
  2-detail.png   - a protocol's detail view open (hash-driven)
  3-filtered.png - the board filtered by search query (hash-driven)
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = r"C:\Users\BRAD\money_engine"
OUT = os.path.join(ROOT, "out-test")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

shot_dir = os.path.join(HERE, "screenshots")
os.makedirs(shot_dir, exist_ok=True)


def shot(name, url, attempt=0):
    path = os.path.join(shot_dir, name)
    prof = os.path.join(ROOT, "chrome-shot", name, str(os.getpid()) + str(attempt))
    cmd = [CHROME, "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
           "--window-size=1440,900", "--force-device-scale-factor=1",
           "--virtual-time-budget=8000",
           "--user-data-dir=" + prof,
           f"--screenshot={path}", url]
    p = subprocess.run(cmd, capture_output=True, timeout=90)
    if p.returncode != 0:
        err = p.stderr.decode("utf-8", "replace")[:300]
        print(f"{name}: chrome exited {p.returncode}: {err}")
    size = os.path.getsize(path) if os.path.exists(path) else 0
    print(f"{name}: bytes={size}")
    if size < 20_000 and attempt < 2:
        print(f"{name}: blank, retrying with fresh profile")
        time.sleep(2)
        shot(name, url, attempt + 1)
    return size


def main():
    file_url = "file:///" + OUT.replace("\\", "/") + "/dashboard/index.html"
    slug = None
    data_js = os.path.join(OUT, "data.js")
    if os.path.exists(data_js):
        txt = open(data_js, encoding="utf-8").read().rstrip()
        m = json.loads(txt[len("window.RADAR="):].rstrip(";"))
        rows = m.get("rows", [])
        if rows:
            slug = rows[0]["slug"]
    shot("1-board.png", file_url)
    shot("2-detail.png", file_url + ("#p=" + slug if slug else ""))
    shot("3-filtered.png", file_url + "#q=lending")
    return 0


if __name__ == "__main__":
    sys.exit(main())
