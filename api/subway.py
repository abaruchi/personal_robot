""" This script is related to the subway API connection and queries
"""

from ast import literal_eval

from aenum import Enum
from bs4 import BeautifulSoup
from requests import get

from utils import ConfigRead, Regex


class Lines(Enum):
    azul = 0
    verde = 1
    vermelha = 2
    amarela = 3
    lilas = 4
    rubi = 5
    diamante = 6
    esmeralda = 7
    turquesa = 8
    coral = 9
    safira = 10
    prata = 11


class GetLinesStatus(object):
    """

    """

    def __init__(self):

        config_read = ConfigRead("config.ini")
        url_to_read = config_read.read_subway_config()
        resp = get(url_to_read["metro"], verify=False)
        bsObj = BeautifulSoup(resp.content)
        self.lines_array = literal_eval(bsObj.string)

    def blue_line_status(self):
        """

        :return:
        """
        blue_line_stat = self.lines_array[Lines.azul.value]['situacao']
        return blue_line_stat

    def red_line_status(self):
        """

        :return:
        """
        red_line_stat = self.lines_array[Lines.vermelha.value]['situacao']
        return red_line_stat

    def yellow_line_status(self):
        """

        :return:
        """
        yellow_line_stat = self.lines_array[Lines.amarela.value]['situacao']
        return yellow_line_stat

    def all_subway_lines_status(self):
        """

        :return:
        """
        status_dict = dict()
        for line in list(Lines):
            status_dict[line.name] = self.lines_array[line.value]['situacao']

        return status_dict
