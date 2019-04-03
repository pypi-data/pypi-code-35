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
__version__ = "0.2.0"

import json
import logging
import os


META_PATH_DIR = "__AIRFLOW_META__"
BRANCH_OPERATOR_FILENAME = "branch_operator.txt"
SHORT_CIRCUIT_OPERATOR_FILENAME = "short_circuit.txt"
SENSOR_OPERATOR_FILENAME = "sensor.txt"
CONTEXT_FILENAME = "context.json"
XCOM_PUSH_FILENAME = "xcom_push.json"


logger = logging.getLogger("airflow_docker_helper")


def _get_branch_operator_file_path(directory):
    return os.path.join(directory, BRANCH_OPERATOR_FILENAME)


def _get_short_circuit_operator_file_path(directory):
    return os.path.join(directory, SHORT_CIRCUIT_OPERATOR_FILENAME)


def _get_sensor_file_path(directory):
    return os.path.join(directory, SENSOR_OPERATOR_FILENAME)


def _get_context_file_path(directory):
    return os.path.join(directory, CONTEXT_FILENAME)


def _get_xcom_push_file_path(directory):
    return os.path.join(directory, XCOM_PUSH_FILENAME)


def _get_container_meta_path():
    tmp_dir = os.environ.get("AIRFLOW_TMP_DIR", ".")
    return os.path.join(tmp_dir, META_PATH_DIR)


def get_host_meta_path(host_dir):
    return os.path.join(host_dir, META_PATH_DIR)


class client:
    @staticmethod
    def branch_to_tasks(task_ids):
        if not isinstance(task_ids, (list, tuple)):
            task_ids = [
                task_ids
            ]  # Handle the possibility that there is only one task id

        meta_path = _get_container_meta_path()
        branch_file_path = _get_branch_operator_file_path(meta_path)

        with open(branch_file_path, "wb") as f:
            f.write(json.dumps(task_ids).encode("utf-8"))
        logger.info("Branching to tasks: {}".format(task_ids))

    @staticmethod
    def short_circuit():
        meta_path = _get_container_meta_path()
        short_circuit_file_path = _get_short_circuit_operator_file_path(meta_path)

        with open(short_circuit_file_path, "wb") as f:
            f.write(json.dumps(False).encode("utf-8"))

        logger.info("Short Circuiting")

    @staticmethod
    def sensor(outcome):
        meta_path = _get_container_meta_path()
        sensor_file_path = _get_sensor_file_path(meta_path)

        with open(sensor_file_path, "wb") as f:
            result = json.dumps(outcome)
            f.write(result.encode("utf-8"))

        logger.info("sensor outcome: {}".format(outcome))

    @classmethod
    def context(cls):
        meta_path = _get_container_meta_path()
        context_file_path = _get_context_file_path(meta_path)

        with open(context_file_path, "rb") as f:
            logger.debug("Loading context")
            return json.loads(f.read().decode("utf-8"))

    @classmethod
    def xcom_push(cls, key, value):
        meta_path = _get_container_meta_path()
        file_path = _get_xcom_push_file_path(meta_path)

        data = json.dumps({"key": key, "value": value}) + "\n"
        with open(file_path, "ab") as f:
            f.write(data.encode("utf-8"))

        logger.debug("xcom_push data: {}".format(data))


class host:
    @staticmethod
    def branch_task_ids(tmp_dir):
        meta_path = get_host_meta_path(tmp_dir)
        branch_file_path = _get_branch_operator_file_path(meta_path)

        if not os.path.exists(branch_file_path):
            logger.info("Branch Task IDs output not found. Assuming [].")
            return []

        with open(branch_file_path, "rb") as f:
            task_ids = f.read().decode("utf-8")
            logger.info("Branching to: {}".format(task_ids))
            return json.loads(task_ids)

    @staticmethod
    def short_circuit_outcome(tmp_dir):
        meta_path = get_host_meta_path(tmp_dir)
        short_circuit_file_path = _get_short_circuit_operator_file_path(meta_path)

        if not os.path.exists(short_circuit_file_path):
            logger.info("Short Circuit output not found. Assuming True.")
            return True

        with open(short_circuit_file_path, "rb") as f:
            result = f.read().decode("utf-8").strip()
            logger.info("Short Circuit outcome: {}".format(result))
            return bool(json.loads(result))

    @staticmethod
    def sensor_outcome(tmp_dir):
        meta_path = get_host_meta_path(tmp_dir)
        sensor_file_path = _get_sensor_file_path(meta_path)

        if not os.path.exists(sensor_file_path):
            logger.info("Sensor output not found. Assuming False.")
            return False

        with open(sensor_file_path, "rb") as f:
            result = f.read().decode("utf-8").strip()
            logger.info("Sensor outcome: {}".format(result))
            return bool(json.loads(result))

    @staticmethod
    def write_context(context, host_tmp_dir):
        meta_path = get_host_meta_path(host_tmp_dir)
        context_file_path = _get_context_file_path(meta_path)

        with open(context_file_path, "wb") as f:
            logger.info("Writing context to: {}".format(context_file_path))
            f.write(json.dumps(serialize_context(context)).encode("utf-8"))

    @staticmethod
    def get_xcom_push_data(host_tmp_dir):
        meta_path = get_host_meta_path(host_tmp_dir)
        file_path = _get_xcom_push_file_path(meta_path)

        if not os.path.exists(file_path):
            return []

        with open(file_path, "rb") as f:
            data = f.read().decode("utf-8")

        logger.info("Getting xcom_push data: {}".format(data))
        return [json.loads(row) for row in data.strip().split("\n")]

    @staticmethod
    def make_meta_dir(host_tmp_dir):
        meta_path = get_host_meta_path(host_tmp_dir)
        try:
            os.makedirs(meta_path)
        except OSError as e:
            if os.path.exists(meta_path):
                pass
            else:
                raise e


def serialize_context(context):
    return {
        "dag": serialize_dag(context["dag"]),
        "ds": context["ds"],
        "next_ds": context["next_ds"],
        "next_ds_nodash": context["next_ds_nodash"],
        "prev_ds": context["prev_ds"],
        "prev_ds_nodash": context["prev_ds_nodash"],
        "ds_nodash": context["ds_nodash"],
        "ts": context["ts"],
        "ts_nodash": context["ts_nodash"],
        "ts_nodash_with_tz": context["ts_nodash_with_tz"],
        "yesterday_ds": context["yesterday_ds"],
        "yesterday_ds_nodash": context["yesterday_ds_nodash"],
        "tomorrow_ds": context["tomorrow_ds"],
        "tomorrow_ds_nodash": context["tomorrow_ds_nodash"],
        "END_DATE": context["END_DATE"],
        "end_date": context["end_date"],
        "dag_run": serialize_dag_run(context["dag_run"]),
        "run_id": context["run_id"],
        "execution_date": context["execution_date"].isoformat(),
        "prev_execution_date": context["prev_execution_date"].isoformat(),
        "next_execution_date": context["next_execution_date"].isoformat(),
        "latest_date": context["latest_date"],
        "params": context["params"],
        "task": serialize_task(context["task"]),
        "task_instance": serialize_task_instance(context["task_instance"]),
        "ti": serialize_task_instance(context["ti"]),
        "task_instance_key_str": context["task_instance_key_str"],
        "test_mode": context["test_mode"],
    }


def serialize_dag(dag):
    return {}


def serialize_dag_run(dag_run):
    return {}


def serialize_task(task):
    return {}


def serialize_task_instance(task_instance):
    return {}
