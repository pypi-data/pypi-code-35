# -*- coding: utf-8 -*-

"""Console script for checking_smtp_starttls."""
import sys
import click


@click.command()
def main(args=None):
    """Console script for checking_smtp_starttls."""
    click.echo("Replace this message by putting your code into "
               "checking_smtp_starttls.cli.main")
    click.echo("See click documentation at http://click.pocoo.org/")
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
