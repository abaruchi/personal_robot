""" This script is related to the telegram API connection and commands
"""

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, RegexHandler, Updater)

from handlers import commands, conversations, messages
from utils import ConfigRead


def main():
    """Run bot."""
    config_read = ConfigRead("config.ini")
    telegram_conf = config_read.read_telegram_config()
    updater = Updater(telegram_conf["token"])

    conv_traffic = conversations.Location()
    conv_weather = conversations.Weather()

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    weather_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('weather', conv_weather.crazy_weather)],
        states={
            conv_weather.PLACE:
                [RegexHandler('^(Home|Work)$',
                              conv_weather.my_places,
                                pass_user_data=True),
                MessageHandler(Filters.location,
                               conv_weather.my_cur_location,
                               pass_user_data=True)],
            conv_weather.INFO:
                [RegexHandler('^(This Hour|Next 6 Hours)$',
                              conv_weather.info_test,
                              pass_user_data=True)],
        },
        fallbacks=[CommandHandler('done', conv_weather.cancel)]
    )
    dp.add_handler(weather_conv_handler)

    traffic_conv_handler = ConversationHandler(
        entry_points=[CommandHandler('letsgo', conv_traffic.lets_go)],
        states={
            conv_traffic.MY_LOCATION:
                [MessageHandler(Filters.location,
                                conv_traffic.my_current_address,
                                pass_user_data=True)],
            conv_traffic.OTHER_LOCATION:
                [MessageHandler(Filters.text,
                                conv_traffic.my_other_address,
                               pass_user_data=True)],
            conv_traffic.DIRECTION:
                [MessageHandler(Filters.text,
                                conv_traffic.my_directions,
                                pass_user_data=True)]
        },
        fallbacks=[CommandHandler('done', conv_traffic.cancel)]
    )
    dp.add_handler(traffic_conv_handler)

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", commands.start))
    dp.add_handler(CommandHandler("lines", commands.line, pass_args=True))
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
