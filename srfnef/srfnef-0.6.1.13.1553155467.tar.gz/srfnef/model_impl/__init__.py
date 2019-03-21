# encoding: utf-8
'''
@author: Minghao Guo
@contact: mh.guo0111@gmail.com
@software: srf_ct
@file: __init__.py
@date: 2/26/2019
@desc:
'''

# from srfnef.typing import TYPE_BIND
from ._bproj_siddon import bproj_siddon, bproj_siddon_cuda
from ._proj_siddon import proj_siddon, proj_siddon_cuda
#
# TYPE_BIND.update({'BackProjectorDistanceDriven': BackProjectorDistanceDriven,
#                   'BackProjectorSiddon': BackProjectorSiddon,
#                   'ProjectorDistanceDriven': ProjectorDistanceDriven,
#                   'ProjectorSiddon': ProjectorSiddon})
