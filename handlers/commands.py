"""
"""

from telegram import KeyboardButton, ReplyKeyboardMarkup

from api.subway import GetLinesStatus
from api.traffic import TrafficInformation, TrafficNow
from utils import Messages


def start(bot, update):
    user = update.message.from_user
    update.message.reply_text(Messages.start_message(user))


def line(bot, update, args):
    """

    :param bot:
    :param update:
    :param args:
    :return:
    """
    arg_size = len(args)
    if arg_size == 1:
        metro_stat = GetLinesStatus()
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


def go_home(bot, update):
    """

    :param bot:
    :param update:
    :return:
    """
    gmaps = TrafficInformation()
    tf_dict = gmaps.home_and_work_info()

    message_str_01 = "Work to Home information:\n"
    message_str_02 = "Distance: " + tf_dict['distance'] + "\n"
    message_str_03 = "Time: " + tf_dict['duration']

    cur_info = message_str_01 + message_str_02 + message_str_03
    bot.sendMessage(
        update.message.chat_id,
        text=cur_info
    )


def go_work(bot, update):
    """

    :param bot:
    :param update:
    :return:
    """
    gmaps = TrafficInformation()
    tf_dict = gmaps.home_and_work_info(to_home=False)

    message_str_01 = "Home to Work information:\n"
    message_str_02 = "Distance: " + tf_dict['distance'] + "\n"
    message_str_03 = "Time: " + tf_dict['duration']

    cur_info = message_str_01 + message_str_02 + message_str_03
    bot.sendMessage(
        update.message.chat_id,
        text=cur_info
    )


def cet_data(bot, update, args):
    """

    :param bot:
    :param update:
    :return:
    """

    cet = TrafficNow()
    arg_size = len(args)
    if arg_size >= 1:

        if args == "total_traffic":
            message_str_01 = "Traffic Jam: "
            message_str_02 = cet.get_total_traffic()
            cur_info = message_str_01 + message_str_02

            bot.sendMessage(
                update.message.chat_id,
                text=cur_info
            )

        elif args == "tendency":
            message_str_01 = "Traffic Tendency: "
            message_str_02 = cet.get_tendency()
            cur_info = message_str_01 + message_str_02

            bot.sendMessage(
                update.message.chat_id,
                text=cur_info
            )

        elif args == "map":
            return cet.get_cet_graph()

        else:
            bot.sendMessage(
                update.message.chat_id,
                text="Need to know what you want, see help message about args"
            )
