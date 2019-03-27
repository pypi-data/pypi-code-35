# -*- coding: utf8 -*-
import logging
import multiprocessing
import pickle
import sys
import os
import signal
import traceback
from multiprocessing.pool import ThreadPool

import six

DEFAULT_USE_THREADS = True


__exception_value_cross_process = None
__exception_value_cross_process_pipe = None


def process_worker_init(parent_id, exception_value_cross_process, exception_value_cross_process_pipe):
    global __exception_value_cross_process
    global __exception_value_cross_process_pipe

    def sig_int(_signal_num, _frame):
        os.kill(parent_id, signal.SIGSTOP)

    def sig_int_sef_fault(_signal_num, _frame):
        os.kill(parent_id, signal.SIGTERM)

    __exception_value_cross_process = exception_value_cross_process
    __exception_value_cross_process_pipe = exception_value_cross_process_pipe

    signal.signal(signal.SIGINT, sig_int)
    signal.signal(signal.SIGSEGV, sig_int_sef_fault)


class _MultiProcessControlShim(object):
    __futures = []

    def __init__(self, use_threads=None):
        if use_threads is None:
            self.__use_threads = DEFAULT_USE_THREADS
        else:
            self.__use_threads = use_threads

    class MultiShimFuture(object):
        def __init__(self, exc_info):
            self._method_exc_info = exc_info

        def wait(self):
            if self._method_exc_info is not None:
                six.reraise(*self._method_exc_info)

    # noinspection PyUnusedLocal
    @classmethod
    def execute(cls, method, args, callback=None, high=False):
        method_exc_info = None
        # noinspection PyBroadException
        try:
            result = method(*args)
            if callback is not None:
                callback(result)
        except Exception:
            method_exc_info = sys.exc_info()

        future = cls.MultiShimFuture(method_exc_info)
        cls.__futures.append(future)

        return future

    @property
    def using_threads(self):
        return self.__use_threads

    def terminate(self):
        pass

    def close(self):
        pass

    def join(self):
        while self.__futures:
            future = self.__futures.pop(0)
            future.wait()


def get_multi_process_control(processes, use_threads=None):
    if processes == 1:
        return _MultiProcessControlShim(use_threads=use_threads)

    if use_threads is None:
        use_threads = DEFAULT_USE_THREADS

    if use_threads is True:
        use_processes = os.environ.get('MALI_PROCESSES', '0') == '1'
        use_threads = not use_processes

    return _MultiProcessControl(processes, use_threads)


class _RemoteTraceback(Exception):
    def __init__(self, tb):
        self.tb = tb

    def __str__(self):
        return self.tb


class _ExceptionWithTraceback(object):
    def __init__(self, exc, tb):
        tb = traceback.format_exception(type(exc), exc, tb)
        tb = ''.join(tb)
        self.exc = exc
        self.tb = '\n"""\n%s"""' % tb

    def __reduce__(self):
        return _rebuild_exc, (self.exc, self.tb)


def _rebuild_exc(exc, tb):
    exc.__cause__ = _RemoteTraceback(tb)
    return exc


def _log_exceptions(method, error_callback, *args, **kwargs):
    global __exception_value_cross_process
    global __exception_value_cross_process_pipe

    result = None

    try:
        result = method(*args, **kwargs)
    except Exception as ex:
        exc_info = sys.exc_info()

        if __exception_value_cross_process is not None:
            e = _ExceptionWithTraceback(ex, exc_info[2])
            __exception_value_cross_process_pipe.send_bytes(pickle.dumps(e, pickle.HIGHEST_PROTOCOL))
            __exception_value_cross_process.value = 1
        elif error_callback is not None:
            error_callback(exc_info)  # this wil also rerise the originl ex

    # It was fine, give a normal answer
    return result


def _apply_async_with_exc(apply_method, method, args=(), kwds=None, callback=None, error_callback=None):
    args = (method, error_callback) + args
    return apply_method(_log_exceptions, args, kwds or {}, callback)


class _ThreadLoggingPool(ThreadPool):
    def apply_async_with_exc(self, method, args=(), kwds=None, callback=None, error_callback=None):
        return _apply_async_with_exc(super(_ThreadLoggingPool, self).apply_async, method, args, kwds, callback, error_callback)


class _ProcessLoggingPool(multiprocessing.pool.Pool):
    def apply_async_with_exc(self, method, args=(), kwds=None, callback=None, error_callback=None):
        return _apply_async_with_exc(super(_ProcessLoggingPool, self).apply_async, method, args, kwds, callback, error_callback)


class _MultiProcessControl(object):
    def __init__(self, processes, use_threads, max_pending_items=1000):
        processes = multiprocessing.cpu_count() * 5 if processes == -1 else processes
        self.__using_threads = False
        self.__semaphore = multiprocessing.Semaphore(max_pending_items)
        self.__semaphore_high = multiprocessing.Semaphore(int(max_pending_items / 10))
        self.__exception_value = None
        self.__exception_value_cross_process = multiprocessing.Value('b', 0)
        self.__exception_value_cross_process_pipe_sender, self.__exception_value_cross_process_pipe_recv = multiprocessing.Pipe()

        if use_threads:
            self.__use_threads(processes)
        else:
            try:
                self.__processing_pool = _ProcessLoggingPool(processes, process_worker_init, initargs=(os.getpid(), self.__exception_value_cross_process, self.__exception_value_cross_process_pipe_sender))
                self.__processing_pool_high = _ProcessLoggingPool(1, process_worker_init, initargs=(os.getpid(), self.__exception_value_cross_process, self.__exception_value_cross_process_pipe_sender))
            except AssertionError:
                self.__use_threads(processes)

    @property
    def using_threads(self):
        return self.__using_threads

    def __use_threads(self, processes):
        self.__using_threads = True
        self.__processing_pool = _ThreadLoggingPool(processes)
        self.__processing_pool_high = _ThreadLoggingPool(1)

    def __reraise_if_needed(self):
        if self.__exception_value is not None:
            six.reraise(*self.__exception_value)

        if self.__exception_value_cross_process.value:
            b = self.__exception_value_cross_process_pipe_recv.recv_bytes()
            rmeote_exc = pickle.loads(b)
            self.terminate()
            raise rmeote_exc

    def join(self):
        logging.debug('%s pool joining', self.__class__)
        self.__wait_pending_jobs()
        logging.debug('%s pool joined', self.__class__)

        self.__reraise_if_needed()

    close = join

    def __wait_pending_jobs(self):
        self.__processing_pool.close()

        self.__processing_pool.join()
        self.__processing_pool_high.close()
        self.__processing_pool_high.join()

    def __get_semaphore(self, high):
        return self.__semaphore_high if high else self.__semaphore

    def _finished_with_exc_if_needed(self, exc_info):
        if exc_info:
            self.__exception_value = exc_info
            self.terminate()
            six.reraise(*exc_info)

    def execute(self, method, args, callback=None, high=False):
        self.__get_semaphore(high).acquire()

        processing_pool = self.__processing_pool_high if high and self.__processing_pool_high else self.__processing_pool

        def finished(exc_info=None):
            self.__get_semaphore(high).release()

            self._finished_with_exc_if_needed(exc_info)

        def callback_wrapper(result):
            finished()
            if callback is not None:
                callback(result)

        self.__reraise_if_needed()

        job_async_result = processing_pool.apply_async_with_exc(
            method,
            args=args,
            callback=callback_wrapper,
            error_callback=finished if self.__using_threads else None)

        return job_async_result

    def terminate(self):
        self.__processing_pool.terminate()
        self.__processing_pool_high.terminate()
