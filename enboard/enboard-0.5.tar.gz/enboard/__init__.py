'''Manage Python environments easily.'''

__version__ = '0.5'

from .menu import create_menu_cli

def main(argv=None):
    cli = create_menu_cli()
    res = cli.run()
    if res:
        res.activate()
