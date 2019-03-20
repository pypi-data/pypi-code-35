#!/usr/local/bin/python3.7
import sys
import os
import curses
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from rover_position_rjg.clients.monitor.monitor import Shell


def main(stdscr: any):
    shell = Shell(stdscr)
    shell.run(stdscr)


if __name__ == '__main__':
    curses.wrapper(main)
