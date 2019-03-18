# coding=utf-8
from __future__ import print_function

import contextlib
import functools
import multiprocessing
from multiprocessing import Pool as ProcessPool
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing.dummy import current_process as currentThread

import tqdm

from suanpan import utils

WORKERS = multiprocessing.cpu_count()
DEFAULT_PBAR_FORMAT = "{desc}: {n_fmt}/{total_fmt} |{bar}"
DEFAULT_PBAR_CONFIG = {"bar_format": DEFAULT_PBAR_FORMAT}


@contextlib.contextmanager
def multiThread(workers=None):
    workers = workers or WORKERS
    pool = ThreadPool(processes=workers)
    yield pool
    pool.close()


@contextlib.contextmanager
def multiProcess(workers=None):
    workers = workers or WORKERS
    pool = ProcessPool(processes=workers)
    yield pool
    pool.close()


def parsePbarConfig(pbar):
    if pbar is True:
        return utils.merge({}, DEFAULT_PBAR_CONFIG, {"desc": "Processing"})
    elif isinstance(pbar, str):
        return utils.merge({}, DEFAULT_PBAR_CONFIG, {"desc": pbar})
    elif pbar in (False, None):
        return utils.merge({}, DEFAULT_PBAR_CONFIG, {"disable": True})
    elif isinstance(pbar, dict):
        return utils.merge({}, DEFAULT_PBAR_CONFIG, pbar)
    else:
        raise Exception("Invalid pbar config: bool | str | dict. but {}".format(pbar))


def pbarRunner(pbar, quantity=1):
    def _dec(runner):
        @functools.wraps(runner)
        def _runner(*args, **kwargs):
            result = runner(*args, **kwargs)
            pbar.update(quantity)
            return result

        return _runner

    return _dec


def map(func, iterable, chunksize=None, workers=None, pbar=None, thread=False):
    mapFunc = "imap" if not thread else "map"
    chunksize = (chunksize or 1) if mapFunc == "imap" else chunksize
    items = list(iterable)
    pbarConfig = parsePbarConfig(pbar)
    pbarConfig.update(total=len(items))
    poolClass = multiThread if thread else multiProcess
    with poolClass(workers) as pool:
        if mapFunc == "imap":
            with tqdm.tqdm(
                pool.imap(func, items, chunksize=chunksize), **pbarConfig
            ) as pbar:
                results = list(pbar)
        else:
            with tqdm.tqdm(**pbarConfig) as pbar:
                run = pbarRunner(pbar)(func)
                results = pool.map(run, items, chunksize=chunksize)
    return results


def imap(func, iterable, chunksize=1, workers=None, pbar=None, thread=False):
    items = list(iterable)
    pbarConfig = parsePbarConfig(pbar)
    pbarConfig.update(total=len(items))
    poolClass = multiThread if thread else multiProcess
    with poolClass(workers) as pool:
        with tqdm.tqdm(
            pool.imap(func, items, chunksize=chunksize), **pbarConfig
        ) as pbar:
            results = list(pbar)
    return pbar


def starmap(func, iterable, chunksize=1, workers=None, pbar=None, thread=False):
    if pbar and not thread:
        raise Exception("Pbar is disabled when thread is False")
    items = list(iterable)
    poolClass = multiThread if thread else multiProcess
    if pbar:
        pbarConfig = parsePbarConfig(pbar)
        pbarConfig.update(total=len(items))
        with poolClass(workers) as pool:
            with tqdm.tqdm(**pbarConfig) as pbar:
                run = pbarRunner(pbar)(func)
                results = pool.starmap(run, items, chunksize=chunksize)
    else:
        with poolClass(workers) as pool:
            results = pool.starmap(func, items, chunksize=chunksize)
    return results


def run(func, args=(), kwds={}, thread=False, **kwargs):
    poolClass = multiThread if thread else multiProcess
    with poolClass(1) as pool:
        return pool.apply_async(func, args=args, kwds=kwds, **kwargs)
