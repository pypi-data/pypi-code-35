# Copyright 2018, 2019 Felix Krull
# Licensed under the MIT license, see LICENSE for details.

import sys


def get_root_fs() -> str:
    with open('/proc/cmdline', 'r', encoding=sys.getfilesystemencoding()) as f:
        args = f.read()  # type: str
    for arg in (arg.strip() for arg in args.split()):
        if arg.startswith('root='):
            return arg[5:]
    return ''
