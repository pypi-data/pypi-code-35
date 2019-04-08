# encoding: utf-8
'''
srfnef.adapter
~~~~~~~~~~~~~~

This module provides adapters to used to match the form srf package.
'''

import json

import h5py
import numpy as np

from srfnef.data_types import Block, PetCylindricalScanner, Lors, Listmode


def _block_from_API(path):
    with open(path, 'r') as fin:
        dct = json.load(fin)
        _shape = dct['scanner']['petscanner']['block']['grid']
        _size = dct['scanner']['petscanner']['block']['size']
        _block = Block(_size, _shape)
        return _block


def _scanner_from_API(path):
    _block = _block_from_API(path)
    with open(path, 'r') as fin:
        dct = json.load(fin)
        _inner_radius = dct['scanner']['petscanner']['ring']['inner_radius']
        _outer_radius = dct['scanner']['petscanner']['ring']['outer_radius']
        _nb_rings = dct['scanner']['petscanner']['ring']['nb_rings']
        _nb_blocks_per_ring = dct['scanner']['petscanner']['ring']['nb_blocks_per_ring']
        _gap = dct['scanner']['petscanner']['ring']['gap']
        _scanner = PetCylindricalScanner(_inner_radius, _outer_radius, _nb_rings,
                                         _nb_blocks_per_ring, _gap, _block)
        return _scanner


def load_listmode_from_h5(path, scanner, *, cut_number = None, compress = True):
    ''' Load old typed listmode data in form of `'.h5`. It stored lors in a `fst` dataset
    and a `snd` dataset. Duplicate lors may appears.

    This function load the h5 file aforementioned and transform it to well-suited `Listmode`
    DataClass tyoe. It will merge repeated lors to valued listmode data.

    '''
    with h5py.File(path, 'r') as fin:
        fst = np.array(fin['listmode_data']['fst'])
        snd = np.array(fin['listmode_data']['snd'])
    if cut_number is not None:
        fst = fst[:cut_number, :]
        snd = snd[:cut_number, :]
    if compress:
        return Listmode.from_lors(Lors.from_fst_snd(fst, snd)).compress(scanner)
    else:
        return Listmode.from_lors(Lors.from_fst_snd(fst, snd))
