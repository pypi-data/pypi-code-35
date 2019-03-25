# bot/irc.py
#
#

""" IRC bot module. """

import logging
import os
import queue
import re
import socket
import ssl
import textwrap
import time
import threading

import bot
import bot.base
import bot.bot
import bot.event
import bot.store
import bot.tasks
import bot.users
import bot.utils

from bot.base import cfg, get_type, sliced, __version__, __txt__
from bot.kernel import kernel
from bot.tasks import launch
from bot.utils import locked

## classes

class Cfg(bot.base.Dotted):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.blocking = 1
        self.channel = "#bot"
        self.ipv6 = False
        self.nick = "bot"
        self.port = 6667
        self.realname = "boti the bot"
        self.server = ""
        self.ssl = False
        self.username = "bot"

class IEvent(bot.event.Event):

    def __init__(self, txt):
        super().__init__(txt)
        self.arguments = []
        self.cc = ""
        self.channel = ""
        self.command = ""
        self.nick = ""
        self.target = ""

class DEvent(bot.event.Event):

    def __init__(self, txt):
        super().__init__(txt)
        self._sock = None
        self._fsock = None
        self.channel = ""

class TextWrap(textwrap.TextWrapper):

    def __init__(self):
        super().__init__()
        self.drop_whitespace = False
        self.fix_sentence_endings = True
        self.replace_whitespace = True
        self.tabsize = 4
        self.width = 500

class IRC(bot.bot.Bot):

    def __init__(self):
        super().__init__()
        self._buffer = []
        self._connected = threading.Event()
        self._outqueue = queue.Queue()
        self._sock = None
        self._fsock = None
        self._threaded = True
        self.cc = "!"
        self.cfg = Cfg()
        self.channels = []
        self.resume = bot.base.Dotted()
        self.state = bot.base.Dotted()
        self.state.error = ""
        self.state.last = 0
        self.state.lastline = ""
        self.state.nrsend = 0
        self.state.pongcheck = False
        self.register("352", self.handler)
        self.register("366", self.handler)
        self.register("376", self.handle_connect)
        self.register("433", self.handler)
        self.register("ERROR", self.handle_error)
        self.register("MODE", self.handler)
        self.register("PING", self.handler)
        self.register("PONG", self.handler)
        self.register("PRIVMSG", self.handle_privmsg)

    def _parsing(self, txt):
        rawstr = str(txt)
        obj = IEvent(rawstr)
        obj.txt = ""
        obj.cc = self.cc
        obj.command = ""
        obj.arguments = []
        arguments = rawstr.split()
        obj.origin = arguments[0]
        if obj.origin.startswith(":"):
            obj.origin = obj.origin[1:]
            if len(arguments) > 1:
                obj.command = arguments[1]
            if len(arguments) > 2:
                txtlist = []
                adding = False
                for arg in arguments[2:]:
                    if arg.startswith(":"):
                        adding = True
                        txtlist.append(arg[1:])
                        continue
                    if adding:
                        txtlist.append(arg)
                    else:
                        obj.arguments.append(arg)
                    obj.txt = " ".join(txtlist)
        else:
            obj.cmd = obj.command = obj.origin
            obj.origin = self.cfg.server
        try:
            obj.nick, obj.origin = obj.origin.split("!")
        except ValueError:
            obj.nick = ""
        if obj.arguments:
            obj.target = obj.arguments[-1]
        else:
            obj.target = ""
        if obj.target.startswith("#"):
            obj.channel = obj.target
        else:
            obj.channel = obj.nick
        if not obj.txt:
            if rawstr[0] == ":":
                rawstr = rawstr[1:]
            obj.txt = rawstr.split(":", 1)[-1]
        if not obj.txt and len(arguments) == 1:
            obj.txt = arguments[1]
        obj.args = obj.txt.split()
        obj.orig = repr(self)
        obj.rest = " ".join(obj.args)
        obj.parse()
        return obj

    def _some(self, use_ssl=False, encoding="utf-8"):
        if use_ssl:
            inbytes = self._sock.read()
        else:
            inbytes = self._sock.recv(512)
        txt = str(inbytes, encoding)
        if txt == "":
            raise ConnectionResetError
        txt = bytes(txt, "utf-8").decode("unicode_escape")
        self.state.lastline += txt
        splitted = self.state.lastline.split("\r\n")
        for s in splitted[:-1]:
            self._buffer.append(s)
            if not s.startswith("PING") and not s.startswith("PONG"):
                logging.warning(s.strip())
        self.state.lastline = splitted[-1]

    def announce(self, txt):
        for channel in self.channels:
            self.say(repr(self), channel, txt)

    def command(self, cmd, *args):
        if not args:
            self.raw(cmd)
            return
        if len(args) == 1:
            self.raw("%s %s" % (cmd.upper(), args[0]))
            return
        if len(args) == 2:
            self.raw("%s %s :%s" % (cmd.upper(), args[0], " ".join(args[1:])))
            return
        if len(args) >= 3:
            self.raw("%s %s %s :%s" % (cmd.upper(), args[0], args[1], " ".join(args[2:])))
            return

    def connect(self):
        oldsock = None
        if self.cfg.ipv6:
            oldsock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            oldsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        oldsock.setblocking(int(self.cfg.blocking or True))
        oldsock.settimeout(60.0)
        oldsock.connect((self.cfg.server, int(self.cfg.port)))
        oldsock.setblocking(int(self.cfg.blocking))
        oldsock.settimeout(700.0)
        if self.cfg.ssl:
            self._sock = ssl.wrap_socket(oldsock)
        else:
            self._sock = oldsock
        self.resume.fd = self._sock.fileno()
        self._fsock = self._sock.makefile("r")
        os.set_inheritable(self.resume.fd, os.O_RDWR)
        self._connected.set()
        logging.warning("connect %s %s" % (self.cfg.server, self.cfg.port))
        return True

    def dispatch(self, event):
        if event.command:
            func = self.get_handler(event.command)
            if func:
                func(event)
                return
        super().dispatch(event)

    def get_event(self):
        if not self._buffer:
            try:
                self._some()
            except socket.timeout as ex:
                e = IEvent(str(ex))
                e.command = "ERROR"
                return e
        return self._parsing(self._buffer.pop(0))

    def handle_connect(self, event):
        if "servermodes" in self:
            self.raw("MODE %s %s" % (self.cfg.nick, self.cfg.servermodes))
        self.joinall()

    def handle_error(self, event):
        logging.error(event.txt)
        self.state.error = event

    def handle_privmsg(self, event):
        users.userhosts[event.nick] = event.origin
        if not users.allowed(event.origin, "USER"):
            return
        if event.txt.startswith("\001DCC"):
            try:
                dcc = DCC()
                kernel.add(dcc)
                dcc.encoding = "utf-8"
                launch(dcc.connect, event)
                return
            except ConnectionRefusedError:
                return
        elif event.txt.startswith("\001VERSION"):
            txt = "\001VERSION %s %s - %s\001" % ("BOTLIB", __version__, __txt__)
            self.command("NOTICE", event.channel, txt)
            return
        if event.txt and event.txt[0] == self.cc:
            event.txt = event.txt[1:]
            event.txt = self.get_aliased(event.txt)
            event.parse()
        super().dispatch(event)

    def handler(self, event):
        cmd = event.command
        if cmd == "PING":
            self.state.pongcheck = True
            self.command("PONG", event.txt)
        elif cmd == "PONG":
            self.state.pongcheck = False
        elif cmd == "433":
            nick = event.target + "_"
            self.cfg.nick = nick
            self.command("NICK", nick)

    def joinall(self):
        for channel in self.channels:
            self.command("JOIN", channel)

    def logon(self, server, nick):
        self._connected.wait()
        self.raw("NICK %s" % nick, True)
        self.raw("USER %s %s %s :%s" % (self.cfg.username, server, server, self.cfg.realname), True)

    def loop(self):
        try:
            self._connected.wait()
            super().loop()
        except ConnectionResetError:
            self.stop()
            self.start()

    def output(self):
        self._connected.wait()
        while not self._stopped:
            channel, txt = self._outqueue.get()
            if not channel and not txt:
                break
            self.command("PRIVMSG", channel, txt)

    @locked
    def raw(self, txt, direct=False):
        self._connected.wait()
        txt = txt.rstrip()
        if self._stopped:
            return
        if not txt.startswith("PING") and not txt.startswith("PONG"):
            logging.warning(txt)
        if not txt.endswith("\r\n"):
            txt += "\r\n"
        txt = txt[:512]
        txt = bytes(txt, "utf-8")
        if not direct:
            if (time.time() - self.state.last) < 3.0:
                time.sleep(1.0 * (self.state.nrsend % 10))
        self.state.last = time.time()
        self.state.nrsend += 1
        self._sock.send(txt)

    def say(self, orig, channel, txt):
        wrapper = TextWrap()
        txt = str(txt)
        for line in txt.split("\n"):
            for t in wrapper.wrap(line):
                self._outqueue.put((channel, t))

    def start(self):
        last = store.last(get_type(self.cfg))
        if last:
            self.cfg.update(last)
        prev = bot.base.Dotted(self.cfg)
        self.cfg.upgrade(cfg)
        if prev != self.cfg:
            self.cfg.save()
        if self.cfg.channel:
            self.channels.append(self.cfg.channel)
        nr = 1
        self.state.error = ""
        while 1:
            try:
                self.connect()
                break
            except socket.gaierror as ex:
                logging.warn(ex)
                break
            except ConnectionRefusedError:
                txt = "%s connection refused" % self.cfg.server
                logging.warning(txt)
                break
            time.sleep(nr * 3.0)
            nr += 1
        if not self.state.error:
            self.logon(self.cfg.server, self.cfg.nick)
            super().start()
            launch(self.output)
        return self

    def stop(self):
        self._stopped = True
        super().stop()
        self._outqueue.put_nowait((None, None))
        self.ready()

class DCC(bot.bot.Bot):

    def __init__(self):
        super().__init__()
        self._sock = None
        self._fsock = None
        self.encoding = "utf-8"
        self.origin = ""

    def announce(self, txt):
        self.raw(txt)

    def connect(self, event):
        arguments = event.txt.split()
        addr = arguments[3]
        port = arguments[4][:-1]
        port = int(port)
        if re.search(':', addr):
            s = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((addr, port))
        s.send(bytes('Welcome to %s %s !!\n' % (cfg.name, event.nick), "utf-8"))
        s.setblocking(True)
        os.set_inheritable(s.fileno(), os.O_RDWR)
        self._sock = s
        self._fsock = self._sock.makefile("rw")
        self.origin = event.origin
        super().start()

    def errored(self, event):
        self.state.error = event
        logging.error(str(event))

    def event(self, txt):
        txt = self.get_aliased(txt)
        e = DEvent(txt)
        e._sock = self._sock
        e._fsock = self._fsock
        e.orig = repr(self)
        e.channel = self.origin
        e.origin = self.origin or "root@dcc"
        return e

    def get_event(self):
        txt = self._fsock.readline()
        return self.event(txt)

    def raw(self, txt):
        self._fsock.write(txt.rstrip())
        self._fsock.write("\n")
        self._fsock.flush()

    def say(self, orig, channel, txt):
        self.raw(txt)

## instances

store = bot.store.Store()
users = bot.users.Users()

## functions

def init():
    bot = IRC()
    kernel.add(bot)
    thr = launch(bot.start)
    return thr