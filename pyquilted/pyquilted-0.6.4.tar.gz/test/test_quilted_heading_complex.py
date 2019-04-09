import unittest
from pyquilted.quilted.heading_complex import HeadingComplex


class TestHeadingComplex(unittest.TestCase):
    def test_heading_complex(self):
        heading = HeadingComplex(name='Jon Snow',
                                 adjacent="Python Dev",
                                 primary="Seeking to destroy my enemies",
                                 top_side="Greater Boston",
                                 bottom_side="cocoroutine")
        valid = {
                "heading-complex": {
                    "name": "Jon Snow",
                    "adjacent": "Python Dev",
                    "primary": "Seeking to destroy my enemies",
                    "top_side": "Greater Boston",
                    "bottom_side": "cocoroutine"
                    }
                }
        self.assertEqual(heading.serialize(), valid)


if __name__ == '__main__':
    unittest.main()
