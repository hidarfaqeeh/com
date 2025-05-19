from aiogram import Router, types
from utils.db import get_user, add_user
from utils.misc import welcome_text, get_main_menu

router = Router()

@router.message(commands=["start"])
async def cmd_start(msg: types.Message):
    user = await get_user(msg.from_user.id)
    if not user:
        await add_user(msg.from_user)
    await msg.answer(welcome_text, reply_markup=get_main_menu())

def register(dp):
    dp.include_router(router)
