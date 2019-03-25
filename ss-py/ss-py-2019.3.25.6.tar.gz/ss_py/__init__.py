from aigpy import cmdHelper
from aigpy import convertHelper
from ss_py.tool import SSTool
from ss_py.tool import CountTool


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

def start(tool):
    # 检查是否已经启动
    if tool.isSSOpen():
        tool.printStatus()
        return
    # 尝试启动
    if tool.startSS():
        tool.printStatus()
        return
    # 如果启动失败则查看是否后台有其他的ss服务在运行
    pids = tool.getAnotherSSPID()
    if len(pids) > 0:
        cmdHelper.myprint('关闭其他ss服务(y/n):',cmdHelper.TextColor.Yellow)
        choice = cmdHelper.myinput('')
        # 再次尝试启动
        if choice == 'y' or choice == 'Y':
            tool.killAnotherSSPID()
            tool.startSS()
    tool.printStatus()

def main(argv=None):
    tool = CountTool()
    tool.start()
    return
    tool = SSTool()
    if tool.isCountProcess():
        tool = CountTool()
        tool.start()
        return

    printMenu(tool)
    while True:
        cmdHelper.myprint('输入选择(3显示菜单):',cmdHelper.TextColor.Yellow)
        choice = cmdHelper.myinputInt('',9999)
        if choice == 1:
            start(tool)
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

__all__ = ['main']
