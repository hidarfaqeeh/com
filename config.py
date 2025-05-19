import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "7533295302:AAEgqpo4SXf0K5IH4bFTWfNZc5LSxMcHE4E")
ADMIN_ID = int(os.getenv("ADMIN_ID", "6194809472"))
EVENTS_CHANNEL = os.getenv("EVENTS_CHANNEL", "-1001861242334")  # معرف قناة الأحداث
COMP_CHANNELS = [
    "-1001470989107",  # معرف القناة الإلزامية الأولى
    "-100222222222",  # معرف القناة الإلزامية الثانية (يمكن حذفها أو زيادتها)
]
COMPETITION_END = os.getenv("COMPETITION_END", "2025-12-31 23:59:59")  # نهاية المسابقة (تاريخ/وقت)
REFERRAL_POINTS = 100  # نقاط لكل إحالة ناجحة
TOP_LIMIT = 10  # عدد أفضل المتسابقين في القائمة العلوية

# اسم مستخدم البوت (حدثه بعد إنشاء البوت)
BOT_USERNAME = os.getenv("BOT_USERNAME", "Competyebot")
