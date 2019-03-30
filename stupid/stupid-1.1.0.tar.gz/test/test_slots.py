from unittest import TestCase
from stupid import Stupid, StupidData

class TestSlots(TestCase):
    def test_slots_created(self):
        for cls in (StupidData, Stupid):
            with self.subTest(cls=cls):
                class Test(cls):
                    pass
                self.assertEqual(Test().__slots__, ())

    def test_slots_no_dict(self):
        for cls in (StupidData, Stupid):
            with self.subTest(cls=cls):
                class Test(cls):
                    pass
                self.assertNotIn('__dict__', dir(Test()))

    def test_slots_crated_from_annotations(self):
        for cls in (StupidData, Stupid):
            with self.subTest(cls=cls):
                class Test(cls):
                    a: int
                    b: str

                self.assertEqual(Test.__slots__, ('a', 'b'))
