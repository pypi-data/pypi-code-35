#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 通用函数
from __future__ import print_function
import sys
import os
import logging
import time
import traceback

# abs path
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
BASE_PATH = os.path.realpath(CUR_PATH + '/../../')
sys.path.append(BASE_PATH)
print(CUR_PATH, BASE_PATH)
from machinelearning.lib import utils

LOG_LEVEL = logging.DEBUG


def log(type, msg, model=''):
    """写日志"""
    if type == 'debug' and LOG_LEVEL != logging.DEBUG:  # 线上配置日志等级不是DEBUG时跳过debug日志
        return

    try:
        model = model.__name__.lower()
    except:
        model = 'sys'
    curtime = time.time()
    millisecond = int((curtime - int(curtime)) * 10000)
    utils.mkdir(BASE_PATH + "/log/")
    fo = open(BASE_PATH + "/log/" + model + "." + time.strftime('%Y%m%d%H', time.localtime(curtime)) + ".log", "a")
    """if isinstance(msg, unicode):
        msg = msg.encode("utf8")
    elif isinstance(msg, str) == False:
        msg = str(msg)"""
    msg = '[' + type.upper() + ']\t' + time.strftime("%Y-%m-%d %H:%M:%S",
                                                     time.localtime(curtime)) + "." + "%04d" % millisecond + "\t" + msg
    fo.write(msg + "\n")
    fo.close()

    if LOG_LEVEL == logging.DEBUG:  # debug时输出到屏幕
        print(msg)


def debug(msg, model=''):
    """
    debug日志打印
    :param msg:
    :param model:
    :return:
    """
    log('debug', msg, model)


def info(msg, model=''):
    """
    info日志打印
    :param msg:
    :param model:
    :return:
    """
    log('info', msg, model)


def warning(msg, model=''):
    """
    warning日志打印
    :param msg:
    :param model:
    :return:
    """
    log('warning', msg, model)


def error(msg, model=''):
    """
    error日志打印
    :param msg:
    :param model:
    :return:
    """
    log('error', msg, model)


def get_trace():
    """获得异常栈内容"""
    try:
        errmsg = "Traceback (most recent call last):\n "
        exc_type, exc_value, exc_tb = sys.exc_info()
        for filename, linenum, funcname, source in traceback.extract_tb(exc_tb):
            errmsg += "  File \"%-23s\", line %s, in %s() \n\t  %s \n" % (filename, linenum, funcname, source)
        errmsg += str(exc_type.__name__) + ": " + str(exc_value)
        # traceback.print_exc()
    except:
        traceback.print_exc()
        errmsg = ''
    return errmsg


if __name__ == '__main__':
    """函数测试"""
    info("test", "test")
    warning("test", "test")
    print(1)
