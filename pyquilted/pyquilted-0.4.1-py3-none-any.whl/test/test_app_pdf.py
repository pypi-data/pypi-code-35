import inspect
import unittest
from pyquilted.pdf_app import PdfApp


class TestAppPdf(unittest.TestCase):
    def test_app_pdf(self):
        app = PdfApp("resume.yml", "dst.yml")

        self.assertTrue(hasattr(app, 'style_options'))
        self.assertTrue(hasattr(app, 'section_options'))
        self.assertTrue(hasattr(app, 'resume_file'))
        self.assertTrue(hasattr(app, 'path'))
        self.assertTrue(inspect.ismethod(app.run))


if __name__ == '__main__':
    unittest.main()
