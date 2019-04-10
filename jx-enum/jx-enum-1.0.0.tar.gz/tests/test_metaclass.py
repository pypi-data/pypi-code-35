import unittest

from six import with_metaclass


class MetaclassTestCase(unittest.TestCase):

    def test(self):

        name = 'mcs name'

        class EnumBaseMeta(type):
            def __new__(mcs, clsname, bases, classdict):
                mcs = super(EnumBaseMeta, mcs).__new__(mcs, clsname, bases, classdict)
                mcs.NAME = name
                return mcs

        class EnumBase(with_metaclass(EnumBaseMeta)):
            pass

        self.assertEqual(name, EnumBase.NAME)
        ins = EnumBase()
        self.assertEqual(name, ins.NAME)



if __name__ == '__main__':
    unittest.main()

