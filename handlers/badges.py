from aiogram import Router, types
from utils.db import get_badge, get_level

router = Router()

@router.message(lambda m: m.text == "شاراتي")
async def badges(msg: types.Message):
    badge = await get_badge(msg.from_user.id)
    level = await get_level(msg.from_user.id)
    await msg.answer(f"شارتك: {badge}\nمستواك: {level}")

def register(dp):
    dp.include_router(router)
