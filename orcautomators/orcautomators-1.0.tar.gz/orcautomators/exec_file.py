# -*- coding: utf-8 -*-
import os
import threading

import yaml
from Pyautomators.__main__ import main

'''
@author: Kaue Bonfim
'''
"""Importando bibliotecas externas"""
"""Importando bibliotecas internas"""


class GenericModel():
    def __init__(self, dict_yaml):
        self.dict_yaml = dict_yaml
        self.exec_options = []
        for option in self.dict_yaml:
            if option == 'Name':
                self.exec_options.append("-Dname=" + self.dict_yaml[option])
            elif option == 'Feature':
                self.exec_options.append(self.dict_yaml[option])
            elif option == 'Tags':
                for arg in self.dict_yaml[option]:
                    tag_string = str(",").join(self.dict_yaml[option])
                self.exec_options.append("--tags=" + tag_string)
            elif option == 'Args':
                for arg in self.dict_yaml[option]:
                    self.exec_options.append(
                        '-D' + str(arg) + '=' + str(self.dict_yaml[option][arg]))


class WebModel(GenericModel):

    def run_web(self, Browser):

        for option in self.dict_yaml:
            if option == 'Reports':
                dir = "docs/reports/"
                self.exec_options.append('--junit')
                self.exec_options.append(
                    '--junit-directory=' + dir + self.dict_yaml['Name'] + '/')
                self.exec_options.append('--format=json.pretty')
                self.exec_options.append(
                    '-o=' +
                    dir +
                    self.dict_yaml['Name'] +
                    '/' +
                    str(Browser) +
                    "-" +
                    self.dict_yaml["Name"] +
                    ".json")
                self.exec_options.append('--format=json_cucumber.pretty')
                self.exec_options.append(
                    '-o=' +
                    dir +
                    str(Browser) +
                    "-" +
                    self.dict_yaml["Name"] +
                    "-cucumber.json")
            elif option == "Logs":
                self.exec_options.append('--format=sphinx.steps')
                self.exec_options.append(
                    '-o=log/' + str(Browser) + "-" + self.dict_yaml["Name"])
                self.exec_options.append('--format=steps.doc')
                self.exec_options.append(
                    '-o=' +
                    "log/steps/" +
                    self.dict_yaml["Name"] +
                    "-" +
                    "location.log")
                self.exec_options.append('--format=steps.usage')
                self.exec_options.append(
                    '-o=' +
                    "log/features/" +
                    self.dict_yaml["Name"] +
                    "-" +
                    "location.log")

        self.exec_options.append('-Dbrowser=' + Browser)
        return self.exec_options


class MobileModel(GenericModel):
    def run_mobile(self, Device):

        for option in self.dict_yaml:
            if option == 'Reports':
                dir = "docs/reports/"
                self.exec_options.append('--junit')
                self.exec_options.append(
                    '--junit-directory=' + dir + self.dict_yaml['Name'] + '/')
                self.exec_options.append('--format=json.pretty')
                self.exec_options.append(
                    '-o=' +
                    dir +
                    self.dict_yaml['Name'] +
                    '/' +
                    str(Device) +
                    "-" +
                    self.dict_yaml["Name"] +
                    ".json")
                self.exec_options.append('--format=json_cucumber.pretty')
                self.exec_options.append(
                    '-o=' +
                    dir +
                    str(Device) +
                    "-" +
                    self.dict_yaml["Name"] +
                    "-cucumber.json")
            elif option == "Logs":
                self.exec_options.append('--format=sphinx.steps')
                self.exec_options.append(
                    '-o=log/' + str(Device) + "-" + self.dict_yaml["Name"])
                self.exec_options.append('--format=steps.doc')
                self.exec_options.append(
                    '-o=' +
                    "log/steps/" +
                    self.dict_yaml["Name"] +
                    "-" +
                    "location.log")
                self.exec_options.append('--format=steps.usage')
                self.exec_options.append(
                    '-o=' +
                    "log/features/" +
                    self.dict_yaml["Name"] +
                    "-" +
                    "location.log")

        self.exec_options.append('-Ddevice=' + Device)
        return self.exec_options


class DesktopModel(GenericModel):
    def run_desktop(self):

        for option in self.dict_yaml:
            if option == 'Reports':
                dir = "docs/reports/"
                self.exec_options.append('--junit')
                self.exec_options.append(
                    '--junit-directory=' + dir + self.dict_yaml['Name'] + '/')
                self.exec_options.append('--format=json.pretty')
                self.exec_options.append(
                    '-o=' +
                    dir +
                    self.dict_yaml['Name'] +
                    '/' +
                    self.dict_yaml["Name"] +
                    ".json")
                self.exec_options.append('--format=json_cucumber.pretty')
                self.exec_options.append(
                    '-o=' + dir + self.dict_yaml["Name"] + "-cucumber.json")
            elif option == "Logs":
                self.exec_options.append('--format=sphinx.steps')
                self.exec_options.append('-o=log/' + self.dict_yaml["Name"])
                self.exec_options.append('--format=steps.doc')
                self.exec_options.append(
                    '-o=' +
                    "log/steps/" +
                    self.dict_yaml["Name"] +
                    "-" +
                    "location.log")
                self.exec_options.append('--format=steps.usage')
                self.exec_options.append(
                    '-o=' +
                    "log/features/" +
                    self.dict_yaml["Name"] +
                    "-" +
                    "location.log")

        return self.exec_options


class ThreadRun(threading.Thread):
    def __init__(self, list_exec, item=None):
        threading.Thread.__init__(self)
        self.item = item
        self.list_exec = list_exec

    def run(self):
        valor = None
        if self.list_exec['Type'] == 'Web':
            valor = WebModel(self.list_exec).run_web(self.item)
        elif self.list_exec['Type'] == 'Mobile':
            valor = MobileModel(self.list_exec).run_mobile(self.item)
        elif self.list_exec['Type'] == 'Desktop':
            valor = DesktopModel(self.list_exec).run_desktop()
        main(valor)


def runner(dict_execute):
    list_exec = []
    if dict_execute['Type'] == 'Web':
        for Browser in dict_execute['Browsers']:
            list_exec.append(ThreadRun(dict_execute, Browser))
    elif dict_execute['Type'] == 'Mobile':
        for Device in dict_execute['Devices']:
            list_exec.append(ThreadRun(dict_execute, Device))
    elif dict_execute['Type'] == 'Desktop':
        list_exec.append(ThreadRun(dict_execute))
    for option in list_exec:
        option.start()


def orchestra():
    file = open("manager/Pyautomators.yaml", "r")
    tests = yaml.load(file)
    for test in tests:
        if str(test).find("Teste") != -1:
            runner(tests[test])
        else:
            ERROR = """Undefined Test"""
            Exception(ERROR)
