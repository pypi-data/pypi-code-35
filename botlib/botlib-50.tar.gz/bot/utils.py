# bot/utils.py
#
#

""" utility functions. """


import html
import html.parser
import importlib
import os
import re
import sys
import time
import traceback
import logging
import urllib
import urllib.error

from bot.base import cfg, fn_time, rtime

from random import randint
from datetime import datetime

import _thread

## defines

exceptions = []

timestrings = [
    "%a, %d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S %z",
    "%d %b %Y %H:%M:%S",
    "%a, %d %b %Y %H:%M:%S",
    "%d %b %a %H:%M:%S %Y %Z",
    "%d %b %a %H:%M:%S %Y %z",
    "%a %d %b %H:%M:%S %Y %z",
    "%a %b %d %H:%M:%S %Y",
    "%d %b %Y %H:%M:%S",
    "%a %b %d %H:%M:%S %Y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dt%H:%M:%S+00:00",
    "%a, %d %b %Y %H:%M:%S +0000",
    "%d %b %Y %H:%M:%S +0000",
]

year_formats = [
    "%b %H:%M",
    "%b %H:%M:%S",
    "%a %H:%M %Y",
    "%a %H:%M",
    "%a %H:%M:%S",
    "%Y-%m-%d",
    "%d-%m-%Y",
    "%d-%m",
    "%m-%d",
    "%Y-%m-%d %H:%M:%S",
    "%d-%m-%Y %H:%M:%S",
    "%d-%m %H:%M:%S",
    "%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M",
    "%d-%m-%Y %H:%M",
    "%d-%m %H:%M",
    "%m-%d %H:%M",
    "%H:%M:%S",
    "%H:%M"
]

## exceptions

class ENODATE(Exception):
    pass

## utility functions

def locked(func):

    lock = _thread.allocate_lock()

    def lockedfunc(*args, **kwargs):
        lock.acquire()
        res = None
        try:
            res = func(*args, **kwargs)
        finally:
            try:
                lock.release()
            except Exception:
                pass
        return res

    return lockedfunc

## functions

def day():
    return str(datetime.today()).split()[0]

def days(obj):
    return elapsed(time.time() - fn_time(obj._container.get("path", 0)))

def elapsed(seconds, short=True):
    txt = ""
    nsec = float(seconds)
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    sec = nsec - minutes*minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    elif sec < 1 or not short:
        txt += "%.3fs" % sec
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt

def fields(main):
    for obj in main.values():
        for key in obj:
            yield key

def file_time(timestamp):
    return str(datetime.fromtimestamp(timestamp)).replace(" ", os.sep) + "." + str(randint(111111, 999999))

@locked
def get_feed(url):
    import feedparser
    if cfg.debug:
        logging.warning("skip %s" % url)
        return
    try:
        result = get_url(url).data
        result = feedparser.parse(result)
    except ValueError:
        logging.warn("not an url %s" % url)
        return
    except urllib.error.HTTPError as ex:
        txt = "%s %s" % (url, ex.msg)
        logging.error(txt)
        return result
    if "entries" in result:
        for entry in result["entries"]:
            yield entry

def get_name(obj):
    try:
        n = "%s.%s" % (obj.__self__.__class__.__name__, obj.__name__)
    except AttributeError:
        try:
            n = "%s.%s" % (obj.__class__.__name__, obj.__name__)
        except AttributeError:
            try:
                n = obj.__class__.__name__
            except AttributeError:
                n = obj.__name__
    return n

def get_url(*args):
    url = urllib.parse.urlunparse(urllib.parse.urlparse(args[0]))
    req = urllib.request.Request(url, headers={"User-Agent": useragent()})
    resp = urllib.request.urlopen(req)
    resp.data = resp.read()
    #print(dir(resp))
    logging.debug("%s get_url %s" % (resp.getcode(), " ".join(args)))
    return resp

def get_exception(txt=""):
    exctype, excvalue, tb = sys.exc_info()
    trace = traceback.extract_tb(tb)
    result = ""
    for elem in trace:
        fname = elem[0]
        linenr = elem[1]
        func = elem[2]
        plugfile = fname[:-3].split(os.sep)
        mod = []
        for elememt in plugfile[::-1]:
            mod.append(elememt)
            if elememt == "bot":
                break
        ownname = '.'.join(mod[::-1])
        result += "%s:%s %s | " % (ownname, linenr, func)
    res = "%s%s: %s %s" % (result, exctype, excvalue, str(txt))
    if res not in exceptions:
        exceptions.append(res)
    del trace
    return res

def get_hour(daystr):
    try:
        hmsre = re.search(r'(\d+):(\d+):(\d+)', str(daystr))
        hours = 60 * 60 * (int(hmsre.group(1)))
        hoursmin = hours  + int(hmsre.group(2)) * 60
        hms = hoursmin + int(hmsre.group(3))
    except AttributeError:
        pass
    except ValueError:
        pass
    try:
        hmre = re.search(r'(\d+):(\d+)', str(daystr))
        hours = 60 * 60 * (int(hmre.group(1)))
        hms = hours + int(hmre.group(2)) * 60
    except AttributeError:
        return 0
    except ValueError:
        return 0
    return hms

def get_time(daystr):
    for f in year_formats:
        try:
            t = time.mktime(time.strptime(daystr, f))
            return t
        except Exception:
            pass

def hd(*args):
    homedir = os.path.abspath(os.path.expanduser("~"))
    return os.path.abspath(os.path.join(homedir, *args))


def matching(keys, value):
    for key in keys:
        if key in value:
            return True
    return False

def now():
    return str(datetime.now()).split()[0]

def strip_html(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def stripped(jid):
    try:
        return str(jid).split("/")[0]
    except (IndexError, ValueError):
        return str(jid)

def today():
    t = rtime().split(".")[0]
    ttime = time.strptime(t, "%Y-%m-%d/%H:%M:%S")
    result = time.mktime(ttime)
    return result

def to_day(daystring):
    line = ""
    daystr = str(daystring)
    for word in daystr.split():
        if "-" in word:
            line += word + " "
        elif ":" in word:
            line += word
    if "-" not in line:
        line = day() + " " + line
    try:
        return get_time(line.strip())
    except ValueError:
        pass

def to_time(daystr):
    daystr = daystr.strip()
    if "," in daystr:
        daystr = " ".join(daystr.split(None)[1:7])
    elif "(" in daystr:
        daystr = " ".join(daystr.split(None)[:-1])
    else:
        try:
            d, h = daystr.split("T")
            h = h[:7]
            daystr = " ".join([d, h])
        except (ValueError, IndexError):
            pass
    res = 0
    for tstring in timestrings:
        try:
            res = time.mktime(time.strptime(daystr, tstring))
        except ValueError:
            try:
                res = time.mktime(time.strptime(" ".join(daystr.split()[:-1]), tstring))
            except ValueError:
                pass
        if res:
            break
    if not res:
        raise ENODATE(daystr)
    return res

def useragent():
    return 'Mozilla/5.0 (X11; Linux x86_64) BOTLIB +https://bitbucket.org/bthate/bot)'

def unescape(text):
    txt = re.sub(r"\s+", " ", text)
    return html.parser.HTMLParser().unescape(txt)
