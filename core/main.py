import telebot
import os
import logging
from telebot.types import InlineQueryResultArticle,InputTextMessageContent
import requests
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)


DOWNLOAD_DIRS= "downloads/"

if not os.path.exists("downloads"):
    os.makedirs("downloads")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    logger.info("triggered welcome")
    bot.send_message(message.chat.id,"""Hey send a link and i download it for you :3""")

def download_file(url):
    local_filename = url.split('/')[-1]
    file_path = DOWNLOAD_DIRS + local_filename
    with requests.get(url,stream=True) as r:
        r.raise_for_status()
        with open(file_path,'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return(file_path)

@bot.message_handler(func=lambda message:True)
def download_file_url(message):
    logger.info(message.text)
    url = message.text
    try:
        file_path = download_file(url)
        bot.send_document(chat_id=message.chat.id,reply_to_message_id=message.id, document=open(file_path,'rb'), caption="Enjoy :D")
    except:
        bot.reply_to(message, text="Problem downloading the requested file :C")

bot.infinity_polling()