from aiogram import Router, types
from utils.db import get_rank

router = Router()

async def notify_near_top10(bot, user_id):
    rank = await get_rank(user_id)
    if rank and rank <= 15:
        await bot.send_message(user_id, "أنت تقترب من دخول قائمة أفضل 10! استمر!")

async def send_winner_message(bot, winners):
    medals = ["🥇", "🥈", "🥉"]
    for i, user in enumerate(winners):
        await bot.send_message(user['tg_id'], f"مبروك! {medals[i]} فزت في مسابقة الإحالات!")

def register(dp):
    pass
