#!/bin/bash

echo "🎵 Spotify Telegram Bot"
echo "======================"

if [ ! -f .env ]; then
    cp .env.example .env
    echo "❌ لطفاً فایل .env رو ویرایش کنید و TELEGRAM_BOT_TOKEN رو بذارید"
    exit 1
fi

source .env

if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN تنظیم نشده!"
    exit 1
fi

echo "✅ توکن پیدا شد"
echo "🚀 در حال اجرا..."
echo ""

python bot.py
