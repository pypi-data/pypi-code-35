#!usr/bin/env python

import pyfftw
import numpy as np

from . import _utils


def _dtypes(a_dtype):
    if a_dtype == "float32":
        untransformed_dtype = "float32"
        transformed_dtype = "complex64"
    elif a_dtype == "complex64":
        untransformed_dtype = "complex64"
        transformed_dtype = "complex64"
    elif a_dtype == "complex128":
        untransformed_dtype = "complex128"
        transformed_dtype = "complex128"
    else:
        untransformed_dtype = "float64"
        transformed_dtype = "complex128"

    return untransformed_dtype, transformed_dtype


def _inverse_dtypes(a_dtype):
    if a_dtype in ("complex64", "float32"):
        untransformed_dype = "float32"
        transformed_dtype = "complex64"
    else:
        untransformed_dype = "float64"
        transformed_dtype = "complex128"

    return untransformed_dype, transformed_dtype


def _fft_shape(a, nfft, axis):
    shape = _utils.get_shape(a)
    n = shape[axis]

    # Set up pyfftw shapes
    if nfft is None:
        nfft = shape[axis]
    else:
        shape = list(shape)
        shape[axis] = nfft

    return shape, n, nfft


def _fftn_shape(a, shape, axes):
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

    untransformed_shape = list(a_shape)
    for k, axis in enumerate(axes):
        untransformed_shape[axis] = shape[k]

    return a_shape, axes, untransformed_shape


def _irfft_shape(a, nfft, axis):
    shape = _utils.get_shape(a)
    n = 2*(shape[axis] - 1)

    # Set up pyfftw shapes
    if nfft is None:
        nfft = n
    else:
        shape = list(shape)
        shape[axis] = nfft

    u_shape = tuple(_utils.replace(shape, axis, nfft))
    v_shape = tuple(_utils.replace(shape, axis, nfft//2 + 1))

    return u_shape, v_shape, n, nfft


def _irfftn_shape(a, shape, axes):
    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = [n for n in a_shape]
            shape[-1] = 2*(shape[-1] - 1)
        else:
            shape = [a_shape[axis] for axis in axes]
            shape[axes[-1]] = 2*(shape[axes[-1]] - 1)
    else:
        shape = list(shape)

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
    u_shape = list(a_shape)
    v_shape = list(a_shape)

    for n, axis in zip(range(len(axes)), axes):
        u_shape[axis] = shape[n]
        v_shape[axis] = shape[n]

    v_shape[axes[-1]] = v_shape[axes[-1]]//2 + 1

    return



def _fft_preparations(a, nfft, axis, real_valued=False):
    """Common preparations for FFT planners."""
    shape, n, nfft = _fft_shape(a, nfft, axis)
    untransformed_dtype, transformed_dtype = _dtypes(np.asarray(a).dtype.name)
    if real_valued is True:
        if not untransformed_dtype.startswith("float"):
            raise TypeError("Cannot plan a real-valued FFT of a "
                            "complex-valued array")
        transformed_shape = _utils.replace(shape, axis, nfft//2 + 1)
    else:
        untransformed_dtype = transformed_dtype
        transformed_shape = shape

    # Set up input and output arrays and FFT object
    u = pyfftw.empty_aligned(shape, dtype=untransformed_dtype)
    v = pyfftw.empty_aligned(transformed_shape, dtype=transformed_dtype)

    return shape, u, v, n, nfft


def _ifft_preparations(a, nfft, axis, real_valued=False):
    """Common preparations for IFFT planners."""
    untransformed_dtype, transformed_dtype = \
        _inverse_dtypes(np.asarray(a).dtype.name)
    if real_valued is True:
        u_shape, v_shape, n, nfft = _irfft_shape(a, nfft, axis)
    else:
        u_shape, n, nfft = _fft_shape(a, nfft, axis)
        v_shape = u_shape
        untransformed_dtype = transformed_dtype

    u = pyfftw.empty_aligned(u_shape, dtype=untransformed_dtype)
    v = pyfftw.empty_aligned(v_shape, dtype=transformed_dtype)

    return v_shape, n, nfft, u, v


def _fftn_preparations(a, shape, axes, real_valued=False):
    """Common preparations for N-dimensional FFT planners."""
    a_shape, axes, untransformed_shape = _fftn_shape(a, shape, axes)
    untransformed_dtype, transformed_dtype = _dtypes(np.asarray(a).dtype.name)
    if real_valued is True:
        if not untransformed_dtype.startswith("float"):
            raise TypeError("Cannot plan a real-valued FFT of a "
                            "complex-valued array")
        transformed_shape = untransformed_shape.copy()
        transformed_shape[axes[-1]] = transformed_shape[axes[-1]]//2 + 1
    else:
        untransformed_dtype = transformed_dtype
        transformed_shape = untransformed_shape

    u = pyfftw.empty_aligned(untransformed_shape, dtype=untransformed_dtype)
    v = pyfftw.empty_aligned(transformed_shape, dtype=transformed_dtype)

    return a_shape, axes, u, v, untransformed_shape


def _irfftn_preparations(a, shape, axes):
    untransformed_dtype, transformed_dtype = _dtypes(np.asarray(a).dtype.name)

    a_shape = _utils.get_shape(a)
    n_dim = len(a_shape)

    if shape is None:
        if axes is None:
            shape = [n for n in a_shape]
            shape[-1] = 2*(shape[-1] - 1)
        else:
            shape = [a_shape[axis] for axis in axes]
            shape[axes[-1]] = 2*(shape[axes[-1]] - 1)
    else:
        shape = list(shape)

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
    u_shape = list(a_shape)
    v_shape = list(a_shape)

    for n, axis in zip(range(len(axes)), axes):
        u_shape[axis] = shape[n]
        v_shape[axis] = shape[n]

    v_shape[axes[-1]] = v_shape[axes[-1]]//2 + 1

    # Set up slices
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, v_shape[axis])

    # Set data types
    if np.asarray(a).dtype.name in ('float32', 'int32', 'complex64'):
        dtype = 'float32'
        fft_dtype = 'complex64'
    else:
        dtype = 'float64'
        fft_dtype = 'complex128'

    u = pyfftw.empty_aligned(u_shape, dtype=dtype)
    v = pyfftw.empty_aligned(v_shape, dtype=fft_dtype)

    return a_shape, v_shape, axes, slices, u, v


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
    shape, u, v, n, nfft = _fft_preparations(a, nfft, axis)
    fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

    # Define fft function
    if n == nfft:
        def planned_fft(x):
            u[:] = x
            return fft_obj().copy()

    elif n < nfft:
        def planned_fft(x):
            u[:] = _utils.pad_array(x, shape)
            return fft_obj().copy()

    else:
        slices = tuple(_utils.replace([slice(None)]*len(shape),
                                      axis,
                                      slice(None, nfft)))

        def planned_fft(x):
            u[:] = x[tuple(slices)]
            return fft_obj().copy()

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
    shape, u, v, n, nfft = _fft_preparations(a, nfft, axis)
    fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

    # Define fft function
    if n == nfft:
        def planned_fft(x):
            u[:] = x
            return fft_obj().copy()

    elif n < nfft:
        def planned_fft(x):
            u[:] = _utils.pad_array(x, shape)
            return fft_obj().copy()

    else:
        slices = tuple(_utils.replace([slice(None)]*len(shape),
                                      axis,
                                      slice(None, nfft)))

        def planned_fft(x):
            u[:] = x[tuple(slices)]
            return fft_obj().copy()

    # Define ifft function
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD',
                           axes=(axis,))

    if n > nfft:
        raise ValueError("NFFT must be at least equal to signal "
                         "length when returning an FFT pair.")

    elif n < nfft and crop_ifft:
        slices = tuple(_utils.replace([slice(None)]*len(shape),
                                      axis,
                                      slice(None, n)))

        def planned_ifft(x):
            v[:] = x
            return ifft_obj().copy()[tuple(slices)]

    else:
        def planned_ifft(x):
            v[:] = x
            return ifft_obj().copy()

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
    shape, u, v, n, nfft = _fft_preparations(a, nfft, axis, real_valued=True)

    # Set up slices and pyfftw shapes
    fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

    # Define fft function
    if n == nfft:
        def planned_rfft(x):
            u[:] = x
            return fft_obj().copy()

    elif n < nfft:
        def planned_rfft(x):
            u[:] = _utils.pad_array(x, shape)
            return fft_obj().copy()

    else:
        slices = tuple(_utils.replace([slice(None)]*len(shape),
                                      axis,
                                      slice(None, nfft)))

        def planned_rfft(x):
            u[:] = x[tuple(slices)]
            return fft_obj().copy()

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
    shape, u, v, n, nfft = _fft_preparations(a, nfft, axis, real_valued=True)

    # Set up slices and pyfftw shapes
    fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

    # Define fft function
    if n == nfft:
        def planned_rfft(x):
            u[:] = x
            return fft_obj().copy()

    elif n < nfft:
        def planned_rfft(x):
            u[:] = _utils.pad_array(x, shape)
            return fft_obj().copy()

    else:
        slices = tuple(_utils.replace([slice(None)]*len(shape),
                                      axis,
                                      slice(None, nfft)))

        def planned_rfft(x):
            u[:] = x[tuple(slices)]
            return fft_obj().copy()

    # Define ifft function
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD',
                           axes=(axis,))

    if n > nfft:
        raise ValueError("NFFT must be at least equal to signal "
                         "length when returning an FFT pair.")

    elif n < nfft and crop_ifft:
        slices = tuple(_utils.replace([slice(None)]*len(shape),
                                      axis,
                                      slice(None, n)))

        def planned_irfft(x):
            v[:] = x
            return ifft_obj().copy()[tuple(slices)]

    else:
        def planned_irfft(x):
            v[:] = x
            return ifft_obj().copy()

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
    a_shape, axes, u, v, fft_shape = _fftn_preparations(a, shape, axes)
    n_dim = len(a_shape)

    # Set up slices
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, fft_shape[axis])

    fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    # Define fft function
    if has_smaller_axis and has_larger_axis:
        def planned_fftn(x):
            u[:] = _utils.pad_array(x[tuple(slices)], fft_shape)
            return fft_obj().copy()

    elif has_larger_axis:
        def planned_fftn(x):
            u[:] = x[tuple(slices)]
            return fft_obj().copy()

    elif has_smaller_axis:
        def planned_fftn(x):
            u[:] = _utils.pad_array(x, fft_shape)
            return fft_obj().copy()

    else:
        def planned_fftn(x):
            u[:] = x
            return fft_obj().copy()

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
    a_shape, axes, u, v, fft_shape = _fftn_preparations(a, shape, axes)
    n_dim = len(a_shape)

    # Set up slices
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, fft_shape[axis])

    fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    # Define fft function
    if has_smaller_axis and has_larger_axis:
        def planned_fftn(x):
            u[:] = _utils.pad_array(x[tuple(slices)], fft_shape)
            return fft_obj().copy()

    elif has_larger_axis:
        def planned_fftn(x):
            u[:] = x[tuple(slices)]
            return fft_obj().copy()

    elif has_smaller_axis:
        def planned_fftn(x):
            u[:] = _utils.pad_array(x, fft_shape)
            return fft_obj().copy()

    else:
        def planned_fftn(x):
            u[:] = x
            return fft_obj().copy()

    # Define ifftn function
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=axes)

    if has_larger_axis:
        raise ValueError("Number of FFT points must be equal to or greater"
                         "than the signal length for each axis when "
                         "returning an FFT pair")

    elif has_smaller_axis and crop_ifft:
        for axis in axes:
            slices[axis] = slice(0, a_shape[axis])

        def planned_ifftn(x):
            v[:] = x
            return ifft_obj().copy()[tuple(slices)]
    else:
        def planned_ifftn(x):
            v[:] = x
            return ifft_obj().copy()

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
    a_shape, axes, u, v, fft_shape = \
        _fftn_preparations(a, shape, axes, real_valued=True)
    n_dim = len(a_shape)
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, fft_shape[axis])

    fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    # Define fft function
    if has_smaller_axis and has_larger_axis:
        def planned_rfftn(x):
            u[:] = _utils.pad_array(x[tuple(slices)], fft_shape)
            return fft_obj().copy()

    elif has_larger_axis:
        def planned_rfftn(x):
            u[:] = x[tuple(slices)]
            return fft_obj().copy()

    elif has_smaller_axis:
        def planned_rfftn(x):
            u[:] = _utils.pad_array(x, fft_shape)
            return fft_obj().copy()

    else:
        def planned_rfftn(x):
            u[:] = x
            return fft_obj().copy()

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
    a_shape, axes, u, v, fft_shape = \
        _fftn_preparations(a, shape, axes, real_valued=True)
    n_dim = len(a_shape)
    slices = [slice(None)] * n_dim
    for axis in axes:
        slices[axis] = slice(0, fft_shape[axis])

    fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    # Define fft function
    if has_smaller_axis and has_larger_axis:
        def planned_rfftn(x):
            u[:] = _utils.pad_array(x[tuple(slices)], fft_shape)
            return fft_obj().copy()

    elif has_larger_axis:
        def planned_rfftn(x):
            u[:] = x[tuple(slices)]
            return fft_obj().copy()

    elif has_smaller_axis:
        def planned_rfftn(x):
            u[:] = _utils.pad_array(x, fft_shape)
            return fft_obj().copy()

    else:
        def planned_rfftn(x):
            u[:] = x
            return fft_obj().copy()

    # Define ifftn function
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=axes)

    if has_larger_axis:
        raise ValueError("Number of FFT points must be equal to or greater"
                         "than the signal length for each axis when "
                         "returning an FFT pair")

    elif has_smaller_axis and crop_ifft:
        for axis in axes:
            slices[axis] = slice(0, a_shape[axis])

        def planned_irfftn(x):
            v[:] = x
            return ifft_obj().copy()[tuple(slices)]
    else:
        def planned_irfftn(x):
            v[:] = x
            return ifft_obj().copy()

    return planned_rfftn, planned_irfftn


def _ifft(n, nfft, u, v, v_shape, axis):
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=(axis,))

    # Define ifft function
    if n == nfft:
        def planned_irfft(x):
            v[:] = x
            return ifft_obj().copy()

    elif n < nfft:
        def planned_irfft(x):
            v[:] = _utils.pad_array(x, v_shape)
            return ifft_obj().copy()

    else:
        slices = tuple(_utils.replace([slice(None)]*len(v_shape),
                                      axis,
                                      slice(0, nfft//2 + 1)))

        def planned_irfft(x):
            v[:] = x[tuple(slices)]
            return ifft_obj().copy()

    return planned_irfft


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
    shape, n, nfft, u, v = _ifft_preparations(a, nfft, axis)
    return _ifft(n, nfft, u, v, shape, axis)


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
    shape, n, nfft, u, v = _ifft_preparations(a, nfft, axis)
    planned_ifft = _ifft(n, nfft, u, v, shape, axis)

    # Define FFT function
    fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

    if n > nfft:
        raise ValueError("NFFT must be at least equal to signal length "
                         "when returning an FFT pair.")

    elif n < nfft and crop_fft:
        slices = _utils.replace([slice(None)]*len(shape), axis, slice(None, n))

        def planned_fft(x):
            u[:] = x
            return fft_obj().copy()[tuple(slices)]

    else:
        def planned_fft(x):
            u[:] = x
            return fft_obj().copy()

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
    v_shape, n, nfft, u, v = _ifft_preparations(a, nfft, axis, real_valued=True)
    return _ifft(n, nfft, u, v, v_shape, axis)


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
    v_shape, n, nfft, u, v = _ifft_preparations(a, nfft, axis, real_valued=True)
    planned_irfft = _ifft(n, nfft, u, v, v_shape, axis)

    # Define FFT function
    fft_obj = pyfftw.FFTW(u, v, direction='FFTW_FORWARD', axes=(axis,))

    if n <= nfft:
        def planned_rfft(x):
            u[:] = x
            return fft_obj().copy()
    else:
        raise ValueError("NFFT must be at least equal to signal length "
                         "when returning an FFT pair.")

    return planned_irfft, planned_rfft


def _ifftn(has_smaller_axis, has_larger_axis, slices, v_shape, u, v, axes):
    ifft_obj = pyfftw.FFTW(v, u, direction='FFTW_BACKWARD', axes=axes)

    # Define ifft function
    if has_smaller_axis and has_larger_axis:
        def planned_irfftn(x):
            v[:] = _utils.pad_array(x[tuple(slices)], v_shape)
            return ifft_obj().copy()

    elif has_larger_axis:
        def planned_irfftn(x):
            v[:] = x[tuple(slices)]
            return ifft_obj().copy()

    elif has_smaller_axis:
        def planned_irfftn(x):
            v[:] = _utils.pad_array(x, v_shape)
            return ifft_obj().copy()

    else:
        def planned_irfftn(x):
            v[:] = x
            return ifft_obj().copy()

    return planned_irfftn


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
    a_shape, axes, u, v, fft_shape = \
        _fftn_preparations(a, shape, axes)

    # Set up slices
    slices = [slice(None)]*len(a_shape)
    for axis in axes:
        slices[axis] = slice(0, fft_shape[axis])

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    return _ifftn(has_smaller_axis, has_larger_axis, slices, fft_shape,
                  u, v, axes)


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
    a_shape, axes, u, v, fft_shape = \
        _fftn_preparations(a, shape, axes)

    # Set up slices
    slices = [slice(None)]*len(a_shape)
    for axis in axes:
        slices[axis] = slice(0, fft_shape[axis])

    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, fft_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, fft_shape))

    planned_ifftn = _ifftn(has_smaller_axis, has_larger_axis, slices, fft_shape, u, v, axes)

    # Define fftn function
    fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

    if has_larger_axis:
        raise ValueError("Number of FFT points must be equal to or greater"
                         "than the signal length for each axis when "
                         "returning an FFT pair.")

    elif has_smaller_axis and crop_fft:
        for axis in axes:
            slices[axis] = slice(0, a_shape[axis])

        def planned_fftn(x):
            u[:] = x
            return fft_obj().copy()[tuple(slices)]

    else:
        def planned_fftn(x):
            u[:] = x
            return fft_obj().copy()

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
    a_shape, v_shape, axes, slices, u, v = _irfftn_preparations(a, shape, axes)
    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, v_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, v_shape))
    return _ifftn(has_smaller_axis, has_larger_axis, slices, v_shape, u, v, axes)


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
    a_shape, v_shape, axes, slices, u, v = _irfftn_preparations(a, shape, axes)
    has_smaller_axis = any(s1 < s2 for s1, s2 in zip(a_shape, v_shape))
    has_larger_axis = any(s1 > s2 for s1, s2 in zip(a_shape, v_shape))
    planned_irfftn = _ifftn(has_smaller_axis, has_larger_axis, slices, v_shape, u, v, axes)
    # Define ifftn function
    fft_obj = pyfftw.FFTW(u, v, direction="FFTW_FORWARD", axes=axes)

    if has_larger_axis:
        raise ValueError("Number of FFT points must be equal to or greater"
                         "than the signal length for each axis when "
                         "returning an FFT pair")

    else:
        def planned_rfftn(x):
            u[:] = x
            return fft_obj().copy()

    return planned_irfftn, planned_rfftn
