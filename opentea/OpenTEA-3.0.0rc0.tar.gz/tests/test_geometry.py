# pylint: disable=missing-docstring
import pytest
import numpy as np
import math

from .context import opentea, geometry, Project

 
class TestParallelogram(Project):
    @classmethod
    def setup_class(cls):
        super(TestParallelogram, cls).setup_class()

    def test_area(self):
        rectangle = geometry.Parallelogram(np.array([1.0, 0.0]),
                                           (1.0, 1.0), (0.0, 2.0))
        assert rectangle.area() == 2.0

    def test_project(self):
        rectangle = geometry.Parallelogram(np.array([1.0, 0.0]),
                                           (1.0, 1.0), (0.0, 2.0))
        assert np.sum(np.subtract(rectangle.project((4.0, 1.0)),
                                  (3.5, 0.5))) < 1.e-12

    def test_is_inside(self):
        rectangle = geometry.Parallelogram(np.array([1.0, 0.0]),
                                           (1.0, 1.0), (0.0, 2.0))
        assert rectangle.is_inside((1.5, 0.6)) == 1 

    def test_is_notinside(self):
        rectangle = geometry.Parallelogram(np.array([1.0, 0.0]),
                                           (1.0, 1.0), (0.0, 2.0))
        assert not rectangle.is_inside((0.5, -0.4)) == 1 


class TestParallelepiped(Project):
    @classmethod
    def setup_class(cls):
        super(TestParallelepiped, cls).setup_class()

    def test_area_cube(self):
        cube = geometry.Parallelepiped(np.array([1.0, 2.0, 0.0]),
                                       (1.0, 0.0, 0.0),
                                       (0.0, 2.0, 0.0),
                                       (0.0, 0.0, 4.0))
        assert np.abs(cube.volume() - 8.0) < 1.0e-12

    def test_project_cube(self):
        cube = geometry.Parallelepiped(np.array([1.0, 2.0, 0.0]),
                                       (1.0, 0.0, 0.0),
                                       (0.0, 2.0, 0.0),
                                       (0.0, 0.0, 4.0))
        assert np.sum(np.subtract(cube.project((4.0, 1.0, 3.0)),
                                  (3.5, 0.5, 0.75))) < 1.e-12

    def test_is_inside_cube(self):
        cube = geometry.Parallelepiped(np.array([1.0, 2.0, 0.0]),
                                       (1.0, 0.0, 0.0),
                                       (0.0, 2.0, 0.0),
                                       (0.0, 0.0, 4.0))
        assert cube.is_inside((1.5, 2.4, 2.0)) == 1 

    def test_is_notinside_cube(self):
        cube = geometry.Parallelepiped(np.array([1.0, 2.0, 0.0]),
                                       (1.0, 0.0, 0.0),
                                       (0.0, 2.0, 0.0),
                                       (0.0, 0.0, 4.0))
        assert not cube.is_inside((0.4, -0.4, 2.0)) == 1 


class TestCircle(Project):
    @classmethod
    def setup_class(cls):
        super(TestCircle, cls).setup_class()

    def test_area_circle(self):
        circle = geometry.Circle(np.array([0.0, 0.0]), 2.0)
        assert np.abs(circle.area() - 4. * math.pi) < 1.0e-12

    def test_is_inside_circle(self):
        circle = geometry.Circle(np.array([0.0, 0.0]), 2.0)
        assert circle.is_inside(np.array([1.9, 0.0])) == 1

    def test_is_notinside_circle(self):
        circle = geometry.Circle(np.array([0.0, 0.0]), 2.0)
        assert not circle.is_inside(np.array([2.1, 0.0])) == 1


class TestSphere(Project):
    @classmethod
    def setup_class(cls):
        super(TestSphere, cls).setup_class()

    def test_volume_sphere(self):
        sphere = geometry.Sphere(np.array([0.0, 0.0, 0.0]), 2.0)
        assert np.abs(sphere.volume() - 4./3 * math.pi * 8) < 1.0e-12

    def test_is_inside_sphere(self):
        sphere = geometry.Sphere(np.array([0.0, 0.0, 0.0]), 2.0)
        assert sphere.is_inside(np.array([1.9, 0.0, 0.0])) == 1

    def test_is_notinside_sphere(self):
        sphere = geometry.Sphere(np.array([0.0, 0.0, 0.0]), 2.0)
        assert not sphere.is_inside(np.array([2.1, 0.0, 0.0])) == 1


class TestCylinder(Project):
    @classmethod
    def setup_class(cls):
        super(TestCylinder, cls).setup_class()

    def test_volume_cylinder(self):
        cylinder = geometry.Cylinder(np.array([0.0, 0.0, 0.0]),
                                     2.0, (0.0, 0.0, 1.0))
        assert np.abs(cylinder.volume() - math.pi * 4) < 1.0e-12

    def test_is_inside_cylinder(self):
        cylinder = geometry.Cylinder(np.array([0.0, 0.0, 0.0]),
                                     2.0, (0.0, 0.0, 1.0))
        assert cylinder.is_inside((1.2, 1.2, 0.5)) == 1

    def test_is_notinside_cylinder(self):
        cylinder = geometry.Cylinder(np.array([0.0, 0.0, 0.0]),
                                     2.0, (0.0, 0.0, 1.0))
        assert not cylinder.is_inside((1.9, 2.1, 0.5)) == 1
