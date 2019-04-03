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

import numpy as np
from scipy import interpolate
from scipy import sparse

import srfnef as nef
from srfnef.func_types import EmapMlem
from srfnef.typing import dataclass, funcclass
from srfnef.utils import tqdm
from .psf_fitter import FittedXy, FittedZ, PsfFitter

_threshold = 1e-16


@dataclass
class EmapMlemPsf(EmapMlem):
    pass


@dataclass
class KernelXy:
    data: sparse.coo_matrix


@dataclass
class KernelZ:
    data: np.ndarray


@funcclass
class PSFMaker:
    fitter: PsfFitter

    # kernel_xy: KernelXy = attr.ib(default = None)
    # kernel_z: KernelZ = attr.ib(default = None)
    # emap_mlem_psf: EmapMlemPsf = attr.ib(default = None)

    # def __call__(self, pnt_img_path, emap):
    #     print("step 1/4: fitting parameters...")
    #     fitted_xy, fitted_z = self.fitter(pnt_img_path)
    #     _pnt_img = nef.load(pnt_img_path[0])
    #     shape, unit_size = _pnt_img.shape, _pnt_img.unit_size
    #
    #     print("step 2/4: making xy kernel...")
    #     self.kernel_xy = self.xy_main(fitted_xy, shape[0:2], unit_size[0:2])
    #
    #     print("step 3/4: making z kernel...")
    #     self.kernel_z = self.z_main(fitted_z, shape[2], unit_size[2])
    #     print("step 4/4: generating psf efficiency map...")
    #     self.emap_mlem_psf = self.map_process(self.kernel_xy, self.kernel_z, emap)
    #     return self.emap_mlem_psf

    def __call__(self, fitted_xy: FittedXy, image: nef.data_types.Image):
        kernel_xy = self.xy_main(fitted_xy, image, half_patch_range = 5)
        # kernel_z = self.z_main(fitted_z, shape[2], unit_size[2])
        return kernel_xy

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
        pmesh = np.arctan2(ymesh, xmesh)
        return rmesh, pmesh

    def locate_kernel(self, x, y, sigx2, sigy2):
        ans = 1.0 / np.sqrt(2 * np.pi * sigx2) \
              / np.sqrt(2 * np.pi * sigy2) \
              * np.exp(-x ** 2 / 2 / sigx2) \
              * np.exp(-y ** 2 / 2 / sigy2)
        return ans / np.sum(ans)

    def rotate_image(self, img, angle):
        shape_ = img.shape
        x, y = np.arange(shape_[0]), np.arange(shape_[1])
        x1, y1 = np.meshgrid(x, y, indexing = 'ij')

    def rotate_kernel(self, img, angle):
        '''
        rotate an 2D kernel in X-Y plane.
        Args:
            img: input kernel to be rotated
            angle: the rotation angle
        Returns:
            rotated kernel
        '''
        from scipy import ndimage
        img_r = ndimage.interpolation.rotate(img, np.rad2deg(angle), reshape = False)
        # shape0 = np.array(img.shape)
        # shape1 = np.array(img_r.shape)
        # # calculate the valid central part of kernel
        # istart = np.round((shape1 - shape0) / 2).astype(int)
        # iend = (shape0 + istart).astype(int)
        # img_r = img_r[istart[0]:iend[0], istart[1]:iend[1]]
        # if not img.shape == img_r.shape:
        #     print(img.shape, img_r.shape, istart, iend, angle)
        #     raise ValueError
        return img_r

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

    def preprocess_xy_para(self, fitted_xy: FittedXy, grid, voxsize):
        axy, ux, uy, sigmax, sigmay = fitted_xy.axy, fitted_xy.ux, fitted_xy.uy, fitted_xy.sigx, \
                                      fitted_xy.sigy

        ux = (ux - math.ceil(grid[0] / 2)) * voxsize[0]
        sigmax = sigmax * voxsize[0]
        uy = (uy - math.ceil(grid[1] / 2)) * voxsize[1]
        sigmay = sigmay * voxsize[1]
        return np.vstack((axy, ux, sigmax, uy, sigmay)).T

    def xy_main(self, fitted_xy: FittedXy, image: nef.data_types.Image, *, half_patch_range = 0):
        x = (np.arange(image.shape[0]) + 0.5) * image.unit_size[0] - image.size[0] / 2 + \
            image.center[0]
        y = (np.arange(image.shape[1]) + 0.5) * image.unit_size[1] - image.size[1] / 2 + \
            image.center[1]
        xmesh, ymesh = np.meshgrid(x, y, indexing = 'ij')
        rmesh, pmesh = self.make_polargrid(xmesh, ymesh)
        # import time
        row, col, data = [], [], []
        fsigx = interpolate.interp1d(fitted_xy.ux, fitted_xy.sigx, fill_value =
        'extrapolate')
        fsigy = interpolate.interp1d(fitted_xy.ux, fitted_xy.sigy, fill_value =
        'extrapolate')

        # start = time.time()
        for i in nef.utils.tqdm(range(image.shape[0])):
            for j in range(image.shape[1]):
                irow = j + i * image.shape[1]
                r, phi = rmesh[i, j], pmesh[i, j]
                if r > np.max(fitted_xy.ux):
                    continue

                px = np.arange(max(i - half_patch_range, 0),
                               min(i + half_patch_range, image.shape[0]))
                py = np.arange(max(j - half_patch_range, 0),
                               min(j + half_patch_range, image.shape[1]))
                x_ = (px + 0.5 - i) * image.unit_size[0]
                y_ = (py + 0.5 - j) * image.unit_size[1]
                xmesh_, ymesh_ = np.meshgrid(x_, y_, indexing = 'ij')

                original_kernel = self.locate_kernel(xmesh_, ymesh_, fsigx(r), fsigy(r))
                rot_kernel = self.rotate_kernel(original_kernel, phi)

                # full_kernel = np.zeros((image.shape[0], image.shape[1]), dtype = np.float32)
                # full_kernel[max(i - half_patch_range, 0):
                #             min(i + half_patch_range, image.shape[0]),
                # max(j - half_patch_range, 0):
                # min(j + half_patch_range, image.shape[1])] = rot_kernel
                # kernel_flat = full_kernel.reshape((-1))
                # spa_kernel = sparse.coo_matrix(kernel_flat)

                kernel_flat = rot_kernel.reshape((-1))
                spa_kernel = sparse.coo_matrix(kernel_flat)
                col = spa_kernel.col
                ix = col // image.shape[1]
                iy = col % image.shape[1]
                incre_x = max(i - half_patch_range, 0)
                incre_y = max(j - half_patch_range, 0)
                id_ele = spa_kernel.data > 1e-8
                nb_ele = np.sum(id_ele)
                # nb_ele = spa_kernel.data.size
                # nb_ele_big = np.sum(spa_kernel.data > 1e-8)
                if nb_ele > 0:
                    row = np.append(row, [irow] * nb_ele)
                    col = np.append(col,
                                    (spa_kernel.col + incre_x * image.shape[1] + incre_y)[id_ele])
                    data = np.append(data, spa_kernel.data[id_ele])
        # return np.array([row, col, data])

        row = row.astype(int)
        col = col.astype(int)

        kernel_xy = KernelXy(sparse.coo_matrix((data, (col, row)),
                                               shape = (image.shape[0] * image.shape[1],
                                                        image.shape[0] * image.shape[1]),
                                               dtype = np.float32))
        return kernel_xy, pmesh

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

    def map_process(self, kernel_xy, kernel_z, emap):
        import numpy as np
        import copy
        emap_data = copy.copy(emap.data)
        emap_data[emap_data >= 1] = 1 / emap_data[emap_data >= 1]
        emap_data_reshaped = emap_data.reshape((-1, emap.shape[2]))

        emap_data_z = np.matmul(emap_data_reshaped, kernel_z.data)
        emap_data_psf = kernel_xy.data.dot(emap_data_z)

        emap_data_psf = emap_data_psf.reshape(emap.shape)

        emap_data_psf /= np.max(emap_data_psf)

        emap_data_psf[emap_data_psf < nef.utils._eps] = 0
        emap_data_psf[emap_data_psf > nef.utils._eps] = \
            1 / emap_data_psf[emap_data_psf > nef.utils._eps]
        return EmapMlemPsf(emap_data_psf, emap.center, emap)
