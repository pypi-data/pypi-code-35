# btz/handler.py
#
#

""" event handler. """

import threading

from obj.base import cfg
from obj.command import Command

## classes

class Event(Command):

    def __init__(self, txt=""):
        super().__init__(txt)
        self._func = None
        self._ready = threading.Event()
        self._result = []
        self._results = []
        self._target = None
        self._thrs = []
        self._trace = ""
        self.batched = True
        self.channel = ""

    def display(self):
        from bot.run import kernel
        for txt in self._result:
            kernel.announce(txt)

    def ok(self, txt=""):
        self.reply("ok %s" % txt or self.cmd.cmd)

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self._result.append(txt)

    def show(self, bot):
        for txt in self._result:
            bot.say(self.orig, self.channel, txt)

    def wait(self):
        self._ready.wait()
        result = []
        thrs = []
        for thr in self._thrs:
            try:
                ret = thr.join()
            except RuntimeError:
                continue
            thrs.append(thr)
            self._results.append(ret)
        for thr in thrs:
            self._thrs.remove(thr)
        return self
