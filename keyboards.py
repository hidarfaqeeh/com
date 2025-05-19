from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

def main_keyboard(user_id):
    ref_link = f"https://t.me/{config.BOT_USERNAME}?start={user_id}"
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton("اشترك بالمسابقة", callback_data="join"),
        InlineKeyboardButton("مشاركة الدعوة", switch_inline_query=ref_link),
        InlineKeyboardButton("نقاطي", callback_data="mypoints"),
        InlineKeyboardButton("ملفي", callback_data="profile"),
        InlineKeyboardButton("أفضل 10", callback_data="top10"),
        InlineKeyboardButton("متصدرو اليوم", callback_data="topdaily"),
        InlineKeyboardButton("من دعاني؟", callback_data="whoinvited"),
        InlineKeyboardButton("قناة المسابقة", url=f"https://t.me/{config.EVENTS_CHANNEL.replace('-100','')}")
    )
    kb.add(InlineKeyboardButton("التواصل مع الإدارة", url=f"https://t.me/{config.ADMIN_ID}"))
    return kb

def points_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("تحديث 🔄", callback_data="refresh"))
    return kb
