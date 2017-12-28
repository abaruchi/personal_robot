""" This script contains routines to keep the overall project clean and
organized
"""

# System Imports
import configparser


# Third-party Imports


# Local source tree Imports


def read_telegram_config (config_file_path):
    """
    This routine reads section related to Telegram Robot

    :param config_file_path: The file path where all configuration is located
    :return: A dict with configurations options
    """
    telegram_conf_dict = dict()

    Conf = configparser.ConfigParser()
    Conf.read(config_file_path)

    options = Conf.options("Telegram")
    for option in options:
        telegram_conf_dict[option] = Conf.get("Telegram", option)

    return telegram_conf_dict


def read_googlemaps_config(config_file_path):
    """

    :param config_file_path:
    :return:
    """

    googlemaps_conf_dict = dict()
    Conf = configparser.ConfigParser()
    Conf.read(config_file_path)

    options = Conf.options("GoogleMaps")
    for option in options:
        googlemaps_conf_dict[option] = Conf.get("GoogleMaps", option)

    return googlemaps_conf_dict


def read_subway_config(config_file_path):
    """

    :param config_file_path:
    :return:
    """

    subway_conf_dict = dict()
    Conf = configparser.ConfigParser()
    Conf.read(config_file_path)

    options = Conf.options("Subway")
    for option in options:
        subway_conf_dict[option] = Conf.get("Subway", option)

    return subway_conf_dict
