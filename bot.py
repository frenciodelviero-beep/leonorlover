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
    await update.message.reply_text(
        '🎵 لینک اسپاتیفای رو بفرست تا آهنگ رو برات بفرستم!'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        '📖 لینک آهنگ اسپاتیفای رو بفرست، خودش دانلود و ارسال میشه.'
    )

def download_with_spotdl(url: str, output_dir: str) -> list:
    try:
        logger.info(f"Downloading: {url}")
        
        result = subprocess.run(
            ['spotdl', 'download', url, '--output', output_dir],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        logger.info(f"spotdl stdout: {result.stdout}")
        if result.stderr:
            logger.error(f"spotdl stderr: {result.stderr}")
        
        if result.returncode != 0:
            logger.error(f"spotdl failed with return code: {result.returncode}")
            return []
        
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
    message_text = update.message.text
    
    if not message_text:
        return
    
    match = re.search(SPOTIFY_PATTERN, message_text)
    
    if not match:
        return
    
    url = match.group(0)
    logger.info(f"Detected Spotify URL: {url}")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        audio_files = download_with_spotdl(url, temp_dir)
        
        if not audio_files:
            await update.message.reply_text('❌ آهنگ پیدا نشد.')
            return
        
        for audio_file in audio_files:
            try:
                song_name = Path(audio_file).stem
                file_size = os.path.getsize(audio_file)
                
                logger.info(f"Sending: {song_name} ({file_size} bytes)")
                
                if file_size > 50 * 1024 * 1024:
                    await update.message.reply_text(f'⚠️ فایل خیلی بزرگه ({file_size // (1024*1024)}MB)')
                    continue
                
                with open(audio_file, 'rb') as audio:
                    await update.message.reply_audio(
                        audio=audio,
                        caption=f'🎵 {song_name}',
                        title=song_name,
                        performer='Spotify'
                    )
                
                logger.info(f"Sent: {song_name}")
                
            except Exception as e:
                logger.error(f"Error sending {audio_file}: {e}")
                await update.message.reply_text('❌ خطا در ارسال فایل')
        
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text('❌ خطا در دانلود')
    
    finally:
        try:
            shutil.rmtree(temp_dir)
        except:
            pass

def main() -> None:
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not set!")
        return
    
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
