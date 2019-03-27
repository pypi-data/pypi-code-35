import shutil
import sys
import os

from os.path import abspath, join, dirname

sys.path.insert(0, abspath(join(dirname(__file__), '..')))
import opentea
from opentea import quaternions, data3d, geometry, viewer3d_case_utilities


class Project(object):
    project_path = abspath(join(dirname(__file__),
                                "data",
                                "test_project",
                                "project"))
    xml_file = join(project_path, "dataset.xml")

    @classmethod
    def setup_class(cls):
        try:
            os.mkdir(cls.project_path)
        except OSError:
            cls.teardown_class()
            os.mkdir(cls.project_path)
        shutil.copy(join(cls.project_path, "..", "project.xml"),
                    join(cls.project_path, "dataset.xml"))

    @classmethod
    def teardown_class(cls):
        shutil.rmtree(cls.project_path)
