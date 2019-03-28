import os
from vprint.vprint_level import VPRINT_KEYWORD
from vprint.loggers import get_verbose_logger
from vprint.tests.really_long_name_for_testing_truncation import test_long_name
from vprint import vprint, aprint, spike


def run_tests():
    """
    Run basic tests.

    This is going to be tricky due to the way `vprint` initializes
    Examples:
        >>> vprint('foo') # nothing should happen

        >>> os.environ[VPRINT_KEYWORD] = '1'
        >>> log_vprint_on = get_verbose_logger('vl2')
        >>> vprint = log_vprint_on.debug
        >>> vprint('foo')
        __init__.p~_tests:0>:1> foo
    """
    vprint('should not print unless VPRINTV is set before runtime')
    aprint('always print')
    spike('this is here')

    os.environ[VPRINT_KEYWORD] = '1'
    log_vprint_on = get_verbose_logger('vl2')
    log_vprint_on.debug('verbose set')
    test_long_name()

