import os
import sys
import time
import subprocess

from aigpy import cmdHelper
from aigpy import fileHelper
from aigpy import convertHelper
from aigpy import systemHelper

from ss_py.ssprofile   import SSProfile
from ss_py.flowprofile import FlowProfile

PATH_BASE        = '/etc/ss_py/'
FILE_PROFILE     = PATH_BASE + 'profile.json'
FILE_SSERVER_PID = PATH_BASE + 'ssserverpid.txt'
FILE_FLOW        = PATH_BASE + 'flow.json'

class SSTool(object):
    def __init__(self):
        self.profile = SSProfile(FILE_PROFILE)
        self.flow    = FlowProfile(FILE_FLOW)

    def _checkPortRanges(self, port):
        port = int(port)
        if port > 0 and port <= 65536:
            return True
        return False

    def __getSSPidByFile(self):
        pid = fileHelper.getFileContent(FILE_SSERVER_PID)
        if pid == "":
            return -1
        pid.strip()
        pid.strip('\n')
        pid = int(pid)
        return pid

    def startSS(self):
        if self.isSSOpen():
            return True
        cmd = 'ssserver -qq -c ' + FILE_PROFILE + ' 2>/dev/null >/dev/null & echo $! > ' + FILE_SSERVER_PID
        res = subprocess.call(cmd, shell=True)
        # 等待一下,要给上面的进程一段时间判断启动是否正常
        time.sleep(0.5)
        if self.isSSOpen() == False:
            return False
        return True

    def stopSS(self):
        pid = self.__getSSPidByFile()
        if pid == -1:
            return False
        array = systemHelper.getProcessID('`basename ssserver`')
        if pid in array:
            systemHelper.killProcess(pid)
            os.remove(FILE_SSERVER_PID)
            return True
        return False
    
    def isSSOpen(self):
        pid = self.__getSSPidByFile()
        if pid == -1:
            return False
        array = systemHelper.getProcessID('`basename ssserver`')
        if pid in array:
            return True
        return False

    def getAnotherSSPID(self):
        array = systemHelper.getProcessID('`basename ssserver`')
        if len(array) == 0:
            return []
        pid = self.__getSSPidByFile()
        if pid == -1:
            return array
        if str(pid) in array:
            array.remove(str(pid))
        return array
    
    def killAnotherSSPID(self):
        array = self.getAnotherSSPID()
        for item in array:
            systemHelper.killProcess(item)

    def addDelPort(self, isAdd, port, pwd, limit):
        if self._checkPortRanges(port) == False:
            return False
        if isAdd:
            self.profile.addPort(port, pwd)
            self.flow.addPort(port, limit)
        else:
            self.profile.delPort(port)
            self.flow.delPort(port)

        self.profile.save(FILE_PROFILE)
        self.flow.save(FILE_FLOW)
        if self.isSSOpen():
            self.stopSS()
            self.startSS()
    
    def printPorts(self):
        if len(self.profile.ports) <= 0:
            cmdHelper.myprint('[错误] ',cmdHelper.TextColor.Red)
            print('未设置端口')

        cols =['Port','Password','Limit','Remaining']
        rows = []
        # print('--------------------------------------------------------')
        # print('| Port  |      Password     |    Limit   |  Remaining  |')
        for port, pwd in self.profile.ports.items():
            limit = self.flow.profile[port]['limit']
            used  = self.flow.profile[port]['used']
            rema  = limit - used
            if rema < 0:
                rema = 0
            limit = convertHelper.convertStorageUnitToString(limit, 'byte')
            rema  = convertHelper.convertStorageUnitToString(rema, 'byte')
            rows.append([port, pwd, limit, rema])
        cmdHelper.showTable(cols, rows, cmdHelper.TextColor.Red, cmdHelper.TextColor.Green)
            # port  = port.ljust(6)
            # pwd   = pwd.center(18)
            # limit = limit.center(11)
            # rema  = rema.center(12)
            # print('| ', end='')
            # cmdHelper.myprint(port,cmdHelper.TextColor.Green)
            # print('| ', end='')
            # cmdHelper.myprint(pwd,cmdHelper.TextColor.Green)
            # print('| ', end='')
            # cmdHelper.myprint(limit,cmdHelper.TextColor.Green)
            # print('| ', end='')
            # cmdHelper.myprint(rema,cmdHelper.TextColor.Green)
            # print('|')
        # print('--------------------------------------------------------')

    def printStatus(self):
        print('[状态] ', end='')
        if self.isSSOpen():
            cmdHelper.myprint('已启动\n',cmdHelper.TextColor.Green)
        else:
            cmdHelper.myprint('停止\n',cmdHelper.TextColor.Red)

