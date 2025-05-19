import asyncpg, os
DB_URL = os.getenv("DATABASE_URL")
_pool = None
async def get_pool():
    global _pool
    if not _pool: _pool = await asyncpg.create_pool(dsn=DB_URL)
    return _pool

async def get_user(tg_id):
    pool = await get_pool()
    return await pool.fetchrow("SELECT * FROM users WHERE tg_id = $1", tg_id)

async def add_user(user, inviter_id=None):
    pool = await get_pool()
    await pool.execute(
        "INSERT INTO users (tg_id, username, full_name, inviter_id) VALUES ($1, $2, $3, $4) ON CONFLICT DO NOTHING",
        user.id, user.username, user.full_name, inviter_id
    )

async def generate_referral_link(user_id):
    pool = await get_pool()
    link = f"https://t.me/YourBot?start={user_id}"
    await pool.execute("UPDATE users SET referral_link = $1 WHERE tg_id = $2", link, user_id)
    return link

async def get_points(user_id):
    pool = await get_pool()
    row = await pool.fetchrow("SELECT points FROM users WHERE tg_id = $1", user_id)
    return row["points"] if row else 0

async def get_rank(user_id):
    pool = await get_pool()
    row = await pool.fetchrow(
        "SELECT COUNT(*)+1 AS rank FROM users WHERE points > (SELECT points FROM users WHERE tg_id=$1)", user_id
    )
    return row["rank"]

async def get_badge(user_id):
    pool = await get_pool()
    row = await pool.fetchrow("SELECT badge FROM users WHERE tg_id = $1", user_id)
    return row["badge"] if row else "none"

async def get_level(user_id):
    pool = await get_pool()
    row = await pool.fetchrow("SELECT level FROM users WHERE tg_id = $1", user_id)
    return row["level"] if row else 1

async def add_points(user_id, pts):
    pool = await get_pool()
    await pool.execute("UPDATE users SET points = points + $1 WHERE tg_id = $2", pts, user_id)

async def check_subscription(user_id):
    # تحقق الاشتراك (تحتاج API Bot أو مكتبة خاصة)
    return True

async def get_top10_users():
    pool = await get_pool()
    rows = await pool.fetch("SELECT full_name, points FROM users ORDER BY points DESC LIMIT 10")
    return rows

async def get_leaderboard():
    pool = await get_pool()
    rows = await pool.fetch("SELECT full_name, points FROM users ORDER BY points DESC")
    return rows

async def get_mandatory_channels():
    return os.getenv("MANDATORY_CHANNELS", "").split(",")

async def log_event(user_id, event_type, details):
    pool = await get_pool()
    await pool.execute(
        "INSERT INTO events_log (user_id, event_type, details) VALUES ($1, $2, $3)",
        user_id, event_type, details
    )

async def export_csv():
    import csv, tempfile
    pool = await get_pool()
    rows = await pool.fetch("SELECT tg_id, username, full_name, points, badge, level FROM users")
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    with open(tmp.name, "w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["tg_id", "username", "full_name", "points", "badge", "level"])
        for r in rows:
            writer.writerow([r["tg_id"], r["username"], r["full_name"], r["points"], r["badge"], r["level"]])
    return tmp.name

async def ban_user(user_id):
    pool = await get_pool()
    await pool.execute("UPDATE users SET is_banned = TRUE WHERE tg_id = $1", user_id)

async def get_cheat_reports():
    pool = await get_pool()
    rows = await pool.fetch("SELECT reported_user_id, reason FROM cheat_reports WHERE status='pending'")
    return rows

async def get_active_challenges():
    pool = await get_pool()
    rows = await pool.fetch("SELECT * FROM challenges WHERE start_date <= CURRENT_DATE AND end_date >= CURRENT_DATE")
    return rows

async def join_challenge(user_id, challenge_id):
    pool = await get_pool()
    await pool.execute(
        "INSERT INTO challenge_participation (user_id, challenge_id) VALUES ($1, $2) ON CONFLICT DO NOTHING",
        user_id, challenge_id
    )