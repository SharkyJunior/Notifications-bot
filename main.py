from telebot import *
from telebot import types
import constants
from jsonhandler import *

DATABASE_PATH = constants.Notifications_bot.DATABASE_PATH

bot = TeleBot(constants.Notifications_bot.API_KEY)

print("Starting bot...")

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    testbutton = types.KeyboardButton("Test")
    markup.add(testbutton)

    if(not LoadJson(DATABASE_PATH).contains(message.from_user)):
        data = LoadJson(DATABASE_PATH)
        data.Append(message.from_user)
        DumpJson(DATABASE_PATH, data)
    
    bot.send_message(message.chat.id,
    f"Hello {message.from_user.username}, I'm notifications bot. I can help you remember all your events and importnat things.",
    reply_markup = markup)

bot.polling(none_stop = True)
