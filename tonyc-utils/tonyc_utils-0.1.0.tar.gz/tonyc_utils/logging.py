import logging
import os
import sys

LOG_LEVEL_DEFAULT=3
LOG_LEVELS = [
    "critical",
    "error",
    "warning",
    "info",
    "debug",
    "trace"
]

DEFAULT_FORMAT="%(asctime)s [%(module)16s:%(lineno)-4d] [%(levelname)8s] %(message)s"

log_level = None
stdout_handler = None
logger = None
formatter = None

def set_stdout_level(level=log_level):
    global stdout_handler
    assert(stdout_handler)

    try:
        handler = next(h for h in logger.handlers if h.stream == sys.stdout)
    except StopIteration:
        return

    handler.setLevel(level)

def add_log_handler(handler):
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def setup_logging(level=0, handlers=[], log_format=DEFAULT_FORMAT, quiet_stdout=False):

    global logger
    global log_level
    global stdout_handler
    global formatter

    log_level = LOG_LEVEL_DEFAULT + level
    if log_level < 0 or log_level >= len(LOG_LEVELS):
        raise Exception("bad log level: %d" %(log_level))
    # add "trace" log level
    TRACE_LEVEL_NUM = 9
    logging.addLevelName(TRACE_LEVEL_NUM, "TRACE")
    logging.TRACE = TRACE_LEVEL_NUM
    def trace(self, message, *args, **kws):
        if self.isEnabledFor(TRACE_LEVEL_NUM):
            self._log(TRACE_LEVEL_NUM, message, args, **kws)
    logging.Logger.trace = trace

    if isinstance(level, str):
        log_level = getattr(logging, log_level.upper())
    else:
        log_level = getattr(logging, LOG_LEVELS[log_level].upper())

    if not isinstance(handlers, list):
        handlers = [handlers]

    logger = logging.getLogger()
    formatter = logging.Formatter(
        log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger.setLevel(log_level)
    stdout_handler = logging.StreamHandler(sys.stdout)
    set_stdout_level(logging.CRITICAL if quiet_stdout else log_level)

    handlers.insert(0, stdout_handler)
    # if not handlers:
    #     handlers = [logging.StreamHandler(sys.stdout)]
    for handler in handlers:
        add_log_handler(handler)

    # logger = logging.basicConfig(
    #     level=level,
    #     format="%(asctime)s [%(module)16s:%(lineno)-4d] [%(levelname)8s] %(message)s",
    #     datefmt="%Y-%m-%d %H:%M:%S"
    # )

    # FIXME: move this elsewhere
    logging.getLogger("requests").setLevel(log_level+1)
    logging.getLogger("urllib3").setLevel(log_level+1)
    return logger

__all__ = [
    "setup_logging",
    "set_stdout_level",
    "add_log_handler"
]
