# pylint: disable=missing-docstring
import shutil
import os

from os.path import join
from textwrap import dedent

import pytest

from .context import opentea, Project, viewer3d_case_utilities

import numpy as np


# class Testviewer3d_case_utilities(Project):
#     @classmethod
#     def setup_class(cls):
#         super(Testviewer3d_case_utilities, cls).setup_class()
#         view = viewer3d_case_utilities
#         cls.dts = opentea.Dataset(cls.xml_file)
#         cls.view = view.View3dObject(cls.dts,
#                                      "test1", "view_3d_energydeposit",
#                                      default_color="#ff9d00",
#                                      default_aspect="edges")
# 
#     def test_dump_nopart(self):
#         self.view.dump()
# 
#     def test_dump_withpart(self):
#         self.view.add_part("energy_depot")
#         self.view.dump()
