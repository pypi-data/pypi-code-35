import sys
import json
from tablat import Table
import unittest
from pathlib import Path
from io import StringIO


class TestTable(unittest.TestCase):

    _input_folder = Path(__file__).parent / 'input'
    _data_dict = {}
    _expected_data = []
    _target = None

    def test_table_init(self):
        """
        Test internal vars in `Table` initialization
        """
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_table_init']

        table = Table(data_obj['data'], data_obj['headers'])
        self.assertEqual(table._num_columns, expected_data['num_columns'])
        self.assertEqual(table._column_max, expected_data['columns_max'])

    def test_headers_update(self):
        """
        Test internal vars when headers are updated
        """
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_headers_update']

        table = Table(data_obj['data'], data_obj['headers'])
        table.headers = table.headers[:-2]
        self.assertEqual(table._num_columns, expected_data['num_columns'])
        self.assertEqual(table._column_max, expected_data['columns_max'])

    def test_data_update(self):
        """
        Test internal vars when table data is changed
        """
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_data_update']

        table = Table(data_obj['data'], data_obj['headers'])
        table.table_data = list.reverse(table.table_data)
        self.assertEqual(table._num_columns, expected_data['num_columns'])
        self.assertEqual(table._column_max, expected_data['columns_max'])

    def test_data_addition(self):
        """
        Test internal vars when table data is added
        """
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_data_addition']

        table = Table(data_obj['data'], data_obj['headers'])
        table.add_data(['This is a testcase', 'Short', 'but it does his job', ';)'])
        self.assertEqual(table._num_columns, expected_data['num_columns'])
        self.assertEqual(table._column_max, expected_data['columns_max'])

    def test_getitem(self):
        """
        Test `getitem` magic method
        """
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_getitem']

        table = Table(data_obj['data'], data_obj['headers'])
        self.assertEqual(table[0], expected_data['first_row'])
        self.assertEqual(table[2][1], expected_data['third_row_second_col'])

    def test_no_data_print(self):
        """
        Test warning rise when printing table with no data
        """
        table = Table()
        with self.assertWarns(UserWarning):
            table.print_table()

    def test_table_content_init(self):
        """
        Test printed table content
        """
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_table_content_init']

        # Create table
        table =Table(data_obj['data'], data_obj['headers'])
        table.style.update(True, False, False)

        # Get printed table as str
        table_str = str(table)
        table_lines = table_str.split('\n')
        table_lines = table_lines[3:]
        for exp_line, exp_content in expected_data.items():
            try:
                index = int(exp_line)

            except ValueError:
                self.fail(f"Error in expected test data. Expected a `int` as key, found: {exp_line}")

            for exp_data in exp_content:
                self.assertTrue(str(exp_data) in table_lines[index])

    def test_table_content_add(self):
        """
        Test printed table content when data is added after initialization
        """
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_table_content_add']

        # Create table
        table =Table(data_obj['data'], data_obj['headers'])
        table.add_data(expected_data['14'])
        table.style.update(True, False, False)

        # Get printed table as str
        table_str = str(table)
        table_lines = table_str.split('\n')
        table_lines = table_lines[3:]
        for exp_line, exp_content in expected_data.items():
            try:
                index = int(exp_line)

            except ValueError:
                self.fail(f"Error in expected test data. Expected a `int` as key, found: {exp_line}")

            for exp_data in exp_content:
                self.assertTrue(str(exp_data) in table_lines[index])

    def test_table_content_filter(self):
        """
        Test printed table content when hide and show filters are used
        """
        data_obj = self.get_data()
        expected_data = self.get_test_expected()['test_table_content_filter']

        table =Table(data_obj['data'], data_obj['headers'])
        table.style.update(True, False, False)

        # Backup stdout
        stdout_backup = sys.stdout

        # Generate table (printed to stdout) with show filter
        show_ind = [0, 2]
        sys.stdout = StringIO()
        table.print_table(show_columns=show_ind)
        table_str_show = sys.stdout.getvalue()
        sys.stdout.close()

        # Generate table (printed to stdout) with hide filter
        hide_ind = [1, 2]
        sys.stdout = StringIO()
        table.print_table(hide_columns=hide_ind)
        table_str_hide = sys.stdout.getvalue()
        sys.stdout.close()

        # Restore stdout
        sys.stdout = stdout_backup

        # Test show table
        table_lines = table_str_show.split('\n')
        table_lines = table_lines[3:]
        for exp_line, exp_content in expected_data.items():
            try:
                index = int(exp_line)

            except ValueError:
                self.fail(f"Error in expected test data. Expected a `int` as key, found: {exp_line}")

            for i, exp_data in enumerate(exp_content):
                if i in show_ind:
                    self.assertTrue(str(exp_data) in table_lines[index])

                else:
                    self.assertFalse(str(exp_data) in table_lines[index])

        # Test hide table
        table_lines = table_str_hide.split('\n')
        table_lines = table_lines[3:]
        for exp_line, exp_content in expected_data.items():
            try:
                index = int(exp_line)

            except ValueError:
                self.fail(f"Error in expected test data. Expected a `int` as key, found: {exp_line}")

            for i, exp_data in enumerate(exp_content):
                if i in hide_ind:
                    self.assertFalse(str(exp_data) in table_lines[index])

                else:
                    self.assertTrue(str(exp_data) in table_lines[index])

    def preview(self):
        data_obj = self.get_data()
        table = Table(data_obj['data'], data_obj['headers'])
        print()
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
