import telebot
import os
import logging

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    logger.info("triggered welcome")
    bot.reply_to(message, """\
Hi there :D
""")
    
@bot.message_handler(commands=['setname'])
def setup_name(meessage):
    bot.send_message(meessage.chat.id,"what is your first name brother?")
    bot.register_next_step_handler(meessage,assign_first_name)

def assign_first_name(message):
    first_name = message.text
    bot.send_message(message.chat.id,f'what is ur last name {first_name}?')
    bot.register_next_step_handler(message,assign_last_name,first_name)

def assign_last_name(message,first_name):
    last_name = message.text
    bot.send_message(message.chat.id,f'well well welcome {first_name} {last_name} to my bot :)')





bot.infinity_polling()