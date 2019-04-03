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
        sonic_model = None
        expected_model = None

        with open(os.path.join(self.basedir, "yaml", "pipe4", ".sonic.yml"), "r") as ymlfile:
            sonic_model = yaml.load(ymlfile)

        with open(os.path.join(self.basedir, "yaml", "pipe4", "expected-model.yml"), "r") as ymlfile:
            expected_model = yaml.load(ymlfile)

        mock_util.get_maven_cache_location.return_value = "/path/to/maven/cache"
        mock_config.get_registry.return_value = "01234567890.dkr.ecr.eu-west-1.amazonaws.com"

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
        mock_config.get_networks.return_value = networks

        def get_config_mock(*args, **kwargs):
            property_name = args[0]
            if property_name == mock_config.Keys.map_environment_variables:
                return {
                    "SONIC_TASK": "${sonic_task}",
                    "ZONE": "${zone}",
                    "SITE": "${site}",
                    "SOLUTION": "${solution}",
                    "ENVIRONMENT": "${environment}",
                    "FLAVOUR": "${flavour}",
                    "COMPONENT": "${component}",
                    "SHORTNAME": "${shortname}",
                    "VERSION": "${version}",
                    "DOMAIN": "${domain}",
                    "SSH_AUTH_SOCK": "/tmp/ssh_auth_sock"
                }

        mock_config.get.side_effect = get_config_mock

        logging.info("The created model for shorthand formats should be the one expected")
        compose.task_config = sonic.get_task_config(sonic_model)
        model = compose.create_model("build", sonic_model["tasks"]["build"][0], 1)

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
            model = compose.create_model("test", sonic_model)
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
