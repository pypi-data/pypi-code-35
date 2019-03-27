"""Contains functions to configure log output.
"""

import logging
import logging.config
import logging.handlers


_DATE_FMT = "%Y-%m-%d/%H:%M:%S"


def auto(debug=False, thread=False, datetime=True, level=True,
         syslog_tag=None, syslog_address="/dev/log",
         file_name=None, file_when="midnight", file_backup_count=7):
    """Configure handler from input arguments.

    If syslog_tag passed, configure Syslog handler. Else if file_name passed, configure
    TimedRotatingFileHandler handler. Else create Stdout handler.

    Full output format: 2019-03-22/10:17:28 MainThread INFO    info message

    Args:
        debug (bool): show log messages with debug level?
        thread (bool): add thread name to log messages?
        datetime (bool): add datetime to log messages?
        level (bool): add level name to log messages?

        syslog_tag (str): syslog tag
        syslog_address (str or tuple): address of syslog server

        file_name (str): path to the log file
        file_when (str): type of rotating interval
        file_backup_count (int): keep last N files

    More information: https://docs.python.org/2.7/library/logging.handlers.html
    """

    if syslog_tag and file_name:
        raise ValueError("both syslog_tag and file_name are present")

    fmt = choose_format(datetime=datetime, thread=thread, level=level)
    lvl = logging.DEBUG if debug else logging.INFO

    logger = logging.getLogger()

    # if we get syslog_tag, use SysLogHandler
    if syslog_tag:
        # always disable datetime for syslog messages
        fmt = syslog_tag + ": " + choose_format(datetime=False, thread=thread, level=level)
        handler = logging.handlers.SysLogHandler(address=syslog_address)
        formatter = logging.Formatter(fmt=fmt, datefmt=_DATE_FMT)

    # if we get file_name, use TimedRotatingFileHandler
    elif file_name:
        handler = logging.handlers.TimedRotatingFileHandler(
            filename=file_name, interval=1, when=file_when, backupCount=file_backup_count
        )
        formatter = logging.Formatter(fmt=fmt, datefmt=_DATE_FMT)

    # otherwise, use StreamHandler
    else:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(fmt=fmt, datefmt=_DATE_FMT)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(lvl)


def choose_format(datetime=True, thread=True, level=True):
    fmt = "%(message)s"
    if level:
        fmt = "%(levelname)-7s " + fmt
    if thread:
        fmt = "%(threadName)-10s " + fmt
    if datetime:
        fmt = "%(asctime)s " + fmt

    return fmt
