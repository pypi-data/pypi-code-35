# bot/base.py
#
#

""" base classes. """

import datetime
import importlib
import json
import logging
import os
import os.path
import string
import time
import types

## defines

__version__ = 15
__txt__ = "Framework to program bots"

basic_types = [str, int, float, bool, None]
allowedchars = string.ascii_letters + string.digits + "_,-. \n" + string.punctuation
allowednamechars = string.ascii_letters + string.digits + '!.@'

starttime = time.time()

## defines

classes = {
         "Aliases": "bot.cmds",
         "Bot": "bot.bot",
         "Cache": "bot.base",
         "Cfg": "bot,bot.irc,bot.rss,bot.xmpp",
         "Dotted": "bot.base",
         "Email": "bot.email",
         "Event": "bot.event",
         "Feed": "bot.rss",
         "Fleet": "bot.fleet",
         "Handler": "bot.handler",
         "Log": "bot.entry",
         "Object": "bot.base",
         "OutputCache": "bot.bot",
         "Poller": "bot.poller",
         "Register": "bot.base",
         "Rss": "bot.rss",
         "Seen": "bot.rss",
         "Selector": "bot.store",
         "Shell": "bot.bot",
         "Store": "bot.store",
         "Task": "bot.tasks",
         "Todo": "bot.entry",
         "Worker": "bot.handler",
         "User": "bot.users",
         "Users": "bot.users"
}

## exceptions

class EOVERLOAD(Exception):
    pass

class ENOPATH(Exception):
    pass

## classes

class Object:

    def __iter__(self):
        return iter(self.__dict__)

    def __repr__(self) -> str:
        return "%s.%s at %s" % (
            self.__class__.__module__,
            self.__class__.__name__,
            str(hex(id(self)))
        )

    def __str__(self):
        return json.dumps(self, default=smooth, indent=4, sort_keys=True)

    def __hash__(self):
        return hash(str(self))

    def cache(self, key):
        try:
            return cache[key]
        except KeyError:
            return self.load(key)

    def dumps(self):
        return json.dumps(self, default=smooth, sort_keys=True)

    def format(self, keys=None, full=False):
        if keys is None:
            keys = sorted(self.__dict__.keys())
        res = []
        txt = ""
        for k in set(keys):
            if k.startswith("_"):
                continue
            #v = self.get_attr(k)
            try:
                v = self[k]
            except (KeyError, TypeError):
                continue
            if not v:
                continue
            v = str(v)
            if full:
                res.append("%s=%s " % (k, v))
            else:
                res.append(v)
        for v in res:
            txt += "%s " % v.strip()
        return txt.strip()

    def get_attr(self, k, d=""):
        return getattr(self, k, d)

    def load(self, path):
        assert path
        p = os.path.abspath(os.path.join(cfg.workdir, path))
        logging.debug("load %s" % path)
        with open(p) as f:
            data = json.load(f)
            for k, v in data.items():
                self.set_attr(k, v)
        self._container = {}
        self._container["path"] = path
        cache[path] = self
        return self

    def search(self, m: None):
        if not m:
            m = {}
        res = False
        for k, v in m.items():
            if k.startswith("_"):
                continue
            vv = self.get_attr(k)
            if v in str(vv):
                res = True
            else:
                res = False
                break
        return res

    def save(self, path="", stime="", timed=True):
        if not path and not stime:
            try:
                path = self._container["path"]
            except (TypeError, AttributeError, KeyError):
                pass
        if not path and timed:
            path = os.path.join(get_type(self), stime or rtime())
        if not path:
            txt = str(self)
            raise ENOPATH(txt)
        self._container = {}
        self._container["path"] = path
        logging.info("save %s" % path)
        p = os.path.abspath(os.path.join(cfg.workdir, path))
        d = os.path.dirname(p)
        if not os.path.isdir(d):
            cdir(d)
        if not self:
            txt = "EEMPTY %s" % path
            logging.error(txt)
            return path
        with open(p, "w") as f:
            json.dump(self, f, default=smooth, indent=4, sort_keys=True)
        if path not in cache:
            cache[path] = self
        return path

    def set_attr(self, k, v):
        return setattr(self, k, v)

class Dotted(Object, dict):

    def __init__(self, *args, **kwargs):
        Object.__init__(self)
        dict.__init__(self, *args, **kwargs)
        
    def __getattribute__(self, attrname):
        try:
            return self[attrname]
        except KeyError:
            return super().__getattribute__(attrname)

    def __getattr__(self, attrname):
        try:
            return self[attrname]
        except KeyError:
            try:
                return super().__getattribute__(attrname)
            except AttributeError:
                if "_default" in self:
                    self[attrname] = self["_default"]
        return self.__getattribute__(attrname)

    def __setattr__(self, key, value):
        func = self.get(key)
        if isinstance(func, types.MethodType):
            raise EOVERLOAD(key)
        if isinstance(value, types.MethodType):
            return super().__setattr__(key, value)
        return self.__setitem__(key, value)

    def __setitem__(self, key, value):
        func = self.get(key)
        if isinstance(func, types.MethodType):
            raise EOVERLOAD(key)
        return super().__setitem__(key, value)

    def join(self):
        pass

    def upgrade(self, d):
        for k, v in d.items():
            if v:
                self[k] = v
        return self

    def upgrade2(self, d):
        for k, v in self.items():
            if k in d:
                if not v:
                    self[k] = d[k]

class Cfg(Dotted):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._default = ""
        self.workdir = ""

    def __iter__(self):
        for k in self.keys():
            if k.startswith("_"):
                continue
            yield k

class OutputCache(Dotted):

    def add(self, dest, txt):
        if "dest" not in self:
            self[dest] = []
        self[dest].append(txt)

    def more(self, dest, nr=10):
        if "dest" in dir(self):
            res = self[dest][-nr:]
            del self[dest][-nr:]
            return res
        return []

class Register(Dotted):

    def register(self, k, v):
        if k not in self:
            self[k] = []
        self[k].append(v)
        return self[k]

## instances

cache = Dotted()
cfg = Cfg(_default="")
cfg.workdir = "data"
cfg.logdir = "logs"

## functions

def cdir(path):
    res = ""
    for p in path.split(os.sep):
        res += "%s%s" % (p, os.sep)
        p = os.path.abspath(os.path.normpath(res))
        try:
            os.mkdir(p)
        except (IsADirectoryError, NotADirectoryError, FileExistsError):
            pass
    return True

def construct(fn):
    try:
        type = get_fntype(fn)
        cls = get_cls(type)
        return cls().cache(fn)
    except TypeError:
        logging.error("ETYPE %s" % fn)
    except json.decoder.JSONDecodeError:
         logging.error("EDECODE %s" % fn)
    except ModuleNotFoundError:
        pass

def fn_time(daystr):
    daystr = daystr.replace("_", ":")
    datestr = " ".join(daystr.split(os.sep)[-2:])
    datestr = datestr.split(".")[0]
    try:
        t = time.mktime(time.strptime(datestr, "%Y-%m-%d %H:%M:%S"))
    except ValueError:
        t = 0
    return t

def get_clsfromstr(clsname):
    if clsname.startswith("<class "):
        clsname = clsname.split("<class ")[-1].split()[0][1:-2]

def get_cls(name):
    modname, clsname = name.rsplit(".", 1)
    mod = importlib.import_module(modname)
    return getattr(mod, clsname)

def get_class(clsname):
    if clsname:
        name = clsname.split(".")[-1]
    cls = classes.get(clsname, None)
    if cls:
        return "%s.%s" % clsname, cls

def get_fntype(fn):
    return fn.split(os.sep)[0]

def get_type(obj):
    return obj.__class__.__module__ + "." + obj.__class__.__qualname__

def get_types(name):
    res = []
    for x in os.listdir(cfg.workdir):
        if name is not None:
            if name.lower() == x.split(".")[-1].lower():
                res.append(x)
            elif name.lower() == x.lower():
                res.append(x)
    return res

def now():
    return str(datetime.datetime.now()).split()[0]

def rtime():
    res = str(datetime.datetime.now()).replace(" ", os.sep)
    return res

def sliced(o, keys=None):
    cls = get_cls(get_type(o))
    oo = cls()
    if not keys:
        keys = o.keys()
    for k in keys:
        if k.startswith("_"):
            continue
        try:
            oo[k] = o[k]
        except KeyError:
            pass
    return oo

def smooth(obj):
    if isinstance(obj, Object):
        return vars(obj)
    if type(obj) not in [dict, list, str, int, float, bool, None]:
        return repr(obj)
    return str(obj)
