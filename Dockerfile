# استخدم صورة بايثون رسمية خفيفة
FROM python:3.11-slim

# تعيين مجلد العمل
WORKDIR /app

# نسخ متطلبات البايثون
COPY requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ جميع الملفات البرمجية
COPY . .

# فتح المنفذ (اختياري، لو لديك لوحات ويب)
EXPOSE 8080

# الأمر الرئيسي لتشغيل البوت
CMD ["python", "bot.py"]
