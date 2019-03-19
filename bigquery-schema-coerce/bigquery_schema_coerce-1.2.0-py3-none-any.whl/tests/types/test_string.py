import unittest

from bigquery_schema_coerce import core

schema = """[{
    "mode": "REPEATED",
    "name": "value",
    "type": "STRING"
}]"""


class TestTypesString(unittest.TestCase):
    def setUp(self):
        self.schema = core.parse_schema(text=schema)

    def test_convert(self):
        candidate = {"value": ["120", "12", 12]}
        result = core.convert(candidate, self.schema)
        expected = {"value": ["120", "12", "12"]}
        self.assertDictEqual(expected, result)
