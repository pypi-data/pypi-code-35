# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: psf_fitter.py
@date: 3/29/2019
@desc:
'''
import typing

import attr
import numpy as np
import scipy.optimize as opt

import srfnef as nef
from srfnef.typing import funcclass, dataclass

_threshold = 1e-16


@dataclass
class PointSource(nef.data_types.Image):
    pos: typing.List[float] = attr.ib(converter = np.array)

    @property
    def psf_type(self):
        if self.pos[2] == 0.0:
            return 'xy'
        else:
            return 'z'


@dataclass
class FittedXy:
    data: np.ndarray = attr.ib(converter = np.array)

    @property
    def axy(self):
        return self.data[:, 0]

    @property
    def sigx(self):
        return self.data[:, 1]

    @property
    def sigy(self):
        return self.data[:, 2]

    @property
    def ux(self):
        return self.data[:, 3]

    @property
    def uy(self):
        return self.data[:, 4]

    def __add__(self, other):
        new_data = np.vstack((self.data, other.data))
        return self.__class__(new_data)


@dataclass
class FittedZ:
    data: np.ndarray = attr.ib(converter = np.array)

    @property
    def az(self):
        return self.data[:, 0]

    @property
    def sigz(self):
        return self.data[:, 1]

    @property
    def uz(self):
        return self.data[:, 2]

    def __add__(self, other):
        new_data = np.vstack((self.data, other.data))
        return self.__class__(new_data)


@dataclass
class Fitted:
    fitted_xy: FittedXy
    fitted_z: FittedZ

    def __add__(self, other):
        new_fxy = self.fitted_xy + other.fitted_xy
        new_fz = self.fitted_z + other.fitted_z
        return self.__class__(new_fxy, new_fz)


def fitting_psf_xy(pnt_img, half_slice_range, half_patch_range, mode):
    px, py, pz = np.floor((pnt_img.pos + pnt_img.center + pnt_img.size / 2) /
                          pnt_img.unit_size).astype(np.int32)
    nx, ny, nz = pnt_img.shape
    img_avg = np.average(pnt_img.data[
                         max(px - half_patch_range, 0):
                         min(px + half_patch_range + 1, nx),
                         max(py - half_patch_range, 0):
                         min(py + half_patch_range + 1, ny),
                         max(pz - half_slice_range, 0):
                         min(pz + half_slice_range + 1, nz)],
                         axis = 2)
    x, y = np.meshgrid(
        (np.arange(max(px - half_patch_range, 0),
                   min(px + half_patch_range + 1, nx)) + 0.5) *
        pnt_img.unit_size[0] + pnt_img.center[0] - pnt_img.size[0] / 2,
        (np.arange(max(py - half_patch_range, 0),
                   min(py + half_patch_range + 1, ny)) + 0.5) *
        pnt_img.unit_size[1] + pnt_img.center[1] - pnt_img.size[1] / 2,
        indexing = 'ij'
    )
    out_xy = _fit_gaussian(img_avg, (x, y), mode = mode, mu = [pnt_img.pos[0], pnt_img.pos[1]])
    out_xy[0] = 1.0
    _dist_ones = _gaussian_2d(*out_xy)(x, y)
    _amp = np.sum(img_avg) / np.sum(_dist_ones)
    out_xy[0] = _amp
    return out_xy  # the sigma output is squared


def fitting_psf_z(pnt_img, half_slice_range, half_patch_range, mode):
    px, py, pz = np.floor((pnt_img.pos + pnt_img.center + pnt_img.size / 2) /
                          pnt_img.unit_size).astype(np.int32)
    nx, ny, nz = pnt_img.shape

    img_avg = np.average(pnt_img.data[
                         max(px - half_slice_range, 0):
                         min(px + half_slice_range + 1, nx),
                         max(py - half_slice_range, 0):
                         min(py + half_slice_range + 1, ny),
                         max(pz - half_patch_range, 0):
                         min(pz + half_patch_range + 1, nz)],
                         axis = (0, 1))
    z = (np.arange(max(pz - half_patch_range, 0),
                   min(pz + half_patch_range + 1, nz)) + 0.5) * \
        pnt_img.unit_size[2] + pnt_img.center[2] - pnt_img.size[2] / 2

    out_z = _fit_gaussian(img_avg, z, mode = mode, mu = pnt_img.pos[2])
    out_z[0] = 1.0
    _dist_ones = _gaussian_1d(*out_z)(z)
    _amp = np.sum(img_avg) / np.sum(_dist_ones)
    out_z[0] = _amp
    return out_z  # the sigma output is squared


@funcclass
class PsfFitter:
    half_slice_range: int
    half_patch_range: int
    mode: str

    def __call__(self, pnt_img_path):
        data_xy = np.array([])
        data_z = np.array([])

        print('fitting psf kernel parameters')
        for _path in nef.utils.tqdm(pnt_img_path):
            pnt_img = nef.load(_path)
            if pnt_img.psf_type == 'xy':
                out_xy = fitting_psf_xy(pnt_img, self.half_slice_range, self.half_patch_range,
                                        self.mode)
                if data_xy.size == 0:
                    data_xy = out_xy
                else:
                    data_xy = np.vstack((data_xy, out_xy))
            else:
                out_z = fitting_psf_z(pnt_img, self.half_slice_range, self.half_patch_range,
                                      self.mode)
                if data_z.size == 0:
                    data_z = out_z
                else:
                    data_z = np.vstack((data_z, out_z))

        fxy = FittedXy(data_xy)
        fz = FittedZ(data_z)
        return fxy, fz


def _gaussian_1d(amp, sig2, mu):
    return lambda x: amp / np.sqrt(2 * np.pi * sig2) * np.exp(-(x - mu) ** 2 / 2 / sig2)


def _gaussian_2d(amp, sigx2, sigy2, mux, muy):
    return lambda x, y: amp / np.sqrt(2 * np.pi * sigx2) \
                        / np.sqrt(2 * np.pi * sigy2) \
                        * np.exp(-(x - mux) ** 2 / 2 / sigx2) * \
                        np.exp(-(y - muy) ** 2 / 2 / sigy2)


def _gaussian_3d(amp, sigx2, sigy2, sigz2, mux, muy, muz):
    return lambda x, y, z: amp / np.sqrt(2 * np.pi * sigx2) \
                           / np.sqrt(2 * np.pi * sigy2) \
                           / np.sqrt(2 * np.pi * sigz2) \
                           * np.exp(-(x - mux) ** 2 / 2 / sigx2) * \
                           np.exp(-(y - muy) ** 2 / 2 / sigy2) * \
                           np.exp(-(z - muz) ** 2 / 2 / sigz2)


def _gaussian_1d_fix_mu(amp, sig2):
    return lambda x: amp / np.sqrt(2 * np.pi * sig2) * np.exp(-x ** 2 / 2 / sig2)


def _gaussian_2d_fix_mu(amp, sigx2, sigy2):
    return lambda x, y: amp / np.sqrt(2 * np.pi * sigx2) \
                        / np.sqrt(2 * np.pi * sigy2) \
                        * np.exp(-x ** 2 / 2 / sigx2) \
                        * np.exp(-y ** 2 / 2 / sigy2)


def _gaussian_3d_fix_mu(amp, sigx2, sigy2, sigz2):
    return lambda x, y, z: amp / np.sqrt(2 * np.pi * sigx2) \
                           / np.sqrt(2 * np.pi * sigy2) \
                           / np.sqrt(2 * np.pi * sigz2) \
                           * np.exp(-x ** 2 / 2 / sigx2) * \
                           np.exp(-y ** 2 / 2 / sigy2) * \
                           np.exp(-z ** 2 / 2 / sigz2)


def _fit_gaussian(data, pos, mode = None, **kwargs):
    ndim = len(pos)
    if ndim > 3:
        ndim = 1
    if ndim == 1:
        if 'mu' in kwargs.keys():
            kmu = kwargs['mu']
            mu = kmu[0] if isinstance(kmu, tuple) else kmu
        else:
            mu = 0
        if isinstance(pos, tuple):
            pos = pos[0]

        x, data = pos.ravel(), data.ravel()
        x = x[data > _threshold]
        data = data[data > _threshold]
        if mode == 'fix_mu':
            def _error_function(p):
                return np.ravel(_gaussian_1d_fix_mu(*p)(x - mu) - data)

            if 'initial_guess' in kwargs.keys():
                init = kwargs['initial_guess']
            else:
                init = [np.max(data), 1]
            p = opt.leastsq(_error_function, init)
            return np.append(p[0], [mu])
        elif mode == 'fit_mu':
            def _error_function(p):
                return np.ravel(_gaussian_1d(*p)(x) - data)

            if 'initial_guess' in kwargs.keys():
                init = kwargs['initial_guess']
            else:
                init = [np.max(data), 1, mu]
            p = opt.leastsq(_error_function, init)
            return p[0]

        else:
            raise NotImplementedError
    elif ndim == 2:
        if 'mu' in kwargs.keys():
            kmu = kwargs['mu']
            mux, muy = kmu[0], kmu[1]
        else:
            mux = muy = 0

        x, y, data = pos[0].ravel(), pos[1].ravel(), data.ravel()
        maxv = np.max(data)
        x = x[data > _threshold * maxv]
        y = y[data > _threshold * maxv]
        data = data[data > _threshold * maxv]

        if mode == 'fix_mu':
            def _error_function(p):
                return np.ravel(_gaussian_2d_fix_mu(*p)(x - mux, y - muy) - data)

            if 'initial_guess' in kwargs.keys():
                init = kwargs['initial_guess']
            else:
                init = [np.max(data), 1, 1]
            p = opt.leastsq(_error_function, init)

            return np.append(p[0], [mux, muy])
        elif mode == 'fit_mu':
            def _error_function(p):
                return np.ravel(_gaussian_2d(*p)(x, y) - data)

            if 'initial_guess' in kwargs.keys():
                init = kwargs['initial_guess']
            else:
                init = [1e6, 1, 1, mux, muy]
            p = opt.leastsq(_error_function, init)
            return p[0]
        else:
            raise NotImplementedError
    elif ndim == 3:
        if 'mu' in kwargs.keys():
            kmu = kwargs['mu']
            mux, muy, muz = kmu[0], kmu[1], kmu[2]
        else:
            mux = muy = muz = 0

        x, y, z, data = pos[0].ravel(), pos[1].ravel(), pos[2].ravel(), data.ravel()
        maxv = np.max(data)
        x = x[data > _threshold * maxv]
        y = y[data > _threshold * maxv]
        z = z[data > _threshold * maxv]
        data = data[data > _threshold * maxv]
        if mode == 'fix_mu':
            def _error_function(p):
                return np.ravel(_gaussian_3d_fix_mu(*p)(x - mux, y - muy, z - muz) - data)

            if 'initial_guess' in kwargs.keys():
                init = kwargs['initial_guess']
            else:
                init = [np.max(data), 1, 1, 1]
            p = opt.leastsq(_error_function, init)
            return np.append(p[0], [mux, muy, muz])
        elif mode == 'fit_mu':
            def _error_function(p):
                return np.ravel(_gaussian_3d(*p)(x, y, z) - data)

            if 'initial_guess' in kwargs.keys():
                init = kwargs['initial_guess']
            else:
                init = [np.max(data), 1, 1, 1, mux, muy, muz]
            p = opt.leastsq(_error_function, init)
            return p[0]

        else:
            raise NotImplementedError
    else:
        raise NotImplementedError
