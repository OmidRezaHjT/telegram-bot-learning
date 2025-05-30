import telebot
import os
import logging

API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)
logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

@bot.chat_join_request_handler()
def join_req_handler(request):
    logger.info(request)
    bot.approve_chat_join_request(request.chat.id,request.from_user.id)

@bot.message_handler(content_types='new_chat_members')
def handle_join_msg(message):
    for member in message.new_chat_members:
        bot.send_message(message.chat.id, f'Welcome to the group, {member.first_name}!')


@bot.message_handler(commands=['pin'])
def pin_msg(message):
    if message.reply_to_message:
        try:
            bot.pin_chat_message(
                chat_id=message.chat.id,
                message_id=message.reply_to_message.message_id
            )
        except Exception as e:
            bot.reply_to(message, f"❌ Failed to pin: {e}")
    else:
        bot.reply_to(message, "⚠️ You must reply to a message to pin it.")

bot.infinity_polling()
