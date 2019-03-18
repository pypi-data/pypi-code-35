import unittest
import copy
from nucling.snippet.pipelines import (
    Pipeline, Pipeline_manager, Transform_keys_camel_case_to_snake,
    Remove_nones
)


class Test_pipeline_copy( unittest.TestCase ):
    def setUp( self ):
        self.p = Pipeline()
        self.q = Pipeline()
        self.result = self.p | self.q

    def test_copy_should_create_a_new_array( self ):
        c = copy.copy( self.result )
        self.assertIsNot( c.children, self.result.children )

    def test_copy_should_contain_the_childrens_in_the_same_order( self ):
        c = copy.copy( self.result )
        for pp, p in zip( c.children, self.result.children ):
            self.assertIs( pp, p )


class Test_pipeline_manager( unittest.TestCase ):
    def setUp( self ):
        self.p = Pipeline()
        self.q = Pipeline()
        self.manager = Pipeline_manager()

    def test_append_should_add_to_the_childrens_queue( self ):
        self.manager.append( self.p )
        self.assertIs( self.manager.children[0], self.p )

    def test_or_should_append_pipelines( self ):
        new_manager = self.manager | self.p
        self.assertIs( new_manager.children[0], self.p )

    def test_or_with_a_manager_should_create_a_new_manager( self ):
        manager = Pipeline_manager()
        manager_2 = Pipeline_manager()
        result = manager | manager_2
        self.assertIsNot( result, manager )
        self.assertIsNot( result, manager_2 )

    def test_or_with_a_manager_should_join_both_children_lists( self ):
        manager = Pipeline_manager() | self.p
        manager_2 = Pipeline_manager() | self.q
        result = manager | manager_2
        self.assertIs( result.children[0], self.p )
        self.assertIs( result.children[1], self.q )

    def test_to_dict_should_return_the_dict_with_the_childrens( self ):
        manager = Pipeline() | Pipeline()
        self.assertIsInstance( manager.to_dict(), dict )
        self.assertTrue( manager.to_dict()[ 'children' ] )

    def test_run_should_use_all_childrens_and_pass_the_results( self ):
        result = Transform_keys_camel_case_to_snake().process(
            {
                'HolaWorld': 'hola_world',
                'none': None } )
        result = Remove_nones().process( result )

        pipe = Transform_keys_camel_case_to_snake() | Remove_nones()
        result_2 = pipe.run(
            {
                'HolaWorld': 'hola_world',
                'none': None } )
        self.assertEqual( result_2, result )

    def test_run_should_work_only_sending_the_class( self ):
        result = Transform_keys_camel_case_to_snake().process(
            {
                'HolaWorld': 'hola_world',
                'none': None } )
        result = Remove_nones().process( result )

        pipe = Transform_keys_camel_case_to_snake | Remove_nones
        result_2 = pipe.run(
            {
                'HolaWorld': 'hola_world',
                'none': None } )
        self.assertEqual( result_2, result )
