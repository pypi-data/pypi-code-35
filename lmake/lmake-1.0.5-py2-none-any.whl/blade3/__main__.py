#!/usr/bin/env python

import os
import sys

sys.path.append(os.path.dirname(__file__))


def main():
    from lmake.blade3 import pconfig
    from lmake.blade3.config import find_build_root

    root = find_build_root()
    if root is None:
        print 'lmake must run under the root dir of the codebase'
        exit(1)
    print 'found lmake root dir:', root

    if len(sys.argv) == 1:
        print >> sys.stderr, "Please specify a package directory"
    pconfig.main(sys.argv)


if __name__ == '__main__':
    main()
