import os
import pytest
import shutil
import subprocess
from invoke.context import Context
from pathlib import Path

from civilservant.tasks.utils.pipenv import Pipenv, PIPENV

PACKAGE_PREFIX = "civilservant-"
PIPFILE = "Pipfile"
TEMP_ENV = {
    "LANG": os.environ["LANG"],
    "PATH": str(Path(shutil.which("git")).parent),
    "PIPENV_VENV_IN_PROJECT": "1",
    "PYTHONPATH": os.environ["PYTHONPATH"]
}

@pytest.fixture
def current_pipenv():
    return Pipenv(context = Context(), package_prefix=PACKAGE_PREFIX)

@pytest.fixture
def temp_pipenv(temp_pipenv_environment):
    return Pipenv(context = Context(),
                  root_path = temp_pipenv_environment,
                  package_prefix=PACKAGE_PREFIX)

@pytest.fixture(scope="session")
def temp_pipenv_environment(tmp_path_factory):
    path = tmp_path_factory.getbasetemp()
    pipenv_cmd = [PIPENV, "install"]
    
    assert not Path(path, PIPFILE).exists()
    subprocess.run(pipenv_cmd, cwd=path, env=TEMP_ENV).check_returncode()
    assert Path(path, PIPFILE).exists()

    return path


