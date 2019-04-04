# -*- coding: utf-8 -*-

"""Console script for chaostoolkit_openstack."""
import sys
import click
import os
from logzero import logger
from chaosopenstack.utils import print_server_list
from chaosopenstack.compute.actions import (
    start_server,
    stop_server,
    suspend_server,
    resume_server,
    pause_server,
    unpause_server,
)

switcher = {
    1: print_server_list,
    2: stop_server,
    3: start_server,
    4: suspend_server,
    5: resume_server,
    6: pause_server,
    7: unpause_server,
}

secrets = {
    "region": os.getenv("OS_REGION_NAME"),
    "auth_url": os.getenv("OS_AUTH_URL"),
    "project_name": os.getenv("OS_TENANT_NAME"),
    "username": os.getenv("OS_USERNAME"),
    "password": os.getenv("OS_PASSWORD"),
}


@click.command()
@click.option(
    "--cmd",
    default=0,
    help="""
any num of: 
    1: print_server_list, 
    2: stop server, 
    3: start server,
    4: suspend_server,
    5: resume_server,
    6: pause_server,
    7: unpause_server
""",
)
@click.option(
    "--server_name", default=None, help="a server name if needed by the command"
)
def cli(cmd, server_name):
    click.echo("A small cli for Openstack")

    func = switcher.get(cmd, None)
    if not func:
        click.echo("You have to provide a cmd number")
        return 0

    click.echo("CMD: {}".format(func))
    if server_name is None:
        func(secrets=secrets)
    else:
        func(server_name=server_name, secrets=secrets)
    return 0


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
