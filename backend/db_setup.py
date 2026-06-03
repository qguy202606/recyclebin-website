import sqlite3
import json
import os

DB_PATH = "events.db"
JSON_PATH = "../events.json"

def init_db(conn):
    conn.execute("""
    CREATE TABLE IF NOT EXISTS events (
      id TEXT PRIMARY KEY,
      date TEXT NOT NULL,
      title TEXT NOT NULL,
      desc TEXT,
      location TEXT,
      body TEXT,
      join_url TEXT,
      source TEXT,
      created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()

def normalize_record(row):
    return {
        "id": row[0],
        "date": row[1],
        "title": row[2],
        "desc": row[3],
        "location": row[4],
        "body": row[5],
        "join_url": row[6],
    }

def count_rows(conn):
    cur = conn.execute("SELECT COUNT(*) FROM events")
    row = cur.fetchone()
    return row[0] if row else 0

def seed_from_json(conn):
    if not os.path.exists(JSON_PATH):
        return 0
    data = json.load(open(JSON_PATH, "r", encoding="utf-8"))
    inserted = 0
    for item in data:
        id_ = item.get("id")
        date = item.get("date")
        title = item.get("title")
        desc = item.get("desc")
        location = item.get("location")
        body = item.get("body")
        join_url = item.get("join_url", "#")
        source = item.get("source", "import")
        conn.execute(
            "INSERT OR REPLACE INTO events (id, date, title, desc, location, body, join_url, source) VALUES (?,?,?,?,?,?,?,?)",
            (id_, date, title, desc, location, body, join_url, source),
        )
        inserted += 1
    conn.commit()
    return inserted

def list_upcoming(conn):
    today = "2026-01-01"
    cur = conn.execute(
        "SELECT id, date, title, desc, location, body, join_url FROM events WHERE date >= ? AND title IS NOT NULL ORDER BY date ASC",
        (today,),
    )
    rows = cur.fetchall()
    return [normalize_record(r) for r in rows]

def main():
    conn = sqlite3.connect(DB_PATH)
    init_db(conn)
    print(f"Rows before import: {count_rows(conn)}")
    n = seed_from_json(conn)
    print(f"Imported from {JSON_PATH}: {n}")
    print(f"Rows after import: {count_rows(conn)}")
    upcoming = list_upcoming(conn)
    print(f"Upcoming events (today-relative): {len(upcoming)}")
    for ev in upcoming:
        print(ev["date"], "|", ev["title"], "|", ev["location"])
    conn.close()

if __name__ == "__main__":
    main()
