# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: image.py
@date: 3/20/2019
@desc:
'''
import typing

import attr
import numpy as np
import scipy.ndimage as nd

from srfnef.typing import dataclass


@dataclass
class Image(object):
    """
    Image data with center and size info.
    """

    data: np.ndarray
    center: typing.List[float] = attr.ib(converter = lambda x: np.array(x).astype(np.float32))
    size: typing.List[float] = attr.ib(converter = lambda x: np.array(x).astype(np.float32))

    @property
    def ndim(self):
        return len(self.data.shape)

    @property
    def unit_size(self):
        return np.array([self.size[i] / self.shape[i] for i in range(self.ndim)])

    def shift(self, dist):
        '''shift image in mm'''
        _dist = dist / self.unit_size
        if np.abs(_dist[2] - round(_dist[2])) < 1e-3 and _dist[0] == 0 and _dist[1] == 0:
            idist = int(round(_dist[2]))
            if idist == 0:
                return self.replace()
            elif idist > 0:
                data_ = np.zeros(self.shape, dtype = self.data.dtype)
                data_[:, :, idist:] = self.data[:, :, :-idist]
                return self.replace(data = data_)
            else:
                data_ = np.zeros(self.shape, dtype = self.data.dtype)
                data_[:, :, :idist] = self.data[:, :, -idist:]
                return self.replace(data = data_)
        else:
            return self.replace(data = nd.shift(self.data, _dist, order = 3))

    def rotate(self, angle):
        '''rotate x-y'''
        if angle == 0:
            return self
        return self.replace(data = nd.rotate(self.data, np.rad2deg(angle), order = 1,
                                             reshape = False))

    def zoom(self, scale):
        return self.replace(data = nd.zoom(self.data, scale, order = 1))

    @property
    def central_slices(self):
        t0 = self.data[int(self.shape[0] / 2), :, :]
        t1 = self.data[:, int(self.shape[1] / 2), :]
        t2 = self.data[:, :, int(self.shape[2] / 2)]
        return t0, t1, t2

    @property
    def central_profiles(self):
        p0 = self.data[:, int(self.shape[1] / 2), int(self.shape[2] / 2)]
        p1 = self.data[int(self.shape[0] / 2), :, int(self.shape[2] / 2)]
        p2 = self.data[int(self.shape[0] / 2), int(self.shape[1] / 2), :]
        return p0, p1, p2
