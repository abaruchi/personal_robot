""" This script is related to the telegram API connection and commands
"""

# System Imports


# Third-party Imports
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)
from telegram import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove)


# Local source tree Imports
from utils import read_telegram_config
from api.traffic import TrafficInformation
from handlers import commands, messages

MY_LOCATION, OTHER_LOCATION, DIRECTION = range(3)


# Routines to handle Location
def lets_go(bot, update):
    """

    :param bot:
    :param update:
    :return:
    """
    message = """
Here we go again... Dude, I dont have a crystal ball!\n
Send me your location, before I give up helping you...\n    
    """

    bot.sendMessage(
        update.message.chat_id,
        text=message,
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Send My Location", request_location=True)]],
            one_time_keyboard=True
        )
    )
    return MY_LOCATION


def my_current_address(bot, update):
    gmaps = TrafficInformation()
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    coord_tuples = (latitude, longitude)
    address = gmaps.current_address(coord_tuples)
    addr_01 = address['street'] + "," + address['number'] + "-" + \
              address['neibor']
    return ConversationHandler.END


def cancel(bot, update):
    update.message.reply_text('Shit.. I always waste my time with you.. ',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

###############################


def main():
    """Run bot."""
    telegram_conf = read_telegram_config("config.ini")
    updater = Updater(telegram_conf["token"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", commands.start))
    dp.add_handler(CommandHandler("metro", commands.metro, pass_args=True))
    dp.add_handler(CommandHandler("cptm", commands.cptm, pass_args=True))
    dp.add_handler(CommandHandler("gohome", commands.go_home))
    dp.add_handler(CommandHandler("gowork", commands.go_work))

    dp.add_handler(CommandHandler("mylocation",
                                  commands.my_location_button,
                                  pass_args=True))
    dp.add_handler(MessageHandler(Filters.location,
                                  messages.coordinates_to_address))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('letsgo', lets_go)],
        states={
            MY_LOCATION: [MessageHandler(Filters.location,
                                         my_current_address)]
        },
        fallbacks=[CommandHandler('done', cancel)]
    )
    dp.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
