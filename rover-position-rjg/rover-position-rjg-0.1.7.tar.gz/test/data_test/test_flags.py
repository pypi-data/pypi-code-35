import unittest

from rover_position_rjg.data.flags import Flags


class FlagsTest(unittest.TestCase):
    def test_all_false_by_default(self):
        flags = Flags()
        self.assertEqual(0x00, int(flags))

    def test_initial_value_too_small(self):
        with self.assertRaises(ValueError):
            Flags(-1)

    def test_initial_value_too_large(self):
        with self.assertRaises(ValueError):
            Flags(0x1FF)

    def test_can_initialise_with_int(self):
        flags = Flags(0xFF)
        self.assertEqual(0xFF, int(flags))

    def test_set_flags(self):
        flags = Flags()
        flags[0] = flags[1] = flags[2] = flags[3] = True
        self.assertEqual(0x0F, int(flags))

    def test_can_clear_flags(self):
        flags = Flags()
        self.assertFalse(flags[0])
        flags[0] = flags[1] = flags[2] = flags[3] = flags[4] = flags[5] = flags[6] = flags[7] = True
        flags[2] = False
        self.assertEqual(0xFB, int(flags))

    def test_can_get_flags(self):
        flags = Flags()
        self.assertFalse(flags[3])
        flags[3] = True
        self.assertTrue(flags[3])

    def test_index_cannot_be_negative(self):
        flags = Flags()
        with self.assertRaises(IndexError):
            flags[-1] = True
        with self.assertRaises(IndexError):
            a = flags[-1]

    def test_index_too_large(self):
        flags = Flags()
        with self.assertRaises(IndexError):
            flags[8] = True
        with self.assertRaises(IndexError):
            a = flags[8]

    def test_equals(self):
        a = Flags()
        self.assertEqual(a, a)
        b = Flags()
        self.assertEqual(a, b)
        a[0] = True
        self.assertNotEqual(a, b)
        b[0] = True
        self.assertEqual(a, b)

    def test_not_equals_different_type(self):
        flags = Flags()
        self.assertNotEqual(flags, None)
        self.assertNotEqual(None, flags)
        self.assertNotEqual(flags, 1)
        self.assertNotEqual(1, flags)

    def test_str(self):
        a = Flags()
        self.assertEqual('0x00', str(a))
        a[7] = a[4] = a[2] = a[1] = True
        self.assertEqual('0x96', str(a))

    def test_repr(self):
        a = Flags()
        self.assertEqual('0x00', repr(a))
        a[7] = a[4] = a[2] = a[1] = True
        self.assertEqual('0x96', repr(a))

    def test_int(self):
        a = Flags()
        self.assertEqual(0, int(a))
        a[7] = a[4] = a[2] = a[1] = True
        self.assertEqual(150, int(a))
