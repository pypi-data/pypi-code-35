# pylint: disable=missing-docstring
from os.path import join
import pytest

from .context import opentea, Project, data3d
from opentea import data3d
import numpy as np
import math

class Testdata3d(Project):
    @classmethod
    def setup_class(cls):
        super(Testdata3d, cls).setup_class()
        cls.pro = opentea.BaseProcess(
            dataset_name=join(cls.project_path, "dataset.xml"))

    # really necessary?
    def test_norm(self):
        dict1 = {"x": 1.0, "y": 1.0, "z": 0.0}
        item = data3d.norm(dict1)
        assert np.abs(item - np.sqrt(2)) < 0.000001

    def test_rotate(self):
        float1 = 1.0
        float2 = 1.0
        listres = [-1.0, 1.0]
        res = data3d.rotate(float1, float2, 90)
        assert all([np.abs(res[i] - listres[i]) < 0.00001 for i in
                    range(len(res))])
