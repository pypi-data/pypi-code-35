import unittest
from pynosql.common.model_helper import ModelHelper


class TestSetup(unittest.TestCase):
    """ Model Test """

    def test_basic_model_structure(self):
        """ Test valid model load of basic structure """
        values = {
            'test1': 'value1',
            'test2': 'value2',
            'test3': 'value3'
        }
        expected = {
            'test1': 'value1',
            'test2': 'value2',
            'test3': 'value3',
            'test4': None
        }
        mh = ModelHelper({
            'test1': None,
            'test2': None,
            'test3': None,
            'test4': None
        })
        mh.load(values)
        self.assertDictEqual(mh.model, expected)

    def test_basic_model_with_sub_structure(self):
        """ Test valid model load of base sub structure """
        values = {
            'test1': 'value1',
            'test2': {
                'sub1': 'subvalue1',
                'sub2': 'subvalue2'
            },
            'test3': 'value3'
        }
        expected = {
            'test1': 'value1',
            'test2': {
                'sub1': 'subvalue1',
                'sub2': 'subvalue2',
                'sub3': None
            },
            'test3': 'value3',
            'test4': None
        }
        mh = ModelHelper({
            'test1': None,
            'test2': {
                'sub1': None,
                'sub2': None,
                'sub3': None
            },
            'test3': None,
            'test4': None
        })
        mh.load(values)
        self.assertDictEqual(mh.model, expected)

    def test_basic_model_with_multiple_nested_structure(self):
        """ Test valid model load of multiple nested structure """
        values = {
            'test1': 'value1',
            'test2': {
                'sub1': 'subvalue1',
                'sub2': 'subvalue2',
                'sub3': {
                    'nested1': 'nestedvalue1'
                }
            },
            'test3': 'value3'
        }
        expected = {
            'test1': 'value1',
            'test2': {
                'sub1': 'subvalue1',
                'sub2': 'subvalue2',
                'sub3': {
                    'nested1': 'nestedvalue1',
                    'nested2': None,
                }
            },
            'test3': 'value3',
            'test4': None
        }
        mh = ModelHelper({
            'test1': None,
            'test2': {
                'sub1': None,
                'sub2': None,
                'sub3': {
                    'nested1': None,
                    'nested2': None,
                }
            },
            'test3': None,
            'test4': None
        })
        mh.load(values)
        self.assertDictEqual(mh.model, expected)

    def test_basic_model_with_non_present_keys(self):
        """ Test valid model with keys not present in model """
        values = {
            'test1': 'value1',
            'test2': 'value2',
            'test5': 'value5'
        }
        expected = {
            'test1': 'value1',
            'test2': 'value2',
            'test3': None,
            'test4': None
        }
        mh = ModelHelper({
            'test1': None,
            'test2': None,
            'test3': None,
            'test4': None
        })
        mh.load(values)
        self.assertDictEqual(mh.model, expected)

    def test_basic_model_with_sub_structure_and_non_present_keys(self):
        """ Test valid model load of base sub structure and non present keys"""
        values = {
            'test1': 'value1',
            'test2': {
                'sub1': 'subvalue1',
                'sub4': 'subvalue4'
            },
            'test3': 'value3',
            'test6': {
                'sub7': 'subvalue7',
                'sub8': 'subvalue8'
            }
        }
        expected = {
            'test1': 'value1',
            'test2': {
                'sub1': 'subvalue1',
                'sub2': None,
                'sub3': None
            },
            'test3': 'value3',
            'test4': None,
            'test5': {
                'sub5': None,
                'sub6': None
            }
        }
        mh = ModelHelper({
            'test1': None,
            'test2': {
                'sub1': None,
                'sub2': None,
                'sub3': None
            },
            'test3': None,
            'test4': None,
            'test5': {
                'sub5': None,
                'sub6': None
            }
        })
        mh.load(values)
        self.assertDictEqual(mh.model, expected)

    def test_basic_model_structure_with_list_values(self):
        """ Test valid model load of basic structure with list values"""
        values = [
            {
                'test1': 'value1',
                'test2': 'value2',
                'test3': 'value3'
            },
            {
                'test1': 'value4',
                'test2': 'value5',
                'test3': 'value6'
            },
            {
                'test1': 'value7',
                'test2': 'value8',
                'test3': 'value9'
            }
        ]
        expected = [
            {
                'test1': 'value1',
                'test2': 'value2',
                'test3': 'value3',
                'test4': None
            },
            {
                'test1': 'value4',
                'test2': 'value5',
                'test3': 'value6',
                'test4': None
            },
            {
                'test1': 'value7',
                'test2': 'value8',
                'test3': 'value9',
                'test4': None
            }
        ]
        mh = ModelHelper({
            'test1': None,
            'test2': None,
            'test3': None,
            'test4': None
        })
        mh.load(values, True)
        self.assertListEqual(mh.model, expected)
