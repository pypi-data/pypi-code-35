import unittest
from nucling.snippet.is_type import is_iter


class Basic_test_is_iter:
    def test_when_is_empty_should_be_true( self ):
        self.assertTrue( is_iter( self.empty ) )

    def test_when_have_something_should_be_true( self ):
        self.assertTrue( is_iter( self.with_numbers ) )


class Test_with_tuple( Basic_test_is_iter, unittest.TestCase ):
    def setUp( self ):
        self.empty = tuple()
        self.with_numbers = tuple( range( 10 ) )


class Test_with_list( Basic_test_is_iter, unittest.TestCase ):
    def setUp( self ):
        self.empty = list()
        self.with_numbers = list( range( 10 ) )


class Test_with_object_no_iter( unittest.TestCase ):
    def test_no_iter_obj_should_be_false( self ):
        self.assertFalse( is_iter( 10 ) )
