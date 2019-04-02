from aigpy import cmdHelper

def printErr(length, elsestr):
    cmdHelper.myprint("[ERR]".ljust(length), cmdHelper.TextColor.Red, None)
    print(elsestr)
def printSUCCESS(length, elsestr):
    cmdHelper.myprint("[SUCCESS]".ljust(length), cmdHelper.TextColor.Green, None)
    print(elsestr)
def printChoice(string, isInt=False, default=None):
    cmdHelper.myprint(string, cmdHelper.TextColor.Yellow, None)
    if not isInt:
        return cmdHelper.myinput("")
    else:
        return cmdHelper.myinputInt("",default)
def printMenu():
    print("=====================Choice=========================")
    cmdHelper.myprint(" Enter '0': ", cmdHelper.TextColor.Green, None)
    print("Exit.")
    cmdHelper.myprint(" Enter '1': ", cmdHelper.TextColor.Green, None)
    print("LogIn And Get SessionID.")
    cmdHelper.myprint(" Enter '2': ", cmdHelper.TextColor.Green, None)
    print("Setting(OutputDir/Quality/ThreadNum).")
    cmdHelper.myprint(" Enter '3': ", cmdHelper.TextColor.Green, None)
    print("Download Album.")
    cmdHelper.myprint(" Enter '4': ", cmdHelper.TextColor.Green, None)
    print("Download Track.")
    cmdHelper.myprint(" Enter '5': ", cmdHelper.TextColor.Green, None)
    print("Download PlayList.")
    cmdHelper.myprint(" Enter '6': ", cmdHelper.TextColor.Green, None)
    print("Download Video.")
    cmdHelper.myprint(" Enter '7': ", cmdHelper.TextColor.Green, None)
    print("Download Favorite.")
    print("====================================================")
