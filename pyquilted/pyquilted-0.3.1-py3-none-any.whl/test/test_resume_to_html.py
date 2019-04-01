import inspect
import unittest
from pyquilted.resume_to_html import ResumeToHtml


class MockResume(ResumeToHtml):
    def __init__(self):
        pass


class TestResumeToHtml(unittest.TestCase):
    def test_resume_to_html(self):
        mock = MockResume()
        self.assertTrue(inspect.ismethod(mock.resume_to_html))


if __name__ == '__main__':
    unittest.main()
