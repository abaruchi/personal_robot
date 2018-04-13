"""
"""

import logging
import logging.handlers


class Log(object):
    """
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %('
                                             'processName)s - %(message)s')


        file_to_log = "./log/telegram_bot.log"
        logHandler = logging.handlers.TimedRotatingFileHandler(file_to_log,
                                                                when='W6',
                                                                interval=1,
                                                                backupCount=3)
        logHandler.setLevel(logging.INFO)
        logHandler.setFormatter(logger_formatter)
        self.logger.addHandler(logHandler)

    def log_my_robot (self, contact_name, command, log_message):
        """

        :param contact_name:
        :param command:
        :param log_message:
        :return:
        """
        log = "Contact: {}, Command: {} - {}".format(contact_name,
                                                     command,
                                                     log_message)
        self.logger.info(log)
