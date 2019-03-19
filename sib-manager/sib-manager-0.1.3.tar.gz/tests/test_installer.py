import pytest
import click
from click.testing import CliRunner
from os import path
from sib.installer import Installer

class TestInstaller(object):

    @pytest.fixture(autouse=True)
    def setup(self, tmp_path):
        self.installer = Installer("sibtest", path.join(tmp_path,'sibtest'), True)

    def test_create_project(self):
        result = self.installer.create_project()
        assert result == True
