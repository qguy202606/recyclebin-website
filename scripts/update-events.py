#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

REPO = Path(__file__).resolve().parents[1]
EVENTS_PATH = REPO / "events" / "events.json"

USA_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL",
    "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT",
    "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI",
    "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY", "DC",
}


def run(cmd: str) -> str:
    out = subprocess.run(cmd, shell=True, text=True, cwd=REPO, capture_output=True)
    return (out.stdout or out.stderr or "").strip()


def git(*args: str) -> str:
    return run("git " + " ".join(args))


def fetch_url(url: str) -> str:
    return run(f'curl -fsSL "{url}"')


def normalize_date(raw: str) -> str:
    s = str(raw).strip()
    m = re.match(r"(\w+)\s+(\d{1,2}),?\s*(\d{4})", s, re.IGNORECASE)
    if m:
        months = {
            "january": "01", "february": "02", "march": "03", "april": "04",
            "may": "05", "june": "06", "july": "07", "august": "08",
            "september": "09", "october": "10", "november": "11", "december": "12",
        }
        mon = months.get(m.group(1).lower())
        if mon:
            return f"{m.group(3)}-{mon}-{int(m.group(2)):02d}"
    m2 = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m2:
        return s[:10]
    return ""


def fetch_ocwr() -> list[dict]:
    html = fetch_url("https://oclandfills.com/events/compost-giveaway")
    if not html:
        return []
    m = re.search(r"[A-Za-z]+\s+\d{1,2},\s*\d{4}", html)
    if not m:
        return []
    return [
        {
            "date": normalize_date(m.group(0)),
            "state": "CA",
            "title": "OCWR Compost Giveaway",
            "desc": "Free compost distribution for Orange County residents. Bring your own bins or bags.",
            "location": "Orange County, CA",
            "join_url": "https://oclandfills.com/events/compost-giveaway",
        }
    ]


def fetch_eventbrite_recycling() -> list[dict]:
    search_urls = [
        "https://www.eventbrite.com/d/california--irvine/recycling/?mode=search",
        "https://www.eventbrite.com/d/california--los-angeles/recycling/?mode=search",
        "https://www.eventbrite.com/d/united-states/recycling/?mode=search",
    ]
    out = []
    seen_urls = set()
    for url in search_urls:
        html = fetch_url(url)
        if not html:
            continue
        urls = re.findall(r"https://www\.eventbrite\.com/e/[^\"\s'>]+", html)
        for u in urls[:8]:
            if u in seen_urls:
                continue
            seen_urls.add(u)
            out.append(
                {
                    "date": "",
                    "state": "US",
                    "title": "Recycling Event on Eventbrite",
                    "desc": "More details on Eventbrite.",
                    "location": "United States",
                    "join_url": u,
                }
            )
    return out[:10]


def fetch_epa_events() -> list[dict]:
    """EPA environmental events and webcasts"""
    html = fetch_url("https://www.epa.gov/events")
    if not html:
        return []
    out = []
    for m in re.finditer(r'<h3[^>]*>([^<]+)</h3>', html):
        title = m.group(1).strip()
        if title and "recycl" in title.lower():
            out.append(
                {
                    "date": "",
                    "state": "US",
                    "title": title,
                    "desc": "EPA event.",
                    "location": "United States",
                    "join_url": "https://www.epa.gov/events",
                }
            )
    return out[:5]


def fetch_calrecycle() -> list[dict]:
    html = fetch_url("https://www.calrecycle.ca.gov/events/")
    if not html:
        return []
    out = []
    for m in re.finditer(r'"title":"([^"]+)"', html):
        title = m.group(1).strip()
        if title and "recycl" in title.lower():
            out.append(
                {
                    "date": "",
                    "state": "CA",
                    "title": title,
                    "desc": "CalRecycle event.",
                    "location": "California",
                    "join_url": "https://www.calrecycle.ca.gov/events/",
                }
            )
    return out[:5]


def key(ev: dict) -> str:
    d = normalize_date(ev.get("date", ""))
    return f"{d} {ev.get('title', '').lower()}".strip()


def prune_old(data: list[dict]) -> list[dict]:
    today = datetime.now()
    cutoff = today - __import__("datetime").timedelta(days=7)
    future = today + __import__("datetime").timedelta(days=90)
    out = []
    seen = set()
    for e in data:
        state = e.get("state", "")
        if state not in USA_STATES:
            continue
        d = normalize_date(e.get("date", ""))
        if not d:
            continue
        try:
            dt = datetime.strptime(d, "%Y-%m-%d")
        except Exception:
            continue
        if dt < cutoff or dt > future:
            continue
        k = (d, e.get("title", "").lower())
        if k in seen:
            continue
        seen.add(k)
        out.append(e)
    return out


def main() -> int:
    try:
        data = json.loads(EVENTS_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            data = []
    except Exception:
        data = []

    index = {key(ev): ev for ev in data if key(ev)}

    for source in (fetch_ocwr, fetch_eventbrite_recycling, fetch_epa_events, fetch_calrecycle):
        try:
            items = source()
            if not items:
                continue
            for ev in items:
                ev.setdefault("id", key(ev))
                idx = key(ev)
                if idx:
                    index[idx] = ev
        except Exception as exc:
            print("[update-events] source failed:", exc, file=sys.stderr)

    out = sorted(index.values(), key=lambda e: e.get("date", ""), reverse=True)
    out = prune_old(out)

    EVENTS_PATH.write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )

    git("add", str(EVENTS_PATH.relative_to(REPO)))
    if git("diff", "--cached", "--quiet"):
        print("[update-events] no changes")
        return 0
    git("commit", "-m", "chore(events): refresh events.json")
    git("push", "origin", "main")
    print(f"[update-events] updated {len(out)} events")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
