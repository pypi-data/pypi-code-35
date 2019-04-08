# -*- coding: utf-8 -*-

# Copyright (C) 2017 github.com/shyal
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import getpass
import highlighter as hi

class CardContext(object):

    def __init__(self, card, command, banner, prompt):
        self.card = card
        self.preamble = hi.highlight(card.preamble)
        # need to fix highlighter...
        if not self.preamble:
            self.preamble = card.preamble
        self.__command = command
        self.banner = banner
        self.__prompt = prompt
        return

    @property
    def prompt(self):
        if isinstance(self.__prompt, str):
            return [self.__prompt]
        elif isinstance(self.__prompt, list):
            return self.__prompt

    @property
    def command(self):
        if isinstance(self.__command, str):
            if self.__command:
                return [self.__command]
            return []
        elif isinstance(self.__command, list):
            return self.__command

    def render(self):
        pre = []
        if self.banner:
            pre.append(self.banner)
            pre.append("\n")
        pre.extend(self.prompt)
        pre.extend(self.preamble[:])
        for i, t in enumerate(pre):
            if isinstance(t, tuple):
                if t[1] == '\n':
                    pre[i] = ('', '\n'+self.__prompt)
        pre.append("\n")
        pre.extend(self.prompt)
        pre.append("\n")
        pre.extend(self.prompt)
        pre.append(('dark blue', "# "))
        pre.append(('dark blue', self.card.question))
        return pre

class PythonCardContext(CardContext):

    def __init__(self, *args, **kwargs):
        command = "python"
        banner = """Python 2.7.10 (default, Jul 14 2015, 19:46:27)
[GCC 4.2.1 Compatible Apple LLVM 6.0 (clang-600.0.39)] on darwin
Type "help", "copyright", "credits" or "license" for more information."""
        prompt = ">>> "
        super(PythonCardContext, self).__init__(command=command, banner=banner, prompt=prompt, *args, **kwargs)

class SQLite3CardContext(CardContext):

    def __init__(self, *args, **kwargs):
        command = "sqlite3"
        banner = """SQLite version 3.8.7.4 2014-12-09 01:34:36
Enter ".help" for usage hints.
Connected to a transient in-memory database.
Use ".open FILENAME" to reopen on a persistent database."""
        prompt = "sqlite> "
        super(SQLite3CardContext, self).__init__(command=command, banner=banner, prompt=prompt, *args, **kwargs)

class NodeCardContext(CardContext):

    def __init__(self, *args, **kwargs):
        command = "node"
        prompt = "> "
        super(NodeCardContext, self).__init__(command=command, banner='', prompt=prompt, *args, **kwargs)

class RubyCardContext(CardContext):

    def __init__(self, *args, **kwargs):
        command = "ruby"
        banner = """ruby 2.0.0p481 (2014-05-08 revision 45883) [universal.x86_64-darwin14]"""
        prompt = ""
        super(RubyCardContext, self).__init__(command=command, banner=banner, prompt=prompt, *args, **kwargs)

class SQLCardContext(CardContext):

    def __init__(self, *args, **kwargs):
        command = "mysql"
        banner = """Welcome to the MariaDB monitor.  Commands end with ; or \\g.
Your MariaDB connection id is 5
Server version: 10.1.23-MariaDB Homebrew

Copyright (c) 2000, 2017, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\\h' for help. Type '\\c' to clear the current input statement."""
        prompt = "MariaDB [(none)]> "
        super(SQLCardContext, self).__init__(command=command, banner=banner, prompt=prompt, *args, **kwargs)

def bash_prompt():
    return [("dark blue", getpass.getuser()), "@", ("dark green", "vulcan"), ":",("dark blue", "~ ")]

class BashCardContext(CardContext):

    def __init__(self, *args, **kwargs):
        super(BashCardContext, self).__init__(command='', banner='', prompt=bash_prompt(), *args, **kwargs)

    def render(self):
        pre = []
        pre.append("\n")
        pre.extend(self.preamble[:])
        pre.append("\n")
        pre.append("\n")
        return pre + bash_prompt() + ["# " + self.card.question]

def prompt(card):
    if card.context == "python":
        return PythonCardContext(card)
    if card.context == "sqlite3":
        return SQLite3CardContext(card)
    if card.context in ['node', 'nodejs', 'react', 'redux']:
        return NodeCardContext(card)
    elif card.context == "sql":
        return SQLCardContext(card)
    elif card.context == "ruby":
        return RubyCardContext(card)
    return BashCardContext(card)
