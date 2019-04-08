#!/usr/bin/env python
"""get/set `demo.details` `description`"""
# -*- coding: utf-8 -*-
import click
import jsfiddle
import os

MODULE_NAME = "jsfiddle.details.description"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s path [value]' % MODULE_NAME


@click.command()
@click.argument('path', required=True)
@click.argument('value', required=False)
def _cli(path, value=None):
    if os.path.exists(path) and os.path.isfile(path):
        path = os.path.dirname(path)
    os.chdir(path)
    details = jsfiddle.details.load()
    if not value:
        description = details.get("description", None)
        if description:
            print(description)
    else:
        details["description"] = value
        jsfiddle.details.save(details)


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
