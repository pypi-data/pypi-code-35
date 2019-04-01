import asyncio
import inspect
import functools
import logging
import operator
import typing

from frozendict import frozendict

__author__ = "Bogdan Gladyshev"
__copyright__ = "Copyright 2017, Bogdan Gladyshev"
__credits__ = ["Bogdan Gladyshev"]
__license__ = "MIT"
__version__ = "0.4.0"
__maintainer__ = "Bogdan Gladyshev"
__email__ = "siredvin.dark@gmail.com"
__status__ = "Production"
__all__ = [
    'SyncSideEffectSignal', 'AsyncSideEffectSignal', 'SyncElectionSignal',
    'SyncInplaceEffectSignal', 'AsyncInplaceEffectSignal'
]
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
        self.select_callbacks.cache_clear()

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


class SyncInplaceEffectSignal(GenericSignal):

    def dispatch(self, axis_values, callback_args=()) -> None:
        for callback in self.select_callbacks(axis_values):
            callback(*callback_args)


class AsyncInplaceEffectSignal(GenericSignal):

    async def dispatch(self, axis_values, callback_args=()) -> None:
        for callback in self.select_callbacks(axis_values):
            if inspect.iscoroutinefunction(callback):
                await callback(*callback_args)
            else:
                callback(*callback_args)


class SyncElectionSignal(GenericSignal):

    def dispatch(self, axis_values, callback_args=(), callback_kwargs=frozendict({})):
        candidates = []
        for election_callback in self.select_callbacks(axis_values):
            try:
                election_result = election_callback(*callback_args, **callback_kwargs)
                if election_result is not None:
                    candidates.append(election_result)
            except Exception:  # pylint: disable=broad-except
                _log.exception('Exception when dispatch election signal')
        return max(candidates, default=(None, None), key=operator.itemgetter(1))[0]
