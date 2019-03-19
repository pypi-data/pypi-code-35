"""
test aws_lambda_sls.
"""
import os
from click.testing import CliRunner
from aws_lambda_sls import cli
from aws_lambda_sls.factory import CLIFactory


def _run_cli_command(function, args, project_dir=None, cli_factory=None):
    if project_dir is None:
        project_dir = os.getcwd()
    else:
        project_dir = os.path.abspath(project_dir)
    if cli_factory is None:
        cli_factory = CLIFactory(project_dir)
    return CliRunner().invoke(
        function, args, obj={
            'project_dir': project_dir,
            'debug': False,
            'factory': cli_factory
        }
    )


def test_cli_create_new_project():
    result = CliRunner().invoke(cli.new_project, ['dw'])
    assert result.exit_code == 0, result.exception


def test_cli_package_project():
    result = _run_cli_command(cli.package, [], project_dir="./dw")
    assert result.exit_code == 0, result.exception


def test_cli_deploy_project():
    result = _run_cli_command(cli.deploy, [], project_dir="./dw")
    assert result.exit_code == 0, result.exception


def test_cli_local_server():
    result = _run_cli_command(cli.local, ["--host", "192.168.5.65"], project_dir="./dw")
    assert result.exit_code == 0, result.exception


if __name__ == '__main__':
    test_cli_deploy_project()
