from aiogram import Router, types
from utils.db import get_user, generate_referral_link, check_subscription, add_points, log_event, add_user

router = Router()

@router.message(lambda m: m.text == "اشترك بالمسابقة")
async def join_competition(msg: types.Message):
    user = await get_user(msg.from_user.id)
    if not user["referral_link"]:
        link = await generate_referral_link(msg.from_user.id)
    else:
        link = user["referral_link"]
    await msg.answer(
        f"رابطك الخاص للمسابقة:\n{link}\n\nانسخه وشاركه مع أصدقائك!\nكل إحالة ناجحة = 100 نقطة.",
        reply_markup=types.ReplyKeyboardRemove()
    )

@router.message(lambda m: m.text.startswith("/start "))
async def handle_referral(msg: types.Message):
    inviter_id = int(msg.text.split(" ")[1])
    if inviter_id == msg.from_user.id:
        await msg.answer("لا يمكنك دعوة نفسك!")
        return
    user = await get_user(msg.from_user.id)
    if user and user["inviter_id"]:
        await msg.answer("تم تسجيلك من قبل، لا يمكن تغيير المحيل.")
        return
    if not await check_subscription(msg.from_user.id):
        await msg.answer("يرجى الاشتراك في القنوات أولاً.")
        return
    await add_user(msg.from_user, inviter_id=inviter_id)
    await add_points(inviter_id, 100)
    await log_event(inviter_id, "referral_success", f"أحال {msg.from_user.id}")
    await msg.bot.send_message(inviter_id, f"تهانينا! حصلت على 100 نقطة لإحالتك {msg.from_user.full_name}")

def register(dp):
    dp.include_router(router)
