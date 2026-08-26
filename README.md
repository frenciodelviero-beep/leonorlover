# 🎵 Spotify Telegram Bot

یک بات تلگرام برای دانلود و ارسال آهنگ‌ها از اسپاتیفای.

## ✨ امکانات

- ✅ پشتیبانی از لینک تک آهنگ، آلبوم و پلی‌لیست
- ✅ کار در گروه‌ها و چت خصوصی
- ✅ ارسال فایل صوتی با کیفیت بالا
- ✅ قابل استقرار در Railway

## 🚀 راه‌اندازی

### 1. ساخت بات تلگرام

1. به [@BotFather](https://t.me/BotFather) در تلگرام پیام بدید
2. دستور `/newbot` رو بزنید
3. اسم و یوزرنیم بات رو انتخاب کنید
4. توکن بات رو کپی کنید

### 2. تنظیمات اسپاتیفای (اختیاری)

**بدون کلاینت آیدی هم کار میکنه!** ولی اگه بخواید از اکانت خودتون استفاده کنید:

1. به [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) برید
2. یک اپلیکیشن جدید بسازید
3. Client ID و Client Secret رو کپی کنید

### 3. استقرار در Railway

#### روش اول: با GitHub

1. این ریپو رو به GitHub آپلود کنید
2. به [Railway.app](https://railway.app) برید
3. روی "New Project" کلیک کنید
4. "Deploy from GitHub repo" رو انتخاب کنید
5. ریپو رو انتخاب کنید
6. به بخش Variables برید و متغیر زیر رو اضافه کنید:

```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

(متغیرهای SPOTDL_CLIENT_ID و SPOTDL_CLIENT_SECRET اختیاری هستند)

#### روش دوم: با Railway CLI

```bash
# نصب Railway CLI
npm install -g @railway/cli

# لاگین
railway login

# ساخت پروژه جدید
railway init

# اضافه کردن متغیر اصلی
railway variables set TELEGRAM_BOT_TOKEN=your_token_here

# (اختیاری) اگه کلاینت آیدی اسپاتیفای دارید:
# railway variables set SPOTDL_CLIENT_ID=your_client_id_here
# railway variables set SPOTDL_CLIENT_SECRET=your_client_secret_here

# استقرار
railway up
```

### 4. اجرا محلی (برای تست)

```bash
# نصب وابستگی‌ها
pip install -r requirements.txt

# کپی فایل env
cp .env.example .env

# ویرایش فایل .env و اضافه کردن توکن‌ها
nano .env

# اجرا
python bot.py
```

## 📝 نحوه استفاده

1. بات رو به گروه اضافه کنید یا در چت خصوصی باهاش صحبت کنید
2. لینک اسپاتیفای رو بفرستید
3. صبر کنید تا آهنگ دانلود و ارسال بشه

مثال:
```
https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh
```

## ⚠️ نکات مهم

- **بدون کلاینت آیدی هم کار میکنه!** ولی محدودیت‌هایی داره
- دانلود آلبوم و پلی‌لیست ممکنه زمان‌بر باشه
- فایل‌های صوتی معمولاً با فرمت MP3 ارسال میشن
- اگه مشکلی پیش اومد، کلاینت آیدی اسپاتیفای رو اضافه کنید

## 🛠️ تکنولوژی‌ها

- Python 3.11
- python-telegram-bot
- spotdl
- yt-dlp
- FFmpeg

## 📄 لایسنس

MIT License
