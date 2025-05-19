from aiogram import Router

router = Router()

async def send_weekly_reminder(bot, users):
    for user in users:
        await bot.send_message(user['tg_id'], f"تذكير أسبوعي: ترتيبك الحالي {user['rank']}, نقاطك: {user['points']}")

def register(dp):
    pass
