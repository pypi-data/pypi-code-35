# OBJ - Timestamped JSON objects
#
# obj/run.py

""" place to stash runtime objects. """

import sys

from obj.base import Cfg
from bot.kernel import Kernel
from bot.users import Users

cfg = Cfg()
kernel = Kernel()
users = Users()

## functions

def cmd(txt):
    e = kernel.cmd(txt)
    e.wait()
    return e
    
def get(name):
    return getattr(sys.modules[__name__], name, None)

def set(name, obj):
    return setattr(sys.modules[__name__], name, obj)
