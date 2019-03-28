#!/usr/bin/env python
# encoding: utf-8


import cli_print as cp


def raw(s: str = ''):
    """
    Get input, if empty retry.

    :param str s: prompt
    :return: str
    """
    while True:
        value = input('> {}: '.format(s))
        if value:
            return value


def confirm(s: str = ''):
    """
    Ask yes/no, if invalid retry.

    :param str s: prompt
    :return: bool
    """
    while True:
        value = input('> {} [y/n]: '.format(s)).lower()
        if value:
            if value in 'yesrtui':
                return True
            elif value in 'novbm,':
                return False


def pause(s: str = 'press any key to continue'):
    """
    Pause with a prompt.

    :param str s: prompt
    :return: None
    """
    _ = input('# {}: '.format(s))
    return


def copy(value: str, force: bool = False, key: str = None):
    """
    Copy to clip.

    :param str value: value to be copied
    :param bool force: without a prompt pause
    :param str key: tip
    :return: None
    """
    import cli_print as cp
    import pyperclip

    if not force:
        if key:
            pause('Press any key to copy {} '.format(key)
                  + cp.Fore.LIGHTCYAN_EX + str(value)
                  + cp.Style.RESET_ALL + ' to clip')
        else:
            pause('Press any key to copy '
                  + cp.Fore.LIGHTCYAN_EX + str(value)
                  + cp.Style.RESET_ALL + ' to clip')

        cp.wr('\x1b[1A\x1b[2K')  # remove the prompt line.
        cp.fi()
    if key:
        cp.about_t('Copy {}'.format(key), value, 'to clip')
    else:
        cp.about_t('Copy', value, 'to clip')
    pyperclip.copy(value)
    cp.success()
    return


def _print_sleep(i: int, t: int):
    """
    Function for `sleep`.

    :param int i: current
    :param int t: amount
    :return: None
    """
    if t < 90:
        cp.wr(cp.Fore.LIGHTBLUE_EX + ' - [' + '>' * i + '-' * (t - i) + '] sleep {}/{} s\r'.format(i, t))
        cp.fx()
    else:
        cp.wr(cp.Fore.LIGHTBLUE_EX + ' - sleep {}/{} s\r'.format(i, t))
        cp.fx()
    return


def sleep(t: int = None, b: int = None):
    """
    Sleep for a while.

    :param int t: Min seconds
    :param int b: Max seconds
    :return:
    """
    import time
    import random

    if t and b:
        t = random.randint(t, b)
    elif t is None:
        t = random.randint(10, 60)

    _print_sleep(0, t)

    for i in range(1, t + 1):
        time.sleep(1)
        cp.previous_line(True)
        _print_sleep(i, t)

    return t
