import colorlog
import os
import sys
import json
import subprocess

import colorama
from colorama import Fore, Style

__all__ = ['configure_logger', 'get_variable', 'required', 'enable_debug', 'success', 'fail']


def configure_logger():
    """Configure logger to produce colorized output."""

    # Colorlog initialises colorama, however we need to reinit() it to not strip ANSI codes when
    # no tty is attached (i.e inside a docker run in pipes).
    colorama.deinit()
    colorama.init(strip=False)

    # Initialises logging.
    handler = colorlog.StreamHandler()
    handler.setFormatter(colorlog.ColoredFormatter(
        '%(log_color)s%(levelname)s: %(message)s'))
    logger = colorlog.getLogger('root')
    logger.addHandler(handler)
    logger.setLevel('INFO')
    return logger


def get_variable(name, required=False, default=None):
    """Fetch the value of a pipe variable.

    Args:
        name (str): Variable name.
        required (bool, optional): Throw an exception if the env var is unset.
        default (:obj:`str`, optional): Default value if the env var is unset.

    Returns:
        Value of the variable

    Raises
        Exception: If a required variable is missing.
    """
    value = os.getenv(name)
    if required and (value == None or not value.strip()):
        raise Exception('{} variable missing.'.format(name))
    return value if value else default


def required(name):
    """Get the value of a required pipe variable.

    This function is basically an alias to get_variable with the required 
        parameter set to True.

    Args:
        name (str): Variable name.

    Returns:
        Value of the variable

    Raises
        Exception: If a required variable is missing.
    """
    return get_variable(name, required=True)


def enable_debug():
    """Enable the debug log level."""

    debug = get_variable('DEBUG', required=False, default="False").lower()
    if debug == 'true':
        logger = colorlog.getLogger('root')
        logger.info('Enabling debug mode.')
        logger.setLevel('DEBUG')


def success(message='Success', do_exit=True):
    """Prints the colorized success message (in green)

    Args:
        message (str, optional): Output message
        do_exit (bool, optional): Call sys.exit if set to True

    """
    print('{}✔ {}{}'.format(Fore.GREEN, message, Style.RESET_ALL))

    if do_exit:
        sys.exit(0)


def fail(message='Fail!', do_exit=True):
    """Prints the colorized failure message (in red)

    Args:
        message (str, optional): Output message
        do_exit (bool, optional): Call sys.exit if set to True

    """
    print('{}✖ {}{}'.format(Fore.RED, message, Style.RESET_ALL))

    if do_exit:
        sys.exit(1)
