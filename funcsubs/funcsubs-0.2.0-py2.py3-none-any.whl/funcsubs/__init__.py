import asyncio
import inspect
import functools
import logging
import typing

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.2.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"
_log = logging.getLogger(__name__)

T = typing.TypeVar('T')


def always_predicate(*_args):
    return True


class GenericSignal:

    __slots__ = ('callbacks', )

    def __init__(self):
        self.callbacks = ()

    def add_callback(self, callback: typing.Callable, predicate=always_predicate) -> None:
        self.callbacks += ((predicate, callback), )

    @functools.lru_cache(None)
    def select_callbacks(self, axis_values):
        return tuple(callback for predicate, callback in self.callbacks if predicate(axis_values))

    def clear(self):
        self.callbacks = ()
        self.select_callbacks.cache_clear()


class SyncSideEffectSignal(GenericSignal):

    def dispatch(self, axis_values, callback_args=()) -> None:
        for callback in self.select_callbacks(axis_values):
            try:
                callback(*callback_args)
            except Exception:  # pylint: disable=broad-except
                _log.exception('Exception when dispatch side effect signal')


class AsyncSideEffectSignal(GenericSignal):

    async def dispatch(self, axis_values, callback_args=()) -> None:
        for callback in self.select_callbacks(axis_values):
            try:
                if inspect.iscoroutinefunction(callback):
                    await callback(*callback_args)
                else:
                    callback(*callback_args)
            except Exception:  # pylint: disable=broad-except
                _log.exception('Exception when dispatch side effect signal')
