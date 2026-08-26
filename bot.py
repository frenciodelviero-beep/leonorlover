import os
import re
import logging
import subprocess
import tempfile
import shutil
import glob
import json
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

SPOTIFY_PATTERN = r'https?://open\.spotify\.com/(track|album|playlist)/([a-zA-Z0-9]+)'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('🎵 لینک اسپاتیفای رو بفرست!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('لینک اسپاتیفای رو بفرست، آهنگ رو میفرستم.')

def get_spotify_info(url: str) -> dict:
    """Get track info from Spotify URL using spotdl."""
    try:
        result = subprocess.run(
            ['spotdl', 'url', url],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0 and result.stdout.strip():
            urls = result.stdout.strip().split('\n')
            return {'urls': [u.strip() for u in urls if u.strip()]}
        return None
    except Exception as e:
        logger.error(f"Error getting spotify info: {e}")
        return None

def download_audio(url: str, output_dir: str) -> list:
    """Download audio using yt-dlp."""
    try:
        logger.info(f"Downloading with yt-dlp: {url}")
        
        output_template = os.path.join(output_dir, '%(title)s.%(ext)s')
        
        result = subprocess.run(
            [
                'yt-dlp',
                '-x',  # Extract audio
                '--audio-format', 'mp3',
                '--audio-quality', '0',  # Best quality
                '-o', output_template,
                '--no-playlist',
                '--max-filesize', '50m',
                url
            ],
            capture_output=True,
            text=True,
            timeout=180
        )
        
        logger.info(f"yt-dlp stdout: {result.stdout}")
        if result.stderr:
            logger.warning(f"yt-dlp stderr: {result.stderr}")
        
        audio_files = []
        for ext in ['*.mp3', '*.m4a', '*.opus', '*.ogg', '*.wav', '*.webm']:
            audio_files.extend(glob.glob(os.path.join(output_dir, ext)))
        
        return audio_files
        
    except subprocess.TimeoutExpired:
        logger.error("yt-dlp timed out")
        return []
    except Exception as e:
        logger.error(f"yt-dlp error: {e}")
        return []

def download_with_spotdl(url: str, output_dir: str) -> list:
    """Download using spotdl."""
    try:
        logger.info(f"Downloading with spotdl: {url}")
        
        result = subprocess.run(
            ['spotdl', 'download', url, '--output', output_dir],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        logger.info(f"spotdl stdout: {result.stdout}")
        if result.stderr:
            logger.warning(f"spotdl stderr: {result.stderr}")
        
        audio_files = []
        for ext in ['*.mp3', '*.m4a', '*.opus', '*.ogg', '*.wav']:
            audio_files.extend(glob.glob(os.path.join(output_dir, ext)))
        
        return audio_files
        
    except Exception as e:
        logger.error(f"spotdl error: {e}")
        return []

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message_text = update.message.text
    
    if not message_text:
        return
    
    match = re.search(SPOTIFY_PATTERN, message_text)
    
    if not match:
        return
    
    url = match.group(0)
    content_type = match.group(1)
    
    logger.info(f"Processing: {url}")
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Method 1: Try spotdl download
        audio_files = download_with_spotdl(url, temp_dir)
        
        # Method 2: If spotdl fails, try getting URLs and using yt-dlp
        if not audio_files:
            logger.info("spotdl failed, trying yt-dlp method...")
            info = get_spotify_info(url)
            if info and 'urls' in info:
                for spotify_url in info['urls'][:3]:  # Limit to 3 tracks
                    files = download_audio(spotify_url, temp_dir)
                    audio_files.extend(files)
        
        if not audio_files:
            await update.message.reply_text('❌ آهنگ پیدا نشد. لینک رو چک کنید.')
            return
        
        # Send each audio file
        for audio_file in audio_files[:5]:  # Limit to 5 files
            try:
                song_name = Path(audio_file).stem
                file_size = os.path.getsize(audio_file)
                
                logger.info(f"Sending: {song_name} ({file_size} bytes)")
                
                if file_size > 50 * 1024 * 1024:
                    await update.message.reply_text(f'⚠️ فایل خیلی بزرگه')
                    continue
                
                if file_size < 1000:  # Less than 1KB, probably empty
                    logger.warning(f"File too small, skipping: {audio_file}")
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
    
    logger.info("Bot started!")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
