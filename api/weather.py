""" This script is related to the weather API connection and queries
"""

from forecastio import load_forecast

from utils import ConfigRead


class WeatherInformation(object):
    """

    """

    def __init__(self, lat=None, long=None, defaultplace=None):

        config_read = ConfigRead("config.ini")
        self.weather_conf = config_read.read_weather_config()
        self.weather_key = self.weather_conf["token"]

        if lat is None or long is None:
            if defaultplace == "Home":
                if "home_coordinates" in self.weather_conf.keys():
                    home_coordinates = self.weather_conf["home_coordinates"]
                    lat, long = map(float, home_coordinates.split(','))
                    self.latitute, self.longitute = lat, long

            elif defaultplace == "Work":
                if "work_coordinates" in self.weather_conf.keys():
                    work_coordinates = self.weather_conf["work_coordinates"]
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
