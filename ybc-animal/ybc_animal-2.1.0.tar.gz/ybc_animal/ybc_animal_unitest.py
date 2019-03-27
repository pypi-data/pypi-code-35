import unittest
from .ybc_animal import *

path_pic = os.path.join(os.path.split(os.path.abspath(__file__))[0], 'test.jpg')


class MyTestCase(unittest.TestCase):
    def test_what(self):
        self.assertEqual('狗', what(path_pic))

    def test_breed(self):
        self.assertEqual('金毛狗', breed(path_pic))

    def test_desc(self):
        self.assertIsNotNone(desc(path_pic))

    def test_desc_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用desc方法时，'filename'参数类型错误。$"):
            desc(1)

    def test_desc_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用desc方法时，'filename'参数不在允许范围内。$"):
            desc('')

    def test_what_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用what方法时，'filename'参数类型错误。$"):
            what(1)

    def test_what_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用what方法时，'filename'参数不在允许范围内。$"):
            what('')

    def test_breed_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError, "^参数类型错误 : 调用breed方法时，'filename'参数类型错误。$"):
            breed(1)

    def test_breed_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用breed方法时，'filename'参数不在允许范围内。$"):
            breed('')


if __name__ == '__main__':
    unittest.main()
