import unittest
from nucling.snippet.pipelines import (
    Pipeline, Pipeline_manager, Transform_keys_camel_case_to_snake,
    Remove_nones,
)


class Pipeline_with_FUN( Pipeline ):
    def FUN( p, x ):
        return x + 15


class Test_pipeline( unittest.TestCase ):
    def setUp( self ):
        self.p = Pipeline()
        self.q = Pipeline()

    def test_when_the_class_dont_have_fun_should_raise_no_implemented( self ):
        with self.assertRaises( NotImplementedError ):
            Pipeline().process( {} )

    def test_when_the_instance_is_assing_fun_should_run_the_function( self ):
        result = Pipeline( fun=lambda x: x + 10 ).process( 10 )
        self.assertEqual( result, 20 )

    def test_when_the_pipiline_have_FUN_should_run_the_function( self ):
        result = Pipeline_with_FUN().process( 40 )
        self.assertEqual( result, 55 )

    def test_when_combine_with_another_thing_should_return_a_manaager( self ):
        result = self.p | self.q
        self.assertIsInstance( result, Pipeline_manager )

    def test_the_new_manager_should_contain_the_pipeline_and_the_other( self ):
        result = self.p | self.q
        self.assertIs( result.children[0], self.p )
        self.assertIs( result.children[1], self.q )

    def test_do_or_to_the_class_should_be_a_manager_with_both_class( self ):
        result = Pipeline | Pipeline
        self.assertIsInstance( result, Pipeline_manager )
        self.assertIsInstance( result.children[0], type )
        self.assertIsInstance( result.children[1], type )


class Test_camel_case( unittest.TestCase ):
    def setUp( self ):
        self.prev_dict = { 'HelloWorld': 'hello_world' }
        self.result_dict = { 'hello_world': 'hello_world' }

    def test_transform_key_to_camel_to_sanke_should_transform_the_keys( self ):
        result = Transform_keys_camel_case_to_snake().process( self.prev_dict )
        self.assertDictEqual( result, self.result_dict )


class Test_remove_nones( unittest.TestCase ):
    def setUp( self ):
        self.prev_dict = { 'nones': None, 'hello_world': 'hello_world' }
        self.result_dict = { 'hello_world': 'hello_world' }

    def test_remove_nones_should_no_return_a_none( self ):
        result = Remove_nones().process(
            { 'day': None, 'month': None, 'year': '100' } )
        result = Remove_nones().process( self.prev_dict )
        self.assertDictEqual( result, self.result_dict )
