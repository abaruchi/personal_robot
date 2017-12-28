""" This script is related to the telegram API connection and commands
"""

# System Imports


# Third-party Imports
from telegram.ext import (Updater, CommandHandler)


# Local source tree Imports
from utils import (read_telegram_config, Messages)
from api.subway import (GetSubwayLineStatus, GetCPTMStatus)


def start(bot, update):
    message = 'Hello there, this is a particular Bot. My master is Artur ' \
              'Baruchi. If you want to talk to him, please check his github (' \
              'http://github.com/abaruchi). See you soon!'
    update.message.reply_text(message)


def metro(bot, update, args):
    """

    :param bot:
    :param update:
    :param args:
    :return:
    """
    arg_size = len(args)
    if arg_size == 1:
        metro_stat = GetSubwayLineStatus()
        if args[0] == "all":
            msg_dict = metro_stat.all_subway_lines_status()
            message = ""
            for line, status in msg_dict.items():
                message = line + ": " + status + "\n" + message
            bot.send_message(
                chat_id=update.message.chat_id,
                text=message)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                text=Messages.metro_usage_help())


def cptm(bot, update, args):
    """

    :param bot:
    :param update:
    :param args:
    :return:
    """
    arg_size = len(args)
    if arg_size == 1:
        cptm_stat = GetCPTMStatus()
        if args[0] == "all":
            msg_dict = cptm_stat.all_cptm_lines_status()
            print(msg_dict)
            message = ""
            for line, status in msg_dict.items():
                message = line + ": " + status + "\n" + message
            bot.send_message(
                chat_id=update.message.chat_id,
                text=message)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                text=Messages.cptm_usage_help())

def main():
    """Run bot."""
    telegram_conf = read_telegram_config("config.ini")
    updater = Updater(telegram_conf["token"])

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("metro", metro, pass_args=True))
    dp.add_handler(CommandHandler("cptm", cptm, pass_args=True))

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
