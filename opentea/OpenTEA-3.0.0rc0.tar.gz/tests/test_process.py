# pylint: disable=missing-docstring
import os
import re
from os.path import isdir, isfile, join

from .context import opentea, Project


class TestBaseProcess(Project):
    @classmethod
    def setup_class(cls):
        super(TestBaseProcess, cls).setup_class()
        cls.pro = opentea.BaseProcess(
            dataset_name=join(cls.project_path, "dataset.xml"))

    def test_structure(self):
        assert isdir(join(self.project_path, opentea.constants.COMMON))

    def test_finish(self):
        self.pro.finish()
        assert isfile(join(self.project_path, "out_dataset.xml"))

    def test_loadmesh(self):
        mesh = self.pro.loadmesh("tests/data/mesh3D.mesh.h5")
        assert mesh.__class__ == opentea.Mesh

    def test_get_executor(self):
        exe = self.pro.get_executor("test")
        assert exe.__class__ == opentea.Executor

    def test_progress(self):
        pattern = re.compile(r"^\ {0,2}\d{1,3}%.*$")
        progr = self.pro.progress(0.6, "Hello world")
        assert pattern.match(progr)


class TestBaseProcessChdir(Project):
    @classmethod
    def setup_class(cls):
        super(TestBaseProcessChdir, cls).setup_class()
        cls.pro = opentea.BaseProcess(
            dataset_name=join(cls.project_path, "dataset.xml"))

    def test_finish_change_dir(self):
        start_dir = os.getcwd()
        os.chdir('..')
        self.pro.finish()
        assert os.getcwd() == start_dir


class TestCodeProcess(Project):
    @classmethod
    def setup_class(cls):
        super(TestCodeProcess, cls).setup_class()
        cls.pro = opentea.CodeProcess(
            dataset_name=join(cls.project_path, "dataset.xml"))

    def test_structure(self):
        assert isdir(join(self.project_path, opentea.constants.COMMON))
        assert isdir(join(self.project_path, "RUN_CURRENT"))

    def test_run_dirs(self):
        assert self.pro.this_run is None
        assert self.pro.next_run == "RUN_001"

    def test_write_case(self):
        self.pro.write_case()
        assert isdir(join(self.project_path, "RUN_001"))
        assert isfile(join(self.project_path, "RUN_001", "RUN_001.xml"))


class TestLibProcess(Project):
    @classmethod
    def setup_class(cls):
        super(TestLibProcess, cls).setup_class()
        cls.pro = opentea.LibProcess(
            dataset_name=join(cls.project_path, "dataset.xml"))
