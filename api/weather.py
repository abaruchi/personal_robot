""" This script is related to the weather API connection and queries
"""

from forecastio import load_forecast

from utils import Regex, read_weather_config


class WeatherInformation(object):
    """

    """

    def __init__(self, lat=None, long=None, defaultplace=None):
        weather_conf = read_weather_config("config.ini")
        self.weather_key = weather_conf["token"]

        if lat is None or long is None:
            if defaultplace == "Home":
                if "home_coordinates" in weather_conf.keys():
                    home_coordinates = weather_conf["home_coordinates"]
                    lat, long = map(float, home_coordinates.split(','))
                    self.latitute, self.longitute = lat, long

            elif defaultplace == "Work":
                if "work_coordinates" in weather_conf.keys():
                    work_coordinates = weather_conf["work_coordinates"]
                    lat, long = map(float, work_coordinates.split(','))
                    self.latitute, self.longitute = lat, long
        else:
            self.latitute, self.longitute = lat, long
        self.unit = 'si'

    def __forecast_init(self):
        """

        :return:
        """
        forecast = load_forecast(self.weather_key,
                                 self.latitute,
                                 self.longitute,
                                 units=self.unit)
        return forecast

    def get_current_rain_probability(self):
        """

        :return:

        """
        forecast = self.__forecast_init()
        forecast_current = forecast.currently()
        return forecast_current.precipProbability

    def get_current_summary(self):
        """

        :return:
        """
        forecast = self.__forecast_init()
        forecast_current = forecast.currently()
        return forecast_current.summary

    def get_hour_rain_probability(self):
        """

        :return:
        """
        prob_dict = dict()
        forecast = self.__forecast_init()
        forecast_daily = forecast.hourly()

        for h in forecast_daily.data[0:6]:
            prob_dict[str(h.time)] = h.precipProbability

        return prob_dict

    def get_hour_summary(self):
        """

        :return:
        """
        summ_dict = dict()
        forecast = self.__forecast_init()
        forecast_daily = forecast.hourly()

        for h in forecast_daily.data[0:6]:
            summ_dict[str(h.time)] = h.summary

        return summ_dict
