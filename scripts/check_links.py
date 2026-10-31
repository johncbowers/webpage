#!/usr/bin/env python3
"""Check every link on the built site (run `zensical build` first).

    python3 -I scripts/check_links.py            # all links
    python3 -I scripts/check_links.py --internal # only links into /bowersjc/

Prints one line per link that doesn't load (code, URL, pages it's on) and
exits 1 if any did. 403/401/418/429/202 are listed separately: those sites
usually block scripts but work in a browser, so they're not counted as broken.
Internal links are checked against the live site, since public_html holds
files this repo doesn't build (files/, fya/, ...).
"""
import glob
import html
import os
import re
import subprocess
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

BASE = "https://w3.cs.jmu.edu/bowersjc/"
BLOCKED = {"202", "401", "403", "418", "429"}
SKIP = ("mailto:", "#", "data:", "webcal:", "javascript:")

root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "site")
internal_only = "--internal" in sys.argv

links = {}
for path in sorted(glob.glob(os.path.join(root, "*.html"))):
    page = os.path.basename(path)
    if page == "404.html":
        continue
    text = open(path, encoding="utf-8").read()
    # HTML comments hold commented-out content, not live links
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    for u in re.findall(r'(?:href|src)="([^"]+)"', text):
        u = html.unescape(u)
        if u.startswith(SKIP):
            continue
        full = urllib.parse.urljoin(BASE + page, u).split("#")[0]
        if "/assets/" in full or "fonts.g" in full or "zensical.org" in full:
            continue
        # Wayback snapshots don't go away, and archive.org times out under load
        if full.startswith("https://web.archive.org/web/"):
            continue
        if internal_only and not full.startswith(BASE):
            continue
        links.setdefault(full, set()).add(page)


def check(u):
    out = subprocess.run(
        ["curl", "-s", "-L", "-o", "/dev/null", "-m", "25",
         "-A", "Mozilla/5.0 (Macintosh) Safari/605", "-w", "%{http_code}", u],
        capture_output=True, text=True).stdout
    return u, out or "000"


with ThreadPoolExecutor(16) as ex:
    results = list(ex.map(check, sorted(links)))

broken = [(c, u) for u, c in results if c != "200" and c not in BLOCKED]
blocked = [(c, u) for u, c in results if c in BLOCKED]
for c, u in broken:
    print(f"BROKEN {c} {u}  ({', '.join(sorted(links[u]))})")
for c, u in blocked:
    print(f"blocked-by-site {c} {u}  ({', '.join(sorted(links[u]))})")
print(f"{len(links)} links checked, {len(broken)} broken, {len(blocked)} blocked")
sys.exit(1 if broken else 0)
