import time
import logging
from typing import Optional


class _TimeIt(object):
    """Decorator  class to track function execution time.

    This decorator should probably be used as convenience. If you need
    to benchmark your code, you should probably use standard module
    timeit.
    """

    _time_map = {
        'ms': ('millisecond(s)', 1000),
        's': ('second(s)', 1),
        'm': ('minute(s)', 1/60),
        'h': ('hour(s)', 1/3600),
    }

    def __init__(
        self,
        log_level: Optional[str] = None,
        msg_fmt: str = "'{_f_name}' took {_dur:.2f} {_uom_name}",
            uom: str = 's') -> None:
        """Initialize specified arguments for _TimeIt object.

        Args:
            log_level: logging level to use (default: {None})
            msg_fmt: message format. Possible keys for message format:
                - main:
                  - '_f_name': function name.
                  - '_dur': time it took to execute function (in format
                    specified in time_fmt).
                  - '_uom_name': unit of measure name (second(s),
                    minute(s) etc.).
                - positional arguments: arg0, arg1, arg2 etc. Will name
                    positional arguments (if any) of function that uses
                    this decorator. If function has __self__ attribute,
                    it will be used for arg0.
                - keyword arguments: keyword arguments (if any) of
                    function that uses this decorator.
                (default: {"'{f_name}' took {dur:.2f} {uom_name}"})
            uom: time unit of measure to output. Possible values:
                'ms' (milliseconds), 's' (seconds), 'm' (minutes), 'h'
                (hours) (default: {'s'})
        """
        self.log_level = log_level
        self.msg_fmt = msg_fmt
        self.uom = uom

    def _get_message_vals(self, func, duration, args=None, kwargs=None):

        def insert_args(args, func, vals):
            pos = 0
            if hasattr(func, '__self__'):
                vals['arg0'] = func.__self__
                # Move position to right, because arg0 is now already
                # assigned.
                pos = 1
            for i, arg in enumerate(args, pos):
                vals['arg%s' % i] = arg

        if not args:
            args = ()
        if not kwargs:
            kwargs = {}
        uom_name, uom_ratio = self._time_map[self.uom]
        # Define main vals.
        vals = {
            '_f_name': func.__name__,
            '_dur': duration * uom_ratio,
            '_uom_name': uom_name
        }
        insert_args(args, func, vals)
        # Insert kwargs. Will overwrite old keys if some already exist.
        vals.update(kwargs)
        return vals

    def _get_message(
        self,
        func,
        duration: float,
        args: Optional[tuple] = None,
            kwargs: Optional[dict] = None):
        vals = self._get_message_vals(func, duration, args=args, kwargs=kwargs)
        return self.msg_fmt.format(**vals)

    def output(self, func, duration, args=None, kwargs=None):
        msg = self._get_message(func, duration, args=args, kwargs=kwargs)
        if self.log_level:
            log_level = self.log_level.lower()
            getattr(logging, log_level)(msg)
        else:
            print(msg)

    def __call__(self, func):
        """Wrap function and track time it took to execute it."""
        def wrapped(*args, **kwargs):
            ts = time.time()
            res = func(*args, **kwargs)
            te = time.time()
            self.output(func, te-ts, args=args, kwargs=kwargs)
            return res
        return wrapped


time_it = _TimeIt
