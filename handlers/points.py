from aiogram import Router, types
from utils.db import get_points, get_rank, get_badge

router = Router()

@router.message(lambda m: m.text == "نقاطي")
async def my_points(msg: types.Message):
    points = await get_points(msg.from_user.id)
    rank = await get_rank(msg.from_user.id)
    badge = await get_badge(msg.from_user.id)
    await msg.answer(f"نقاطك: <b>{points}</b>\nترتيبك: <b>{rank}</b>\nشارتك: {badge}")

def register(dp):
    dp.include_router(router)
