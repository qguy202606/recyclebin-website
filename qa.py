#!/usr/bin/env python3
"""RecycleBin website smoke test — run before push."""
import re, sys, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PAGES = ["index.html", "events.html", "guides.html", "centers.html", "lookup.html", "search.html", "game.html"]
URL = "https://qguy202606.github.io/recyclebin-website/"

errors = []

for page in PAGES:
    url = URL + page
    print(f"[FETCH] {url}")
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        errors.append(f"FAIL fetch {page}: {e}")
        continue

    # 1) CSS check
    if '/css/main.css' not in html:
        errors.append(f"FAIL {page}: missing <link rel=\"stylesheet\" href=\"/css/main.css\">")

    # 2) script src check (robust)
    has_site_js = "js/site.js" in html
    has_page_js = bool(re.search(r'<script[^>]+src="js/[^"]+\.js"', html))
    if not (has_site_js or has_page_js):
        errors.append(f"FAIL {page}: no local script loaded")

    # 3) Internal link check
    links = re.findall(r'href="(/[^"]+|https?://qguy202606\.github\.io/recyclebin-website/[^"]+)"', html)
    for href in set(links):
        target = ROOT / href.lstrip("/") if href.startswith("/") else href
        if not target.exists():
            errors.append(f"FAIL {page}: broken link -> {href}")

    # 4) Console script tag check (alert/console.log used?)
    inline_scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
    for script in inline_scripts:
        if "console.log" in script or "alert(" in script:
            pass  # ignore for now

if errors:
    print("\n[RESULT] FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
else:
    print("\n[RESULT] PASS — all pages ok")
    sys.exit(0)
