""" This script is related to the telegram API connection and commands
"""

# System Imports


# Third-party Imports
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)
from telegram import (KeyboardButton, ReplyKeyboardMarkup)


# Local source tree Imports
from utils import (read_telegram_config, Messages)
from api.subway import (GetSubwayLineStatus, GetCPTMStatus)
from api.traffic import TrafficInformation


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


def my_location_button(bot, update, args):
    """

    :param bot:
    :param update:
    :param args:
    :return:
    """
    bot.sendMessage(
        update.message.chat_id,
        text='Thanks! Press the button bellow and send me your location!',
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("Send My Location", request_location=True)]],
            one_time_keyboard=True
        )
    )


def coordinates_to_address(bot, update):
    gmaps = TrafficInformation()
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    coord_tuples = (latitude, longitude)
    address = gmaps.current_address(coord_tuples)
    #print(address)
    addr_str_01 = "Your location is: \n"
    addr_str_02 = address['street'] + ", " + address['number'] + " - " + \
                  address['neibor'] + " - " + address['city'] + " - " + \
                  address['country'] + " - " + address['postal_code'] + "\n"
    cur_addr = addr_str_01 + addr_str_02
    bot.sendMessage(
        update.message.chat_id,
        text=cur_addr
    )


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
    dp.add_handler(CommandHandler("mylocation",
                                  my_location_button,
                                  pass_args=True))
    dp.add_handler(MessageHandler(Filters.location, coordinates_to_address))

    # Start the Bot
    updater.start_polling()

    # Block until you press Ctrl-C or the process receives SIGINT, SIGTERM or
    # SIGABRT. This should be used most of the time, since start_polling() is
    # non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
