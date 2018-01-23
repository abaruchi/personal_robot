"""
"""

import logging

from utils import ConfigRead


class Log(object):
    """
    """
    def __init__(self):
        config_reader = ConfigRead("config.ini")
        self.config_params = config_reader.read_global_config()
        self.log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        self.logger = logging.getLogger(__name__)
