import numpy as np

from srfnef.data_types import Image, Listmode
from srfnef.func_types import Projector
from srfnef.typing import funcclass

__all__ = ('UmapProjector', 'AttenuationCorrector')


@funcclass
class UmapProjector:
    projector: Projector

    def __call__(self, u_map: Image, lors):
        u_map_proj = self.projector(u_map, lors)
        dx = u_map_proj.lors.data[:, 0] - u_map_proj.lors.data[:, 3]
        dy = u_map_proj.lors.data[:, 1] - u_map_proj.lors.data[:, 4]
        dz = u_map_proj.lors.data[:, 2] - u_map_proj.lors.data[:, 5]
        L = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        u_map_proj = u_map_proj * L * L
        return u_map_proj.replace(data = np.exp(-u_map_proj.data))


@funcclass
class AttenuationCorrector:
    u_map_projector: UmapProjector

    def __call__(self, listmode: Listmode):
        return listmode / self.u_map_projector
