import sqlite3
from typing import Optional, List, Tuple

DB_NAME = "referral_competition.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            points INTEGER DEFAULT 0,
            referrals INTEGER DEFAULT 0,
            invited_by INTEGER,
            join_date TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_type TEXT,
            user_id INTEGER,
            info TEXT,
            event_time TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def add_user(user_id: int, username: str, invited_by: Optional[int] = None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO users (user_id, username, invited_by)
        VALUES (?, ?, ?)
    ''', (user_id, username, invited_by))
    conn.commit()
    conn.close()

def get_user(user_id: int) -> Optional[Tuple]:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def add_points(user_id: int, points: int):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('UPDATE users SET points = points + ?, referrals = referrals + 1 WHERE user_id = ?', (points, user_id))
    conn.commit()
    conn.close()

def get_top_users(limit: int = 10) -> List[Tuple]:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT user_id, username, points FROM users ORDER BY points DESC, referrals DESC LIMIT ?', (limit,))
    users = c.fetchall()
    conn.close()
    return users

def get_user_rank(user_id: int) -> int:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT user_id FROM users ORDER BY points DESC, referrals DESC')
    ids = [row[0] for row in c.fetchall()]
    conn.close()
    try:
        return ids.index(user_id) + 1
    except ValueError:
        return -1

def log_event(event_type: str, user_id: int, info: str = ""):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO events (event_type, user_id, info)
        VALUES (?, ?, ?)
    ''', (event_type, user_id, info))
    conn.commit()
    conn.close()
