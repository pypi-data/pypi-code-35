# -*- coding: utf-8 -*-

"""Console script for endorphin."""
import sys
import click


@click.group()
def main(args=None):
    """Console script for endorphin."""
    click.echo("Replace this message by putting your code into "
               "endorphin.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0

@main.command()
def new(project):
    pass

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
