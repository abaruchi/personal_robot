"""
"""

# System Imports
from re import (match, compile, IGNORECASE)
from time import sleep

# Third-party Imports
from telegram.ext import ConversationHandler
from telegram import (KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove)


# Local source tree Imports
from api.traffic import TrafficInformation

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
