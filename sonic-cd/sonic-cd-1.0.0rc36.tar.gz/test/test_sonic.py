# -*- coding: utf-8 -*-
import unittest
from mock import patch, call, Mock
from soniclib import sonic, compose
import yaml
import os
import logging

from soniclib.context import Context
from test import TestCaseBase


class TestSonic(TestCaseBase):

    @patch('soniclib.sonic.config')
    @patch('soniclib.sonic.init_context')
    @patch('soniclib.sonic.login_if_needed')
    @patch('soniclib.sonic.metrics')
    @patch('soniclib.sonic.setup')
    @patch('soniclib.sonic.clean')
    @patch('soniclib.sonic.run_pipe')
    @patch('soniclib.sonic.run_task')
    def test_run(self, run_task_mock, run_pipe_mock, clean_mock, setup_mock, metrics_mock, login_if_needed_mock,
                 init_context_mock, config_mock):
        parser_results = Mock()
        parser_results.file = os.path.join(self.basedir, "yaml", "pipe1", ".sonic.yml")
        with open(parser_results.file) as control_file:
            parser_results.sequence = ["build", "test"]
            parser_results.pull = False
            parser_results.context = []
            parser_results.version = False
            parser_results.config = False
            # 1st shot
            logging.info("sonic.run with 'run' as parser_results.sequences should call both build and test")
            sonic.run(parser_results)
            sonic_model = yaml.load(control_file)
            expected_calls = [
                call("build", sonic_model),
                call("test", sonic_model)
            ]
            run_pipe_mock.assert_has_calls(expected_calls)
            # 2nd shot
            logging.info("sonic.run with 'build' as parser_results.sequences should only call build")
            parser_results.sequence = ["build"]
            run_pipe_mock.reset_mock()
            sonic.run(parser_results)
            run_pipe_mock.assert_called_once_with("build", sonic_model)
            # 3rd shot
            logging.info("sonic.run with 'test' as parser_results.sequences should only call test")
            parser_results.sequence = ["test"]
            run_pipe_mock.reset_mock()
            sonic.run(parser_results)
            run_pipe_mock.assert_called_once_with("test", sonic_model)
            # 4th shot
            logging.info("sonic.run with 'clean' as parser_results.sequences should only call clean")
            parser_results.sequence = ["clean"]
            run_pipe_mock.reset_mock()
            sonic.run(parser_results)
            clean_mock.assert_called_once()
            assert not run_pipe_mock.called, 'sonic.run_task was called even though it should not have been called'
            # 5th shot
            logging.info("sonic.run with 'setup' as parser_results.sequences should only call setup")
            parser_results.sequence = ["setup"]
            run_pipe_mock.reset_mock()
            sonic.run(parser_results)
            setup_mock.assert_called_once()
            assert not run_pipe_mock.called, 'sonic.run_task was called even though it should not have been called'

    @patch('soniclib.context.Context.load')
    @patch('soniclib.sonic.config', autospec=True)
    @patch('soniclib.sonic.compose.config', autospec=True)
    @patch('soniclib.compose.run', autospec=True)
    def test_build_with_single_task(self, run_mock, compose_config_mock, sonic_config_mock, load_mock):
        sonic_model = {"tasks": {"build": "maven clean package"}}
        compose_config_mock.get_available_gateway.return_value = "192.168.69.1"
        compose.task_config = sonic.get_task_config(sonic_model)
        model = compose.create_model("build", sonic_model["tasks"]["build"])
        logging.info("sonic.build with single task should call run with expected arguments")
        sonic.run_task("build", sonic_model)
        run_mock.assert_called_once_with("build", model)

    @patch('soniclib.context.Context.load')
    @patch('soniclib.sonic.config', autospec=True)
    @patch('soniclib.sonic.compose.config', autospec=True)
    @patch('soniclib.compose.run', autospec=True)
    def test_build_with_list_of_tasks(self, run_mock, compose_config_mock, sonic_config_mock, load_mock):
        sonic_model = {
            "tasks": {
                "build": [
                    "maven clean compile",
                    "maven package"
                ]
            }
        }
        compose_config_mock.get_available_gateway.return_value = "192.168.69.1"
        logging.info("sonic.build with list of tasks should call run with expected arguments")
        compose.task_config = sonic.get_task_config(sonic_model)
        sonic.run_task("build", sonic_model)
        expected_calls = [
            call("build", compose.create_model("build", sonic_model["tasks"]["build"][0], 0), 0),
            call("build", compose.create_model("build", sonic_model["tasks"]["build"][1], 1), 1)
        ]
        run_mock.assert_has_calls(expected_calls)

    @patch('soniclib.context.Context.load')
    @patch('soniclib.sonic.config', autospec=True)
    @patch('soniclib.sonic.compose', autospec=True)
    def test_build_with_full_format(self, compose_mock, config_mock, load_mock):
        sonic_model = {
            "tasks": {
                "build": {
                    "main": {
                        "image": "012345678901.dkr.ecr.eu-west-1.amazonaws.com/delivery-engine-centos7-dockerbase",
                        "user": "root",
                        "command": "docker build --pull -t 012345678901.dkr.ecr.eu-west-1.amazonaws.com/${component}:${semantic_version} --build-arg VERSION=${semantic_version} /workdir",
                        "volumes": [
                            "${workdir}:/workdir",
                            "${user_home}/.docker/config.json:/root/.docker/config.json",
                            "/var/run/docker.sock:/var/run/docker.sock"
                        ]
                    }
                }
            }
        }
        task_config = sonic.get_task_config(sonic_model)
        logging.info("sonic.build with dict of tasks should call compose.create_model with expected arguments")
        sonic.run_task("build", sonic_model)
        compose_mock.create_model.assert_called_once_with("build", sonic_model["tasks"]["build"])

    @patch('soniclib.context.Context.load')
    @patch('soniclib.sonic.config', autospec=True)
    @patch('soniclib.sonic.compose.config', autospec=True)
    @patch('soniclib.compose.run', autospec=True)
    def test_test_with_single_task(self, run_mock, compose_config_mock, sonic_config_mock, load_mock):
        sonic_model = {"tasks": {"test": "maven -Pcomponent-test test"}}
        compose.task_config = sonic.get_task_config(sonic_model)
        model = compose.create_model("test", sonic_model["tasks"]["test"])
        model["networks"]["default"]["ipam"]["config"][0] = {
            "subnet": "192.168.69.1/24",
            "gateway": "192.168.69.1"
        }
        compose_config_mock.get_available_gateway.return_value = "192.168.69.1"
        logging.info("sonic.test with single task should call run with expected arguments")
        sonic.run_task("test", sonic_model)
        run_mock.assert_called_once_with("test", model)

    @patch('soniclib.context.Context.load')
    @patch('soniclib.sonic.config', autospec=True)
    @patch('soniclib.sonic.compose.config', autospec=True)
    @patch('soniclib.compose.run', autospec=True)
    def test_test_with_list_of_tasks(self, run_mock, compose_config_mock, config_mock, load_mock):
        sonic_model = {
            "tasks": {
                "test": [
                    "maven -Pcomponent-test test",
                    "maven -Pcomponent-test integration-test"
                ]
            }
        }
        compose_config_mock.get_available_gateway.return_value = "192.168.69.1"
        logging.info("sonic.test with list of tasks should call run with expected arguments")
        compose.task_config = sonic.get_task_config(sonic_model)
        sonic.run_task("test", sonic_model)
        expected_calls = [
            call("test", compose.create_model("test", sonic_model["tasks"]["test"][0], 0), 0),
            call("test", compose.create_model("test", sonic_model["tasks"]["test"][1], 1), 1)
        ]
        run_mock.assert_has_calls(expected_calls)

    @patch('soniclib.context.Context.load')
    @patch('soniclib.sonic.config', autospec=True)
    @patch('soniclib.sonic.compose.config', autospec=True)
    @patch('soniclib.compose.run', autospec=True)
    def test_test_with_list_of_tasks_default_image(self, run_mock, compose_config_mock, sonic_config_mock, load_mock):
        sonic_model = {
            "tasks": {
                "test": [
                    "$ test",
                    "$ -Pcomponent-test integration-test"
                ]
            }
        }
        compose_config_mock.get_available_gateway.return_value = "192.168.69.1"
        logging.info("sonic.test with list of tasks should call run with expected arguments")
        compose.task_config = sonic.get_task_config(sonic_model)
        sonic.run_task("test", sonic_model)
        expected_calls = [
            call("test", compose.create_model("test", sonic_model["tasks"]["test"][0], 0), 0),
            call("test", compose.create_model("test", sonic_model["tasks"]["test"][1], 1), 1)
        ]
        run_mock.assert_has_calls(expected_calls)

    @patch('soniclib.context.Context.load')
    @patch('soniclib.sonic.config', autospec=True)
    @patch('soniclib.sonic.compose.config', autospec=True)
    @patch('soniclib.sonic.util.config', autospec=True)
    @patch('soniclib.sonic.util.os', autospec=True)
    @patch('soniclib.sonic.util.get_docker_group_id', autospec=True)
    @patch('soniclib.sonic.util.get_component', autospec=True)
    @patch('soniclib.sonic.compose.util.system_uses_vagrant', autospec=True)
    @patch('soniclib.sonic.compose.util.get_local_maven_repository', autospec=True)
    @patch('soniclib.sonic.compose.run', autospec=True)
    def test_test_full_format(self, compose_run_mock, get_local_maven_repository_mock, system_uses_vagrant_mock,
                              get_component_mock, get_docker_group_id_mock, mock_os, util_mock_config,
                              compose_mock_config, config_mock, load_mock):
        with open(os.path.join(self.basedir, "yaml", "pipe4", ".sonic.yml"), "r") as ymlfile:
            de_yaml = yaml.load(ymlfile)
            get_local_maven_repository_mock.return_value = '/maven/cache'
            system_uses_vagrant_mock.return_value = False
            get_component_mock.return_value = 'deploy-engine-jar-test-delivery'
            get_docker_group_id_mock.return_value = 600
            util_mock_config.get_registry.return_value = '012345678901.dkr.ecr.eu-west-1.amazonaws.com'
            compose_mock_config.get_networks.return_value = {
                "default": {
                    "driver": "bridge",
                    "driver_opts": {
                        "com.docker.network.driver.mtu": "1400"
                    },
                    "ipam": {
                        "driver": "default",
                        "config": [{
                            "subnet": "192.168.70.1/24",
                            "gateway": "192.168.70.1"
                        }],
                    }
                }
            }
            logging.info("sonic.test with dict should call compose.run with expected model")
            sonic.run_task("test", de_yaml)
            expected_model = {
                'services': {
                    'wiremock': {
                        'image': '012345678901.dkr.ecr.eu-west-1.amazonaws.com/wiremock'
                    },
                    'activemq': {
                        'image': '012345678901.dkr.ecr.eu-west-1.amazonaws.com/activemq'
                    },
                    'suthost': {
                        'environment': [
                            'DEPLOY_COMMAND=full-deploy',
                            'ENVIRONMENT_ID=pool',
                            'LD_PRELOAD='
                        ],
                        'image': '${component}:${semantic_version}',
                        'links': [
                            'wiremock',
                            'mongodb',
                            'memcached',
                            'activemq',
                            'waiter'
                        ],
                        'mem_limit': '2048m',
                        'volumes': [
                            'log-volume:/var/opt/vgt/logs/'
                        ]
                    },
                    'waiter': {
                        'image': '012345678901.dkr.ecr.eu-west-1.amazonaws.com/service-waiter',
                        'links': [
                            'wiremock',
                            'mongodb',
                            'memcached',
                            'activemq'],
                        'volumes': [
                            '${workdir}:/workdir'
                        ]
                    },
                    'mongodb': {
                        'image': '012345678901.dkr.ecr.eu-west-1.amazonaws.com/mongodb'
                    },
                    'application-logs': {
                        'environment': [
                            'LOG_PATH=/var/opt/vgt/logs/*/*-json.log'
                        ],
                        'image': '012345678901.dkr.ecr.eu-west-1.amazonaws.com/logging-agent',
                        'volumes': [
                            'log-volume:/var/opt/vgt/logs/'
                        ]
                    },
                    'main': {
                        'image': '012345678901.dkr.ecr.eu-west-1.amazonaws.com/deploy-engine-component-test',
                        'links': [
                            'suthost',
                            'wiremock',
                            'mongodb',
                            'memcached',
                            'activemq'],
                        'volumes': [
                            '${workdir}:/workdir',
                            '${maven_cache}:/var/cache/maven'
                        ]
                    },
                    'memcached': {
                        'image': '012345678901.dkr.ecr.eu-west-1.amazonaws.com/memcached'
                    }
                },
                'volumes': {
                    'log-volume': {}
                },
                'networks': {
                    "default": {
                        "driver": "bridge",
                        "driver_opts": {
                            "com.docker.network.driver.mtu": "1400"
                        },
                        'ipam': {
                            'config': [
                                {
                                    'subnet': '192.168.70.1/24',
                                    'gateway': '192.168.70.1'
                                }
                            ],
                            'driver': 'default'
                        }
                    }
                },
                'version': '2.1'
            }
            compose_run_mock.assert_called_with("test", expected_model)

    @patch.dict('soniclib.sonic.os.environ', {
        'SUDO_USER': 'goran',
        'SUDO_UID': '1001',
        'SUDO_GID': '1001'
    })
    @patch('soniclib.sonic.json')
    @patch('soniclib.sonic.util')
    def test_setup(self, mock_util, mock_json):
        # stub
        mock_util.get_user_id.return_value = 0
        mock_util.run.return_value = 0, ""
        mock_util.get_docker_daemon_json_location.return_value = '/etc/docker/daemon.json'
        prior_daemon_json_contents = {
            "bip": "192.168.69.1/24",
            "dns": [
                "10.57.77.210",
                "8.8.8.8"
            ]
        }
        mock_util.load_json.return_value = prior_daemon_json_contents
        mock_util.get_docker_group_id.return_value = 500
        # shoot
        logging.info("sonic.setup should store expected content")
        sonic.setup(dryrun=False)
        # verify
        new_daemon_json_contents = {}
        new_daemon_json_contents.update(prior_daemon_json_contents)
        new_daemon_json_contents.update({
            "userns-remap": 'goran',
            'mtu': 1400
        })
        mock_util.store_as_json.assert_called_with(new_daemon_json_contents, '/etc/docker/daemon.json')
        expected_calls = [
            call("goran:\d+:\d+", "goran:1001:65536", "/etc/subuid", False),
            call("goran:\d+:\d+", "goran:500:65536", "/etc/subgid", False)
        ]
        mock_util.replace_add.assert_has_calls(expected_calls)
        mock_util.run.assert_called_with("service docker restart")

    @patch('soniclib.context.Context.load')
    @patch('soniclib.sonic.run_pre_tasks')
    @patch('soniclib.sonic.get_task_config')
    @patch('soniclib.sonic.do_task', autospec=True)
    def test_run_task_with_exception(self, do_task_mock, get_task_config_mock, run_pre_tasks_mock, load_mock):
        do_task_mock.side_effect = Exception('Boom!')
        with self.assertRaises(Exception) as boom:
            sonic.run_task("test", {"tasks": {"test": {}}})

        assert str(boom.exception) == "Boom!"
        context = Context()
        assert context.get("status") == 1

    @patch('soniclib.sonic.config.get')
    def test_find_encompassing_task(self, config_get_mock):
        config_tasks = None
        config_get_mock.side_effect = lambda value: config_tasks if value == "tasks" else None

        config_tasks = {}
        task = sonic.find_encompassing_task("post", "release", {"tasks": {}})
        assert task == []

        config_tasks = {"post-release": ["postreleaseimage"]}
        task = sonic.find_encompassing_task("post", "release", {"tasks": {}})
        assert task == config_tasks["post-release"]

        config_tasks = {"post-task": ["posttaskimage"]}
        task = sonic.find_encompassing_task("post", "release", {"tasks": {}})
        assert task == config_tasks["post-task"]

        task = sonic.find_encompassing_task("post", "release", {"tasks": {"post-release": ["image in list"]}})
        assert task == ["image in list"] + config_tasks["post-task"]

        task = sonic.find_encompassing_task("post", "release", {"tasks": {"post-release": "image not in list"}})
        assert task == ["image not in list"] + config_tasks["post-task"]


if __name__ == "__main__":
    unittest.main()
