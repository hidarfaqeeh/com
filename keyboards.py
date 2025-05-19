from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import config

def main_keyboard(user_id):
    ref_link = f"https://t.me/{config.BOT_USERNAME}?start={user_id}"
    keyboard = [
        [
            InlineKeyboardButton(text="اشترك بالمسابقة", callback_data="join"),
            InlineKeyboardButton(text="مشاركة الدعوة", switch_inline_query=ref_link)
        ],
        [
            InlineKeyboardButton(text="نقاطي", callback_data="mypoints"),
            InlineKeyboardButton(text="ملفي", callback_data="profile")
        ],
        [
            InlineKeyboardButton(text="أفضل 10", callback_data="top10"),
            InlineKeyboardButton(text="متصدرو اليوم", callback_data="topdaily")
        ],
        [
            InlineKeyboardButton(text="من دعاني؟", callback_data="whoinvited"),
            InlineKeyboardButton(
                text="قناة المسابقة",
                url=f"https://t.me/{config.EVENTS_CHANNEL.replace('-100','')}"
            )
        ],
        [
            InlineKeyboardButton(
                text="التواصل مع الإدارة",
                url=f"https://t.me/{config.ADMIN_ID}"
            )
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def points_keyboard():
    keyboard = [
        [InlineKeyboardButton(text="تحديث 🔄", callback_data="refresh")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
