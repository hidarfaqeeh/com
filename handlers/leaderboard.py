from aiogram import Router, types
from utils.db import get_top10_users, get_leaderboard

router = Router()

@router.message(lambda m: m.text == "أفضل 10 متسابقين")
async def top10(msg: types.Message):
    top = await get_top10_users()
    msg_txt = "🏆 <b>أفضل 10 متسابقين:</b>\n"
    for i, user in enumerate(top, 1):
        msg_txt += f"{i}. {user['full_name']} — {user['points']} نقطة\n"
    await msg.answer(msg_txt)
    
@router.message(lambda m: m.text == "عرض المتسابقين تنازليًا")
async def leaderboard_desc(msg: types.Message):
    users = await get_leaderboard()
    msg_txt = "📋 <b>جميع المتسابقين (ترتيب تنازلي):</b>\n"
    for i, user in enumerate(users, 1):
        msg_txt += f"{i}. {user['full_name']} — {user['points']} نقطة\n"
    await msg.answer(msg_txt[:4000])

def register(dp):
    dp.include_router(router)
