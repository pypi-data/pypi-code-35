#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__createTime__ = "2018/11/2 14:47"
__author__ = "WeiYanfeng"
__email__ = "weiyf1225@qq.com"
__version__ = "0.0.1"
        
~~~~~~~~~~~~~~~~~~~~~~~~
程序单元功能描述
借助线程，延迟定时执行某些函数。

参考 [在python中延迟执行函数 - Arian's Blog](https://arianx.me/2018/06/27/Simple-time-event-loop-in-python/)

[heapq — Heap queue algorithm — Python 3.7.1 documentation](https://docs.python.org/3/library/heapq.html)

heapq 使用示例如下：

    >>> from heapq import *
    >>> h = []
    >>> heappush(h, (5, 'write code'))
    >>> heappush(h, (7, 'release product'))
    >>> h
    [(5, 'write code'), (7, 'release product')]
    >>> heappush(h, (1, 'write spec'))
    >>> h
    [(1, 'write spec'), (7, 'release product'), (5, 'write code')]
    >>> heappush(h, (3, 'create tests'))
    >>> h
    [(1, 'write spec'), (3, 'create tests'), (5, 'write code'), (7, 'release product')]
    >>> heappop(h)
    (1, 'write spec')
    >>> h
    [(3, 'create tests'), (7, 'release product'), (5, 'write code')]
~~~~~~~~~~~~~~~~~~~~~~~~
# 依赖包 Package required
# pip install weberFuncs

"""
import sys
from .WyfPublicFuncs import PrintTimeMsg, GetYYYYMMDDhhnnss, PrintAndSleep
import heapq
# import time
# from datetime import datetime, timedelta
from threading import Thread, Lock


class CDeferFunc:
    # 延迟函数
    def __init__(self, sFuncTag, cbFunc, iDeferSeconds, *args, **kwargs):
        self.sFuncTag = sFuncTag
        self.cbFunc = cbFunc
        self.sYmdHnsAddTime = GetYYYYMMDDhhnnss(0)
        self.iDeferSeconds = iDeferSeconds
        self.sYmdHnsPlanTime = GetYYYYMMDDhhnnss(iDeferSeconds)
        self.args = args
        self.kwargs = kwargs
        self.oResult = None

        self.bRunAlive = False  # 是否在执行中
        self.bAlreayRun = False  # 是否已执行

    def __str__(self):
        return 'CDeferFunc(%s,%s,%+d=%s)' % (self.sFuncTag, self.sYmdHnsAddTime,
                                             self.iDeferSeconds, self.sYmdHnsPlanTime)

    def getIdStr(self):
        # 返回该延迟函数的标识串，以函数标记和计划执行函数为标识
        return '%s.%s' % (self.sFuncTag, self.sYmdHnsPlanTime)

    def __lt__(self, other):
        # For heap sort.
        return self.sYmdHnsPlanTime < other.sYmdHnsPlanTime

    def execute(self):
        self.bRunAlive = True
        self.oResult = self.cbFunc(*self.args, **self.kwargs)
        self.bRunAlive = False
        self.bAlreayRun = True
        return self.oResult


class CDeferFuncThread:
    # 延迟执行线程
    def __init__(self):
        self.lsDeferFuncs = []  # 延迟函数列表
        self.setDeferFuncs = set()  # 延迟函数集合，按 sFuncTag. 去重
        self.mutex = Lock()  # 避免操作冲突
        self.bLoopRunFlag = True  # 是否已执行
        self.oThread = Thread(target=self.ThreadLoopRun, args=[])
        self.oThread.start()

    def AddDeferFunc(self, sFuncTag, cbFunc, iDeferSeconds, *args, **kwargs):
        # 增加一个延迟事件
        oEvent = CDeferFunc(sFuncTag, cbFunc, iDeferSeconds, *args, **kwargs)
        sIdStr = oEvent.getIdStr()
        if sIdStr in self.setDeferFuncs:
            PrintTimeMsg('AddDeferFunc(%s)AlreayAdd, SKIP!' % sIdStr)
            return None
        if self.mutex.acquire():  # blocking
            heapq.heappush(self.lsDeferFuncs, oEvent)
            self.setDeferFuncs.add(sIdStr)
            self.mutex.release()
            PrintTimeMsg('AddDeferFunc(%s)OK!' % oEvent)
        return oEvent

    def PopDeferFunc(self):
        # 完成一个延迟事件
        bEmpty = False
        if self.mutex.acquire():  # blocking
            try:
                oEvent = heapq.heappop(self.lsDeferFuncs)
            except IndexError:
                bEmpty = True
            sIdStr = oEvent.getIdStr()
            self.setDeferFuncs.remove(sIdStr)
            self.mutex.release()
            PrintTimeMsg('PopDeferFunc(%s)End!' % oEvent)
        return bEmpty

    def ThreadLoopRun(self, sYmdHnsTimeOut=''):
        PrintTimeMsg('CDeferFuncThread.ThreadLoopRun.Start...')
        iLoopCnt = 0
        while self.bLoopRunFlag:
            fSleepSeconds = 0.1
            if len(self.lsDeferFuncs) > 0:
                oEvent = self.lsDeferFuncs[0]  # 第0个就是最先的
                if GetYYYYMMDDhhnnss(0) >= oEvent.sYmdHnsPlanTime:
                    oEvent.execute()
                    self.PopDeferFunc()
                    fSleepSeconds = 0.001
                else:
                    fSleepSeconds = 0.01
            if sYmdHnsTimeOut and GetYYYYMMDDhhnnss(0) >= sYmdHnsTimeOut:
                PrintTimeMsg('CDeferFuncThread.ThreadLoopRun.TimeOut=%s!' % sYmdHnsTimeOut)
                break
            PrintAndSleep(fSleepSeconds,
                          'CDeferFuncThread.ThreadLoopRun.iLoopCnt=%s=' % iLoopCnt,
                          iLoopCnt % 10000 == 0)
            iLoopCnt += 1


def mainCDeferFuncThread():
    def cbTest(a, b):
        PrintTimeMsg('cbTest.a=%s,b=%s=' % (a, b))

    o = CDeferFuncThread()
    o.AddDeferFunc('DF01', cbTest, 5, 1, 2)
    o.AddDeferFunc('DF01', cbTest, 10, 3, 4)
    PrintAndSleep(1, 'DeferFunc...')
    o.AddDeferFunc('DF01', cbTest, 4, 4, 4)
    o.AddDeferFunc('DF03', cbTest, 6, 5, 6)

# --------------------------------------
if __name__ == '__main__':
    mainCDeferFuncThread()
