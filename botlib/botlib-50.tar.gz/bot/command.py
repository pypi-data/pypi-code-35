# bot/command.py
#
#

""" list of tokens parsed into a command. """

import bot.base
import threading

from bot.utils import get_time, to_day

## classes

defaults = bot.base.Dotted()
defaults.cfg = "server"
defaults.email = "From"
defaults.feed = "title"
defaults.log = "txt"
defaults.rss = "rss"
defaults.todo = "txt"
defaults.user = "user"

args = bot.base.Dotted()
args["bot.kernel.Cfg"] = "server"
args["bot.email.Email"] = "From"
args["bot.rss.Feed"] = "title"
args["bot.entry.Log"] = "txt"
args["bot.rss.Rss"] = "rss"
args["bot.entry.Todo"] = "txt"
args["bot.user.User"] = "user"

types = bot.base.Dotted()
types.cfg = "bot.kernel.Cfg"
types.email = "bot.email.Email"
types.feed = "bot.rss.Feed"
types.log = "bot.log.Log"
types.rss = "bot.rss.Rss"
types.todo = "bot.todo.Todo"
types.user = "bot.user.User"

class Token(bot.base.Dotted):

    """ transfer a word to a token (word with meta data). """
    
    def __init__(self, word):
        super().__init__()
        self.arg = ""
        self.dkey = ""
        self.down = None
        self.equal = ""
        self.ignore = ""
        self.index = None
        self.options = []
        self.selector = ""
        self.setter = ""
        self.up = None
        self.value = ""
        self.word = word
        self.parse()

    def parse(self):
        if "http" in self.word:
            self.value = self.word
            self.arg = self.word
            return
        try:
            v = int(self.word)
            if v >= 0:
                self.index = v 
                return
        except:
            pass
        if self.word.startswith("-"):
            try:
                self.down = int(self.word)
                return
            except ValueError:
                pass
        if self.word.startswith("+"):
            try:
                self.up = int(self.word[1:])
                return
            except ValueError:
                pass
        if self.word.endswith("-"):
            self.ignore = self.word[:-1]
            self.word = self.ignore
        if "==" in self.word:
            self.selector, self.value = self.word.split("==")
            self.dkey = self.selector
        elif "=" in self.word:
            self.setter, self.value = self.word.split("=")
            self.dkey = self.setter
        else:
            self.arg = self.word
            self.value = self.word

class Command(bot.base.Dotted):

    """ List of tokens. """
    
    def __init__(self, txt):
        super().__init__()
        self.args = []
        self.cmd = ""
        self.delta = 0
        self.dkeys = []
        self.ignore = ""
        self.index = None
        self.options = [x for x in bot.base.cfg.options.split(",") if x]
        self.rest = ""
        self.selector = bot.base.Dotted()
        self.setter = bot.base.Dotted()
        self.tokens = []
        self.txt = txt
        self.parse()

    def parse(self):
        nr = -1
        self.args = []
        self.dkeys = []
        self.options = []
        self.tokens = []
        if not self.txt:
            return
        for word in self.txt.split():
            nr += 1
            if nr == 0:
                if word.startswith("!"):
                    word = word[1:]
                self.cmd = word
                continue
            if nr == 1:
                self.type = types.get(word, word)
            self.tokens.append(Token(word))
        nr = -1
        prev = ""
        for token in self.tokens:
             nr += 1
             if prev == "-o":
                 self.options.extend(token.value.split(","))
             if prev == "-i":
                 try:
                     self.index = int(token.value)
                 except ValueError:
                     pass
             #if token.options:
             #    self.options.extend(token.options)
             if token.arg:
                 self.args.append(token.arg)
             if token.ignore:
                 self.ignore = token.ignore
             elif token.dkey:
                 self.dkeys.append(token.dkey)
             elif token.arg:
                 self.dkeys.append(token.arg)
             if token.selector:
                 self.selector[token.selector] = token.value
             if token.setter:
                 self.setter[token.setter] = token.value
             if token.index is not None:
                 self.index = token.index
             if token.up:
                 self.delta = parse_date(token.up)
             if token.down:
                 self.delta = parse_data(token.down)
             prev = token.value
        self.rest = " ".join(self.args)
        self.time = to_day(self.rest)

    def ready(self):
        return self._ready.set()
        
    def wait(self):
        return self._ready.wait()

## funcions

def parse_date(daystr):
    sec = 0
    min = 0
    hour = 0
    day = 0
    w = 0
    diff = 0
    prev = ""
    val = 0
    total = 0
    for c in daystr:
        if c not in ["s", "m", "h", "d", "w", "y"]:
            val += c
            continue
        if c == "y":
            total += val * 3600*24*365
        if c == "w":
            total += val * 3600*24*7
        elif c == "d":
            total += val * 3600*24
        elif c == "h":
            total += val * 3600
        elif c == "m":
            total += val * 60
        else:
            total += val
        val = 0
    return total        
        