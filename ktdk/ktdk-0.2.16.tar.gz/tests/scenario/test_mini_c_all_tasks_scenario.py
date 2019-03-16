import os
import shutil

import pytest

from ktdk import KTDK, Test
from ktdk.scenarios.c import mini
from tests.paths import TEST_RESOURCES_BASE


@pytest.fixture
def workspace_dir(tmpdir):
    workspace = tmpdir.mkdir('workspace')
    return workspace


@pytest.fixture
def test_files_dir(tmpdir):
    test_files = tmpdir.mkdir('test_files')
    return test_files


@pytest.fixture
def submission_dir(tmpdir):
    submission = tmpdir.mkdir('submission')
    return submission


@pytest.fixture()
def prepared_sources(submission_dir):
    path = os.path.join(submission_dir, 'src')
    shutil.copytree(str(TEST_RESOURCES_BASE / 'c_mini'), path)
    return path


@pytest.fixture()
def mini_test():
    mini_test = Test(name="MiniTest", desc="Super mini test")
    mini_scenario = mini.CMiniAllTasksScenario(points=1)
    mini_test.add_task(mini_scenario)
    return mini_test


@pytest.fixture()
def naostro(mini_test):
    naostro = Test(name="naostro", desc="Test naostro", tags=['naostro'])
    naostro.add_test(mini_test)
    return naostro


@pytest.fixture()
def ktdk(workspace_dir, test_files_dir, prepared_sources, naostro):
    ktdk = KTDK(
        test_files=prepared_sources,
        submission=prepared_sources,
        workspace=workspace_dir,
        devel=True
    )
    ktdk.suite.add_test(naostro)
    return ktdk


def test_run_the_scenario(prepared_sources, ktdk):
    ktdk.invoke()
    assert ktdk.suite.result.effective.passed
    assert round(ktdk.suite.result.effective_points, 3) == 1
