# -*- coding: utf-8 -*-
"""
planfftw provides Julia-inspired function planners for FFT and FFT-based
functions.  If available, the planned functions use `pyfftw` as a
backend for great good. If not, automatic fallback to `scipy.fftpack`
and `numpy` is provided.
"""

from .planners import (fft,
                       fft_pair,
                       rfft,
                       rfft_pair,
                       fftn,
                       fftn_pair,
                       rfftn,
                       rfftn_pair,
                       ifft,
                       ifft_pair,
                       irfft,
                       irfft_pair,
                       ifftn,
                       ifftn_pair,
                       irfftn,
                       irfftn_pair,
                       firfilter,
                       firfilter2,
                       firfilter_const_filter,
                       firfilter_const_signal,
                       correlate,
                       correlate2,
                       correlate_const_x,
                       correlate_const_y,
                       convolve,
                       convolve2,
                       convolve_const_x,
                       convolve_const_y)

# clean up namespace
del planners

__version__ = '1.0'
