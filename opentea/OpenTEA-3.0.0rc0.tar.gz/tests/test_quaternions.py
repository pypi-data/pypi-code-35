# pylint: disable=missing-docstring
from os.path import join
import pytest

from .context import opentea, Project, quaternions
import numpy as np
import math

#@pytest.fixture(scope='module')
#def resource_a_setup(request):
#    print('\nresources_a_setup()')
#    def resource_a_teardown():
#        print('\nresources_a_teardown()')
#    request.addfinalizer(resource_a_teardown)

#def setup_module(module):
#    print('\nsetup_module()')
#    resource_a_setup()

#def teardown_module(module):
#    print('\nteardown_module()')
#    resource_a_teardown()

#def test_vect_normalize(resource_a_setup):
#    print "works"
#    assert (vect_normalize((1.0, 1.0))



class Testquaternions(Project):
    @classmethod
    def setup_class(cls):
        super(Testquaternions, cls).setup_class()
        cls.pro = opentea.BaseProcess(
            dataset_name=join(cls.project_path, "dataset.xml"))

    def test_vect_normalize(self):
        tuple1 = quaternions.vect_normalize((1.0, 1.0)) 
        tuple2 = (np.sqrt(2)/2, np.sqrt(2)/2)
        assert all([np.abs(a-b) < 0.00001 for a, b in zip(tuple1, tuple2)])
               
    def test_tuple_plus(self):
        tuple1 = quaternions.tuple_plus((1.0, 1.0), (2.0, 2.0)) 
        assert tuple1 == (3.0, 3.0) 

    def test_tuple_minus(self):
        tuple1 = quaternions.tuple_minus((1.0, 1.0), (2.0, 2.0)) 
        assert tuple1 == (-1.0, -1.0) 

    def test_quat_mult(self):
        tuple1 = (1.0, 0.0, 1.0, 0.0)
        tuple2 = (1.0, 0.5, 0.5, 0.75)
        assert quaternions.quat_mult(tuple1, tuple2) == (0.5, 1.25, 1.5, 0.25)

    def test_quat_conjugate(self):
        tuple1 = (1.0, 2.0, 1.0, 0.0)
        assert (quaternions.quat_conjugate(tuple1) == 
                quaternions.vect_normalize((1.0, -2.0, -1.0, 0.0)))

    def test_quat_axisangle_to_quat(self):
        tuple1 = (1.0, 0.0, 0.0)
        tuple2 = (np.sqrt(2)/2, np.sqrt(2)/2, 0.0, 0.0)
        res = quaternions.axisangle_to_quat(tuple1, math.pi/2)
        assert all([np.abs(a - b) < 0.00001
                    for a, b in zip(res, tuple2)])
