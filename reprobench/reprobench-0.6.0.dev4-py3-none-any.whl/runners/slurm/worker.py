import atexit
import os
import signal
import time

import click
import strictyaml
import zmq
from loguru import logger
from playhouse.apsw_ext import APSWDatabase

from reprobench.core.schema import schema
from reprobench.runners.local.worker import RUN_REGISTER
from reprobench.utils import import_class


def clean_up():
    signal.signal(signal.SIGTERM, signal.SIG_IGN)
    os.killpg(os.getpgid(0), signal.SIGTERM)
    time.sleep(3)
    os.killpg(os.getpgid(0), signal.SIGKILL)


@click.command()
@click.option("-c", "--config", required=True, type=click.File())
@click.option(
    "-d",
    "--database",
    required=True,
    type=click.Path(dir_okay=False, resolve_path=True),
)
@click.argument("server_address")
@click.argument("run_id", type=int)
def run(config, database, server_address, run_id):
    atexit.register(clean_up)

    config = config.read()
    config = strictyaml.load(config, schema=schema).data

    context = zmq.Context()
    socket = context.socket(zmq.DEALER)
    socket.connect(server_address)
    send_event(socket, RUN_REGISTER, run_id)
    run = decode_message(socket.recv())

    tool = import_class(run.tool.module)
    context = config.copy()
    context["tool"] = tool
    context["run"] = run
    logger.info(f"Processing task: {run['directory']}")

    for runstep in config["steps"]["run"]:
        logger.debug(f"Running step {runstep['step']}")
        step = import_class(runstep["step"])
        step.execute(context, runstep.get("config", {}))


if __name__ == "__main__":
    run()
