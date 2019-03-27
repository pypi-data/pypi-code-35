# pylint: disable=missing-docstring
import os
from .context import opentea, Project
from os.path import join, abspath, dirname
from opentea import lazy_methods


class Testlazy_methods(object):
    def test_replace_pattern_in_file(self):
        project_path = abspath(join(dirname(__file__),
                                    "data",
                                    "test_project"))
        project_file = join(project_path, "file1.dat") 
        with open(project_file, 'w') as f:
            f.write("The quick brown fox jumps over the lazy dog")
        lazy_methods.replace_pattern_in_file(project_file, "fox", "hippo")
        lazy_methods.replace_pattern_in_file(project_file, "dog", "tiger")
        funny_situation = ("The quick brown hippo jumps over the lazy tiger")
        with open(project_file, 'r') as f:
            assert f.read() == funny_situation
        os.remove(project_file)

    def test_currentnext(self):
        item = list(range(3))
        a = lazy_methods.currentnext(item)
        assert a == [[0, 1], [1, 2]]
