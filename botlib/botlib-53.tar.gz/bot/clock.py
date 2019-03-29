# bot/clock.py
#
#

""" timers, repeaters. """

import threading
import time
import bot
import bot.base
import bot.store
import bot.tasks
import bot.utils

from bot.tasks import launch
from bot.utils import get_time, to_day

## classes

class Cfg(bot.base.Dotted):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.latest = 0

class Timers(bot.base.Dotted):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._stopped = False
        self.cfg = Cfg()
        self.timers = bot.base.Dotted()

    def loop(self):
        while not self._stopped:
            time.sleep(1.0)
            remove = []
            for t, event in self.timers.items():
                if time.time() > t:
                    self.cfg.latest = time.time()
                    self.cfg.save()
                    event.raw(event.txt)
                    remove.append(t)
            for r in remove:
                del self.timers[r]

    def start(self):
        for e in store.all("bot.clock.Timers"):
            if "done" in e and e.done:
                continue
            if "time" not in e:
                continue
            if time.time() < int(e.time):
                self.timers[e.time] = e
        return launch(self.loop)

    def stop(self):
        self._stopped = True

class Timer(bot.base.Dotted):

    def __init__(self, sleep, func, *args, **kwargs):
        super().__init__()
        self._func = func
        self._name = kwargs.get("name", bot.utils.get_name(func))
        self.sleep = sleep
        self.args = args
        self.kwargs = kwargs
        self.state = bot.base.Dotted()

    def start(self):
        timer = threading.Timer(self.sleep, self.run, self.args, self.kwargs)
        timer.setName(self._name)
        timer.sleep = self.sleep
        timer.state = self.state
        timer.state.starttime = time.time()
        timer.state.latest = time.time()
        timer._func = self._func
        timer.start()
        return timer

    def run(self, *args, **kwargs):
        self.state.latest = time.time()
        launch(self._func, *args, **kwargs)

    def exit(self):
        self.cancel()

class Repeater(Timer):

    def run(self, *args, **kwargs):
        self._func(*args, **kwargs)
        return launch(self.start)

## instances

store = bot.store.Store()

