""" This script is related to the telegram API connection and commands
"""

# System Imports


# Third-party Imports
from telegram.ext import (Updater, CommandHandler)


# Local source tree Imports
from utils import read_telegram_config


def start(bot, update):
    message = 'Hello there, this is a particular Bot. My master is Artur ' \
              'Baruchi. If you want to talk to him, please check his github (' \
              'http://github.com/abaruchi). See you soon!'
    update.message.reply_text(message)


def main():
    """Run bot."""
    telegram_conf = read_telegram_config("config.ini")
    updater = Updater(telegram_conf["token"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    # dp.add_handler(CommandHandler("help", start))
    # dp.add_handler(CommandHandler("set", set_timer,
    #                               pass_args=True,
    #                               pass_job_queue=True,
    #                               pass_chat_data=True))
    # dp.add_handler(CommandHandler("unset", unset, pass_chat_data=True))

    # log all errors
    # dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
