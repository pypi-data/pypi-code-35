import unittest
from nucling.snippet.regex import is_camelcase


class Test_camel_case( unittest.TestCase ):
    def test_is_camelcase_should_be_true( self ):
        self.assertEqual( is_camelcase( 'CamelCase' ), True )
        self.assertEqual( is_camelcase( 'camelCase' ), True )
        self.assertNotEqual( is_camelcase( 'camelcase' ), True )
