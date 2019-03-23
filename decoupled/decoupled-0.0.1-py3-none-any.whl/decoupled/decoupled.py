''' decoupled: run a function in a different process '''

import functools
import multiprocessing
import queue


def decoupled(timeout=None):
    ''' run a function in a different process '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result_queue = multiprocessing.Queue()

            def proc():
                try:
                    result_queue.put({'returnValue': func(*args, **kwargs)})
                except Exception as err:  # pylint: disable=broad-except
                    result_queue.put({'err': err})

            process = multiprocessing.Process(target=proc)
            process.start()
            process.join(timeout=timeout)

            try:
                if process.exitcode is None:
                    raise ChildTimeoutError

                try:
                    retval = result_queue.get(timeout=0)
                    try:
                        return retval['returnValue']
                    except KeyError:
                        raise retval['err']
                except queue.Empty:
                    raise ChildCrashedError
            finally:
                process.terminate()
        return wrapper
    return decorator


class ChildTimeoutError(Exception):
    ''' thrown when the child process takes too long '''


class ChildCrashedError(Exception):
    ''' thrown when the child process crashes '''
