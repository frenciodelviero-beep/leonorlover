# 🎵 Spotify Telegram Bot

بات تلگرام برای دانلود آهنگ از اسپاتیفای.

## ✨ قابلیت‌ها

- ✅ کار در گروه و چت خصوصی
- ✅ پشتیبانی از track، album، playlist
- ✅ ارسال فایل MP3
- ✅ بدون نیاز به API اسپاتیفای

## 🚀 استقرار در Railway

### 1. توکن بات بگیرید
به @BotFather برید و `/newbot` بزنید.

### 2. آپلود در GitHub
این پوشه رو به GitHub آپلود کنید.

### 3. اتصال به Railway
1. به railway.app برید
2. New Project → Deploy from GitHub repo
3. ریپو رو انتخاب کنید
4. به Variables برید و اضافه کنید:
   ```
   TELEGRAM_BOT_TOKEN=توکن_بات
   ```
5. Deploy کنید

## 🧪 تست محلی

```bash
pip install -r requirements.txt
cp .env.example .env
# ویرایش .env و اضافه کردن توکن
python bot.py
```

یا:
```bash
chmod +x run_local.sh
./run_local.sh
```

## 📝 استفاده

لینک اسپاتیفای رو بفرستید:
```
https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh
```

بات خودش دانلود و ارسال میکنه.

## 🔧 عیب‌یابی

اگه کار نکرد:
1. لاگ‌های Railway رو چک کنید
2. `test_download.py` رو اجرا کنید
3. مطمئن بشید ffmpeg نصبه

## 📦 وابستگی‌ها

- python-telegram-bot 20.7
- spotdl 4.2.5
- yt-dlp
- ffmpeg
