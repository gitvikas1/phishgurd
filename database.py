import sqlite3
from datetime import datetime

def init_db(db_path="phishguard.db"):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            is_phishing INTEGER NOT NULL,
            probability REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def insert_result(db_path, url, is_phishing, probability):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO results (url, is_phishing, probability, created_at) VALUES (?,?,?,?)",
        (url, is_phishing, probability, datetime.utcnow().isoformat())
    )
    con.commit()
    con.close()

def get_phishing_history(db_path, limit=250):
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    cur.execute(
        "SELECT id, url, is_phishing, probability, created_at FROM results WHERE is_phishing=1 ORDER BY id DESC LIMIT ?",
        (limit,)
    )
    rows = cur.fetchall()
    con.close()
    return rows
