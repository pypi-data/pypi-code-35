import inspect
import unittest
from pyquilted.builder.resume import ResumeBuilder


class TestResumeBuilder(unittest.TestCase):
    def test_resume_builder(self):
        builder = ResumeBuilder({"key": "value"})

        self.assertTrue(hasattr(builder, 'resume_odict'))
        self.assertTrue(hasattr(builder, 'resume'))
        self.assertTrue(inspect.ismethod(builder.section_map))


if __name__ == '__main__':
    unittest.main()
