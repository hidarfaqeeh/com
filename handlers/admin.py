from aiogram import Router, types
from aiogram.filters import Command
from database import get_all_users, ban_user, export_csv, get_cheat_reports

router = Router()

@router.message(Command("admin"))
async def admin_panel(msg: types.Message):
    await msg.answer("لوحة تحكم المشرف:\n1. عرض المتسابقين\n2. تصدير CSV\n3. مراجعة تقارير الغش\n4. استبعاد/إعادة مستخدم")

@router.message(Command("تصدير_csv"))
async def export(msg: types.Message):
    csv_data = export_csv()
    await msg.answer_document(types.InputFile(csv_data, filename="users.csv"))

@router.message(Command("استبعاد"))
async def ban(msg: types.Message):
    user_id = int(msg.text.split()[1])
    ban_user(user_id)
    await msg.answer(f"تم استبعاد المستخدم {user_id}")

@router.message(Command("تقارير_الغش"))
async def cheat(msg: types.Message):
    reports = get_cheat_reports()
    txt = "\n".join([f"{r['reported_user_id']} - {r['reason']}" for r in reports])
    await msg.answer(txt)

def register(dp):
    dp.include_router(router)
