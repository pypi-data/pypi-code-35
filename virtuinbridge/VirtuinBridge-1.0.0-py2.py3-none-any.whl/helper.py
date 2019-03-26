import os
# IronPython modules
try:
    from System.Diagnostics import Process
    __VIRT_ANDUIN_ENV__ = True
# Python 2/3 modules
except ImportError:
    __VIRT_ANDUIN_ENV__ = False
    from subprocess import Popen, PIPE

import virtuinglobalstubs as anduinFuncStubs


def getAnduinGlobalStubs():
    """ Create stubs for Anduin injected global routines. """
    globalStubs = dict()
    for name in dir(anduinFuncStubs):
        if name.startswith('_'):
            continue
        attr = getattr(anduinFuncStubs, name, None)
        globalStubs[name] = attr
    return globalStubs


def getAnduinGlobalData(anduinGlobals):
    """
    Extracts Anduin configs that are injected globally including
    slot, slot.Dut, station, and TestSpecs
    Args:
        None
    Returns:
        dict: Python dict with keys dut, station, and specs.
    """
    configs = dict(dut={}, station={}, specs={})
    # On Anduin get real configs
    if __VIRT_ANDUIN_ENV__:
        lclDut = net2dict(anduinGlobals['slot'].Dut)
        configs['dut'].update(lclDut)
        lclStation = net2dict(anduinGlobals['station'])
        kvKey = 'translateKeyValDictionary'
        stationConstants = anduinGlobals[kvKey](anduinGlobals['station'].Constants)
        lclStation.update(stationConstants)
        configs['station'].update(lclStation)
        for specName, specDict in anduinGlobals['TestSpecs'].iteritems():
            fullSpecDict = dict(lsl=None, usl=None, details='')
            fullSpecDict.update(specDict.copy())
            if "counts_in_result" in fullSpecDict:
                # IronPython json uses incorrect boolean so change to string
                fullSpecDict["counts"] = str(fullSpecDict["counts_in_result"])
                fullSpecDict["counts_in_result"] = fullSpecDict["counts"]
            configs['specs'][specName] = fullSpecDict
    # Get dummy configs
    else:
        configs['dut'] = anduinGlobals.get('dut', {})
        configs['specs'] = anduinGlobals.get('specs', {})
        configs['station'] = anduinGlobals.get('station', {})
    return configs

def getVirtuinPath():
    """
    Helper function to find Virtuin GUI path
    Args:
        None
    Returns:
        str: GUI Path
    """
    # Check if VirtuinGUI is env variable and exists
    virtuinGUI = os.environ.get('VIRT_GUI_PATH', None)
    if virtuinGUI and os.path.isfile(virtuinGUI) and os.access(virtuinGUI, os.X_OK):
        return virtuinGUI

    # Check if VIRT_PATH/bin/VirtuinGUI exists
    virtuinPath = os.environ.get('VIRT_PATH', '')
    virtuinGUI = os.path.join(virtuinPath, 'bin', 'VirtuinGUI.exe').replace('\\', '/')
    if virtuinGUI and os.path.isfile(virtuinGUI) and os.access(virtuinGUI, os.X_OK):
        return virtuinGUI
    virtuinGUI = os.path.join(virtuinPath, 'bin', 'VirtuinGUI.exe.lnk').replace('\\', '/')
    if virtuinGUI and os.path.isfile(virtuinGUI) and os.access(virtuinGUI, os.X_OK):
        return virtuinGUI

    # See if already on path
    virtuinGUI = 'VirtuinGUI.exe'
    if os.path.isfile(virtuinGUI) and os.access(virtuinGUI, os.X_OK):
        return virtuinGUI

    raise Exception('Unable to locate VirtuinGUI')

def runCommand(args, inputStr=None):
    """
    Helper function to run child process using .NET Process or built-in subprocess
    Args:
        args (list: str): Command arguments w/ first
        being executable.
        inputStr (str, None): Standard input to pass in.
    Returns:
        str: Standard output
        str: Standard error
        int: Process exit code
    """
    p = None
    stdout = None
    stderr = None
    code = 130
    try:
        if __VIRT_ANDUIN_ENV__:
            p = Process()
            have_stdin = inputStr is not None
            p.StartInfo.UseShellExecute = False
            p.StartInfo.RedirectStandardInput = have_stdin
            p.StartInfo.RedirectStandardOutput = True
            p.StartInfo.RedirectStandardError = True
            p.StartInfo.FileName = args[0]
            p.StartInfo.Arguments = " ".join(args[1:])
            p.Start()
            if have_stdin:
                p.StandardInput.Write(inputStr)
            p.WaitForExit()
            stdout = p.StandardOutput.ReadToEnd()
            stderr = p.StandardError.ReadToEnd()
            code = p.ExitCode
        else:
            p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate(inputStr)
            code = p.returncode
        return stdout, stderr, code
    except KeyboardInterrupt:
        if p:
            p.kill()
            stderr = 'Process terminated by user. {0}'.format(stderr if stderr else '')
            code = 130
        return stdout, stderr, code


def net2dict(obj):
    """
    Converts .NET object public primitive attributes to python dict.
    .NET bool gets mapped to int due to IronPython compatibility issue.
    Function performs only shallow mapping (non-recursive).
    Args:
        obj (.Net object): .Net object
    Returns:
        dict: converted python dict
    """
    def _isPrimitive(var):
        return isinstance(var, (int, float, bool, str))

    attrs = (name for name in dir(obj) if not name.startswith('_') and
             _isPrimitive(obj.__getattribute__(name)))
    objDict = dict()
    for attribute in attrs:
        val = obj.__getattribute__(attribute)
        # IronPython json uses incorrect boolean so change to int
        val = int(val) if isinstance(val, bool) else val
        objDict[attribute] = val
    return objDict
