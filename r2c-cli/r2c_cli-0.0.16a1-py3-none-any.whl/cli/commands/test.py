import os
import sys

import click

from r2c.cli.commands.cli import cli
from r2c.cli.logger import (
    abort_on_build_failure,
    print_error_exit,
    print_msg,
    print_success,
)
from r2c.cli.network import get_registry_data
from r2c.cli.util import find_and_open_analyzer_manifest, parse_remaining
from r2c.lib.errors import SymlinkNeedsElevationError
from r2c.lib.run import build_docker, integration_test, run_docker_unittest
from r2c.lib.versioned_analyzer import VersionedAnalyzer


@cli.command()
@click.option("--analyzer-directory", default=os.getcwd())
@click.argument("env-args-string", nargs=-1, type=click.Path())
@click.pass_context
def unittest(ctx, analyzer_directory, env_args_string):
    """
    Locally unit tests for the current analyzer directory.

    You can define how to run your unit tests in `src/unittest.sh`.

    You may have to login if your analyzer depends on privately
    published analyzers.
    """
    verbose = ctx.obj["VERBOSE"]
    env_args_dict = parse_remaining(env_args_string)

    manifest, analyzer_directory = find_and_open_analyzer_manifest(
        analyzer_directory, ctx
    )

    print_msg("🔨 Building docker container")
    abort_on_build_failure(
        build_docker(
            manifest.analyzer_name,
            manifest.version,
            os.path.relpath(analyzer_directory, os.getcwd()),
            env_args_dict=env_args_dict,
            verbose=verbose,
        )
    )

    image_id = VersionedAnalyzer(manifest.analyzer_name, manifest.version).image_id

    status = run_docker_unittest(
        analyzer_directory=analyzer_directory,
        analyzer_name=manifest.analyzer_name,
        docker_image=image_id,
        verbose=verbose,
        env_args_dict=env_args_dict,
    )
    if status == 0:
        print_success(f"Unit tests passed")
        sys.exit(0)
    else:
        print_error_exit(f"Unit tests failed with status {status}", status_code=status)


@cli.command()
@click.option("-d", "--analyzer-directory", default=os.getcwd())
@click.argument("env-args-string", nargs=-1, type=click.Path())
@click.pass_context
def test(ctx, analyzer_directory, env_args_string):
    """
    Locally run integration tests for the current analyzer.

    You can add integration test files to the `examples/` directory.
    For more information, refer to the integration test section of the README.

    You may have to login if your analyzer depends on privately
    published analyzers.
    """

    verbose = ctx.obj["VERBOSE"]
    env_args_dict = parse_remaining(env_args_string)
    print_msg(
        f"Running integration tests for analyzer {'with debug mode' if ctx.obj['DEBUG'] else ''}"
    )

    manifest, analyzer_directory = find_and_open_analyzer_manifest(
        analyzer_directory, ctx
    )

    print_msg("🔨 Building docker container")
    abort_on_build_failure(
        build_docker(
            manifest.analyzer_name,
            manifest.version,
            os.path.relpath(analyzer_directory, os.getcwd()),
            env_args_dict=env_args_dict,
            verbose=verbose,
        )
    )

    try:
        integration_test(
            manifest=manifest,
            analyzer_directory=analyzer_directory,
            workdir=None,
            env_args_dict=env_args_dict,
            registry_data=get_registry_data(),
        )
        print_success(f"Integration tests passed")
    except SymlinkNeedsElevationError as sym:
        print_error_exit(
            f"Error setting up integration tests. {sym}. Try again as an admin"
        )
