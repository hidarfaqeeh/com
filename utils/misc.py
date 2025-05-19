from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
welcome_text = "👋 أهلاً بك في مسابقة الإحالات الكبرى!\n- اشترك في القنوات الإجبارية\n- احصل على رابطك الخاص وابدأ بإحالة أصدقائك\n- اجمع النقاط وتصدر الترتيب\n\nاختر من القائمة:"

def get_main_menu():
    kb = [
        [KeyboardButton(text="اشترك بالمسابقة")],
        [KeyboardButton(text="نقاطي"), KeyboardButton(text="أفضل 10 متسابقين")],
        [KeyboardButton(text="شاراتي"), KeyboardButton(text="تقدمي")],
        [KeyboardButton(text="عرض المتسابقين تنازليًا"), KeyboardButton(text="العد التنازلي")],
        [KeyboardButton(text="تحدياتي"), KeyboardButton(text="تحقق الاشتراك")]
    ]
    return ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

def get_contest_countdown():
    from datetime import datetime
    from os import getenv
    end = datetime.fromisoformat(getenv("CONTEST_END_TIMESTAMP"))
    remain = end - datetime.utcnow()
    return f"الوقت المتبقي: {remain.days} يوم، {remain.seconds//3600} ساعة."