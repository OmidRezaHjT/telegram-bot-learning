import telebot
import os
import logging
import io
from PIL import Image
from telebot.types import InlineQueryResultArticle , InputTextMessageContent

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
    bot.send_message(message.chat.id, "Hey send a photo and i will compress it for you :3")

@bot.message_handler(content_types=['photo'])
def pic_comp(message):
    photo = message.photo[-1]
    file_info = bot.get_file(photo.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image = Image.open(io.BytesIO(downloaded_file))

    file_path = os.path.join(DOWNLOAD_DIR, f"{photo.file_id}_compressed.jpg")

    image.save(file_path, format="JPEG", optimize=True, quality=30)
    with open(file_path, 'rb') as photo_file:
        bot.send_chat_action(chat_id=message.chat.id,action='upload_photo')
        bot.send_photo(message.chat.id, photo_file, caption="Enjoy 💙")

@bot.inline_handler(func= lambda query: True)
def query_handler(query):
    logger.info(query)
    results=[]
    results.append(
        InlineQueryResultArticle(
            id='1',
            title='Join the bot',
            input_message_content=InputTextMessageContent(message_text='Join the bot'),
            url='https://t.me/LrnPy044Bot'
            )
        
    )
    results.append(
        InlineQueryResultArticle(
            id='2',
            title='check website',
            input_message_content=InputTextMessageContent(message_text='https://camoshan.ir'),
            url='https://camoshan.ir'
            )
        
    )
    bot.answer_inline_query(query.id,results,cache_time=0)
    
bot.infinity_polling()
