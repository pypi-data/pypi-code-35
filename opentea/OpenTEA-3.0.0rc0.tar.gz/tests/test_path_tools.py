# pylint: disable=missing-docstring
import shutil
import os

import pytest

from os.path import abspath, join, isfile, isdir

from .context import opentea


class TestPathTools(object):
    @classmethod
    def setup_class(cls):
        cls.ptl = opentea.PathTools()
        cls.tmp = "./TMP_TESTS"
        cls.sub = "./TMP_TESTS/SUB"
        cls.dum = "./TMP_TESTS/dummy.txt"
        os.makedirs(cls.sub)
        with open(cls.dum, 'w') as dum:
            dum.write("contents")

    def teardown_class(cls):
        shutil.rmtree(cls.tmp)

    def test_abspath(self):
        assert self.ptl.abspath(self.dum) == abspath(self.dum)

    def test_relpath(self):
        assert self.ptl.relpath(abspath(self.dum)) == self.dum

    def test_copy_file(self):
        dest = join(self.sub, "dummy.txt")
        final = self.ptl.copy_file(self.dum, dest)
        assert final == abspath(dest)
        assert isfile(dest)

    def test_move_file(self):
        copy = join(self.sub, "dummy.txt")
        dest = join(self.sub, "dummy_moved.txt")
        self.ptl.copy_file(self.dum, dest)
        final = self.ptl.move_file(copy, dest)
        assert final == abspath(dest)
        assert isfile(dest)

    def test_copy_dir_rename(self):
        dest = join(self.tmp, "SUB2")
        self.ptl.copy_dir(self.sub, dest)
        assert isdir(dest)

    def test_copy_dir_slash(self):
        dest = join(self.tmp, "SUB2/")
        self.ptl.ensure_dir(dest)
        self.ptl.copy_dir(self.sub, dest)
        assert isdir(join(dest, "SUB"))

    def test_copy_dir_to_file(self):
        with pytest.raises(OSError):
            self.ptl.copy_dir(self.sub, self.dum)

    def test_copy_dir_from_file(self):
        with pytest.raises(OSError):
            self.ptl.copy_dir(self.dum, self.sub)

    def test_ensure_dir_already_exists(self):
        final = self.ptl.ensure_dir(self.sub)
        assert final == abspath(self.sub)
        assert isdir(self.sub)

    def test_ensure_dir_new(self):
        new = join(self.tmp, "SUB3")
        final = self.ptl.ensure_dir(new)
        assert final == abspath(new)
        assert isdir(new)

    def test_get_file_list(self):
        pass
        # file_list = self.ptl.get_file_list(self.tmp)
        # assert file_list == ['dummy.txt']
