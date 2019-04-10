#!/usr/bin/env python3
# coding: utf-8

from __future__ import division, print_function

import os
import time


def _iter_lines(path, *args, **kwargs):
    with open(path, *args, **kwargs) as fin:
        for line in fin:
            yield line


def _iter_stdin_lines():
    import sys
    for line in sys.stdin:
        yield line


def iter_lines(path, *args, **kwargs):
    if not path or path == '-':
        return _iter_stdin_lines()
    else:
        return _iter_lines(path, *args, **kwargs)


def nonblank_lines_of(path, *args, **kwargs):
    for line in iter_lines(path, *args, **kwargs):
        line = line.strip()
        if not line:
            continue
        yield line


class AtomicTailer(object):
    """
    Read log file on-line
    inspired by https://github.com/six8/pytailer

    a minimized version with this issue fixed:
        https://github.com/six8/pytailer/issues/9
    """

    def __init__(self, file, read_size=1024, interval=1.,
                 linesep=None, timeout=60):

        if isinstance(file, str):
            self.file = open(file)
        else:
            self.file = file

        self.read_size = read_size
        self.start_pos = self.file.tell()
        self.interval = interval
        self.linesep = linesep or os.linesep
        self.timeout = timeout

    def __iter__(self):
        return self.follow()

    def follow(self):
        """\
        follow a growing file

        tldr: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/157035
        """
        tm = time.time()
        while True:
            pos = self.file.tell()
            line = self.file.readline()
            if line.endswith(self.linesep):
                tm = time.time()
                yield line
            else:
                if time.time() - tm > self.timeout:
                    if line:
                        yield line
                    break
                self.file.seek(pos)
                time.sleep(self.interval)

    def follow_lines(self, limit=1000):
        tm = time.time()
        lines = []
        while True:
            if len(lines) >= limit:
                yield lines
                lines = []
            pos = self.file.tell()
            line = self.file.readline()
            if line.endswith(self.linesep):
                tm = time.time()
                lines.append(line)
            else:
                if time.time() - tm > self.timeout:
                    if line:
                        lines.append(line)
                    if lines:
                        yield lines
                    break
                self.file.seek(pos)
                time.sleep(self.interval)
