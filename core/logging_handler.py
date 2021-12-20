import logging
from configparser import ConfigParser
from time import strftime


class bcolors:
    blue = '\033[94m'
    red = '\033[31m'
    green = '\033[32m'
    orange = '\033[33m'
    cend = '\033[0m'


class UserLoggingHandler():

    def __init__(self, name: str):

        # create a logger
        self.logger = logging.getLogger("main-user-"+name)

        # create a logging format
        hdlr = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(message)s")
        hdlr.setFormatter(formatter)

        fhdlr = logging.FileHandler("user.log")

        # add the handlers to the logger
        self.logger.addHandler(hdlr)
        self.logger.addHandler(fhdlr)

        # set logger level from config and add handler
        file = 'config.ini'
        self.config = ConfigParser()
        self.config.read(file)
        del file

        if self.config.get('bot_info', 'logging_level') == 'DEBUG':
            self.logger.setLevel(logging.DEBUG)
        elif self.config.get('bot_info', 'logging_level') == 'INFO':
            self.logger.setLevel(logging.INFO)
        elif self.config.get('bot_info', 'logging_level') == 'WARNING':
            self.logger.setLevel(logging.WARNING)
        elif self.config.get('bot_info', 'logging_level') == 'ERROR':
            self.logger.setLevel(logging.ERROR)
        elif self.config.get('bot_info', 'logging_level') == 'CRITICAL':
            self.logger.setLevel(logging.CRITICAL)

    def debug(self, message):
        self.logger.debug(strftime("[DEBUG][%d.%m.%y][%H:%M:%S]")+message)

    def info(self, message):
        self.logger.info(strftime("[INFO][%d.%m.%y][%H:%M:%S]")+message)

    def warning(self, message):
        self.logger.warning(strftime("[WARNING][%d.%m.%y][%H:%M:%S]")+message)
