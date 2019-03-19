import unittest

from bigquery_schema_coerce import core

schema = """[{
    "mode": "REPEATED",
    "name": "value",
    "type": "BOOLEAN"
}]"""


class TestTypesBool(unittest.TestCase):
    def setUp(self):
        self.schema = core.parse_schema(text=schema)

    def test_convert_true(self):
        candidate = {"value": ["T", "Y", 1, "1", "yes", "Yes", "True", "true"]}
        result = core.convert(candidate, self.schema)
        for result_value in result["value"]:
            self.assertTrue(result_value)

    def test_convert_false(self):
        candidate = {"value": ["F", "N", 0, "0", "no", "No", "False", "false"]}
        result = core.convert(candidate, self.schema)
        for result_value in result["value"]:
            self.assertFalse(result_value)
