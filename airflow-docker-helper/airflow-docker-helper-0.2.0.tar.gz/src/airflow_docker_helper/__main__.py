# -*- coding: utf-8 -*-
#
#     Copyright 2019 Hunter Senft-Grupp
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import logging
import os
import sys

from airflow_docker_helper import client

logger = logging.getLogger("airflow_docker_helper")


def setup_logging():
    logging.basicConfig(level=logging.INFO)


def get_parser():
    parser = argparse.ArgumentParser(prog="airflow-docker-helper")
    parser.add_argument("--dry-run", action="store_true")
    sub_parsers = parser.add_subparsers()

    short_circuit = sub_parsers.add_parser("short-circuit")
    short_circuit.set_defaults(func=do_short_circuit)

    branch_to_task = sub_parsers.add_parser("branch-to-tasks")
    branch_to_task.set_defaults(func=do_branch_to_tasks)
    branch_to_task.add_argument("task_ids", nargs="*")

    sensor = sub_parsers.add_parser("sensor")
    sensor.set_defaults(func=do_sensor)
    sensor_flags = sensor.add_mutually_exclusive_group()
    sensor_flags.add_argument("--true", dest="outcome", action="store_true")
    sensor_flags.add_argument("--false", dest="outcome", action="store_false")

    return parser


def do_short_circuit(options):
    if not options.dry_run:
        client.short_circuit()
    logger.info("Short Circuiting")


def do_branch_to_tasks(options):
    if not options.dry_run:
        client.branch_to_tasks(options.task_ids)
    logger.info("Branch To Tasks: {}".format(options.task_ids))


def do_sensor(options):
    if not options.dry_run:
        client.sensor(options.outcome)
    logger.info("Sensor Outcome: {}".format(options.outcome))


def main():
    setup_logging()
    parser = get_parser()
    options = parser.parse_args()
    options.func(options)
    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
