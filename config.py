import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "ضع_توكن_البوت_هنا")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))
EVENTS_CHANNEL = os.getenv("EVENTS_CHANNEL", "-100123456789")  # معرف قناة الأحداث
COMP_CHANNELS = [
    "-100111111111",  # معرف القناة الإلزامية الأولى
    "-100222222222",  # معرف القناة الإلزامية الثانية (يمكن حذفها أو زيادتها)
]
COMPETITION_END = os.getenv("COMPETITION_END", "2025-12-31 23:59:59") # نهاية المسابقة (تاريخ/وقت)
REFERRAL_POINTS = 100  # نقاط لكل إحالة ناجحة
TOP_LIMIT = 10  # عدد أفضل المتسابقين في القائمة العلوية
