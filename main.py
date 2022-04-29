from datetime import datetime
import re #oh no
from types import new_class
from telegram import *
from telegram.ext import *
import constants # you should create constants.py file in bot directory and input api key and database path as variables there
from jsonhandler import *

DATABASE_PATH = constants.DATABASE_PATH #path to json file where all data is contained
TIME_REGEX = re.compile("[0-2]\d[.: ][0-5]\d[, ] ?[0-3]\d[/.][01]\d[/.]\d\d\d\d") # to filter incorrect time to prevent errors
TITLE, DESCRIPTION, DUETIME = range(3) # Conversation handler states
#---------Default keyboard----------
reply_keyboard = [['Create new task', 'My info'], ['View all tasks',  'View most urgent task'], ['Delete task', 'Credits']]
MAINMENU_KEYBOARD = ReplyKeyboardim
Markup(
            reply_keyboard, one_time_keyboard=False, input_field_placeholder='Press a button or write here to start using bot'
        )
#------End of default keyboard------
new_task = {}
is_creating = False

def start(update: Update, context: CallbackContext):
    if(not str(update.message.from_user.id) in LoadJson(DATABASE_PATH).keys()): #checking if user id already in database
        data = LoadJson(DATABASE_PATH) # if not, will create list for this id
        data[str(update.message.from_user.id)] = []
        DumpJson(DATABASE_PATH, data)
    
    update.message.reply_text(
    f"Hello {update.message.from_user.first_name}, I'm notifications bot. I can help you remember all your events and importnat things.",
    reply_markup=MAINMENU_KEYBOARD)

#-----Stuff for ConversationHandler-----
def start_task_creation(update: Update, context: CallbackContext):
    global is_creating
    is_creating = True
    update.message.reply_text(f"Ok {update.message.from_user.first_name}, let's make your task! You can cancel creation by sending /cancel.\nSend me task title...",
    reply_markup=ReplyKeyboardRemove())
    return TITLE

def got_title(update: Update, context: CallbackContext):
    if is_creating:
        global new_task
        new_task = {"title" : update.message.text}
        update.message.reply_text(f"Fine, now provide some description for {update.message.text.lower()} (if you're lazy, just type 'no')...")
        return DESCRIPTION
    else:
        print('oh no cringe')

def got_description(update: Update, context: CallbackContext):
    if is_creating:
        reply = update.message.text
        if not reply == 'no':
            global new_task
            new_task["description"] = update.message.text
            update.message.reply_text("Great! Now, finally, what is the deadline for your task (HH:MM DD/MM/YYYY)?")
        else:
            new_task["description"] = "No description provided."
            update.message.reply_text("Not surprising. Now, finally, what is the deadline for your task (HH:MM DD/MM/YYYY)?")
        return DUETIME

#time regex: [0-2]\d[.: ][0-5]\d[, ] ?[0-3]\d[/.][01]\d[/.]\d\d\d\d (12:34 12/12/2022 - matches)
def got_duetime(update: Update, context: CallbackContext):
    if is_creating:
        reply = update.message.text
        if TIME_REGEX.match(reply):
            global new_task
            new_task["duetime"] = reply
                        
            data = LoadJson(DATABASE_PATH)
            data[str(update.message.from_user.id)].append(new_task)
            DumpJson(DATABASE_PATH, data)
            update.message.reply_text("Done!", reply_markup=MAINMENU_KEYBOARD)
            return ConversationHandler.END            
        else:
            update.message.reply_text("Oops! I cannot understand this type of time, please try again.")
            return DUETIME
#----------End of this stuff----------

def todo_list(update: Update, context: CallbackContext):
    global is_creating
    is_creating = False
    data = LoadJson(DATABASE_PATH)
    id = update.message.from_user.id
    if(str(id) in data.keys()): # checks if user is in database (good to prevent strange errors) 
        if (not len(data.get(str(id))) == 0): # if there are any tasks
            for task in data.get(str(id)): # for each task
                update.message.reply_text(f"{task['title']}\n{task['description']}\n{task['duetime']}")
        else:
            update.message.reply_text("Oops, I cannot find any tasks for you!")
    else:
        print("cringe")

#-----ConversationHandler fallback-----
def cancel_creation(update: Update, context: CallbackContext):
    global is_creating
    is_creating = False
    update.message.reply_text("Ok.", reply_markup=MAINMENU_KEYBOARD)
    return ConversationHandler.END

def credits(update: Update, context: CallbackContext):
    global is_creating
    is_creating = False
    update.message.reply_text(open('credits.txt').read())

def main():
    print("Starting bot...")

    updater = Updater(constants.API_KEY)

    dispatcher = updater.dispatcher

    #-------------ConversationHandler---------------
    taskcr_conv_handler = ConversationHandler(entry_points = [MessageHandler(Filters.regex("^(Create first task|Create new task)$"), start_task_creation)],
                            states = {TITLE : [MessageHandler(Filters.text, got_title)],
                                    DESCRIPTION : [MessageHandler(Filters.text, got_description)],
                                    DUETIME : [MessageHandler(Filters.text, got_duetime)]},
                                    fallbacks = [CommandHandler("cancel", cancel_creation)],
                                    allow_reentry=True) 

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex("(?i)View all tasks"), todo_list))
    dispatcher.add_handler(MessageHandler(Filters.regex("(?i)cancel|break|stop"), cancel_creation), group=0)
    dispatcher.add_handler(MessageHandler(Filters.regex("(?i)credits|socials|creators|devs|developers"), credits))
    dispatcher.add_handler(taskcr_conv_handler)
    
    updater.start_polling()

    updater.idle()

main()


