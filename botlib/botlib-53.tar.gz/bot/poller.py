# bot/poller.py
#
#

""" polling based handler. """

import logging
import os
import select

import bot
import bot.base
import bot.handler
import bot.tasks

from bot.tasks import launch
from bot.utils import get_name

## exceptions

class ENOTIMPLEMENTED(Exception):
    pass

## classes

class Poller(bot.handler.Handler):

    def __init__(self):
        super().__init__()
        self._fds = []
        self._poll = select.epoll()
        self._stopped = False
        self.resume = bot.base.Dotted()

    def events(self):
        self._poll.poll()
        yield self.get_event()

    def get_event(self):
        raise ENOTIMPLEMENTED

    def register_fd(self, fd):
        if "fileno" in dir(fd):
            fd = fd.fileno()
        #self._poll.register(fd, select.EPOLLET)
        self._poll.register(fd)
        self._fds.append(fd)
        self.resume.fd = fd
        os.set_inheritable(self.resume.fd, os.O_RDWR)

    def resume(self):
        if not self.resume.fd:
             raise ERESUME
        logging.info("! resume on %s" % self.resume.fd)
        self._poll = select.epoll.fromfd(self.resume.fd)

    def loop(self):
        while not self._stopped:
            for event in self.events():
                if not event:
                    self._stopped = True
                    break
                self.put(event)
        self.stop()

    def register(self, bot):
        logging.warning("register %s" % get_name(bot))
        self.register_fd(bot)

    def start(self):
        self._stopped = False
        super().start()
        launch(self.work)

    def stop(self):
        for fd in self._fds:
            self.unregister_fd(fd)

    def unregister_fd(self, fd):
        if fd in self._fds:
            self._fds.remove(fd)
        try:
            self._poll.unregister(fd)
        except (PermissionError, FileNotFoundError):
            pass
