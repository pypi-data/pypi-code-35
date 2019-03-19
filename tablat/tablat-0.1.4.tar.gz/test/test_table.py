import json
from tablat import Table
import unittest
from pathlib import Path


class TestTable(unittest.TestCase):

    _input_folder = Path(__file__).parent / 'input'
    _data_dict = {}
    _expected_data = []
    _target = None

    def test_table_init(self):
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_table_init']

        table = Table(data_obj['data'], data_obj['headers'])
        self.assertEqual(table._num_columns, expected_data['num_columns'])
        self.assertEqual(table._column_max, expected_data['columns_max'])

    def test_headers_update(self):
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_headers_update']

        table = Table(data_obj['data'], data_obj['headers'])
        table.headers = table.headers[:-2]
        self.assertEqual(table._num_columns, expected_data['num_columns'])
        self.assertEqual(table._column_max, expected_data['columns_max'])

    def test_data_update(self):
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_data_update']

        table = Table(data_obj['data'], data_obj['headers'])
        table.table_data = list.reverse(table.table_data)
        self.assertEqual(table._num_columns, expected_data['num_columns'])
        self.assertEqual(table._column_max, expected_data['columns_max'])

    def test_data_addition(self):
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_data_addition']

        table = Table(data_obj['data'], data_obj['headers'])
        table.add_data(['This is a testcase', 'Short', 'but it does his job', ';)'])
        self.assertEqual(table._num_columns, expected_data['num_columns'])
        self.assertEqual(table._column_max, expected_data['columns_max'])

    def test_getitem(self):
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_getitem']

        table = Table(data_obj['data'], data_obj['headers'])
        self.assertEqual(table[0], expected_data['first_row'])
        self.assertEqual(table[2][1], expected_data['third_row_second_col'])

    def test_no_data_print(self):
        table = Table()
        with self.assertWarns(UserWarning):
            table.print_table()

    def preview(self, table):
        """
        Prints test table data
        """
        table.print_table()
        print("\n** Stats **\n > num_columns: {}\n > columns_size: {}".format(table._num_columns,
                                                                              table._column_max))

    def get_data(self):
        """
        Returns a `dict` with the test data
        """
        if not self._data_dict:
            self._data_dict = self._load_data()

        return self._data_dict

    def get_test_expected(self):
        """
        Returns a `list` with the expected outputs for test
        """
        if not self._expected_data:
            self._expected_data = self._load_test_expected()

        return self._expected_data

    def _load_data(self):

        # Load data
        input_data_path = self._input_folder / 'table_data.json'
        with open(input_data_path.resolve(), 'r') as f:
            data_obj = json.load(f)

        # Reduce data size
        line_lenght = len(data_obj['headers'])
        step = 60
        num_lines = 14
        small_data = []
        for i in range(num_lines):
            small_data.extend(data_obj['data'][i * step:i * step + line_lenght])

        data_obj['data'] = small_data
        return data_obj

    def _load_test_expected(self):
        expected_file_path = self._input_folder / 'test_tab_expected.json'
        with open(expected_file_path.resolve(), 'r') as f:
            expected_data = json.load(f)

        return expected_data


if __name__ == '__main__':
    TestTable().preview()
