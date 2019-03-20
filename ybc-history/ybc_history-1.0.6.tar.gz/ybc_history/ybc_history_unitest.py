import unittest
from ybc_history import *


class MyTestCase(unittest.TestCase):
    def test_history(self):
        content = "2010年1月1日，中国－东盟自贸区正式建成。\n2006年1月1日，中国政府废止农业税。\n1998年1月1日，我国与南非建立外交关系。"
        self.assertEqual(content, history_info(1, 1))

    def test_history_info_ParameterTypeError(self):
        with self.assertRaisesRegex(ParameterTypeError,
                                    "^参数类型错误 : 调用history_info方法时，'month'、'day'、'number'、'type'参数类型错误。$"):
            history_info("month", "day", "num", 1)

    def test_history_info_ParameterValueError(self):
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用history_info方法时，'day'、'number'参数不在允许范围内。$"):
            history_info(2, 30, -1)
        with self.assertRaisesRegex(ParameterValueError, "^参数数值错误 : 调用history_info方法时，'month'、'number'参数不在允许范围内。$"):
            history_info(13, 30, -1)


if __name__ == '__main__':
    unittest.main()
