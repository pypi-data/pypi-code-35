"""
Command line interface for aws_lambda_sls.
Contains commands for deploying aws_lambda_sls.

"""
import os
import platform
import sys
import traceback
import botocore.exceptions
import click
import logging

from aws_lambda_sls.constants import *
from aws_lambda_sls.factory import CLIFactory, validate_python_version
from aws_lambda_sls.utils import OSUtils


def run_local_server(factory, app_object, host, port, stage):
    server = factory.create_local_server(app_object, host, port, stage)
    server.serve_forever()


def create_new_project_skeleton(project_name):
    if not os.path.exists(project_name):
        os.makedirs(project_name)
    with open(os.path.join(project_name, 'app.py'), 'w') as f:
        f.write(TEMPLATE_APP % project_name)
    with open(os.path.join(project_name, '.gitignore'), 'w') as f:
        f.write(GITIGNORE)


def get_system_info():
    python_info = "python {}.{}.{}".format(sys.version_info[0],
                                           sys.version_info[1],
                                           sys.version_info[2])
    platform_system = platform.system().lower()
    platform_release = platform.release()
    platform_info = "{} {}".format(platform_system, platform_release)
    return "{}, {}".format(python_info, platform_info)


def config_logging(file_name=None):
    log_formatter = logging.Formatter("%(asctime)s: %(message)s")
    root_logger = logging.getLogger()

    if file_name:
        file_handler = logging.FileHandler(file_name)
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    root_logger.addHandler(console_handler)


@click.group()
@click.version_option(version=APP_VERSION,
                      message='%(prog)s %(version)s, {}'
                      .format(get_system_info()))
@click.option('--project-dir',
              help='The project directory.  Defaults to CWD')
@click.option('--debug/--no-debug',
              default=False,
              help='Print debug logs to stderr.')
@click.pass_context
def cli(ctx, project_dir, debug=False):
    if project_dir is None:
        project_dir = os.getcwd()
    else:
        project_dir = os.path.abspath(project_dir)
    ctx.obj['project_dir'] = project_dir
    ctx.obj['debug'] = debug
    ctx.obj["os_utils"] = OSUtils()
    ctx.obj['factory'] = CLIFactory(project_dir, debug, environ=os.environ)
    os.chdir(project_dir)


@cli.command('create-app')
@click.argument('project_name', required=True)
def create_app(project_name):
    if os.path.isdir(project_name):
        click.echo("Directory already exists: %s" % project_name, err=True)
        raise click.Abort()
    create_new_project_skeleton(project_name)
    validate_python_version()


@cli.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=8888, type=click.INT)
@click.option('--stage', default=DEFAULT_STAGE_NAME,
              help='Name of the sls stage for the local server to use.')
@click.option('--deploy-file', help='deployment file.')
@click.option('--log-file', help='output log file path.')
@click.pass_context
def local(ctx, host='127.0.0.1', port=8888, stage=DEFAULT_STAGE_NAME, deploy_file=None, log_file=None):
    factory, os_utils = ctx.obj['factory'], ctx.obj["os_utils"]
    if not deploy_file:
        deploy_file = os_utils.joinpath(
            ctx.obj['project_dir'],
            DEFAULT_PACKAGE_DIST,
            DEFAULT_PACKAGE_FILE
        )
    if not os.path.exists(deploy_file):
        click.echo("Deploy zipfile not exists: %s" % deploy_file, err=True)
        raise click.Abort()
    config_logging(log_file)
    project_dir = os_utils.joinpath(os.environ["HOME"], DEFAULT_LOCAL_DIST)
    os_utils.recreate_dir(project_dir)
    os_utils.extract_zipfile(deploy_file, project_dir)
    sys.path = [project_dir, os.path.dirname(os.__file__)]
    app_object = factory.load_app(project_dir)
    run_local_server(factory, app_object, host, port, stage)


@cli.command()
@click.option('--host', default='127.0.0.1')
@click.option('--port', default=8888, type=click.INT)
@click.option('--stage', default=DEFAULT_STAGE_NAME,
              help='Name of the sls stage for the local server to use.')
@click.option('--log-file', help='output log file path.')
@click.pass_context
def run(ctx, host='127.0.0.1', port=8888, stage=DEFAULT_STAGE_NAME, log_file=None):
    factory, os_utils = ctx.obj['factory'], ctx.obj["os_utils"]
    config_logging(log_file)
    project_dir = os_utils.joinpath(os.environ["HOME"], DEFAULT_LOCAL_DIST)
    if not os.path.exists(project_dir):
        click.echo("Sls project not exists: %s" % project_dir, err=True)
        raise click.Abort()
    sys.path = [project_dir, os.path.dirname(os.__file__)]
    app_object = factory.load_app(project_dir)
    run_local_server(factory, app_object, host, port, stage)


@cli.command()
@click.option('--stage', default=DEFAULT_STAGE_NAME,
              help=('Name of the sls stage to deploy to. '
                    'Specifying a new sls stage will create '
                    'an entirely new set of AWS resources.'))
@click.option('--profile', help='Override profile at deploy time.')
@click.option('--deploy-file', help='deployment file.')
@click.option('--s3-key', help='s3 file.')
@click.pass_context
def deploy(ctx, stage, profile, deploy_file, s3_key):
    factory, os_utils = ctx.obj['factory'], ctx.obj["os_utils"]
    if not deploy_file:
        deploy_file = factory.create_deploy_file(ctx.obj['project_dir'])
    if not (s3_key or os.path.exists(deploy_file)):
        click.echo("Deploy file not exists: %s" % deploy_file, err=True)
        raise click.Abort()
    deployer = factory.create_app_deployer(stage, profile)
    deployer.deploy_app(deploy_file, s3_key)


@cli.command('package')
@click.option('--generate-sam', is_flag=True, default=False,
              help=("Create a single packaged file. "
                    "By default, the 'out' argument "
                    "specifies a directory in which the "
                    "package assets will be placed.  If "
                    "this argument is specified, a single "
                    "zip file will be created instead."))
@click.option('--stage', default=DEFAULT_STAGE_NAME,
              help="lambda function stage, default dev.")
@click.option('--out', default=DEFAULT_PACKAGE_DIST,
              help="lambda package out directory, default dist.")
@click.option('--force-download', is_flag=True, default=False,
              help="If force download dependency lib, default false.")
@click.pass_context
def package(ctx, generate_sam, stage, out, force_download):
    factory = ctx.obj['factory']
    factory.create_deploy_directory(ctx.obj["project_dir"], out)
    factory.generate_requirement_file()
    packager = factory.create_app_packager(
        stage=stage, force_download=force_download)
    packager.package_app(out_dir=out, generate_sam=generate_sam)


def main():
    try:
        return cli(obj={})
    except botocore.exceptions.NoRegionError:
        click.echo("No region configured. "
                   "Either export the AWS_DEFAULT_REGION "
                   "environment variable or set the "
                   "region value in our ~/.aws/config file.", err=True)
        return 2
    except Exception:
        click.echo(traceback.format_exc(), err=True)
        return 2


if __name__ == '__main__':
    main()
