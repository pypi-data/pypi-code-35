import sys
import os
from importlib import import_module

class Commander:

    def __init__(self, arguments):
        self.arguments = arguments
        sys.path.insert(1, os.getcwd())
        self.cmdname = ''
        for key in arguments:
            if arguments[key] == True:
                self.cmdname = key
                break
        
        self.module = import_module('cli.%s.%s' % ('cmd', self.cmdname))
        
    def run(self):
        cmdclass = ''.join(x for x in self.cmdname.title() if not x.isspace())
        self.cmd = getattr(self.module, cmdclass)()
        return getattr(self.cmd, 'main')(args=self.arguments)