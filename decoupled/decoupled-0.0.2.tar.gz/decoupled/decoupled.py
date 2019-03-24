''' decoupled: run a function in a different process '''

# pylint: disable=keyword-arg-before-vararg
# This is the order decorator needs

import multiprocessing
import queue

from decorator import decorator


@decorator
def decoupled(func, timeout=None, *args, **kwargs):
    ''' run a function in a different process '''
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


class ChildTimeoutError(Exception):
    ''' thrown when the child process takes too long '''


class ChildCrashedError(Exception):
    ''' thrown when the child process crashes '''
