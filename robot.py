""" This script is related to the telegram API connection and commands
"""

# System Imports


# Third-party Imports
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
from telegram import (KeyboardButton, ReplyKeyboardMarkup)


# Local source tree Imports
from utils import (read_telegram_config, Messages)
from api.subway import (GetSubwayLineStatus, GetCPTMStatus)


def start(bot, update):
    user = update.message.from_user
    update.message.reply_text(Messages.start_message(user))


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

        elif args[0] == "azul":
            stat = metro_stat.blue_line_status()
            message = "Linha Azul: " + stat
            bot.send_message(
                chat_id=update.message.chat_id,
                text=message)

        elif args[0] == "vermelha":
            stat = metro_stat.red_line_status()
            message = "Linha Vermelha: " + stat
            bot.send_message(
                chat_id=update.message.chat_id,
                text=message)

        elif args[0] == "amarela":
            stat = metro_stat.yellow_line_status()
            message = "Linha Amarela: " + stat
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
            message = ""
            for line, status in msg_dict.items():
                message = line + ": " + status + "\n" + message
            bot.send_message(
                chat_id=update.message.chat_id,
                text=message)
        elif args[0] == "esmeralda":
            stat = cptm_stat.esmeralda_line_status()
            message = "Linha Esmeralda: " + stat
            bot.send_message(
                chat_id=update.message.chat_id,
                text=message)
    else:
        bot.send_message(chat_id=update.message.chat_id,
                text=Messages.cptm_usage_help())


def test_loc(bot, update, args):
    """

    :param bot:
    :param update:
    :param args:
    :return:
    """
    print("AAAA")
    location_kb = KeyboardButton(text="send location",
                                 request_location=True)
    reply_markup = ReplyKeyboardMarkup(location_kb, one_time_keyboard=True)
    update.message.reply_text(
        "Would you mind sharing your location with me?",
        reply_markup=reply_markup
    )
    # bot.sendMessage(
    #     update.message.chat_id,
    #     text='location',
    #     reply_markup=ReplyKeyboardMarkup(
    #         [[KeyboardButton("test", request_location=True)]],
    #         one_time_keyboard=True
    #     )
    # )


def entered_location(bot, update):
    print(update.message.location.latitute)
    print(update.message.location.longitude)

    # location_kb = KeyboardButton(text="send location",
    #                              request_location=True)
    # contact_kb = KeyboardButton(text="send contact",
    #                             request_contact=True)
    #
    # custom_kb = [
    #     [location_kb, contact_kb]
    # ]
    # reply_markup = ReplyKeyboardMarkup(custom_kb)
    # update.message.reply_text(
    #     "Would you mind sharing your location and contact with me?",
    #     reply_markup=reply_markup
    # )


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
    dp.add_handler(CommandHandler("loc", test_loc, pass_args=True))
    # dp.add_handler(MessageHandler(Filters.location, entered_location))



    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
