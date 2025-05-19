import logging
from aiogram import Bot, Dispatcher, executor, types
from datetime import datetime
import config
import database
import keyboards
from utils import get_badge, format_username

database.init_db()
logging.basicConfig(level=logging.INFO)
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)

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

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    args = message.get_args()
    user_id = message.from_user.id
    username = message.from_user.username or ""
    invited_by = int(args) if args.isdigit() and int(args) != user_id else None

    if not database.get_user(user_id):
        database.add_user(user_id, username, invited_by)
        database.log_event("register", user_id, f"invited_by:{invited_by}")

    # تحقق من الاشتراك الإجباري
    if not await check_mandatory_channels(user_id):
        channels_links = "\n".join(
            [f"- <a href='https://t.me/{ch.replace('-100','')}'>{ch}</a>" for ch in config.COMP_CHANNELS]
        )
        await message.answer(
            f"🚨 للاشتراك بالمسابقة، يجب عليك الاشتراك في القنوات التالية أولاً:\n{channels_links}\n\nثم أعد إرسال /start.",
            disable_web_page_preview=True
        )
        return

    text = (
        "👋 أهلاً بك في <b>مسابقة الإحالة</b>!\n"
        "شارك رابط الإحالة الخاص بك لجمع النقاط والفوز بجوائز قيّمة.\n\n"
        "اضغط على الأزرار بالأسفل للتحكم والمشاركة 👇"
    )
    await message.answer(text, reply_markup=keyboards.main_keyboard(user_id))

@dp.callback_query_handler(lambda c: c.data == "join")
async def send_referral_link(call: types.CallbackQuery):
    user_id = call.from_user.id
    link = f"https://t.me/{config.BOT_USERNAME}?start={user_id}"
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
    badge = get_badge(rank)
    text = (
        f"✨ نقاطك: <b>{points}</b>\n"
        f"👥 إحالاتك: <b>{referrals}</b>\n"
        f"🏅 ترتيبك: <b>{rank}</b> {badge}"
    )
    await call.answer()
    await call.message.answer(text, reply_markup=keyboards.points_keyboard())

@dp.callback_query_handler(lambda c: c.data == "refresh")
async def refresh_points(call: types.CallbackQuery):
    await my_points(call)

@dp.callback_query_handler(lambda c: c.data == "top10")
async def show_top10(call: types.CallbackQuery):
    top = database.get_top_users(config.TOP_LIMIT)
    msg = "🏆 <b>أفضل 10 متسابقين</b>:\n\n"
    for i, (uid, username, points) in enumerate(top, start=1):
        mention = format_username(uid, username)
        badge = get_badge(i)
        msg += f"{i}- {mention} — <b>{points}</b> نقطة {badge}\n"
    await call.answer()
    await call.message.answer(msg)

@dp.callback_query_handler(lambda c: c.data == "topdaily")
async def show_top_daily(call: types.CallbackQuery):
    top = database.get_top_daily_users(config.TOP_LIMIT)
    msg = "🔥 <b>متصدرو اليوم</b>:\n\n"
    for i, (uid, username, pts) in enumerate(top, start=1):
        mention = format_username(uid, username)
        msg += f"{i}- {mention} — <b>{pts}</b> إحالة اليوم\n"
    await call.answer()
    await call.message.answer(msg)

@dp.callback_query_handler(lambda c: c.data == "profile")
async def show_profile(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = database.get_user(user_id)
    if not user:
        await call.answer("سجل أولاً عبر /start", show_alert=True)
        return
    rank = database.get_user_rank(user_id)
    badge = get_badge(rank)
    text = (
        f"👤 <b>ملفك الشخصي</b>\n"
        f"الاسم: @{user[1]}\n"
        f"النقاط: {user[2]}\n"
        f"الإحالات: {user[3]}\n"
        f"الترتيب: {rank} {badge}\n"
        f"تاريخ الانضمام: {user[5]}"
    )
    await call.answer()
    await call.message.answer(text)

@dp.callback_query_handler(lambda c: c.data == "whoinvited")
async def who_invited(call: types.CallbackQuery):
    user_id = call.from_user.id
    user = database.get_user(user_id)
    if not user or not user[4]:
        await call.answer("لا يوجد محيل مسجّل لك.", show_alert=True)
        return
    inviter = database.get_user(user[4])
    if not inviter:
        await call.answer("محيلك غير معروف.", show_alert=True)
        return
    await call.answer()
    await call.message.answer(f"👤 محيلك هو: @{inviter[1]} (ID: {inviter[0]})")

@dp.message_handler()
async def handle_join(message: types.Message):
    args = message.get_args()
    user_id = message.from_user.id
    username = message.from_user.username or ""
    invited_by = int(args) if args.isdigit() and int(args) != user_id else None

    if not database.get_user(user_id):
        database.add_user(user_id, username, invited_by)
        database.log_event("register", user_id, f"invited_by:{invited_by}")

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
            channels_links = "\n".join(
                [f"- <a href='https://t.me/{ch.replace('-100','')}'>{ch}</a>" for ch in config.COMP_CHANNELS]
            )
            await bot.send_message(
                user_id,
                f"عليك الاشتراك في القنوات الإلزامية أولاً ليتم احتساب الإحالة.\n{channels_links}\n\nثم أعد إرسال /start.",
                disable_web_page_preview=True
            )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
