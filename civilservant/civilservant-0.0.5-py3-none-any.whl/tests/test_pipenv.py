import os
import multiprocessing
import subprocess

from tests.fixtures.pipenv import *
from civilservant.tasks.utils.pipenv import Pipenv, PIPENV

INSTALL_TEST_PACKAGE = "pytest"
INSTALL_TEST_REPO = "git+https://github.com/kennethreitz/requests#egg=requests"
INSTALL_TEST_REPO_PACKAGE = "requests"

def _run_with_clean_env(function):
    def clean_function():
        os.environ = TEMP_ENV
        function()
    proc = multiprocessing.Process(target=clean_function)
    proc.start()
    proc.join()

def test_ensure_active_while(current_pipenv):
    assert current_pipenv.ensure_active()

def test_has_package(current_pipenv):
    assert current_pipenv.has_package("civilservant")

def test_get_root_path(current_pipenv):
    cmd = [PIPENV, "--where"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    result.check_returncode()
    assert current_pipenv.root_path == Path(result.stdout.rstrip())

def test_get_venv_path(current_pipenv):
    cmd = [PIPENV, "--venv"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    result.check_returncode()
    assert current_pipenv.venv_path == Path(result.stdout.rstrip())

def test_load_pipfile(current_pipenv):
    pipfile = current_pipenv.load_pipfile()
    #assert "packages" in pipfile
    assert "dev-packages" in pipfile
    assert "source" in pipfile

def test_install_from_github(temp_pipenv):
    pipfile = temp_pipenv.load_pipfile()
    assert INSTALL_TEST_REPO_PACKAGE not in pipfile["packages"]
    _run_with_clean_env(lambda: temp_pipenv.install(INSTALL_TEST_REPO))
    pipfile = temp_pipenv.load_pipfile()
    assert INSTALL_TEST_REPO_PACKAGE in pipfile["packages"]

def test_install_from_pip(temp_pipenv):
    pipfile = temp_pipenv.load_pipfile()
    assert INSTALL_TEST_PACKAGE not in pipfile["packages"]
    _run_with_clean_env(lambda: temp_pipenv.install(INSTALL_TEST_PACKAGE))
    pipfile = temp_pipenv.load_pipfile()
    assert INSTALL_TEST_PACKAGE in pipfile["packages"]

def test_run(temp_pipenv, temp_pipenv_environment):
    test_text = "this is a test of the emergency broadcast system"
    test_file = Path(temp_pipenv_environment, "test_file.txt")
    temp_pipenv.run(f"echo {test_text} > {test_file}")
    with test_file.open() as f:
        assert f.read().rstrip() == test_text

