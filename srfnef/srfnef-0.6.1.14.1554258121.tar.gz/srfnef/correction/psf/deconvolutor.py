# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: deconvolutor.py
@date: 3/31/2019
@desc:
'''

from copy import copy

import attr
import numpy as np
from scipy import interpolate
from scipy import sparse

import srfnef as nef
from .psf_fitter import FittedXy, FittedZ


@nef.typing.funcclass
class DeconvolutorXy(object):
    n_iter: int
    fitted_xy: FittedXy
    data: sparse.coo_matrix = attr.ib(default = None)

    def __call__(self, image: nef.data_types.Image, is_tqdm = False):
        if self.data is None:
            raise ValueError('Please run `make_kernel` first')
        image_data = copy(image.data)
        x = np.ones((image.shape[0] * image.shape[1], image.shape[2]), dtype = np.float32)
        d = image_data.reshape((-1, image.shape[2]))
        if is_tqdm:
            range_ = nef.utils.tqdm(range(self.n_iter))
        else:
            range_ = range(self.n_iter)
        for i in range_:
            c = self.data @ x
            c[c < 1e-16] = 1e16
            x *= self.data.transpose() @ (d / c)
        return image.replace(data = x.reshape(image.shape))

    def make_kernel(self, image: nef.data_types.Image):
        kernel_xy = self.xy_main(self.fitted_xy, image, half_patch_range = 5)
        object.__setattr__(self, 'data', kernel_xy)

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
        return img_r

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

    def xy_main(self, fitted_xy: FittedXy, image: nef.data_types.Image, *, half_patch_range = 0):
        x = (np.arange(image.shape[0]) + 0.5) * image.unit_size[0] - image.size[0] / 2 + \
            image.center[0]
        y = (np.arange(image.shape[1]) + 0.5) * image.unit_size[1] - image.size[1] / 2 + \
            image.center[1]
        xmesh, ymesh = np.meshgrid(x, y, indexing = 'ij')
        rmesh, pmesh = self.make_polargrid(xmesh, ymesh)
        # import time
        row, col, data = [], [], []
        fsigx = interpolate.interp1d(fitted_xy.ux, fitted_xy.sigx, fill_value = 0)
        fsigy = interpolate.interp1d(fitted_xy.ux, fitted_xy.sigy, fill_value = 0)

        out = sparse.lil_matrix((image.shape[0] * image.shape[1],
                                 image.shape[0] * image.shape[1]),
                                dtype = np.float32)
        # start = time.time()
        for i in nef.utils.tqdm(range(image.shape[0])):
            for j in range(image.shape[1]):
                irow = j + i * image.shape[1]
                r, phi = rmesh[i, j], pmesh[i, j]
                if r > np.max(fitted_xy.ux):
                    continue

                px = np.arange(max(i - half_patch_range, 0),
                               min(i + half_patch_range + 1, image.shape[0]))
                py = np.arange(max(j - half_patch_range, 0),
                               min(j + half_patch_range + 1, image.shape[1]))
                x_ = (px - i) * image.unit_size[0]
                y_ = (py - j) * image.unit_size[1]
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
                ix = col // len(py)
                iy = col % len(py)
                incre_x = i - min(half_patch_range, i)
                ix += incre_x
                incre_y = j - min(half_patch_range, j)
                iy += incre_y
                if any(ix >= image.shape[0]):
                    raise ValueError
                id_ele = spa_kernel.data > 1e-8
                nb_ele = np.sum(id_ele)
                # nb_ele = spa_kernel.data.size
                # nb_ele_big = np.sum(spa_kernel.data > 1e-8)
                if nb_ele > 0:
                    row = [irow] * nb_ele
                    col = (ix * image.shape[1] + iy)[id_ele]
                    data = spa_kernel.data[id_ele]
                    # row = np.append(row, [irow] * nb_ele)
                    # col = np.append(col,
                    #                 (spa_kernel.col + incre_x * image.shape[1] + incre_y)[id_ele])
                    # data = np.append(data, spa_kernel.data[id_ele])
                    out[col, row] = data

        return out.tocoo()
        # return np.array([row, col, data])

        # row = row.astype(int)
        # col = col.astype(int)
        #
        # return sparse.coo_matrix((data, (col, row)),
        #                          shape = (image.shape[0] * image.shape[1],
        #                                   image.shape[0] * image.shape[1]),
        #                          dtype = np.float32)


@nef.typing.funcclass
class DeconvolutorZ(object):
    n_iter: int
    fitted_z: FittedZ
    data: sparse.coo_matrix = attr.ib(default = None)

    def __call__(self, image: nef.data_types.Image, is_tqdm = False):
        if self.data is None:
            raise ValueError('Please run `make_kernel` first')
        image_data = copy(image.data)
        x = np.ones((image.shape[0] * image.shape[1], image.shape[2]), dtype = np.float32)
        d = image_data.reshape((-1, image.shape[2]))
        if is_tqdm:
            range_ = nef.utils.tqdm(range(self.n_iter))
        else:
            range_ = range(self.n_iter)
        for _ in range_:
            c = x @ self.data
            c[c < 1e-16] = 1e16
            x *= (d / c) @ self.data.transpose()
        return image.replace(data = x.reshape(image.shape))

    def make_kernel(self, image: nef.data_types.Image):
        kernel_z = self.z_main(self.fitted_z, image, half_patch_range = 5)
        object.__setattr__(self, 'data', kernel_z)

    def z_main(self, fitted_z: FittedZ, image: nef.data_types.Image, half_patch_range = 0):
        fsigz = interpolate.interp1d(fitted_z.uz, fitted_z.sigz, fill_value = 'extrapolate')
        out = sparse.lil_matrix(image.shape[2], image.shape[2], dtype = np.float32)

        for i in nef.utils.tqdm(range(image.shape[2])):
            z = (i + 0.5) * image.unit_size[2] - image.size[2] / 2
            zmesh = (np.arange(image.shape[2]) - i) * image.unit_size[2]
            local_kernel = self.locate_kernel(zmesh, fsigz(z))
            spa_kernel = sparse.coo_matrix(local_kernel)
            id_ele = spa_kernel.data > 1e-8
            nb_ele = np.sum(id_ele)
            if nb_ele > 0:
                row = [i] * nb_ele
                col = sparse.col[id_ele]
                data = spa_kernel.data[id_ele]
                out[col, row] = data
        return out.tocoo()

    def locate_kernel(self, mesh, sig2):
        ans = 1.0 / np.sqrt(2 * np.pi * sig2) * np.exp(-mesh ** 2 / 2 / sig2)
        return ans / np.sum(ans)
