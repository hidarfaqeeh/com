from aiogram import Router, types
from utils.progress import get_user_progress_bar

router = Router()

@router.message(lambda m: m.text == "تقدمي")
async def progress(msg: types.Message):
    bar = await get_user_progress_bar(msg.from_user.id)
    await msg.answer(bar)

def register(dp):
    dp.include_router(router)