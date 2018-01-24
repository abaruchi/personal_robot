"""
"""

import logging
import os

from utils import ConfigRead


class Log(object):
    """
    """
    def __init__(self):
        read_config = ConfigRead("config.ini")
        self.global_conf = read_config.read_global_config()
        self.log_format = '%(asctime)s - %(name)s - %(processName)s ' \
                          '- %(message)s'

    def __create_log_file(self):
        """

        :return:
        """
        pass
