import unittest
from nucling.snippet import parser

fixture_zipcodes_and_clean = [
    ( '12345', '12345'), ( '12345-67890', '1234567890' ), ( 'asdf', '' ),
    ( 'asdf-12345', '12345' ), ( None, None ),
]

fixture_parse_bool = [
    ( 'false', False ), ( 'true', True ), ( '0', False ), ( '1', True ),
    ( object(), True ), ( 0, False ), ( 1, True ),
]


class Test_clean_zipcode( unittest.TestCase ):
    def test_should_clean_was_expected( self ):
        for value, expected in fixture_zipcodes_and_clean:
            result = parser.clean_zipcode( value )
            self.assertEqual( result, expected )


class Test_to_bool( unittest.TestCase ):
    def test_should_parsse_was_expected( self ):
        for value, expected in fixture_parse_bool:
            result = parser.to_bool( value )
            self.assertEqual( result, expected )
