import logging

from vprint.loggers import get_verbose_logger

verbose_logger = get_verbose_logger('verbose_logger')
always_logger = get_verbose_logger('always_logger', verbose=True)
spike_logger = get_verbose_logger('spike_logger', verbose=True,
                                  fmt='%(asctime)s-%(pathname)s:%(lineno)d> %(message)s')


def vprint(msg, end='', *args, **kwargs):
    # type: (str, str, Any, Any) -> None
    """
    Drop-in replacement for `print`, but provides source file and line number.
    Only prints when env variable KW_VERBOSE > 0
    Bare `print`s are bad! Traceable prints are good!
    :param msg: Message to print
    :param end: Termination string. Not really relevant, since each log prints
    a new line automatically. Provides drop-in compatibility with most prints
    """

    # Just overload it later
    pass


# todo: actually assign this function more elegantly
# todo: custom log functions
# todo: spike should be able to take no argument
vprint = logging.getLogger('verbose_logger').debug
aprint = logging.getLogger('always_logger').debug
spike = logging.getLogger('spike_logger').debug

