# bot/entry.py
#
#

""" simple data entry commands. """

from obj.base import Dotted

## entry

class Log(Dotted):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(Dotted):

    def __init__(self):
        super().__init__()
        self.txt = ""

def log(event):
    obj = Log()
    obj.txt = event.rest
    obj.save(timed=True)
    event.ok(1)

def todo(event):
    obj = Todo()
    obj.txt = event.rest
    obj.save(timed=True)
    event.ok(1)
