# OBJ - Timestamped JSON objects
#
# obj/run.py

""" place to stash runtime objects. """

import sys

from obj.store import Store
from bot.fleet import Fleet
from bot.users import Users

fleet = Fleet()
store = Store()
users = Users()

def get(name):
    return getattr(sys.modules[__name__], name, None)

def set(name, obj):
    return setattr(sys.modules[__name__], name, obj)
