# Copyright (c) 2018 DDN. All rights reserved.
# Use of this source code is governed by a MIT-style
# license that can be found in the LICENSE file.

import sys
from subprocess import call
from itertools import chain, imap


def flat_map(fn, xs):
    return chain.from_iterable(imap(fn, xs))


def main():
    args = sys.argv[1:]

    code = call(["sosreport"] + args + ["--batch", "--log-size=0"])

    sys.exit(code)

def chroma_diagnostics():
    print "chroma-diagnostics no longer exists. Please use 'iml-diagnostics' instead."
