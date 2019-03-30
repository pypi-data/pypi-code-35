# -*- coding: utf-8 -*-

from math import ceil, log2

import numpy as np

from . import _utils
try:
    import pyfftw
    from ._pyfftw_basics import (fft, fft_pair, rfft, rfft_pair,
                                 fftn, fftn_pair, rfftn, rfftn_pair,
                                 ifft, ifft_pair, irfft, irfft_pair,
                                 ifftn, ifftn_pair, irfftn, irfftn_pair)
except ImportError:
    try:
        import scipy.fftpack as _
        from ._scipy_basics import (fft, fft_pair, rfft, rfft_pair,
                                    fftn, fftn_pair, rfftn, rfftn_pair,
                                    ifft, ifft_pair, irfft, irfft_pair,
                                    ifftn, ifftn_pair, irfftn, irfftn_pair)
    except ImportError:
        from ._numpy_basics import (fft, fft_pair, rfft, rfft_pair,
                                    fftn, fftn_pair, rfftn, rfftn_pair,
                                    ifft, ifft_pair, irfft, irfft_pair,
                                    ifftn, ifftn_pair, irfftn, irfftn_pair)


# ### Hidden functions

def _convolve_slice(mode, len_x, len_y):
    if mode == "valid":
        return slice(len_y - 1, len_x)
    elif mode == "same":
        return slice((len_y - 1)//2, len_x + (len_y - 1)//2)
    elif mode == "full":
        return slice(0, len_x + len_y - 1)
    else:
        raise ValueError("Invalid mode: {} (must be one of 'valid', "
                         "'same' or 'full'".format(mode))


def _nd_preparations(x_shape, y_shape, mode, correlation):
    """Slices and FFT functions for N-dimensional convolution/correlation."""
    n_dimensions_x = len(x_shape)
    n_dimensions_y = len(y_shape)
    if not n_dimensions_x == n_dimensions_y:
        fn_type = "correlation" if correlation is True else "convolution"
        raise ValueError("Cannot plan {} for inputs of shape "
                         "{} and {}".format(fn_type, x_shape, y_shape))
    max_shape = np.max((x_shape, y_shape), axis=0)
    nfft = tuple(np.power(2, np.ceil(np.log2(2*max_shape - 1))).astype(int))
    rev_slices = tuple([slice(None, None, -1)]*n_dimensions_y)
    out_slices = tuple(_convolve_slice(mode, len_x, len_y)
                       for len_x, len_y in zip(x_shape, y_shape))

    axes = list(range(n_dimensions_x))
    planned_rfftn, planned_irfftn = \
        rfftn_pair(tuple(max_shape), nfft, axes=axes)

    return rev_slices, out_slices, planned_rfftn, planned_irfftn


def _1d_perparations(x_shape, y_shape, axis, mode):
    """Wrappers, slices and FFT functions for 1-D convolution/correlation."""

    n_dimensions_x = len(x_shape)
    n_dimensions_y = len(y_shape)
    n_dimensions_out = max(n_dimensions_x, n_dimensions_y)

    if axis is None:
        axis = -1

    if n_dimensions_y == 1 and not n_dimensions_x == 1:
        input_shape_ = list(x_shape)
        input_shape_[axis] = max(input_shape_[axis], y_shape[0])
        x_wrapper = _utils.id

        def y_wrapper(y_fft):
            return _utils.expand_me(y_fft, axis, n_dimensions_x)

        x_rfft_, y_rfft_ = (0, 1)

    elif n_dimensions_x == 1 and not n_dimensions_y == 1:
        input_shape_ = list(y_shape)
        input_shape_[axis] = max(input_shape_[axis], x_shape[0])
        y_wrapper = _utils.id

        def x_wrapper(x_fft):
            return _utils.expand_me(x_fft, axis, n_dimensions_x)

        x_rfft_, y_rfft_ = (1, 0)

    else:
        input_shape_ = np.max((x_shape, y_shape), axis=0)
        x_wrapper, y_wrapper = (_utils.id, _utils.id)
        x_rfft_, y_rfft_ = (0, 0)

    planned_rffts = [None, None]
    input_shape = tuple(input_shape_)
    nfft = (int(2**ceil(log2(2*input_shape[axis] - 1))),)
    len_x = x_shape[0] if n_dimensions_x == 1 else x_shape[axis]
    len_y = y_shape[0] if n_dimensions_y == 1 else y_shape[axis]
    rev_slices = tuple(_utils.replace([slice(None)]*n_dimensions_y,
                                      axis,
                                      slice(None, None, -1)))
    out_slices = tuple(_utils.replace([slice(None)]*n_dimensions_out,
                                      axis,
                                      _convolve_slice(mode, len_x, len_y)))

    planned_rffts[0], planned_irfft = rfft_pair(input_shape,
                                                nfft[0],
                                                axis=axis)
    if not n_dimensions_x == n_dimensions_y:
        input_length = x_shape[0] if n_dimensions_x == 1 else y_shape[0]
        planned_rffts[1] = rfft(input_length, nfft[0])
    else:
        planned_rffts[1] = planned_rffts[0]

    return (x_wrapper,
            y_wrapper,
            rev_slices,
            out_slices,
            planned_rffts[x_rfft_],
            planned_rffts[y_rfft_],
            planned_irfft)


def _convolve_or_correlate(plan_x,
                           plan_y,
                           mode="full",
                           axis=None,
                           correlation=False):
    """Returns a planned function for computing the convolution of two
    sequences or arrays.

    Parameters
    ----------
    plan_x : integer, shape or array-like
        First input sequence, it's shape or length.
    plan_y : integer, shape or array-like
        Second input sequence, it's shape or length.
    mode : Optional[str]
        A string indicating the output size.

        'full'
            The output is the full discrete linear convolution of the
            inputs. (Default)
        'valid'
            The output consists only of those elements that do not rely on
            zero-padding.
        'same'
            The output is the same size as plan_x, centered with respect to
            the 'full' output.
    axis : Optional[int]
        The axis or axes along which the convolution is computed.
        Default is the last N axes of the highest-rank input where N is the
        rank of the lowest-rank input.
    correlation : Optional[bool]
        Indicates that correlation, rather than convolution, should be
        planned. Default is False.

    Returns
    -------
    planned_function(x_transformed, y_transformed)
        Planned convolution or correlation function.
    planned_x_transform_function(x)
        Planned transform function for x
    planned_y_transform_function(y)
        Planned transform function for y

    Raises
    ------
    ValueError
        If no function can be planned for the given arguments.
    """

    # Get dimensions
    x_shape = _utils.get_shape(plan_x)
    y_shape = _utils.get_shape(plan_y)

    if axis is None and min(len(x_shape), len(y_shape)) > 1:
        rev_slices, out_slices, x_rfft, planned_irfft = \
            _nd_preparations(x_shape, y_shape, mode, correlation)
        y_rfft = x_rfft
        x_wrapper = _utils.id
        y_wrapper = _utils.id

    else:
        (x_wrapper,
         y_wrapper,
         rev_slices,
         out_slices,
         x_rfft,
         y_rfft,
         planned_irfft) = _1d_perparations(x_shape, y_shape, axis, mode)

    def x_transform_function(x):
        return x_wrapper(x_rfft(x))

    if correlation:
        def y_transform_function(y):
            return y_wrapper(y_rfft(y[rev_slices]))
    else:
        def y_transform_function(y):
            return y_wrapper(y_rfft(y))

    def planned_function(x_fft, y_fft):
        return planned_irfft(x_fft*y_fft)[out_slices]

    return planned_function, x_transform_function, y_transform_function


# ### Public functions

def firfilter2(filter_coefficients, signal, axis=-1):
    """Returns a planned FIR-filter function.

    The planned function is returned along with separate input transform
    functions. This is intended for more advanced use cases, such as when
    precise control of transforms is required for memoization or other
    reasons. For most use cases, `firfilter`, `firfilter_const_filter`
    or `firfilter_const_signal` are more appropriate.

    Parameters
    ----------
    filter_coefficients: Union[Array-like, int]
        An array of filter coefficients or a filter length
    signal: Union[Array-like, Tuple[int, int], int]
        A signal array, shape or length
    axis: int
        The axis of `signal` along which the filter shall be applied

    Returns
    planned_filter(b_transformed, x_transformed)
        The filtering function
    b_transform_function(b)
        The filter transform function
    x_transform_function(x)
        The signal transform function

    See also
    --------
    firfilter, firfilter_const_filter, firfilter_const_signal
    """

    filter_length = _utils.get_shape(filter_coefficients)[0]
    signal_shape = _utils.get_shape(signal)
    signal_length = signal_shape[axis]
    n_dim = len(signal_shape)

    fft_size = _utils.compute_filter_nfft(filter_length, signal_length)

    # ### Make pyfftw plans
    u_shape = tuple(_utils.replace(signal_shape, axis, fft_size))
    rfft_function, irfft_function = rfft_pair(tuple(u_shape),
                                              fft_size,
                                              axis=axis)

    if n_dim > 1:
        rfft_function_filter = rfft(fft_size)
    else:
        rfft_function_filter = rfft_function

    segment_length = fft_size - filter_length + 1
    padded_signal_shape = tuple(_utils.replace(signal_shape, axis, fft_size))

    def filter_transform_function(b):
        return rfft_function_filter(
            np.hstack((b, np.zeros(fft_size - filter_length))))

    def signal_transform_function(x):
        if not all(a == b for a, b in zip(x.shape, signal_shape)):
            raise ValueError("Invalid signal shape {}, function expects {}"
                             .format(x.shape, signal_shape))
        slices = [slice(None)] * n_dim
        for k in range(0, signal_length, segment_length):
            k_to = np.min((k + segment_length, signal_length))
            slices_ = tuple(_utils.replace(slices, axis, slice(k, k_to)))
            yield rfft_function(_utils.pad_array(x[slices_],
                                                 padded_signal_shape))

    def filter_function(transformed_filter, transformed_segments):
        y = np.zeros(signal_shape)
        slices = [slice(None)]*n_dim
        for k in range(0, signal_length, segment_length):
            y_ = irfft_function(np.apply_along_axis(
                lambda x: x*transformed_filter,
                axis,
                next(transformed_segments)))
            y_to = np.min((signal_length, k + fft_size))
            out_slices = tuple(_utils.replace(slices, axis, slice(k, y_to)))
            part_slices = \
                tuple(_utils.replace(slices, axis, slice(0, y_to - k)))
            y[out_slices] += y_[part_slices].real

        return y

    return (filter_function,
            filter_transform_function,
            signal_transform_function)


def firfilter(plan_b, plan_x, axis=-1):
    """Returns a planned function that filters a signal using the frequency
    domain overlap-and-add method with pyfftw.

    Parameters
    ----------
    plan_b : integer, shape or array-like
        A filter vector or its length or shape
    plan_x : integer, shape or array-like
        A signal vector or its length or shape
    axis : optional[int]
        Axis in plan_x along which the filter is applied

    Returns
    -------
    planned_filter(b, x)
        The filtering function

    Raises
    ------
    ValueError
        If filter has more than one dimensions.
    """

    (filter_function,
     filter_transform_function,
     signal_transform_function) = firfilter2(plan_b, plan_x, axis=axis)

    def planned_firfilter(b, x):
        return filter_function(filter_transform_function(b),
                               signal_transform_function(x))

    return planned_firfilter


def firfilter_const_filter(b, plan_x, axis=-1):
    """Returns a planned function that filters a signal using the frequency
    domain overlap-and-add method with pyfftw.

    Parameters
    ----------
    b : array-like
        A filter vector
    plan_x : integer, shape or array-like
        A signal vector or its length or shape
    axis : optional[int]
        Axis in plan_x along which the filter is applied

    Returns
    -------
    planned_firfilter(x)
        The planned FIR-filtering function.

    Raises
    ------
    ValueError
        If filter has more than one dimensions.
    """

    (filter_function,
     filter_transform_function,
     signal_transform_function) = firfilter2(b, plan_x, axis=axis)

    b_ = filter_transform_function(b)

    def planned_firfilter(x):
        return filter_function(b_, signal_transform_function(x))

    return planned_firfilter


def firfilter_const_signal(plan_b, x, axis=-1):
    """Returns a planned function that filters a signal using the frequency
    domain overlap-and-add method with pyfftw.

    Parameters
    ----------
    plan_b : integer, shape or array-like
        A filter vector or its length or shape
    x : Array-like
        A signal vector or array
    axis : optional[int]
        Axis in plan_x along which the filter is applied

    Returns
    -------
    planned_firfilter(b)
        The planned FIR-filtering function.

    Raises
    ------
    ValueError
        If filter has more than one dimensions.
    """

    (filter_function,
     filter_transform_function,
     signal_transform_function) = firfilter2(plan_b, x, axis=axis)

    x_ = signal_transform_function(x)

    def planned_firfilter(b):
        return filter_function(filter_transform_function(b), x_)

    return planned_firfilter


def convolve2(plan_x, plan_y, mode='full', axis=None):
    """Plan a function for convolving two arrays.

    The planned function is returned along with separate input transform
    functions. This is intended for more advanced use cases, such as when
    precise control of transforms is required for memoization or other
    reasons. For most use cases, `convolve`, `convolve_const_x` or
    `convolve_const_y` are more appropriate.

    This planner distinguishes between several different cases:

        1. 1-D convolution of 1-D sequences or along single axis in N-D arrays
        2. N-D convolution of N-D sequences
        3. 1-D convolution along single axis in N-D array with 1-D sequence
        4. 1-D convolution of 1-D sequence along single axis in N-D array

        The shapes of the two inputs are usually sufficient to determine which
        case should be used. However, to get 1-D convolution along single axis
        in N-D arrays, 'axes' must be a single integer or a length 1 sequence.

    Parameters
    ----------
    plan_x : integer, shape or array-like
        First input sequence, it's shape or length.
    plan_y : integer, shape or array-like
        Second input sequence, it's shape or length.
    mode : Optional[str]
        A string indicating the output size.

        'full'
            The output is the full discrete linear convolution of the
            inputs. (Default)
        'valid'
            The output consists only of those elements that do not rely on
            zero-padding.
        'same'
            The output is the same size as plan_x, centered with respect to
            the 'full' output.
    axis : Optional[int or sequence of ints]
        The axis or axes along which the convolution is computed.
        Default is the last N axes of the highest-rank input where N is the
        rank of the lowest-rank input.

    Returns
    -------
    planned_convolve(x_transformed, y_transformed)
        Planned convolution function.
    x_transform_function(x)
        Planned transform function for first sequence
    y_transform_function(y)
        Planned transform function for second sequence

    Raises
    ------
    ValueError
        If no function can be planned for the given arguments.

    See also
    --------
    convolve, convolve_const_x, convolve_const_y
    """
    return _convolve_or_correlate(plan_x, plan_y, mode=mode, axis=axis)


def convolve(plan_x, plan_y, mode='full', axis=None):
    """Plan a function for convolving two arrays.

    This planner distinguishes between several different cases:

        1. 1-D convolution of 1-D sequences or along single axis in N-D arrays
        2. N-D convolution of N-D sequences
        3. 1-D convolution along single axis in N-D array with 1-D sequence
        4. 1-D convolution of 1-D sequence along single axis in N-D array

        The shapes of the two inputs are usually sufficient to determine which
        case should be used. However, to get 1-D convolution along single axis
        in N-D arrays, 'axes' must be a single integer or a length 1 sequence.

    Parameters
    ----------
    plan_x : integer, shape or array-like
        First input sequence, it's shape or length.
    plan_y : integer, shape or array-like
        Second input sequence, it's shape or length.
    mode : Optional[str]
        A string indicating the output size.

        'full'
            The output is the full discrete linear convolution of the
            inputs. (Default)
        'valid'
            The output consists only of those elements that do not rely on
            zero-padding.
        'same'
            The output is the same size as plan_x, centered with respect to
            the 'full' output.
    axis : Optional[int or sequence of ints]
        The axis or axes along which the convolution is computed.
        Default is the last N axes of the highest-rank input where N is the
        rank of the lowest-rank input.

    Returns
    -------
    planned_convolve(x, y)
        Planned convolution function.

    Raises
    ------
    ValueError
        If no function can be planned for the given arguments.
    """

    planned_function, x_transform_function, y_transform_function = \
        convolve2(plan_x, plan_y, mode=mode, axis=axis)

    def convolve_function(x, y):
        return planned_function(x_transform_function(x),
                                y_transform_function(y))

    return convolve_function


def convolve_const_x(x, plan_y, mode='full', axis=None):
    """Plan a function for convolving a constant array with another array.

    This planner distinguishes between several different cases:

        1. 1-D convolution of 1-D sequences or along single axis in N-D arrays
        2. N-D convolution of N-D sequences
        3. 1-D convolution along single axis in N-D array with 1-D sequence
        4. 1-D convolution of 1-D sequence along single axis in N-D array

        The shapes of the two inputs are usually sufficient to determine which
        case should be used. However, to get 1-D convolution along single axis
        in N-D arrays, 'axes' must be a single integer or a length 1 sequence.

    Parameters
    ----------
    x: Array-like
        First input (constant)
    plan_y: integer, shape or array-like
        Second input or it's shape or length.
    mode: Optional[str]
        A string indicating the output size.

        'full'
            The output is the full discrete linear convolution of the
            inputs. (Default)
        'valid'
            The output consists only of those elements that do not rely on
            zero-padding.
        'same'
            The output is the same size as plan_x, centered with respect to
            the 'full' output.
    axis: Optional[int or sequence of ints]
        The axis or axes along which the convolution is computed.
        Default is the last N axes of the highest-rank input where N is the
        rank of the lowest-rank input.

    Returns
    -------
    planned_convolve(y)
        Planned convolution function.

    Raises
    ------
    ValueError
        If no function can be planned for the given arguments.
    """

    planned_function, x_transform_function, y_transform_function = \
        convolve2(x, plan_y, mode=mode, axis=axis)
    x_fft = x_transform_function(x)

    def convolve_function(y):
        return planned_function(x_fft, y_transform_function(y))

    return convolve_function


def convolve_const_y(plan_x, y, mode='full', axis=None):
    """Plan a function for convolving an array with another constant array.

    This planner distinguishes between several different cases:

        1. 1-D convolution of 1-D sequences or along single axis in N-D arrays
        2. N-D convolution of N-D sequences
        3. 1-D convolution along single axis in N-D array with 1-D sequence
        4. 1-D convolution of 1-D sequence along single axis in N-D array

        The shapes of the two inputs are usually sufficient to determine which
        case should be used. However, to get 1-D convolution along single axis
        in N-D arrays, 'axes' must be a single integer or a length 1 sequence.

    Parameters
    ----------
    plan_x: integer, shape or Array-like
        First input or it's shape or length.
    y: Array-like
        Second input (constant)
    mode: Optional[str]
        A string indicating the output size.

        'full'
            The output is the full discrete linear convolution of the
            inputs. (Default)
        'valid'
            The output consists only of those elements that do not rely on
            zero-padding.
        'same'
            The output is the same size as plan_x, centered with respect to
            the 'full' output.
    axis: Optional[int or sequence of ints]
        The axis or axes along which the convolution is computed.
        Default is the last N axes of the highest-rank input where N is the
        rank of the lowest-rank input.

    Returns
    -------
    planned_convolve(x)
        Planned convolution function.

    Raises
    ------
    ValueError
        If no function can be planned for the given arguments.
    """

    planned_function, x_transform_function, y_transform_function = \
        convolve2(plan_x, y, mode=mode, axis=axis)
    y_fft = y_transform_function(y)

    def convolve_function(x):
        return planned_function(x_transform_function(x), y_fft)

    return convolve_function


def correlate2(plan_x, plan_y, mode='full', axis=None):
    """Plan a function for correlating two arrays.

    The planned function is returned along with separate input transform
    functions. This is intended for more advanced use cases, such as when
    precise control of transforms is required for memoization or other
    reasons. For most use cases, `correlate`, `correlate_const_x` or
    `correlate_const_y` are more appropriate.

    This planner distinguishes between several different cases:

        1. 1-D correlation of 1-D sequences or along single axis in N-D arrays
        2. N-D correlation of N-D sequences
        3. 1-D correlation along single axis in N-D array with 1-D sequence
        4. 1-D correlation of 1-D sequence along single axis in N-D array

        The shapes of the two inputs are usually sufficient to determine which
        case should be used. However, to get 1-D correlation along single axis
        in N-D arrays, 'axes' must be a single integer or a length 1 sequence.

    Parameters
    ----------
    plan_x : integer, shape or array-like
        First input sequence, it's shape or length.
    plan_y : integer, shape or array-like
        Second input sequence, it's shape or length.
    mode : Optional[str]
        A string indicating the output size.

        'full'
            The output is the full discrete linear correlation of the
            inputs. (Default)
        'valid'
            The output consists only of those elements that do not rely on
            zero-padding.
        'same'
            The output is the same size as plan_x, centered with respect to
            the 'full' output.
    axis : Optional[int or sequence of ints]
        The axis or axes along which the correlation is computed.
        Default is the last N axes of the highest-rank input where N is the
        rank of the lowest-rank input.

    Returns
    -------
    planned_correlate(x_transformed, y_transformed)
        Planned correlation function
    x_transform_function(x)
        Planned transform function for the first array
    y_transform_function(y)
        Planned transform function for the second array

    Raises
    ------
    ValueError
        If no function can be planned for the given arguments.
    """
    return _convolve_or_correlate(plan_x,
                                  plan_y,
                                  mode=mode,
                                  axis=axis,
                                  correlation=True)


def correlate(plan_x, plan_y, mode='full', axis=None):
    """Plan a function for correlating two arrays.

    This planner distinguishes between several different cases:

        1. 1-D correlation of 1-D sequences or along single axis in N-D arrays
        2. N-D correlation of N-D sequences
        3. 1-D correlation along single axis in N-D array with 1-D sequence
        4. 1-D correlation of 1-D sequence along single axis in N-D array

        The shapes of the two inputs are usually sufficient to determine which
        case should be used. However, to get 1-D correlation along single axis
        in N-D arrays, 'axes' must be a single integer or a length 1 sequence.

    Parameters
    ----------
    plan_x : integer, shape or array-like
        First input sequence, it's shape or length.
    plan_y : integer, shape or array-like
        Second input sequence, it's shape or length.
    mode : Optional[str]
        A string indicating the output size.

        'full'
            The output is the full discrete linear correlation of the
            inputs. (Default)
        'valid'
            The output consists only of those elements that do not rely on
            zero-padding.
        'same'
            The output is the same size as plan_x, centered with respect to
            the 'full' output.
    axis : Optional[int or sequence of ints]
        The axis or axes along which the correlation is computed.
        Default is the last N axes of the highest-rank input where N is the
        rank of the lowest-rank input.

    Returns
    -------
    planned_correlate(x, y)
        Planned correlation function.

    Raises
    ------
    ValueError
        If no function can be planned for the given arguments.
    """

    planned_function, x_transform_function, y_transform_function = \
        correlate2(plan_x, plan_y, mode=mode, axis=axis)

    def correlate_function(x, y):
        return planned_function(x_transform_function(x),
                                y_transform_function(y))

    return correlate_function


def correlate_const_x(x, plan_y, mode='full', axis=None):
    """Plan a function for correlating a constant array with another array.

    This planner distinguishes between several different cases:

        1. 1-D correlation of 1-D sequences or along single axis in N-D arrays
        2. N-D correlation of N-D sequences
        3. 1-D correlation along single axis in N-D array with 1-D sequence
        4. 1-D correlation of 1-D sequence along single axis in N-D array

        The shapes of the two inputs are usually sufficient to determine which
        case should be used. However, to get 1-D correlation along single axis
        in N-D arrays, 'axes' must be a single integer or a length 1 sequence.

    Parameters
    ----------
    x: Array-like
        First input (constant)
    plan_y: integer, shape or array-like
        Second input or it's shape or length.
    mode: Optional[str]
        A string indicating the output size.

        'full'
            The output is the full discrete linear correlation of the
            inputs. (Default)
        'valid'
            The output consists only of those elements that do not rely on
            zero-padding.
        'same'
            The output is the same size as plan_x, centered with respect to
            the 'full' output.
    axis: Optional[int or sequence of ints]
        The axis or axes along which the correlation is computed.
        Default is the last N axes of the highest-rank input where N is the
        rank of the lowest-rank input.

    Returns
    -------
    planned_correlate(y)
        Planned correlation function.

    Raises
    ------
    ValueError
        If no function can be planned for the given arguments.
    """

    planned_function, x_transform_function, y_transform_function = \
        correlate2(x, plan_y, mode=mode, axis=axis)
    x_fft = x_transform_function(x)

    def correlate_function(y):
        return planned_function(x_fft, y_transform_function(y))

    return correlate_function


def correlate_const_y(plan_x, y, mode='full', axis=None):
    """Plan a function for correlating an array with another constant array.

    This planner distinguishes between several different cases:

        1. 1-D correlation of 1-D sequences or along single axis in N-D arrays
        2. N-D correlation of N-D sequences
        3. 1-D correlation along single axis in N-D array with 1-D sequence
        4. 1-D correlation of 1-D sequence along single axis in N-D array

        The shapes of the two inputs are usually sufficient to determine which
        case should be used. However, to get 1-D correlation along single axis
        in N-D arrays, 'axes' must be a single integer or a length 1 sequence.

    Parameters
    ----------
    x: Array-like
        First input (constant)
    plan_y: integer, shape or array-like
        Second input or it's shape or length.
    mode: Optional[str]
        A string indicating the output size.

        'full'
            The output is the full discrete linear correlation of the
            inputs. (Default)
        'valid'
            The output consists only of those elements that do not rely on
            zero-padding.
        'same'
            The output is the same size as plan_x, centered with respect to
            the 'full' output.
    axis: Optional[int or sequence of ints]
        The axis or axes along which the correlation is computed.
        Default is the last N axes of the highest-rank input where N is the
        rank of the lowest-rank input.

    Returns
    -------
    planned_correlate(x)
        Planned correlation function.

    Raises
    ------
    ValueError
        If no function can be planned for the given arguments.
    """

    planned_function, x_transform_function, y_transform_function = \
        correlate2(plan_x, y, mode=mode, axis=axis)
    y_fft = y_transform_function(y)

    def correlate_function(x):
        return planned_function(x_transform_function(x), y_fft)

    return correlate_function
