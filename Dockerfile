# استخدم نسخة Python 3.11 الرسمية
FROM python:3.11-slim

# تعيين مجلد العمل داخل الحاوية
WORKDIR /app

# نسخ ملف المتطلبات أولًا لتسريع التخزين المؤقت
COPY requirements.txt .

# تثبيت المتطلبات
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# نسخ كل ملفات المشروع
COPY . .

# تعيين متغيرات البيئة إذا كانت موجودة
# ENV DATABASE_URL=your_database_url_here
# ENV OTHER_ENV=...

# تشغيل التطبيق باستخدام uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]