#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(r"C:/Users/opc/source/repos/recyclebin-website-v2")
EVENTS_PATH = REPO / "events" / "events.json"


def run(cmd: str) -> str:
    out = subprocess.run(cmd, shell=True, text=True, cwd=REPO, capture_output=True)
    return (out.stdout or out.stderr or "").strip()


def git(*args: str) -> str:
    return run("git " + " ".join(args))


def fetch_url(url: str) -> str:
    return run(f'curl -fsSL "{url}"')


def fetch_ocwr() -> dict | None:
    html = fetch_url("https://oclandfills.com/events/compost-giveaway")
    if not html:
        return None
    m = re.search(r"[A-Za-z]+ \d{1,2}, \d{4}", html)
    date = m.group(0) if m else ""
    return {
        "date": date,
        "state": "CA",
        "title": "OCWR Compost Giveaway",
        "desc": "Free compost distribution for Orange County residents. Bring your own bins or bags.",
        "location": "Orange County, CA",
        "join_url": "https://oclandfills.com/events/compost-giveaway",
    }


def fetch_eventbrite() -> list[dict]:
    html = fetch_url(
        "https://www.eventbrite.com/d/california--irvine/recycling/?mode=search"
    )
    if not html:
        return []
    urls = re.findall(r"https://www\.eventbrite\.com/e/[^\"\s'>]+", html)
    seen: set[str] = set()
    out: list[dict] = []
    for url in urls[:8]:
        if url in seen:
            continue
        seen.add(url)
        out.append(
            {
                "date": "",
                "state": "CA",
                "title": "Eventbrite Event",
                "desc": "Auto-discovered from Eventbrite.",
                "location": "Irvine, CA",
                "join_url": url,
            }
        )
    return out


def key(ev: dict) -> str:
    return ev.get("id") or (ev.get("date", "") + " " + ev.get("title", ""))


def main() -> int:
    try:
        data = json.loads(EVENTS_PATH.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            data = []
    except Exception:
        data = []

    index = {key(ev): ev for ev in data}

    for source in (fetch_ocwr,):
        try:
            ev = source()
            if not ev:
                continue
            ev.setdefault("id", key(ev))
            index[key(ev)] = ev
        except Exception as exc:
            print("[update-events] source failed:", exc, file=sys.stderr)

    for ev in fetch_eventbrite():
        ev.setdefault("id", key(ev))
        index[key(ev)] = ev

    out = sorted(index.values(), key=lambda e: e.get("date", ""))
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
