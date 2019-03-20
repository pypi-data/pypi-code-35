#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   systemHelper.py
@Time    :   2018/12/20
@Author  :   Yaron Huang 
@Version :   1.0
@Contact :   yaronhuang@qq.com
@Desc    :   
'''
import os
import platform

def getOwnPath(in__file__):
    return os.path.dirname(os.path.realpath(in__file__))

def isWindows():
    sysName = platform.system()
    return sysName == "Windows"

def isLinux():
    sysName = platform.system()
    return sysName == "Linux"

def getProcessID(name):
    """
    #Func    :   通过进程名获取进程ID，可以用`basename xxx`         
    #Param   :   name   [in]    进程名          
    #Return  :   进程ID数组(int)
    """
    # try:
    lines = os.popen('ps aux | grep "' + name + '" | grep -v grep').readlines()
    if len(lines) <= 0:
        print('ID数组空:'+lines)
        return []
    id = []
    for item in lines:
        array = item.split()
        print(str(array[1]))
        id.append(int(array[1]))
    return id
    # except:
    #     print('ID数组失败:')
    #     return []

def killProcess(id):
    """
    #Func    :   杀死进程       
    #Param   :   id [in] 进程ID     
    #Return  :   True/False     
    """
    try:
        os.popen('kill -9 ' + str(id))
        lines = os.popen('ps ' + str(id)).readlines()
        if len(lines) <= 1:
            print('杀ID'+str(id) + '成功')
            return True
            print('杀ID'+str(id) + '失败')
        return False
    except:
        print('杀ID'+str(id) + '失败')
        return False
