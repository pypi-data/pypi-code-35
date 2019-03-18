import unittest
from nucling.snippet import string

fixture_camel_case = [
    ( 'camelCase', 'camel_case', ),
    ( 'CamelCase', 'camel_case' ),
    ( 'camel_case', 'camel_case' ),
    ( 'IAmACamelCase', 'i_am_a_camel_case' ),
    ( 'AKAS', 'akas' ),
    ( 'Explotion!!!!', 'explotion!!!!' ),
]


class Test_string( unittest.TestCase ):
    def test_camel_to_snake_should_be_expected( self ):
        for value, expected in fixture_camel_case:
            self.assertEqual( string.camel_to_snake( value ), expected )
