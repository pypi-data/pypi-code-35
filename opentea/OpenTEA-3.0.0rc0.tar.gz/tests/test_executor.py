# pylint: disable=missing-docstring
from .context import opentea


class TestExecutorCode(object):
    @classmethod
    def setup_class(cls):
        pass
        # cls.pro = opentea.CodeProcess(dataset_name="tests/data/example_lite.xml")
        # cls.exe = opentea.Executor(cls.pro, '-code_exe-')

    def test_copy_file_temp(self):
        return True


class TestExecutorTool(object):
    @classmethod
    def setup_class(cls):
        pass
        # cls.pro = opentea.BaseProcess(dataset_name="tests/data/example_lite.xml")
        # cls.exe = opentea.Executor(cls.pro, '-tool-')

    def test_copy_file_temp(self):
        return True

