#!/usr/bin/env python
# Copyright 2014-2018 The PySCF Developers. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Author: Qiming Sun <osirpt.sun@gmail.com>
#

import numpy

# D2h   C2h   C2v   D2   Cs   Ci   C2   C1
# E     E     E     E    E    E    E    E
# C2x               C2x
# C2y               C2y
# C2z   C2    C2    C2z            C2
# i     i                     i
# sx          sx
# sy          sy
# sz    sh                sh

POINTGROUP = ('D2h', 'C2h', 'C2v', 'D2' , 'Cs' , 'Ci' , 'C2' , 'C1' ,)

OPERATOR_TABLE = {
    'D2h': ('E', 'C2x', 'C2y', 'C2z', 'i', 'sx' , 'sy' , 'sz' ),
    'C2h': ('E',               'C2z', 'i',               'sz' ),
    'C2v': ('E',               'C2z',      'sx' , 'sy' ,      ),
    'D2' : ('E', 'C2x', 'C2y', 'C2z',                         ),
    'Cs' : ('E',                                         'sz' ),
    'Ci' : ('E',                      'i',                    ),
    'C2' : ('E',               'C2z',                         ),
    'C1' : ('E',                                              ),
}

#
IRREP_ID_TABLE = {      # bin for XOR
    'D2h': {'Ag' : 0,   # 000
            'B1g': 1,   # 001
            'B2g': 2,   # 010
            'B3g': 3,   # 011
            'Au' : 4,   # 100
            'B1u': 5,   # 101
            'B2u': 6,   # 110
            'B3u': 7,}, # 111
    'C2h': {'Ag': 0,    # 00
            'Bg': 1,    # 01
            'Au': 2,    # 10
            'Bu': 3,},  # 11
    'C2v': {'A1': 0,    # 00
            'A2': 1,    # 01
            'B1': 2,    # 10
            'B2': 3,},  # 11
    'D2' : {'A' : 0,    # 00
            'B1': 1,    # 01
            'B2': 2,    # 10
            'B3': 3,},  # 11
    'Cs' : {'A\'': 0,   # 0
            'A\"': 1,}, # 1
    'Ci' : {'Ag': 0,    # 0
            'Au': 1,},  # 1
    'C2' : {'A': 0,     # 0
            'B': 1,},   # 1
    'C1' : {'A': 0,},   # 0
}

IRREP_ID_MOLPRO = {'D2h': (1,   # Ag
                           4,   # B1g
                           6,   # B2g
                           7,   # B3g
                           8,   # Au
                           5,   # B1u
                           3,   # B2u
                           2),  # B3u
                   'C2v': (1,   # A1
                           4,   # A2
                           2,   # B1
                           3),  # B2
                   'C2h': (1,   # Ag
                           4,   # Bg
                           2,   # Au
                           3),  # Bu
                   'D2' : (1,   # A
                           4,   # B1
                           3,   # B2
                           2),  # B3
                   'Cs' : (1,   # A'
                           2),  # A"
                   'C2' : (1,   # A
                           2),  # B
                   'Ci' : (1,   # Ag
                           2),  # Au
                   'C1' : (1,)}

#                   E,C2x,C2y,C2z,i, sx,sy,sz
CHARACTER_TABLE = {                              # XOR
    'D2h': (('Ag' , 1, 1,  1,  1,  1, 1, 1, 1),  # 000
            ('B1g', 1,-1, -1,  1,  1,-1,-1, 1),  # 001
            ('B2g', 1,-1,  1, -1,  1,-1, 1,-1),  # 010
            ('B3g', 1, 1, -1, -1,  1, 1,-1,-1),  # 011
            ('Au' , 1, 1,  1,  1, -1,-1,-1,-1),  # 100
            ('B1u', 1,-1, -1,  1, -1, 1, 1,-1),  # 101
            ('B2u', 1,-1,  1, -1, -1, 1,-1, 1),  # 110
            ('B3u', 1, 1, -1, -1, -1,-1, 1, 1)), # 111
#                  E,C2,i, sh                    # XOR
    'C2h': (('Ag', 1, 1, 1, 1),                  # 00
            ('Bg', 1,-1, 1,-1),                  # 01
            ('Au', 1, 1,-1,-1),                  # 10
            ('Bu', 1,-1,-1, 1)),                 # 11
#                  E,C2,sx,sy                    # XOR
    'C2v': (('A1', 1, 1, 1, 1),                  # 00
            ('A2', 1, 1,-1,-1),                  # 01
            ('B1', 1,-1,-1, 1),                  # 10
            ('B2', 1,-1, 1,-1)),                 # 11
#                  E,C2x,C2y,C2z                 # XOR
    'D2' : (('A' , 1, 1,  1,  1),                # 00
            ('B1', 1,-1, -1,  1),                # 01
            ('B2', 1,-1,  1, -1),                # 10
            ('B3', 1, 1, -1, -1)),               # 11
#                  E, sh                         # XOR
    'Cs' : (('A\'',1, 1,),                       # 0
            ('A\"',1,-1,)),                      # 1
#                  E, i                          # XOR
    'Ci' : (('Ag', 1, 1,),                       # 0
            ('Au', 1,-1,)),                      # 1
#                 E, C2                          # XOR
    'C2' : (('A', 1, 1,),                        # 0
            ('B', 1,-1,)),                       # 1
#                 E                              # XOR
    'C1' : (('A', 1),),                          # 0
}

#     D2h   C2h   C2v   D2   Cs   Ci   C2   C1
SYMM_DESCENT_Z = (
    ('Ag' , 'Ag', 'A1', 'A' , 'A\'', 'Ag', 'A', 'A'),
    ('B1g', 'Ag', 'A2', 'B1', 'A\'', 'Ag', 'A', 'A'),
    ('B2g', 'Bg', 'B1', 'B2', 'A\"', 'Ag', 'B', 'A'),
    ('B3g', 'Bg', 'B2', 'B3', 'A\"', 'Ag', 'B', 'A'),
    ('Au' , 'Au', 'A2', 'A' , 'A\'', 'Au', 'A', 'A'),
    ('B1u', 'Au', 'A1', 'B1', 'A\'', 'Au', 'A', 'A'),
    ('B2u', 'Bu', 'B2', 'B2', 'A\"', 'Au', 'B', 'A'),
    ('B3u', 'Bu', 'B1', 'B3', 'A\"', 'Au', 'B', 'A'),
)
SYMM_DESCENT_X = (
    ('Ag' , 'Ag', 'A1', 'A' , 'A\'', 'Ag', 'A', 'A'),
    ('B1g', 'Bg', 'B2', 'B1', 'A\"', 'Ag', 'B', 'A'),
    ('B2g', 'Bg', 'B1', 'B2', 'A\"', 'Ag', 'B', 'A'),
    ('B3g', 'Ag', 'A2', 'B3', 'A\'', 'Ag', 'A', 'A'),
    ('Au' , 'Au', 'A2', 'A' , 'A\"', 'Au', 'A', 'A'),
    ('B1u', 'Bu', 'B1', 'B1', 'A\'', 'Au', 'B', 'A'),
    ('B2u', 'Bu', 'B2', 'B2', 'A\'', 'Au', 'B', 'A'),
    ('B3u', 'Au', 'A1', 'B3', 'A\"', 'Au', 'A', 'A'),
)
SYMM_DESCENT_Y = (
    ('Ag' , 'Ag', 'A1', 'A' , 'A\'', 'Ag', 'A', 'A'),
    ('B1g', 'Bg', 'B2', 'B1', 'A\"', 'Ag', 'B', 'A'),
    ('B2g', 'Ag', 'A2', 'B2', 'A\'', 'Ag', 'A', 'A'),
    ('B3g', 'Bg', 'B1', 'B3', 'A\"', 'Ag', 'B', 'A'),
    ('Au' , 'Au', 'A2', 'A' , 'A\"', 'Au', 'A', 'A'),
    ('B1u', 'Bu', 'B1', 'B1', 'A\'', 'Au', 'B', 'A'),
    ('B2u', 'Au', 'A1', 'B2', 'A\"', 'Au', 'A', 'A'),
    ('B3u', 'Bu', 'B2', 'B3', 'A\'', 'Au', 'B', 'A'),
)


SPHERIC_GTO_PARITY_ODD = (
# s
    ((0, 0, 0),),
# px, py, pz
    ((1, 0, 0),(0, 1, 0),(0, 0, 1)),
# dxy, dyz, dz2, dxz, dx2y2
    ((1, 1, 0),(0, 1, 1),(0, 0, 0),(1, 0, 1),(0, 0, 0),),
# fyx2, fxyz, fyz2, fz3, fxz2, fzx2, fx3
    ((0, 1, 0),(1, 1, 1),(0, 1, 0),(0, 0, 1),(1, 0, 0),
     (0, 0, 1),(1, 0, 0),),
# g
    ((1, 1, 0),(0, 1, 1),(1, 1, 0),(0, 1, 1),(0, 0, 0),
     (1, 0, 1),(0, 0, 0),(1, 0, 1),(0, 0, 0),),
# h
    ((0, 1, 0),(1, 1, 1),(0, 1, 0),(1, 1, 1),(0, 1, 0),
     (0, 0, 1),(1, 0, 0),(0, 0, 1),(1, 0, 0),(0, 0, 1),
     (1, 0, 0),),
# i
    ((1, 1, 0),(0, 1, 1),(1, 1, 0),(0, 1, 1),(1, 1, 0),
     (0, 1, 1),(0, 0, 0),(1, 0, 1),(0, 0, 0),(1, 0, 1),
     (0, 0, 0),(1, 0, 1),(0, 0, 0),),
# j
    ((0, 1, 0),(1, 1, 1),(0, 1, 0),(1, 1, 1),(0, 1, 0),
     (1, 1, 1),(0, 1, 0),(0, 0, 1),(1, 0, 0),(0, 0, 1),
     (1, 0, 0),(0, 0, 1),(1, 0, 0),(0, 0, 1),(1, 0, 0))
)

SUBGROUP = {
    'Dooh':('Coov', 'D2h', 'C2v', 'C2h', 'C2', 'Cs', 'Ci', 'C1'),
    'Coov':('C2v', 'C2', 'C1'),
    'D2h': ('D2h', 'C2v', 'C2h', 'C2', 'Cs', 'Ci', 'C1'),
    'C2v': ('C2v', 'C2' , 'Cs' , 'C1'),
    'C2h': ('C2h', 'C2' , 'Cs' , 'C1'),
    'D2' : ('D2' , 'C2' , 'Ci' , 'C1'),
    'Cs' : ('Cs' , 'C1'),
    'Ci' : ('Ci' , 'C1'),
    'C2' : ('C2' , 'C1'),
    'C1' : ('C1',),
}

D2H_OPS = {'E'  : numpy.eye(3),
           'C2z': numpy.diag((-1.,-1., 1.)),
           'C2x': numpy.diag(( 1.,-1.,-1.)),
           'C2y': numpy.diag((-1., 1.,-1.)),
           'i'  : numpy.diag((-1.,-1.,-1.)),
           'sz' : numpy.diag(( 1., 1.,-1.)),
           'sx' : numpy.diag((-1., 1., 1.)),
           'sy' : numpy.diag(( 1.,-1., 1.)),}
