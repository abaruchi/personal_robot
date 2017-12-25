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
