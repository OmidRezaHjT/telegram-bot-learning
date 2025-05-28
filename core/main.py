import telebot
import os
import logging
from yt_dlp import YoutubeDL

API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

DOWNLOAD_DIR = "downloads/"

if not os.path.exists(DOWNLOAD_DIR):
    os.makedirs(DOWNLOAD_DIR)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info("triggered welcome")
    bot.send_message(message.chat.id, "Hey send a link and I’ll download it for you :3")

def download_youtube_video(url, download_dir="downloads/"):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'quiet': True,
        'merge_output_format': 'mp4',
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        title = info.get('title', 'No Title')
        return filename, title

@bot.message_handler(func=lambda message: True)
def handle_url(message):
    url = message.text.strip()
    logger.info(f"Received URL: {url}")

    try:
        if "youtube.com" in url or "youtu.be" in url:
            file_path, title = download_youtube_video(url)
            with open(file_path, 'rb') as video:
                bot.send_document(
                    chat_id=message.chat.id,
                    document=video,
                    caption=title,
                    reply_parameters=message.id
                )
        else:
            bot.reply_to(message, "Only YouTube links are supported.")
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        bot.reply_to(message, "Problem downloading the requested file :C")

bot.infinity_polling()
