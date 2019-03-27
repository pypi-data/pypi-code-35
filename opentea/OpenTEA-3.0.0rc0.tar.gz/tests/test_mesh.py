# pylint: disable=missing-docstring

from os.path import join

import pytest

from .context import opentea, Project


class TestMesh3D(Project):
    @classmethod
    def setup_class(cls):
        super(TestMesh3D, cls).setup_class()
        cls.pro = opentea.BaseProcess(
            dataset_name=join(cls.project_path, "dataset.xml"))
        cls.mes = opentea.Mesh("tests/data/mesh3D.mesh.h5", cls.pro)

    def test_get_infos(self):
        self.mes.get_infos()
        assert abs(self.mes.voldomain - 1) < 1e-6


class TestMesh2D_quad(Project):
    @classmethod
    def setup_class(cls):
        super(TestMesh2D_quad, cls).setup_class()
        cls.pro = opentea.BaseProcess(
            dataset_name=join(cls.project_path, "dataset.xml"))
        cls.mes = opentea.Mesh("tests/data/mesh2D_quad.mesh.h5", cls.pro)

    def test_get_infos(self):
        self.mes.get_infos()
        assert abs(self.mes.voldomain - 1) < 1e-6


class TestMesh2D_tri(Project):
    @classmethod
    def setup_class(cls):
        super(TestMesh2D_tri, cls).setup_class()
        cls.pro = opentea.BaseProcess(
            dataset_name=join(cls.project_path, "dataset.xml"))
        cls.mes = opentea.Mesh("tests/data/mesh2D_tri.mesh.h5", cls.pro)

    def test_get_infos(self):
        self.mes.get_infos()
        assert abs(self.mes.voldomain - 1) < 1e-6


class TestMesh2D_avbp62(Project):
    @classmethod
    def setup_class(cls):
        super(TestMesh2D_avbp62, cls).setup_class()
        cls.pro = opentea.BaseProcess(
            dataset_name=join(cls.project_path, "dataset.xml"))
        cls.mes = opentea.Mesh("tests/data/62mesh/mesh.mesh.h5",
                               cls.pro)

    # Important: This test must be performed before get_infos as the previous
    # will modify the mesh_version and update it to the latest.
    def test_get_mesh_version(self):
        assert self.mes.get_mesh_version() == '01.42.02'

    @pytest.mark.exec_dependency
    def test_get_infos(self):
        self.mes.get_infos()
        assert abs(self.mes.voldomain - 9.375e-05) < 1.e-10

    @pytest.mark.exec_dependency
    def test_execute_meshsample(self):
        prefix = 'fluid'
        self.mes.execute_meshsample(prefix)
