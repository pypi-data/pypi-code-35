import unittest

from bigquery_schema_coerce import core

schema = """[{
    "mode": "REPEATED",
    "name": "value",
    "type": "TIMESTAMP"
}]"""


class TestTypesTimestamp(unittest.TestCase):
    def setUp(self):
        self.schema = core.parse_schema(text=schema)

    def test_convert(self):
        candidate = {"value": ["Mar 3, 2019 2:12:12PM", "2019-01-01T3:33:33"]}
        result = core.convert(candidate, self.schema)
        expected = {"value": ["2019-03-03T14:12:12", "2019-01-01T03:33:33"]}
        self.assertDictEqual(expected, result)
