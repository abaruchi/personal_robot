"""
"""

from api.traffic import TrafficInformation
from utils import Messages


def start(bot, update):
    user = update.message.from_user
    update.message.reply_text(Messages.start_message(user))


def coordinates_to_address(bot, update):
    gmaps = TrafficInformation()
    latitude = update.message.location.latitude
    longitude = update.message.location.longitude

    coord_tuples = (latitude, longitude)
    address = gmaps.current_address(coord_tuples)
    addr_str_01 = "Your location is: \n"
    addr_str_02 = address['street'] + ", " + address['number'] + " - " + \
                  address['neibor'] + " - " + address['city'] + " - " + \
                  address['country'] + " - " + address['postal_code'] + "\n"
    cur_addr = addr_str_01 + addr_str_02
    bot.sendMessage(
        update.message.chat_id,
        text=cur_addr
    )
