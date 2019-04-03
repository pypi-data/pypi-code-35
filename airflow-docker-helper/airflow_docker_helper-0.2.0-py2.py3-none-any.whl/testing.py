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
import json

from . import client, host
from .compat import BUILTIN_NAME, mock


def test_client(mock_context=None):
    if mock_context is None:
        mock_context = {}

    class _client:
        _mock_context = mock_context

        _mock_context_file = mock.Mock()
        _mock_short_circuit_file = mock.Mock()
        _mock_branch_to_tasks_file = mock.Mock()
        _mock_sensor_file = mock.Mock()
        _mock_xcom_push_file = mock.Mock()

        @classmethod
        def short_circuit(cls, *args, **kwargs):
            with mock.patch(
                "{}.open".format(BUILTIN_NAME),
                mock.mock_open(cls._mock_short_circuit_file),
            ):
                return client.short_circuit(*args, **kwargs)

        @classmethod
        def branch_to_tasks(cls, *args, **kwargs):
            with mock.patch(
                "{}.open".format(BUILTIN_NAME),
                mock.mock_open(cls._mock_branch_to_tasks_file),
            ):
                return client.branch_to_tasks(*args, **kwargs)

        @classmethod
        def sensor(cls, *args, **kwargs):
            with mock.patch(
                "{}.open".format(BUILTIN_NAME), mock.mock_open(cls._mock_sensor_file)
            ):
                return client.sensor(*args, **kwargs)

        @classmethod
        def context(cls, *args, **kwargs):
            with mock.patch(
                "{}.open".format(BUILTIN_NAME),
                mock.mock_open(
                    cls._mock_context_file,
                    read_data=json.dumps(cls._mock_context).encode("utf-8"),
                ),
            ):
                return client.context(*args, **kwargs)

        @classmethod
        def xcom_push(cls, *args, **kwargs):
            with mock.patch(
                "{}.open".format(BUILTIN_NAME), mock.mock_open(cls._mock_xcom_push_file)
            ):
                return client.xcom_push(*args, **kwargs)

        @classmethod
        def assert_sensor_called_with(cls, value):
            assert (
                len(cls._mock_sensor_file().write.mock_calls) >= 1
            ), "Sensor never called"
            assert (
                json.loads(
                    cls._mock_sensor_file().write.mock_calls[0][1][0].decode("utf-8")
                )
                == value
            ), "Sensor not called with expected value"

        @classmethod
        def assert_short_circuited(cls):
            assert (
                len(cls._mock_short_circuit_file().write.mock_calls) >= 1
            ), "Never short circuited"
            assert (
                json.loads(
                    cls._mock_short_circuit_file()
                    .write.mock_calls[0][1][0]
                    .decode("utf-8")
                )
                is False
            ), "Did not short circuit as expected"

        @classmethod
        def assert_not_short_circuited(cls):
            assert (
                len(cls._mock_short_circuit_file().write.mock_calls) == 0
            ), "Short circuited"

        @classmethod
        def assert_branched_to_tasks(cls, tasks, written=True):
            if not written:
                assert (
                    len(cls._mock_branch_to_tasks_file().write.mock_calls) == 0
                ), "Tasks to branch to were written"
                assert not tasks, "Unexpected tasks to branch to when not written"
            else:
                assert (
                    len(cls._mock_branch_to_tasks_file().write.mock_calls) >= 1
                ), "Never branched to tasks"
                assert set(
                    json.loads(
                        cls._mock_branch_to_tasks_file()
                        .write.mock_calls[0][1][0]
                        .decode("utf-8")
                    )
                ) == set(tasks), "A different set of tasks were branched to"

        @classmethod
        def assert_context_accessed(cls):
            assert (
                len(cls._mock_context_file().read.mock_calls) > 0
            ), "Context never accessed"

    return _client


def test_host(task_ids=None, sensor=None, short_circuit=None, xcom_push=None):
    class _host:
        _task_ids = task_ids
        _sensor = sensor
        _short_circuit = short_circuit
        _xcom_push = xcom_push

        _mock_context_file = mock.Mock()
        _mock_sensor_file = mock.Mock()
        _mock_short_circuit_file = mock.Mock()
        _mock_branch_file = mock.Mock()
        _mock_xcom_push = mock.Mock()

        @classmethod
        def branch_task_ids(cls, *args, **kwargs):
            if cls._task_ids is not None:
                with mock.patch(
                    "{}.open".format(BUILTIN_NAME),
                    mock.mock_open(
                        cls._mock_branch_file,
                        read_data=json.dumps(cls._task_ids).encode("utf-8"),
                    ),
                ):
                    with mock.patch("os.path.exists") as exists:
                        exists.return_value = True
                        return host.branch_task_ids(*args, **kwargs)
            else:
                with mock.patch("os.path.exists") as exists:
                    exists.return_value = False
                    return host.branch_task_ids(*args, **kwargs)

        @classmethod
        def short_circuit_outcome(cls, *args, **kwargs):
            if cls._short_circuit is None:
                with mock.patch("os.path.exists") as exists:
                    exists.return_value = False
                    return host.short_circuit_outcome(*args, **kwargs)
            else:
                with mock.patch(
                    "{}.open".format(BUILTIN_NAME),
                    mock.mock_open(
                        cls._mock_short_circuit_file,
                        read_data=json.dumps(cls._short_circuit).encode("utf-8"),
                    ),
                ):
                    with mock.patch("os.path.exists") as exists:
                        exists.return_value = True
                        return host.short_circuit_outcome(*args, **kwargs)

        @classmethod
        def sensor_outcome(cls, *args, **kwargs):
            if cls._sensor is None:
                with mock.patch("os.path.exists") as exists:
                    exists.return_value = False
                    return host.sensor_outcome(*args, **kwargs)
            else:
                with mock.patch(
                    "{}.open".format(BUILTIN_NAME),
                    mock.mock_open(
                        cls._mock_sensor_file,
                        read_data=json.dumps(cls._sensor).encode("utf-8"),
                    ),
                ):
                    with mock.patch("os.path.exists") as exists:
                        exists.return_value = True
                        return host.sensor_outcome(*args, **kwargs)

        @classmethod
        def write_context(cls, *args, **kwargs):
            with mock.patch(
                "{}.open".format(BUILTIN_NAME), mock.mock_open(cls._mock_context_file)
            ):
                return host.write_context(*args, **kwargs)

        @classmethod
        def get_xcom_push_data(cls, *args, **kwargs):
            if cls._xcom_push is None:
                with mock.patch("os.path.exists") as exists:
                    exists.return_value = False
                    return host.get_xcom_push_data(*args, **kwargs)
            else:
                with mock.patch(
                    "{}.open".format(BUILTIN_NAME),
                    mock.mock_open(cls._mock_sensor_file, read_data=cls._xcom_push),
                ):
                    with mock.patch("os.path.exists") as exists:
                        exists.return_value = True
                        return host.get_xcom_push_data(*args, **kwargs)

        @staticmethod
        def make_meta_dir(*args, **kwargs):
            return host.make_meta_dir(*args, **kwargs)

    return _host
