import telebot
import os
import logging
from telebot.types import InlineQueryResultArticle,InputTextMessageContent

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    logger.info("triggered welcome")
    bot.send_message(message.chat.id,"""hey man""")


@bot.inline_handler(func=lambda query:True )
def query_handler(query):
    logger.info(query)
    results=[]
    results.append(
        InlineQueryResultArticle(
            id='1',
            title='test',
            input_message_content=InputTextMessageContent(message_text='this is a response'),
            description='this is a description'
        )
    
    )
    results.append(
        InlineQueryResultArticle(
            id='2',
            title='join the bot',
            input_message_content=InputTextMessageContent(message_text='join the bot'),
            url='https://t.me/LrnPy044Bot'
        )
    )
    bot.answer_inline_query(query.id,results,cache_time=0)

bot.infinity_polling()