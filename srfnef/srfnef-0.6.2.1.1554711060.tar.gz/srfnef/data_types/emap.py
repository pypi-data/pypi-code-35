# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: emap.py
@date: 3/20/2019
@desc:
'''

import numpy as np

from srfnef.typing import dataclass
from srfnef.utils import tqdm
from .image import Image


@dataclass
class EmapMlem(Image):
    from .scanner import PetCylindricalScanner
    # TODO correct emap generations in ring mode.
    @classmethod
    def from_scanner(cls, scanner: PetCylindricalScanner, bprojector, mode = 'thin-ring'):
        from .scanner import Lors
        from .projection import Listmode
        emap = cls(np.zeros(bprojector.shape, np.float32), bprojector.center, bprojector.size)
        if mode == 'full':
            from ._mesh_grid import _mesh_detector_full
            lor_data = _mesh_detector_full(scanner)
            lors = Lors(lor_data)
            return bprojector(Listmode.from_lors(lors))
        elif mode == 'ring-full':
            from ._mesh_grid import _mesh_detector_ring
            lors_data = _mesh_detector_ring(scanner, 0)
            lors = Lors(lors_data)
            for i in tqdm(np.arange(scanner.nb_rings)):
                for j in np.arange(scanner.nb_rings):
                    if i > j:
                        continue
                    lors.data[:, 2] += i * (scanner.blocks.size[2] + scanner.gap) - \
                                       scanner.axial_length / 2 + scanner.blocks.size[2] / 2
                    lors.data[:, 5] += j * (scanner.blocks.size[2] + scanner.gap) - \
                                       scanner.axial_length / 2 + scanner.blocks.size[2] / 2
                    _emap = bprojector(Listmode.from_lors(lors))
                    lors.data[:, 2] -= i * (scanner.blocks.size[2] + scanner.gap) - \
                                       scanner.axial_length / 2 + scanner.blocks.size[2] / 2
                    lors.data[:, 5] -= j * (scanner.blocks.size[2] + scanner.gap) - \
                                       scanner.axial_length / 2 + scanner.blocks.size[2] / 2
                    if i == j:
                        emap = emap + _emap
                    else:
                        emap = emap + _emap * 2
            return emap
        elif mode == 'ring':
            from ._mesh_grid import _mesh_detector_ring
            lors_data = _mesh_detector_ring(scanner, 0)
            lors = Lors(lors_data)
            for d in tqdm(np.arange(scanner.nb_rings)):
                lors.data[:, 2] += -d / 2 * (scanner.blocks.size[2] + scanner.gap) + \
                                   scanner.blocks.size[2] / 2
                lors.data[:, 5] += d / 2 * (scanner.blocks.size[2] + scanner.gap) + \
                                   scanner.blocks.size[2] / 2
                _emap = bprojector(Listmode.from_lors(lors))
                lors.data[:, 2] -= -d / 2 * (scanner.blocks.size[2] + scanner.gap) + \
                                   scanner.blocks.size[2] / 2
                lors.data[:, 5] -= d / 2 * (scanner.blocks.size[2] + scanner.gap) + \
                                   scanner.blocks.size[2] / 2
                for i in np.arange(scanner.nb_rings):
                    j = i + d
                    if not 0 <= j < scanner.nb_rings:
                        continue
                    if d == 0:
                        emap = emap + _emap.shift(
                            [0, 0, (i + d / 2) * (scanner.blocks.size[2] + scanner.gap) -
                             scanner.axial_length / 2])
                    else:
                        emap = emap + _emap.shift(
                            [0, 0, (i + d / 2) * (scanner.blocks.size[2] + scanner.gap) -
                             scanner.axial_length / 2]) * 2
            return emap
        elif mode == 'thin-ring-full':
            from ._mesh_grid import _mesh_detector_thin_ring
            lors_data = _mesh_detector_thin_ring(scanner, 0)
            lors = Lors(lors_data)
            for i in tqdm(np.arange(scanner.nb_thin_rings)):
                for j in np.arange(scanner.nb_thin_rings):
                    if i > j:
                        continue
                    lors.data[:, 2] += i * scanner.blocks.unit_size[2] + i // \
                                       scanner.blocks.shape[2] * scanner.gap - \
                                       scanner.axial_length / 2 + scanner.blocks.unit_size[2] / 2
                    lors.data[:, 5] += j * scanner.blocks.unit_size[2] + j // \
                                       scanner.blocks.shape[2] * scanner.gap - \
                                       scanner.axial_length / 2 + scanner.blocks.unit_size[2] / 2
                    _emap = bprojector(Listmode.from_lors(lors))
                    lors.data[:, 2] -= i * scanner.blocks.unit_size[2] + i // \
                                       scanner.blocks.shape[2] * scanner.gap - \
                                       scanner.axial_length / 2 + scanner.blocks.unit_size[2] / 2
                    lors.data[:, 5] -= j * scanner.blocks.unit_size[2] + j // \
                                       scanner.blocks.shape[2] * scanner.gap - \
                                       scanner.axial_length / 2 + scanner.blocks.unit_size[2] / 2
                    if i == j:
                        emap = emap + _emap
                    else:
                        emap = emap + _emap * 2
            return emap
        elif mode == 'thin-ring':
            from ._mesh_grid import _mesh_detector_thin_ring
            lors_data = _mesh_detector_thin_ring(scanner, 0)
            lors = Lors(lors_data)
            for d in tqdm(np.arange(scanner.nb_thin_rings)):
                lors.data[:, 2] += (-d / 2 + 0.5) * scanner.blocks.unit_size[2]
                lors.data[:, 5] += (d / 2 + 0.5) * scanner.blocks.unit_size[2]
                _emap = bprojector(Listmode.from_lors(lors))
                lors.data[:, 2] -= (-d / 2 + 0.5) * scanner.blocks.unit_size[2]
                lors.data[:, 5] -= (d / 2 + 0.5) * scanner.blocks.unit_size[2]
                for i in np.arange(scanner.nb_thin_rings):
                    j = d + i
                    if not 0 <= j < scanner.nb_thin_rings:
                        continue
                    if d == 0:
                        emap = emap + _emap.shift(
                            [0, 0, (i + d / 2) * scanner.blocks.unit_size[2] -
                             scanner.axial_length / 2])
                    else:
                        emap = emap + _emap.shift(
                            [0, 0, (i + d / 2) * scanner.blocks.unit_size[2] -
                             scanner.axial_length / 2]) * 2
            return emap
            # emap_data = emap.data
            # emap_data[:, :, :20] = emap_data[:, :, :-21:-1]
            # return emap.replace(data = emap_data)

            # TODO find out why it different of first half and last half
        else:
            raise NotImplementedError

    @classmethod
    def from_scanner_full(cls, scanner: PetCylindricalScanner, bprojector):
        from .scanner import Lors
        from .projection import Listmode
        _emap = bprojector(Listmode.from_lors(Lors.from_scanner(scanner)))
        return cls(_emap.data, _emap.center, _emap.size)
