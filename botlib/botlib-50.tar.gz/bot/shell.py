# bot/shell.py
#
#

""" shell related commands. """

import atexit
import logging
import logging.handlers
import optparse
import os
import os.path
import readline
import rlcompleter
import stat
import sys
import termios

from bot.base import Dotted, OutputCache, cdir, cfg, get_type
from bot.bot import Bot
from bot.tasks import launch
from bot.utils import get_exception

## defines

opts = [
    ('-a', '', 'store_true', False, 'all', 'load all modules'),
    ('-b', '', 'store_true', False, 'background', 'enable daemon mode.'),
    ('-c', '', "string", '', 'channel', 'channel to join.'),
    ('-d', '', 'string', '', 'workdir', 'set working directory.'),
    ('-l', '', 'string', 'error', 'level', 'loglevel.'),
    ('-m', '', 'string', '', 'modules', 'modules to load.'),
    ('-n', '', 'string', '', 'nick', 'nickname to use when joining a channel'),
    ('-o', '', "string", '', 'options', 'character options to use.'),
    ('-p', '', "string", '', 'password', 'provide password to login with.'),
    ('-s', '', 'string', '', 'server', 'connect server channel nick.'),
    ('-v', '', 'store_true', False, 'verbose', 'enable verbose mode.'),
    ('-x', '', 'string', '', 'exclude', 'exclude module'),
    ('-y', '', 'store_true', False, 'yes', 'use yes as default answer.'),
    ('-z', '', "store_true", False, 'shell', 'enable shell.'),
    ('', '--debug', "store_true", False, 'debug', 'enable debug mode.'),
    ('', '--logdir', "string", "" , 'logdir', 'logging directory'),
    ('', '--name', "string", "", 'name', 'name of the program.'),
    ('', '--port', "store_true", False, 'port', 'provide port number to connect to.'),
    ('', '--resume', "store_true", False, 'resume', 'resume from filedescriptor.'),
]

def ld(*args):
    return os.path.abspath(os.path.join(cfg.logdir, *args))

histfile = ""
resume = {}

## classes

class Completer(rlcompleter.Completer):

    def __init__(self, commands=None):
        super().__init__()
        self.commands = commands or []
        self.matches = []

    def complete(self, text, state):
        if state == 0:
            if text: 
                self.matches = [s for s in self.commands if s and s.startswith(text)]
            else:
                self.matches = self.commands[:]
        try:
            return self.matches[state]
        except IndexError:
            return None

class DumpHandler(logging.StreamHandler):

    propagate = False

    def emit(self, record):
        pass

class Shell(Bot):

    def __init__(self):
        super().__init__()
        self._err = sys.stderr
        self._in = sys.stdin
        self._out = sys.stdout
        self._type = get_type(self)
        self._userhosts = Dotted()
        self.cache = OutputCache()
        self.prompt = True

    def announce(self, txt):
        self.raw(txt)

    def dispatch(self, event):
        super().dispatch(event)
        event.wait()
        self.show_prompt()
     
    def get_event(self):
        import bot.event
        txt = input()
        if not txt:
            self._out.write("\n")
            self.show_prompt()
            return
        txt = self.get_aliased(txt)
        e = bot.event.Event(txt)
        e.orig = repr(self)
        e.origin = "root@shell"
        return e

    def raw(self, txt):
        if self.verbose:
            self._out.write(str(txt))
            self._out.write("\n")
            #self._out.flush()

    def resume(self):
        pass

    def say(self, botid, channel, txt):
        self.cache.add(channel, txt)
        super().say(botid, channel, txt)

    def show_prompt(self):
        if self.prompt:
            self._out.write("> ")
            self._out.flush()
        
    def start(self):
        logging.warning("starting shell")
        if not cfg.workdir:
            cfg.workdir = hd(".bot")
            cdir(cfg.workdir)
        if cfg.resume:
            self.resume()
        super().start()
        set_completer(self.names.keys())

## utility functions

def check_permissions(path, dirmask=0o700, filemask=0o600):
    uid = os.getuid()
    gid = os.getgid()
    try:
        stats = os.stat(path)
    except FileNotFoundError:
        return
    except OSError:
        dname = os.path.dirname(path)
        cdir(dname)
        stats = os.stat(dname)
    if stats.st_uid != uid:
        os.chown(path, uid, gid)
    if os.path.isfile(path):
        mask = filemask
    else:
        mask = dirmask
    mode = oct(stat.S_IMODE(stats.st_mode))
    if mode != oct(mask):
        os.chmod(path, mask)

def close_history():
    try:
        readline.write_history_file(histfile)
    except:
        pass

def daemon():
    pid = os.fork()
    if pid != 0:
        reset()
        os._exit(0)
    os.setsid()
    os.umask(0)
    pid = os.fork()
    if pid != 0:
        reset()
        os._exit(0)
    if not os.path.exists(cfg.logdir):
        cdir(cfg.logdir)
    path = os.path.join(cfg.logdir, "pidfile")
    f = open(path, 'w')
    f.write(str(os.getpid()))
    f.flush()
    f.close()
    sys.argv[0] = "bot"
    sys.stdout.flush()
    sys.stderr.flush()
    si = open("/dev/null", 'r')
    so = open("/dev/null", 'a+')
    se = open("/dev/null", 'a+')
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def enable_history():
    readline.read_history_file(histfile)
    atexit.register(close_history)

def get_completer() -> Completer:
    return readline.get_completer()

def level(loglevel, logfile="bot.log", nostream=False):
    if not os.path.exists(cfg.logdir):
        cdir(cfg.logdir)
    logfile = os.path.join(cfg.logdir, logfile)
    datefmt = '%H:%M:%S'
    format_time = "%(asctime)-8s %(message)-70s"
    format_plain = "%(message)-0s"
    loglevel = loglevel.upper()
    logger = logging.getLogger("")
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    if logger.handlers:
        for handler in logger.handlers:
            logger.removeHandler(handler)
    try:
        logger.setLevel(loglevel)
    except ValueError:
        print("no level %s" % loglevel)
        return
    formatter = logging.Formatter(format_plain, datefmt)
    if nostream:
        dhandler = DumpHandler()
        dhandler.propagate = False
        dhandler.setLevel(loglevel)
        logger.addHandler(dhandler)
    else:
        handler = logging.StreamHandler()
        handler.propagate = False
        handler.setFormatter(formatter)
        handler.setLevel(loglevel)
        logger.addHandler(handler)
    formatter2 = logging.Formatter(format_time, datefmt)
    filehandler = logging.handlers.TimedRotatingFileHandler(logfile, 'midnight')
    filehandler.propagate = False
    filehandler.setFormatter(formatter2)
    filehandler.setLevel(loglevel)
    logger.addHandler(filehandler)
    return logger

def make_opts(options, usage, version):
    parser = optparse.OptionParser(usage=usage, version=version)
    for opt in options:
        otype, deft, dest, htype = opt[2:]
        if "store" in otype:
            parser.add_option(opt[0], opt[1], action=otype, default=deft, dest=dest, help=htype)
        else:
            parser.add_option(opt[0], opt[1], type=otype, default=deft, dest=dest, help=htype)
    return parser.parse_args()

def parse_cli(name="bot", options=None, usage="", version="", workdir=""):
    global histfile
    ver = "%s #%s" % (name.upper(), version)
    if not options:
        options = opts
    opt, arguments = make_opts(options, usage, ver)
    cfg.update(vars(opt))
    cfg.logdir = os.path.abspath(os.path.join(os.path.expanduser("~"), ".%slogs" % name))
    cfg.name = name
    cfg.version = version
    cfg.args = arguments
    if workdir:
        cfg.workdir = cfg.workdir or workdir
    if not cfg.workdir:
        cfg.workdir = os.path.abspath(os.path.join(os.path.expanduser("~"), ".%s" % cfg.name))
    if not os.path.exists(cfg.workdir):
        cdir(cfg.workdir)
    if not os.path.exists(cfg.logdir):
        cdir(cfg.logdir)
    histfile = ld("history")
    touch(histfile)
    readline.read_history_file(histfile)
    return cfg

def reset():
    close_history()
    if "old" in resume:
        termreset(resume["fd"], resume["old"])

def set_completer(commands):
    completer = Completer(commands)
    #readline.set_completer_delims(' ')
    #readline.set_completion_display_matches_hook(completer.display)
    readline.set_completer(completer.complete)
    readline.parse_and_bind("tab: complete")
    atexit.register(lambda: readline.set_completer(None))

def startup():
    resume["fd"] = sys.stdin.fileno()
    resume["old"] = termsetup(sys.stdin.fileno())
    atexit.register(reset)

def termreset(fd, old):
    termios.tcsetattr(fd, termios.TCSADRAIN, old)

def termsetup(fd):
    old = termios.tcgetattr(fd)
    return old

def touch(fname):
    try:
        fd = os.open(fname, os.O_RDONLY | os.O_CREAT)
        os.close(fd)
    except TypeError:
        pass

if __name__ == "__main__":
    startup()
    try:
        shell = Shell()
        shell.start()
        shell.wait()
    except Exception as ex:
        logging.error(get_exception())
    reset()    
