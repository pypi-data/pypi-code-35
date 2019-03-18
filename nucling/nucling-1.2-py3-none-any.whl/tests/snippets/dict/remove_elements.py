import unittest
from nucling.snippet.dict import remove_element


class Test_remove_element( unittest.TestCase ):
    def test_should_remove_none_in_simple_dict( self ):
        d = { 'a': None, 'b': 1 }
        remove_element( d, None )
        self.assertNotIn( 'a', d )

    def test_should_remove_in_recursive( self ):
        d = { 'a': None, 'b': 1, 'c': {'a': None, 'b': 1} }
        remove_element( d, None )
        self.assertNotIn( 'a', d[ 'c' ] )

    def test_should_remove_in_recursive_in_list( self ):
        d = { 'a': None, 'b': 1, 'c': [ {'a': None, 'b': 1} ] }
        remove_element( d, None )
        self.assertNotIn( 'a', d[ 'c' ][0] )

    def test_should_remove_empty_dicts( self ):
        d = { 'a': None, 'b': 1, 'c': {} }
        remove_element( d, None )
        self.assertNotIn( 'c', d )

    def test_should_remove_empty_list( self ):
        d = { 'a': None, 'b': 1, 'c': [] }
        remove_element( d, None )
        self.assertNotIn( 'c', d )

    def test_should_remove_the_keys_of_empty_dicts( self ):
        d = { 'a': None, 'b': 1, 'c': { 'a': None } }
        remove_element( d, None )
        self.assertNotIn( 'c', d )
