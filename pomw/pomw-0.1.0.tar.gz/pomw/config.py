# -*- python-indent-offset: 4; -*-

from configparser import ConfigParser
from os.path import expanduser


class Config:
    def __init__(self, config_filename="%s/.config/pomw/pomwrc" % expanduser("~")):
        self.__config = ConfigParser()
        self.__config.read(config_filename)

    @property
    def config(self):
        return self.__config
