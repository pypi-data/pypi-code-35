import unittest
from pyquilted.quilted.heading_simple import HeadingSimple


class TestHeadingSimple(unittest.TestCase):
    def test_heading_simple(self):
        heading = HeadingSimple(name='Jon Snow', adjacent="Greater Boston",
                                primary="Python Dev")
        valid = {
                "heading-simple": {
                    "name": "Jon Snow",
                    "adjacent": "Greater Boston",
                    "primary": "Python Dev"
                    }
                }
        self.assertEqual(heading.serialize(), valid)


if __name__ == '__main__':
    unittest.main()
