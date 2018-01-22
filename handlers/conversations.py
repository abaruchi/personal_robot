"""
"""

# System Imports
from re import IGNORECASE, compile
from time import sleep

from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
# Third-party Imports
from telegram.ext import ConversationHandler

# Local source tree Imports
from api.traffic import TrafficInformation
from api.weather import WeatherInformation

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


def my_current_address(bot, update, user_data):
    gmaps = TrafficInformation()
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    coord_tuples = (latitude, longitude)
    address = gmaps.current_address(coord_tuples)
    addr_01 = address['street'] + "," + address['number'] + "-" + \
              address['neibor']

    user_data['my_location'] = addr_01

    message = "Right.. Now I know where you are Genius.. So, tell me the " \
              "another address. And please.. write this shit right, I don't " \
              "give a shit if you write this wrong"
    bot.sendMessage(
        update.message.chat_id,
        text=message
    )
    return OTHER_LOCATION


def my_other_address(bot, update, user_data):
    """

    :param bot:
    :param update:
    :param user_data:
    :return:
    """
    user_data['other_location'] = update.message.text
    message = "Ok Dude, we are almost there.. So, you want to go FROM your " \
              "current location or TO your location.. " \
              "Tip for you idiot:\n answer FROM or TO"
    bot.sendMessage(
        update.message.chat_id,
        text=message
    )
    return DIRECTION


def my_directions(bot, update, user_data):
    """

    :param bot:
    :param update:
    :param user_data:
    :return:
    """

    user_data['directions'] = update.message.text

    from_regex = compile('from', IGNORECASE)
    to_regex = compile('to', IGNORECASE)

    if from_regex.match(user_data['directions']):
        from_loc = user_data['my_location']
        to_loc = user_data['other_location']
    elif to_regex.match(user_data['directions']):
        from_loc = user_data['other_location']
        to_loc = user_data['my_location']
    else:
        bye_message = "Oh GOD! You need just to write FROM or TO.. " \
                      "and you can't.. See you later bitch, Im done here..."
        bot.sendMessage(
            update.message.chat_id,
            text=bye_message
        )

        return ConversationHandler.END

    gmaps = TrafficInformation()
    route_info = gmaps.time_to_somewhere(
        from_loc,
        to_loc
    )

    message_part_01 = "So, you want to go FROM:\n " + from_loc + "\n" +\
                      "TO: \n" + to_loc
    bot.sendMessage(
        update.message.chat_id,
        text=message_part_01
    )

    sleep(2)
    message_part_02 = "Route Information:\n" + "Distance: " + route_info[
        'distance'] + "\n" + "Time: " + route_info['duration']
    bot.sendMessage(
        update.message.chat_id,
        text=message_part_02
    )

    return ConversationHandler.END


def cancel(bot, update):
    update.message.reply_text('Shit.. I always waste my time with you.. ',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

##############


PLACE, INFO, GRANULARITY = range(3)

reply_place_keyboard = [['Home', 'Work'],
                        [KeyboardButton("Send My Location",
                                        request_location=True)]]
markup_place = ReplyKeyboardMarkup(reply_place_keyboard,
                                   one_time_keyboard=True)

reply_gran_keyboard = [['This Hour', 'Next 6 Hours']]
markup_gran = ReplyKeyboardMarkup(reply_gran_keyboard,
                                  one_time_keyboard=True)


def crazy_weather(bot, update):
    """

    :param bot:
    :param update:
    :return:
    """
    message = \
    """
    So, do you wanna know about the Weather.. From where do you wanna know?    
    """

    update.message.reply_text(
        text=message,
        reply_markup=markup_place)

    return PLACE


def my_places(bot, update, user_data):
    """

    :param bot:
    :param update:
    :param user_data:
    :return:
    """
    text = update.message.text
    user_data['choice'] = text
    forecast = WeatherInformation(defaultplace=text)
    user_data['forecast_obj'] = forecast

    message = \
    """
    Do you wanna know the forecast for next 6 hours or just for now?    
    """

    update.message.reply_text(
        text=message,
        reply_markup=markup_gran)

    return INFO


def my_cur_location(bot, update, user_data):
    """

    :param bot:
    :param update:
    :param user_data:
    :return:
    """
    user_data['latitude'] = float(update.message.location.latitude)
    user_data['longitude'] = float(update.message.location.longitude)
    user_data['forecast_obj'] = WeatherInformation(lat=user_data['latitude'],
                                               long=user_data['longitude'])

    message = \
    """
    Do you wanna know the forecast for next 6 hours or just for now?    
    """

    update.message.reply_text(
        text=message,
        reply_markup=markup_gran)

    return INFO


def info_test(bot, update, user_data):
    """

    :param bot:
    :param update:
    :param user_data:
    :return:
    """
    forecast = user_data['forecast_obj']
    text = update.message.text
    if text == "This Hour":
        text_01 = "Current prob rain is {}".format(
            forecast.get_current_rain_probability())
        text_02 = "Weather Summary:\n{}".format(forecast.get_current_summary())

        bot.sendMessage(
            update.message.chat_id,
            text=text_01
        )
        sleep(2)
        bot.sendMessage(
            update.message.chat_id,
            text=text_02
        )

    else:
        rain_prob = forecast.get_hour_rain_probability()
        weather_summ = forecast.get_hour_summary()
        for hour in rain_prob.keys():
            text_01 = "{} rain prob is {}".format(hour, rain_prob[hour])
            text_02 = "Summary:\n{}".format(weather_summ[hour])
            bot.sendMessage(
                update.message.chat_id,
                text=text_01
            )
            bot.sendMessage(
                update.message.chat_id,
                text=text_02
            )
            sleep(2)

    return ConversationHandler.END
