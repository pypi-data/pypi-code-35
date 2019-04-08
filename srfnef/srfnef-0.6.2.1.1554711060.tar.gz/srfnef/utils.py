# encoding: utf-8
'''
srfnef.utils
~~~~~~~~~~~~

This module provides utility functions that are used within SRF-NEF
that are alose useful for extenel comsumptions.
'''

import getpass
import os
import platform
import re
import sys
import time

import numpy as np
import tqdm as tqdm_
from matplotlib import pyplot as plt

__all__ = (
    'is_notebook', 'tqdm', '_eps', '_small', '_tiny', '_huge', '_pi', 'main_path', 'separator')


def is_notebook():
    '''check if the current environment is `ipython`/ `notebook`
    '''
    return 'ipykernel' in sys.modules


is_ipython = is_notebook


def tqdm(*args, **kwargs):
    '''same as tqdm.tqdm
    Automatically switch between `tqdm.tqdm` and `tqdm.tqdm_notebook` accoding to the runtime
    environment.
    '''
    if is_notebook():
        return tqdm_.tqdm_notebook(*args, **kwargs)
    else:
        return tqdm_.tqdm(*args, **kwargs)


def _dataclass_to_md(dat, indent = 0):
    out_string = ''
    out_string += '   ' * indent + f'- {dat.__class__.__name__}:\n\n'
    if callable(dat):
        out_string += '   ' * (indent + 1) + f'- callable\n\n'
    for key, value in dat.to_dict(recurse = False).items():
        from srfnef.typing import DataClass
        if isinstance(value, DataClass):
            out_string += _dataclass_to_md(value, indent + 1)
        elif key == 'data':
            out_string += '   ' * (
                    indent + 1) + f'- {key}: array(shape = {value.shape}, dtype = {value.dtype})\n\n'
        else:
            out_string += '   ' * (indent + 1) + f'- {key}: {value}\n\n'
    return out_string + '\n'


def _imshow(dat):
    out = ''
    if isinstance(dat, list):
        for img in dat:
            out += _dataclass_to_md(img)
        n = len(dat)

        plt.figure(figsize = (3 * n, 3))
        for i in range(n):
            plt.subplot(1, n, i + 1)
            dat[i].imshow()
        else:
            plt.savefig(f'recon_image.png')

        out += f'![alt text](recon_image.png)\n\n'

        plt.figure(figsize = (3 * n, 3))
        for i in range(n):
            p0, p1 = dat[i].central_profiles[:2]
            shape, center, size, unit_size = dat[i].shape, dat[i].center, dat[i].size, dat[
                i].unit_size
            coo_0 = (np.arange(shape[0]) + 0.5) * unit_size[0] - size[0] / 2 + center[0]
            coo_1 = (np.arange(shape[1]) + 0.5) * unit_size[1] - size[1] / 2 + center[1]
            plt.subplot(1, n, i + 1)
            plt.plot(coo_0, p0, label = 'x profile')
            plt.plot(coo_1, p1, label = 'y profile')
        else:
            plt.savefig(f'recon_profile.png')
        out += f'![alt text](recon_profile.png)'

    else:
        i = 0
        plt.figure(figsize = (3, 3))
        dat.imshow()
        plt.savefig(f'recon_image_{i}.png')

        plt.figure(figsize = (3, 3))
        plt.subplot(211)
        p0, p1 = dat.central_profiles[:2]
        shape, center, size, unit_size = dat.shape, dat.center, dat.size, dat.unit_size
        coo_0 = (np.arange(shape[0]) + 0.5) * unit_size[0] - size[0] / 2 + center[0]
        coo_1 = (np.arange(shape[1]) + 0.5) * unit_size[1] - size[1] / 2 + center[1]
        plt.plot(coo_0, p0, label = 'x profile')
        plt.plot(coo_1, p1, label = 'y profile')
        plt.savefig(f'recon_profile_{i}.png')
        out += f'![alt text](recon_image_{i}.png)![alt text](recon_profile_{i}.png)\n\n'
    return out


def write_markdown(path, args, output):
    out_string = ''
    out_string += f'# Title: test generate markdown doc \n\n'
    out_string += f'Time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}\n\n'
    out_string += f'Author: {getpass.getuser()}\n\n'
    for arg in args:
        out_string += '---\n\n'
        out_string += _dataclass_to_md(arg)
    out_string += '---\n\n'
    out_string += '## Output: \n\n'
    out_string += _imshow(output)
    with open(path, 'w', encoding = 'utf8') as fout:
        fout.write(out_string)


_eps = 1e-8

_small = 1e-4

_tiny = 1e-8

_huge = 1e8

_pi = 3.14159265358979323846264338

if 'Windows' in platform.system():
    separator = '\\'
else:
    separator = '/'

main_path = os.path.abspath(os.path.dirname(os.path.abspath(__file__))) + separator


def convert_Camal_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def convert_snake_to_Camel(name):
    out = ''
    for ele in name.split('_'):
        out += ele.capitalize()
    return out
