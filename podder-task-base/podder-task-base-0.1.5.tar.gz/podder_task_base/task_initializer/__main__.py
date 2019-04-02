"""
podder task base - task TaskInitializer
"""
import click

from podder_task_base.task_initializer.builder import Builder
from podder_task_base import __version__


# CLI codes.
# Add '-h' option
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.group(context_settings=CONTEXT_SETTINGS)
@click.version_option(version=__version__, prog_name="task_initializer")
def task_initializer():
    pass


# [python -m podder_task_base.task_initializer init] command
@click.command()
@click.argument('task-name')
@click.option('--target-dir', '-t',
    default='/usr/local/poc_base',
    help="install directory")
def init(task_name: str, target_dir: str):
    Builder(task_name, target_dir).init_task()


task_initializer.add_command(init)


def main():
    task_initializer()


if __name__ == '__main__':
    main()
