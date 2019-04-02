#!/usr/bin/python
# -*- coding: utf-8 -*-

__author__ = "Robin 'r0w' Weiland"
__credits__ = ["Robin Weiland", ]
__copyright__ = "Copyright 2019, Robin Weiland"

__date__ = "2019-04-01"
__version__ = "0.1.0"
__license__ = "MIT"

__status__ = "In Development"
__maintainer__ = "Robin Weiland"

__all__ = ['lmgc']

# imports:
from warnings import warn
from platform import system
from time import sleep
# 'from winsound import Beep' on line 43, since it is platform specific


__doc__ = """
This module provides functionality to catch errors and notify you if
something goes wrong, so if you do something heavily time consuming,
like training neural networks, searching primes, etc., you can walk
away and still know if an error occurs.

usage:
    from letmegetcoffee import lmgc

    # specify the type of exception you want to catch
    lmgc.EXCEPTIONS = IndexError  # or any other error(s); defaults to (Exception,)

    # specify the function to call after an exception
    lmgc.ON_EXCEPTION = lmgc.on_exception_beep  # starts to beep on exception

while 'lmgc.EXCEPTIONS' isn't really necessary to specify, 'lmgc.ON_EXCEPTION'
is really important to specify after import because it will default to 'print'
otherwise and just print out the exception-object.

At the moment the module only supports beeping on errors, but others like
email should come in the future.

    @lmgc.catch
    def someFunction(arg):
        ...
"""


class lmgc:  # lowercase class, horrible I know, but it seems to fit here
    __doc__ = __doc__

    EXCEPTIONS = (Exception,)
    ON_EXCEPTION = print

    @staticmethod
    def catch(func):
        """
        decorator for the function that should be monitored
        like this:

        @lmgc.catch
        def someFunction(arg):
            ...

        :param func: the function; gets handled by the decorator
        :return: the wrapper; also part of the decorator
        """
        if lmgc.ON_EXCEPTION == print: warn('lmgc.ON_EXCEPTION is not specified; defaults to print')

        def wrapper(*args, **kwargs):
            try: func(*args, **kwargs)
            except lmgc.EXCEPTIONS as e: lmgc.ON_EXCEPTION(e)
        return wrapper

    @staticmethod
    def on_exception_beep(e):
        """
        beep when an error occurred, not to be called by the user, only set onto lmgc.ON_EXCEPTION
        REMEBER to turn your volume up
        :param e: Exception(child) object; passed by lmgc.catch
        :return: None
        """
        name = e.__class__.__name__
        line = e.__traceback__.tb_lineno
        file = e.__traceback__.tb_frame.f_code.co_filename
        print('{} at line {} in file \'{}\''.format(name, line, file))
        if system() == 'Windows':
            from winsound import Beep
            while True:
                Beep(1000, 1000)
                sleep(0.5)
        elif system() in ('Linux', 'Darwin',):
            while True:
                print('\a', sep='')
                sleep(0.5)


if __name__ == '__main__': pass
