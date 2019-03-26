#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   flowprofile.py
@Time    :   2019/03/19
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   流量配置：增加端口、删除端口、修改端口流量限制     
             文件示例："8080":{"limit":1024,"used":500}
'''

import os
import json

class FlowProfile(object):
    def __init__(self, fileName = None):
        self.profile = {}
        try:
            if fileName != None:
                str = None
                with open(fileName, 'r+') as fd:
                    str = fd.read(str)
                self.profile = json.loads(str)
        except:
            pass

    def addPort(self, port, limit):
        port  = str(port)
        limit = int(limit)
        used  = 0
        if self.profile.get(port) != None:
            self.profile[port]['limit'] = limit
            self.profile[port]['changeLimit'] = 1
        else:
            self.profile[port] = {'limit':limit, 'used':0}

    def delPort(self, port):
        port = str(port)
        if self.profile.get(port) != None:
            self.profile.pop(port)

    def resetPortUsed(self, port):
        port = str(port)
        if self.profile.get(port) != None:
            self.profile[port]['used'] = 0
            self.profile[port]['reset'] = 1

    def save(self, fileName):
        try:
            str   = json.dumps(self.profile)
            index = fileName.rfind('/')
            path  = fileName[0:index+1]
            if not os.path.exists(path):
                os.makedirs(path)
            with open(fileName, 'w+') as fd:
                fd.write(str)
        except:
            return False
        return True


    def __isPortReset(self, profile, port):
        if profile[port].get('reset') != None:
            if profile[port]['reset'] == 1:
                return True
        return False

    def __isPortChangeLimit(self, profile, port):
        if profile[port].get('changeLimit') != None:
            if profile[port]['changeLimit'] == 1:
                return True
        return False

    def reload(self, fileName):
        """
        #Func    :   重载主要是读取开关,包括:增删端口、重置流量、修改上限       
        """
        if fileName == None:
            return
        try:
            str = None
            with open(fileName, 'r+') as fd:
                str = fd.read(str)
            value = json.loads(str)
            for port in value:
                if self.profile.get(port) == None:
                    self.addPort(port, value[port]['limit'])
                elif self.__isPortReset(value, port):
                    self.profile[port]['used'] = 0
                    self.profile[port]['reset'] = 0
                elif self.__isPortChangeLimit(value, port):
                    self.profile[port]['limit'] = value[port]['limit']
                    self.profile[port]['changeLimit'] = 0
            for port in self.profile:
                if value.get(port) == None:
                    self.delPort(port)
        except:
            pass
    



