import unittest
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pelops.myconfigtools import read_config, validate_config
from skeiron.relayservice import Relayservice


class TestValidateConfig(unittest.TestCase):
    def test_validate_config(self):
        filename = "config.yaml"
        if not os.getcwd().endswith("tests_unit"):
            filename = "tests_unit/"+filename
        config = read_config(filename)
        validation_result = validate_config(config, Relayservice.get_schema())
        self.assertIsNone(validation_result)


if __name__ == '__main__':
    unittest.main()
