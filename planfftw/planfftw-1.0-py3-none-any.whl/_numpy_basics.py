#!usr/bin/env python

import numpy as np
try:
    from . import _utils
except ImportError:
    import _utils


def fft(a, nfft=None, axis=-1):
    """Plan a discrete Fourier transform function.

    Parameters
    ----------
    a : number, shape or array-like
        An input array, its shape or length.
    nfft : Optional[int]
        Number of FFT points. Default is input size along specified
        axis
    axis : Optional[int]
        Axis along which to perform the fft. Default is -1.

    Returns
    -------
    planned_fft(x)
        Planned fft function.
    """
    if nfft is None:
        shape = _utils.get_shape(a)
        nfft = shape[axis]

    # Define fft function
    def planned_fft(x):
        return np.fft.fft(x, nfft, axis)

    return planned_fft


def fft_pair(a, nfft=None, axis=-1, crop_ifft=False):
    """Plan a discrete Fourier transform function pair.

    Parameters
    ----------
    a : number, shape or array-like
        An input array, its shape or length.
    nfft : Optional[int]
        Number of FFT points. Default is input size along specified
        axis
    axis : Optional[int]
        Axis along which to perform the fft. Default is -1.
    crop_ifft : Optional[boolean]
        Indicates whether the planned ifft function should crop its
        output to match input size. Default is False.

    Returns
    -------
    planned_fft(x)
        Planned fft function.
    planned_ifft(x)
        Planned ifft function.
    """
    # Get shape
    shape = _utils.get_shape(a)
    n = shape[axis]

    # Set up slices and pyfftw shapes
    n_dim = len(shape)
    slices = [slice(None)] * n_dim

    if nfft is None:
        nfft = shape[axis]

    # Define fft function
    def planned_fft(x):
        return np.fft.fft(x, nfft, axis)

    if n > nfft:
        raise ValueError("NFFT must be at least equal to signal "
                         "length when returning an FFT pair.")

    elif n < nfft and crop_ifft:
        slices[axis] = slice(None, n)

        def planned_ifft(x):
            return np.fft.ifft(x, nfft, axis)[tuple(slices)]

    else:
        def planned_ifft(x):
            return np.fft.ifft(x, nfft, axis)

    return planned_fft, planned_ifft


def rfft(a, nfft=None, axis=-1):
    """Returns a planned function that computes the 1-D DFT of a real-valued
    sequence or array.

    Parameters
    ----------
    a : number, shape or array-like
        An input array, its shape or length.
    nfft : Optional[int]
        Number of FFT points. Default is input size along specified axis
    axis : Optional[int]
        Axis along which to perform the fft. Default is -1.

    Returns
    -------
    planned_rfft(x)
        Planned fft function.
    """
    if nfft is None:
        shape = _utils.get_shape(a)
        nfft = shape[axis]

    # Define fft function
    def planned_rfft(x):
        return np.fft.rfft(x, nfft, axis)

    return planned_rfft


def rfft_pair(a, nfft=None, axis=-1, crop_ifft=False):
    """Returns a planned function that computes the 1-D DFT of a real-valued
    sequence or array.

    Parameters
    ----------
    a : number, shape or array-like
        An input array, its shape or length.
    nfft : Optional[int]
        Number of FFT points. Default is input size along specified axis
    axis : Optional[int]
        Axis along which to perform the fft. Default is -1.
    crop_ifft : Optional[boolean]
        Indicates whether the planned ifft function should crop its
        output to match input size. Default is False.

    Returns
    -------
    planned_rfft(x)
        Planned fft function
    planned_irfft(x)
        Planned ifft function
    """
    # Get shape
    shape = _utils.get_shape(a)
    n = shape[axis]
    n_even = 1 - (n % 2)

    if nfft is None:
        nfft = shape[axis]

    # Define fft function
    def planned_rfft(x):
        return np.fft.rfft(x, nfft, axis)

    # Define ifft function
    if n > nfft:
        raise ValueError("NFFT must be at least equal to signal "
                         "length when returning an FFT pair.")

    elif n < nfft and crop_ifft:
        n_dim = len(shape)
        slices = [slice(None)] * n_dim
        slices[axis] = slice(None, n)
        slices = tuple(slices)

        def planned_irfft(x):
            return np.fft.irfft(x, nfft, axis)[slices]

    else:
        def planned_irfft(x):
            return np.fft.irfft(x, nfft, axis)


    return planned_rfft, planned_irfft


def fftn(a, shape=None, axes=None):
    """Returns a planned function that computes the N-D DFT of an array.

    Parameters
    ----------
    a : array-like or shape
        An input array or its shape
    shape : Optional[List[int]]
        Number of FFT points. Default is input size along specified axes
    axes : Optional[sequence of ints]
        Axes along which to perform the fft. Default is all axes.

    Returns
    -------
    planned_fftn(x)
        Planned fft function.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = a_shape
        else:
            shape = [a_shape[axis] for axis in axes]

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Define fft function
    def planned_fftn(x):
        return np.fft.fftn(x, shape, axes)

    return planned_fftn


def fftn_pair(a, shape=None, axes=None, crop_ifft=False):
    """Returns a planned function that computes the N-D DFT of an array.

    Parameters
    ----------
    a : array-like or shape
        An input array or its shape
    shape : Optional[List[int]]
        Number of FFT points. Default is input size along specified axes
    axes : Optional[sequence of ints]
        Axes along which to perform the fft. Default is all axes.
    crop_ifft : Optional[boolean]
        Indicates whether the planned ifft function should crop its output
        to match input size. Default is False.

    Returns
    -------
    planned_fftn(x)
        Planned fft function.
    planned_ifftn(x)
        Planned ifft function.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = a_shape
        else:
            shape = [a_shape[axis] for axis in axes]

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Compute FFT shape
    fft_shape = list(a_shape)
    for n, axis in zip(range(len(axes)), axes):
        fft_shape[axis] = shape[n]

    # Set up slices
    slices = [slice(None)] * n_dim

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    # Define fft function
    def planned_fftn(x):
        return np.fft.fftn(x, shape, axes)

    # Define ifftn function
    if has_larger_axis:
        raise ValueError("Number of FFT points must be equal to or greater"
                         "than the signal length for each axis when "
                         "returning an FFT pair")

    elif has_smaller_axis and crop_ifft:
        for axis in axes:
            slices[axis] = slice(0, a_shape[axis])

        def planned_ifftn(x):
            return np.fft.ifftn(x, shape, axes)[tuple(slices)]

    else:
        def planned_ifftn(x):
            return np.fft.ifftn(x, shape, axes)

    return planned_fftn, planned_ifftn


def rfftn(a, shape=None, axes=None):
    """Returns a planned function that computes the N-D DFT of a real-valued
    array.

    Parameters
    ----------
    a : array-like or shape
        An input array or its shape.
    shape : Optional[sequence of ints]
        Number of FFT points. Default is input size along specified axes
    axes : Optional[sequence of ints]
        Axes along which to perform the fft. Default is all axes.

    Returns
    -------
    planned_rfftn(x)
        Planned fft function.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = a_shape
        else:
            shape = [a_shape[axis] for axis in axes]

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Define fft function
    def planned_rfftn(x):
        return np.fft.rfftn(x, shape, axes)

    return planned_rfftn


def rfftn_pair(a, shape=None, axes=None, crop_ifft=False):
    """Returns a planned function that computes the N-D DFT of a real-valued
    array.

    Parameters
    ----------
    a : array-like or shape
        An input array or its shape.
    shape : Optional[sequence of ints]
        Number of FFT points. Default is input size along specified axes
    axes : Optional[sequence of ints]
        Axes along which to perform the fft. Default is all axes.
    crop_ifft : Optional[boolean]
        Indicates whether the planned ifft function should crop its output
        to match input size. Default is False.

    Returns
    -------
    planned_rfftn(x)
        Planned fft function.
    planned_irfftn(x)
        Planned ifft function.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = a_shape
        else:
            shape = [a_shape[axis] for axis in axes]

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Compute FFT shape
    fft_shape = list(a_shape)
    for n, axis in zip(range(len(axes)), axes):
        fft_shape[axis] = shape[n]

    # Set up slices
    slices = [slice(None)] * n_dim

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    # Define fft function
    def planned_rfftn(x):
        return np.fft.rfftn(x, shape, axes)[tuple(slices)]

    # Define ifftn function
    if has_larger_axis:
        raise ValueError("Number of FFT points must be equal to or greater"
                         "than the signal length for each axis when "
                         "returning an FFT pair")

    elif has_smaller_axis and crop_ifft:
        for axis in axes:
            slices[axis] = slice(0, a_shape[axis])

        def planned_irfftn(x):
            return np.fft.irfftn(x, shape, axes)[tuple(slices)]

    else:
        def planned_irfftn(x):
            return np.fft.irfftn(x, shape, axes)

    return planned_rfftn, planned_irfftn


def ifft(a, nfft=None, axis=-1):
    """Returns a planned function that computes the 1-D inverse DFT of a
    sequence or array.

    Parameters
    ----------
    a : number, shape or array-like
        An input array, its shape or length.
    nfft : Optional[int]
        Number of FFT points. Default is input size along specified axis
    axis : Optional[int]
        Axis along which to perform the fft. Default is -1.

    Returns
    -------
    planned_ifft(x)
        Planned ifft function.
    """
    if nfft is None:
        shape = _utils.get_shape(a)
        nfft = shape[axis]

    # Define ifft function
    def planned_ifft(x):
        return np.fft.ifft(x, nfft, axis)

    return planned_ifft


def ifft_pair(a, nfft=None, axis=-1, crop_fft=False):
    """Returns a planned function that computes the 1-D inverse DFT of a
    sequence or array.

    Parameters
    ----------
    a : number, shape or array-like
        An input array, its shape or length.
    nfft : Optional[int]
        Number of FFT points. Default is input size along specified axis
    axis : Optional[int]
        Axis along which to perform the fft. Default is -1.
    crop_fft : Optional[boolean]
        Indicates that the fft function should crop its output to match
        the shape of the input to the ifft function

    Returns
    -------
    planned_ifft(x)
        Planned ifft function.
    planned_fft(x)
        Planned fft function.
    """
    # Get shape
    shape = _utils.get_shape(a)
    n = shape[axis]

    # Set up slices and pyfftw shapes
    n_dim = len(shape)
    slices = [slice(None)] * n_dim

    if nfft is None:
        nfft = shape[axis]
    else:
        shape = list(shape)
        shape[axis] = nfft

    # Define ifft function
    def planned_ifft(x):
        return np.fft.ifft(x, nfft, axis)

    # Define fft function
    if n > nfft:
        raise ValueError("NFFT must be at least equal to signal length "
                         "when returning an FFT pair.")

    elif n < nfft and crop_fft:
        slices[axis] = slice(None, n)

        def planned_fft(x):
            return np.fft.fft(x, nfft, axis)[tuple(slices)]

    else:
        def planned_fft(x):
            return np.fft.fft(x, nfft, axis)

    return planned_ifft, planned_fft


def irfft(a, nfft=None, axis=-1):
    """Returns a planned function that computes the real-valued 1-D inverse DFT
    of a sequence or array.

    Parameters
    ----------
    a : number, shape or array-like
        An input array, its shape or length.
    nfft : Optional[int]
        Number of FFT points. Default is input size along specified axis
    axis : Optional[int]
        Axis along which to perform the fft. Default is -1.

    Returns
    -------
    planned_irfft(x)
        Planned ifft function.
    """
    shape = _utils.get_shape(a)
    n = 2*(shape[axis] - 1)

    if nfft is None:
        nfft = n

    # Define ifft function
    def planned_irfft(x):
        return np.fft.irfft(x, nfft, axis)

    return planned_irfft


def irfft_pair(a, nfft=None, axis=-1):
    """Returns a planned function that computes the real-valued 1-D inverse DFT
    of a sequence or array.

    Parameters
    ----------
    a : number, shape or array-like
        An input array, its shape or length.
    nfft : Optional[int]
        Number of FFT points. Default is input size along specified axis
    axis : Optional[int]
        Axis along which to perform the fft. Default is -1.

    Returns
    -------
    planned_irfft(x)
        Planned ifft function.
    planned_rfft(x)
        Planned fft function.
    """
    # Get shape
    shape = _utils.get_shape(a)
    n = 2*(shape[axis] - 1)

    # Set up slices and pyfftw shapes
    n_dim = len(shape)
    slices = [slice(None)] * n_dim

    if nfft is None:
        nfft = n

    # Define ifft function
    def planned_irfft(x):
        return np.fft.irfft(x, nfft, axis)

    # Define fft function
    if n == nfft:
        def planned_rfft(x):
            return np.fft.rfft(x, nfft, axis)

    elif n < nfft:
        slices[axis] = n

        def planned_rfft(x):
            return np.fft.rfft(x, nfft, axis)[slices]

    else:
        raise ValueError("NFFT must be at least equal to signal length "
                         "when returning an FFT pair.")

    return planned_irfft, planned_rfft


def ifftn(a, shape=None, axes=None):
    """Returns a planned function that computes the N-D DFT of an array.

    Parameters
    ----------
    a : array-like or shape
        An input array or its shape
    nfft : Optional[sequence of ints]
        Number of FFT points. Default is input size along specified axes
    axes : Optional[sequence of ints]
        Axes along which to perform the fft. Default is all axes.

    Returns
    -------
    planned_ifftn(x)
        Planned fft function.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = a_shape
        else:
            shape = [a_shape[axis] for axis in axes]

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Define ifft function
    def planned_ifftn(x):
        # scipy.fftpack.fftn doesn't handle mixed sign axes well
        return np.fft.ifftn(x, shape, axes)

    return planned_ifftn


def ifftn_pair(a, shape=None, axes=None, crop_fft=False):
    """Returns a planned function that computes the N-D DFT of an array.

    Parameters
    ----------
    a : array-like or shape
        An input array or its shape
    shape : Optional[sequence of ints]
        Number of FFT points. Default is input size along specified axes
    axes : Optional[sequence of ints]
        Axes along which to perform the fft. Default is all axes.
    crop_fft : Optional[boolean]
        Indicates that the fft function should crop its output to match
        the shape of the input to the ifft function

    Returns
    -------
    planned_ifftn(x)
        Planned fft function.
    planned_fftn(x)
        Planned ifft function.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = a_shape
        else:
            shape = [a_shape[axis] for axis in axes]

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Compute FFTW shape
    fft_shape = list(a_shape)
    for n, axis in zip(range(len(axes)), axes):
        fft_shape[axis] = shape[n]

    # Set up slices
    slices = [slice(None)] * n_dim

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    # Define ifft function
    def planned_ifftn(x):
        # scipy.fftpack.fftn doesn't handle mixed sign axes well
        return np.fft.ifftn(x, shape, axes)

    # Define fftn function
    if has_larger_axis:
        raise ValueError("Number of FFT points must be equal to or greater"
                         "than the signal length for each axis when "
                         "returning an FFT pair.")

    elif has_smaller_axis and crop_fft:
        for axis in axes:
            slices[axis] = slice(0, a_shape[axis])

        def planned_fftn(x):
            # scipy.fftpack.fftn doesn't handle mixed sign axes well
            return np.fft.fftn(x, shape, axes)[tuple(slices)]

    else:
        def planned_fftn(x):
            # scipy.fftpack.fftn doesn't handle mixed sign axes well
            return np.fft.fftn(x, shape, axes)

    return planned_ifftn, planned_fftn


def irfftn(a, shape=None, axes=None):
    """Returns a planned function that computes the N-D DFT of a real-valued
    array.

    Parameters
    ----------
    a : array-like or shape
        An input array or its shape.
    shape : Optional[sequence of ints]
        Number of FFT points. Default is input size along specified axes
    axes : Optional[sequence of ints]
        Axes along which to perform the fft. Default is all axes.

    Returns
    -------
    planned_irfftn(x)
        Planned ifft function.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = list(a_shape)
            shape[-1] = 2*(shape[-1] - 1)
        else:
            shape = [a_shape[axis] for axis in axes]
            shape[axes[-1]] = 2*(shape[axes[-1]] - 1)

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    # Define ifft function
    def planned_irfftn(x):
        # scipy.fftpack.fftn doesn't handle mixed sign axes well
        return np.fft.irfftn(x, shape, axes)

    return planned_irfftn


def irfftn_pair(a, shape=None, axes=None):
    """Returns a planned function that computes the N-D DFT of a real-valued
    array.

    Parameters
    ----------
    a : array-like or shape
        An input array or its shape.
    shape : Optional[sequence of ints]
        Number of FFT points. Default is input size along specified axes
    axes : Optional[sequence of ints]
        Axes along which to perform the fft. Default is all axes.

    Returns
    -------
    planned_irfftn(x)
        Planned ifft function.
    planned_rfftn(x)
        Planned fft function.
    """
    # Get shape of input
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = list(a_shape)
            shape[-1] = 2*(shape[-1] - 1)
        else:
            shape = [a_shape[axis] for axis in axes]
            shape[axes[-1]] = 2*(shape[axes[-1]] - 1)

    if axes is None:
        n_dim_s = len(shape)
        dim_diff = n_dim - n_dim_s
        axes = [k + dim_diff for k in range(n_dim_s)]

    # Make sure axes and shape are iterable
    if np.asarray(axes).ndim == 0:
        axes = (axes,)
    if np.asarray(shape).ndim == 0:
        shape = (shape,)

    a_shape_out = list(a_shape)
    a_shape_out[axes[-1]] = 2*(a_shape_out[axes[-1]] - 1)

    # Set up slices
    slices = [slice(None)] * n_dim

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape_out, shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape_out, shape))

    # Define ifft function
    def planned_irfftn(x):
        # scipy.fftpack.fftn doesn't handle mixed sign axes well
        return np.fft.irfftn(x, shape, axes)

    # Define fftn function
    if has_larger_axis:
        raise ValueError("Number of FFT points must be equal to or greater"
                         "than the signal length for each axis when "
                         "returning an FFT pair.")

    else:
        def planned_rfftn(x):
            # scipy.fftpack.fftn doesn't handle mixed sign axes well
            return np.fft.rfftn(x, shape, axes)

    return planned_irfftn, planned_rfftn

