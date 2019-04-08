from unittest import TestCase
import tempfile, shutil
from faker import Factory as Faker_factory
from chibi.file.snippets import current_dir, cd, join, mkdir
from chibi.file import Chibi_file
from chibi.snippet.dict import (
    keys_to_snake_case, replace_keys, pop_regex, get_regex, rename_keys,
    lower_keys
)


faker = Faker_factory.create()


class Test_keys_to_snake_case( TestCase ):
    def setUp( self ):
        self.d = { 'camelCase': { 'snake_case': { 'PascalCase': '' } } }
        self.expected = {
            'camel_case': { 'snake_case': { 'pascal_case': '' } } }

    def test_should_transform_to_snake_case( self ):
        result = keys_to_snake_case( self.d )
        self.assertEqual( result, self.expected )

class Test_dict(TestCase):

    def setUp( self ):
        pass

    def test_change_keys_dict_simple( self ):
        expected = {
            "new_id": 123
        }
        dict_for_change = {
            "id": 123
        }
        key_for_change = {
            "id": "new_id"
        }
        replace_keys( dict_for_change, key_for_change )
        self.assertEqual( dict_for_change, expected )

    def test_change_keys_list_of_dicts( self ):
        expected = [ {
            "new_id": 123
        } for i in range( 10 ) ]
        dict_for_change = [ {
            "id": 123
        } for i in range( 10 ) ]
        key_for_change = {
            "id": "new_id"
        }
        replace_keys( dict_for_change, key_for_change )
        self.assertEqual( dict_for_change, expected )

    def test_change_keys_dict_with_dicts( self ):
        expected = {
            "new_id": 123,
            "dict": { "bar": "foo" }
        }
        dict_for_change = {
            "id": 123,
            "dict": { "foo": "foo" }
        }
        key_for_change = {
            "id": "new_id",
            "foo": "bar"
        }
        replace_keys( dict_for_change, key_for_change )
        self.assertEqual( dict_for_change, expected )

    def test_change_keys_dict_with_lists( self ):
        expected = {
            "new_id": 123,
            "dict": [ { "bar": "foo" } for i in range( 10 ) ]
        }
        dict_for_change = {
            "id": 123,
            "dict": [ { "foo": "foo" } for i in range( 10 ) ]
        }
        key_for_change = {
            "id": "new_id",
            "foo": "bar"
        }
        replace_keys( dict_for_change, key_for_change )
        self.assertEqual( dict_for_change, expected )

    def test_pop_regex( self ):
        dict_test = {
            "new_id": 123,
            "new_asdf": 234,
            "new_zxcv": 345,
            "new_qwer": 456,
            "stuff": 123
        }
        dict_result_expected = {
            "new_id": 123,
            "new_asdf": 234,
            "new_zxcv": 345,
            "new_qwer": 456,
        }
        dict_expected = {
            "stuff": 123
        }
        result = pop_regex( dict_test, r'new_.*' )
        self.assertEqual( result, dict_result_expected )
        self.assertEqual( dict_test, dict_expected )

    def test_get_regex( self ):
        dict_test = {
            "new_id": 123,
            "new_asdf": 234,
            "new_zxcv": 345,
            "new_qwer": 456,
            "stuff": 123
        }
        dict_result_expected = {
            "new_id": 123,
            "new_asdf": 234,
            "new_zxcv": 345,
            "new_qwer": 456,
        }
        dict_expected = {
            "new_id": 123,
            "new_asdf": 234,
            "new_zxcv": 345,
            "new_qwer": 456,
            "stuff": 123
        }
        result = get_regex( dict_test, r'new_.*' )
        self.assertEqual( result, dict_result_expected )
        self.assertEqual( dict_test, dict_expected )

    def test_rename_keys( self ):
        dict_test = {
            "new_id": 123, "new_asdf": 234, "new_zxcv": 345,
            "new_qwer": 456, "stuff": 123
        }
        dict_result_expected = {
            "id": 123, "asdf": 234, "zxcv": 345,
            "qwer": 456, "stuff": 123
        }
        result = rename_keys(
            dict_test, func=lambda x: x.replace( 'new_', '' ) )
        self.assertEqual( result, dict_result_expected )

    def test_lower_keys( self ):
        dict_test = {
            "ID": 123, "ASDF": 234, "ZXCV": 345,
            "QWER": 456, "STUFF": 123
        }
        dict_result_expected = {
            "id": 123, "asdf": 234, "zxcv": 345,
            "qwer": 456, "stuff": 123
        }
        result = lower_keys( dict_test )
        self.assertEqual( result, dict_result_expected )
