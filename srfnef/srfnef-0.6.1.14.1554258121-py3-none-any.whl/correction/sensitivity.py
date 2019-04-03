# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: sensitivity.py
@date: 3/30/2019
@desc:
'''

from copy import copy

import numpy as np
from scipy import interpolate

from srfnef.correction.psf.psf_fitter import FittedZ
from srfnef.data_types import Listmode, PetCylindricalScanner, Image
from srfnef.typing import funcclass


@funcclass
class SensitivityListmodeCorrector:
    scanner: PetCylindricalScanner

    def __call__(self, listmode: Listmode):
        lz = np.abs(listmode.lors.data[:, 2] - listmode.lors.data[:, 5])
        cos_ = np.sqrt(self.scanner.average_radius ** 2 + lz ** 2) / self.scanner.average_radius
        return listmode * cos_


@funcclass
class SensitivityPsfCorrector:
    fitted_z: FittedZ

    def __call__(self, image: Image):
        f = interpolate.interp1d(self.fitted_z.uz, self.fitted_z.az, fill_value = 'extrapolate')
        image_data = copy(image.data)
        for i in range(image.shape[2]):
            d = abs(i - image.shape[2] / 2 + 0.5) * image.unit_size[2]
            if d > np.max(self.fitted_z.uz):
                continue
            image_data[:, :, i] /= f(d)
        return image.replace(data = image_data)
