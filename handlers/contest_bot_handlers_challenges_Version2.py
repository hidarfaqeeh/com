from aiogram import Router, types
from utils.db import get_active_challenges, join_challenge

router = Router()

@router.message(lambda m: m.text == "تحدياتي")
async def challenges(msg: types.Message):
    active = await get_active_challenges()
    txt = "🗓️ تحدياتك الحالية:\n"
    for ch in active:
        txt += f"- {ch['description']} ({ch['type']})\n"
    await msg.answer(txt)

@router.message(lambda m: m.text.startswith("انضم للتحدي"))
async def join(msg: types.Message):
    challenge_id = int(msg.text.split()[-1])
    await join_challenge(msg.from_user.id, challenge_id)
    await msg.answer("تم انضمامك للتحدي!")

def register(dp):
    dp.include_router(router)