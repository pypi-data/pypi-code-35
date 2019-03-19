from aigpy import cmdHelper
from aigpy import convertHelper
from ss_py.sstool import SSTool

def printMenu(tool):
    print('======================')
    cmdHelper.myprint('1.  ',cmdHelper.TextColor.Green)
    print('启动')
    cmdHelper.myprint('2.  ',cmdHelper.TextColor.Green)
    print('停止')
    cmdHelper.myprint('3.  ',cmdHelper.TextColor.Green)
    print('菜单')
    print('-------------')
    cmdHelper.myprint('4.  ',cmdHelper.TextColor.Green)
    print('添加用户')
    cmdHelper.myprint('5.  ',cmdHelper.TextColor.Green)
    print('删除用户')
    cmdHelper.myprint('6.  ',cmdHelper.TextColor.Green)
    print('显示用户')
    print('')
    tool.printStatus()
    print('======================')

def main(argv=None):
    tool = SSTool()
    printMenu(tool)
    while True:
        cmdHelper.myprint('输入选择:',cmdHelper.TextColor.Yellow)
        choice = cmdHelper.myinputInt('',9999)
        if choice == 1:
            tool.startSS()
            tool.printStatus()
        elif choice == 2:
            tool.stopSS()
            tool.printStatus()
        elif choice == 3:
            printMenu(tool)
        elif choice == 4:
            port  = cmdHelper.myinputInt('端口:', -1)
            pwd   = cmdHelper.myinput('密码:')
            limit = cmdHelper.myinputInt('流量(G):', 1)
            limit = convertHelper.convertStorageUnit(limit, 'gb', 'byte')
            tool.addDelPort(True, port, pwd, limit)
        elif choice == 5:
            port = cmdHelper.myinputInt('端口:', -1)
            tool.addDelPort(False, port, None, None)
        elif choice == 6:
            tool.printPorts()

def main2(argv=None):
    pass


__all__ = ['main', 'main2']
