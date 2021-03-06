""" This script contains routines to keep the overall project clean and
organized
"""


import configparser


class ConfigRead(object):

    def __init__(self, config_file_path):
        self.Conf = configparser.ConfigParser()
        self.Conf.read(config_file_path)

    def read_telegram_config (self):
        """
        This routine reads section related to Telegram Robot

        :param config_file_path: The file path where all configuration is located
        :return: A dict with configurations options
        """
        telegram_conf_dict = dict()

        options = self.Conf.options("Telegram")
        for option in options:
            telegram_conf_dict[option] = self.Conf.get("Telegram", option)

        return telegram_conf_dict

    def read_googlemaps_config(self):
        """

        :param config_file_path:
        :return:
        """

        googlemaps_conf_dict = dict()

        options = self.Conf.options("GoogleMaps")
        for option in options:
            googlemaps_conf_dict[option] = self.Conf.get("GoogleMaps", option)

        return googlemaps_conf_dict

    def read_cet_config(self):
        """

        :return:
        """
        cet_conf_dict = dict()

        options = self.Conf.options("CET")
        for option in options:
            cet_conf_dict[option] = self.Conf.get("CET", option)

        return cet_conf_dict

    def read_subway_config(self):
        """

        :param config_file_path:
        :return:
        """
        subway_conf_dict = dict()

        options = self.Conf.options("Subway")
        for option in options:
            subway_conf_dict[option] = self.Conf.get("Subway", option)

        return subway_conf_dict

    def read_weather_config(self):
        """

        :param config_file_path:
        :return:
        """

        weather_conf_dict = dict()

        options = self.Conf.options("Weather")
        for option in options:
            weather_conf_dict[option] = self.Conf.get("Weather", option)

        return weather_conf_dict

    def read_global_config(self):
        """

        :param config_file_path:
        :return:
        """

        global_conf_dict = dict()

        options = self.Conf.options("Bot")
        for option in options:
            global_conf_dict[option] = self.Conf.get("Bot", option)

        return global_conf_dict


class Regex(object):

    @staticmethod
    def remove_td_html_tag():
        return r'<td>|<\/td>'

    @staticmethod
    def get_tendency():
        return r'title=\"(\w*)\"'

    @staticmethod
    def remove_bold_html_tag():
        return r"\<b\>(\d+)\<\/b\>"


class Messages(object):

    @staticmethod
    def start_message(user):
        part_01 = "Hello " + user.first_name + "!!!!" + "\n"

        part_02 = """
Hi man.. here is the deal.. Im a robot and don't like you. My master is a guy, 
called Artur Baruchi. If you want to see some of his shits, including me, 
you can check his git at http://github.com/abaruchi. So get out or ask me some
questions..
        """
        return part_01 + part_02

    @staticmethod
    def metro_usage_help():
        msg = """
This command inform the subway (metro) lines status. 
Usage:
    /metro all: informs status of all subway lines
    /metro azul: informs status of subway line blue
    /metro vermelha: informs status of subway line red
    /metro amarela: informs status of subway line red
"""
        return msg

    @staticmethod
    def cptm_usage_help():
        msg = """
This command inform the train (cptm) lines status. 
Usage:
    /cptm all: informs status of all subway lines
    /cptm esmeralda: informs status of cptm line esmeralda
"""
        return msg
