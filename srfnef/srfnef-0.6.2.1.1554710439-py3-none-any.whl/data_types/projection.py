# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: projection.py
@date: 3/20/2019
@desc:
'''

import attr
import numpy as np
from scipy import sparse

from srfnef.typing import dataclass
from .scanner import PetCylindricalScanner, Lors


@dataclass
class Sinogram(object):
    data: sparse.csr_matrix
    scanner: PetCylindricalScanner

    @property
    def vproj(self):
        return self.data

    @classmethod
    def initializer(cls, scanner):
        D = np.ones((scanner.nb_detectors, scanner.nb_detectors), dtype = np.float32)
        return cls(sparse.csr_matrix(D), scanner)

    def to_listmode(self):
        return _sinogram_to_listmode(self)


def _sinogram_to_listmode(sino: Sinogram):
    scanner = sino.scanner
    csr = sino.data
    row, col = csr.nonzero()
    iy1 = row % scanner.blocks.shape[1]
    ib1 = (row // scanner.blocks.shape[1]) % scanner.nb_blocks_per_ring
    i_thin_ring1 = row // scanner.nb_detectors_per_thin_ring
    lors_data = np.zeros((csr.nnz, 6), dtype = np.float32)
    x0 = (scanner.inner_radius + scanner.outer_radius) / 2
    y0 = (iy1 + 0.5) * scanner.blocks.unit_size[1] - scanner.blocks.size[1] / 2
    theta = scanner.angle_per_block * ib1
    lors_data[:, 0] = x0 * np.cos(theta) - y0 * np.sin(theta)
    lors_data[:, 1] = x0 * np.sin(theta) + y0 * np.cos(theta)
    lors_data[:, 2] = (i_thin_ring1 + 0.5) * scanner.blocks.unit_size[2] - scanner.axial_length / 2

    iy2 = col % scanner.blocks.shape[1]
    ib2 = (col // scanner.blocks.shape[1]) % scanner.nb_blocks_per_ring
    i_thin_ring2 = col // scanner.nb_detectors_per_thin_ring
    #     print(iy1, iy2, ib1, ib2, i_thin_ring1, i_thin_ring2)
    x0 = (scanner.inner_radius + scanner.outer_radius) / 2
    y0 = (iy2 + 0.5) * scanner.blocks.unit_size[1] - scanner.blocks.size[1] / 2
    theta = scanner.angle_per_block * ib2
    lors_data[:, 3] = x0 * np.cos(theta) - y0 * np.sin(theta)
    lors_data[:, 4] = x0 * np.sin(theta) + y0 * np.cos(theta)
    lors_data[:, 5] = (i_thin_ring2 + 0.5) * scanner.blocks.unit_size[2] - scanner.axial_length / 2

    return Listmode(csr.data, Lors(lors_data))


@dataclass
class Listmode(object):
    data: np.ndarray = attr.ib(converter = lambda x: np.array(x).astype(np.float32))
    lors: Lors

    @property
    def length(self):
        return self.data.shape[0]

    @property
    def vproj(self):
        return self.data

    @classmethod
    def from_scanner(cls, scanner):
        _lors = Lors.from_scanner(scanner)
        _data = np.ones((len(_lors),), dtype = np.float32)
        return cls(_data, _lors)

    def __len__(self):
        return len(self.lors)

    @classmethod
    def from_lors(cls, lors: Lors):
        return cls(np.ones((len(lors),), dtype = np.float32), lors)

    def to_sinogram(self, scanner: PetCylindricalScanner):
        iblock1 = _position_to_block_index(self.lors.data[:, :3], scanner)
        iblock2 = _position_to_block_index(self.lors.data[:, 3:], scanner)
        iring1 = _position_to_thin_ring_index(self.lors.data[:, :3], scanner)
        iring2 = _position_to_thin_ring_index(self.lors.data[:, 3:], scanner)
        _fst = _rotate_to_block0(self.lors.data[:, :3], scanner, iblock1)
        iy1 = _position_to_y_index_per_block(_fst, scanner)
        _snd = _rotate_to_block0(self.lors.data[:, 3:], scanner, iblock2)
        iy2 = _position_to_y_index_per_block(_snd, scanner)
        row = iy1 + scanner.blocks.shape[1] * iblock1 + scanner.nb_detectors_per_thin_ring * iring1
        col = iy2 + scanner.blocks.shape[1] * iblock2 + scanner.nb_detectors_per_thin_ring * iring2

        return Sinogram(sparse.csr_matrix((self.data, (row, col)), shape = (scanner.nb_detectors,
                                                                            scanner.nb_detectors
                                                                            )), scanner)

    def compress(self, scanner: PetCylindricalScanner):
        return self.to_sinogram(scanner).to_listmode()


def _position_to_block_index(pos, scanner: PetCylindricalScanner):
    xc, yc = pos[:, 0], pos[:, 1]
    return np.round(np.arctan2(yc, xc) / scanner.angle_per_block).astype(
        int) % scanner.nb_blocks_per_ring


def _position_to_thin_ring_index(pos, scanner: PetCylindricalScanner):
    zc = pos[:, 2]
    return np.floor((zc + scanner.axial_length / 2) / scanner.blocks.unit_size[2]).astype(int)


def _rotate_to_block0(pos, scanner: PetCylindricalScanner, iblock):
    angle = iblock * scanner.angle_per_block
    _pos = np.zeros(pos.shape)
    xc, yc = pos[:, 0], pos[:, 1]
    _pos[:, 0] = xc * np.cos(angle) + yc * np.sin(angle)
    _pos[:, 1] = -xc * np.sin(angle) + yc * np.cos(angle)
    _pos[:, 2] = pos[:, 2]
    return _pos


def _position_to_y_index_per_block(pos, scanner: PetCylindricalScanner):
    return np.round((pos[:, 1] + scanner.blocks.size[1] / 2) // scanner.blocks.unit_size[1]).astype(
        int)
