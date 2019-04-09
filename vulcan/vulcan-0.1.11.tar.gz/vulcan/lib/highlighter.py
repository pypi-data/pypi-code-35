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

import re
import json
from base64 import b64decode, b64encode
from textwrap import dedent

from pygments import highlight as pyhighlight
from pygments.formatter import Formatter
from pygments.lexers import PythonLexer

class URWIDFormatter(Formatter):

    def __init__(self, **options):
        Formatter.__init__(self, **options)

        # create a dict of (start, end) tuples that wrap the
        # value of a token so that we can use it in the format
        # method later
        self.styles = {}

        # we iterate over the `_styles` attribute of a style item
        # that contains the parsed style values.
        for token, style in self.style:
            start = end = ''
            # a style item is a tuple in the following form:
            # colors are readily specified in hex: 'RRGGBB'
            if style['color']:
                start += '["%s", "'%self.urwid_cols(style['color'])
                end = '"],' + end
            else:
                start += '["", "'
                end = '"],' + end
            self.styles[token] = (start, end)

    def urwid_cols(self, col):
        urwid_cols = {
            '008000': 'dark blue',
            '888888': 'grey',
            'BA2121': 'dark green',
            '0044DD': 'dark green',
            '666666': 'dark green',
            '408080': 'grey'
        }

        if col in urwid_cols:
            return urwid_cols[col]

        return 'grey'

    def format(self, tokensource, outfile):
        # lastval is a string we use for caching
        # because it's possible that an lexer yields a number
        # of consecutive tokens with the same token type.
        # to minimize the size of the generated html markup we
        # try to join the values of same-type tokens here
        lastval = ''
        lasttype = None

        for ttype, value in tokensource:
            # if the token type doesn't exist in the stylemap
            # we try it with the parent of the token type
            # eg: parent of Token.Literal.String.Double is
            # Token.Literal.String
            while ttype not in self.styles:
                ttype = ttype.parent
            if ttype == lasttype:
                # the current token type is the same of the last
                # iteration. cache it
                lastval += value
            else:
                # not the same token as last iteration, but we
                # have some data in the buffer. wrap it with the
                # defined style and write it to the output file
                if lastval:
                    stylebegin, styleend = self.styles[lasttype]
                    lastval = b64encode(str.encode(lastval)).decode('utf-8')
                    outfile.write(stylebegin + lastval + styleend)
                # set lastval/lasttype to current values
                lastval = value
                lasttype = ttype

        # if something is left in the buffer, write it to the
        # output file, then close the opened <pre> tag
        if lastval:
            stylebegin, styleend = self.styles[lasttype]
            lastval = b64encode(str.encode(lastval)).decode('utf-8')
            outfile.write(stylebegin + lastval + styleend)

class PyGToURWID:

    def __init__(self, code):
        self.code = code
        self.py_highlighted = pyhighlight(code, PythonLexer(), URWIDFormatter())
        r = "["+self.py_highlighted[:-1]+"]"
        j = json.loads(r)
        for i, it in enumerate(j):
            if type(it) is list:
                j[i] = (it[0], b64decode(it[1]).decode('utf-8'))
            else:
                j[i] = b64decode(j[i]).decode('utf-8')

        self.final = j

def highlight(code):
    pygt = PyGToURWID(code)
    return pygt.final

if __name__ == "__main__":

    from urwid import *
    palette = [
        ('dark blue', 'dark blue', '', 'standout'),
        ('dark green', 'dark green', '', 'standout'),
        ('grey', 'light gray', '', 'standout'),
        ('brown', 'brown', '', 'standout'),
    ]

    code = """
    class PyGToURWID:

        def __init__(self, code):
            self.code = code
            self.py_highlighted = highlight(code, PythonLexer(), OldHtmlFormatter())
            r = "["+self.py_highlighted[:-1]+"]"
            j = json.loads(r)
            for i, it in enumerate(j):
                if type(it) is list:
                    j[i] = (it[0], b64decode(it[1]).decode('utf-8'))
                else:
                    j[i] = b64decode(j[i]).decode('utf-8')

            print(j)

            self.final = j
    """
    pygt = PyGToURWID(code)

    loop = MainLoop(Filler(Text(pygt.final), 'top'), palette=palette)
    loop.run()



