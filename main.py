from telebot import *
from telegram import *
from telegram.ext import *
import constants # you should create constants.py file in bot directory and input api key and database path as variables there
from jsonhandler import *

DATABASE_PATH = constants.DATABASE_PATH


def start(update: Update, context: CallbackContext):

    if(not str(update.message.from_user.id) in LoadJson(DATABASE_PATH).keys()):
        data = LoadJson(DATABASE_PATH)
        data[update.message.from_user.id] = []
        DumpJson(DATABASE_PATH, data)
    
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
    f"Hello {update.message.from_user.first_name}, I'm notifications bot. I can help you remember all your events and importnat things.",
    reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Input '
        )
    )

def todo_list(update: Update, context: CallbackContext):
    data = LoadJson(DATABASE_PATH)
    id = update.message.from_user.id
    if(str(id) in data.keys()):
        if (not len(data.get(str(id))) == 0):
            for task in data.get(str(id)):
                update.message.reply_text(f"{task['name']}\n{task['description']}\n{task['duetime']}")
        else:
            update.message.reply_text("Oops, I cannot find any tasks for you!")
    else:
        print("cringe")

def main():
    print("Starting bot...")

    updater = Updater(constants.API_KEY)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("taskslist", todo_list))
    
    updater.start_polling()

    updater.idle()

main()


