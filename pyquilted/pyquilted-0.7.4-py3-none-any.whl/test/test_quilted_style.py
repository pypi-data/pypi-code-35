import unittest
from pyquilted.quilted.style import Style


class TestStyle(unittest.TestCase):
    def test_style_defaults(self):
        style = Style()
        self.assertEqual(style.page_height, "9in")
        self.assertEqual(style.page_width, "6in")
        self.assertEqual(style.name_color, "#0066cc")
        self.assertEqual(style.font_main, "verdana, arial, sans-serif")
        self.assertEqual(style.font_other, "verdana, arial, sans-serif")
        self.assertEqual(style.font_size, "10pt")

    def test_font_other(self):
        style = Style(font_main="monaco")
        self.assertEqual(style.font_other, "monaco")
        style2 = Style(font_main="monaco", font_other="helvetica")
        self.assertEqual(style2.font_other, "helvetica")


if __name__ == '__main__':
    unittest.main()
