""" This script is related to the traffic API connection and queries
"""

from datetime import datetime
from re import findall
from urllib import request

from bs4 import BeautifulSoup
from googlemaps import Client
from requests import get

from utils import ConfigRead, Regex


class TrafficInformation(object):
    """

    """

    def __init__(self):
        config_read = ConfigRead("config.ini")
        gmaps_conf = config_read.read_googlemaps_config()
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

        now = datetime.now()

        dt_info = self.gmaps.directions(
            departure,
            destination,
            mode='driving',
            departure_time=now
        )
        info_dict['distance'] = dt_info[0]['legs'][0]['distance']['text']
        info_dict['duration'] = dt_info[0]['legs'][0]['duration_in_traffic']['text']

        return info_dict

    def time_to_somewhere(self, from_addr, to_addr):
        """

        :param from_addr:
        :param to_addr:
        :return:
        """

        now = datetime.now()
        info_dict = dict()
        dt_info = self.gmaps.directions(
            from_addr,
            to_addr,
            mode='driving',
            departure_time=now
        )
        info_dict['distance'] = dt_info[0]['legs'][0]['distance']['text']
        info_dict['duration'] = dt_info[0]['legs'][0]['duration_in_traffic']['text']

        return info_dict


class TrafficNow(object):
    """

    """
    def __init__(self):
        config_read = ConfigRead("config.ini")
        cet_conf = config_read.read_cet_config()
        cet_url = cet_conf["traffic_url"]
        resp = get(cet_url, verify=False)
        self.bsObj = BeautifulSoup(resp.content, "html.parser")
        self.cet_graph = cet_conf["traffic_slowness"]
    def get_total_traffic(self):
        """

        :return:
        """

        total = self.bsObj.findAll("div")[8].findNext()
        return findall(Regex.remove_bold_html_tag(), str(total))[0]

    def get_tendency(self):
        """

        :return:
        """
        tendency = self.bsObj.findAll("div")[10].findAll("img")[0]
        return findall(Regex.get_tendency(), str(tendency))[0]

    def get_cet_graph(self):
        """

        :return:
        """

        file_name = "/tmp/cet_graph" + ".jpg"
        request.urlretrieve(self.cet_graph, file_name)
        return file_name
