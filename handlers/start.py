from aiogram import Router, types
from aiogram.filters import Command
from utils.db import get_user, add_user
from utils.misc import welcome_text, get_main_menu

router = Router()

@router.message(Command("start"))
async def cmd_start(msg: types.Message):
    user = await get_user(msg.from_user.id)
    if not user:
        await add_user(msg.from_user)
    await msg.answer(welcome_text, reply_markup=get_main_menu())

def register(dp):
    dp.include_router(router)
