import unittest
from nucling.snippet.dict import (
    keys_to_snake_case, _inner_keys_to_snake_case
)


camel_dict = {
    'CamelCase': 'a',
    'IAmACamelCase': 'a',
    'AKAS': 'a',
    'Explotion!!!!': 'a',
}


snake_dict = {
    'camel_case': 'a',
    'i_am_a_camel_case': 'a',
    'akas': 'a',
    'explotion!!!!': 'a',
}


class Test_keys_to_snake_case( unittest.TestCase ):
    def test_should_work( self ):
        result = keys_to_snake_case( camel_dict )
        self.assertSetEqual( set( result.keys() ), set( snake_dict.keys() ) )

    def test_should_work_with_complex( self ):
        camel_dict[ 'AA' ] = camel_dict.copy()
        snake_dict[ 'aa' ] = snake_dict.copy()

        camel_dict[ 'AB' ] = camel_dict.copy()
        snake_dict[ 'ab' ] = snake_dict.copy()
        keys_to_snake_case( camel_dict )

    def test_should_work_with_complex_with_list( self ):
        camel_dict[ 'AA' ] = camel_dict.copy()
        snake_dict[ 'aa' ] = snake_dict.copy()

        camel_dict[ 'AB' ] = [ camel_dict.copy() for i in range( 5 ) ]
        snake_dict[ 'ab' ] = [ snake_dict.copy() for i in range( 5 ) ]
        result = keys_to_snake_case( camel_dict )
        self.assertDictEqual( result, snake_dict )

    def test_inner_keys_should_work( self ):
        result = _inner_keys_to_snake_case( camel_dict )
        self.assertSetEqual( set( result.keys() ), set( snake_dict.keys() ) )

    def test_inner_keys_should_ignore_string( self ):
        result = _inner_keys_to_snake_case( 'explotion!!!' )
        self.assertEqual( result, 'explotion!!!' )

    def test_inner_keys_should_ignore_int( self ):
        result = _inner_keys_to_snake_case( 1 )
        self.assertEqual( result, 1 )

    def test_inner_keys_should_ignore_float( self ):
        result = _inner_keys_to_snake_case( 1.1 )
        self.assertEqual( result, 1.1 )
