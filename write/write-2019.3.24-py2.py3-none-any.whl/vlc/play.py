#!/usr/bin/env python
"""open/continue play video"""
import click
import vlc

MODULE_NAME = "vlc.play"
USAGE = "python -m %s [path] [start]" % MODULE_NAME
PROG_NAME = 'python -m %s' % MODULE_NAME


@click.command()
@click.argument('path', required=False)
@click.argument('start', required=False)
def _cli(path=None, start=None):
    vlc.play(path, start)


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
