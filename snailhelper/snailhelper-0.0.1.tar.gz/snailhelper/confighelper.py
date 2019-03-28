# -*- conding:utf-8 -*-
"""配置文件【读取】助手"""
import re
import configparser
from snail import datehelper


class __Config:
    """读取配置文件助手"""
    def __init__(self, filename):
        self.__config = configparser.ConfigParser()
        self.__config.read(filenames=[filename], encoding='UTF-8')

    def get(self, key):
        """获取配置信息"""
        try:
            i = key.rindex('.')
            section = key[0:i]
            option = key[i+1:]
            return self.__config[section][option]
        except:
            return None

    def get_int(self, key):

        val = self.get(key)

        if not val:
            return None

        return int(val)

    def get_float(self, key):

        val = self.get(key)

        if not val:
            return None

        return float(val)

    def get_boolean(self, key):

        val = self.get(key)

        if not val:
            return False

        return '1' == val or 'TRUE' == val.upper()

    def get_list(self, key):

        val = self.get(key)

        if not val:
            return None

        return re.split(r'\s*\,\s*', val)

    def get_time(self, key):
        return datehelper.parse(self.get(key))


def instance(filename):
    return __Config(filename)



