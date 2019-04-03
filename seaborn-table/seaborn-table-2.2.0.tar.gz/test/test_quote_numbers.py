import os
import unittest

from seaborn_table.table import SeabornTable, UNICODE, BASESTRING

PATH = os.path.split(os.path.abspath(__file__))[0]


class QuoteNumbersTest(unittest.TestCase):
    def quote_number_test(self, source):
        file_path = os.path.join(PATH, 'data', 'test_file.rst')
        table = SeabornTable.file_to_obj(file_path=file_path)
        table.map(lambda x: UNICODE(x))
        result_path = os.path.join(PATH, 'test_file.%s' % source)
        result = table.obj_to_file(result_path, quote_numbers=False)
        expected_file = os.path.join(PATH, 'data', 'expected',
                                     'test_file.%s'%source)
        with open(expected_file, 'rb') as fp:
            self.assertEqual(fp.read().decode('utf-8').replace('\r', ''),
                             result.replace('\r', ''))
        os.remove(result_path)

    def test_quote_numbers_md(self):
        self.quote_number_test('md')

    def test_quote_numbers_csv(self):
        self.quote_number_test('csv')

    def test_quote_numbers_txt(self):
        self.quote_number_test('txt')

    def test_quote_numbers_html(self):
        self.quote_number_test('html')

    def test_quote_numbers_grid(self):
        self.quote_number_test('grid')

    def test_quote_numbers_json(self):
        self.quote_number_test('json')

    def test_quote_numbers_rst(self):
        self.quote_number_test('rst')

    def test_quote_numbers_psql(self):
        self.quote_number_test('psql')


class EvalCellsFalseTest(unittest.TestCase):
    def eval_cells_test(self, source):
        file_path = os.path.join(PATH, 'data', 'test_file.%s' % source)
        table = SeabornTable.file_to_obj(eval_cells=False, file_path=file_path)
        assert isinstance(table[0]['TU'], BASESTRING)

    def test_eval_cells_false_md(self):
        self.eval_cells_test('md')

    def test_eval_cells_false_csv(self):
        self.eval_cells_test('csv')

    def test_eval_cells_false_txt(self):
        self.eval_cells_test('txt')

    # XXX uncomment after implementing html_to_obj
    # def test_eval_cells_false_html(self):
    #     self.eval_cells_test('html')

    def test_eval_cells_false_grid(self):
        self.eval_cells_test('grid')

    def test_eval_cells_false_json(self):
        self.eval_cells_test('json')

    def test_eval_cells_false_rst(self):
        self.eval_cells_test('rst')

    def test_eval_cells_false_psql(self):
        self.eval_cells_test('psql')


if __name__ == '__main__':
    unittest.main()
