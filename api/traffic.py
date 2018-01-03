""" This script is related to the traffic API connection and queries
"""

# System Imports
from datetime import datetime

# Third-party Imports
from googlemaps import Client


# Local source tree Imports
from utils import read_googlemaps_config


class TrafficInformation(object):
    """

    """

    def __init__(self):
        gmaps_conf = read_googlemaps_config("config.ini")
        self.gmaps = Client(key=gmaps_conf["token"])
        self.home = gmaps_conf["home"]
        self.work = gmaps_conf["work"]

    def current_address(self, gl_tuple):
        """

        :return:
        """
        adress_dict = dict()
        address_list = self.gmaps.reverse_geocode(gl_tuple)

        for addr_data in address_list[0]['address_components']:
            if addr_data['types'][0] == 'street_number':
                adress_dict['number'] = addr_data['long_name']
            if addr_data['types'][0] == 'route':
                adress_dict['street'] = addr_data['long_name']
            if addr_data['types'][0] == 'political':
                adress_dict['neibor'] = addr_data['long_name']
            if addr_data['types'][0] == 'locality':
                adress_dict['city'] = addr_data['long_name']
            if addr_data['types'][0] == 'country':
                adress_dict['country'] = addr_data['long_name']
            if addr_data['types'][0] == 'postal_code':
                adress_dict['postal_code'] = addr_data['long_name']

        return adress_dict

    def home_and_work_info(self, to_home=True):
        """

        :param to_home:
        :return:
        """
        info_dict = dict()

        if to_home:
            destination, departure = self.home, self.work
        else:
            destination, departure = self.work, self.home

        # now = datetime.now()

        dt_info = self.gmaps.directions(
            departure,
            destination
        )
        info_dict['distance'] = dt_info[0]['legs'][0]['distance']['text']
        info_dict['duration'] = dt_info[0]['legs'][0]['duration']['text']

        return info_dict

    def time_to_somewhere(self, from_addr, to_addr):
        """

        :param from_addr:
        :param to_addr:
        :return:
        """
        info_dict = dict()









