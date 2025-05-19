from aiogram import Router, types
from utils.db import check_subscription, get_mandatory_channels

router = Router()

@router.message(lambda m: m.text == "تحقق الاشتراك")
async def check_sub(msg: types.Message):
    if await check_subscription(msg.from_user.id):
        await msg.answer("✅ تم التأكد من اشتراكك.")
    else:
        channels = await get_mandatory_channels()
        await msg.answer("❌ يجب الاشتراك في القنوات التالية:\n" + "\n".join(channels))

def register(dp):
    dp.include_router(router)
