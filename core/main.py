import telebot
import os
import logging
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)
API_TOKEN = os.environ.get('API_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    logger.info("triggered welcome")
    bot.send_message(message.chat.id,"""hey man""")
    markup = InlineKeyboardMarkup(one_time_keyboard=True)
    button_google = InlineKeyboardButton("google",url="https://google.com")
    button_test = InlineKeyboardButton('Test',callback_data="Test")
    markup.add(button_google)
    markup.add(button_test)

    bot.send_message(message.chat.id, """Hi there :D""",reply_markup=markup)

@bot.callback_query_handler(func= lambda call:True)
def reply_call(call):
    if call.data == "Test":
        bot.answer_callback_query(call.id,"clicked on test",show_alert=True)




@bot.message_handler(func= lambda message: message.text == "Meow")
def send_Meow(message):
    bot.send_message(message.chat.id,"""hey meow meow""") 
@bot.message_handler(func= lambda message: message.text == "help")
def send_Meow(message):
    bot.send_message(message.chat.id,"""hey what do u need baby?""") 

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



@bot.message_handler(commands=['send_voice'])
def send_voice(message):
    voice_file = open("./files/voicee.mp3",'rb')  
    bot.send_chat_action(message.chat.id,action="upload_voice") 
    bot.send_voice(message.chat.id,voice_file)
    
@bot.message_handler(commands=['send_video'])
def send_video(message):
    video_file = open("./files/videoo.mp4",'rb')  
    bot.send_chat_action(message.chat.id,action="upload_video") 
    bot.send_video(message.chat.id,video_file)

@bot.message_handler(commands=['send_doc'])
def send_document(message):
    doc_file = open("./files/docc.pdf",'rb')  
    bot.send_chat_action(message.chat.id,action="upload_document") 
    bot.send_document(message.chat.id,doc_file)


bot.infinity_polling()