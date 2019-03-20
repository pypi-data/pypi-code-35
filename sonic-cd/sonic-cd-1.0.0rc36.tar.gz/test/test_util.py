# -*- coding: utf-8 -*-
import unittest
import yaml
from mock import patch
from soniclib import util
import os
import logging
from test import TestCaseBase


class TestUtil(TestCaseBase):
    this_file = os.path.realpath(__file__)
    basedir = os.path.dirname(this_file)

    @patch('soniclib.util.get_file')
    @patch.dict('soniclib.util.os.environ', {
        'M2_HOME': os.path.join(basedir, '/M2_HOME')
    })
    def test_get_maven_settings_file(self, get_file_mock):
        user_specific_settings_xml_file = os.path.join(self.basedir, '.m2', 'settings.xml')
        system_wide_settings_xml_file = os.path.join(self.basedir, 'M2_HOME', 'conf', 'settings.xml')

        logging.info("No user specific settings should fallback to system-wide settings")
        get_file_mock.side_effect = [None, open(system_wide_settings_xml_file)]
        # shoot
        settings_file = util.get_maven_settings_file()
        # assert
        self.assertIsNotNone(settings_file)
        self.assertEqual(system_wide_settings_xml_file, settings_file.name)

        logging.info("User specific settings should be preferred to system-wide settings")
        get_file_mock.side_effect = [open(user_specific_settings_xml_file), open(system_wide_settings_xml_file)]
        # shoot
        settings_file = util.get_maven_settings_file()
        # assert
        self.assertIsNotNone(settings_file)
        self.assertEqual(user_specific_settings_xml_file, settings_file.name)

    @patch.dict('soniclib.util.os.environ', {
        'environment': 'custom123'
    })
    @patch('soniclib.util.get_maven_cache_location')
    def test_format_model(self, get_maven_cache_location_mock):
        logging.info("Named volumes should be created automatically and placeholders should be replaced")
        get_maven_cache_location_mock.return_value = '/some/maven/cache/location'
        # shoot
        model = {
            "application-logs": {
                "volumes": [
                    "log-volume:/var/opt/vgt/logs/",
                    "${maven_cache}:/var/cache/maven",
                    "${workdir}:/workdir"
                ],
                "environment": [
                    'zone=${zone}',
                    'site=${site}',
                    'solution=${solution}',
                    'environment=${environment}',
                    'flavour=${flavour}'
                ]
            }
        }
        services, volumes = util.format_model(model)
        logging.debug("Got services: %s" % yaml.dump(services))
        logging.debug("Got volumes: %s" % yaml.dump(volumes))
        # assert
        self.assertIsNotNone(services)
        self.assertIsNotNone(volumes)
        self.assertDictEqual(volumes, {'log-volume': {}})
        self.assertListEqual(services["application-logs"]["volumes"], [
            'log-volume:/var/opt/vgt/logs/',
            '${maven_cache}:/var/cache/maven',
            '${workdir}:/workdir'
        ])
        self.assertListEqual(services["application-logs"]["environment"], [
            'zone=${zone}',
            'site=${site}',
            'solution=${solution}',
            'environment=${environment}',
            'flavour=${flavour}'
        ])

    def test_in_unittest(self):
        logging.info("Unit test detection should work")
        self.assertTrue(util.in_unittest())


if __name__ == "__main__":
    unittest.main()
