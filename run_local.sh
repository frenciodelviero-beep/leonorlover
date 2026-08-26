#!/bin/bash

# Script to run the bot locally for testing

echo "🎵 Spotify Telegram Bot - Local Test"
echo "===================================="

# Check if .env file exists
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    echo "Creating .env from example..."
    cp .env.example .env
    echo "Please edit .env and add your TELEGRAM_BOT_TOKEN"
    exit 1
fi

# Source .env file
source .env

# Check if token is set
if [ -z "$TELEGRAM_BOT_TOKEN" ]; then
    echo "❌ TELEGRAM_BOT_TOKEN not set in .env!"
    echo "Please edit .env and add your bot token"
    exit 1
fi

echo "✅ Token found"

# Test spotdl
echo ""
echo "Testing spotdl installation..."
if command -v spotdl &> /dev/null; then
    echo "✅ spotdl is installed"
    spotdl --version
else
    echo "❌ spotdl not found! Installing..."
    pip install spotdl
fi

echo ""
echo "Starting bot..."
echo "Press Ctrl+C to stop"
echo ""

python bot.py
