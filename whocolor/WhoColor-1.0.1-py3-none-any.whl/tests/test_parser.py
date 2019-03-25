import unittest
import pickle
import os

from WhoColor.parser import WikiMarkupParser


class TestParser(unittest.TestCase):
    def test_parser(self):
        test_data_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'test_data.p')
        with open(test_data_file_path, 'rb') as f:
            test_data = pickle.load(f)

        for article, data in test_data.items():
            p = WikiMarkupParser(data['rev_text'], data['tokens'])
            p.generate_extended_wiki_markup()

            # Some of the entries in tuple are out of order. Not sure why and hence sorting both based on author id
            p.present_editors = tuple(sorted(list(p.present_editors), key=lambda x: x[0]))
            data['present_editors'] = tuple(sorted(list(data['present_editors']), key=lambda x: x[0]))

            assert p.extended_wiki_text == data['extended_wiki_text'], article
            assert p.present_editors == data['present_editors'], article
