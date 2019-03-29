# bot/rss.py
#
#

""" feed fetcher. """

import re

import bot
import bot.base
import bot.clock
import bot.fleet
import bot.store
import bot.tasks

from bot.base import Dotted, get_type
from bot.kernel import kernel
from bot.tasks import launch
from bot.utils import file_time, get_feed
from bot.utils import strip_html, to_time, unescape

## classes

class Cfg(Dotted):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.display_list = ["title", "link"]
        self.summary = []

class Seen(Dotted):

    def __init__(self):
        super().__init__()
        self.urls = []

class Feed(Dotted):

    pass

class Fetcher(Dotted):

    def __init__(self):
        super().__init__()
        self._thrs = []
        self.cfg = Cfg()

    def display(self, obj):
        result = ""
        if "display_list" in obj:
            dl = obj.display_list
        else:
            dl = self.cfg.display_list
        for key in dl:
            if key == "summary":
                skip = False
                for txt in self.cfg.summary:
                    if txt not in obj.link:
                        skip = True
                if skip:
                    continue
            data = obj.get(key, None)
            if data:
                data = str(data)
                data = data.replace("\n", " ")
                data = strip_html(data.rstrip())
                data = re.sub(r"\s+", " ", data)
                data = unescape(data)
                result += data.rstrip()
            result += " - "
        return result[:-2].rstrip()

    def fetch(self, rssobj):
        counter = 0
        objs = []
        for obj in get_feed(rssobj.rss):
            if not obj:
                continue
            feed = Feed(dict(obj))
            if feed.link in seen.urls:
                continue
            seen.urls.append(feed.link)
            counter += 1
            feed.update(rssobj)
            objs.append(feed)
            if "updated" in feed:
                date = file_time(to_time(feed.updated))
                feed.save(stime=date)
                continue
            elif "published" in feed:
                date = file_time(to_time(feed.published))
                feed.save(stime=date)
                continue
            feed.save()
        seen.save()
        for obj in objs:
            txt = self.display(obj)
            kernel.announce(txt)
        return counter

    def join(self):
        for thr in self._thrs:
            thr.join()

    def run(self):
        for obj in store.all("bot.rss.Rss"):
            self._thrs.append(launch(self.fetch, obj))
        return self._thrs

    def start(self, repeat=True):
        last = store.last(get_type(self))
        if last:
            self.cfg.upgrade(last)
            self.cfg.save()
        last_seen = store.last("bot.rss.Seen")
        if last_seen:
            seen.update(last_seen)
        if repeat:
            repeater = bot.clock.Repeater(600, self.run)
            repeater.start()
            return repeater

    def stop(self):
        seen.save()

## defines

seen = Seen()
store = bot.store.Store()

## functions

def init():
    obj = Fetcher()
    return obj.start()

## commands

class Rss(Dotted):

    def __init__(self):
        super().__init__()
        self.rss = ""

def fetch(event):
    obj = Fetcher()
    obj.start(repeat=False)
    thrs = obj.run()
    res = []
    for thr in thrs:
        res.append(thr.join())
    event.reply("fetched %s" % ",".join([str(x or "0") for x in res]))

def rss(event):
    if not event.rest or "http" not in event.rest:
        event.reply("rss <url>")
        return
    obj = Rss()
    obj.rss = event.rest
    obj.save()
    event.reply("ok 1")
