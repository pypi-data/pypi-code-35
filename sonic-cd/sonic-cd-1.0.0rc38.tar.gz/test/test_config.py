# -*- coding: utf-8 -*-
import logging
from mock import patch
from soniclib import config
from test import TestCaseBase


class TestConfig(TestCaseBase):

    @patch('soniclib.config.util')
    def test_load(self, mock_util):
        logging.info("Global config should be returned if no user-level config exists")
        global_config = {'a': 1, 'b': 10}
        user_config = None
        mock_util.load_yaml.side_effect = [global_config, user_config]
        # shoot
        config.clear()
        conf = config.load()
        # assert
        merged_config = {'a': 1, 'b': 10}
        self.assertDictEqual(merged_config, conf)

        logging.info("User-level config should override global config")
        global_config = {'a': 1, 'b': 10}
        user_config = {'a': 2}
        mock_util.load_yaml.side_effect = [global_config, user_config]
        # shoot
        config.clear()
        conf = config.load()
        # assert
        merged_config = {'a': 2, 'b': 10}
        self.assertDictEqual(merged_config, conf)

    @patch('soniclib.config.util')
    @patch('soniclib.config.load')
    def test_get_registry(self, load_mock, mock_util):
        # 1st shot
        configured_registry = '123456789012.dkr.ecr.eu-west-1.amazonaws.com'
        load_mock.return_value = {'registry': configured_registry}
        logging.info("config.get_registry should return the registry from the config, when available")
        registry = config.get_registry()
        self.assertIsNotNone(registry)
        self.assertEqual(registry, configured_registry)
        # 2nd shot
        load_mock.reset_mock()
        load_mock.return_value = {}
        registry_authenticated_against = '210987654321.dkr.ecr.eu-west-1.amazonaws.com'
        mock_util.load_json.return_value = {
            'auths': {
                registry_authenticated_against: {
                    'auth': 'yaddayaddayadda'
                }
            }
        }
        logging.info("config.get_registry should return the registry from the docker config file, when available")
        registry = config.get_registry()
        self.assertIsNotNone(registry)
        self.assertEqual(registry_authenticated_against, registry)
        # 3rd shot
        load_mock.reset_mock()
        mock_util.reset_mock()
        load_mock.return_value = {}
        mock_util.load_json.return_value = None
        with self.assertRaises(Exception) as context:
            config.get_registry()
            self.assertTrue('No registry found in' in context.exception.message)
