"""Contains functions to configure log output.
"""

import logging
import logging.config
import logging.handlers


_DATE_FMT = "%Y-%m-%d/%H:%M:%S"


def auto(debug=False, thread=False, datetime=True,
         syslog_tag=None, syslog_address="/dev/log",
         file_name=None, file_when="midnight", file_backup_count=7):
    """Configure handler from input arguments.

    If syslog_tag passed, configure Syslog handler. Else if file_name passed, configure
    TimedRotatingFileHandler handler. Else create Stdout handler.

    Full output format: 2019-03-22/10:17:28 MainThread INFO    info message

    More information: https://docs.python.org/2.7/library/logging.handlers.html
    """

    if syslog_tag and file_name:
        raise ValueError("both syslog_tag and file_name are present")

    fmt = choose_format(datetime=datetime, thread=thread)
    lvl = logging.DEBUG if debug else logging.INFO

    logger = logging.getLogger()

    # if we get syslog_tag, use SysLogHandler
    if syslog_tag:
        # always disable datetime for syslog messages
        fmt = syslog_tag + ": " + choose_format(datetime=False, thread=thread)
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


def choose_format(datetime=True, thread=True):
    fmt = "%(levelname)-7s %(message)s"
    if thread:
        fmt = "%(threadName)-10s " + fmt
    if datetime:
        fmt = "%(asctime)s " + fmt

    return fmt
