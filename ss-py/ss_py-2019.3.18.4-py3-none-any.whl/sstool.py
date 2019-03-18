import sys
import subprocess
from aigpy import cmdHelper
from aigpy import fileHelper
from ss_py.ssprofile import SSProfile

PATH_BASE        = '/etc/ss_py/'
FILE_PROFILE     = PATH_BASE + 'profile.json'
FILE_SSERVER_PID = PATH_BASE + 'ssserverpid.txt'

class SSTool(object):
    def __init__(self):
        self.profile = SSProfile(FILE_PROFILE)

    def _checkPortRanges(self, port):
        port = int(port)
        if port > 0 and port <= 65536:
            return True
        return False

    def startSS(self):
        if self.isSSOpen():
            self.stopSS()
        cmd = 'ssserver -qq -c ' + FILE_PROFILE + ' 2>/dev/null >/dev/null & echo $! > ' + FILE_SSERVER_PID
        res = subprocess.call(cmd, shell=True)
        if res != 0:
            return False
        if self.isSSOpen() == False:
            return False
        return True

    def stopSS(self):
        cmd = 'kill `cat ' + FILE_SSERVER_PID + '` 2>/dev/null'
        res = subprocess.call(cmd, shell=True)
        if res == 0:
            return True
        return False
    
    def isSSOpen(self):
        pid = fileHelper.getFileContent(FILE_SSERVER_PID)
        if pid == "":
            return False
        cmd = 'ps `cat ' + FILE_SSERVER_PID + '` 2>/dev/null | grep `basename ssserver` 2>/dev/null >/dev/null'
        res = subprocess.call(cmd, shell=True)
        if res == 0:
            return True
        return False
        
    def addDelPort(self, isAdd, port, pwd):
        if self._checkPortRanges(port) == False:
            return False
        if isAdd:
            self.profile.addPort(port, pwd)
        else:
            self.profile.delPort(port)
        self.profile.save(FILE_PROFILE)
        if self.isSSOpen():
            self.stopSS()
            self.startSS()
    
    def printPorts(self):
        if len(self.profile.ports) <= 0:
            cmdHelper.myprint('[错误] ',cmdHelper.TextColor.Red)
            print('未设置端口')
        print('-----------------------------')
        print('| Port  |      Password     |')
        for key,value in self.profile.ports.items():
            key = key.ljust(6)
            value = value.center(18)
            print('| ', end='')
            cmdHelper.myprint(key,cmdHelper.TextColor.Green)
            print('| ', end='')
            cmdHelper.myprint(value,cmdHelper.TextColor.Green)
            print('|')
        print('-----------------------------')

    def printStatus(self):
        print('[状态] ', end='')
        if self.isSSOpen():
            cmdHelper.myprint('已启动\n',cmdHelper.TextColor.Green)
        else:
            cmdHelper.myprint('停止\n',cmdHelper.TextColor.Red)
