import os
import re
import logging
import asyncio
import tempfile
import shutil
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from spotdl import Spotdl

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize SpotDL client (works without credentials too!)
SPOTDL_CLIENT_ID = os.getenv('SPOTDL_CLIENT_ID', '')
SPOTDL_CLIENT_SECRET = os.getenv('SPOTDL_CLIENT_SECRET', '')

# Initialize spotdl client - if credentials are empty, spotdl uses its own
if SPOTDL_CLIENT_ID and SPOTDL_CLIENT_SECRET:
    spotdl_client = Spotdl(
        client_id=SPOTDL_CLIENT_ID,
        client_secret=SPOTDL_CLIENT_SECRET
    )
    logger.info("SpotDL initialized with custom credentials")
else:
    spotdl_client = Spotdl()
    logger.info("SpotDL initialized with default credentials (no API keys needed)")

# Spotify URL pattern
SPOTIFY_PATTERN = r'https?://open\.spotify\.com/(track|album|playlist)/([a-zA-Z0-9]+)'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        '🎵 سلام! من بات دانلود آهنگ از اسپاتیفای هستم.\n\n'
        'لینک آهنگ، آلبوم یا پلی‌لیست اسپاتیفای رو بفرست تا برات دانلود کنم!\n\n'
        'مثال:\n'
        'https://open.spotify.com/track/xxxxx'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        '📖 راهنما:\n\n'
        '1. لینک اسپاتیفای رو بفرست\n'
        '2. صبر کن تا آهنگ دانلود بشه\n'
        '3. فایل صوتی برات ارسال میشه\n\n'
        'پشتیبانی از:\n'
        '• تک آهنگ (track)\n'
        '• آلبوم (album)\n'
        '• پلی‌لیست (playlist)'
    )

async def download_spotify_track(url: str, output_dir: str) -> list:
    """Download track(s) from Spotify URL using spotdl."""
    try:
        # Download the song
        songs = spotdl_client.download(url)
        return songs
    except Exception as e:
        logger.error(f"Error downloading: {e}")
        return []

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages and check for Spotify links."""
    message_text = update.message.text
    
    if not message_text:
        return
    
    # Check for Spotify URL
    match = re.search(SPOTIFY_PATTERN, message_text)
    
    if not match:
        return
    
    url = match.group(0)
    content_type = match.group(1)
    
    # Send processing message
    processing_msg = await update.message.reply_text('⏳ در حال دانلود آهنگ... لطفاً صبر کنید.')
    
    # Create temporary directory for downloads
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Change to temp directory for download
        original_dir = os.getcwd()
        os.chdir(temp_dir)
        
        # Download the track(s)
        songs = await download_spotify_track(url, temp_dir)
        
        if not songs:
            await processing_msg.edit_text('❌ خطا در دانلود آهنگ. لطفاً لینک رو چک کنید.')
            return
        
        # Find downloaded files
        downloaded_files = list(Path(temp_dir).glob('*.mp3')) + list(Path(temp_dir).glob('*.m4a')) + list(Path(temp_dir).glob('*.opus'))
        
        if not downloaded_files:
            await processing_msg.edit_text('❌ فایل صوتی پیدا نشد.')
            return
        
        # Send each audio file
        await processing_msg.edit_text(f'✅ {len(downloaded_files)} آهنگ پیدا شد. در حال ارسال...')
        
        for audio_file in downloaded_files:
            try:
                # Get song info for caption
                song_name = audio_file.stem
                caption = f'🎵 {song_name}'
                
                # Send audio file
                with open(audio_file, 'rb') as audio:
                    await update.message.reply_audio(
                        audio=audio,
                        caption=caption,
                        title=song_name,
                        duration=0  # Let Telegram detect duration
                    )
                
                logger.info(f"Sent audio: {song_name}")
                
            except Exception as e:
                logger.error(f"Error sending audio {audio_file}: {e}")
                await update.message.reply_text(f'⚠️ خطا در ارسال فایل: {audio_file.name}')
        
        # Delete processing message
        await processing_msg.delete()
        
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        await processing_msg.edit_text('❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.')
    
    finally:
        # Change back to original directory
        os.chdir(original_dir)
        
        # Cleanup temp directory
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            logger.error(f"Error cleaning up temp dir: {e}")

def main() -> None:
    """Start the bot."""
    # Get bot token from environment variable
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return
    
    # Create the Application
    application = Application.builder().token(token).build()
    
    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Run the bot
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
