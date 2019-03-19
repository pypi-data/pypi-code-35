import click
from . import __version__
from .installer import Installer
from .runner import Runner

# click entrypoint
@click.group()
def main():
    """Startin'Blox installer"""
    pass

@main.command()
@click.argument('name', nargs=1)
@click.argument('directory', required=False)
@click.option('--venv', is_flag=True, default=False, help='Create a virtualenv')
@click.option('-m', '--modules', multiple=True, help='List of modules to install')
def startproject(name, venv, directory=None, modules=None):

    """Start a new startin'blox project"""

    # split modules and distributions in dependencies
    deps = []
    for module in modules:
        try:
            pkg, dist = module.split(':')
        except ValueError:
            pkg = module
            dist = module

        deps.append((pkg, dist))

    installer = Installer(
        project_name=name,
        project_folder=directory,
        venv=venv,
        modules=deps
    )
    installer.create_project()

@main.command()
def runserver():

    """Start a local server"""

    runner = Runner()
    runner.start_project()

@main.command()
def version():
    """Print module version"""
    click.echo(__version__)
