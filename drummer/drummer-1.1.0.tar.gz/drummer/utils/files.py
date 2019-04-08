#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import yaml

class JsonFile():

    @staticmethod
    def write(filename, data):

        # save file
        with open(filename,'w') as f:
            json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

        return True


    @staticmethod
    def read(filename):

        # read file
        with open(filename,'r',encoding='utf-8') as fp:
            data = json.load(fp)

        return data


class YamlFile():

    @staticmethod
    def write(filename, data):

        with open(filename, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)

        return True


    @staticmethod
    def read(filename):

        with open(filename, 'r', encoding='utf-8') as f:
                filedata = yaml.load(f, Loader=yaml.FullLoader)

        return filedata
