# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: _mesh_grid.py
@date: 3/20/2019
@desc:
'''

import numpy as np
from numba import jit

from .scanner import PetCylindricalScanner


@jit
def _mesh_detector_full(scanner: PetCylindricalScanner):
    if scanner.nb_rings > 1:
        raise ValueError('Please use _mesh_detector_ring instead')
    lors = np.zeros((scanner.nb_detectors * scanner.nb_detectors, 6), dtype = np.float32)

    x = np.ones(scanner.blocks.shape[1], ) * scanner.average_radius
    y = (np.arange(scanner.blocks.shape[1]) + 0.5) * scanner.blocks.unit_size[1] - \
        scanner.blocks.size[1] / 2
    z = (np.arange(scanner.blocks.shape[2]) + 0.5) * scanner.blocks.unit_size[2] - \
        scanner.blocks.size[2] / 2
    xx = np.kron(x, [1] * scanner.nb_blocks_per_ring)
    yy = np.kron(y, [1] * scanner.nb_blocks_per_ring)
    theta = 2 * np.pi / scanner.nb_blocks_per_ring * np.arange(scanner.nb_blocks_per_ring)
    theta1 = np.kron(theta, [[1]] * scanner.blocks.shape[1]).ravel()
    xx1 = xx * np.cos(theta1) - yy * np.sin(theta1)
    yy1 = xx * np.sin(theta1) + yy * np.cos(theta1)
    xd = np.kron(xx1, [[1]] * scanner.blocks.shape[2]).ravel()
    yd = np.kron(yy1, [[1]] * scanner.blocks.shape[2]).ravel()
    zd = np.kron(z, [1] * scanner.blocks.shape[1] * scanner.nb_blocks_per_ring)

    lors[:, 0] = np.kron(xd, [1] * scanner.nb_detectors_per_ring)
    lors[:, 1] = np.kron(yd, [1] * scanner.nb_detectors_per_ring)
    lors[:, 2] = np.kron(zd, [1] * scanner.nb_detectors_per_ring)
    lors[:, 3] = np.kron(xd, [[1]] * scanner.nb_detectors_per_ring).ravel()
    lors[:, 4] = np.kron(yd, [[1]] * scanner.nb_detectors_per_ring).ravel()
    lors[:, 5] = np.kron(zd, [[1]] * scanner.nb_detectors_per_ring).ravel()

    return lors


@jit
def _mesh_detector_ring(scanner: PetCylindricalScanner, d):
    lors = np.zeros((scanner.nb_detectors_per_ring * scanner.nb_detectors_per_ring, 6),
                    dtype = np.float32)

    x = np.ones(scanner.blocks.shape[1], ) * scanner.average_radius
    y = (np.arange(scanner.blocks.shape[1]) + 0.5) * scanner.blocks.unit_size[1] - \
        scanner.blocks.size[1] / 2
    z = (np.arange(scanner.blocks.shape[2]) + 0.5) * scanner.blocks.unit_size[2] - \
        scanner.blocks.size[2] * (d + 1) / 2
    xx = np.kron(x, [1] * scanner.nb_blocks_per_ring)
    yy = np.kron(y, [1] * scanner.nb_blocks_per_ring)
    theta = 2 * np.pi / scanner.nb_blocks_per_ring * np.arange(scanner.nb_blocks_per_ring)
    theta1 = np.kron(theta, [[1]] * scanner.blocks.shape[1]).ravel()
    xx1 = xx * np.cos(theta1) - yy * np.sin(theta1)
    yy1 = xx * np.sin(theta1) + yy * np.cos(theta1)
    xd = np.kron(xx1, [[1]] * scanner.blocks.shape[2]).ravel()
    yd = np.kron(yy1, [[1]] * scanner.blocks.shape[2]).ravel()
    zd = np.kron(z, [1] * scanner.blocks.shape[1] * scanner.nb_blocks_per_ring)

    lors[:, 0] = np.kron(xd, [1] * scanner.nb_detectors_per_ring)
    lors[:, 1] = np.kron(yd, [1] * scanner.nb_detectors_per_ring)
    lors[:, 2] = np.kron(zd, [1] * scanner.nb_detectors_per_ring)
    lors[:, 3] = np.kron(xd, [[1]] * scanner.nb_detectors_per_ring).ravel()
    lors[:, 4] = np.kron(yd, [[1]] * scanner.nb_detectors_per_ring).ravel()
    lors[:, 5] = np.kron(zd + d * (scanner.blocks.size[2] + scanner.gap),
                         [[1]] * scanner.nb_detectors_per_ring).ravel()

    return lors


@jit
def _mesh_detector_thin_ring(scanner: PetCylindricalScanner, d):
    if scanner.gap > 0.0:
        raise ValueError('Please use _mesh_detector_ring instead')
    lors = np.zeros((scanner.nb_detectors_per_thin_ring * scanner.nb_detectors_per_thin_ring, 6),
                    dtype = np.float32)

    x = np.ones(scanner.blocks.shape[1], ) * scanner.average_radius
    y = (np.arange(scanner.blocks.shape[1]) + 0.5) * scanner.blocks.unit_size[1] - \
        scanner.blocks.size[1] / 2
    z = 0.5 * scanner.blocks.unit_size[2] - scanner.blocks.unit_size[2] * (d + 1) / 2
    xx = np.kron(x, [1] * scanner.nb_blocks_per_ring)
    yy = np.kron(y, [1] * scanner.nb_blocks_per_ring)
    theta = 2 * np.pi / scanner.nb_blocks_per_ring * np.arange(scanner.nb_blocks_per_ring)
    theta1 = np.kron(theta, [[1]] * scanner.blocks.shape[1]).ravel()
    xd = xx * np.cos(theta1) - yy * np.sin(theta1)
    yd = xx * np.sin(theta1) + yy * np.cos(theta1)
    zd = np.kron(z, [1] * scanner.blocks.shape[1] * scanner.nb_blocks_per_ring)

    lors[:, 0] = np.kron(xd, [1] * scanner.nb_detectors_per_thin_ring)
    lors[:, 1] = np.kron(yd, [1] * scanner.nb_detectors_per_thin_ring)
    lors[:, 2] = np.kron(zd, [1] * scanner.nb_detectors_per_thin_ring)
    lors[:, 3] = np.kron(xd, [[1]] * scanner.nb_detectors_per_thin_ring).ravel()
    lors[:, 4] = np.kron(yd, [[1]] * scanner.nb_detectors_per_thin_ring).ravel()
    lors[:, 5] = np.kron(zd, [[1]] * scanner.nb_detectors_per_thin_ring).ravel() + d * \
                 scanner.blocks.unit_size[2]

    return lors
