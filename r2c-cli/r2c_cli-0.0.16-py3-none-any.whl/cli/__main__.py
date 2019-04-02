#!/usr/bin/env python3
import logging
import os
import sys

import click

from r2c.cli import R2C_SUPPORT_EMAIL
from r2c.cli.commands.build import build
from r2c.cli.commands.cli import cli
from r2c.cli.commands.init import init
from r2c.cli.commands.login import login, logout
from r2c.cli.commands.push import push
from r2c.cli.commands.run import run
from r2c.cli.commands.test import test, unittest
from r2c.cli.errors import CliError
from r2c.cli.logger import print_exception_exit

if __name__ == "__main__":
    try:
        cli(obj={}, prog_name="r2c")
    except CliError as ce:
        print_exception_exit("There was an unexpected client error", ce)
    except Exception as e:
        print_exception_exit("There was an exception", e)
