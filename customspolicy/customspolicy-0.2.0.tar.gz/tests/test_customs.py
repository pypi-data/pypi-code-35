import unittest
import customs
from customs import orchestrator
from customs import validator
import json


class TestDates(unittest.TestCase):
    def test_sussessive_entries_exists(self):
        with open('tests/entriesexitsnotrespected.json', 'r') as outfile:
            data = json.load(outfile)
        transformed = orchestrator.transform_data(
            data['Reference Date'], data['Entries'], data['Exits'])
        flag = orchestrator.not_accurate_entries_exists(transformed['df'])
        self.assertEqual(flag, True)

    def test_invalid_date_json(self):
        # parse = customs.data_are_valid('tests/dateinjsoninvalid.json')
        with open('tests/dateinjsoninvalid.json', 'r') as outfile:
            data = json.load(outfile)
        check = validator.is_json_correct(data)
        print(check)
        self.assertEqual(check, "'201-04-06' is not a 'date'")


if __name__ == "__main__":
    unittest.main()
