#!/usr/bin/env python
"""get/set `demo.details` `resources`"""
# -*- coding: utf-8 -*-
import click
import jsfiddle
import os

MODULE_NAME = "jsfiddle.details.resources"
PROG_NAME = 'python -m %s' % MODULE_NAME
USAGE = 'python -m %s path [url ...]' % MODULE_NAME


@click.command()
@click.argument('path', required=True)
@click.argument('urls', nargs=-1, required=False)
def _cli(path, urls):
    if os.path.exists(path) and os.path.isfile(path):
        path = os.path.dirname(path)
    os.chdir(path)
    details = jsfiddle.details.load()
    if not urls:
        if details.get("resources", []):
            print("\n".join(details["resources"]))
    else:
        if len(urls) == 1 and urls[0] == "":
            urls = []
        details["resources"] = list(sorted(set(urls)))
        jsfiddle.details.save(details)


if __name__ == '__main__':
    _cli(prog_name=PROG_NAME)
