import io

import pytest

from ktdk import KTDK, Test
from ktdk.scenarios.simple import InOutFileScenario
from ktdk.tasks.cpp import RawCompilerTask
from tests.utils import get_test_context


@pytest.fixture
def context(prepared_dir):
    config = dict(workspace=prepared_dir, devel=True)
    return get_test_context(suite_config=config, test_config={})


@pytest.fixture()
def workspace(tmpdir):
    return tmpdir.mkdir('workspace')


@pytest.fixture()
def ktdk_instance(workspace):
    return KTDK(
        workspace=workspace,
        devel=True
    )


@pytest.fixture
def prepared_dir(tmpdir, workspace):
    c_file = workspace.join('main.c')
    c_file.write("""
        #include <stdio.h>\n
        #include <string.h>\n
        int main(int argc, char *argv[]) {
            for(int i = 1; i < argc; i++) {
                puts(argv[i]);
            }
            char buffer[256];
            fgets(buffer, 255, stdin);
            puts(buffer);
            return 0; 
        }
    """)
    return workspace


@pytest.fixture()
def scenario(prepared_dir):
    test = Test(name="Simple test")
    test.add_task(RawCompilerTask(compiler='gcc', executable='hello', files=['main.c']))
    scenario = InOutFileScenario(
        executable='hello',
        stdout=io.StringIO("hello\n"),
        stdin=io.StringIO("hello"),
    )
    test.add_task(scenario)
    return test


def test_compile_tasks(ktdk_instance, scenario):
    ktdk_instance.suite.add_test(scenario)
    result = ktdk_instance.run()
    assert result
    assert ktdk_instance.suite.result.effective.passed
