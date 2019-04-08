#!/usr/bin/python3
# -*- coding: utf-8 -*-
from drummer.utils.files import YamlFile
from os import path

class ConfigurationException(Exception):
    pass


class Configuration():

    @staticmethod
    def load(BASE_DIR):

        CONFIG_FILENAME = path.join(BASE_DIR, 'config/drummer-config.yml')
        TASKS_FILENAME = path.join(BASE_DIR, 'config/drummer-tasks.yml')

        try:
            configuration = YamlFile.read(CONFIG_FILENAME)

        except:
            raise ConfigurationException('Configuration file not found')

        try:
            tasks = YamlFile.read(TASKS_FILENAME)
            configuration['tasks'] = tasks

        except:
            raise ConfigurationException('Task file not found')

        return configuration
