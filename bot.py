import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
from datetime import datetime
import config
import database
import keyboards
from utils import get_badge, format_username
from aiogram.client.bot import DefaultBotProperties

database.init_db()
logging.basicConfig(level=logging.INFO)
bot = Bot(
    token=config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()

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

async def get_channel_link(channel_id):
    try:
        chat = await bot.get_chat(channel_id)
        if chat.username:
            return f"https://t.me/{chat.username}"
        else:
            return f"(قناة خاصة، تواصل مع الإدارة)"
    except Exception:
        return "(تعذر جلب الرابط)"

@dp.message(Command("start"))
async def start_command(message: types.Message):
    args = ""
    parts = message.text.split(maxsplit=1)
    if len(parts) > 1:
        args = parts[1]
    user_id = message.from_user.id
    username = message.from_user.username or ""
    invited_by = int(args) if args.isdigit() and int(args) != user_id else None

    if not database.get_user(user_id):
        database.add_user(user_id, username, invited_by)
        database.log_event("register", user_id, f"invited_by:{invited_by}")

    if not await check_mandatory_channels(user_id):
        channels_links = ""
        for ch in config.COMP_CHANNELS:
            link = await get_channel_link(ch)
            channels_links += f"- {link}\n"
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

# كرر نفس فكرة استخراج args في أي handler آخر يستخدم get_args()
# مثال:
@dp.message()
async def handle_join(message: types.Message):
    args = ""
    parts = message.text.split(maxsplit=1)
    if len(parts) > 1:
        args = parts[1]
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
            channels_links = ""
            for ch in config.COMP_CHANNELS:
                link = await get_channel_link(ch)
                channels_links += f"- {link}\n"
            await bot.send_message(
                user_id,
                f"عليك الاشتراك في القنوات الإلزامية أولاً ليتم احتساب الإحالة.\n{channels_links}\n\nثم أعد إرسال /start.",
                disable_web_page_preview=True
            )

# باقي الهاندلرز كما هي


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
