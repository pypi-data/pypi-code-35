"""Docstring for ``Wrapper``.

===========================
High-level Function Wrapper
===========================
==================== =========================================================
Operation Wrapper
==============================================================================
multiprocessor       Functional wrapper for multiprocessing.
==================== =========================================================
==================== =========================================================
Interfaces
==============================================================================
uprint               Print option interface within a function.
lprint               stdout the shape of input layer & output layer in DL
aprint               Stdout the `numpy.ndarray` in pretty.
==================== =========================================================
"""


import numpy as np
import itertools as it
import multiprocessing as mpr


__all__ = [
    'multiprocessor',
    'uprint',
    'lprint',
    'aprint',
]


def multiprocessor(func, worker=2, arg_zip=None, *args, **kwargs):
    """Use multiprocessing as a function.

    Just for convenience.

    Parameters
    ----------
    func: Function
      Any function without ``lambda``.

    worker: int (default: 2)
      A number of processes.

    arg_zip: zip (default: None)
      A ``zip`` instance.

    Returns
    -------
    list
      A list contains results of each processes.

    See Also
    --------
    ``multiprocessing.pool``

    Examples
    --------
    >>> from unipy.utils.wrapper import multiprocessor
    >>> alist = [1, 2, 3]
    >>> blist = [-1, -2, -3]
    >>> def afunc(x, y):
    ...     return x + y
    ...
    >>> multiprocessor(afunc, arg_zip=zip(alist, blist))
    [0, 0, 0]
    >>> def bfunc(x):
    ...     return x + 2
    ...
    >>> multiprocessor(bfunc, arg_zip=zip(alist))
    [3, 4, 5]

    """
    with mpr.pool.Pool(processes=worker) as pool:
        resp = pool.starmap(func, arg_zip, *args, **kwargs)

    return resp


def uprint(*args, print_ok=True, **kwargs):
    """Print option interface.

    This function is equal to ``print`` function but added ``print_ok``
    option. This allows you to control printing in a function.

    Parameters
    ----------
    *args: whatever ``print`` allows.
      It is same as ``print`` does.

    print_ok: Boolean (default: True)
      An option whether you want to print something out or not.

    arg_zip: zip (default: None)
      A ``zip`` instance.

    """
    if print_ok:
        print(*args, **kwargs)


def lprint(input_x, output, name=None):
    """Print option interface.

    This function is to stdout the shape of input layer & output layer
    in Deep Learning architecture.

    Parameters
    ----------
    input_x: numpy.ndarray
      A ``numpy.ndarray`` object of input source.

    output: numpy.ndarray
      A ``numpy.ndarray`` object of output target.

    name: str (default: None)
      An optional name you want to print out.

    """
    print(f'{str(name)}:\t{input_x.shape} -> {output.shape}')


def aprint(*arr, maxlen=None, name_list=None, decimals=None):
    """Stdout the `numpy.ndarray` in pretty.

    It prints the multiple `numpy.ndarray` out "Side by Side."

    Parameters
    ----------
    arr: numpy.ndarray
      Any arrays you want to print out.

    maxlen: int (default: None)
      A length for each array to print out.
      It is automatically calculated in case of `None`.

    name_list: list (default: None)
      A list contains the names of each arrays.
      Upper Alphabet is given in case of `None`.

    decimals: int (default: None)
      A number to a specified number of digits to truncate.


    Examples
    --------
    >>> from unipy.utils.wrapper import aprint
    >>> arr_x = np.array([
    ... [.6, .5, .1],
    ... [.4, .2, .8],
    ... ])
    >>> arr_y = np.array([
    ... [.4, .6],
    ... [.7, .3,],
    ... ])
    >>> aprint(arr_x, arr_y)
    =========================================
    |  A                 |    B             |
    |  (2, 3)            |    (2, 2)        |
    =========================================
    |  [[0.6 0.5 0.1]    |    [[0.4 0.6]    |
    |   [0.4 0.2 0.8]]   |     [0.7 0.3]]   |
    =========================================
    >>> aprint(arr_x, arr_y, name_list=['X', 'Y'])
    =========================================
    |  X                 |    Y             |
    |  (2, 3)            |    (2, 2)        |
    =========================================
    |  [[0.6 0.5 0.1]    |    [[0.4 0.6]    |
    |   [0.4 0.2 0.8]]   |     [0.7 0.3]]   |
    =========================================
    >>> aprint(arr_x, arr_y, arr_y[:1], name_list=['X', 'Y', 'Y_1'])
    ============================================================
    |  X                 |    Y             |    Y_1           |
    |  (2, 3)            |    (2, 2)        |    (1, 2)        |
    ============================================================
    |  [[0.6 0.5 0.1]    |    [[0.4 0.6]    |    [[0.4 0.6]]   |
    |   [0.4 0.2 0.8]]   |     [0.7 0.3]]   |                  |
    ============================================================

    """
    if not all(isinstance(a, np.ndarray) for a in arr):
        raise AttributeError("All objects should be 'numpy.ndarray' objects.")

    if decimals is not None:
        arr = [a.round(decimals) for a in arr]

    arr_shape_list = [str(a.shape) for a in arr]
    str_arr_list = [str(a).splitlines() for a in arr]

    if maxlen is None:
        maxlen_list = [len(max(s, key=len)) for s in str_arr_list]
    else:
        maxlen_list = [int(maxlen) for s in str_arr_list]

    if name_list is None:
        name_list = list(map(chr, range(ord('A'), ord('B')+1)))[:len(arr)]


    def formatter(iterable, len_list):
        base_format = "  {line:<{l}}  |"
        return '|' + ' '.join([base_format.format(line=a, l=l)
                                if a
                                else base_format.format(line='', l=l)
                                for (a, l) in zip(iterable, len_list)])


    for i, arrs in enumerate(it.zip_longest(*str_arr_list)):
        str_line = formatter(arrs, maxlen_list)
        str_len = len(str_line)
        if i == 0:
            print('=' * str_len)
            col_line = formatter(name_list, maxlen_list)
            shape_line = formatter(arr_shape_list, maxlen_list)

            print(col_line)
            print(shape_line)
            print('=' * str_len)
        print(str_line)

    print('=' * str_len)
