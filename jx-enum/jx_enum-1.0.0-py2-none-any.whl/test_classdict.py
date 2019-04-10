import unittest

from six import with_metaclass


class MetaclassTestCase(unittest.TestCase):

    def test_with_prefix_underline_then_error(self):

        class EnumBaseMeta(type):
            def __new__(mcs, clsname, bases, classdict):
                mcs = super(EnumBaseMeta, mcs).__new__(mcs, clsname, bases, classdict)
                d = {}
                d.update((n, v) for n, v in classdict.items())
                type.__setattr__(mcs, 'NAME_TO_VALUE', d)
                return mcs

        class EnumBase(with_metaclass(EnumBaseMeta)):
            NAME_TO_VALUE = {'a': 1}

        class EnumA(EnumBase):
            AA = 1

        self.assertIn('__module__', EnumBase.NAME_TO_VALUE)
        self.assertIn('__module__', EnumA.NAME_TO_VALUE)

    def test_without_prefix_underline_then_ok(self):
        """
        We don't want __module__
        """

        class EnumBaseMeta(type):
            def __new__(mcs, clsname, bases, classdict):
                mcs = super(EnumBaseMeta, mcs).__new__(mcs, clsname, bases, classdict)
                d = {}
                d.update((n, v) for n, v in classdict.items() if not n.startswith('__'))
                type.__setattr__(mcs, 'NAME_TO_VALUE', d)
                return mcs

        class EnumBase(with_metaclass(EnumBaseMeta)):
            NAME_TO_VALUE = {'a': 1}

        class EnumA(EnumBase):
            AA = 1

        self.assertDictEqual(EnumBase.NAME_TO_VALUE, {'NAME_TO_VALUE': {'a': 1}})
        self.assertDictEqual(EnumA.NAME_TO_VALUE, {'AA': 1})

    def test_recursive_update_attribute(self):

        class EnumBaseMeta(type):
            def __new__(mcs, clsname, bases, classdict):
                mcs = super(EnumBaseMeta, mcs).__new__(mcs, clsname, bases, classdict)
                d = {}
                for base in reversed(mcs.__bases__):
                    if hasattr(base, 'NAME_TO_VALUE'):
                        d.update(base.NAME_TO_VALUE)
                d.update((n, v) for n, v in classdict.items() if not n.startswith('__') and not isinstance(v, dict))
                type.__setattr__(mcs, 'NAME_TO_VALUE', d)
                return mcs

        class EnumBase(with_metaclass(EnumBaseMeta)):
            NAME_TO_VALUE = {}

        class EnumA(EnumBase):
            AA = 1
            CC = 3

        class EnumB(EnumA):
            BB = 2
            CC = 3

        self.assertDictEqual(EnumB.NAME_TO_VALUE, {'AA': 1, 'BB': 2, 'CC': 3})


if __name__ == '__main__':
    unittest.main()

