# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: imshow_full.py
@date: 4/2/2019
@desc:
'''
from matplotlib import pyplot as plt

import srfnef as nef


def imshow(self, *args, **kwargs):
    assert nef.utils.is_notebook()
    plt.imshow(self.central_slices[2], *args, **kwargs)


nef.data_types.Image.imshow = imshow


def imshow_full(self, *args, **kwargs):
    assert nef.utils.is_notebook()
    plt.figure(figsize = (15, 15))
    plt.subplot(131)
    plt.imshow(self.central_slices[0], *args, **kwargs)
    plt.subplot(132)
    plt.imshow(self.central_slices[1], *args, **kwargs)
    plt.subplot(133)
    plt.imshow(self.central_slices[2], *args, **kwargs)


nef.data_types.Image.imshow_full = imshow_full
