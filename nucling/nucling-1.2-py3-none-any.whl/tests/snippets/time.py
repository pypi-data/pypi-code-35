import time
import unittest

from datetime import datetime
from nucling.snippet.time import Timekeeper


class Test_time_kepeer( unittest.TestCase ):
    def setUp( self ):
        self.timekeeper = Timekeeper()

    def test_should_work_with_a_inner_exception( self ):
        with self.assertRaises( Exception ):
            with self.timekeeper:
                raise Exception( 'Explotion!!!' )

    def test_should_have_end_time_when_have_a_inner_exception( self ):
        with self.assertRaises( Exception ):
            with self.timekeeper:
                raise Exception( 'Explotion!!!' )
        self.assertIsInstance( self.timekeeper.end, datetime )

    def test_should_have_a_different_time_when_exit_the_context( self ):
        with self.timekeeper:
            time.sleep( 0.1 )
        self.assertLessEqual( 100, self.timekeeper.delta.microseconds )
