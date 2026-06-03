#!/usr/bin/env python3
"""RecycleBin website smoke test — lightweight, production-aware."""
import re, sys, urllib.request
from pathlib import PurePosixPath

ROOT = r"C:/Users/opc/source/repos/recyclebin-website"
DOMAIN = "https://qguy202606.github.io/recyclebin-website"

# 哪些頁面要求是正式「有掛 main.css + local script」的頁面
REQUIRED_STYLE_PAGES = {
    "index.html","events.html","guides.html","centers.html",
    "lookup.html","search.html","game.html","howto.html","event-detail.html"
}

# 一些靜態 landing 頁不需要強制掛共用 stylesheet（維持現狀）
# 這裡不強制檢查。

CORE_PAGES = sorted(REQUIRED_STYLE_PAGES)
URL = DOMAIN + "/"

errors = []

def norm_href(href):
    # 只解析真正落盤的 relative/absolute 路徑：不含 query/hash，且是站內 link
    if href.startswith("mailto:") or href.startswith("tel:") or href.startswith("#"):
        return None
    if href.startswith("http://") or href.startswith("https://"):
        if not href.startswith(DOMAIN):
            return None
        href = href[len(DOMAIN):]
    # 清掉 query/hash
    p = href.split("?",1)[0].split("#",1)[0]
    if not p or p.startswith("//"):
        return None
    return p.lstrip("/")

for page in CORE_PAGES:
    url = URL + page
    print(f"[FETCH] {url}")
    try:
        with urllib.request.urlopen(url, timeout=15) as r:
            html = r.read().decode("utf-8", errors="replace")
    except Exception as e:
        errors.append(f"FAIL fetch {page}: {e}")
        continue

    # style / script 規則（只針對 REQUIRED 清單）
    if page in REQUIRED_STYLE_PAGES:
        if '/css/main.css' not in html:
            errors.append(f"FAIL {page}: missing /css/main.css")
        if not (('js/site.js' in html) or re.search(r'<script[^>]+src="js/[^"]+\.js"', html)):
            errors.append(f"FAIL {page}: no local script")

    # 只檢查靜態可解析的內部連結（排除 JS 動態路由）
    links = re.findall(r'href=(["\'])([^"\']+)\1', html)
    checked = set()
    for quote, href in links:
        target = norm_href(href)
        if target is None:
            continue
        if target in checked:
            continue
        checked.add(target)
        if re.search(r'[?*<>\|]', target):
            continue
        fs_target = ROOT / PurePosixPath(target)
        if not fs_target.exists():
            errors.append(f"FAIL {page}: broken link -> {target}")

if errors:
    print("\n[RESULT] FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
else:
    print("\n[RESULT] PASS — all production pages ok")
    sys.exit(0)
