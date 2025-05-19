import asyncpg
import os
import csv
from datetime import datetime

DATABASE_URL = os.getenv("DATABASE_URL")

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(DATABASE_URL)
    return _pool

# إضافة مستخدم جديد
async def add_user(user):
    pool = await get_pool()
    await pool.execute(
        """
        INSERT INTO users (tg_id, username, full_name, joined_at)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (tg_id) DO NOTHING
        """,
        user.id,
        user.username,
        f"{user.first_name or ''} {user.last_name or ''}".strip(),
        datetime.utcnow()
    )

# جلب مستخدم واحد
async def get_user(tg_id):
    pool = await get_pool()
    row = await pool.fetchrow("SELECT * FROM users WHERE tg_id = $1", tg_id)
    return row

# جلب جميع المستخدمين
async def get_all_users():
    pool = await get_pool()
    rows = await pool.fetch("SELECT * FROM users")
    return rows

# حظر مستخدم (تحديث is_banned)
async def ban_user(tg_id):
    pool = await get_pool()
    await pool.execute("UPDATE users SET is_banned = TRUE WHERE tg_id = $1", tg_id)

# تصدير المستخدمين إلى ملف CSV
async def export_csv(filename="users_export.csv"):
    users = await get_all_users()
    if not users:
        return None
    fieldnames = users[0].keys()
    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in users:
            writer.writerow(dict(row))
    return filename

# جلب تقارير الغش (من جدول cheat_reports)
async def get_cheat_reports():
    pool = await get_pool()
    rows = await pool.fetch("SELECT * FROM cheat_reports")
    return rows

# ------ الدوال الخاصة بالإحالة ------
# توليد رابط الإحالة للمستخدم
def generate_referral_link(bot_username, user_id):
    return f"https://t.me/{bot_username}?start={user_id}"

# التحقق من الاشتراك في قناة (مثال: تحقق من وجود المستخدم في جدول subscriptions)
async def check_subscription(tg_id, channel_username):
    pool = await get_pool()
    row = await pool.fetchrow(
        "SELECT * FROM subscriptions WHERE tg_id = $1 AND channel = $2", tg_id, channel_username
    )
    return bool(row)

# إضافة نقاط لمستخدم
async def add_points(tg_id, points):
    pool = await get_pool()
    await pool.execute(
        "UPDATE users SET points = COALESCE(points, 0) + $1 WHERE tg_id = $2", points, tg_id
    )

# تسجيل حدث (log) في جدول الأحداث
async def log_event(tg_id, event_type, data=None):
    pool = await get_pool()
    await pool.execute(
        "INSERT INTO events (tg_id, event_type, data, created_at) VALUES ($1, $2, $3, $4)",
        tg_id, event_type, data, datetime.utcnow()
    )
