from aiogram import Router, types
from utils.misc import get_contest_countdown

router = Router()

@router.message(lambda m: m.text == "العد التنازلي")
async def countdown(msg: types.Message):
    await msg.answer(get_contest_countdown())

def register(dp):
    dp.include_router(router)
