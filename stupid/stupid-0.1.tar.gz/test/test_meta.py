from unittest import TestCase
from stupid import StupidMeta

class Test(metaclass=StupidMeta):
    a: int
    b: str

class TestNew(TestCase):
    def test_slots(self):
        self.assertEqual(Test.__slots__, ('a', 'b'))

    def test_inherit(self):
        class Test2(Test):
            c: bool
        self.assertEqual(Test2.__slots__, ('c', 'a', 'b'))

    def test_inherit_multiple(self):
        class A(Test):
            a1: bool
        class B(Test):
            b1: bool

        class C(A, B):
            pass

        self.assertEqual(C.__slots__, ('a1', 'a', 'b', 'b1'))

    def test_inherit_multiple_normalcls(self):
        class A(Test):
            a1: bool
        class B(Test):
            b1: bool

        class C: pass

        class D(A, B, C):
            pass


        self.assertEqual(D.__slots__, ('a1', 'a', 'b', 'b1'))

    def test_inherit_instanceof(self):
        class A(Test):
            pass

        a = A()
        self.assertIsInstance(a, A)
        self.assertIsInstance(a, Test)

    def test_inherit_not_instanceof(self):
        class A(Test):
            pass

        class B: pass

        a = A()
        self.assertNotIsInstance(a, B)
