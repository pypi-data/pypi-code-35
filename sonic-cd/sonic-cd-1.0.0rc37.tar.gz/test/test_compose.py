# -*- coding: utf-8 -*-
import unittest
from mock import patch
from soniclib import compose, sonic
import yaml
import os
import logging

from test import TestCaseBase


class TestCompose(TestCaseBase):

    @patch.dict('soniclib.compose.os.environ', {
        'http_proxy': 'http://user:passwd@the_evil_proxy:8080',
        'https_proxy': 'http://user:passwd@the_evil_proxy:8080',
        'no_proxy': 'I_WISH'
    })
    @patch('soniclib.compose.config')
    @patch('soniclib.compose.util')
    def test_create_model_with_shorthand_format(self, mock_util, mock_config):
        with open(os.path.join(self.basedir, "yaml", "pipe4", ".sonic.yml"), "r") as ymlfile:
            sonic_model = yaml.load(ymlfile)
            services = {
                "builder1": {
                    "image": "356026449505.dkr.ecr.eu-west-1.amazonaws.com/delivery-engine-docker-maven-set-version",
                    "command": "${semantic_version}",
                    "environment": {
                        "COMPONENT": '${component}',
                        "DOMAIN": '${domain}',
                        "ENVIRONMENT": '${environment}',
                        "FLAVOUR": '${flavour}',
                        "SHORTNAME": '${shortname}',
                        "SITE": '${site}',
                        "SOLUTION": '${solution}',
                        "SSH_AUTH_SOCK": "/tmp/ssh_auth_sock",
                        "VERSION": '${version}',
                        "ZONE": '${zone}',
                        'http_proxy': 'http://user:passwd@the_evil_proxy:8080',
                        'https_proxy': 'http://user:passwd@the_evil_proxy:8080',
                        'no_proxy': 'I_WISH'
                    },
                    "mem_limit": "2048m",
                    "shm_size": "512m",
                    "volumes": [
                        '${workdir}:/workdir',
                        '/var/run/docker.sock:/var/run/docker.sock',
                        '${user_home}/.docker/config.json:/root/.docker/config.json:ro',
                        '${user_home}/.aws:/root/.aws:ro',
                        '${user_home}/.aws/cli:/root/.aws/cli',
                        '${user_home}/.ssh:/root/.ssh:ro',
                        '${user_home}/.gitconfig:/root/.gitconfig:ro',
                        '${maven_cache}:/var/cache/maven'
                    ]
                }
            }
            volumes = [
                "log-volume"
            ]
            networks = {
                "default": {
                    "driver": "bridge",
                    "driver_opts": {
                        "com.docker.network.driver.mtu": 1400
                    },
                    "ipam": {
                        "driver": "default",
                        "config": [
                            {
                                "subnet": "192.168.70.1/24",
                                "gateway": "192.168.70.1"
                            }
                        ],
                    }
                }
            }
            mock_util.format_model.return_value = services, volumes
            mock_util.get_maven_cache_location.return_value = "/path/to/maven/cache"
            mock_config.get_networks.return_value = networks
            mock_config.get_registry.return_value = "356026449505.dkr.ecr.eu-west-1.amazonaws.com"
            logging.info("The created model for shorthand formats should be the one expected")
            compose.task_config = sonic.get_task_config(sonic_model)
            model = compose.create_model("build", 1, sonic_model["tasks"]["build"][0])
            expected_model = {
                "services": services,
                "version": "2.1",
                "networks": networks,
                "volumes": volumes
            }
            logging.debug("Expecting model:\n%s" % yaml.dump(expected_model))
            logging.debug("Got model:\n%s" % yaml.dump(model))
            self.assertDictEqual(expected_model, model)

    @patch('soniclib.compose.config')
    @patch('soniclib.compose.util')
    def test_create_model_with_full_format(self, mock_util, mock_conig):
        with open(os.path.join(self.basedir, "yaml", "pipe4", ".sonic.yml"), "r") as ymlfile:
            sonic_model = yaml.load(ymlfile)
            services = {
                "application-logs": {
                    "volumes": [
                        'log-volume:/var/opt/vgt/logs/',
                        '/some/maven/cache/location:/var/cache/maven',
                        '..:/workdir'
                    ]
                }
            }
            volumes = [
                "log-volume"
            ]
            networks = {
                "default": {
                    "driver": "bridge",
                    "driver_opts": {
                        "com.docker.network.driver.mtu": 1400
                    },
                    "ipam": {
                        "driver": "default",
                        "config": [
                            {
                                "subnet": "192.168.70.1/24",
                                "gateway": "192.168.70.1"
                            }
                        ],
                    }
                }
            }
            mock_util.format_model.return_value = services, volumes
            mock_conig.get_networks.return_value = networks
            logging.info("The created model should contain services, version, volumes and networks")
            compose.task_config = sonic.get_task_config(sonic_model)
            model = compose.create_model("test", 1, sonic_model)
            expected_model = {
                "services": services,
                "version": "2.1",
                "volumes": volumes,
                "networks": networks
            }
            logging.debug("Expecting model:\n%s" % yaml.dump(expected_model))
            logging.debug("Got model:\n%s" % yaml.dump(model))
            self.assertDictEqual(expected_model, model)


if __name__ == "__main__":
    unittest.main()
