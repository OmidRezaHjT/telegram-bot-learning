import telebot
import os
import logging

API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

@bot.message_handler(func=lambda message:message.chat.type in ["supergroup","group"])
def handle_gp(message):
    logger.info("triggered gp")
    

@bot.message_handler(func= lambda message:message.chat.type in ["private"])
def handle_pv(message):
    logger.info("triggered pv")

@bot.chat_join_request_handler()
def join_req_handler(request):
    logger.info(request)
    bot.approve_chat_join_request(request.chat.id,request.from_user.id)

@bot.message_handler(content_types='new_chat_members')
def handle_join_msg(message):
    for member in message.new_chat_members:
        bot.send_message(message.chat.id, f'Welcome to the group, {member.first_name}!')

bot.infinity_polling()
