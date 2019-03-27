# bot/entry.py
#
#

""" simple data entry commands. """

import bot
import bot.base

## entry

class Log(bot.base.Dotted):

    def __init__(self):
        super().__init__()
        self.txt = ""

class Todo(bot.base.Dotted):

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
