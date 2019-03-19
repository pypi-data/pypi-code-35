import pytest
import click
from click.testing import CliRunner
from os import path
from sib.cli import main as cli

class TestCli(object):

    """Test the process of project creation"""

    def test_startproject_by_folder(self, tmp_path):

        runner = CliRunner()
        result = runner.invoke(cli, ['startproject', 'sibtest', path.join(tmp_path, 'sibtest')])
        assert result.exit_code == 0
