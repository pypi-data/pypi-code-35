from unittest import TestCase

from nucling import donkey


class Test_donkey(TestCase):

    def setUp( self ):
        pass

    def test_key( self ):
        result = donkey.key( 'a', 'b', 'c' )
        expected = 'a__b__c'
        self.assertEqual( result, expected )

    def test_partition( self ):
        expected = [ 'a', 'b', 'c' ]
        result = donkey.partion( 'a__b__c' )
        self.assertEqual( result, expected )

    def test_init( self ):
        expected = 'a'
        result = donkey.init( 'a__b__c' )
        self.assertEqual( result, expected )

    def test_last( self ):
        expected = 'c'
        result = donkey.last( 'a__b__c' )
        self.assertEqual( result, expected )

    def test_get_lvl_1( self ):
        d = {
            'a': 3,
            'b': { 'c': 1 },
            'c': { 'd': { 'f': 10 } },
        }
        expected = 3
        result = donkey.get( 'a', d )
        self.assertEqual( result, expected )

    def test_get_lvl_3( self ):
        d = {
            'a': 3,
            'b': { 'c': 1 },
            'c': { 'd': { 'f': 10 } },
        }
        expected = 10
        result = donkey.get( 'c__d__f', d )
        self.assertEqual( result, expected )

    def test_get_keyerror( self ):
        d = {
            'a': 3,
            'b': { 'c': 1 },
            'c': { 'd': { 'f': 10 } },
        }
        with self.assertRaises( KeyError ):
            donkey.get( 'c__g__f', d )

    def test_set( self ):
        d = {
            'a': 3,
            'b': { 'c': 1 },
            'c': { 'd': { 'f': 10 } },
        }
        expected = 16
        donkey.setter( 'c__d__f', d, 16 )
        result = donkey.get( 'c__d__f', d )
        self.assertEqual( result, expected )

    def test_set_build_dict( self ):
        d = { }
        expected = {
            'c': { 'd': { 'f': 20 } },
        }
        donkey.setter( 'c__d__f', d, 20 )
        self.assertEqual( d, expected )

    def test_inflate( self ):
        expected = { 'a': 10, 'b': { 'c': 30, 'b': 22 } }
        param = { 'a': 10, 'b__c': 30, 'b__b': 22 }
        result = donkey.inflate( param )
        self.assertEqual( result, expected )

    def test_inflate_with_conflics( self ):
        param = { 'a': 10, 'a__c': 30, 'a__b': 22 }
        with self.assertRaises( ValueError ):
            donkey.inflate( param )

    def test_compress( self ):
        param_2 = { 'a': 10, 'b': { 'c': 30, 'b': 22 } }
        param = { 'a': 10, 'c': [ 1, 2, param_2 ], 'b': { 'c': 30, 'b': 22 } }
        expected = {
            'a': 10, 'b__c': 30, 'b__b': 22, 'c': [ 1, 2, param_2 ] }
        result = donkey.compress( param )
        self.assertEqual( result, expected )

    def test_compress_other( self ):
        params = {
            'ssn_trace': {
                'issued': {
                    'date': '1985-01-01T00:00:00', 'state': 'Kansas',
                    'year': 1985
                },
                'ssn': '732672805',
                'is_deceased': False,
                'is_random': False,
                'is_valid': False,
            }
        }
        expected = {
            'ssn_trace__is_deceased': False,
            'ssn_trace__is_random': False,
            'ssn_trace__is_valid': False,
            'ssn_trace__issued__date': '1985-01-01T00:00:00',
            'ssn_trace__issued__state': 'Kansas',
            'ssn_trace__issued__year': 1985,
            'ssn_trace__ssn': '732672805'
        }
        result = donkey.compress( params )
        self.assertEqual( result, expected )
