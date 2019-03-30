#!usr/bin/env python
"""A set of utility functions for the planners.
"""

from typing import Tuple

import numpy as np


def id(x):
    return x


def is_shape(s):
    # If it's not a tuple, it's not a shape
    if not isinstance(s, tuple):
        return False

    # If any value is not an int, it's not a shape
    for dimension in s:
        if not dimension == int(dimension):
            return False

    # Otherwise it's a shape
    return True


def get_shape(a) -> Tuple[int]:
    # If it's already a shape, just return it
    if is_shape(a):
        return a

    # If it's a numpy array, it's simple
    try:
        return a.shape
    except AttributeError:
        pass

    # If not, let's see if it's a number
    try:
        # noinspection PyRedundantParentheses
        return (int(a),)
    except (ValueError, TypeError):
        pass

    # Finally, let's try to make it an array
    return np.asarray(a).shape


def get_segment_axis(shape, axis, s_axis):
    axis = len(shape) + axis if axis < 0 else axis
    s_axis = len(shape) + s_axis if s_axis < 0 else s_axis
    if s_axis < axis:
        return axis - 1
    else:
        return axis


def compute_filter_nfft(n_filter, n_signal):
    # Verify that n_filter and n_signal are positive numbers
    n_ok = type(n_filter) in (int, float) and n_filter > 0
    n_x_ok = type(n_signal) in (int, float) and n_signal > 0
    if not (n_ok and n_x_ok):
        raise ValueError("n_filter and n_signal must be positive numbers")
    if n_filter > n_signal:
        return 2**np.ceil(np.log2(n_filter+n_signal-1))
    else:
        fft_flops = np.array([18, 59, 138, 303, 660, 1441, 3150, 6875,
                              14952, 32373, 69762, 149647, 319644, 680105,
                              1441974, 3047619, 6422736, 13500637,
                              28311786, 59244791])
        # noinspection PyTypeChecker
        nfft_list = np.power(2, np.arange(np.ceil(np.log2(n_filter)), 21))
        # noinspection PyTypeChecker
        fft_flops = fft_flops[-len(nfft_list):]
        l_list = nfft_list - (n_filter - 1)
        min_idx = np.argmin(np.ceil(n_signal/l_list) * fft_flops)
        return int(nfft_list[min_idx])


def pad_array(a, shape):
    pads = [(0, x - y) for x, y in zip(shape, a.shape)]
    return np.pad(a, pads, mode='constant', constant_values=0)


def expand_me(a, axis, ndim):
    # Validate axis and make it absolute if needed
    if axis >= ndim:
        raise ValueError("Target axis must be within dimensions.")
    elif axis < 0:
        axis += ndim

    # Add leading dimensions
    for k in range(axis):
        a = np.expand_dims(a, 0)

    # Add trailing dimensions
    for k in range(axis+1, ndim):
        a = np.expand_dims(a, -1)

    return a


def scipy_rfft_to_complex(a, axis=-1):
    odd = a.shape[axis] % 2
    n_dim = len(a.shape)

    # define slices
    slices_0 = [slice(None)] * n_dim
    slices_0[axis] = slice(0, 1)
    slices = [slice(None)] * n_dim
    slices[axis] = slice(1, None, 2)

    # take real part
    a_complex = np.concatenate((a[tuple(slices_0)],
                                a[tuple(slices)]), axis=axis) + 0j

    # change slices and add complex part
    slices[axis] = slice(2, None, 2)
    if odd:
        slices_0[axis] = slice(1, None)
        a_complex[tuple(slices_0)] += 1j*a[tuple(slices)]
    else:
        slices_0[axis] = slice(1, -1)
        a_complex[tuple(slices_0)] += 1j*a[tuple(slices)]

    return a_complex


def complex_to_scipy_rfft(a_complex, axis=-1, even=None):
    # If not given, determine odd or even output
    if even is None:
        if a_complex[-1].imag == 0:
            even = 1
        else:
            even = 0

    # Define output shape and create empty matrix
    out_shape = list(a_complex.shape)
    n = out_shape[axis]
    out_shape[axis] += out_shape[axis] - (1 + even)
    a_sfft = np.empty(out_shape)

    # set up slices and divide input into real and imaginary parts
    slices_0 = [slice(None)] * len(out_shape)
    slices = [slice(None)] * len(out_shape)
    slices_0[axis] = slice(0, 1)
    ar = a_complex.real
    ac = a_complex.imag

    # Fill the output
    a_sfft[tuple(slices_0)] = ar[tuple(slices_0)]
    slices_0[axis] = slice(1, None, 2)
    slices[axis] = slice(1, None)
    a_sfft[tuple(slices_0)] = ar[tuple(slices)]
    slices_0[axis] = slice(2, None, 2)
    slices[axis] = slice(1, n - even)
    a_sfft[tuple(slices_0)] = ac[tuple(slices)]

    return a_sfft


def replace(xs, k, v):
    """Replace the element with index `k` in `xs` with `v`"""
    xs_ = list(xs)
    xs_[k] = v
    return xs_
