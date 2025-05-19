import asyncio, logging, os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from handlers import (
    start, referral, points, leaderboard, countdown,
    subscription, notifications, user_progress, badges,
    weekly_reminder, challenges, admin
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(storage=MemoryStorage())

for handler in [start, referral, points, leaderboard, countdown, subscription,
                notifications, user_progress, badges, weekly_reminder, challenges, admin]:
    handler.register(dp)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
