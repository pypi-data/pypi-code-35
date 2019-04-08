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

def hilight_between(code, sep, attr):
    hl = []
    if isinstance(code, list):
        for c in code:
            hl.extend(hilight_between(code=c, sep=sep, attr=attr))
    elif isinstance(code, str):
        r = '{0}([^\{0}]+){0}'.format(sep)
        if re.search(r, code):
            m = re.search(r, code)
            tokens = code.split(sep+m.group(1)+sep)
            l = len(tokens)
            for i, t in enumerate(tokens):
                hl.extend(hilight_between(code=t, sep=sep, attr=attr))
                if i < l-1:
                    hl.append((attr, sep+m.group(1)+sep))
        else:
            return [code]
    elif isinstance(code, tuple):
        return [code]
    return hl


def hilight(code, token, attr):
    hl = []
    if isinstance(code, list):
        for c in code:
            hl.extend(hilight(code=c, token=token, attr=attr))
    elif (isinstance(code, str)) and code:
        r = '({0})'.format(token)
        m = re.search(r, code)
        if m:
            tokens = code.split(m.group(1))
            l = len(tokens)
            for i, t in enumerate(tokens):
                hl.extend(hilight(code=t, token=token, attr=attr))
                if i < l-1:
                    hl.append((attr, m.group(1)))
        else:
            return [code]
    elif isinstance(code, tuple):
        return [code]
    return hl

def highlight(code):
    txt = hilight_between(code=code, sep='"', attr='dark blue')
    txt = hilight_between(code=txt, sep="'", attr='dark blue')
    txt = hilight(code=txt, token='import|from|print|try|except|def|return', attr='dark green')
    txt = hilight(code=txt, token='=|\+', attr='brown')
    txt = hilight(code=txt, token='\n', attr='')
    return txt

if __name__ == "__main__":
    from urwid import *
    palette = [
        ('dark blue', 'dark blue', '', 'standout'),
        ('dark green', 'dark green', '', 'standout'),
        ('brown', 'brown', '', 'standout'),
    ]

    txt = highlight('from f import foo\nprint("hello")\nprint("world")\nhello = 1\nprint(\'foo\')')
    print(txt)
    loop = MainLoop(Filler(Text(txt), 'top'), palette=palette)
    loop.run()



