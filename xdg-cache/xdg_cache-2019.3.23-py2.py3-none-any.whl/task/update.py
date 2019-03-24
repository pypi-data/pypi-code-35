#!/usr/bin/env python
"""create/update all tasks"""
import task.setup
from task import classes


def _cli():
    classes.update()


if __name__ == "__main__":
    _cli()
