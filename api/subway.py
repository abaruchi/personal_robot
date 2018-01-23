""" This script is related to the subway API connection and queries
"""

from re import sub

from bs4 import BeautifulSoup
from requests import get

from utils import Regex, ConfigRead


class GetSubwayLineStatus(object):
    """

    """

    def __init__(self):

        config_read = ConfigRead("config.ini")
        url_to_read = config_read.read_subway_config()
        resp = get(url_to_read["metro"], verify=False)
        self.bsObj = BeautifulSoup(resp.content)

    def _find_line_status(self, string_to_find):
        """

        :param string_to_find:
        :return:
        """
        lines = self.bsObj.findAll("table")[1].findAll("tr")

        for i in lines:
            for j in i.findAll("td"):
                if str(j) == string_to_find:
                    stat = i.findAll("td")[1]
                    stat = str(stat)
                    stat = sub(Regex.remove_td_html_tag(), "", stat)
                    return stat
        return None

    def blue_line_status(self):
        """

        :return:
        """
        blue_line_stat = self._find_line_status("<td>Linha 1-Azul</td>")
        return blue_line_stat

    def red_line_status(self):
        """

        :return:
        """
        red_line_stat = self._find_line_status("<td>Linha 3-Vermelha</td>")
        return red_line_stat

    def yellow_line_status(self):
        """

        :return:
        """
        yellow_line_stat = self._find_line_status("<td>Linha 4-Amarela</td>")
        return yellow_line_stat

    def all_subway_lines_status(self):
        """

        :return:
        """
        status_dict = dict()
        string_dict ={
            'Linha Amarela': '<td>Linha 4-Amarela</td>',
            'Linha Vermelha': '<td>Linha 3-Vermelha</td>',
            'Linha Prata': '<td>Linha 15-Prata</td>',
            'Linha Verde': '<td>Linha 2-Verde</td>',
            'Linha Azul': '<td>Linha 1-Azul</td>',
            'Linha Lilas': '<td>Linha 5-Lilás</td>'
        }

        for line_name, line_str in string_dict.items():
            status_dict[line_name] = self._find_line_status(line_str)
        return status_dict


class GetCPTMStatus(object):
    """

    """

    def __init__(self):

        url_to_read = read_subway_config("config.ini")
        resp = get(url_to_read["cptm"], verify=False)
        self.bsObj = BeautifulSoup(resp.content)

    def _find_line_status(self, string_to_find):
        """

        :param string_to_find:
        :return:
        """
        lines = self.bsObj.findAll("table")[1].findAll("tr")

        for i in lines:
            for j in i.findAll("td"):
                if str(j) == string_to_find:
                    stat = i.findAll("td")[1]
                    stat = str(stat)
                    stat = sub(Regex.remove_td_html_tag(), "", stat)
                    return stat
        return None

    def esmeralda_line_status(self):
        """

        :return:
        """
        esmeralda_line_stat = self._find_line_status("<td>ESMERALDA</td>")
        return esmeralda_line_stat

    def all_cptm_lines_status(self):
        """

        :return:
        """
        status_dict = dict()
        string_dict ={
            'Azul': '<td>AZUL</td>',
            'Verde': '<td>VERDE</td>',
            'Vermelha': '<td>VERMELHA</td>',
            'Amarela': '<td>AMARELA</td>',
            'Lilas': '<td>LILÁS</td>',
            'Rubi': '<td>RUBI</td>',
            'Diamante': '<td>DIAMANTE</td>',
            'Esmeralda': '<td>ESMERALDA</td>',
            'Turquesa': '<td>TURQUESA</td>',
            'Coral': '<td>CORAL</td>',
            'Safira': '<td>SAFIRA</td>',
            'Prata': '<td>PRATA</td>'
        }

        for line_name, line_str in string_dict.items():
            status_dict[line_name] = self._find_line_status(line_str)
        return status_dict
