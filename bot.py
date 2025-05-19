import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
import asyncio

import config
import database

# تشغيل قاعدة البيانات عند بدء البوت
database.init_db()

logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

def get_ref_link(user_id: int):
    return f"https://t.me/{bot.username}?start={user_id}"

def is_competition_active():
    end = datetime.strptime(config.COMPETITION_END, "%Y-%m-%d %H:%M:%S")
    return datetime.now() < end

async def check_mandatory_channels(user_id: int):
    for channel in config.COMP_CHANNELS:
        try:
            member = await bot.get_chat_member(channel, user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                return False
        except Exception:
            return False
    return True

def main_keyboard():
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("اشترك بالمسابقة", callback_data="join"),
        InlineKeyboardButton("نقاطي", callback_data="mypoints"),
        InlineKeyboardButton("أفضل 10", callback_data="top10"),
        InlineKeyboardButton("قناة المسابقة", url=f"https://t.me/{config.EVENTS_CHANNEL.replace('-100','')}")
    )
    kb.add(InlineKeyboardButton("التواصل مع الإدارة", url=f"https://t.me/{config.ADMIN_ID}"))
    return kb

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    args = message.get_args()
    user_id = message.from_user.id
    username = message.from_user.username or ""
    invited_by = int(args) if args.isdigit() and int(args) != user_id else None

    if not database.get_user(user_id):
        database.add_user(user_id, username, invited_by)
        database.log_event("register", user_id, f"invited_by:{invited_by}")

    text = (
        "👋 أهلاً بك في <b>مسابقة الإحالة</b>!\n"
        "شارك رابط الإحالة الخاص بك لجمع النقاط والفوز بجوائز قيّمة.\n\n"
        "اضغط على الأزرار بالأسفل للتحكم والمشاركة 👇"
    )
    await message.answer(text, reply_markup=main_keyboard())

@dp.callback_query_handler(lambda c: c.data == "join")
async def send_referral_link(call: types.CallbackQuery):
    user_id = call.from_user.id
    link = f"https://t.me/{(await bot.get_me()).username}?start={user_id}"
    text = (
        f"📢 رابط الإحالة الخاص بك:\n{link}\n\n"
        "أرسل هذا الرابط لأصدقائك، كل شخص ينضم ويشترك بالقنوات يمنحك 100 نقطة!"
    )
    await call.answer()
    await call.message.answer(text)

@dp.callback_query_handler(lambda c: c.data == "mypoints")
async def my_points(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = database.get_user(user_id)
    if not user:
        await call.answer("سجل أولاً عبر /start", show_alert=True)
        return
    rank = database.get_user_rank(user_id)
    points = user[2]
    referrals = user[3]
    text = (
        f"✨ نقاطك: <b>{points}</b>\n"
        f"👥 إحالاتك: <b>{referrals}</b>\n"
        f"🏅 ترتيبك: <b>{rank}</b>"
    )
    await call.answer()
    await call.message.answer(text)

@dp.callback_query_handler(lambda c: c.data == "top10")
async def show_top10(call: types.CallbackQuery):
    top = database.get_top_users(config.TOP_LIMIT)
    msg = "🏆 <b>أفضل 10 متسابقين</b>:\n\n"
    for i, (uid, username, points) in enumerate(top, start=1):
        mention = f"@{username}" if username else f"ID:{uid}"
        msg += f"{i}- {mention} — <b>{points}</b> نقطة\n"
    await call.answer()
    await call.message.answer(msg)

@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def handle_new_member(message: types.Message):
    # ليس للاستخدام في البوت الخاص، فقط مجموعات (يمكن تجاهله)
    pass

@dp.message_handler()
async def handle_join(message: types.Message):
    # يتابع التحقق من الإحالة عند دخول شخص جديد عبر رابط الإحالة
    args = message.get_args()
    user_id = message.from_user.id
    username = message.from_user.username or ""
    invited_by = int(args) if args.isdigit() and int(args) != user_id else None

    if not database.get_user(user_id):
        database.add_user(user_id, username, invited_by)
        database.log_event("register", user_id, f"invited_by:{invited_by}")

        # تحقق من الاشتراك الإجباري
        if invited_by and await check_mandatory_channels(user_id):
            database.add_points(invited_by, config.REFERRAL_POINTS)
            await bot.send_message(
                invited_by,
                f"🎉 تم إضافة إحالة جديدة إليك!\nمبروك، حصلت على {config.REFERRAL_POINTS} نقطة.",
            )
            await bot.send_message(
                config.EVENTS_CHANNEL,
                f"📥 إحالة جديدة!\nالمحيل: <a href='tg://user?id={invited_by}'>{invited_by}</a>\n"
                f"المحال: <a href='tg://user?id={user_id}'>{user_id}</a>"
            )
            database.log_event("referral", invited_by, f"invited:{user_id}")
        elif invited_by:
            await bot.send_message(
                user_id,
                "عليك الاشتراك في القنوات الإلزامية أولاً ليتم احتساب الإحالة."
            )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
