import sqlite3

conn = sqlite3.connect("bot.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    paid INTEGER DEFAULT 0
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS stats (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER
)
""")

conn.commit()


def is_paid(user_id: int) -> bool:
    cur.execute("SELECT paid FROM users WHERE user_id=?", (user_id,))
    row = cur.fetchone()
    return row and row[0] == 1


def set_paid(user_id: int):
    cur.execute(
        "INSERT OR REPLACE INTO users (user_id, paid) VALUES (?, 1)",
        (user_id,)
    )
    conn.commit()


def add_stat(user_id: int):
    cur.execute("INSERT INTO stats (user_id) VALUES (?)", (user_id,))
    conn.commit()


def total_downloads():
    cur.execute("SELECT COUNT(*) FROM stats")
    return cur.fetchone()[0]
