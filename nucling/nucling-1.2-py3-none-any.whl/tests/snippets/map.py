import unittest
import copy
from nucling.snippet.map import map_list_of_dicts, map_list_of_obj


class dump_class:
    def __init__(self, **kw ):
        for k, v in kw.items():
            setattr( self, k, v )


list_of_dicts = [
    { 'a': 'aa', 'b': 'ba', 'c': 'ca' }, { 'a': 'ab', 'b': 'bb', 'c': 'cb' },
    { 'a': 'ac', 'b': 'bc', 'c': 'cc' },
]


list_of_dicts_2 = [
    { 'a': 'aa', 'b': 'ba', 'c': 'ca' }, { 'a': 'aa', 'b': 'bb', 'c': 'cb' },
    { 'a': 'ac', 'b': 'bc', 'c': 'cc' },
]


list_of_obj = [ dump_class( **d ) for d in copy.deepcopy( list_of_dicts ) ]


list_of_obj_2 = [ dump_class( **d ) for d in copy.deepcopy( list_of_dicts_2 ) ]


class Test_map( unittest.TestCase ):
    def test_map_of_list_should_return_a_dict( self ):
        result = map_list_of_dicts( list_of_dicts, 'a' )
        self.assertIsInstance( result, dict )

    def test_map_of_list_should_a_dict_with_the_3_expected_keys( self ):
        result = map_list_of_dicts( list_of_dicts, 'a' )
        self.assertSetEqual(
            set( result.keys() ), set( ( 'aa', 'ab', 'ac' ) ) )

    def test_map_of_list_should_a_dict_with_the_correct_values( self ):
        result = map_list_of_dicts( list_of_dicts, 'a' )
        self.assertEqual
        (
            {
                'aa': [ list_of_dicts[0] ], 'ab': [ list_of_dicts[1] ],
                'ac': [ list_of_dicts[2] ]
            }, result )

    def test_map_of_list_with_multiple_key_should_be_expected_dict( self ):
        result = map_list_of_dicts( list_of_dicts, 'a', 'b' )
        self.assertEqual(
            {
                'aa': { 'ba': [ list_of_dicts[0] ] },
                'ab': { 'bb': [ list_of_dicts[1] ] },
                'ac': { 'bc': [ list_of_dicts[2] ] }
            }, result )

    def test_with_multiple_key_should_be_the_expected_dict_2( self ):
        result = map_list_of_dicts( list_of_dicts_2, 'a', 'b' )
        self.assertEqual(
            {
                'aa': {
                    'ba': [ list_of_dicts_2[0] ],
                    'bb': [ list_of_dicts_2[1] ] },
                'ac': { 'bc': [ list_of_dicts_2[2] ] }
            }, result )

    def test_map_of_list_should_a_dict_with_the_correct_values_2( self ):
        result = map_list_of_dicts( list_of_dicts_2, 'a' )
        self.assertEqual(
            {
                'aa': [ list_of_dicts_2[0], list_of_dicts_2[1] ],
                'ac': [ list_of_dicts_2[2] ]
            }, result )

    def test_map_of_list_obj_should_return_a_dict( self ):
        result = map_list_of_obj( list_of_obj, 'a' )
        self.assertIsInstance( result, dict )

    def test_map_of_list_obj_should_a_dict_with_the_3_expected_keys( self ):
        result = map_list_of_obj( list_of_obj, 'a' )
        self.assertSetEqual(
            set( result.keys() ), set( ( 'aa', 'ab', 'ac' ) ) )

    def test_map_of_list_obj_should_a_dict_with_the_correct_values( self ):
        result = map_list_of_obj( list_of_obj, 'a' )
        self.assertEqual(
            {
                'aa': [ list_of_obj[0] ], 'ab': [ list_of_obj[1] ],
                'ac': [ list_of_obj[2] ]
            }, result )

    def test_map_of_list_obj_with_multiple_key_should_be_expected_dict( self ):
        result = map_list_of_obj( list_of_obj, 'a', 'b' )
        self.assertEqual(
            {
                'aa': { 'ba': [ list_of_obj[0] ] },
                'ab': { 'bb': [ list_of_obj[1] ] },
                'ac': { 'bc': [ list_of_obj[2] ] }
            }, result )

    def test_map_of_list_obj_with_multiple_key_should_be_dict_2( self ):
        result = map_list_of_obj( list_of_obj_2, 'a', 'b' )
        self.assertEqual(
            {
                'aa': {
                    'ba': [ list_of_obj_2[0] ],
                    'bb': [ list_of_obj_2[1] ] },
                'ac': { 'bc': [ list_of_obj_2[2] ] }
            }, result )

    def test_map_of_list_obj_should_a_dict_with_the_correct_values_2( self ):
        result = map_list_of_obj( list_of_obj_2, 'a' )
        self.assertEqual(
            {
                'aa': [ list_of_obj_2[0], list_of_obj_2[1] ],
                'ac': [ list_of_obj_2[2] ]
            }, result )
