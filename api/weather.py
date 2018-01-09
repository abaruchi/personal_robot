""" This script is related to the weather API connection and queries
"""

from utils import Regex, read_weather_config


class WeatherInformation(object):
    """

    """

    def __init__(self):
        weather_conf = read_weather_config("config.ini")
        self.weather_key = weather_conf["token"]

        if "home_coordinates" in weather_conf.keys():
            self.home_coordinates = weather_conf["home_coordinates"]
        elif "work_coordinates" in weather_conf.keys():
            self.work_coordinates = weather_conf["work_coordinates"]
