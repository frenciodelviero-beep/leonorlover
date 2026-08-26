# 🎵 Spotify Telegram Bot

یک بات تلگرام برای دانلود و ارسال آهنگ‌ها از اسپاتیفای.

## ✨ امکانات

- ✅ پشتیبانی از لینک تک آهنگ، آلبوم و پلی‌لیست
- ✅ کار در گروه‌ها و چت خصوصی
- ✅ ارسال فایل صوتی با کیفیت بالا
- ✅ قابل استقرار در Railway
- ✅ **بدون نیاز به کلاینت آیدی اسپاتیفای**

## 🚀 راه‌اندازی

### 1. ساخت بات تلگرام

1. به [@BotFather](https://t.me/BotFather) در تلگرام پیام بدید
2. دستور `/newbot` رو بزنید
3. اسم و یوزرنیم بات رو انتخاب کنید
4. توکن بات رو کپی کنید

### 2. استقرار در Railway

#### روش اول: با GitHub (پیشنهادی)

1. این ریپو رو به GitHub آپلود کنید
2. به [Railway.app](https://railway.app) برید
3. روی "New Project" کلیک کنید
4. "Deploy from GitHub repo" رو انتخاب کنید
5. ریپو رو انتخاب کنید
6. به بخش Variables برید و متغیر زیر رو اضافه کنید:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

7. روی "Deploy" کلیک کنید

#### روش دوم: با Railway CLI

```bash
# نصب Railway CLI
npm install -g @railway/cli

# لاگین
railway login

# ساخت پروژه جدید
railway init

# اضافه کردن متغیر
railway variables set TELEGRAM_BOT_TOKEN=your_token_here

# استقرار
railway up
```

### 3. اجرا محلی (برای تست)

```bash
# نصب وابستگی‌ها
pip install -r requirements.txt

# کپی فایل env
cp .env.example .env

# ویرایش فایل .env و اضافه کردن توکن
nano .env

# اجرا
python bot.py
```

یا از اسکریپت آماده استفاده کنید:
```bash
chmod +x run_local.sh
./run_local.sh
```

## 📝 نحوه استفاده

1. بات رو به گروه اضافه کنید یا در چت خصوصی باهاش صحبت کنید
2. لینک اسپاتیفای رو بفرستید
3. صبر کنید تا آهنگ دانلود و ارسال بشه

مثال:
```
https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh
```

## 🔧 عیب‌یابی

### بات جواب نمیده؟
- چک کنید `TELEGRAM_BOT_TOKEN` درست تنظیم شده باشه
- چک کنید بات در حال اجرا باشه (لاگ‌ها رو ببینید)

### آهنگ دانلود نمیشه؟
- spotdl ممکنه بعضی آهنگ‌ها رو پیدا نکنه
- لینک رو چک کنید معتبر باشه
- لاگ‌های Railway رو ببینید برای جزئیات خطا

### فایل ارسال نمیشه؟
- حداکثر حجم فایل تلگرام 50MB هست
- فرمت‌های پشتیبانی شده: MP3, M4A, OGG, WAV

## 📊 لاگ‌ها

برای دیدن لاگ‌ها در Railway:
1. به پروژه برید
2. روی "Deployments" کلیک کنید
3. آخرین دیپلویمنت رو انتخاب کنید
4. بخش "Build Logs" و "Deploy Logs" رو ببینید

## 🛠️ تکنولوژی‌ها

- Python 3.11
- python-telegram-bot 20.7
- spotdl 4.2.5
- yt-dlp
- FFmpeg

## 📄 لایسنس

MIT License
