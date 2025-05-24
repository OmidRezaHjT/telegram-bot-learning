import telebot
import os
import logging
import yt_dlp

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

DOWNLOAD_DIRS = "downloads/"

if not os.path.exists(DOWNLOAD_DIRS):
    os.makedirs(DOWNLOAD_DIRS)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info("triggered welcome")
    bot.send_message(message.chat.id, "Hey! Send me a YouTube link and I'll download the video for you :3")

def download_youtube_video(url, download_dir=DOWNLOAD_DIRS):
    ydl_opts = {
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4', 
        'quiet': True, 
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    return filename

@bot.message_handler(func=lambda message: True)
def download_file_url(message):
    url = message.text.strip()
    logger.info(f"Received URL: {url}")
    bot.send_message(message.chat.id,"downloading..")
    try:
        if "youtube.com" in url or "youtu.be" in url:
            file_path = download_youtube_video(url)
        else:
            bot.reply_to(message, "Only YouTube links are supported for now.")
            return

        with open(file_path, 'rb') as doc:
            bot.send_document(chat_id=message.chat.id, reply_to_message_id=message.message_id, document=doc, caption="Enjoy your video! 🎉")

        os.remove(file_path)

    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        bot.reply_to(message, text="Problem downloading the requested video :C")

bot.infinity_polling()