#!/usr/bin/env python3

import sys
import time

try:
    import tkinter
    native = False          # do not use Linux native programs
except Exception:
    import subprocess
    native = True           # use Linux native


def screen_dimensions(width=True, height=False):
    """
    Summary.

        Uses TKinter module in the standard library to find screen dimensions

    Args:
        :width (bool):  If True, return screen width in columns (DEFAULT)
        :height (bool): If True, return screen height in rows

    Returns:
        Screen width, height, TYPE: int

    """
    if native:
        cols = subprocess.getoutput('tput cols')
        rows = subprocess.getoutput('tput lines')
    else:
        root = tkinter.Tk()
        cols = root.winfo_screenwidth()
        rows = root.winfo_screenheight()

    if height:
        return int(rows)
    elif width and height:
        return int(cols), int(rows)
    return int(cols)


def progress_meter(delay=0.1, pattern='.', width=None):
    """
    Summary.

        Graphical progress meter

    Args:
        :pattern (str): Character to print in pattern
        :width (int): Width of pattern to print (columns)
        :delay (int): Delay between prints (seconds)

    Returns:
        stdout pattern

    """
    if width is None:
        stop = int(screen_dimensions() / 3)
    else:
        stop = int(width)

    for i in range(0, stop + 1):

        if i == 0:
            sys.stdout.write('\t%s' % pattern)
            time.sleep(delay)

        elif i > stop:
            sys.stdout.write('\n')
            i = 0

        else:
            sys.stdout.write('%s' % pattern)
            time.sleep(delay)
