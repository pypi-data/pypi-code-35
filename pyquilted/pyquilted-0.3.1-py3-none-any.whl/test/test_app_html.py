import inspect
import unittest
from pyquilted.html_app import HtmlApp


class TestAppHtml(unittest.TestCase):
    def test_app_html(self):
        app = HtmlApp("resume.yml", "dst.yml")

        self.assertTrue(hasattr(app, 'style_options'))
        self.assertTrue(hasattr(app, 'section_options'))
        self.assertTrue(hasattr(app, 'resume_file'))
        self.assertTrue(hasattr(app, 'path'))
        self.assertTrue(inspect.ismethod(app.run))


if __name__ == '__main__':
    unittest.main()
