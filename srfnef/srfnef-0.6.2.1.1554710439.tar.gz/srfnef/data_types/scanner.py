import typing

import attr
import numpy as np

from srfnef.typing import dataclass


@dataclass
class Block:
    size: typing.List[float] = attr.ib(converter = lambda x: np.array(x).astype(np.float32))
    shape: typing.List[int] = attr.ib(converter = lambda x: np.array(x).astype(np.int32))

    @property
    def unit_size(self):
        return np.array([self.size[i] / self.shape[i] for i in range(len(self.size))])


@dataclass
class PetCylindricalScanner:
    inner_radius: float
    outer_radius: float
    nb_rings: int
    nb_blocks_per_ring: int
    gap: float
    blocks: Block

    @property
    def axial_length(self):
        return self.blocks.size[2] * self.nb_rings + self.gap * (self.nb_rings - 1)

    @property
    def central_bin_size(self):
        return 2 * np.pi * self.inner_radius / self.nb_detectors_per_ring / 2

    @property
    def nb_detectors_per_block(self):
        return np.prod(self.blocks.shape)

    @property
    def nb_detectors_per_ring(self):
        return self.nb_detectors_per_block * self.nb_blocks_per_ring

    @property
    def nb_detectors(self):
        return self.nb_detectors_per_ring * self.nb_rings

    @property
    def angle_per_block(self):
        return 2 * np.pi / self.nb_blocks_per_ring

    @property
    def nb_thin_rings(self):
        return self.nb_rings * self.blocks.shape[2]

    @property
    def nb_detectors_per_thin_ring(self):
        return self.blocks.shape[1] * self.nb_blocks_per_ring

    @property
    def average_radius(self):
        return (self.inner_radius + self.outer_radius) / 2


@dataclass
class Lors(object):
    data: np.ndarray

    @property
    def length(self):
        return self.data.shape[0]

    @property
    def fst(self):
        return self.data[:, :3]

    @property
    def snd(self):
        return self.data[:, 3:]

    def __len__(self):
        return self.data.shape[0]

    def __bool__(self):
        return self.__len__() > 0

    @classmethod
    def from_scanner(cls, scanner):
        from ._mesh_grid import _mesh_detector_full
        _lors = _mesh_detector_full(scanner)
        return cls(_lors)

    @classmethod
    def from_scanner_ring(cls, scanner, i, j):
        from ._mesh_grid import _mesh_detector_ring
        _lors = _mesh_detector_ring(scanner, i, j)
        return cls(_lors)

    @classmethod
    def from_scanner_thin_ring(cls, scanner, i, j):
        from ._mesh_grid import _mesh_detector_thin_ring
        _lors = _mesh_detector_thin_ring(scanner, i, j)
        return cls(_lors)

    @classmethod
    def from_fst_snd(cls, fst, snd):
        return cls(np.hstack((fst, snd)))
