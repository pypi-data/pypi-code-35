# -*- coding: utf-8 -*-

# Copyright (C) 2019 github.com/shyal
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

import os
import shelve

prefs_path = os.path.expanduser("~/.vulcan/prefs")

def init_prefs():
    dirname = os.path.dirname(prefs_path)
    if dirname and not os.path.isdir(dirname):
      os.makedirs(dirname)
    return shelve.open(prefs_path)

# prefs are useful, to remember which tag was last selected, for example
prefs = init_prefs()

def reset_prefs():
    if os.path.exists(prefs_path):
        os.unlink(prefs_path)
        global prefs
        prefs = init_prefs()

