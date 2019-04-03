"""Logging helpers to capture and setup logging."""
import io
import contextlib
from typing import Optional
import logging


LOG_FORMAT = '%(asctime)s %(levelname)s %(filename)s: %(message)s'


def capture_output(
    target: object,
    args: Optional[tuple] = None,
        kwargs: Optional[dict] = None) -> str:
    """Redirect stdout and stderr into string buffer and capture it.

    target object is executed with optional args, kwargs and all stdout/
    stderr that is captured, returned in string form.

    Args:
        target: object to execute, usually a function.
        args: target positional arguments (default: {None})
        kwargs: target keyword arguments (default: {None})
    """
    if not args:
        args = ()
    if not kwargs:
        kwargs = {}

    with io.StringIO() as sio:
        with contextlib.redirect_stdout(sio), contextlib.redirect_stderr(sio):
            target(*args, **kwargs)
            output = sio.getvalue()
            return output


def setup_logger(
        log_level: str = logging.WARNING, fmt: str = LOG_FORMAT) -> None:
    """Set up basic logging configuration."""
    logging.basicConfig(
        format=LOG_FORMAT,
        level=log_level)
