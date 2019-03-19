import unittest

from bigquery_schema_coerce import core

schema = """[{
    "mode": "REPEATED",
    "name": "value",
    "type": "FLOAT"
}]"""


class TestTypesFloat(unittest.TestCase):
    def setUp(self):
        self.schema = core.parse_schema(text=schema)

    def test_convert(self):
        candidate = {"value": ["123,120.1234", "12", 12]}
        result = core.convert(candidate, self.schema)
        expected = {"value": [123120.1234, 12, 12]}
        self.assertDictEqual(expected, result)
