import os
import re
import logging
import subprocess
import tempfile
import shutil
import glob
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Spotify URL pattern
SPOTIFY_PATTERN = r'https?://open\.spotify\.com/(track|album|playlist)/([a-zA-Z0-9]+)'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text(
        '🎵 سلام! من بات دانلود آهنگ از اسپاتیفای هستم.\n\n'
        'لینک آهنگ، آلبوم یا پلی‌لیست اسپاتیفای رو بفرست تا برات دانلود کنم!\n\n'
        'مثال:\n'
        'https://open.spotify.com/track/4iV5W9uYEdYUVa79Axb7Rh'
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

def download_with_spotdl(url: str, output_dir: str) -> list:
    """Download track(s) using spotdl command line."""
    try:
        logger.info(f"Downloading: {url}")
        logger.info(f"Output dir: {output_dir}")
        
        # Run spotdl command
        result = subprocess.run(
            ['spotdl', 'download', url, '--output', output_dir],
            capture_output=True,
            text=True,
            timeout=300  # 5 minutes timeout
        )
        
        logger.info(f"spotdl stdout: {result.stdout}")
        if result.stderr:
            logger.error(f"spotdl stderr: {result.stderr}")
        
        if result.returncode != 0:
            logger.error(f"spotdl failed with return code: {result.returncode}")
            return []
        
        # Find downloaded files
        audio_files = []
        for ext in ['*.mp3', '*.m4a', '*.opus', '*.ogg', '*.wav']:
            audio_files.extend(glob.glob(os.path.join(output_dir, ext)))
        
        logger.info(f"Found audio files: {audio_files}")
        return audio_files
        
    except subprocess.TimeoutExpired:
        logger.error("spotdl download timed out")
        return []
    except Exception as e:
        logger.error(f"Error running spotdl: {e}")
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
    
    logger.info(f"Detected Spotify {content_type}: {url}")
    
    # Send processing message
    processing_msg = await update.message.reply_text('⏳ در حال دانلود آهنگ... لطفاً صبر کنید.')
    
    # Create temporary directory for downloads
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Download the track(s)
        audio_files = download_with_spotdl(url, temp_dir)
        
        if not audio_files:
            await processing_msg.edit_text('❌ خطا در دانلود آهنگ. لطفاً لینک رو چک کنید.')
            return
        
        # Send each audio file
        await processing_msg.edit_text(f'✅ {len(audio_files)} آهنگ پیدا شد. در حال ارسال...')
        
        for audio_file in audio_files:
            try:
                # Get song name from filename
                song_name = Path(audio_file).stem
                file_size = os.path.getsize(audio_file)
                
                logger.info(f"Sending: {song_name} ({file_size} bytes)")
                
                # Check file size (Telegram limit is 50MB)
                if file_size > 50 * 1024 * 1024:
                    await update.message.reply_text(f'⚠️ فایل {song_name} خیلی بزرگه ({file_size // (1024*1024)}MB). حداکثر 50MB.')
                    continue
                
                # Send audio file
                with open(audio_file, 'rb') as audio:
                    await update.message.reply_audio(
                        audio=audio,
                        caption=f'🎵 {song_name}',
                        title=song_name,
                        performer='Spotify Download'
                    )
                
                logger.info(f"Successfully sent: {song_name}")
                
            except Exception as e:
                logger.error(f"Error sending audio {audio_file}: {e}")
                await update.message.reply_text(f'⚠️ خطا در ارسال فایل: {Path(audio_file).name}')
        
        # Delete processing message
        try:
            await processing_msg.delete()
        except:
            pass
        
    except Exception as e:
        logger.error(f"Error in handle_message: {e}")
        await processing_msg.edit_text('❌ خطایی رخ داد. لطفاً دوباره تلاش کنید.')
    
    finally:
        # Cleanup temp directory
        try:
            shutil.rmtree(temp_dir)
            logger.info(f"Cleaned up temp dir: {temp_dir}")
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
