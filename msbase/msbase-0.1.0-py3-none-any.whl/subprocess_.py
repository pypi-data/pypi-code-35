import subprocess
import os
import sys
import glob
from os.path import join
import time
import logging
from multiprocessing import Pool, Value
import time
from termcolor import cprint
from threading import Thread
from queue import Queue, Empty

'''Levels:
DEBUG
INFO
WARN
ERROR
CRITICAL
'''

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def timed(func):
    def function_wrapper(*args, **kwargs):
        now = time.time()
        ret = func(*args, **kwargs)
        logger.debug("%s(%s, %s) spent %.2fs" %
                     (func.__qualname__, args, kwargs, time.time() - now))
        return ret
    return function_wrapper

ON_POSIX = 'posix' in sys.builtin_module_names

def enqueue_output(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def call_std(args, cwd=None, env={}, output=True):
    if output:
        p = subprocess.Popen(args, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, bufsize=1,
                             close_fds=ON_POSIX, cwd=cwd, env=dict(os.environ, **env))
        stdout = ""
        q_stdout = Queue()
        t_stdout = Thread(target=enqueue_output, args=(p.stdout, q_stdout))
        t_stdout.daemon = True
        t_stdout.start()
        stderr = ""
        q_stderr = Queue()
        t_stderr = Thread(target=enqueue_output, args=(p.stderr, q_stderr))
        t_stderr.daemon = True
        t_stderr.start()
        while True:
            return_code = p.poll()
            if return_code is not None:
                break
            try:
                stdout_line = str(q_stdout.get_nowait(), "utf-8")
            except Empty:
                stdout_line = ''
            try:
                stderr_line = str(q_stderr.get_nowait(), "utf-8")
            except Empty:
                stderr_line = ''
            if stdout_line:
                stdout += stdout_line
                logger.info(stdout_line.rstrip())
            if stderr_line:
                stderr += stderr_line
                logger.warning(stderr_line.rstrip())
        while True:
            try:
                stdout_line = str(q_stdout.get(timeout=.1), "utf-8")
            except Empty:
                break
            stdout += stdout_line
            logger.info(stdout_line.rstrip())
        while True:
            try:
                stderr_line = str(q_stderr.get(timeout=.1), "utf-8")
            except Empty:
                break
            stderr += stderr_line
            logger.warning(stderr_line.rstrip())

        return (return_code, stdout, stderr)
    else:
        code = subprocess.call(args, cwd=cwd, env=dict(os.environ, **env))
        return (code, None, None)

@timed
def try_call_std(args, cwd=None, env={}, verbose=True,
                 output=True, noexception=False):
    if verbose:
        cprint("+ " + " ".join(args), "blue")
    code, stdout, stderr = call_std(args, cwd, env, output)
    if not noexception and code != 0:
        if verbose:
            print("STDOUT: ")
            print(stdout)
            print("STDERR: ")
            cprint(stderr, "red")
        raise Exception("calling " + " ".join(args) + " failed")
    else:
        return stdout, stderr, code

def multiprocess(task, inputs, n: int, verbose=True, return_dict=True):
    counter = Value('i', 0)
    total = float(len(inputs))
    start_time = time.time()

    global run
    def run(input):
        with counter.get_lock():
            if verbose:
                print("%fs - progress: %f" % (time.time() - start_time, counter.value / total))
            counter.value += 1
        try:
            return (True, task(input))
        except Exception as e:
            return (False, e)

    with Pool(n) as p:
        results = p.map(run, inputs)
        if verbose:
            print("total spent time: %f" % (time.time() - start_time))
        if return_dict:
            return dict(zip(inputs, results))
        else:
            return results

