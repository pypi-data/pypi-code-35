# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: psf.py
@date: 3/5/2019
@desc:
'''
import math

import attr
import numpy as np
import scipy.optimize as opt
from scipy import sparse

import srfnef as nef
from srfnef.typing import dataclass, funcclass
from srfnef.utils import tqdm

_threshold = 1e-16


@dataclass
class PointSource(nef.data_types.data_types.Image):
    pos: np.ndarray

    @property
    def psf_type(self):
        if self.pos[2] == 0.0:
            return 'xy'
        else:
            return 'z'


@dataclass
class FittedXY:
    data: np.ndarray = attr.ib(converter = lambda x: np.array(x).astype(np.float32))

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
    data: np.ndarray = attr.ib(converter = lambda x: np.array(x).astype(np.float32))

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
    fitted_xy: FittedXY
    fitted_z: FittedZ

    def __add__(self, other):
        new_fxy = self.fitted_xy + other.fitted_xy
        new_fz = self.fitted_z + other.fitted_z
        return self.__class__(new_fxy, new_fz)


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
                px, py, pz = np.floor((pnt_img.pos + pnt_img.center + pnt_img.size / 2) /
                                      pnt_img.unit_size).astype(np.int32)
                nx, ny, nz = pnt_img.shape
                img_avg = np.average(pnt_img.data[
                                     px - self.half_patch_range:
                                     min(px + self.half_patch_range + 1, nx),
                                     py - self.half_patch_range:
                                     min(py + self.half_patch_range + 1, ny),
                                     pz - self.half_slice_range:
                                     min(pz + self.half_slice_range + 1, nz)],
                                     axis = 2)
                y, x = np.meshgrid(
                    np.arange(py - self.half_patch_range,
                              min(py + self.half_patch_range + 1, ny)),
                    np.arange(px - self.half_patch_range,
                              min(px + self.half_patch_range + 1, nx)))
                out_xy = _fit_gaussian(img_avg, (x, y), mode = self.mode, mu = [px, py])
                out_xy[1:3] = np.sqrt(out_xy[1:3])
                if data_xy.size == 0:
                    data_xy = out_xy
                else:
                    data_xy = np.vstack((data_xy, out_xy))

            else:
                px, py, pz = np.floor((pnt_img.pos + pnt_img.center + pnt_img.size / 2) /
                                      pnt_img.unit_size).astype(np.int32)
                nx, ny, nz = pnt_img.shape

                img_avg = np.average(pnt_img.data[
                                     px - self.half_slice_range:
                                     min(px + self.half_slice_range + 1, nx),
                                     py - self.half_slice_range:
                                     min(py + self.half_slice_range + 1, ny),
                                     pz - self.half_patch_range:
                                     min(pz + self.half_patch_range + 1, nz)],
                                     axis = (0, 1))
                z = np.arange(pz - self.half_patch_range,
                              min(pz + self.half_patch_range + 1, nz))
                out_z = _fit_gaussian(img_avg, z, mode = 'fit_mu', mu = pz)
                out_z[1] = np.sqrt(out_z[1])
                if data_z.size == 0:
                    data_z = out_z
                else:
                    data_z = np.vstack((data_z, out_z))

        fxy = FittedXY(data_xy)
        fz = FittedZ(data_z)
        return fxy, fz


def _gaussian_1d(amp, sig2, mu):
    return lambda x: amp * np.exp(-(x - mu) ** 2 / 2 / sig2)


def _gaussian_2d(amp, sigx2, sigy2, mux, muy):
    return lambda x, y: amp * np.exp(-(x - mux) ** 2 / 2 / sigx2) * \
                        np.exp(-(y - muy) ** 2 / 2 / sigy2)


def _gaussian_3d(amp, sigx2, sigy2, sigz2, mux, muy, muz):
    return lambda x, y, z: amp * np.exp(-(x - mux) ** 2 / 2 / sigx2) * \
                           np.exp(-(y - muy) ** 2 / 2 / sigy2) * \
                           np.exp(-(z - muz) ** 2 / 2 / sigz2)


def _gaussian_1d_fix_mu(amp, sig2):
    return lambda x: amp * np.exp(-x ** 2 / 2 / sig2)


def _gaussian_2d_fix_mu(amp, sigx2, sigy2):
    return lambda x, y: amp * np.exp(-x ** 2 / 2 / sigx2) * \
                        np.exp(-y ** 2 / 2 / sigy2)


def _gaussian_3d_fix_mu(amp, sigx2, sigy2, sigz2):
    return lambda x, y, z: amp * np.exp(-x ** 2 / 2 / sigx2) * \
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


@dataclass
class KernelXY:
    data: sparse.coo_matrix


@dataclass
class KernelZ:
    data: np.ndarray


@funcclass
class PSFMaker:
    fitter: PsfFitter

    def __call__(self, pnt_img_path):
        print("step 1/4: fitting parameters...")
        fitted_xy, fitted_z = self.fitter(pnt_img_path)
        _pnt_img = nef.load(pnt_img_path[0])
        shape, unit_size = _pnt_img.shape, _pnt_img.unit_size

        print("step 2/4: making xy kernel...")
        kernel_xy = self.xy_main(fitted_xy, shape[0:2], unit_size[0:2])

        print("step 3/4: making z kernel...")
        kernel_z = self.z_main(fitted_z, shape[2], unit_size[2])
        print("step 4/4: generating psf efficiency map...")
        return kernel_xy, kernel_z
        # self.map_process(map_config)
        # print("Task complete!")

    def find_xy_kernel_max_sum(self, kernel_samples):
        kernel_sum = np.sum(np.sum(kernel_samples, axis = 0), axis = 0)
        max_value = np.max(kernel_sum)
        print('max kernel xy sum value', max_value)
        return max_value

    def find_z_kernel_max_sum(self, kernel_samples):
        kernel_sum = np.sum(kernel_samples, axis = 0)
        max_value = np.max(kernel_sum)
        print('max kernel z sum value', max_value)
        return max_value

    def make_meshgrid(self, grid, voxsize):
        nx, ny = grid[0], grid[1]
        ix, iy = voxsize[0], voxsize[1]
        sx, sy = ix * nx, iy * ny
        x = np.linspace((-sx + ix) / 2, (sx - ix) / 2, nx)
        y = np.linspace((-sy + iy) / 2, (sy - iy) / 2, ny)
        xv, yv = np.meshgrid(x, y, indexing = 'ij')
        return xv, yv

    def make_polargrid(self, xmesh, ymesh):
        rmesh = np.sqrt(xmesh ** 2 + ymesh ** 2)
        pmesh = np.arctan2(ymesh, xmesh) * 180 / np.pi
        return rmesh, pmesh

    def locate_kernel(self, sampled_kernels, x_range, r):
        '''
        choose a approximated kernel for a mesh.

        Args:
            sampled_kernels: interpolated kernel parameter array
            x_max: the max x position of kernel samples.
            r_max: the radial distance of a pixel to the origin.

        Returns:
            A kernel image generated according to the samples.
        '''
        # kernel_image = sampled_kernels[:, :, int(
        #     round(r/(x_range/(sampled_kernels.shape[2]-1))))]
        # return kernel_image

        nb_samples = sampled_kernels.shape[2]
        interval = (x_range) / (nb_samples - 1)
        index = int(round((r) / interval))

        if index >= nb_samples:
            #         print("index {} is out of sample domain.".format(index))
            kernel_image = np.zeros((sampled_kernels.shape[0], sampled_kernels.shape[1]))
        else:
            #         print("index:", index)
            kernel_image = sampled_kernels[:, :, index]
        return kernel_image

    def rotate_kernel(self, kernel_image, angle):
        '''
        rotate an 2D kernel in X-Y plane.
        Args:
            kernel_image: input kernel to be rotated
            angle: the rotation angle
        Returns:
            rotated kernel
        '''
        from scipy import ndimage
        img = kernel_image
        img_r = ndimage.interpolation.rotate(img, angle)
        shape0 = np.array(img.shape)
        shape1 = np.array(img_r.shape)
        # calculate the valid central part of kernel
        istart = np.round((shape1 - shape0) / 2)
        iend = shape0 + istart
        img_r = img_r[int(istart[0]):int(iend[0]), int(istart[1]):int(iend[1])]
        return img_r

    def make_xy_kernel(self, xmesh, ymesh, grid, x_range, kernel_samples, epsilon = 1e-4):
        rmesh, pmesh = self.make_polargrid(xmesh, ymesh)
        # import time
        nx, ny = grid[0], grid[1]
        row, col, data = [], [], []
        # start = time.time()
        kernel_max = self.find_xy_kernel_max_sum(kernel_samples)
        for i in tqdm(range(nx)):
            for j in range(ny):
                irow = j + i * ny
                ir, ip = rmesh[i, j], pmesh[i, j]
                original_kernel = self.locate_kernel(kernel_samples, x_range, ir)
                kernel = self.rotate_kernel(original_kernel, ip)
                kernel = kernel / kernel_max
                kernel[kernel < epsilon] = 0.0
                kernel_flat = kernel.reshape((-1))
                from scipy import sparse
                spa_kernel = sparse.coo_matrix(kernel_flat)
                nb_ele = spa_kernel.data.size
                if nb_ele > 0:
                    row = np.append(row, [irow] * nb_ele)
                    col = np.append(col, spa_kernel.col)
                    data = np.append(data, spa_kernel.data)
        return np.array([row, col, data])

    def compute_sample_kernels(self, kernel_array, xmesh, ymesh):
        '''
        Compute the all the kernel images of sample points.

        Args:
            kernel_para: kernel parameters to decide the distribution.
            xmesh: the meshgrid in x axis
            ymesh: the meshgrid in y axis

        Returns:

        '''
        nb_samples = len(kernel_array)
        grid = xmesh.shape
        kernel_images = np.zeros((grid[0], grid[1], nb_samples))
        for k in tqdm(range(nb_samples)):
            a = kernel_array[k, 0]
            ux = kernel_array[k, 1]
            sigx = kernel_array[k, 2]
            uy = kernel_array[k, 3]
            sigy = kernel_array[k, 4]
            for i in range(grid[0]):
                for j in range(grid[1]):
                    kernel_images[i, j, k] = a * np.exp(-(xmesh[i, j] - ux) ** 2 / (
                            2 * sigx ** 2) - (ymesh[i, j] - uy) ** 2 / (2 * sigy ** 2))
        return kernel_images

    def compensate_kernel(self, kernel_array, factor, xrange):
        '''
        The experimental xy_kernel parameters were corase along the x axis.
        Interpolate the kernel parameters in the whole range.

        Args:
            kernel_array: kerenl parameters to be interpolated.
            factor: scale ratio to be refined.
            xrange: the x axis range of kernel.
        Returns:
            An interpolated kernel parameter array.
        '''
        from scipy import interpolate
        nb_samples = len(kernel_array)
        nb_new_samples = int(nb_samples * factor)
        x = np.linspace(0, xrange, nb_samples)
        nb_columns = kernel_array.shape[1]

        kernel_new = np.zeros([nb_new_samples, nb_columns])
        for i_column in range(nb_columns):
            y = kernel_array[:, i_column]
            f = interpolate.interp1d(x, y)
            xnew = np.linspace(0, xrange, nb_new_samples)
            kernel_new[:, i_column] = f(xnew)
        return kernel_new

    def preprocess_xy_para(self, fitted_xy: FittedXY, grid, voxsize):
        axy, ux, uy, sigmax, sigmay = fitted_xy.axy, fitted_xy.ux, fitted_xy.uy, fitted_xy.sigx, \
                                      fitted_xy.sigy

        ux = (ux - math.ceil(grid[0] / 2)) * voxsize[0]
        sigmax = sigmax * voxsize[0]
        uy = (uy - math.ceil(grid[1] / 2)) * voxsize[1]
        sigmay = sigmay * voxsize[1]
        return np.vstack((axy, ux, sigmax, uy, sigmay)).T

    def xy_main(self, fitted_xy: FittedXY, grid, voxsize):
        kernel_array = self.preprocess_xy_para(fitted_xy, grid, voxsize)
        x_range = voxsize[0] * (kernel_array.shape[0] - 1)
        # step2: interpolation
        refined_kernel = self.compensate_kernel(kernel_array, 7, x_range)
        xmesh, ymesh = self.make_meshgrid(grid, voxsize)
        # step3: compute whole kernel
        kernel_samples = self.compute_sample_kernels(refined_kernel, xmesh, ymesh)

        kernel = self.make_xy_kernel(xmesh, ymesh, grid,
                                     x_range, kernel_samples, epsilon = 1e-4)
        row, col, data = kernel[0], kernel[1], kernel[2]
        row = row.astype(int)
        col = col.astype(int)

        kernel_xy = KernelXY(sparse.coo_matrix((data, (row, col)), shape = (
            grid[0] * grid[1], grid[0] * grid[1]), dtype = np.float32))
        return kernel_xy

    def compute_z_sample_kernels(self, kernel_samples, grid_z, zmesh):
        kernel_z = np.zeros((grid_z, grid_z), dtype = np.float32)
        for k in range(len(kernel_samples)):
            az = kernel_samples[k, 0]
            uz = kernel_samples[k, 1]
            sigz = kernel_samples[k, 2]

            for i in range(grid_z):
                kernel_z[i, k] = az * np.exp(-(zmesh[i] - uz) ** 2 / (2 * sigz ** 2))

        kernel_max = self.find_z_kernel_max_sum(kernel_z)
        return kernel_z / kernel_max

    def preprocess_z_para(self, fitted_z: FittedZ, grid_z, voxsize_z):
        az, uz, sigz = fitted_z.az, (fitted_z.uz - math.ceil(
            grid_z / 2)) * voxsize_z, fitted_z.sigz * voxsize_z

        az_neg = np.flipud(az[1:])
        uz_neg = -np.flipud(uz[1:])
        sigmaz_neg = np.flipud(sigz[1:])

        compen_len = int((grid_z - len(az) * 2 + 1) / 2)

        az = np.hstack(
            ([0.0] * compen_len, az_neg, az, [0.0] * compen_len))
        uz = np.hstack(
            ([0.0] * compen_len, uz_neg, uz, [0.0] * compen_len))
        sigmaz = np.hstack(
            ([1.0] * compen_len, sigmaz_neg, sigz, [1.0] * compen_len))

        return np.vstack((az, uz, sigmaz)).T

    def z_main(self, fitted_z: FittedZ, grid_z, voxsize_z):
        zmesh = np.linspace((-voxsize_z * (grid_z - 1)) / 2,
                            (voxsize_z * (grid_z - 1)) / 2, grid_z)
        kernel_samples = self.preprocess_z_para(fitted_z, grid_z, voxsize_z)
        kernel_z = self.compute_z_sample_kernels(kernel_samples, grid_z, zmesh)
        return KernelZ(kernel_z)
    #
    #
    # def map_process(cls, kernel_xy0, kernel_z0, emap):
    #     import scipy.io as sio
    #     from scipy import sparse
    #     kernel_xy = kernel_xy0.data
    #     # print(kernel_xy)
    #     kernel_z = kernel_z0.data
    #     effmap = np.load(config.map_path)
    #     # print('max effmap value', np.max(effmap))
    #     # print('min effmap value', np.min(effmap))
    #     # mask = effmap >1e5
    #     # effmap[effmap > 700] = 0
    #
    #     effmap[effmap >= 1] = 1 / effmap[effmap >= 1]
    #     # print('max effmap value', np.max(effmap))
    #     # print('min effmap value', np.min(effmap))
    #     # effmap[effmap <= 1e-7] = 0
    #     grid = effmap.shape
    #     effmap_reshaped = effmap.reshape((-1, grid[2]))
    #
    #     z_effmap = np.matmul(effmap_reshaped, kernel_z)
    #     # kernel_xy transpose
    #     kernel_xy = sparse.coo_matrix((kernel_xy.data, (kernel_xy.col, kernel_xy.row)),
    #                                   shape = (grid[0] * grid[1], grid[0] * grid[1]),
    #                                   dtype = np.float32)
    #
    #     # print(kernel_xy)
    #     psf_effmap = kernel_xy.dot(z_effmap)
    #
    #     # z_effmap = z_effmap.reshape(grid)
    #     # z_effmap = z_effmap/np.max(z_effmap)
    #     # print('max psfz effmap value', np.max(z_effmap))
    #     # print('min psfz effmap value', np.min(z_effmap))
    #     # z_effmap[z_effmap <= 1e-7] = 0
    #     # z_effmap[z_effmap>1e-7] = 1/z_effmap[z_effmap>1e-7]
    #     # print('max psfz effmap value', np.max(z_effmap))
    #     # print('min psfz effmap value', np.min(z_effmap))
    #
    #     psf_effmap = psf_effmap.reshape(grid)
    #
    #     psf_effmap = psf_effmap / np.max(psf_effmap)
    #     # print('max psf effmap value', np.max(psf_effmap))
    #     # print('min psf effmap value', np.min(psf_effmap))
    #     psf_effmap[psf_effmap <= config.epsilon] = 0
    #     psf_effmap[psf_effmap <= config.epsilon] = 0
    #     psf_effmap[psf_effmap > config.epsilon] = 1 / psf_effmap[psf_effmap > config.epsilon]
    #     print('max psf effmap value', np.max(psf_effmap))
    #     print('min psf effmap value', np.min(psf_effmap))
    #
    #     # effmap[effmap> 1e-7] = 1/effmap[effmap> 1e-7]
    #
    #     # np.save('exp_short_siddon_map_psfz.npy', z_effmap)
    #     np.save(config.psf_map_path, psf_effmap)

#
# from srfnef.data_types import TYPE_BIND
#
# TYPE_BIND.update({'PointSource': PointSource})
