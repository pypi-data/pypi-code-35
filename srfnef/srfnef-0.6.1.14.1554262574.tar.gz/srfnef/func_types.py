import typing

import attr
import numpy as np
from numba import cuda
from numba import jit

from srfnef.data_types import Image, Listmode, EmapMlem, Lors
from .typing import funcclass, Saver
from .utils import tqdm

running_env = jit(nopython = True, parallel = True)


@funcclass
class Projector:
    mode: str = attr.ib(default = 'siddon')
    device: str = attr.ib(default = 'gpu')
    name: str = attr.ib(default = 'projector')

    def __call__(self, image: Image, lors: Lors):
        if self.mode == 'siddon':
            if self.device == 'cpu':
                from .model_impl import proj_siddon
                vproj = proj_siddon(image.data, lors.data, image.size / image.shape, image.center)
            elif self.device == 'gpu':
                from .model_impl import proj_siddon_cuda
                blockdim = (256,)
                griddim = (1 + int(len(lors) / blockdim[0]),)
                vproj = np.zeros((len(lors),), dtype = np.float32)
                proj_siddon_cuda[griddim, blockdim](image.data, lors.data, image.size / image.shape,
                                                    image.center, vproj)
                cuda.synchronize()
        else:
            raise NotImplementedError

        return Listmode(vproj, lors)


@funcclass
class BackProjector:
    shape: typing.List[int] = attr.ib(converter = lambda x: np.array(x).astype(np.int32))
    center: typing.List[float] = attr.ib(converter = lambda x: np.array(x).astype(np.float32))
    size: typing.List[float] = attr.ib(converter = lambda x: np.array(x).astype(np.float32))
    mode: str = attr.ib(default = 'siddon')
    device: str = attr.ib(default = 'gpu')
    name: str = attr.ib(default = 'back_projector')

    @property
    def unit_size(self):
        return self.size / self.shape

    def __call__(self, listmode: Listmode):
        if self.mode == 'siddon':
            if self.device == 'cpu':
                from .model_impl import bproj_siddon
                image_data = bproj_siddon(listmode.data, listmode.lors.data, self.size /
                                          self.shape, self.center, self.shape)
            elif self.device == 'gpu':
                from .model_impl import bproj_siddon_cuda
                blockdim = (256,)
                griddim = (1 + int(len(listmode.lors) / blockdim[0]),)
                image_data = np.zeros(self.shape, dtype = np.float32)
                bproj_siddon_cuda[griddim, blockdim](listmode.data, listmode.lors.data, self.size /
                                                     self.shape, self.center, image_data)
            else:
                raise NotImplementedError
        else:
            raise NotImplementedError
        return Image(image_data, self.center, self.size)


@funcclass
class Mlem:
    n_iter: int
    projector: Projector
    back_projector: BackProjector
    emap_mlem: EmapMlem
    saver: Saver = attr.ib(default = Saver())
    is_tqdm: bool = attr.ib(default = True)
    name: str = attr.ib(default = 'mlem')

    def __call__(self, listmode: Listmode, *, x = None, labels = []):
        if x is None:
            x = Image(np.ones(self.emap_mlem.shape, dtype = np.float32), self.emap_mlem.center,
                      self.emap_mlem.size)
        range_ = range(self.n_iter) if not self.is_tqdm else tqdm(range(self.n_iter))
        for ind in range_:
            proj = self.projector(x, listmode.lors)
            bp = self.back_projector(listmode / proj)
            x = x * bp / self.emap_mlem
            x = self.saver(ind + 1, x, labels = labels)
        return x
