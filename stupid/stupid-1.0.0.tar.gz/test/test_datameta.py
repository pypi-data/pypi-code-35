from unittest import TestCase
from stupid import StupidData

class TestDataMeta(TestCase):

    def test_simple(self):
        class Test(StupidData):
            a: int
            b: str

        t = Test(1, 'b')
        self.assertEqual(t.a, 1)
        self.assertEqual(t.b, 'b')

    def test_single_inherit(self):
        class Test(StupidData):
            a: int
            b: str

        class Test2(Test):
            c: int

        t = Test2(1, 2, 'b')
        self.assertEqual(t.c, 1)
        self.assertEqual(t.a, 2)
        self.assertEqual(t.b, 'b')

    def test_multiple_inherit(self):
        class Test(StupidData):
            a: int
            b: str

        class Test2(StupidData):
            c: int
            d: str

        class Test3(Test, Test2):
            pass

        t = Test3(1, 'a', 2, 'b')
        self.assertEqual(t.a, 1)
        self.assertEqual(t.b, 'a')
        self.assertEqual(t.c, 2)
        self.assertEqual(t.d, 'b')

    def test_instance_of(self):
        class Test(StupidData):
            a: int
            b: int

        t = Test(1, 2)
        self.assertIsInstance(t, Test)

    def test_instance_of_inhertied(self):
        class Test(StupidData):
            a: int
            b: int

        class Test2(Test):
            c: int

        t = Test2(1, 2, 3)
        self.assertIsInstance(t, Test)
        self.assertIsInstance(t, Test2)

    def test_instance_of_inhertied_multi(self):
        class Test(StupidData):
            a: int

        class Test2(StupidData):
            b: int

        class Test3(Test, Test2):
            c: int

        t = Test3(1, 2, 3)
        self.assertIsInstance(t, Test)
        self.assertIsInstance(t, Test2)
        self.assertIsInstance(t, Test3)

    def test_default_value(self):
        class Test(StupidData):
            a: int = 99

        self.assertEqual(Test().a, 99)

    def test_default_value_ins(self):
        class Test(StupidData):
            a: int = 99

        self.assertEqual(Test(97).a, 97)

    def test_default_value_inherit(self):
        class Test1(StupidData):
            a: int = 97

        class Test2(StupidData):
            b: str = 'foo'

        class Test3(Test1, Test2): pass

        ins = Test3()
        self.assertEqual(ins.a, 97)
        self.assertEqual(ins.b, 'foo')

    def test_default_value_ins_inherit(self):
        class Test1(StupidData):
            a: int = 97

        class Test2(StupidData):
            b: str = 'foo'

        class Test3(Test1, Test2): pass

        ins = Test3(98, 'bar')
        self.assertEqual(ins.a, 98)
        self.assertEqual(ins.b, 'bar')
