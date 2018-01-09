""" This script is related to the telegram API connection and commands
"""

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from handlers import commands, conversations, messages
from utils import read_telegram_config

###############################


def main():
    """Run bot."""
    telegram_conf = read_telegram_config("config.ini")
    updater = Updater(telegram_conf["token"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('letsgo', conversations.lets_go)],
        states={
            conversations.MY_LOCATION:
                [MessageHandler(Filters.location,
                                conversations.my_current_address,
                                pass_user_data=True)],
            conversations.OTHER_LOCATION:
                [MessageHandler(Filters.text,
                               conversations.my_other_address,
                               pass_user_data=True)],
            conversations.DIRECTION:
                [MessageHandler(Filters.text,
                                conversations.my_directions,
                                pass_user_data=True)]
        },
        fallbacks=[CommandHandler('done', conversations.cancel)]
    )
    dp.add_handler(conv_handler)

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

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
